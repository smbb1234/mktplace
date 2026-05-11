from __future__ import annotations

from typing import Dict, List, Optional
from pathlib import Path

from src.backend.models.inventory import InventoryVehicle, VehiclePricing
from src.backend.services.inventory.csv_loader import load_inventory
from src.backend.services.inventory.image_resolver import resolve_image


class InventoryCatalog:
    def __init__(self, csv_path: Optional[Path | str] = None):
        self.csv_path = csv_path
        self.vehicles: Dict[str, InventoryVehicle] = {}
        self.pricing: Dict[str, VehiclePricing] = {}

    def load(self) -> None:
        vehicles, pricing = load_inventory(self.csv_path)
        self.vehicles = {v.vehicle_id: v for v in vehicles}
        self.pricing = pricing

    def refresh(self) -> None:
        self.load()

    def list_vehicle_ids(self) -> List[str]:
        return list(self.vehicles.keys())

    def get_vehicle(self, vehicle_id: str) -> Optional[InventoryVehicle]:
        return self.vehicles.get(vehicle_id)

    def get_pricing(self, vehicle_id: str) -> Optional[VehiclePricing]:
        return self.pricing.get(vehicle_id)

    def resolve_vehicle_image(self, vehicle_id: str) -> tuple[str, bool]:
        v = self.get_vehicle(vehicle_id)
        image_path = None
        if v:
            # If CSV included an explicit image_path attribute, use it
            image_path = getattr(v, "image_path", None)
        p, is_placeholder = resolve_image(vehicle_id=vehicle_id, image_path=image_path)
        return str(p), is_placeholder

    def filter(self, *, budget_monthly_max: Optional[float] = None, fuel_type: Optional[str] = None,
               transmission: Optional[str] = None, body_type: Optional[str] = None, limit: int = 50) -> List[InventoryVehicle]:
        results: List[InventoryVehicle] = []
        for vid, v in self.vehicles.items():
            p = self.get_pricing(vid)
            if budget_monthly_max is not None and p is not None and p.monthly_from_gbp is not None:
                if p.monthly_from_gbp > budget_monthly_max:
                    continue
            if fuel_type and v.fuel_type and v.fuel_type.lower() != fuel_type.lower():
                continue
            if transmission and v.transmission and v.transmission.lower() != transmission.lower():
                continue
            if body_type and v.body_type and v.body_type.lower() != body_type.lower():
                continue
            results.append(v)
            if len(results) >= limit:
                break
        return results


# module-level default catalog for quick access
_default_catalog: Optional[InventoryCatalog] = None


def get_default_catalog(csv_path: Optional[Path | str] = None) -> InventoryCatalog:
    global _default_catalog
    if _default_catalog is None:
        # Create a temporary catalog and attempt to load it. Only cache the
        # catalog if loading succeeds to avoid returning a partially
        # initialized catalog when load fails (e.g., missing CSV).
        catalog = InventoryCatalog(csv_path=csv_path)
        catalog.load()
        _default_catalog = catalog
    return _default_catalog


if __name__ == "__main__":
    c = get_default_catalog()
    print("Loaded vehicles:", len(c.list_vehicle_ids()))
