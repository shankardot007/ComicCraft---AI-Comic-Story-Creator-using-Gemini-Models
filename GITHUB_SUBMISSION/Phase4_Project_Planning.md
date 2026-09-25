# Phase 4: Project Planning

## Work Breakdown Structure (WBS)

| Week | Activities | Deliverables |
| :--- | :--- | :--- |
| Week 1 | Requirements gathering, setup of venv + FastAPI skeleton, .env config, model selection (Gemini Flash/Pro, image model). | Project skeleton, requirements.txt, config.py |
| Week 2 | Core functionality: Gemini outline + story JSON parsing, retry/backoff, image fallback chain, PDF engine. | services/ modules, Pydantic schemas |
| Week 3 | FastAPI routing (/api/*), Jinja2 home page, preview grid UI, progress + download flow. | routes/api.py, templates, frontend |
| Week 4 | E2E testing, error handling, VS Code workspace (debug/tasks), documentation, GitHub release. | Tests, README.md, phase docs, GitHub repo |

## Team Member Responsibilities

- **AI Integration & Backend:** Gemini prompt engineering, JSON parsing, retry logic, FastAPI routes.
- **Frontend & Layout Engine:** Web UI, comic grid layout, panel rendering, progress indicators.
- **Testing & Documentation:** Test execution, repository maintenance, phase-wise documentation.

## Setup Plan

```bash
python -m venv .venv
pip install -r requirements.txt
# configure keys in .env
uvicorn app.main:app --reload
```

## Risk & Mitigation

- **Gemini quota (429):** fallback to alternative flash model pool; keep panel count low; inform users about daily caps.
- **Image quota = 0 on free tier:** placeholder + PDF still export; HF key or paid tier recommended for real art.
- **Missing .env:** friendly banner + /api/health report which keys are missing.