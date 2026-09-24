import logging
import uuid

from huggingface_hub import InferenceClient
from PIL import Image, ImageDraw

from app import config
from app.schemas import ImageRequest, ImageResponse

logger = logging.getLogger("comiccraft.images")

_client: InferenceClient | None = None
_plain_client: InferenceClient | None = None


def get_client() -> InferenceClient:
    global _client
    if not config.HF_API_KEY:
        raise RuntimeError("HF_API_KEY is not set. Add it to your .env file.")
    if _client is None:
        _client = InferenceClient(api_key=config.HF_API_KEY)
    return _client


def _gemini_image(prompt: str):
    from google import genai
    from google.genai import types

    if not config.GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY required for image fallback.")
    client = genai.Client(api_key=config.GOOGLE_API_KEY)
    response = client.models.generate_content(
        model=config.GEMINI_IMAGE_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )
    parts = response.candidates[0].content.parts if response.candidates else []
    for part in parts:
        data = getattr(getattr(part, "inline_data", None), "data", None)
        if data:
            import io

            return Image.open(io.BytesIO(data))
    raise RuntimeError("Gemini image model returned no image data.")


def build_image_prompt(req: ImageRequest) -> str:
    parts = [req.image_prompt.rstrip(".")]
    if req.characters:
        chars = "; ".join(
            f"{c.name} ({c.description})" if c.description else c.name
            for c in req.characters
        )
        parts.append(f"characters: {chars}")
    parts.append(f"{req.art_style} comic book panel illustration")
    if req.tone:
        parts.append(f"{req.tone} mood")
    parts.append("bold ink outlines, dynamic composition, vivid colors, high detail")
    parts.append("no text, no lettering, no speech bubbles, no captions, no watermark")
    return ". ".join(parts)


def _placeholder(title: str, detail: str) -> Image.Image:
    img = Image.new("RGB", (1024, 1024), "#16213e")
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, 984, 984], outline="#e94560", width=8)
    draw.text((70, 80), "IMAGE UNAVAILABLE", fill="#e94560")
    draw.text((70, 120), title[:60], fill="#ffffff")
    wrapped = detail[:400]
    y = 180
    for line in [wrapped[i : i + 50] for i in range(0, len(wrapped), 50)]:
        draw.text((70, y), line, fill="#a8b2d1")
        y += 24
    return img


def generate_panel_image(req: ImageRequest) -> ImageResponse:
    filename = f"panel_{uuid.uuid4().hex[:12]}.png"
    path = config.GENERATED_DIR / filename
    url = f"/static/generated/{filename}"
    prompt = build_image_prompt(req)

    if config.HF_API_KEY:
        try:
            image = get_client().text_to_image(prompt, model=config.SD_MODEL)
            image.save(path)
            return ImageResponse(panel_id=req.panel_id, image_url=url, ok=True)
        except Exception as hf_exc:
            logger.warning("Stable Diffusion failed for panel %s: %s", req.panel_id, hf_exc)
    else:
        hf_exc = RuntimeError("HF_API_KEY not set — skipping Stable Diffusion, using Gemini image model.")

    source = "gemini"
    try:
        image = _gemini_image(prompt)
        image.convert("RGB").save(path)
        return ImageResponse(panel_id=req.panel_id, image_url=url, ok=True)
    except Exception as gem_exc:
        logger.warning("Gemini image fallback failed for panel %s: %s", req.panel_id, gem_exc)
        source = "placeholder"
        detail = (
            f"Panel {req.panel_id}: image generation unavailable. "
            f"Hugging Face error: {_short(hf_exc)}. Gemini fallback: {_short(gem_exc)}. "
            "Set GOOGLE_API_KEY (or HF_API_KEY with the Inference permission) to generate real images."
        )
    _placeholder(f"Panel {req.panel_id}", f"Image source: {source}").save(path)
    return ImageResponse(
        panel_id=req.panel_id,
        image_url=url,
        ok=False,
        detail=detail if source == "placeholder" else "",
    )


def _short(exc: Exception) -> str:
    msg = str(exc)
    return msg[:160]