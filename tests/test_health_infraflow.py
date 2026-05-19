from libs.health_checks import HealthSpec, check_api

def test_infraflow_health():
    assert check_api("http://localhost:8100", HealthSpec())
