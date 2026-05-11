from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from src.shared.config.constants import DEFAULT_PLACEHOLDER_IMAGE_PATH, PROJECT_ROOT


def _is_url(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https"}


def recommendation_image_path(path: str | Path | None) -> str:
    """Return recommendation image values as URLs or project-relative paths."""
    if not path:
        path = DEFAULT_PLACEHOLDER_IMAGE_PATH

    raw = str(path)
    if _is_url(raw):
        return raw

    image_path = Path(raw)
    if image_path.is_absolute():
        try:
            return image_path.relative_to(PROJECT_ROOT).as_posix()
        except ValueError:
            return image_path.as_posix()

    return image_path.as_posix().lstrip("./")
