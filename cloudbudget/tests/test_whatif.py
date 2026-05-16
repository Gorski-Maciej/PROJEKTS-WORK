from api.services.whatif_service import simulate_cloud_migration, simulate_rightsizing


def test_simulate_cloud_migration_payback():
    res = simulate_cloud_migration(1000, 20, one_time_migration_cost=1000)
    assert res["monthly_savings"] == 200
    assert res["payback_months"] == 5.0


def test_simulate_rightsizing():
    res = simulate_rightsizing(100, utilization_pct=30)
    assert res["optimized_instance_cost"] == 70.0
