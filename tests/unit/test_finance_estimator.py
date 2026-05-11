from src.backend.services.finance.estimator import estimate_monthly


def test_estimate_monthly_basic():
    res = estimate_monthly(10000, deposit=1000, term_months=36, apr_percent=6.0)
    assert "monthly" in res and res["monthly"] > 0
