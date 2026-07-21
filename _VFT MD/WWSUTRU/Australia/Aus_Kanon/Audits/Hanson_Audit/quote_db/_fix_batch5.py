import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


text = read(ARCH + r"\tvfy_marine.txt")
conn.execute("""
    INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT(citation_key) DO UPDATE SET
        archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
        full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
""", ("tvfy_marine", ARCH + r"\tvfy_marine.txt",
      "https://theyvoteforyou.org.au/people/senate/queensland/pauline_hanson/policies/17",
      now, text, "voting_record_specific", "verified", 1, now))

quote111 = ("Voted No to disallow the Marine Parks Network Management Plan (16 Aug 2018), No on a Great Barrier "
            "Reef climate change motion (27 Feb 2020), No on Great Australian Bight World Heritage listing "
            "(25 Jun 2018), absent for motions to ban offshore oil and gas exploration and to protect Ningaloo "
            "Reef, Shark Bay, and the Exmouth Gulf (2020).")
old111 = conn.execute("SELECT status FROM nodes WHERE node_id=111").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='tvfy_marine', quote_in_doc=?, is_literal_quote=0,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=111""", (quote111, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (111, ?, 'verified', 'manual',
    'Original entry was an honest bracketed paraphrase (not a fabricated literal quote) but cited to the generic tvfy profile page rather than a specific voting record, and had no individually checkable divisions. Replaced with the specific, itemised marine-conservation voting record page, listing named bills, dates, and how she voted on each.', ?)""",
    (old111, now))

conn.commit()
print("node 111:", old111, "-> verified")
conn.close()
