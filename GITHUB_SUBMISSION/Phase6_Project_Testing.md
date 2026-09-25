# Phase 6: Project Testing

## Test Execution Plan

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

## Test Notes

- Live API calls must respect Google free-tier quota (~20 requests/day per model). Retries are capped at 5 with exponential backoff.
- The image-generation chain is the primary resilience test: Stable Diffusion -> Gemini image -> placeholder always returns 200 with a usable image_url.
- All endpoints verified with FastAPI's TestClient and the project venv.