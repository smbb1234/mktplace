from __future__ import annotations

import importlib
import sys


class _FakeStreamlit:
    def __init__(self):
        self.markdown_calls: list[str] = []

    def markdown(self, body: str, **_kwargs):
        self.markdown_calls.append(body)


def _load_finance_summary(fake_st: _FakeStreamlit, monkeypatch):
    monkeypatch.setitem(sys.modules, "streamlit", fake_st)
    sys.modules.pop("src.frontend.components.finance_summary", None)
    return importlib.import_module("src.frontend.components.finance_summary")


def test_finance_summary_title_exists(monkeypatch):
    fake_st = _FakeStreamlit()
    finance_summary = _load_finance_summary(fake_st, monkeypatch)

    finance_summary.finance_summary(monthly_budget=450, term_months=48, deposit=2500)

    rendered = "\n".join(fake_st.markdown_calls)
    assert "Finance Summary" in rendered


def test_finance_summary_formats_amounts_and_term(monkeypatch):
    fake_st = _FakeStreamlit()
    finance_summary = _load_finance_summary(fake_st, monkeypatch)

    finance_summary.finance_summary(monthly_budget=1250, term_months=24, deposit=3500)

    rendered = "\n".join(fake_st.markdown_calls)
    assert "Monthly Budget" in rendered
    assert "£1,250" in rendered
    assert "Term" in rendered
    assert "24 months" in rendered
    assert "Deposit" in rendered
    assert "£3,500" in rendered


def test_finance_summary_button_text_exists(monkeypatch):
    fake_st = _FakeStreamlit()
    finance_summary = _load_finance_summary(fake_st, monkeypatch)

    finance_summary.finance_summary(monthly_budget=600, term_months=36, deposit=1000)

    rendered = "\n".join(fake_st.markdown_calls)
    assert "View Finance Options" in rendered
