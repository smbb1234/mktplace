from __future__ import annotations

import streamlit as st


def get_session_id() -> str:
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = "sess-" + str(len(st.session_state))
    return st.session_state["session_id"]


def set_preferences(prefs: dict) -> None:
    st.session_state.setdefault("preferences", {}).update(prefs)


def get_preferences() -> dict:
    return st.session_state.get("preferences", {})
