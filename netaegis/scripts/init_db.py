from pathlib import Path
import sqlite3

DB=Path("/app/data/netaegis.sqlite3")
DB.parent.mkdir(parents=True, exist_ok=True)
conn=sqlite3.connect(DB)
conn.execute("CREATE TABLE IF NOT EXISTS healthcheck (id INTEGER PRIMARY KEY, ts TEXT DEFAULT CURRENT_TIMESTAMP)")
conn.commit(); conn.close()
print(f"Initialized {DB}")
