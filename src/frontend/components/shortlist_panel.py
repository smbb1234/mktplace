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
            r = client.get(f"{client.base}/shortlist/list", params={"session_id": session_id})
        except Exception:
            st.sidebar.error("Failed to load shortlist")
            return
        st.sidebar.write(r.json())
