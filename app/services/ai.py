import json
import logging
import re
import time

from google import genai
from google.genai import types

from app import config

logger = logging.getLogger("comiccraft.ai")

_client: genai.Client | None = None

RETRYABLE = ("503", "429", "500", "RESOURCE_EXHAUSTED", "UNAVAILABLE")


class AIError(Exception):
    pass


def get_client() -> genai.Client:
    global _client
    if not config.GOOGLE_API_KEY:
        raise AIError("GOOGLE_API_KEY is not set. Add it to your .env file.")
    if _client is None:
        _client = genai.Client(api_key=config.GOOGLE_API_KEY)
    return _client


def parse_json(text: str):
    if not text:
        raise AIError("Empty response from Gemini.")
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise AIError("Could not parse AI response as JSON.")
        try:
            return json.loads(cleaned[start : end + 1])
        except json.JSONDecodeError as exc:
            raise AIError("Could not parse AI response as JSON.") from exc


def generate_json(model: str, prompt: str, temperature: float = 0.8):
    last_error: Exception | None = None
    for attempt in range(5):
        try:
            response = get_client().models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    response_mime_type="application/json",
                    max_output_tokens=8192,
                ),
            )
            return parse_json(response.text or "")
        except AIError:
            raise
        except Exception as exc:
            last_error = exc
            text = str(exc)
            retry = any(token in text for token in RETRYABLE)
            logger.warning(
                "Gemini call failed (attempt %s, retry=%s): %s",
                attempt + 1, retry, exc,
            )
            if not retry or attempt == 4:
                break
            time.sleep(5 * (attempt + 1))
    raise AIError(f"Gemini request failed: {last_error}")