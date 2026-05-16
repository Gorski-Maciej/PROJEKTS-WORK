from api.services.simulation_service import run_what_if_simulation
from ml.anomaly_detector import detect_spend_anomalies


def test_simulation_savings_non_negative():
    result = run_what_if_simulation(1000, 0.8, 0.1)
    assert result["estimated_savings"] >= 0


def test_anomaly_detection():
    rows = [{"amount_usd": 10}, {"amount_usd": 1500}]
    anomalies = detect_spend_anomalies(rows)
    assert len(anomalies) == 1
