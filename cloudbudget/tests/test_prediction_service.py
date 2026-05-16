from datetime import datetime, timedelta

from ml.prophet_forecaster import forecast_monthly_cost


def test_forecast_uses_heuristic_with_small_history():
    now = datetime(2026, 1, 1)
    history = [{"amount_usd": 10.0, "collected_at": now + timedelta(days=i)} for i in range(14)]
    result = forecast_monthly_cost(history)
    assert result["method"] in {"seasonal_heuristic", "prophet"}
    assert result["prediction_30d"] > 0


def test_forecast_empty_history():
    result = forecast_monthly_cost([])
    assert result["prediction_30d"] == 0.0
    assert result["method"] == "empty"
