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

    # Inject global CSS matching the premium sky-blue theme and layout
    st.markdown(
        """
        <style>
        :root{--sky:#0B7CFF;--muted:#4F6690;--card-shadow:0 10px 30px rgba(37,99,235,0.08);} 
        body, .stApp {background: linear-gradient(135deg,#EAF6FF 0%,#F8FBFF 45%,#FFFFFF 100%);} 
        .main-container{padding:24px;display:flex;gap:24px;height:100vh;box-sizing:border-box;} 
        .left-sidebar{width:88px;background:rgba(255,255,255,0.9);border-right:1px solid #DCEBFA;padding-top:12px;}
        .logo-box{width:48px;height:48px;border-radius:8px;background:var(--sky);display:flex;align-items:center;justify-content:center;color:#fff;margin:8px auto;} 
        .side-item{height:72px;display:flex;align-items:center;justify-content:center;color:#334155;font-size:11px;} 
        .side-item.active{background:#EFF7FF;border-left:4px solid var(--sky);color:var(--sky);} 
        .panel{background:rgba(255,255,255,0.88);border:1px solid #D8EAFE;border-radius:22px;padding:24px;box-shadow:0 12px 32px rgba(15,23,42,0.06);overflow:auto;} 
        .chat-panel{width:460px;min-width:420px;max-width:460px;height:calc(100vh - 48px);background:rgba(255,255,255,0.85);border:1px solid #D8EAFE;border-radius:22px;padding:24px;box-shadow:0 12px 32px rgba(15,23,42,0.06);display:flex;flex-direction:column;} 
        .recommend-panel{flex:1;min-width:420px;} 
        .header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;} 
        .title{font-size:28px;font-weight:700;color:#0F172A;} 
        .subtitle{font-size:14px;color:#4F6690;} 
        .new-session{height:44px;background:#FFFFFF;border:1px solid #CFE3FF;color:var(--sky);border-radius:12px;padding:8px 14px;} 
        /* Chat bubbles */
        .msg-ai{max-width:78%;background:linear-gradient(180deg,#F4FAFF 0%,#EAF4FF 100%);border:1px solid #DCEBFA;border-radius:16px;padding:16px;color:#0F172A;font-size:14px;line-height:1.5;margin-bottom:12px;display:flex;gap:12px;} 
        .msg-user{align-self:flex-end;background:linear-gradient(135deg,#DCEEFF 0%,#BFDFFF 100%);border-radius:16px;padding:14px 16px;color:#075BB5;font-weight:600;max-width:70%;margin-bottom:12px;} 
        .ai-avatar{width:36px;height:36px;border-radius:50%;background:var(--sky);display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px;} 
        .quick-chip{display:inline-block;height:38px;padding:0 18px;border:1px solid #BBD7FF;border-radius:10px;background:#fff;color:var(--sky);font-weight:600;margin-right:8px;margin-top:8px;}
        .car-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;margin-top:12px;} 
        .car-card{background:#fff;border:1px solid #DCEBFA;border-radius:18px;padding:18px;min-height:420px;box-shadow:0 10px 24px rgba(15,23,42,0.06);transition:transform .18s,box-shadow .18s;} 
        .car-card:hover{transform:translateY(-4px);box-shadow:0 16px 34px rgba(37,99,235,0.12);} 
        .car-img{width:100%;height:160px;object-fit:contain;background:#fff;margin-bottom:16px;} 
        .badge{background:#D7FAF0;color:#0E9F6E;border-radius:999px;padding:6px 12px;font-size:11px;font-weight:700;display:inline-block;} 
        .heart{position:absolute;right:12px;top:12px;color:#64748B;} 
        .heart:hover{color:var(--sky);} 
        .finance-bar{height:92px;background:linear-gradient(90deg,#F4FAFF 0%,#FFFFFF 100%);border:1px solid #D6E6F8;border-radius:18px;padding:20px 24px;display:flex;align-items:center;justify-content:space-between;margin-top:18px;} 
        .summary-cards{display:flex;gap:12px;margin-bottom:12px;} 
        .summary-small{background:linear-gradient(180deg,#F8FBFF 0%,#EEF7FF 100%);border:1px solid #D6E6F8;border-radius:16px;padding:12px;width:200px;height:78px;} 
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Top header row across the main columns (left column reserved for sidebar)
    top_cols = st.columns([88, 420, 1], gap='large')
    with top_cols[0]:
        # empty left column for sidebar alignment
        st.markdown("", unsafe_allow_html=True)
    with top_cols[1]:
        st.markdown(
            """
            <div class='header' style='align-items:flex-start;'>
              <div>
                <div class='title'>AI Car Buying Assistant ✨</div>
                <div class='subtitle'>Your personal car expert</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_cols[2]:
        st.markdown(
            """
            <div style='display:flex;align-items:center;justify-content:flex-end;height:92px;'>
              <button class='new-session' style='width:132px;height:44px;display:flex;align-items:center;justify-content:center;'>⟳&nbsp;&nbsp;New Session</button>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Main area: fetch recommendations for session
    sid = get_session_id()
    prefs = get_preferences()

    # Main three-column layout: sidebar (88px), chat (420px), recommendations (rest)
    cols = st.columns([88, 420, 1], gap="large")
    # LEFT SIDEBAR
    with cols[0]:
        st.markdown(
            """
            <div style='height:100vh;display:flex;flex-direction:column;align-items:center;padding-top:20px;border-right:1px solid #DCEBFA;background:#FFFFFF;box-shadow:0 8px 30px rgba(37,99,235,0.08);'>
              <div style='height:100px;display:flex;align-items:center;justify-content:center;width:100%;'>
                <div style='width:48px;height:48px;border-radius:14px;background:#0B7CFF;display:flex;align-items:center;justify-content:center;color:white;'>🚗</div>
              </div>
              <div style='margin-top:20px;width:100%;'>
                <div style='height:82px;display:flex;align-items:center;justify-content:center;color:#0B7CFF;background:#EFF7FF;border-left:4px solid #0B7CFF;'>
                  <div style='text-align:center;font-size:11px;'>Chat</div>
                </div>
                <div style='height:82px;display:flex;align-items:center;justify-content:center;color:#334155;'>
                  <div style='text-align:center;font-size:11px;'>Cars</div>
                </div>
                <div style='height:82px;display:flex;align-items:center;justify-content:center;color:#334155;'>
                  <div style='text-align:center;font-size:11px;'>Finance</div>
                </div>
                <div style='height:82px;display:flex;align-items:center;justify-content:center;color:#334155;'>
                  <div style='text-align:center;font-size:11px;'>Shortlist</div>
                </div>
                <div style='height:82px;display:flex;align-items:center;justify-content:center;color:#334155;'>
                  <div style='text-align:center;font-size:11px;'>Settings</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # CHAT PANEL (middle)
    with cols[1]:
        st.markdown("<div class='chat-panel'>", unsafe_allow_html=True)
        chat_panel()
        st.markdown("</div>", unsafe_allow_html=True)

    # RECOMMENDATIONS PANEL (right)
    with cols[2]:
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
        # limit to top 9 for display
        render_recommendation_cards(recs[:9] if recs else [])
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

