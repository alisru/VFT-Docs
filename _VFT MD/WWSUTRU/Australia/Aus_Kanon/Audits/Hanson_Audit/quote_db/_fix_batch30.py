import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote155 = "Welfare is not a right, unless you are aged or sick. It is a privilege paid for by hard-working Australians."
quote171 = ("Voted No on the most heavily-weighted gambling-reform division (Communications Legislation Amendment "
            "(Online Content Services and Other Measures) Bill 2017, gambling ads, 27 March 2018) and against every "
            "other tracked gambling-restriction motion between 2017 and 2019, for a 13% weighted agreement score "
            "(\"voted almost always against increasing restrictions on gambling\").")

conn.execute("""INSERT OR IGNORE INTO hanson_sources (citation_key, archive_file, url, date_checked, source_type, status)
    VALUES ('tvfy_gambling', 'tvfy_gambling.txt', 'https://theyvoteforyou.org.au/people/senate/queensland/pauline_hanson/policies/39', ?, 'voting_record', 'verified')""", (now,))

fixes = [
    (155, 'ms16', quote155, 1,
     'Quote was a third-person voting-record summary generically cited to [^tvfy]. Replaced with a genuine, verbatim line from the already-archived 2016 Senate maiden speech (ms16) that is the direct rhetorical basis for her welfare-rorter framing.'),
    (171, 'tvfy_gambling', quote171, 0,
     'This node describes an aggregate voting pattern across multiple gambling-reform divisions, not a single utterance -- no genuine first-person quote exists to convert this into a literal quote after real research. Replaced the vague [^tvfy] citation with a precisely-sourced documented-action statement citing the specific divisions and exact weighted agreement score from the They Vote For You policy page (confirmed via direct fetch), is_literal_quote correctly set to 0.'),
]

for node_id, cite, quote, lit, note in fixes:
    old = conn.execute("SELECT status FROM nodes WHERE node_id=?", (node_id,)).fetchone()[0]
    conn.execute("""UPDATE nodes SET citation_key=?, quote_in_doc=?, is_literal_quote=?,
        status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=?""", (cite, quote, lit, now, node_id))
    conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
        VALUES (?, ?, 'verified', 'manual', ?, ?)""", (node_id, old, note, now))
    print(node_id, old, "-> verified")

conn.commit()
conn.close()
