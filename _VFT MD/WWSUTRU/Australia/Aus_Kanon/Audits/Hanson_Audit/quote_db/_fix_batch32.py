import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote44 = "We are all here now and we have to solve our differences and live together as Australians."

conn.execute("""INSERT OR IGNORE INTO hanson_sources (citation_key, archive_file, url, date_checked, source_type, status)
    VALUES ('odonoghue_aoy', 'odonoghue_aoy.txt', 'https://racismnoway.com.au/teaching-resources/professor-lowitja-lois-odonoghue-am-cbe/', ?, 'biography', 'verified')""", (now,))

old = conn.execute("SELECT status FROM nodes WHERE node_id=44").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='odonoghue_aoy', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=44""", (quote44, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (44, ?, 'verified', 'manual',
    'This node (a First Nations Perspective shadow entry, not a Hanson quote) had no citation_key at all -- the quote "We have survived the lot. We are still here." attributed to Lowitja O''Donoghue could not be verified anywhere after real research and appears to be conflated with a similar-sounding No Fixed Address song lyric. Restarted the node per the no-fabrication rule: replaced with a genuine, verbatim, properly sourced Lowitja O''Donoghue quote (confirmed via direct fetch of a NSW Department of Education biography page) that fits the same Survival/persistence mechanism.', ?)""",
    (old, now))
conn.commit()
print("node 44:", old, "-> verified")
conn.close()
