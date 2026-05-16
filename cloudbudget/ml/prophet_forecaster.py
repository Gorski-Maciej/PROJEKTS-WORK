def forecast_monthly_cost(history: list[dict]) -> dict:
    total = sum(row.get("amount_usd", 0.0) for row in history)
    baseline = total / max(len(history), 1)
    prediction = round(baseline * 30, 2)
    return {"prediction_30d": prediction, "ci_low": round(prediction * 0.9, 2), "ci_high": round(prediction * 1.1, 2)}
