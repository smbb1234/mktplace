from __future__ import annotations

import streamlit as st
from src.frontend.api_client.client import BackendClient
from src.frontend.components.chat_panel import chat_panel
from src.frontend.components.recommendation_cards import render_recommendation_cards
from src.frontend.components.finance_panel import finance_panel
from src.frontend.state.session_state import get_session_id, get_preferences
from src.frontend.components.preference_controls import preference_controls
from src.frontend.components.car_detail import car_detail
from src.frontend.components.enquiry_form import enquiry_form

client = BackendClient()


def main():
    st.set_page_config(page_title="AI Car Buying Assistant")
    st.title("AI Car Buying Assistant — Demo")

    # Inject minimal CSS for card styling
    st.markdown(
        """
        <style>
        .card {background: #ffffff; border-radius: 8px; padding: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);}
        .card-img {width:160px; height:120px; object-fit:cover; border-radius:4px;}
        .card-title {font-weight:600; font-size:18px; margin-bottom:6px}
        .card-meta {color:#666; font-size:13px}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar assistant and finance
    preference_controls()
    chat_panel()
    finance_panel()

    # Main area: fetch recommendations for session
    sid = get_session_id()
    prefs = get_preferences()
    st.write("Session:", sid)
    st.write("Preferences:")
    st.json(prefs)

    try:
        recs = client.get_recommendations(session_id=sid)
    except Exception:
        recs = []
    render_recommendation_cards(recs)

    # show selected vehicle detail or enquiry form
    sel = st.session_state.get('selected_vehicle_obj')
    if sel:
        car_detail(sel)
    if st.session_state.get('selected_vehicle'):
        enquiry_form(default_vehicle_id=st.session_state.get('selected_vehicle'))


if __name__ == "__main__":
    main()

