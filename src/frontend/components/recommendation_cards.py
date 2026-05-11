from __future__ import annotations

from pathlib import Path
from typing import List
from urllib.parse import urlparse

import streamlit as st

from src.shared.config.constants import DEFAULT_PLACEHOLDER_IMAGE_PATH, PROJECT_ROOT


_URL_SCHEMES = {"http", "https", "data"}


def _is_streamlit_readable_url(value: str) -> bool:
    return urlparse(value).scheme in _URL_SCHEMES


def resolve_streamlit_image_source(image: object | None) -> str | Path:
    """Return a Streamlit-readable image source for recommendation cards.

    Backend responses should provide an explicit URL or a project-relative path.
    Streamlit can read local files directly from ``Path`` objects, so local image
    paths are converted to files on disk instead of being embedded in HTML
    ``<img>`` tags that the browser cannot fetch from arbitrary filesystem
    paths.
    """
    if image:
        raw = str(image).strip()
        if raw and _is_streamlit_readable_url(raw):
            return raw

        if raw:
            image_path = Path(raw)
            candidates: list[Path] = []
            if image_path.is_absolute():
                candidates.append(image_path)
                # Support legacy web-style values such as /assets/placeholder.png.
                candidates.append(PROJECT_ROOT / raw.lstrip("/"))
            else:
                candidates.extend((PROJECT_ROOT / image_path, image_path))

            for candidate in candidates:
                if candidate.exists():
                    return candidate

    return DEFAULT_PLACEHOLDER_IMAGE_PATH


def render_recommendation_cards(recs: List[dict]):
    st.markdown(
        "<div style='display:flex;align-items:center;justify-content:space-between;'>"
        '<div style="font-size:24px;font-weight:700;color:#0F172A;">Top Recommendations</div>'
        '<div style="color:#4F6690;">Results tailored to your answers</div></div>',
        unsafe_allow_html=True,
    )

    if not recs:
        st.info("No recommendations yet — chat with the assistant to get personalised suggestions.")
        return

    for row_start in range(0, len(recs), 3):
        columns = st.columns(3)
        for offset, r in enumerate(recs[row_start : row_start + 3]):
            idx = row_start + offset
            with columns[offset]:
                with st.container(border=True):
                    if idx == 0:
                        st.markdown("<div class='badge'>Best Match</div>", unsafe_allow_html=True)

                    st.image(
                        resolve_streamlit_image_source(r.get("image")),
                        caption=f"{r.get('make', '')} {r.get('model', '')}".strip() or "Vehicle",
                        use_container_width=True,
                    )

                    title = f"{r.get('make', '')} {r.get('model', '')}".strip()
                    pricing = r.get("pricing") or {}
                    price_text = f"£{pricing.get('list_price_gbp')}" if pricing.get("list_price_gbp") else ""
                    monthly_text = (
                        f"from £{pricing.get('monthly_from_gbp')} p/m"
                        if pricing.get("monthly_from_gbp")
                        else ""
                    )
                    st.markdown(
                        f"""
                        <div style='font-size:18px;font-weight:700;color:#0F2A5F;margin-bottom:6px;'>{title}</div>
                        <div style='font-size:13px;color:#526580;margin-bottom:12px;'>{r.get('variant', '')} • {r.get('registration_year', '')}</div>
                        <div style='display:flex;gap:12px;align-items:center;margin-bottom:12px;color:#526580;'>
                          <div>⛽ {r.get('fuel_type', '')}</div>
                          <div>⚙️ {r.get('transmission', '')}</div>
                          <div>👥 {r.get('seats', '')}</div>
                        </div>
                        <div style='margin-top:8px;font-size:24px;font-weight:800;color:#0B7CFF;'>{price_text}</div>
                        <div style='font-size:13px;color:#526580;'>{monthly_text}</div>
                        """,
                        unsafe_allow_html=True,
                    )

                    action_cols = st.columns(3)
                    action_cols[0].button("View Details", key=f"details-{idx}")
                    action_cols[1].button("Shortlist", key=f"shortlist-{idx}")
                    action_cols[2].button("Enquire", key=f"enquire-{idx}")
