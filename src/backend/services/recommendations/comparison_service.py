from __future__ import annotations

from typing import List, Dict, Any


def assemble_comparison(vehicle_dicts: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Build a simple comparison object for 2-3 vehicles
    keys = ["vehicle_id", "make", "model", "list_price_gbp", "monthly_from_gbp", "mileage", "fuel_type", "transmission"]
    items = []
    for v in vehicle_dicts:
        item = {k: v.get(k) or v.get("pricing", {}).get(k) for k in keys}
        items.append(item)
    return {"items": items}
