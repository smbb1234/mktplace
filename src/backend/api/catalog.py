from __future__ import annotations

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException

from src.backend.startup import get_catalog

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/", response_model=List[dict])
def list_catalog(
    budget_monthly_max: Optional[float] = Query(None),
    fuel_type: Optional[str] = Query(None),
    transmission: Optional[str] = Query(None),
    body_type: Optional[str] = Query(None),
    limit: int = Query(50),
):
    catalog = get_catalog()
    if catalog is None:
        raise HTTPException(status_code=503, detail="Catalog not loaded")
    vehicles = catalog.filter(
        budget_monthly_max=budget_monthly_max,
        fuel_type=fuel_type,
        transmission=transmission,
        body_type=body_type,
        limit=limit,
    )
    return [v.model_dump() for v in vehicles]


@router.get("/{vehicle_id}", response_model=dict)
def get_vehicle(vehicle_id: str):
    catalog = get_catalog()
    if catalog is None:
        raise HTTPException(status_code=503, detail="Catalog not loaded")
    v = catalog.get_vehicle(vehicle_id)
    if v is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    pricing = catalog.get_pricing(vehicle_id)
    return {"vehicle": v.model_dump(), "pricing": (pricing.model_dump() if pricing else None)}
