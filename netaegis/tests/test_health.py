from server.main_mcp.main import components, health


def test_health():
    payload = health()
    assert payload["status"] == "ok"
    assert payload["service"] == "main_mcp"


def test_components_contains_redis():
    payload = components()
    assert "redis" in payload
    assert payload["redis"]["enabled"] is True
