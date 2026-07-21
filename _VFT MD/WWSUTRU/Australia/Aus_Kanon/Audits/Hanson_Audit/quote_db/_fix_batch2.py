import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


for key, url, fname, stype in [
    ("7news_border20", "https://www.facebook.com/7NEWSQld/videos/879513852558163/", "7news_border20.txt", "primary_interview"),
    ("armstrong20", "https://www.armstronglegal.com.au/open-the-borders-a-high-court-australia-constitutional-challenge/", "armstrong20.txt", "secondary_legal_commentary"),
]:
    text = read(ARCH + "\\" + fname)
    conn.execute("""
        INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
        VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(citation_key) DO UPDATE SET
            archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
            full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
    """, (key, ARCH + "\\" + fname, url, now, text, stype, "verified", 1, now))

quote56 = ("Under section 92 of the Australian Constitution... they can't close the borders for trade or "
           "commerce or the free movement of people.")
old56 = conn.execute("SELECT status FROM nodes WHERE node_id=56").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='7news_border20', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=56""", (quote56, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (56, ?, 'verified', 'manual',
    'Original quote claimed a verbatim Section 117 citation in a 5 Aug 2021 Senate Hansard committee debate, but was only backed by the thin tvfy (voting-record aggregator) archive text, which does not contain it -- could not verify as written. Replaced with a genuinely verified 26 May 2020 quote where Hanson invokes Section 92 (not 117) to argue Queensland COVID border closures are unconstitutional, and organised a High Court challenge over it. Same horizontal-citizenship/free-movement mechanism as the vector, different constitutional clause than the ideal quotes -- flagged explicitly in the Justification rather than glossed over.', ?)""",
    (old56, now))

conn.commit()
print("node 56:", old56, "-> verified")
conn.close()
