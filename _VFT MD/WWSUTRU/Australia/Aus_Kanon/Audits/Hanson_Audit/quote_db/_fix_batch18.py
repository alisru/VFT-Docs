import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

conn.execute("""INSERT OR IGNORE INTO hanson_sources (citation_key, archive_file, url, date_checked, source_type, status)
    VALUES ('senatorhanson_bradfield19', 'senatorhanson_bradfield19.txt', 'https://www.senatorhanson.com.au/2019/11/01/pauline-hanson-supports-bradfield-scheme-but-china-cant-own-it/', ?, 'media_release', 'verified')""", (now,))

old = conn.execute("SELECT status FROM nodes WHERE node_id=116").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='senatorhanson_bradfield19', is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=116""", (now,))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (116, ?, 'verified', 'manual',
    'Quote text was already fully verbatim and correctly dated but generically cited to [^wiki]. Fetched the original 1 Nov 2019 senatorhanson.com.au media release directly, confirmed exact wording, archived as senatorhanson_bradfield19, and re-cited.', ?)""",
    (old, now))
conn.commit()
print("node 116:", old, "-> verified")
conn.close()
