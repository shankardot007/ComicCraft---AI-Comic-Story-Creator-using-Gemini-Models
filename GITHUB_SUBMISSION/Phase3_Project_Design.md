# Phase 3: Project Design

## System Architecture Flow

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

## Backend Structure

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

## Output Schema (JSON)

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

## Design Decisions

- Gemini Flash does outlines (fast, cheap); Pro does the full script; the script step auto-falls back to Flash on quota blocks.
- Image generation is a separate API loop so each panel's progress can be shown and failures degrade gracefully.
- .env at the project root is loaded once via python-dotenv; models are fully configurable.