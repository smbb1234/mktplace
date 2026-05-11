from __future__ import annotations

from typing import Dict

from src.shared.config.constants import MATCH_SCORE_WEIGHTS


def compute_match_score(prefs: Dict[str, any], vehicle: dict, pricing: dict) -> float:
    # Simple weighted score: budget fit and intent presence
    score = 0.0
    weights = MATCH_SCORE_WEIGHTS
    # budget
    try:
        budget = prefs.get("monthly_budget", None)
        monthly = pricing.get("monthly_from_gbp") if pricing else None
        if budget and monthly:
            # perfect fit gives full budget weight
            fit = max(0.0, 1.0 - abs(monthly - budget) / max(budget, monthly))
            score += fit * weights.get("budget", 0)
    except Exception:
        pass
    # intent
    if prefs.get("intent"):
        score += 1.0 * weights.get("intent", 0)
    # fallback small value
    return float(score * 100)
