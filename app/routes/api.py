import logging
import re

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app import config
from app.schemas import Comic, HealthResponse, ImageRequest, ImageResponse, StoryRequest
from app.services.ai import AIError
from app.services.image_engine import generate_panel_image
from app.services.pdf_engine import build_pdf
from app.services.story_engine import generate_comic

logger = logging.getLogger("comiccraft.api")

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        google_key=bool(config.GOOGLE_API_KEY),
        hf_key=bool(config.HF_API_KEY),
        flash_model=config.GEMINI_FLASH_MODEL,
        pro_model=config.GEMINI_PRO_MODEL,
        sd_model=config.SD_MODEL,
        missing=config.missing_keys(),
    )


@router.post("/generate-story", response_model=Comic)
def generate_story(req: StoryRequest) -> Comic:
    missing = config.missing_keys()
    if "GOOGLE_API_KEY" in missing:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY is not configured on the server.")
    try:
        return generate_comic(req)
    except AIError as exc:
        logger.error("Story generation failed: %s", exc)
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected story generation error")
        raise HTTPException(status_code=500, detail=f"Story generation failed: {exc}") from exc


@router.post("/generate-image", response_model=ImageResponse)
def generate_image(req: ImageRequest) -> ImageResponse:
    if "GOOGLE_API_KEY" in config.missing_keys():
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY is not configured on the server.")
    try:
        return generate_panel_image(req)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected image generation error")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {exc}") from exc


@router.post("/export-pdf")
def export_pdf(comic: Comic) -> FileResponse:
    if not comic.panels:
        raise HTTPException(status_code=400, detail="Comic has no panels to export.")
    try:
        path = build_pdf(comic)
    except Exception as exc:
        logger.exception("PDF export failed")
        raise HTTPException(status_code=500, detail=f"PDF export failed: {exc}") from exc
    slug = re.sub(r"[^A-Za-z0-9]+", "-", comic.title).strip("-").lower() or "comic"
    return FileResponse(path, media_type="application/pdf", filename=f"{slug}.pdf")