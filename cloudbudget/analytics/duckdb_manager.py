import duckdb


def get_connection(path: str = "cloudbudget.duckdb"):
    return duckdb.connect(path)


def init_olap_schema(path: str = "cloudbudget.duckdb"):
    con = get_connection(path)
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS costs (
          tenant_id INTEGER,
          provider VARCHAR,
          service VARCHAR,
          resource_id VARCHAR,
          amount_usd DOUBLE,
          usage_quantity DOUBLE,
          collected_at TIMESTAMP
        )
        """
    )
    con.close()
