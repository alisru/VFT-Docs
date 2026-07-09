#!/usr/bin/env python3
import sys
import sqlite3

DB_PATH = "/tmp/quote_verification.db"
DEFAULT_DUMP_PATH = "/tmp/quote_verification_dump.sql"

if __name__ == "__main__":
    dump_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DUMP_PATH
    with open(dump_path, encoding="utf-8") as f:
        sql = f.read()
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(sql)
    conn.commit()
    n = conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    conn.close()
    print(f"restored -> {DB_PATH} ({n} node rows)")
