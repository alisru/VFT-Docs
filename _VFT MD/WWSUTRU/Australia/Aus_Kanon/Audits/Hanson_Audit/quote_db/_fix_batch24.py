import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote246 = "That the Senate calls on the Federal Government to reject critical race theory from the national curriculum."

conn.execute("""INSERT OR IGNORE INTO hanson_sources (citation_key, archive_file, url, date_checked, source_type, status)
    VALUES ('tvfy_crt21', 'tvfy_crt21.txt', 'https://theyvoteforyou.org.au/divisions/senate/2021-06-21/6', ?, 'division_record', 'verified')""", (now,))

old = conn.execute("SELECT status FROM nodes WHERE node_id=246").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='tvfy_crt21', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=246""", (quote246, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (246, ?, 'verified', 'manual',
    'Quote was a third-person paraphrase of a Conversation article describing the vote, not a direct Hanson quote. Located the actual verbatim text of the Senate motion Hanson moved (via They Vote For You division record, corroborated by the OpenAustralia Hansard debate link) and replaced the paraphrase with the genuine motion wording in quotation marks.', ?)""",
    (old, now))
conn.commit()
print("node 246:", old, "-> verified")
conn.close()
