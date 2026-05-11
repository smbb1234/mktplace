from __future__ import annotations

from fastapi import APIRouter, HTTPException
from typing import List

from src.backend.startup import get_catalog
from src.backend.services.recommendations.comparison_service import assemble_comparison

router = APIRouter(prefix="/comparisons", tags=["comparisons"])


@router.post("/assemble")
def assemble(vehicle_ids: List[str]):
    catalog = get_catalog()
    if not catalog:
        raise HTTPException(status_code=503, detail="Catalog not loaded")
    vehicle_dicts = []
    for vid in vehicle_ids:
        v = catalog.get_vehicle(vid)
        if not v:
            raise HTTPException(status_code=404, detail=f"Vehicle {vid} not found")
        p = catalog.get_pricing(vid)
        d = v.model_dump()
        d["pricing"] = p.model_dump() if p else {}
        vehicle_dicts.append(d)
    return assemble_comparison(vehicle_dicts)
