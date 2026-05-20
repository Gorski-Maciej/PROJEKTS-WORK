import io
import urllib.error

from libs.health_checks import HealthSpec, check_api, with_backoff


class _Resp:
    def __init__(self, status: int):
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_check_api_returns_true_for_expected_status(monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", lambda req, timeout=0: _Resp(200))
    assert check_api("http://example", HealthSpec()) is True


def test_check_api_handles_http_error_status(monkeypatch):
    def _raise(req, timeout=0):
        raise urllib.error.HTTPError(req.full_url, 503, "down", hdrs=None, fp=io.BytesIO())

    monkeypatch.setattr("urllib.request.urlopen", _raise)
    assert check_api("http://example", HealthSpec(expected_status=(200,))) is False


def test_check_api_handles_url_error(monkeypatch):
    def _raise(req, timeout=0):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr("urllib.request.urlopen", _raise)
    assert check_api("http://example", HealthSpec()) is False


def test_with_backoff_eventually_succeeds():
    state = {"count": 0}

    def flaky():
        state["count"] += 1
        return state["count"] >= 3

    assert with_backoff(flaky, retries=4, base_delay=0) is True
