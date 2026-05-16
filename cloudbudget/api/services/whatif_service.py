def simulate_cloud_migration(current_monthly_cost: float, target_discount_pct: float, one_time_migration_cost: float = 0.0) -> dict:
    discounted = current_monthly_cost * (1 - target_discount_pct / 100)
    monthly_savings = current_monthly_cost - discounted
    payback_months = (one_time_migration_cost / monthly_savings) if monthly_savings > 0 else None
    return {
        "current_monthly_cost": round(current_monthly_cost, 2),
        "discounted_monthly_cost": round(discounted, 2),
        "monthly_savings": round(monthly_savings, 2),
        "one_time_migration_cost": round(one_time_migration_cost, 2),
        "payback_months": round(payback_months, 2) if payback_months is not None else None,
    }


def simulate_rightsizing(current_instance_cost: float, utilization_pct: float) -> dict:
    # very simple heuristic: lower utilization implies higher optimization potential
    if utilization_pct < 20:
        factor = 0.5
    elif utilization_pct < 40:
        factor = 0.7
    elif utilization_pct < 60:
        factor = 0.85
    else:
        factor = 0.95
    optimized = current_instance_cost * factor
    return {
        "current_instance_cost": round(current_instance_cost, 2),
        "utilization_pct": round(utilization_pct, 2),
        "optimized_instance_cost": round(optimized, 2),
        "estimated_savings": round(current_instance_cost - optimized, 2),
    }
