# Phase 7: Project Documentation

## Project Summary

ComicCraft is an AI-driven comic story creator built with FastAPI and Google Gemini models. It turns a simple text prompt - plus character, setting, tone, and art-style preferences - into a complete panel-based comic: structured outline, narration, dialogue, comic-style illustrations, and a downloadable PDF. Optional Stable Diffusion integration is used for images when a Hugging Face key is provided; otherwise the Gemini image model handles illustration, with a graceful placeholder fallback so the comic and PDF always export.

## User Guide

1. Launch the app (uvicorn app.main:app --reload from the repository root).
2. Open http://127.0.0.1:8000.
3. Enter your story idea (required), add optional characters, choose setting, tone, art style, and panel count (3-10).
4. Click "Generate Comic" - watch panels render live with progress feedback.
5. Review the comic in the preview grid (title, narration, dialogue bubbles, scene descriptions).
6. Click "Download PDF" to save the full comic as a PDF.

## Developer Notes

- Models are configurable via .env: GEMINI_FLASH_MODEL, GEMINI_PRO_MODEL, GEMINI_IMAGE_MODEL, SD_MODEL.
- The story step automatically falls back from Pro to Flash when quota blocks it.
- Only GOOGLE_API_KEY is required; HF_API_KEY is optional.
- Generate with fewer panels (3-4) to conserve daily free-tier API quota.
- API reference: interactive /docs (Swagger UI).