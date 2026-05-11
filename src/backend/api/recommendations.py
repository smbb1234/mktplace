from __future__ import annotations

from fastapi import APIRouter, HTTPException
from typing import Optional

from src.backend.startup import get_catalog
from src.backend.services.ai.conversation_orchestrator import get_preferences
from src.backend.services.recommendations.filtering import apply_filters
from src.backend.services.recommendations.ranker import rank_vehicles
from src.backend.services.recommendations.explanations import build_explanation

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/from_session")
def recommendations_from_session(session_id: Optional[str] = None, limit: int = 3):
    catalog = get_catalog()
    if not catalog:
        raise HTTPException(status_code=503, detail="Catalog not loaded")
    prefs = get_preferences(session_id or "")
    vehicles = [v.model_dump() for v in catalog.vehicles.values()]
    pricing = {k: v.model_dump() for k, v in catalog.pricing.items()}
    candidates = apply_filters(vehicles, pricing, prefs)
    ranked = rank_vehicles(candidates, pricing, prefs, limit=limit)
    # attach explanations
    for r in ranked:
        vid = r.get("vehicle_id")
        r["explanation"] = build_explanation(prefs, r, pricing.get(vid, {}))
    return ranked
