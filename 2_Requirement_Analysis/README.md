# Phase 2: Requirement Analysis

## Functional Requirements

- **User Input:** Accept story idea, characters, setting, tone, art style, and panel count.
- **Outline Engine:** Use Gemini Flash to generate a structured multi-panel comic outline with a title and logline.
- **Story Engine:** Use Gemini Pro (with automatic Flash fallback) to expand each outline panel into narration and character dialogue, plus a rich image prompt.
- **Visual Generator:** Generate comic-style panel images from each image prompt (Gemini image model, or Stable Diffusion via Hugging Face Inference API when `HF_API_KEY` is set).
- **Preview Interface:** Responsive web UI showing the comic panel-by-panel with thumbnails, narration, and dialogue.
- **Export System:** Compile the full comic into a downloadable PDF with FPDF.

## Non-Functional Requirements

- **Response Time:** Story generation should complete in well under a minute on the free tier; panel images stream in progressively.
- **Resilience:** Graceful fallback chain (Stable Diffusion → Gemini image → placeholder) so the comic and PDF always export.
- **Usability:** Mobile-friendly, single-page web interface with clear progress feedback.
- **Security:** API keys read from `.env`, never hardcoded; `.env` excluded from version control.
- **Validation:** Pydantic-validated request/response models on every endpoint.

## Tech Stack & APIs

| Concern | Technology |
| :--- | :--- |
| **AI Core** | Google Gemini (`gemini-3.6-flash`, image model) |
| **Image (optional)** | Hugging Face Inference API / Stable Diffusion XL |
| **Backend** | Python + FastAPI + Uvicorn |
| **Frontend** | HTML, CSS, vanilla JavaScript (Jinja2 rendering) |
| **PDF** | FPDF2 |
| **Config** | Python `dotenv` (`.env`) |
| **Env/Deploy** | VS Code (debug + tasks), venv, `requirements.txt` |

## API Endpoints

| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| GET | `/api/health` | Key/model status |
| POST | `/api/generate-story` | Outline + full story script |
| POST | `/api/generate-image` | Panel illustration |
| POST | `/api/export-pdf` | Build downloadable comic PDF |