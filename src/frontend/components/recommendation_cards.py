from __future__ import annotations

import streamlit as st
from typing import List


def render_recommendation_cards(recs: List[dict]):
    # top recommendations section
    st.markdown("<div style='display:flex;align-items:center;justify-content:space-between;'><div style=\"font-size:24px;font-weight:700;color:#0F172A;\">Top Recommendations</div><div style=\"color:#4F6690;\">Results tailored to your answers</div></div>", unsafe_allow_html=True)
    # Ensure web-accessible asset path
    placeholder = '/assets/placeholder.png'

    # grid of cards
    if not recs:
        st.info("No recommendations yet — chat with the assistant to get personalised suggestions.")
        return

    st.markdown("<div class='car-grid'>", unsafe_allow_html=True)
    for idx, r in enumerate(recs):
        img_path = r.get("image") or placeholder
        # normalize to web path
        if img_path and not img_path.startswith('/'):
          img_src = '/' + img_path.lstrip('./')
        else:
          img_src = img_path
        title = f"{r.get('make','')} {r.get('model','')}"
        pricing = r.get("pricing") or {}
        price_text = f"£{pricing.get('list_price_gbp')}" if pricing.get('list_price_gbp') else ""
        monthly_text = f"from £{pricing.get('monthly_from_gbp')} p/m" if pricing.get('monthly_from_gbp') else ""
        badge_html = "<div class='badge'>Best Match</div>" if idx == 0 else ""
        st.markdown(f"""
            <div class='car-card'>
          <div style='position:relative;'>
            <div style='position:absolute;right:12px;top:12px;' class='heart'>❤</div>
            {badge_html}
            <img class='car-img' src='{img_src or ""}' alt='vehicle' />
          </div>
          <div style='font-size:18px;font-weight:700;color:#0F2A5F;margin-bottom:6px;'>{title}</div>
          <div style='font-size:13px;color:#526580;margin-bottom:12px;'>{r.get('variant','')} • {r.get('registration_year','')}</div>
          <div style='display:flex;gap:12px;align-items:center;margin-bottom:12px;color:#526580;'>
            <div>⛽ {r.get('fuel_type','')}</div>
            <div>⚙️ {r.get('transmission','')}</div>
            <div>👥 {r.get('seats','')}</div>
          </div>
          <div style='margin-top:8px;font-size:24px;font-weight:800;color:#0B7CFF;'>{price_text}</div>
          <div style='margin-top:8px;display:flex;gap:8px;align-items:end;'>
            <button style='height:38px;border-radius:10px;background:#FFFFFF;border:1px solid #BBD7FF;color:#0B7CFF;'>View Details</button>
            <button style='height:38px;border-radius:10px;background:#FFFFFF;border:1px solid #BBD7FF;color:#0B7CFF;'>Shortlist</button>
            <button style='height:38px;border-radius:10px;background:#0B7CFF;color:#FFFFFF;border:none;'>Enquire</button>
          </div>
        </div>
        """,
                    unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
