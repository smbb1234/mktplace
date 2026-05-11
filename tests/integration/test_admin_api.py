from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

from fastapi.testclient import TestClient

from src.backend.core.database import get_db
from src.backend.main import app
from src.backend.models.leads import Enquiry

client = TestClient(app)


def test_admin_route_list_includes_flush_offline():
    route_methods = {route.path: getattr(route, "methods", set()) for route in app.routes}

    assert "/admin/flush_offline" in route_methods
    assert "POST" in route_methods["/admin/flush_offline"]


def test_admin_route_list_includes_enquiry_list_and_update():
    route_methods = {route.path: getattr(route, "methods", set()) for route in app.routes}

    assert "/admin/enquiries" in route_methods
    assert "GET" in route_methods["/admin/enquiries"]
    assert "/admin/enquiries/{enquiry_id}/status" in route_methods
    assert "POST" in route_methods["/admin/enquiries/{enquiry_id}/status"]


def test_flush_offline_allows_test_path_without_admin_token(monkeypatch):
    from src.backend.scripts import flush_offline_enquiries
    from src.shared.config import settings as settings_module

    monkeypatch.setattr(
        settings_module, "get_settings", lambda: SimpleNamespace(admin_token="")
    )
    monkeypatch.setattr(flush_offline_enquiries, "flush_queue", lambda: None)

    response = client.post("/admin/flush_offline")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_flush_offline_rejects_wrong_admin_token_when_configured(monkeypatch):
    from src.backend.scripts import flush_offline_enquiries
    from src.shared.config import settings as settings_module

    monkeypatch.setattr(
        settings_module,
        "get_settings",
        lambda: SimpleNamespace(admin_token="correct-token"),
    )
    monkeypatch.setattr(flush_offline_enquiries, "flush_queue", lambda: None)

    response = client.post(
        "/admin/flush_offline", headers={"X-Admin-Token": "wrong-token"}
    )

    assert response.status_code == 401


class FakeQuery:
    def __init__(self, items):
        self.items = items

    def order_by(self, *_args, **_kwargs):
        return self

    def offset(self, _offset):
        return self

    def limit(self, limit):
        self.items = self.items[:limit]
        return self

    def all(self):
        return self.items

    def filter(self, *_args, **_kwargs):
        return self

    def one_or_none(self):
        return self.items[0] if self.items else None


class FakeDb:
    def __init__(self, enquiries):
        self.enquiries = enquiries
        self.committed = False
        self.added = []

    def query(self, model):
        assert model is Enquiry
        return FakeQuery(self.enquiries)

    def add(self, item):
        self.added.append(item)

    def commit(self):
        self.committed = True


def _enquiry(status="New"):
    return Enquiry(
        enquiry_id="enq-1",
        session_id="sess-1",
        vehicle_id="vehicle-1",
        full_name="Alex Buyer",
        email="alex@example.com",
        phone="+441234567890",
        status=status,
        created_at=datetime(2026, 5, 11, 12, 0, 0),
    )


def test_admin_enquiry_list_and_update_behaviour(monkeypatch):
    from src.shared.config import settings as settings_module

    fake_db = FakeDb([_enquiry()])
    monkeypatch.setattr(
        settings_module, "get_settings", lambda: SimpleNamespace(admin_token="")
    )

    def override_get_db():
        yield fake_db

    app.dependency_overrides[get_db] = override_get_db
    try:
        list_response = client.get("/admin/enquiries")
        update_response = client.post(
            "/admin/enquiries/enq-1/status", params={"status": "Contacted"}
        )
    finally:
        app.dependency_overrides.pop(get_db, None)

    assert list_response.status_code == 200
    assert list_response.json() == [
        {
            "enquiry_id": "enq-1",
            "full_name": "Alex Buyer",
            "email": "alex@example.com",
            "status": "New",
        }
    ]
    assert update_response.status_code == 200
    assert update_response.json() == {"enquiry_id": "enq-1", "status": "Contacted"}
    assert fake_db.enquiries[0].status == "Contacted"
    assert fake_db.committed is True
