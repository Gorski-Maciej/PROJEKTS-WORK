from agents.base_agent import normalize


def collect_costs(tenant_id: int = 1) -> list[dict]:
    return [
        normalize(tenant_id, "onprem", "compute", "onprem-resource-1", 43.20, 12.0),
        normalize(tenant_id, "onprem", "storage", "onprem-resource-2", 17.80, 200.0),
    ]
