from api.services.ri_optimizer_service import recommend_ri_plan
from api.services.simulation_service import run_provider_migration_simulation


def test_ri_optimizer():
    res = recommend_ri_plan(1000, commitment_years=1)
    assert res["estimated_yearly_savings"] > 0


def test_migration_simulation():
    res = run_provider_migration_simulation(10, 50, 35)
    assert res["savings"] == 150
