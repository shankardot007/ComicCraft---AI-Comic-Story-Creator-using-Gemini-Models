import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
HF_API_KEY = os.getenv("HF_API_KEY", "").strip()

GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.6-flash")
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3.6-flash")
GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
SD_MODEL = os.getenv("SD_MODEL", "stabilityai/stable-diffusion-xl-base-1.0")

GENERATED_DIR = BASE_DIR / "static" / "generated"
DOWNLOADS_DIR = BASE_DIR / "static" / "downloads"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)


def missing_keys() -> list[str]:
    missing = []
    if not GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")
    return missing