from libs.health_checks import HealthSpec, check_api

def test_netaegis_health():
    assert check_api("http://localhost:8300", HealthSpec())
