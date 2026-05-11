from __future__ import annotations

import importlib
import sys


class _FakeStreamlit:
    def __init__(self):
        self.markdown_calls: list[str] = []
        self.session_state: dict[str, object] = {}

    def markdown(self, body: str, **_kwargs):
        self.markdown_calls.append(body)


def _load_summary_cards(fake_st: _FakeStreamlit, monkeypatch):
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)
    sys.modules.pop("src.frontend.components.summary_cards", None)
    return importlib.import_module("src.frontend.components.summary_cards")


def test_summary_cards_formats_input_values(monkeypatch):
    fake_st = _FakeStreamlit()
    summary_cards = _load_summary_cards(fake_st, monkeypatch)

    summary_cards.summary_cards(monthly_budget=500, term_months=36, deposit=0)

    rendered = "\n".join(fake_st.markdown_calls)
    assert "£500 Monthly Budget" in rendered
    assert "36 Months Term" in rendered
    assert "£0 Initial Deposit" in rendered


def test_summary_cards_prefers_session_state_values(monkeypatch):
    fake_st = _FakeStreamlit()
    fake_st.session_state.update(
        {
            "preferences": {"monthly_budget": 625},
            "finance_term": 48,
            "finance_deposit": 1500,
        }
    )
    summary_cards = _load_summary_cards(fake_st, monkeypatch)

    summary_cards.summary_cards(monthly_budget=500, term_months=36, deposit=0)

    rendered = "\n".join(fake_st.markdown_calls)
    assert "£625 Monthly Budget" in rendered
    assert "48 Months Term" in rendered
    assert "£1500 Initial Deposit" in rendered


def test_summary_cards_defaults_are_stable(monkeypatch):
    fake_st = _FakeStreamlit()
    summary_cards = _load_summary_cards(fake_st, monkeypatch)

    summary_cards.summary_cards()

    rendered = "\n".join(fake_st.markdown_calls)
    assert "£0 Monthly Budget" in rendered
    assert "36 Months Term" in rendered
    assert "£0 Initial Deposit" in rendered
