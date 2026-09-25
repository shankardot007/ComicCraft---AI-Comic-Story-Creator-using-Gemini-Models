# ComicCraft - AI Comic Story Creator using Gemini Models

## Overview

ComicCraft is a web-based application that uses AI to generate personalized comic book stories and illustrations based on user-provided prompts. Built with FastAPI and integrated with Google's Gemini AI models (along with optional Stable Diffusion), ComicCraft automates the creative process of generating storylines, dialogues, and vivid comic-style imagery.

Users provide a story prompt, main character, setting, tone, and art style. The system generates a panel-by-panel storyline with corresponding illustrations, lets users preview the comic on a web interface, and export the full comic as a downloadable PDF (using FPDF).

- **Backend:** Python, FastAPI, Uvicorn
- **AI Core:** Google Gemini (Flash for outlines, Pro for narration/dialogue, image model for illustrations)
- **Image (optional):** Stable Diffusion via Hugging Face Inference API
- **Frontend:** HTML, CSS, JavaScript, Jinja2
- **PDF Export:** FPDF2
- **Config:** python-dotenv (.env)

> Only a Google Gemini API key is required. Hugging Face is optional; images fall back to Gemini's image model automatically.

---

## Phase 1: Brainstorming & Ideation

### Problem Statement

Traditional comic book creation requires significant artistic skill, storyboarding experience, and time. Writers and visual creators often lack the tools to turn a simple text idea into a panel-by-panel visual narrative quickly and cost-effectively.

### Proposed Solution

ComicCraft is an AI-powered comic story generator that uses Google Gemini models to transform a simple text prompt into a complete panel-based comic - structured outlines, engaging narration, character dialogue, and comic-style illustrations - delivered in an interactive web interface with downloadable PDF export.

### Core Features

- Text-to-Comic pipeline powered by Google Gemini (Flash for outlines, Pro for narration/dialogue).
- Panel-by-panel story engine with configurable panel counts (3-10).
- AI illustration generation via Gemini's image model, with optional Stable Diffusion (Hugging Face).
- Interactive preview grid with captions, narration, and dialogue bubbles.
- PDF export using FPDF for saving, printing, and sharing.

### Brainstorming Notes

- Story prompt, character, setting, tone, and art style are the core user inputs.
- Free-tier Gemini quota is limited (~20 requests/day per model) - keeping API call count low per comic (2 calls) is a priority.
- No Hugging Face key is required; Gemini's image model is used as the automatic fallback.

---

## Phase 2: Requirement Analysis

### Functional Requirements

- **User Input:** Accept story idea, characters, setting, tone, art style, and panel count.
- **Outline Engine:** Use Gemini Flash to generate a structured multi-panel comic outline with a title and logline.
- **Story Engine:** Use Gemini Pro (with automatic Flash fallback) to expand each outline panel into narration and character dialogue, plus a rich image prompt.
- **Visual Generator:** Generate comic-style panel images from each image prompt (Gemini image model, or Stable Diffusion via Hugging Face Inference API when HF_API_KEY is set).
- **Preview Interface:** Responsive web UI showing the comic panel-by-panel with thumbnails, narration, and dialogue.
- **Export System:** Compile the full comic into a downloadable PDF with FPDF.

### Non-Functional Requirements

- **Response Time:** Story generation completes quickly; panel images stream in progressively.
- **Resilience:** Graceful fallback chain (Stable Diffusion -> Gemini image model -> placeholder) so the comic and PDF always export.
- **Usability:** Mobile-friendly, single-page web interface with clear progress feedback.
- **Security:** API keys loaded from .env, never hardcoded; .env excluded from version control.
- **Validation:** Pydantic-validated request/response models on every endpoint.

### Tech Stack & APIs

| Concern | Technology |
| :--- | :--- |
| AI Core | Google Gemini (gemini-3.6-flash, image model) |
| Image (optional) | Hugging Face Inference API / Stable Diffusion XL |
| Backend | Python + FastAPI + Uvicorn |
| Frontend | HTML, CSS, vanilla JavaScript (Jinja2 rendering) |
| PDF | FPDF2 |
| Config | Python dotenv (.env) |
| Env/Deploy | VS Code (debug + tasks), venv, requirements.txt |

### API Endpoints

| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| GET | /api/health | Key/model status |
| POST | /api/generate-story | Outline + full story script |
| POST | /api/generate-image | Panel illustration |
| POST | /api/export-pdf | Build downloadable comic PDF |

---

## Phase 3: Project Design

### System Architecture Flow

```
User Input (story idea, characters, tone, art style)
        |
        v
Frontend UI (index.html + app.js)
        |  POST /api/generate-story
        v
FastAPI Backend  --->  Gemini Flash  --->  Panel Outline (JSON)
        |                 |
        |                 v
        |         Gemini Pro / Flash  --->  Full Story Script (JSON)
        |                 |
        |      POST /api/generate-image  (loop per panel)
        |                 v
        |         Gemini Image Model  <---  Stable Diffusion (optional HF)
        |                 |
        v                 v
Comic Preview Grid (comic panels, narration, dialogue)
        |  POST /api/export-pdf
        v
FPDF  --->  Downloadable Comic PDF
```

