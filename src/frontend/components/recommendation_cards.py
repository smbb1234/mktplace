from __future__ import annotations

import streamlit as st
from typing import List


def render_recommendation_cards(recs: List[dict]):
    st.header("Recommendations")
    placeholder = None
    try:
        from src.shared.config.constants import DEFAULT_PLACEHOLDER_IMAGE_PATH
        placeholder = str(DEFAULT_PLACEHOLDER_IMAGE_PATH)
    except Exception:
        placeholder = None

    for r in recs:
        # render a styled card
        img_path = r.get("image") or placeholder
        title = f"{r.get('make','')} {r.get('model','')}"
        pricing = r.get("pricing") or {}
        price_text = f"£{pricing.get('list_price_gbp')}" if pricing.get('list_price_gbp') else ""
        monthly_text = f"from £{pricing.get('monthly_from_gbp')} p/m" if pricing.get('monthly_from_gbp') else ""
        explanation = r.get("explanation") if isinstance(r.get("explanation"), dict) else {"explanation": r.get("explanation")}
        html = f"""
        <div class='card'>
          <div style='display:flex; gap:12px;'>
            <div style='flex:0 0 160px;'>
              <img class='card-img' src='{img_path or ''}' alt='vehicle' />
            </div>
            <div style='flex:1;'>
              <div class='card-title'>{title}</div>
              <div class='card-meta'>{explanation.get('explanation','')}</div>
              <div style='margin-top:8px; font-weight:600'>{price_text} {monthly_text}</div>
              <div style='margin-top:6px;'>Match: {r.get('match_score')}</div>
            </div>
          </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        cols = st.columns([1, 1, 1])
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
