from fastapi.testclient import TestClient
from server.main_mcp.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
