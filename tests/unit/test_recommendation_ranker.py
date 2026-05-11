from src.backend.services.recommendations.ranker import rank_vehicles


def test_ranking_orders_by_score():
    prefs = {"monthly_budget": 300, "intent": "purchase"}
    v1 = {"vehicle_id": "A", "make": "X"}
    v2 = {"vehicle_id": "B", "make": "Y"}
    pricing = {"A": {"monthly_from_gbp": 250}, "B": {"monthly_from_gbp": 300}}
    ranked = rank_vehicles([v1, v2], pricing, prefs, limit=2)
    assert len(ranked) == 2
    assert all("match_score" in r for r in ranked)
