import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


text = read(ARCH + r"\sbs_canetoad19.txt")
conn.execute("""
    INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT(citation_key) DO UPDATE SET
        archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
        full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
""", ("sbs_canetoad19", ARCH + r"\sbs_canetoad19.txt",
      "https://www.sbs.com.au/news/article/cane-toad-kill-reward-spruiked-by-hanson/y11ailtxt",
      now, text, "primary_interview_reported", "verified", 1, now))

quote128 = ("As far as I know there's no cane toads in Canberra yet. Get the inquiry up in Queensland, get the "
            "real people who know what to do about this.")
old128 = conn.execute("SELECT status FROM nodes WHERE node_id=128").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='sbs_canetoad19', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=128""", (quote128, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (128, ?, 'verified', 'manual',
    'Quote was already 100 percent verbatim accurate (confirmed against the real 9 Jan 2019 SBS News article) but was cited to the generic onenation.org.au hub instead of the actual article. Re-pointed citation only; quote text unchanged.', ?)""",
    (old128, now))

conn.commit()
print("node 128:", old128, "-> verified")
conn.close()
