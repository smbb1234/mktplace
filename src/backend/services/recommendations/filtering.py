from __future__ import annotations

from typing import List, Dict, Any


def apply_filters(vehicles: List[Dict[str, Any]], pricing: Dict[str, Dict[str, Any]], prefs: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for v in vehicles:
        vid = v.get("vehicle_id")
        p = pricing.get(vid, {})
        # budget
        if prefs.get("monthly_budget") and p.get("monthly_from_gbp"):
            if p.get("monthly_from_gbp") > prefs.get("monthly_budget"):
                continue
        # fuel
        if prefs.get("fuel_type") and v.get("fuel_type"):
            if v.get("fuel_type").lower() != prefs.get("fuel_type").lower():
                continue
        # transmission
        if prefs.get("transmission") and v.get("transmission"):
            if v.get("transmission").lower() != prefs.get("transmission").lower():
                continue
        out.append(v)
    return out
