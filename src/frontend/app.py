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
from src.frontend.components.summary_cards import summary_cards

client = BackendClient()


def main():
    st.set_page_config(page_title="AI Car Buying Assistant")

    # header with logo
    st.markdown(
        """
        <div style='display:flex;align-items:center;gap:8px;'>
          <div style='width:28px;height:28px;border-radius:6px;background:#1e90ff;display:flex;align-items:center;justify-content:center;color:white;'>🚗</div>
          <div style='font-size:20px;font-weight:700;'>AI Car Buying Assistant — Demo</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

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

    # Sidebar nav & controls
    with st.sidebar:
        st.markdown(
            """
            <div style='padding:8px 4px;'>
              <div style='padding:8px 10px;border-radius:8px;background:#e6f2ff;margin-bottom:6px;'>💬 Chat</div>
              <div style='padding:8px 10px;border-radius:8px;'>🚘 Recommendations</div>
              <div style='padding:8px 10px;border-radius:8px;'>💳 Finance</div>
              <div style='padding:8px 10px;border-radius:8px;'>⭐ Shortlist</div>
              <div style='padding:8px 10px;border-radius:8px;'>⚙️ Settings</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        preference_controls()
        finance_panel()

    # Main area: fetch recommendations for session
    sid = get_session_id()
    prefs = get_preferences()

    # Two-column main layout: chat on left, recommendations on right
    left, right = st.columns([1.1, 1.3], gap="large")
    with left:
        chat_panel()
    with right:
        prefs = get_preferences()
        budget = prefs.get('monthly_budget')
        term = st.session_state.get('finance_term', 36)
        deposit = st.session_state.get('finance_deposit', 1000)
        st.markdown(
            """
            <div style='margin-bottom:8px;'>
              <div style='font-size:20px;font-weight:700;'>Top Recommendations</div>
              <div style='font-size:13px;color:#6b7a90;'>Based on your preferences</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
        summary_cards(budget, term, deposit)
        try:
            recs = client.get_recommendations(session_id=sid)
        except Exception:
            recs = []
        # limit to top 3 for display
        render_recommendation_cards(recs[:3] if recs else [])
        # finance summary bar
        st.markdown(
            f"""
            <div class='card' style='margin-top:12px;padding:14px;display:flex;align-items:center;justify-content:space-between;'>
              <div>
                <div style='font-size:13px;color:#6b7a90;'>Finance Summary</div>
                <div style='font-size:14px;'>Budget £{int(budget) if budget else 0} • Term {int(term)} months • Deposit £{int(deposit)}</div>
              </div>
              <div>
                <a href='#' style='background:#1e90ff;color:#fff;text-decoration:none;padding:8px 14px;border-radius:999px;'>View Finance Options</a>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # show selected vehicle detail or enquiry form
    sel = st.session_state.get('selected_vehicle_obj')
    if sel:
        car_detail(sel)
    if st.session_state.get('selected_vehicle'):
        enquiry_form(default_vehicle_id=st.session_state.get('selected_vehicle'))

    # trust note footer
    st.markdown(
        """
        <div style='margin-top:18px;font-size:12px;color:#6b7a90;'>
          Your data is secure and never shared with third parties.
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

