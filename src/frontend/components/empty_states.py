from __future__ import annotations

import streamlit as st


def show_no_results_hint():
    st.warning("No results found — try relaxing budget or other filters.")


def show_loading_placeholder():
    st.info("Loading results — please wait...")
