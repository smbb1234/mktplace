from __future__ import annotations

import streamlit as st
from src.frontend.api_client.client import BackendClient
from src.frontend.components.chat_panel import chat_panel
from src.frontend.components.recommendation_cards import render_recommendation_cards
from src.frontend.components.finance_panel import finance_panel
from src.frontend.state.session_state import get_session_id, get_preferences

client = BackendClient()


def main():
    st.set_page_config(page_title="AI Car Buying Assistant")
    st.title("AI Car Buying Assistant — Demo")

    # Sidebar assistant and finance
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


if __name__ == "__main__":
    main()

