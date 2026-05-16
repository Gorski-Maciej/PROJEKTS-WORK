import polars as pl


def aggregate_costs(rows: list[dict]) -> list[dict]:
    if not rows:
        return []
    df = pl.DataFrame(rows)
    out = (
        df.group_by(["tenant_id", "provider", "service"])
        .agg(pl.col("amount_usd").sum().alias("total_amount_usd"))
        .sort(["tenant_id", "total_amount_usd"], descending=[False, True])
    )
    return out.to_dicts()
