from libs.health_checks import HealthSpec, check_api

def test_netguardian_health():
    assert check_api("http://localhost:8200", HealthSpec())
