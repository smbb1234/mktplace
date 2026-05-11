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
            st.button("Shortlist", key="sl-" + r.get("vehicle_id", ""))
