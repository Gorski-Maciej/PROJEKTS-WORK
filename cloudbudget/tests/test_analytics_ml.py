import pytest

pl = pytest.importorskip("polars")
from analytics.polars_transforms import aggregate_costs
from ml.prophet_forecaster import forecast_monthly_cost


def test_aggregate_costs_groups_rows():
    rows = [
        {"tenant_id": 1, "provider": "aws", "service": "ec2", "amount_usd": 10},
        {"tenant_id": 1, "provider": "aws", "service": "ec2", "amount_usd": 5},
    ]
    result = aggregate_costs(rows)
    assert result[0]["total_amount_usd"] == 15


def test_forecast_monthly_cost_contains_ci():
    result = forecast_monthly_cost([{"amount_usd": 100}, {"amount_usd": 50}])
    assert "ci_low" in result and "ci_high" in result
