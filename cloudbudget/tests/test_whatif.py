from api.services.whatif_service import simulate_cloud_migration, simulate_rightsizing, simulate_architecture_migration


def test_simulate_cloud_migration_payback():
    res = simulate_cloud_migration(1000, 20, one_time_migration_cost=1000)
    assert res["monthly_savings"] == 200
    assert res["payback_months"] == 5.0


def test_simulate_rightsizing():
    res = simulate_rightsizing(100, utilization_pct=30)
    assert res["optimized_instance_cost"] == 70.0


def test_architecture_migration_between_providers():
    records = [
        {"provider": "aws", "amount_usd": 100.0},
        {"provider": "aws", "amount_usd": 100.0},
        {"provider": "azure", "amount_usd": 80.0},
    ]
    res = simulate_architecture_migration(records, provider_from="aws", provider_to="azure", server_count=1)
    assert res["baseline_monthly_cost"] == 280.0
    assert res["projected_monthly_cost"] < 280.0
    assert res["monthly_savings"] > 0
