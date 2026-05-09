"""Application settings for the AI Car Buying Assistant MVP."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.shared.config.constants import (
    DEFAULT_INVENTORY_CSV_PATH,
    DEFAULT_PLACEHOLDER_IMAGE_PATH,
)


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    database_url: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/mktplace",
        alias="DATABASE_URL",
    )
    inventory_csv_path: Path = Field(
        default=DEFAULT_INVENTORY_CSV_PATH,
        alias="INVENTORY_CSV_PATH",
    )
    placeholder_image_path: Path = Field(
        default=DEFAULT_PLACEHOLDER_IMAGE_PATH,
        alias="PLACEHOLDER_IMAGE_PATH",
    )
    chroma_enabled: bool = Field(default=False, alias="CHROMA_ENABLED")
    chroma_db_path: Path = Field(default=Path("vector_db"), alias="CHROMA_DB_PATH")
    fastapi_host: str = Field(default="127.0.0.1", alias="FASTAPI_HOST")
    fastapi_port: int = Field(default=8000, alias="FASTAPI_PORT")
    streamlit_host: str = Field(default="127.0.0.1", alias="STREAMLIT_HOST")
    streamlit_port: int = Field(default=8501, alias="STREAMLIT_PORT")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()