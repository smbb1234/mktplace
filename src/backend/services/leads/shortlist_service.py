from __future__ import annotations

from typing import Dict, List

# In-memory shortlist per session for demo
_SHORTLISTS: Dict[str, List[str]] = {}


def add_to_shortlist(session_id: str, vehicle_id: str) -> List[str]:
    l = _SHORTLISTS.setdefault(session_id, [])
    if vehicle_id not in l:
        l.append(vehicle_id)
    return l


def remove_from_shortlist(session_id: str, vehicle_id: str) -> List[str]:
    l = _SHORTLISTS.setdefault(session_id, [])
    if vehicle_id in l:
        l.remove(vehicle_id)
    return l


def list_shortlist(session_id: str) -> List[str]:
    return _SHORTLISTS.get(session_id, [])
