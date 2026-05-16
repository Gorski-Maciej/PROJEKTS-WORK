from __future__ import annotations

from collections import defaultdict

try:
    import polars as pl
except Exception:
    pl = None


_PROVIDER_PRICE_FACTOR = {
    "aws": 1.00,
    "azure": 0.95,
    "gcp": 0.92,
    "onprem": 0.78,
    "kubernetes": 0.88,
}


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


def simulate_architecture_migration(records: list[dict], provider_from: str, provider_to: str, server_count: int) -> dict:
    if provider_from not in _PROVIDER_PRICE_FACTOR or provider_to not in _PROVIDER_PRICE_FACTOR:
        raise ValueError("Unsupported provider")
    if server_count <= 0:
        raise ValueError("server_count must be positive")

    if not records:
        return {"baseline_monthly_cost": 0.0, "projected_monthly_cost": 0.0, "monthly_savings": 0.0, "migrated_servers": server_count}

    if pl is not None:
        df = pl.DataFrame(records)
        baseline = float(df["amount_usd"].sum())
        from_df = df.filter(pl.col("provider") == provider_from)
        migrated_pool = float(from_df["amount_usd"].sum()) if not from_df.is_empty() else 0.0
        total_servers = max(len(from_df), 1)
        iter_rows = df.iter_rows(named=True)
    else:
        baseline = sum(float(r.get("amount_usd", 0.0)) for r in records)
        from_rows = [r for r in records if r.get("provider") == provider_from]
        migrated_pool = sum(float(r.get("amount_usd", 0.0)) for r in from_rows)
        total_servers = max(len(from_rows), 1)
        iter_rows = records

    moved_fraction = min(server_count / total_servers, 1.0)
    moved_cost = migrated_pool * moved_fraction

    normalized_on_target = moved_cost * (_PROVIDER_PRICE_FACTOR[provider_to] / _PROVIDER_PRICE_FACTOR[provider_from])
    projected = baseline - moved_cost + normalized_on_target

    by_provider = defaultdict(float)
    for row in iter_rows:
        by_provider[row["provider"]] += float(row["amount_usd"])
    by_provider[provider_from] = max(by_provider[provider_from] - moved_cost, 0.0)
    by_provider[provider_to] += normalized_on_target

    return {
        "baseline_monthly_cost": round(baseline, 2),
        "projected_monthly_cost": round(projected, 2),
        "monthly_savings": round(baseline - projected, 2),
        "migrated_servers": server_count,
        "provider_breakdown": {k: round(v, 2) for k, v in by_provider.items()},
    }
