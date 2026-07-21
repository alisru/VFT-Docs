import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote320 = ("I've spoken before about the need to break our universities of their addiction to foreign students. "
            "My concern has always been about the welfare of Australian students and the huge impact of foreign "
            "students on housing demand, but my stance is also about the best interests of the universities themselves.")

conn.execute("""INSERT OR IGNORE INTO hanson_sources (citation_key, archive_file, url, date_checked, source_type, status)
    VALUES ('senate_universities26', 'senate_universities26.txt', 'https://www.openaustralia.org.au/senate/?id=2026-07-01.55.1&m=100857', ?, 'hansard', 'verified')""", (now,))

old = conn.execute("SELECT status FROM nodes WHERE node_id=320").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='senate_universities26', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=320""", (quote320, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (320, ?, 'verified', 'manual',
    'Quote was a third-person paraphrase generically cited to [^wiki] as "Senate committee contributions, 2019-2021". Located a genuine, verbatim, on-point Senate Hansard statement (1 July 2026, Statements by Senators: Universities) confirmed via direct fetch of the OpenAustralia.org Hansard mirror, and replaced the paraphrase with the real quote.', ?)""",
    (old, now))
conn.commit()
print("node 320:", old, "-> verified")
conn.close()
