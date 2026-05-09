from __future__ import annotations

import glob
from pathlib import Path
from typing import Tuple

from src.shared.config.constants import DEFAULT_PLACEHOLDER_IMAGE_PATH


_ASSETS_VEHICLES_DIR = Path("assets") / "vehicles"


def resolve_image(vehicle_id: str | None = None, image_path: str | None = None) -> Tuple[Path, bool]:
    """Resolve the best local image for a vehicle.

    Returns (path, is_placeholder)
    """
    # If explicit image path provided and exists, use it
    if image_path:
        p = Path(image_path)
        if p.exists():
            return p, False

    # If vehicle-specific file exists in assets/vehicles, use the first match
    if vehicle_id:
        pattern = str(_ASSETS_VEHICLES_DIR / f"{vehicle_id}.*")
        matches = glob.glob(pattern)
        if matches:
            return Path(matches[0]), False

    # Fallback to placeholder
    return DEFAULT_PLACEHOLDER_IMAGE_PATH, True


if __name__ == "__main__":
    p, is_placeholder = resolve_image("CAR-UNKNOWN")
    print(p, is_placeholder)
