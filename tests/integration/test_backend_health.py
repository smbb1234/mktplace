import os

from fastapi.testclient import TestClient


def test_backend_health_and_catalog(tmp_path, monkeypatch):
    # Use an in-memory sqlite DB for tests to avoid requiring Postgres
    monkeypatch.setenv("DATABASE_URL", "sqlite+pysqlite:///:memory:")
    # Ensure INVENTORY_CSV_PATH points to the repo data file
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    csv_path = os.path.join(repo_root, "data", "datasetSample.csv")
    if os.path.exists(csv_path):
        monkeypatch.setenv("INVENTORY_CSV_PATH", csv_path)

    # Import app after env vars set
    from src.backend.main import app

    client = TestClient(app)

    # Ensure catalog is loaded for the test environment; startup may not have
    # initialized it in the TestClient lifecycle in some environments.
    import src.backend.startup as startup_module
    from src.backend.services.inventory.catalog import get_default_catalog
    if startup_module.get_catalog() is None:
        # Load catalog and assign it into the startup module so endpoint sees it
        startup_module.catalog = get_default_catalog(csv_path=csv_path)

    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"

    # Catalog endpoint should respond (may be empty list)
    r2 = client.get("/catalog")
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)
