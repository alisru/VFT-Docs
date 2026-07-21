import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


text = read(ARCH + r"\sbs_bushfire20.txt")
conn.execute("""
    INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT(citation_key) DO UPDATE SET
        archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
        full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
""", ("sbs_bushfire20", ARCH + r"\sbs_bushfire20.txt",
      "https://www.sbs.com.au/news/article/lets-look-at-the-pure-facts-pauline-hanson-denies-bushfires-caused-by-climate-change/ptsl0tuib",
      now, text, "primary_news_report_with_verbatim_quote", "verified", 1, now))

quote144 = ("It's a build up of the fuel over the period of time, thirty plus years that it's come to the state now. "
            "If you're gonna have a royal commission into it, throw bloody climate change out the window and let's "
            "look at the pure facts of why we have had the bushfires, how they were handled, what we can do better, "
            "to stop it happening again.")
old144 = conn.execute("SELECT status FROM nodes WHERE node_id=144").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='sbs_bushfire20', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=144""", (quote144, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (144, ?, 'verified', 'manual',
    'Quote content was real (12 Jan 2020 Today show remarks on bushfire fuel loads) but was reordered/truncated with an unverifiable ellipsis and cited to [^tvfy] (voting-record site, not the actual interview source). Verified full verbatim wording via SBS News report and a corroborating Facebook video re-post, restored correct chronological order, and re-cited to sbs_bushfire20. Content/verdict unchanged -- the node''s Description/Justification already correctly frame this as an analogical (fuel-load vs. ore-extraction) reading of the Opencut vector, not a topical mismatch requiring a verdict rewrite.', ?)""",
    (old144, now))

conn.commit()
print("node 144:", old144, "-> verified")
conn.close()
