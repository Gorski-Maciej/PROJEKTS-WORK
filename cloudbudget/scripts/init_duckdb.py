"""Initialize CloudBudget DuckDB schema for local development.

Run:
    python cloudbudget/scripts/init_duckdb.py
"""

from __future__ import annotations

import os
from pathlib import Path

import duckdb


def main() -> None:
    db_path = Path(os.getenv("DUCKDB_PATH", "cloudbudget.duckdb"))
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect(str(db_path))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cost_events (
            id VARCHAR,
            tenant_id VARCHAR NOT NULL,
            provider VARCHAR NOT NULL,
            service VARCHAR,
            resource_id VARCHAR,
            amount_usd DOUBLE NOT NULL,
            currency VARCHAR DEFAULT 'USD',
            usage_quantity DOUBLE,
            usage_unit VARCHAR,
            region VARCHAR,
            tags JSON,
            occurred_at TIMESTAMP NOT NULL,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cost_daily_agg AS
        SELECT
            tenant_id,
            provider,
            DATE(occurred_at) AS cost_date,
            SUM(amount_usd) AS total_amount_usd,
            COUNT(*) AS events_count
        FROM cost_events
        GROUP BY 1,2,3
        LIMIT 0;
        """
    )
    conn.close()
    print(f"Initialized DuckDB schema at: {db_path}")


if __name__ == "__main__":
    main()
