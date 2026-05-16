from __future__ import annotations

from datetime import datetime


def _heuristic_forecast(history: list[dict]) -> dict:
    if not history:
        return {"prediction_30d": 0.0, "ci_low": 0.0, "ci_high": 0.0, "method": "empty"}

    total = 0.0
    weekend = 0.0
    weekend_n = 0
    weekday = 0.0
    weekday_n = 0

    for row in history:
        amount = float(row.get("amount_usd", 0.0))
        ts = row.get("collected_at")
        if isinstance(ts, str):
            ts = datetime.fromisoformat(ts)
        total += amount
        if isinstance(ts, datetime) and ts.weekday() >= 5:
            weekend += amount
            weekend_n += 1
        else:
            weekday += amount
            weekday_n += 1

    baseline_daily = total / max(len(history), 1)
    weekend_avg = weekend / weekend_n if weekend_n else baseline_daily
    weekday_avg = weekday / weekday_n if weekday_n else baseline_daily

    # 30-day month proxy: 22 weekdays + 8 weekend days
    prediction = (22 * weekday_avg) + (8 * weekend_avg)

    return {
        "prediction_30d": round(prediction, 2),
        "ci_low": round(prediction * 0.88, 2),
        "ci_high": round(prediction * 1.12, 2),
        "method": "seasonal_heuristic",
    }


def forecast_monthly_cost(history: list[dict]) -> dict:
    """Forecast 30-day spend.

    Uses Prophet when enough data points are available and dependency is installed.
    Falls back to a lightweight seasonal heuristic otherwise.
    """
    if len(history) < 90:
        return _heuristic_forecast(history)

    try:
        import pandas as pd
        from prophet import Prophet

        rows = []
        for row in history:
            ts = row.get("collected_at")
            if isinstance(ts, str):
                ts = datetime.fromisoformat(ts)
            rows.append({"ds": ts, "y": float(row.get("amount_usd", 0.0))})

        df = pd.DataFrame(rows).dropna(subset=["ds"])
        if df.empty:
            return _heuristic_forecast(history)

        model = Prophet(weekly_seasonality=True, daily_seasonality=False, yearly_seasonality=True)
        model.fit(df)
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future).tail(30)

        prediction = float(forecast["yhat"].sum())
        ci_low = float(forecast["yhat_lower"].sum())
        ci_high = float(forecast["yhat_upper"].sum())

        return {
            "prediction_30d": round(prediction, 2),
            "ci_low": round(ci_low, 2),
            "ci_high": round(ci_high, 2),
            "method": "prophet",
        }
    except Exception:
        return _heuristic_forecast(history)
