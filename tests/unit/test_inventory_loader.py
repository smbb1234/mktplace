from src.backend.services.inventory.catalog import get_default_catalog


def test_catalog_loads_and_filters():
    catalog = get_default_catalog()
    ids = catalog.list_vehicle_ids()
    assert isinstance(ids, list)
    # catalog should be non-empty for sample data
    assert len(ids) > 0
    # basic filter by budget should return a list
    results = catalog.filter(budget_monthly_max=1000)
    assert isinstance(results, list)
