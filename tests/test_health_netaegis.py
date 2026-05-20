import pytest

from libs.health_checks import HealthSpec, check_api


def test_netaegis_health():
    if not check_api("http://localhost:8400", HealthSpec()):
        pytest.skip("netaegis service is not running on localhost:8400")
