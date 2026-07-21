import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote240 = ("You made a comment that reports are handed in from these corporations. Why is that 1,258 Aboriginal "
            "and Torres Strait Islander corporations failed to lodge mandatory reports for the 2023-24 year? "
            "How many of these failed corporations are your agency still dealing with?")

conn.execute("""INSERT OR IGNORE INTO hanson_sources (citation_key, archive_file, url, date_checked, source_type, status)
    VALUES ('senate_estimates_oct25', 'senate_estimates_oct25.txt', 'https://checkhansard.com.au/speech/484533', ?, 'hansard_estimates', 'verified')""", (now,))

old = conn.execute("SELECT status FROM nodes WHERE node_id=240").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='senate_estimates_oct25', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=240""", (quote240, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (240, ?, 'verified', 'manual',
    'Quote was a third-person paraphrase of a One Nation press release, not a direct quote. Located the actual verbatim Hansard exchange (Senate Estimates, Finance and Public Administration Legislation Committee, 7 October 2025) via checkhansard.com.au, in which Hanson directly cites the 1,258-corporations figure in her own words. Archived as senate_estimates_oct25 and replaced the paraphrase with the genuine direct quote.', ?)""",
    (old, now))
conn.commit()
print("node 240:", old, "-> verified")
conn.close()