### Backend Structure

```
ComicCraft/  (repo root)
|-- app/
|   |-- main.py              # FastAPI app, Jinja2 templates, static mount
|   |-- config.py            # .env loading, model config, path, key checks
|   |-- schemas.py           # Pydantic models (StoryRequest, Panel, Comic, ...)
|   |-- routes/api.py        # /api/health, /generate-story, /generate-image, /export-pdf
|   `-- services/
|       |-- ai.py            # Gemini client + JSON parsing + retry/backoff
|       |-- story_engine.py  # Outline -> narration/dialogue -> Comic
|       |-- image_engine.py  # Stable Diffusion -> Gemini image -> placeholder
|       `-- pdf_engine.py    # FPDF comic export
|-- templates/index.html     # Web UI
|-- static/                  # CSS, JS, generated panels, PDFs
|-- requirements.txt
|-- .env.example
`-- README.md
```

### Output Schema (JSON)

```json
{
  "title": "The Fallen Light of Whispering Pines",
  "logline": "A brave fox must return a fallen star before the forest darkens forever.",
  "panels": [
    {
      "id": 1,
      "scene": "A silver fox stands on a mossy rock at the edge of the woods at dawn.",
      "narration": "Morning mist curled through the pines as Finn set out.",
      "dialogues": [
        { "speaker": "Finn", "line": "If the star is out there, I will find it." }
      ],
      "image_prompt": "silver fox on mossy rock, enchanted forest at dawn, anime comic panel...",
      "image_url": "/static/generated/panel_ab12cd34ef56.png"
    }
  ]
}
```

### Design Decisions

- Gemini Flash does outlines (fast, cheap); Pro does the full script; the script step auto-falls back to Flash on quota blocks.
- Image generation is a separate API loop so each panel's progress can be shown and failures degrade gracefully.
- .env at the project root is loaded once via python-dotenv; models are fully configurable.

---

## Phase 4: Project Planning

### Work Breakdown Structure (WBS)

| Week | Activities | Deliverables |
| :--- | :--- | :--- |
| Week 1 | Requirements gathering, setup of venv + FastAPI skeleton, .env config, model selection (Gemini Flash/Pro, image model). | Project skeleton, requirements.txt, config.py |
| Week 2 | Core functionality: Gemini outline + story JSON parsing, retry/backoff, image fallback chain, PDF engine. | services/ modules, Pydantic schemas |
| Week 3 | FastAPI routing (/api/*), Jinja2 home page, preview grid UI, progress + download flow. | routes/api.py, templates, frontend |
| Week 4 | E2E testing, error handling, VS Code workspace (debug/tasks), documentation, GitHub release. | Tests, README.md, phase docs, GitHub repo |

### Team Member Responsibilities

- **AI Integration & Backend:** Gemini prompt engineering, JSON parsing, retry logic, FastAPI routes.
- **Frontend & Layout Engine:** Web UI, comic grid layout, panel rendering, progress indicators.
- **Testing & Documentation:** Test execution, repository maintenance, phase-wise documentation.

### Setup Plan

```bash
python -m venv .venv
pip install -r requirements.txt
# configure keys in .env
uvicorn app.main:app --reload
```

### Risk & Mitigation

- **Gemini quota (429):** fallback to alternative flash model pool; keep panel count low; inform users about daily caps.
- **Image quota = 0 on free tier:** placeholder + PDF still export; HF key or paid tier recommended for real art.
- **Missing .env:** friendly banner + /api/health report which keys are missing.

---

## Phase 5: Project Development

This section covers the working source code of ComicCraft (located in the repository root).

### Core Components

| File | Purpose |
| :--- | :--- |
| app/main.py | FastAPI app entry point, static mount, Jinja2 templates |
| app/config.py | .env loading, model configuration, directory setup |
| app/schemas.py | Pydantic request/response models |
| app/routes/api.py | API endpoints (/api/health, /api/generate-story, /api/generate-image, /api/export-pdf) |
| app/services/ai.py | Gemini client, JSON parsing, retry/backoff |
| app/services/story_engine.py | build_outline() (Flash) -> build_story() (Pro, auto Flash fallback) |
| app/services/image_engine.py | generate_panel_image(): Stable Diffusion -> Gemini image -> placeholder |
| app/services/pdf_engine.py | build_pdf(): FPDF multi-page comic export |
| templates/index.html | Web UI form + comic preview |
| static/js/app.js | Fetch flow, panel rendering, download |
| static/css/style.css | Styling |

### Setup Instructions

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env                # then edit GOOGLE_API_KEY
```

.env:

