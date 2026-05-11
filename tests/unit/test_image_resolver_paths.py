from pathlib import Path
from src.backend.services.inventory.image_resolver import resolve_image


def test_resolve_image_with_explicit_path(tmp_path: Path):
    f = tmp_path / "img.jpg"
    f.write_bytes(b"fakejpeg")
    path, is_placeholder = resolve_image(image_path=str(f))
    assert Path(path).exists()
    assert is_placeholder is False


def test_resolve_image_fallback_to_placeholder():
    path, is_placeholder = resolve_image(vehicle_id="NO_SUCH_ID")
    assert is_placeholder is True
