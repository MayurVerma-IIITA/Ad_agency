from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_env: str = Field(default="development", alias="APP_ENV")
    asset_root: Path = Field(default=Path("./data/assets"), alias="ASSET_ROOT")
    comfyui_base_url: str = Field(default="http://127.0.0.1:8188", alias="COMFYUI_BASE_URL")
    video_provider: str = Field(default="wan", alias="VIDEO_PROVIDER")
    wan_workflow_path: Path | None = Field(default=None, alias="WAN_WORKFLOW_PATH")


@lru_cache
def get_settings() -> Settings:
    return Settings()
