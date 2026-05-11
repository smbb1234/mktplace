from __future__ import annotations

import streamlit as st


def show_error(msg: str):
    st.error(msg)


def show_warning(msg: str):
    st.warning(msg)
