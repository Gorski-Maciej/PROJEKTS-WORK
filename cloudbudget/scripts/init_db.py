from pathlib import Path

import duckdb

DB_PATH = Path("cloudbudget.duckdb")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

with duckdb.connect(str(DB_PATH)) as conn:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS costs (
            id INTEGER,
            service VARCHAR,
            monthly_cost DOUBLE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER,
            name VARCHAR,
            resource_type VARCHAR,
            monthly_cost DOUBLE
        )
        """
    )

print(f"Initialized schema in {DB_PATH}")
