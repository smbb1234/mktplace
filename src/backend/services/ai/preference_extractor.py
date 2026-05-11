from __future__ import annotations

from typing import Dict, Any
import re


def extract_preferences_from_text(text: str) -> Dict[str, Any]:
    """Simple rule-based extractor for demo purposes."""
    prefs: Dict[str, Any] = {}
    # budget: look for numbers with £ or £ sign or 'per month'
    m = re.search(r"(£|GBP)?\s?(\d{2,6})(?:\s?per month|/month| pcm)?", text)
    if m:
        try:
            prefs["monthly_budget"] = float(m.group(2))
        except Exception:
            pass
    # fuel
    if "diesel" in text.lower():
        prefs["fuel_type"] = "Diesel"
    if "petrol" in text.lower():
        prefs["fuel_type"] = "Petrol"
    if "electric" in text.lower():
        prefs["fuel_type"] = "Electric"
    # transmission
    if "auto" in text.lower() or "automatic" in text.lower():
        prefs["transmission"] = "Automatic"
    if "manual" in text.lower():
        prefs["transmission"] = "Manual"
    # intent
    if "buy" in text.lower() or "looking" in text.lower():
        prefs["intent"] = "purchase"
    return prefs
