from __future__ import annotations

import streamlit as st
from src.frontend.api_client.client import BackendClient

client = BackendClient()


def finance_panel(vehicle_id: str | None = None):
    st.sidebar.header("Finance")
    vid = vehicle_id or st.sidebar.text_input("Vehicle ID for estimate")
    deposit = st.sidebar.number_input("Deposit", min_value=0.0, value=0.0)
    term = st.sidebar.number_input("Term months", min_value=6, value=36)
    if st.sidebar.button("Estimate") and vid:
        res = client.get_finance(vehicle_id=vid, deposit=deposit, term_months=int(term))
        st.sidebar.json(res)
