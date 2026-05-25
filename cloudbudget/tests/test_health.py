import os

os.environ.setdefault("JWT_SECRET", "test_jwt_secret_with_minimum_32_chars")

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body.get("status") == "ok"
