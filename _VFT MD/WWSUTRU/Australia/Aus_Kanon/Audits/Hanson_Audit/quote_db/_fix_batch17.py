import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote97 = ("I want to say something clearly, because Australians deserve honesty and respect. At ANZAC Day "
           "services across the country, some booed the Welcome to Country. I don't support that. ANZAC Day "
           "should never be disrupted. It's a sacred day to honour the men and women who gave everything for our country.")

conn.execute("""INSERT OR IGNORE INTO hanson_sources (citation_key, archive_file, url, date_checked, source_type, status)
    VALUES ('x_anzac25', 'x_anzac25.txt', 'https://x.com/PaulineHansonOz/status/1915651025341735280', ?, 'social_media', 'verified')""", (now,))

old = conn.execute("SELECT status FROM nodes WHERE node_id=97").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='x_anzac25', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=97""", (quote97, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (97, ?, 'verified', 'manual',
    'Quote was already fully verbatim but generically cited to [^wiki] with a vague "public statement (2026)" attribution. Confirmed the exact wording against Hanson''s official X/Twitter post of 25 April 2025 (ANZAC Day), archived new source x_anzac25, and re-cited/re-dated accordingly.', ?)""",
    (old, now))
conn.commit()
print("node 97:", old, "-> verified")
conn.close()
