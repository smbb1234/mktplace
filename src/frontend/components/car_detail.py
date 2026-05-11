from __future__ import annotations

import streamlit as st
from src.frontend.api_client.client import BackendClient

client = BackendClient()


def car_detail(vehicle: dict | None):
    st.header("Car details")
    if not vehicle:
        st.info("Select a vehicle to see details")
        return
    st.subheader(f"{vehicle.get('make','')} {vehicle.get('model','')}")
    st.image(vehicle.get('image') or "", width=300)
    st.write(vehicle)
    pricing = vehicle.get('pricing') or {}
    st.write("Pricing:", pricing)
    if st.button("Shortlist this car"):
        sid = st.session_state.get('session_id', 'anon')
        try:
            client.shortlist_add(sid, vehicle.get('vehicle_id'))
            st.success("Added to shortlist")
        except Exception:
            st.error("Failed to add to shortlist")
    if st.button("Enquire about this car"):
        st.session_state['selected_vehicle'] = vehicle.get('vehicle_id')
        st.success("Open enquiry form in main view")
