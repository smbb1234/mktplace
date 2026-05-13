from __future__ import annotations

from typing import Dict, Any
import time

# Minimal in-memory orchestrator for sessions (demo-only)
_SESSIONS: Dict[str, Dict[str, Any]] = {}


def create_or_get_session(session_id: str | None) -> Dict[str, Any]:
    if session_id and session_id in _SESSIONS:
        return _SESSIONS[session_id]
    # create new
    sid = session_id or "sess-" + str(len(_SESSIONS) + 1)
    _SESSIONS[sid] = {
        "session_id": sid,
        "preferences": {},
        "messages": [],
        "last_question_key": None,
        "last_question_asked_at": 0.0,
    }
    return _SESSIONS[sid]


def add_message(session_id: str, message: str) -> None:
    s = create_or_get_session(session_id)
    s["messages"].append(message)


def update_preferences(session_id: str, prefs: Dict[str, Any]) -> None:
    s = create_or_get_session(session_id)
    s["preferences"].update(prefs)


def get_preferences(session_id: str) -> Dict[str, Any]:
    s = create_or_get_session(session_id)
    return s.get("preferences", {})


def set_last_question_key(session_id: str, key: str | None) -> None:
    s = create_or_get_session(session_id)
    s["last_question_key"] = key


def get_last_question_key(session_id: str) -> str | None:
    s = create_or_get_session(session_id)
    return s.get("last_question_key")


def set_last_question_asked_at(session_id: str, timestamp: float | None = None) -> None:
    s = create_or_get_session(session_id)
    s["last_question_asked_at"] = timestamp if timestamp is not None else time.time()


def get_last_question_asked_at(session_id: str) -> float:
    s = create_or_get_session(session_id)
    return float(s.get("last_question_asked_at", 0.0))
