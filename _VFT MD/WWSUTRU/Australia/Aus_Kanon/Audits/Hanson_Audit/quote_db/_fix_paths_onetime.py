#!/usr/bin/env python3
"""One-time fix: convert sandbox-mount paths stored in archive_file columns
(from when this DB was first built inside the Linux sandbox) into real
Windows paths, so Desktop Commander (running natively on Windows) can
actually find the files."""
import sqlite3
import os

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
OLD_PREFIX = "/sessions/sharp-jolly-carson/mnt/Aus_Kanon"
NEW_PREFIX = "E:\\Vector Field Theory\\VFT Docs\\_VFT MD\\WWSUTRU\\Australia\\Aus_Kanon"

def fix(path):
    if path and path.startswith(OLD_PREFIX):
        rest = path[len(OLD_PREFIX):]
        return NEW_PREFIX + rest.replace("/", "\\")
    return path

conn = sqlite3.connect(DB)
for table, col in [("nodes", "archive_file"), ("hanson_sources", "archive_file")]:
    rows = conn.execute(f"SELECT rowid, {col} FROM {table} WHERE {col} IS NOT NULL").fetchall()
    n = 0
    for rowid, val in rows:
        newval = fix(val)
        if newval != val:
            conn.execute(f"UPDATE {table} SET {col}=? WHERE rowid=?", (newval, rowid))
            n += 1
    print(table, "fixed", n, "of", len(rows))
conn.commit()

sample = conn.execute("SELECT archive_file FROM hanson_sources WHERE citation_key='ms16'").fetchone()
print("sample path:", sample[0])
print("exists now:", os.path.exists(sample[0]))
conn.close()
