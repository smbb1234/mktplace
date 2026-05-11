from __future__ import annotations

from typing import Dict, Any


def generate_customer_summary(session_prefs: Dict[str, Any], messages: list) -> Dict[str, Any]:
    return {
        "purpose": session_prefs.get("intent"),
        "budget": session_prefs.get("monthly_budget"),
        "preferences": session_prefs,
        "messages": messages[-10:],
    }
