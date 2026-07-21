import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


text = read(ARCH + r"\fb_familylaw21.txt")
conn.execute("""
    INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT(citation_key) DO UPDATE SET
        archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
        full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
""", ("fb_familylaw21", ARCH + r"\fb_familylaw21.txt",
      "https://www.facebook.com/PaulineHansonAu/videos/why-we-need-to-stop-demonising-men-and-reform-the-family-law-system/4094829733888469/",
      now, text, "primary_video_statement", "verified", 1, now))

quote87 = ("If the cost of raising children was better shared, we would see fewer people withholding children "
           "from the other parent for financial gain through child support. I also believe more parents will "
           "work instead of opting for the dole to avoid paying child support.")
old87 = conn.execute("SELECT status FROM nodes WHERE node_id=87").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='fb_familylaw21', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=87""", (quote87, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (87, ?, 'verified', 'manual',
    'Original quote claimed to be from Hanson''s Dissenting Report as Deputy Chair of the Joint Select Committee on Australia''s Family Law System -- a real position she held (confirmed via IPEA parliamentary records) -- but was cited to tvfy and the literal report wording could not be verified. Replaced with a directly verified 16 March 2021 Facebook statement making the same shared-responsibility/child-support argument.', ?)""",
    (old87, now))

conn.commit()
print("node 87:", old87, "-> verified")
conn.close()
