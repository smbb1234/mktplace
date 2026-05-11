from __future__ import annotations

import streamlit as st
from src.frontend.state.session_state import set_preferences, get_session_id


def preference_controls():
    st.sidebar.header("Preferences")
    session_id = get_session_id()
    budget = st.sidebar.number_input("Monthly budget", min_value=0.0, value=500.0)
    fuel = st.sidebar.selectbox("Fuel type", options=["Any", "Petrol", "Diesel", "Electric"]) 
    transmission = st.sidebar.selectbox("Transmission", options=["Any", "Manual", "Automatic"]) 
    if st.sidebar.button("Apply preferences"):
        prefs = {}
        prefs["monthly_budget"] = budget
        if fuel != "Any":
            prefs["fuel_type"] = fuel
        if transmission != "Any":
            prefs["transmission"] = transmission
        set_preferences(prefs)
        st.sidebar.success("Preferences applied")
