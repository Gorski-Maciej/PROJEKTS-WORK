import sqlite3, os
os.makedirs("/app/data", exist_ok=True)
conn = sqlite3.connect("/app/data/netaegis.db")
conn.execute("CREATE TABLE IF NOT EXISTS alerts (id TEXT PRIMARY KEY, message TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
conn.close()
print("Database initialized")
