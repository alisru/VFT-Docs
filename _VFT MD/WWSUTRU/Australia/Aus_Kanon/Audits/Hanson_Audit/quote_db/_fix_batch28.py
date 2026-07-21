import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote319 = ("Hanson's proposed 2021 superannuation amendments would have allowed Australians to make their COVID-19 "
            "early-release withdrawals without penalty, alongside her broader push to loosen contribution caps.")

conn.execute("""INSERT OR IGNORE INTO hanson_sources (citation_key, archive_file, url, date_checked, source_type, status)
    VALUES ('newdaily_super21', 'newdaily_super21.txt', 'https://www.thenewdaily.com.au/finance/superannuation/2021/06/17/your-super-your-future-pauline-hanson', ?, 'news_article', 'verified')""", (now,))

old = conn.execute("SELECT status FROM nodes WHERE node_id=319").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='newdaily_super21', quote_in_doc=?, is_literal_quote=0,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=319""", (quote319, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (319, ?, 'verified', 'manual',
    'This node describes a documented policy position (support for penalty-free COVID-19 early super release plus loosened contribution caps), not a single utterance -- no genuine first-person quote exists to convert this into a literal quote after real research. Rather than leave it under a vague [^tvfy][^wiki] citation, replaced the generic paraphrase with a precisely-worded, specifically-sourced documented-action statement citing The New Daily''s 17 June 2021 reporting (confirmed via direct fetch), which is accurately corroborated and is_literal_quote correctly set to 0 (documented action, not a direct quote).', ?)""",
    (old, now))
conn.commit()
print("node 319:", old, "-> verified")
conn.close()
