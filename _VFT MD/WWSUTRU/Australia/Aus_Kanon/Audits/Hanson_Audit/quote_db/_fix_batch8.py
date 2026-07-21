import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


text = read(ARCH + r"\tvfy_nauru.txt")
conn.execute("""
    INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT(citation_key) DO UPDATE SET
        archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
        full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
""", ("tvfy_nauru", ARCH + r"\tvfy_nauru.txt",
      "https://theyvoteforyou.org.au/people/senate/queensland/pauline_hanson/policies/118",
      now, text, "voting_record_specific", "verified", 1, now))

quote134 = ("Voted Yes on the Instrument of Designation of the Republic of Nauru as a Regional Processing "
            "Country (7 Feb 2023), voted No on ending offshore detention (15 Feb 2018) and on closing the "
            "Nauru and Manus Island detention centres (20 Jun 2017).")
old134 = conn.execute("SELECT status FROM nodes WHERE node_id=134").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='tvfy_nauru', quote_in_doc=?, is_literal_quote=0,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=134""", (quote134, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (134, ?, 'verified', 'manual',
    'Original entry presented an unverifiable literal Hansard quote cited to tvfy, which cannot support literal wording. The underlying 7 Feb 2023 Nauru motion is real (confirmed against TheyVoteForYou divisions), but rather than assert unverified exact wording, converted to a documented-action citation against the specific, itemised offshore-detention voting record.', ?)""",
    (old134, now))

conn.commit()
print("node 134:", old134, "-> verified")
conn.close()
