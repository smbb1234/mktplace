from __future__ import annotations

import importlib
import sys


class _Context:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class _FakeStreamlit:
    def __init__(self, button_clicked: bool = False):
        self.markdown_calls: list[str] = []
        self.session_state: dict[str, object] = {}
        self.rerun_called = False
        self._button_clicked = button_clicked

    def container(self):
        return _Context()

    def columns(self, _spec):
        return [_Context(), _Context()]

    def markdown(self, body: str, **_kwargs):
        self.markdown_calls.append(body)

    def button(self, _label: str, **_kwargs):
        return self._button_clicked

    def rerun(self):
        self.rerun_called = True


def _reload_frontend_modules(fake_st: _FakeStreamlit, monkeypatch):
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)
    for module_name in (
        "src.frontend.state.session_state",
        "src.frontend.components.header",
    ):
        sys.modules.pop(module_name, None)
    session_state = importlib.import_module("src.frontend.state.session_state")
    header = importlib.import_module("src.frontend.components.header")
    return session_state, header


def test_header_initial_render_includes_title(monkeypatch):
    fake_st = _FakeStreamlit()
    _, header = _reload_frontend_modules(fake_st, monkeypatch)

    header.render_header()

    rendered = "\n".join(fake_st.markdown_calls)
    assert "AI Car Buying Assistant ✨" in rendered
    assert "Your personal car expert" in rendered


def test_reset_session_state_removes_configured_keys(monkeypatch):
    fake_st = _FakeStreamlit()
    session_state, _ = _reload_frontend_modules(fake_st, monkeypatch)
    for key in session_state.RESET_SESSION_STATE_KEYS:
        fake_st.session_state[key] = f"value-for-{key}"
    fake_st.session_state["unrelated"] = "keep-me"

    session_state.reset_session_state()

    for key in session_state.RESET_SESSION_STATE_KEYS:
        assert key not in fake_st.session_state
    assert fake_st.session_state["unrelated"] == "keep-me"


def test_reset_session_state_accepts_specific_keys(monkeypatch):
    fake_st = _FakeStreamlit()
    session_state, _ = _reload_frontend_modules(fake_st, monkeypatch)
    fake_st.session_state.update({"session_id": "old", "chat_messages": [], "keep": True})

    session_state.reset_session_state(keys=("session_id", "chat_messages"))

    assert "session_id" not in fake_st.session_state
    assert "chat_messages" not in fake_st.session_state
    assert fake_st.session_state["keep"] is True


def test_header_new_session_button_resets_state_and_reruns(monkeypatch):
    fake_st = _FakeStreamlit(button_clicked=True)
    session_state, header = _reload_frontend_modules(fake_st, monkeypatch)
    for key in session_state.RESET_SESSION_STATE_KEYS:
        fake_st.session_state[key] = f"value-for-{key}"

    header.render_header()

    for key in session_state.RESET_SESSION_STATE_KEYS:
        assert key not in fake_st.session_state
    assert fake_st.rerun_called is True
