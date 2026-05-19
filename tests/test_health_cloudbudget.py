from libs.health_checks import HealthSpec, check_api

def test_cloudbudget_health():
    assert check_api("http://localhost:8001", HealthSpec())
