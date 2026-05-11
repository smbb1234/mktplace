from __future__ import annotations

from typing import Dict, List

# In-memory shortlist per session for demo
_SHORTLISTS: Dict[str, List[str]] = {}


def add_to_shortlist(session_id: str, vehicle_id: str) -> List[str]:
    shortlist = _SHORTLISTS.setdefault(session_id, [])
    if vehicle_id not in shortlist:
        shortlist.append(vehicle_id)
    return shortlist


def remove_from_shortlist(session_id: str, vehicle_id: str) -> List[str]:
    shortlist = _SHORTLISTS.setdefault(session_id, [])
    if vehicle_id in shortlist:
        shortlist.remove(vehicle_id)
    return shortlist


def list_shortlist(session_id: str) -> List[str]:
    return _SHORTLISTS.get(session_id, [])
