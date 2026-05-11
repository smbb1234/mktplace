from src.backend.services.recommendations.match_score import compute_match_score


def test_compute_match_score_budget_and_intent():
    prefs = {"monthly_budget": 300, "intent": "purchase"}
    vehicle = {"vehicle_id": "V1"}
    pricing = {"monthly_from_gbp": 300}
    score = compute_match_score(prefs, vehicle, pricing)
    assert isinstance(score, float)
    assert score >= 0 and score <= 100


def test_compute_match_score_budget_mismatch():
    prefs = {"monthly_budget": 100}
    vehicle = {"vehicle_id": "V2"}
    pricing = {"monthly_from_gbp": 400}
    score = compute_match_score(prefs, vehicle, pricing)
    assert score >= 0
