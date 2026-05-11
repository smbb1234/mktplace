from __future__ import annotations

from typing import Dict, Any


def build_explanation(prefs: Dict[str, Any], vehicle: Dict[str, Any], pricing: Dict[str, Any]) -> Dict[str, Any]:
    reason = []
    if prefs.get("fuel_type") and vehicle.get("fuel_type"):
        if prefs.get("fuel_type").lower() == vehicle.get("fuel_type").lower():
            reason.append("Matches preferred fuel type")
    if pricing and pricing.get("monthly_from_gbp"):
        reason.append(f"Estimated monthly £{pricing.get('monthly_from_gbp')}")
    return {"explanation": "; ".join(reason) if reason else "Basic match"}
