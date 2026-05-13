from __future__ import annotations

import streamlit as st
from uuid import uuid4


RESET_SESSION_STATE_KEYS = (
    "session_id",
    "chat_messages",
    "preferences",
    "selected_vehicle",
    "selected_vehicle_obj",
    "finance_term",
    "finance_deposit",
)


def reset_session_state(keys: tuple[str, ...] | list[str] | None = None) -> None:
    """Remove session-scoped UI state so a new buying conversation can start."""
    for key in keys or RESET_SESSION_STATE_KEYS:
        st.session_state.pop(key, None)


def get_session_id() -> str:
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = f"sess-{uuid4().hex[:12]}"
    return st.session_state["session_id"]


def set_preferences(prefs: dict) -> None:
    st.session_state.setdefault("preferences", {}).update(prefs)
    if prefs.get("deposit_gbp") is not None:
        st.session_state["finance_deposit"] = prefs["deposit_gbp"]
    if prefs.get("term_months") is not None:
        st.session_state["finance_term"] = prefs["term_months"]


def get_preferences() -> dict:
    return st.session_state.get("preferences", {})
