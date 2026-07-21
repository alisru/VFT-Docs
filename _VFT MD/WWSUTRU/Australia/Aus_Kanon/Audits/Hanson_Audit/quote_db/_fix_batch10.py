import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


sources = [
    ("onenation_wtc24", ARCH + r"\onenation_wtc24.txt",
     "https://www.onenation.org.au/lies-hanson-urges-aussies-to-ignore-welcome-to-country",
     "primary_news_statement"),
    ("senate23water", ARCH + r"\senate23water.txt",
     "https://parlinfo.aph.gov.au/parlInfo/genpdf/chamber/hansards/27146/0198/hansard_frag.pdf;fileType=application/pdf",
     "primary_hansard_speech"),
]
for key, path, url, stype in sources:
    text = read(path)
    conn.execute("""
        INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
        VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(citation_key) DO UPDATE SET
            archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
            full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
    """, (key, path, url, now, text, stype, "verified", 1, now))

# Node 29 - Sport - quote fully verified verbatim, only the citation was wrong/generic (dead policies page)
quote29 = ("These welcomes are based on lies that Australia is not our home. "
           "So many people tell me they are just over it.")
old29 = conn.execute("SELECT status FROM nodes WHERE node_id=29").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='onenation_wtc24', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=29""", (quote29, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (29, ?, 'verified', 'manual',
    'Quote was 100 percent verbatim-correct but cited to [^onenation], a dead generic policies-page link unrelated to the actual statement. Verified the exact quote on One Nation''s own site (18 Sept 2024 article on the AFL Welcome to Country controversy) and re-cited to a new specific source, onenation_wtc24.', ?)""",
    (old29, now))

# Node 73 - The Colonial Survey - quote fully verified verbatim via official Hansard PDF fragment; expanded to full first sentence
quote73 = ("With the exception of the need to support extended deadlines and the greater transparency and "
           "compliance measures in the water market, you can bet the farm that One Nation will not be supporting "
           "this bill. The Water Amendment (Restoring Our Rivers) Bill 2023 is gambling with the farms in a region "
           "that produces more than $22 billion worth of Australia's food and fibre, gambling with the fate of "
           "this production in the Murray-Darling Basin while stacking the odds against it.")
old73 = conn.execute("SELECT status FROM nodes WHERE node_id=73").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='senate23water', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=73""", (quote73, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (73, ?, 'verified', 'manual',
    'Quote was cited to [^tvfy] (a voting-record site, not a speech-transcript source) rather than the actual Hansard record, and was truncated with an unverified ellipsis. Located the official Senate Hansard PDF fragment for the 27 Nov 2023 second-reading speech (page 6024) and confirmed the quote verbatim, extending it to the full first sentence. Corroborated by Hanson''s recorded No vote on the bill''s passage, 30 Nov 2023.', ?)""",
    (old73, now))

conn.commit()
print("node 29:", old29, "-> verified")
print("node 73:", old73, "-> verified")
conn.close()
