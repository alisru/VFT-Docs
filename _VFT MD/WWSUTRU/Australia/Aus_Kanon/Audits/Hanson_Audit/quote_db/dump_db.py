#!/usr/bin/env python3
import sqlite3

DB_PATH = "/tmp/quote_verification.db"
DUMP_PATH = "/tmp/quote_verification_dump.sql"

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    with open(DUMP_PATH, "w", encoding="utf-8") as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")
    conn.close()
    print(f"dumped -> {DUMP_PATH}")
