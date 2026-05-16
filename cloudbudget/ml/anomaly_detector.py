def detect_spend_anomalies(rows: list[dict], threshold: float = 1000.0) -> list[dict]:
    return [r for r in rows if r.get("amount_usd", 0.0) >= threshold]
