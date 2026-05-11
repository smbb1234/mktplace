from __future__ import annotations

import streamlit as st
from src.frontend.components.validation import validate_enquiry_form
from src.frontend.api_client.client import BackendClient

client = BackendClient()


def enquiry_form(default_vehicle_id: str | None = None):
    st.header("Submit an enquiry")
    vehicle_id = st.text_input("Vehicle ID", value=default_vehicle_id or "")
    full_name = st.text_input("Full name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    monthly_budget = st.number_input("Monthly budget", value=0)
    deposit = st.number_input("Deposit", value=0)
    timeframe = st.selectbox("Buying timeframe", options=["ASAP", "1-3 months", "3-6 months", "6+ months"]) 
    if st.button("Submit enquiry"):
        data = {
            "vehicle_id": vehicle_id,
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "monthly_budget_gbp": monthly_budget,
            "deposit_gbp": deposit,
            "buying_timeframe": timeframe,
        }
        if not validate_enquiry_form(data):
            return
        try:
            res = client.post(f"{client.base}/enquiries/", json=data)
            st.success("Enquiry submitted")
        except Exception as e:
            st.error(f"Failed to submit enquiry: {e}")
