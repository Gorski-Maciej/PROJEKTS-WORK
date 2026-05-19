import duckdb
import os

def init_db():
    path = os.getenv("DUCKDB_PATH", "/data/cloudbudget.duckdb")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    con = duckdb.connect(path)
    con.execute("CREATE TABLE IF NOT EXISTS costs (id INTEGER, service VARCHAR, amount FLOAT, date DATE)")
    con.execute("CREATE TABLE IF NOT EXISTS resources (id VARCHAR, type VARCHAR, status VARCHAR)")
    con.close()
