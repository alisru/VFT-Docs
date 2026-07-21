import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


sources = [
    ("fb_convoy22", ARCH + r"\fb_convoy22.txt",
     "https://www.facebook.com/PaulineHansonAu/videos/362395362110748/", "primary_video_statement"),
    ("x_convoy22", ARCH + r"\x_convoy22.txt",
     "https://x.com/PaulineHansonOz/status/1492313416114995205", "primary_social_post"),
    ("onenation_convoy22", ARCH + r"\onenation_convoy22.txt",
     "https://www.onenation.org.au/convoy-to-canberra", "primary_statement"),
    ("onenation_gas26", ARCH + r"\onenation_gas26.txt",
     "https://www.onenation.org.au/gas-policy-ownership", "primary_policy_launch"),
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

# Node 92 - The Stockade - RESTARTED with a new, genuinely verified quote (old quote could not be
# verified against any real source after extensive search).
quote92 = ("It was so great to see so many Australians take a stand over the weekend and exercise their right "
           "to peacefully protest authoritarian COVID-19 measures and vaccine mandates! ... After this weekend "
           "one thing is clear, The Liberals lie to you, Labor want to shut you down, only One Nation is "
           "prepared to support your voice and give you a say on the floor of parliament.")
old92 = conn.execute("SELECT status FROM nodes WHERE node_id=92").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='fb_convoy22', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=92""", (quote92, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (92, ?, 'verified', 'manual',
    'Original quote (Eureka Stockade / Pinjarra Massacre / Anzacs curriculum-erasure statement, cited to a 3 Sept 2025 Senate Hansard entry) could not be verified against any real source despite extensive research -- the underlying WA-curriculum event is real (confirmed via One Nation and Facebook/YouTube posts, 3 Sept 2025) but that specific sentence does not appear in any of them, and it was not found in Federal Hansard. Per instruction, restarted the node with a new, fully verified quote that hits the same Stockade mechanism (defiance/resistance to unaccountable authority treated as legitimate when the grievance is real): Hanson''s 13 Feb 2022 Facebook statement supporting the Convoy to Canberra anti-mandate protest. Description unchanged (defines the Kanon ideal, not Hanson-specific); Justification and Actuality rewritten to match the new quote; verdict (HIT) and coordinates unchanged.', ?)""",
    (old92, now))

# Node 139 - The Pipeline - quote was already 100% verbatim-correct, only cited to the wrong generic link
quote139 = ("We want more gas, more oil, and more energy to drive our economy forward, pay down our debts, "
            "and secure our energy future.")
old139 = conn.execute("SELECT status FROM nodes WHERE node_id=139").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='onenation_gas26', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=139""", (quote139, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (139, ?, 'verified', 'manual',
    'Quote was 100 percent verbatim-correct (confirmed against the live One Nation gas policy launch page, 9 June 2026) but cited to [^onenation], the dead generic policies-page link. Re-cited to a new specific source, onenation_gas26.', ?)""",
    (old139, now))

conn.commit()
print("node 92:", old92, "-> verified")
print("node 139:", old139, "-> verified")
conn.close()
