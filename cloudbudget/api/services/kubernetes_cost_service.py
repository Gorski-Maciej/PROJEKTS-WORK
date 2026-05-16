from dataclasses import dataclass


@dataclass
class NamespaceCost:
    namespace: str
    cpu_cost: float
    memory_cost: float

    @property
    def total(self) -> float:
        return round(self.cpu_cost + self.memory_cost, 2)


def estimate_k8s_namespace_costs(rows: list[dict], cpu_price_per_core_hour: float = 0.04, mem_price_per_gb_hour: float = 0.005) -> list[dict]:
    output: list[dict] = []
    for row in rows:
        ns = row.get("namespace", "default")
        cpu_hours = float(row.get("cpu_core_hours", 0))
        mem_gb_hours = float(row.get("memory_gb_hours", 0))
        item = NamespaceCost(
            namespace=ns,
            cpu_cost=round(cpu_hours * cpu_price_per_core_hour, 2),
            memory_cost=round(mem_gb_hours * mem_price_per_gb_hour, 2),
        )
        output.append({"namespace": item.namespace, "cpu_cost": item.cpu_cost, "memory_cost": item.memory_cost, "total": item.total})
    return output
