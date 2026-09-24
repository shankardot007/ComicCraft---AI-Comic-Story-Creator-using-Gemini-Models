from typing import Optional

from pydantic import BaseModel, Field


class Character(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    description: str = Field(default="", max_length=400)


class StoryRequest(BaseModel):
    idea: str = Field(min_length=5, max_length=3000)
    characters: list[Character] = Field(default_factory=list, max_length=8)
    setting: str = Field(default="", max_length=400)
    tone: str = Field(default="Wholesome", max_length=60)
    art_style: str = Field(default="American Comic", max_length=60)
    panel_count: int = Field(default=6, ge=3, le=10)


class Dialogue(BaseModel):
    speaker: str = Field(max_length=60)
    line: str = Field(max_length=500)


class Panel(BaseModel):
    id: int
    scene: str = Field(default="")
    narration: str = Field(default="")
    dialogues: list[Dialogue] = Field(default_factory=list)
    image_prompt: str = Field(default="")
    image_url: Optional[str] = None


class Comic(BaseModel):
    title: str
    logline: str = ""
    panels: list[Panel]


class ImageRequest(BaseModel):
    panel_id: int = Field(ge=1, le=20)
    image_prompt: str = Field(min_length=3, max_length=2000)
    art_style: str = Field(default="American Comic", max_length=60)
    characters: list[Character] = Field(default_factory=list, max_length=8)
    tone: str = Field(default="", max_length=60)


class ImageResponse(BaseModel):
    panel_id: int
    image_url: str
    ok: bool = True
    detail: str = ""


class HealthResponse(BaseModel):
    google_key: bool
    hf_key: bool
    flash_model: str
    pro_model: str
    sd_model: str
    missing: list[str]