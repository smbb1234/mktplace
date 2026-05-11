from __future__ import annotations

import streamlit as st
from src.frontend.state.session_state import get_session_id, set_preferences
from src.frontend.api_client.client import BackendClient

client = BackendClient()


def chat_panel():
    st.sidebar.header("Assistant")
    session_id = get_session_id()
    txt = st.sidebar.text_input("Say something to the assistant")
    if st.sidebar.button("Send") and txt:
        resp = client.post_chat({"session_id": session_id, "message": txt})
        # update local state preferences
        prefs = {k: v for k, v in resp.items() if v is not None}
        set_preferences(prefs)
        st.sidebar.write("Preferences updated:")
        st.sidebar.json(prefs)
