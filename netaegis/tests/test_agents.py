from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock, patch
import importlib
import sys

from agents.netpulse.checks import check_port
from agents.seclog.agent import get_parser_for_path
from agents.seclog.parsers.auth import parse_line as parse_auth
from agents.seclog.parsers.nginx import parse_line as parse_nginx


def _load_netconfig_agent_module():
    if "git" not in sys.modules:
        fake_git = ModuleType("git")
        fake_git.Repo = MagicMock()
        sys.modules["git"] = fake_git
    return importlib.import_module("agents.netconfig.agent")


def test_auth_parser_failed_login():
    line = "Failed password for root from 10.0.0.2 port 22 ssh2"
    event = parse_auth(line)
    assert event is not None
    assert event["type"] == "failed_login"
    assert event["details"]["ip"] == "10.0.0.2"


def test_nginx_parser_5xx():
    line = '127.0.0.1 - - [12/Jan/2026] "GET /health HTTP/1.1" 503 123 "-" "curl/8.0"'
    event = parse_nginx(line)
    assert event is not None
    assert event["type"] == "http_5xx"
    assert event["details"]["status"] == "503"


def test_nginx_parser_non_5xx_returns_none():
    line = '127.0.0.1 - - [12/Jan/2026] "GET / HTTP/1.1" 200 64 "-" "curl/8.0"'
    assert parse_nginx(line) is None


def test_check_port_closed_local_port():
    assert check_port("127.0.0.1", 1, timeout=0.1) is False


def test_template_file_contains_placeholder():
    template = Path("/workspace/PROJEKTS-WORK/netaegis/agents/netconfig/templates/mikrotik_acl.j2").read_text()
    assert "{{ admin_ip }}" in template


def test_parser_mapping_by_path():
    assert get_parser_for_path("/var/log/auth.log") is not None
    assert get_parser_for_path("/var/log/nginx/access.log") is not None
    assert get_parser_for_path("/tmp/other.log") is None


def test_push_config_executes_commands():
    agent = _load_netconfig_agent_module()
    ssh = MagicMock()

    with patch.object(agent.paramiko, "SSHClient", return_value=ssh):
        import asyncio
        asyncio.run(agent.push_config("192.168.1.1", "line1\nline2\n"))

    ssh.connect.assert_called_once()
    commands = [c.args[0] for c in ssh.exec_command.call_args_list]
    assert commands[0] == "configure terminal"
    assert "line1" in commands
    assert "line2" in commands
    assert commands[-1] == "end"
    ssh.close.assert_called_once()
