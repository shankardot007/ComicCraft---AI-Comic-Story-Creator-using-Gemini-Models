import logging

from app import config
from app.schemas import Comic, StoryRequest
from app.services.ai import AIError, generate_json

logger = logging.getLogger(__name__)


def _characters_block(req: StoryRequest) -> str:
    if not req.characters:
        return "- Invent 2-3 memorable characters with distinct looks and personalities."
    lines = [f"- {c.name}: {c.description or 'supporting character'}" for c in req.characters]
    return "\n".join(lines)


def _validate_panels(panels: list, expected: int, label: str) -> list[dict]:
    if not isinstance(panels, list) or not panels:
        raise AIError(f"{label} returned no panels.")
    cleaned = [p for p in panels if isinstance(p, dict) and p.get("scene")]
    if not cleaned:
        raise AIError(f"{label} returned invalid panels.")
    return cleaned[:expected] if len(cleaned) >= expected else cleaned


def build_outline(req: StoryRequest) -> dict:
    prompt = f"""You are a veteran comic book editor. Design a structured outline for a comic.

STORY IDEA:
{req.idea}

CHARACTERS:
{_characters_block(req)}

SETTING: {req.setting or "choose a fitting setting"}
TONE: {req.tone}
NUMBER OF PANELS: {req.panel_count}

Requirements:
- Each panel is ONE self-contained visual moment that can be drawn as a single image.
- Build a clear arc across panels: setup, escalation, climax, resolution.
- Be concrete: name places, actions, weather, time of day.

Return ONLY valid JSON in this exact shape:
{{
  "title": "short catchy comic title",
  "logline": "one sentence summary",
  "panels": [
    {{"beat": "story beat name", "scene": "detailed visual description of this panel's moment"}}
  ]
}}
The "panels" array must contain exactly {req.panel_count} objects."""
    data = generate_json(config.GEMINI_FLASH_MODEL, prompt, temperature=0.9)
    panels = _validate_panels(data.get("panels", []), req.panel_count, "Outline")
    return {
        "title": str(data.get("title") or "Untitled Comic").strip(),
        "logline": str(data.get("logline") or "").strip(),
        "panels": panels,
    }


def _generate_story_data(req: StoryRequest, prompt: str) -> dict:
    try:
        return generate_json(config.GEMINI_PRO_MODEL, prompt, temperature=0.9)
    except AIError as exc:
        if "limits" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc) or "quota" in str(exc).lower():
            logger.warning("Pro model quota blocked, falling back to Flash: %s", exc)
            return generate_json(config.GEMINI_FLASH_MODEL, prompt, temperature=0.9)
        raise


def build_story(req: StoryRequest, outline: dict) -> Comic:
    outline_text = "\n".join(
        f"{i}. [{p.get('beat', 'beat')}] {p['scene']}"
        for i, p in enumerate(outline["panels"], start=1)
    )
    prompt = f"""You are a professional comic book writer. Expand this outline into a complete comic script.

TITLE: {outline["title"]}
LOGLINE: {outline["logline"]}

OUTLINE PANELS:
{outline_text}

CHARACTERS:
{_characters_block(req)}

SETTING: {req.setting or "as implied by the outline"}
TONE: {req.tone}
ART STYLE: {req.art_style}

Rules:
- Keep the same panel order and count as the outline.
- narration: 1-2 sentence caption box text, vivid and concise.
- dialogues: 1-3 short, punchy lines per panel; speaker must be a character name or "Narrator".
- image_prompt: a rich text-to-image prompt for this panel describing characters' appearance, pose, action, environment, composition, lighting and mood. Never include words for text inside the image.
- Stay consistent with character names, setting and tone.

Return ONLY valid JSON in this exact shape:
{{
  "title": "...",
  "logline": "...",
  "panels": [
    {{
      "id": 1,
      "scene": "what happens visually",
      "narration": "caption text",
      "dialogues": [{{"speaker": "Name", "line": "dialogue"}}],
      "image_prompt": "detailed visual prompt"
    }}
  ]
}}"""
    data = _generate_story_data(req, prompt)
    raw_panels = data.get("panels", [])
    if not isinstance(raw_panels, list) or not raw_panels:
        raise AIError("Story generation returned no panels.")

    panels = []
    for i, p in enumerate(raw_panels[: req.panel_count], start=1):
        if not isinstance(p, dict):
            continue
        dialogues = []
        for d in p.get("dialogues", []) or []:
            if not isinstance(d, dict):
                continue
            speaker = str(d.get("speaker", "")).strip() or "Narrator"
            line = str(d.get("line", "")).strip()
            if line:
                dialogues.append({"speaker": speaker[:60], "line": line[:500]})
        scene = str(p.get("scene", "")).strip()
        image_prompt = str(p.get("image_prompt", "")).strip() or scene
        panels.append(
            {
                "id": i,
                "scene": scene,
                "narration": str(p.get("narration", "")).strip(),
                "dialogues": dialogues,
                "image_prompt": image_prompt,
                "image_url": None,
            }
        )

    if not panels:
        raise AIError("Story generation produced no valid panels.")

    return Comic(
        title=str(data.get("title") or outline["title"]).strip(),
        logline=str(data.get("logline") or outline["logline"]).strip(),
        panels=panels,
    )


def generate_comic(req: StoryRequest) -> Comic:
    outline = build_outline(req)
    return build_story(req, outline)