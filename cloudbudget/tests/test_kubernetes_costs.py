from api.services.kubernetes_cost_service import estimate_k8s_namespace_costs


def test_estimate_k8s_namespace_costs():
    rows = [
        {"namespace": "prod", "cpu_core_hours": 100, "memory_gb_hours": 500},
        {"namespace": "dev", "cpu_core_hours": 10, "memory_gb_hours": 50},
    ]
    result = estimate_k8s_namespace_costs(rows)
    assert result[0]["namespace"] == "prod"
    assert result[0]["total"] > result[1]["total"]
