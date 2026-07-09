#!/usr/bin/env python3
"""One-time (re-run-safe) population of hanson_sources.full_text and
date_checked, now that archive_file paths are correct Windows paths."""
import sqlite3
import os
import datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"

conn = sqlite3.connect(DB)
rows = conn.execute("SELECT citation_key, archive_file FROM hanson_sources").fetchall()
updated, missing = 0, []
for key, archive_file in rows:
    if archive_file and os.path.exists(archive_file):
        with open(archive_file, encoding="utf-8", errors="replace") as f:
            full_text = f.read()
        date_checked = datetime.datetime.fromtimestamp(os.path.getmtime(archive_file)).date().isoformat()
        conn.execute(
            "UPDATE hanson_sources SET full_text=?, date_checked=? WHERE citation_key=?",
            (full_text, date_checked, key),
        )
        updated += 1
    else:
        missing.append((key, archive_file))
conn.commit()

print("updated:", updated)
print("missing archive file:", len(missing))
for key, path in missing:
    print(" ", key, "->", path)

missing_url = conn.execute("SELECT citation_key FROM hanson_sources WHERE url IS NULL").fetchall()
print("missing url:", [r[0] for r in missing_url])

by_type = conn.execute("SELECT source_type, COUNT(*) FROM hanson_sources GROUP BY source_type ORDER BY 2 DESC").fetchall()
for t, c in by_type:
    print(" ", t, c)

conn.close()
