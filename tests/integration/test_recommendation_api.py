from __future__ import annotations

from fastapi.testclient import TestClient

from src.backend.main import app
from src.backend.models.inventory import InventoryVehicle, VehiclePricing
from src.backend.services.ai import conversation_orchestrator

client = TestClient(app)


class InMemoryCatalog:
    def __init__(self):
        self.vehicles = {
            "petrol-auto": InventoryVehicle(
                car_id="petrol-auto",
                make="Ford",
                model="Focus",
                fuel_type="Petrol",
                transmission="Automatic",
                seats=5,
            ),
            "diesel-manual": InventoryVehicle(
                car_id="diesel-manual",
                make="Volkswagen",
                model="Golf",
                fuel_type="Diesel",
                transmission="Manual",
                seats=5,
            ),
            "petrol-expensive": InventoryVehicle(
                car_id="petrol-expensive",
                make="BMW",
                model="3 Series",
                fuel_type="Petrol",
                transmission="Automatic",
                seats=5,
            ),
        }
        self.pricing = {
            "petrol-auto": VehiclePricing(
                price_id="price-1",
                car_id="petrol-auto",
                list_price_gbp=18000,
                monthly_from_gbp=320,
                apr_percent=6.0,
            ),
            "diesel-manual": VehiclePricing(
                price_id="price-2",
                car_id="diesel-manual",
                list_price_gbp=16000,
                monthly_from_gbp=280,
                apr_percent=6.0,
            ),
            "petrol-expensive": VehiclePricing(
                price_id="price-3",
                car_id="petrol-expensive",
                list_price_gbp=38000,
                monthly_from_gbp=700,
                apr_percent=6.0,
            ),
        }

    def resolve_vehicle_image(self, vehicle_id):
        return f"assets/vehicles/{vehicle_id}.png", False


def test_from_session_returns_recommendation_list_when_catalog_loaded(monkeypatch):
    monkeypatch.setattr(
        "src.backend.api.recommendations.get_catalog", lambda: InMemoryCatalog()
    )

    response = client.get("/recommendations/from_session", params={"limit": 2})

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert body
    assert len(body) <= 2
    for item in body:
        assert "match_score" in item
        assert item["explanation"]
        assert item["image"]


def test_session_preferences_filter_recommendations(monkeypatch):
    monkeypatch.setattr(
        "src.backend.api.recommendations.get_catalog", lambda: InMemoryCatalog()
    )
    conversation_orchestrator._SESSIONS.clear()
    chat_response = client.post(
        "/chat/message",
        json={"message": "budget £400 per month, petrol and automatic"},
    )
    session_id = chat_response.json()["session_id"]

    response = client.get(
        "/recommendations/from_session",
        params={"session_id": session_id, "limit": 5},
    )

    assert response.status_code == 200
    body = response.json()
    assert [item["vehicle_id"] for item in body] == ["petrol-auto"]
    assert body[0]["fuel_type"] == "Petrol"
    assert body[0]["transmission"] == "Automatic"
    assert body[0]["match_score"] > 0
    assert body[0]["explanation"]
    assert body[0]["image"] == "assets/vehicles/petrol-auto.png"
