import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import config
from app.routes.api import router as api_router
from app.services.ai import AIError

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="ComicCraft",
    description="AI Comic Story Creator powered by Google Gemini and Stable Diffusion",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(config.BASE_DIR / "static")), name="static")
app.include_router(api_router)

templates = Jinja2Templates(directory=str(config.BASE_DIR / "templates"))


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"missing": config.missing_keys()})


@app.exception_handler(AIError)
async def ai_error_handler(request: Request, exc: AIError):
    return JSONResponse(status_code=502, content={"detail": str(exc)})