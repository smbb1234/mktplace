from __future__ import annotations

import streamlit as st

from src.frontend.state.session_state import reset_session_state

HEADER_TITLE = "AI Car Buying Assistant ✨"
HEADER_SUBTITLE = "Your personal car expert"


def render_header() -> None:
    """Render the application header and session reset action."""
    with st.container():
        left, right = st.columns([1, 0.22])
        with left:
            st.markdown(
                f"""
                <header class="glass-card title-card">
                  <div class="title-row">
                    <div class="title-copy">
                      <h1>{HEADER_TITLE}</h1>
                      <p>{HEADER_SUBTITLE}</p>
                    </div>
                  </div>
                </header>
                """,
                unsafe_allow_html=True,
            )
        with right:
            if st.button("New Session", use_container_width=True):
                reset_session_state()
                st.rerun()
