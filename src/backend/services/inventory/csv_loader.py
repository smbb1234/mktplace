from __future__ import annotations

import csv
import json
from typing import Dict, List, Tuple
from pathlib import Path

from pydantic import ValidationError

from src.backend.models.inventory import InventoryVehicle, VehiclePricing
from src.shared.config.settings import get_settings


def _parse_json_cell(cell: str):
    if not cell:
        return None
    try:
        return json.loads(cell)
    except json.JSONDecodeError:
        # Some CSVs may double-quote JSON; try a fallback
        try:
            return json.loads(cell.replace('""', '"'))
        except Exception:
            return None


def load_inventory(csv_path: Path | str = None) -> Tuple[List[InventoryVehicle], Dict[str, VehiclePricing]]:
    settings = get_settings()
    path = Path(csv_path) if csv_path else Path(settings.inventory_csv_path)
    vehicles: List[InventoryVehicle] = []
    pricing: Dict[str, VehiclePricing] = {}

    if not path.exists():
        raise FileNotFoundError(f"Inventory CSV not found: {path}")

    with path.open("r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for i, row in enumerate(reader, start=1):
            inv_cell = row.get("Car Inventory Data") or row.get("inventory")
            price_cell = row.get("Pricing Details") or row.get("pricing")

            inv_obj = _parse_json_cell(inv_cell) if inv_cell else None
            price_obj = _parse_json_cell(price_cell) if price_cell else None

            if inv_obj:
                try:
                    v = InventoryVehicle(**inv_obj)
                    vehicles.append(v)
                except ValidationError:
                    # skip invalid rows but continue
                    continue

            if price_obj:
                try:
                    p = VehiclePricing(**price_obj)
                    pricing[p.vehicle_id] = p
                except ValidationError:
                    continue

    return vehicles, pricing


if __name__ == "__main__":
    # quick run for local validation
    try:
        v, p = load_inventory()
        print(f"Loaded {len(v)} vehicles and {len(p)} pricing entries")
        if v:
            print("First vehicle:", v[0].display_title())
    except Exception as e:
        print("Error loading inventory:", e)
