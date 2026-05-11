from __future__ import annotations

from src.backend.api.image_paths import recommendation_image_path
from src.shared.config.constants import DEFAULT_PLACEHOLDER_IMAGE_PATH, PROJECT_ROOT


def test_recommendation_api_image_path_is_project_relative():
    assert recommendation_image_path(PROJECT_ROOT / "assets" / "vehicles" / "CAR-2026-0001.png") == (
        "assets/vehicles/CAR-2026-0001.png"
    )


def test_recommendation_api_placeholder_path_is_project_relative_from_constant():
    assert recommendation_image_path(DEFAULT_PLACEHOLDER_IMAGE_PATH) == "assets/placeholder.png"


def test_recommendation_api_image_url_is_preserved():
    image_url = "https://example.com/car.png"
    assert recommendation_image_path(image_url) == image_url
