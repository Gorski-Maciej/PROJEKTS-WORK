import pytest

pytest.importorskip("fastapi")
pytest.importorskip("prometheus_client")

from fastapi.testclient import TestClient
from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics_endpoint_available():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "cloudbudget_" in response.text


def test_tenant_guard_on_cost_summary():
    response = client.get("/api/v1/costs/summary")
    assert response.status_code in (400, 422)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "cloudbudget"
