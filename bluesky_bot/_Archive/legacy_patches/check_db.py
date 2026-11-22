import sqlite3, os

db_path = os.path.join("bluesky_bot", "memory_store.sqlite")
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print("Tables in memory_store.sqlite:", tables)
for t in tables:
    tname = t[0]
    cur.execute(f"SELECT count(*) FROM {tname}")
    count = cur.fetchone()[0]
    cur.execute(f"PRAGMA table_info({tname})")
    cols = [c[1] for c in cur.fetchall()]
    print(f" - {tname}: {count} rows | cols: {cols}")
conn.close()