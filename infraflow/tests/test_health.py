import os
import socket

import pytest
import requests


def _is_open(host: str, port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0


@pytest.mark.integration
def test_docs_health():
    base = os.getenv("TEST_BASE_URL", "http://localhost")
    port = int(os.getenv("TEST_API_PORT", "8200"))
    if not _is_open("localhost", port):
        pytest.skip("service not running")
    r = requests.get(f"{base}:{port}/docs", timeout=3)
    assert r.status_code in (200, 301, 302)
