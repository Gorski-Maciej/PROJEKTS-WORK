import pytest


def _test_client():
    pytest.importorskip("fastapi")
    return pytest.importorskip("fastapi.testclient").TestClient


def test_cloudbudget_health():
    TestClient = _test_client()
    from cloudbudget.api.main import app

    with TestClient(app) as client:
        response = client.get('/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'ok'
    assert payload['service'] == 'cloudbudget-api'


def test_infraflow_health():
    TestClient = _test_client()
    from infraflow.engine.main import app

    with TestClient(app) as client:
        response = client.get('/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'ok'
    assert payload['service'] == 'infraflow-engine'


def test_netguardian_health():
    TestClient = _test_client()
    from netguardian.engine.main import app

    with TestClient(app) as client:
        response = client.get('/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'ok'
    assert payload['service'] == 'netguardian-engine'


def test_netaegis_health():
    TestClient = _test_client()
    from netaegis.server.main_mcp.main import app

    with TestClient(app) as client:
        response = client.get('/health')
    assert response.status_code == 200
    payload = response.json()
    assert payload['status'] == 'ok'
    assert payload['service'] == 'netaegis-main-mcp'
