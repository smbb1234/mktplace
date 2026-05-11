from __future__ import annotations

from typing import Dict


def estimate_monthly(list_price: float, deposit: float = 0.0, term_months: int = 36, apr_percent: float = 6.0) -> Dict[str, float]:
    # naive monthly payment calculation for demo only
    principal = max(0.0, list_price - deposit)
    monthly_rate = apr_percent / 100.0 / 12.0
    if monthly_rate == 0:
        payment = principal / term_months
    else:
        payment = principal * (monthly_rate / (1 - (1 + monthly_rate) ** (-term_months)))
    return {"monthly": round(payment, 2), "principal": principal}
