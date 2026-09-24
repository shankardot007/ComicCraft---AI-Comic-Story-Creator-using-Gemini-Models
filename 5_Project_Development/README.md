# Phase 5: Project Development

The **working source code** for **ComicCraft** lives in the **repository root** (the `5_Project_Development` folder holds these development-phase notes, while the code sits at the top level for simple daily coding in VS Code).

## Core Components (repo root)

| File | Purpose |
| :--- | :--- |
| `app/main.py` | FastAPI app entry point, static mount, Jinja2 templates |
| `app/config.py` | `.env` loading, model configuration, directory setup |
| `app/schemas.py` | Pydantic request/response models |
| `app/routes/api.py` | API endpoints (`/api/health`, `/api/generate-story`, `/api/generate-image`, `/api/export-pdf`) |
| `app/services/ai.py` | Gemini client, JSON parsing, retry/backoff |
| `app/services/story_engine.py` | `build_outline()` (Flash) → `build_story()` (Pro, auto Flash fallback) |
| `app/services/image_engine.py` | `generate_panel_image()`: Stable Diffusion → Gemini image → placeholder |
| `app/services/pdf_engine.py` | `build_pdf()`: FPDF multi-page comic export |
| `templates/index.html` | Web UI form + comic preview |
| `static/js/app.js` | Fetch flow, panel rendering, download |
| `static/css/style.css` | Styling |

## Setup Instructions

```bash
# From the repository root
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env                # then edit GOOGLE_API_KEY
```

`.env`:

```
GOOGLE_API_KEY=your_google_gemini_key
HF_API_KEY=                     # optional — Gemini image model is used when empty
GEMINI_FLASH_MODEL=gemini-3.6-flash
GEMINI_PRO_MODEL=gemini-3.6-flash
GEMINI_IMAGE_MODEL=gemini-2.5-flash-image
SD_MODEL=stabilityai/stable-diffusion-xl-base-1.0
```

## Run Instructions

```bash
uvicorn app.main:app --reload   # from the repo root
```

Open **http://127.0.0.1:8000** — Story Inputs → ⚡ Generate Comic → ⬇ Download PDF.