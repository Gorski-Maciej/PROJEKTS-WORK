import pytest

from libs.health_checks import HealthSpec, check_api


def test_infraflow_health():
    if not check_api("http://localhost:8001", HealthSpec()):
        pytest.skip("infraflow service is not running on localhost:8001")
