import duckdb

DB_PATH = "cloudbudget.duckdb"

rows = [
    (1, "EC2", 320.50),
    (2, "S3", 95.20),
    (3, "RDS", 210.10),
]

with duckdb.connect(DB_PATH) as conn:
    conn.executemany("INSERT INTO costs VALUES (?, ?, ?)", rows)

print("Seeded test data")
