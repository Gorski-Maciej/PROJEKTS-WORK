from dataclasses import dataclass


@dataclass
class SimulationResult:
    current_monthly: float
    after_resize: float
    after_migration: float
    estimated_savings: float


def run_what_if_simulation(current_monthly: float, resize_factor: float = 1.0, migration_discount: float = 0.0) -> dict:
    resized = current_monthly * resize_factor
    migrated = resized * (1 - migration_discount)
    result = SimulationResult(
        current_monthly=round(current_monthly, 2),
        after_resize=round(resized, 2),
        after_migration=round(migrated, 2),
        estimated_savings=round(current_monthly - migrated, 2),
    )
    return result.__dict__


def run_provider_migration_simulation(instance_count: int, current_unit_cost: float, target_unit_cost: float) -> dict:
    current = instance_count * current_unit_cost
    target = instance_count * target_unit_cost
    return {
        "instance_count": instance_count,
        "current_cost": round(current, 2),
        "target_cost": round(target, 2),
        "savings": round(current - target, 2),
        "savings_pct": round(((current - target) / current * 100) if current else 0.0, 2),
    }
