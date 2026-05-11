from __future__ import annotations

from fastapi import APIRouter, HTTPException
from typing import Optional

from src.backend.startup import get_catalog
from src.backend.services.finance.estimator import estimate_monthly

router = APIRouter(prefix="/finance", tags=["finance"])


@router.get("/estimate")
def estimate(vehicle_id: str, deposit: Optional[float] = 0.0, term_months: Optional[int] = 36):
    catalog = get_catalog()
    if not catalog:
        raise HTTPException(status_code=503, detail="Catalog not loaded")
    pricing = catalog.get_pricing(vehicle_id)
    if not pricing:
        raise HTTPException(status_code=404, detail="Pricing not found for vehicle")
    list_price = pricing.list_price_gbp or 0.0
    result = estimate_monthly(list_price=list_price, deposit=deposit or 0.0, term_months=term_months, apr_percent=pricing.apr_percent or 6.0)
    return {"estimate": result, "disclaimer": "All finance figures are examples only and subject to approval."}
