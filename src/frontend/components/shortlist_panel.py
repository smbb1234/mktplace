from __future__ import annotations

import streamlit as st
from src.frontend.api_client.client import BackendClient

client = BackendClient()


def shortlist_panel():
    st.sidebar.header("Shortlist")
    session_id = st.session_state.get("session_id")
    if not session_id:
        st.sidebar.info("Start a session to use shortlist")
        return
    if st.sidebar.button("View shortlist"):
        try:
            r = client.shortlist_list(session_id)
            st.sidebar.write(r)
        except Exception:
            st.sidebar.error("Failed to load shortlist")
            return
