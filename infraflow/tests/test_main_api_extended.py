import sys
from pathlib import Path

import pytest
from fastapi import HTTPException

sys.path.append(str(Path(__file__).resolve().parents[1]))

from engine.main import execute_runbook, get_server, health, list_servers, RunbookRequest


def test_health_contains_service():
    payload = health()
    assert payload["status"] == "ok"
    assert payload["service"] == "infraflow-engine"


def test_list_servers_parsing(tmp_path):
    sample = tmp_path / "servers.yml"
    sample.write_text(
        """\
metadata: ignored
servers:
  - name: web-01
    host: 10.0.0.10
    port: 22
    enabled: true
""",
        encoding="utf-8",
    )

    from engine import main as m

    old = m.CONFIG_PATH
    m.CONFIG_PATH = sample
    try:
        servers = list_servers()
        assert servers and servers[0]["name"] == "web-01"
        assert get_server("web-01")["port"] == 22
        assert get_server("web-01")["enabled"] is True
    finally:
        m.CONFIG_PATH = old


def test_execute_runbook_raises_for_unknown_server():
    with pytest.raises(HTTPException) as exc:
        execute_runbook(RunbookRequest(server="missing-01", action="restart_nginx"))
    assert exc.value.status_code == 404
