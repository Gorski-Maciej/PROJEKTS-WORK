import pytest

from libs.health_checks import HealthSpec, check_api


def test_cloudbudget_health():
    if not check_api("http://localhost:8100", HealthSpec()):
        pytest.skip("cloudbudget service is not running on localhost:8100")
