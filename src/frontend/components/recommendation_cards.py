from __future__ import annotations

import streamlit as st
from typing import List


def render_recommendation_cards(recs: List[dict]):
    st.header("Recommendations")
    for r in recs:
        with st.container():
            st.subheader(r.get("make") + " " + (r.get("model") or ""))
            st.write(r.get("explanation", {}))
            st.write(f"Match score: {r.get('match_score')}")
            cols = st.columns([1,1,1])
            if cols[0].button("View details", key="view-" + r.get("vehicle_id", "")):
                st.session_state['selected_vehicle_obj'] = r
                st.experimental_rerun()
            if cols[1].button("Shortlist", key="sl-" + r.get("vehicle_id", "")):
                sid = st.session_state.get('session_id', 'anon')
                from src.frontend.api_client.client import BackendClient
                client = BackendClient()
                try:
                    client.shortlist_add(sid, r.get('vehicle_id'))
                    st.success("Shortlisted")
                except Exception:
                    st.error("Failed to shortlist")
            if cols[2].button("Enquire", key="enq-" + r.get("vehicle_id", "")):
                st.session_state['selected_vehicle'] = r.get('vehicle_id')
                st.experimental_rerun()
