from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path

from src.shared.config.constants import DEFAULT_PLACEHOLDER_IMAGE_PATH, PROJECT_ROOT


class _FakeContext:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def button(self, *args, **kwargs):
        return False


class _FakeStreamlit:
    def __init__(self):
        self.images = []
        self.infos = []
        self.markdowns = []

    def markdown(self, *args, **kwargs):
        self.markdowns.append((args, kwargs))

    def info(self, message):
        self.infos.append(message)

    def columns(self, count):
        return [_FakeContext() for _ in range(count)]

    def container(self, *args, **kwargs):
        return _FakeContext()

    def image(self, image, *args, **kwargs):
        self.images.append((image, args, kwargs))


def _import_recommendation_cards(monkeypatch):
    monkeypatch.setitem(sys.modules, "streamlit", types.SimpleNamespace())
    return importlib.import_module("src.frontend.components.recommendation_cards")


def test_render_recommendation_cards_with_image_does_not_raise(monkeypatch):
    recommendation_cards = _import_recommendation_cards(monkeypatch)
    fake_st = _FakeStreamlit()
    monkeypatch.setattr(recommendation_cards, "st", fake_st)

    recommendation_cards.render_recommendation_cards(
        [
            {
                "make": "Demo",
                "model": "Car",
                "image": "assets/vehicles/CAR-2026-0001.png",
                "pricing": {"list_price_gbp": 25000, "monthly_from_gbp": 350},
            }
        ]
    )

    assert fake_st.images
    image_source = fake_st.images[0][0]
    assert Path(image_source).exists()
    assert image_source == PROJECT_ROOT / "assets" / "vehicles" / "CAR-2026-0001.png"


def test_render_recommendation_cards_uses_placeholder_when_image_missing(monkeypatch):
    recommendation_cards = _import_recommendation_cards(monkeypatch)
    fake_st = _FakeStreamlit()
    monkeypatch.setattr(recommendation_cards, "st", fake_st)

    recommendation_cards.render_recommendation_cards([{"make": "Demo", "model": "Car"}])

    assert fake_st.images
    assert fake_st.images[0][0] == DEFAULT_PLACEHOLDER_IMAGE_PATH


def test_resolve_streamlit_image_source_placeholder_comes_from_constants(monkeypatch):
    recommendation_cards = _import_recommendation_cards(monkeypatch)

    assert recommendation_cards.resolve_streamlit_image_source(None) == DEFAULT_PLACEHOLDER_IMAGE_PATH
    assert recommendation_cards.resolve_streamlit_image_source("missing.png") == DEFAULT_PLACEHOLDER_IMAGE_PATH
