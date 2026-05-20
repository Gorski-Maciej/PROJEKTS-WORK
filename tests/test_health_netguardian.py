import pytest

from libs.health_checks import HealthSpec, check_api


def test_netguardian_health():
    if not check_api("http://localhost:8300", HealthSpec()):
        pytest.skip("netguardian service is not running on localhost:8300")
