from __future__ import annotations

import streamlit as st
from src.frontend.state.session_state import get_session_id, set_preferences
from src.frontend.api_client.client import BackendClient

client = BackendClient()


def _ensure_messages():
    if 'chat_messages' not in st.session_state:
        st.session_state['chat_messages'] = [
            {'role': 'ai', 'text': 'Hi — I am your AI car buying assistant. What is your preferred fuel type?'}
        ]


def chat_panel():
    _ensure_messages()
    session_id = get_session_id()

    # header inside chat panel
    st.markdown("<div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;'><div style=\"font-size:18px;font-weight:700;\">Conversation</div><div style=\"color:#4F6690;\">Session: {}</div></div>".format(session_id), unsafe_allow_html=True)

    # messages area
    msg_area = st.container()
    with msg_area:
        for m in st.session_state['chat_messages']:
            if m['role'] == 'ai':
                st.markdown(
                    f"<div class='msg-ai'><div class='ai-avatar'>🤖</div><div>{m['text']}</div></div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='msg-user'>{m['text']}</div>", unsafe_allow_html=True
                )

    # quick reply chips (example)
    cols = st.columns([1, 1, 1])
    with cols[0]:
        if st.button('Petrol'):
            _send_message('Petrol', session_id)
    with cols[1]:
        if st.button('Diesel'):
            _send_message('Diesel', session_id)
    with cols[2]:
        if st.button('Hybrid / Electric'):
            _send_message('Hybrid / Electric', session_id)

    # input at bottom: inline input + send icon button
    input_cols = st.columns([0.9, 0.1])
    with input_cols[0]:
        txt = st.text_input('message', placeholder='Type your answer...', key='chat_input', label_visibility='hidden')
    with input_cols[1]:
        send = st.button('➤', key='chat_send')
    if send and txt:
        _send_message(txt, session_id)


def _send_message(txt: str, session_id: str | None = None):
    # append user message
    st.session_state['chat_messages'].append({'role': 'user', 'text': txt})
    try:
        resp = client.post_chat({'session_id': session_id, 'message': txt})
        ai_text = resp.get('reply') if isinstance(resp, dict) else str(resp)
        # update preferences if any
        if isinstance(resp, dict):
            prefs = {k: v for k, v in resp.items() if k not in ('reply',) and v is not None}
            if prefs:
                set_preferences(prefs)
        st.session_state['chat_messages'].append({'role': 'ai', 'text': ai_text or 'OK'})
    except Exception:
        st.session_state['chat_messages'].append({'role': 'ai', 'text': 'Sorry, failed to reach backend.'})
