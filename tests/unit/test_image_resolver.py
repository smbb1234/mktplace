from src.backend.services.inventory.image_resolver import resolve_image
from src.shared.config.constants import DEFAULT_PLACEHOLDER_IMAGE_PATH


def test_resolve_image_placeholder_for_missing():
    path, is_placeholder = resolve_image(vehicle_id="NON_EXISTENT_VEHICLE")
    assert path == DEFAULT_PLACEHOLDER_IMAGE_PATH
    assert is_placeholder is True