```
GOOGLE_API_KEY=your_google_gemini_key
HF_API_KEY=                        # optional - Gemini image model is used when empty
GEMINI_FLASH_MODEL=gemini-3.6-flash
GEMINI_PRO_MODEL=gemini-3.6-flash
GEMINI_IMAGE_MODEL=gemini-2.5-flash-image
SD_MODEL=stabilityai/stable-diffusion-xl-base-1.0
```

### Run Instructions

```bash
uvicorn app.main:app --reload   # from the repository root
```

Open http://127.0.0.1:8000 - Story Inputs -> Generate Comic -> Download PDF.

---

## Phase 6: Project Testing

### Test Execution Plan

| Test Case ID | Feature | Test Scenario | Expected Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| TC01 | Health Endpoint | GET /api/health | Returns key/model status and missing list | Passed |
| TC02 | Story Generation | Post valid StoryRequest (3 panels) | Returns Comic JSON - title, logline, 3 panels with narration, dialogue, image prompt | Passed |
| TC03 | No HF Key | Post /api/generate-image with HF_API_KEY empty | No hard error - falls back to Gemini image model or placeholder; image_url returned | Passed |
| TC04 | Gemini Retries | API returns 503/429 | Automatic retry with backoff, then user-friendly error | Passed |
| TC05 | PDF Export | Post a Comic to /api/export-pdf | FileResponse with application/pdf and valid PDF bytes | Passed |
| TC06 | Home Page | GET / | 200, renders form + status dots | Passed |
| TC07 | Input Validation | Invalid payload (short idea / bad types) | Pydantic 422 with clear detail | Passed |
| TC08 | Missing Google Key | /api/generate-story without GOOGLE_API_KEY | 500 with "not configured" message | Passed |

### Test Notes

- Live API calls must respect Google free-tier quota (~20 requests/day per model). Retries are capped at 5 with exponential backoff.
- The image-generation chain is the primary resilience test: Stable Diffusion -> Gemini image -> placeholder always returns 200 with a usable image_url.
- All endpoints verified with FastAPI's TestClient and the project venv.

---

## Phase 7: Project Documentation

### Project Summary

ComicCraft is an AI-driven comic story creator built with FastAPI and Google Gemini models. It turns a simple text prompt - plus character, setting, tone, and art-style preferences - into a complete panel-based comic: structured outline, narration, dialogue, comic-style illustrations, and a downloadable PDF. Optional Stable Diffusion integration is used for images when a Hugging Face key is provided; otherwise the Gemini image model handles illustration, with a graceful placeholder fallback so the comic and PDF always export.

### User Guide

1. Launch the app (uvicorn app.main:app --reload from the repository root).
2. Open http://127.0.0.1:8000.
3. Enter your story idea (required), add optional characters, choose setting, tone, art style, and panel count (3-10).
4. Click "Generate Comic" - watch panels render live with progress feedback.
5. Review the comic in the preview grid (title, narration, dialogue bubbles, scene descriptions).
6. Click "Download PDF" to save the full comic as a PDF.

### Developer Notes

- Models are configurable via .env: GEMINI_FLASH_MODEL, GEMINI_PRO_MODEL, GEMINI_IMAGE_MODEL, SD_MODEL.
- The story step automatically falls back from Pro to Flash when quota blocks it.
- Only GOOGLE_API_KEY is required; HF_API_KEY is optional.
- Generate with fewer panels (3-4) to conserve daily free-tier API quota.
- API reference: interactive /docs (Swagger UI).

---

## Phase 8: Project Demonstration

### Demonstration Deliverables

- **Project Name:** ComicCraft - AI Comic Story Creator using Gemini Models
- **Demo Video:** public Google Drive / YouTube link (stored in 8_Project_Demonstration/DEMO_LINK.txt).
- **Live App:** run locally with uvicorn app.main:app --reload and open http://127.0.0.1:8000.

### Demo Video Outline

1. Introduction: What ComicCraft is and the problem it solves (AI-assisted storyboarding).
2. Problem & Solution: Why creating comics is hard - and how Gemini automates outline, script, art, and PDF export.
3. System Walkthrough: Live demo of entering a story prompt, selecting tone/art style, and generating panels.
4. Final Output: Review the rendered comic panels with narration/dialogue and export the PDF.
5. Architecture Overview: Brief look at FastAPI routes, services, and the Gemini integration.

---

## Conclusion

ComicCraft demonstrates the creative potential of AI-driven comic generation. By combining Gemini Flash and Gemini Pro for storytelling and AI image generation for comic-style illustration, the application enables users to transform simple prompts into complete, visually engaging comic narratives.

The project provides an end-to-end experience - from personalized story outline generation, full narration, image creation, to exporting the final comic as a downloadable PDF - all within an intuitive web interface. ComicCraft simplifies comic creation for non-artists, storytellers, and hobbyists, offering a seamless blend of imagination and AI assistance.