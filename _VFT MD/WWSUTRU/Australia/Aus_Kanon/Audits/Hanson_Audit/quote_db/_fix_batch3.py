import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


# refresh/insert sources
sources = [
    ("onenation_bradfield19",
     "https://shop.onenation.org.au/blogs/labor-ldp-plan-to-burn-cane-growers/pauline-hanson-calls-for-construction-of-bradfield-and-ord-schemes-to-drought-proof-inland-australia",
     "onenation_bradfield19.txt", "primary_interview_transcript"),
    ("onenation_nativetitle_sunset", "https://www.onenation.org.au/a-thorough-review-of-the-native-title-system-is-critical",
     "onenation_nativetitle_sunset.txt", "party_platform_statement"),
]
for key, url, fname, stype in sources:
    text = read(ARCH + "\\" + fname)
    conn.execute("""
        INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
        VALUES (?,?,?,?,?,?,?,?,?)
        ON CONFLICT(citation_key) DO UPDATE SET
            archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
            full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
    """, (key, ARCH + "\\" + fname, url, now, text, stype, "verified", 1, now))

node_fixes = [
    (119, "onenation_bradfield19",
     "What I've been pushing for is the Bradfield Scheme that comes from North Queensland, the Herbert, Tully, and the Burdekin Rivers, to actually direct it inland. Flood inland Queensland, flow down to the Murray-Darling, and run it through.",
     "Quote text was already accurate to the real 29 Jan 2019 Sky News interview; the archive file behind [^onenation_bradfield19] had gone dead (404) since this audit was first written, which is what tripped the fabrication flag. Re-verified via a working party-site mirror of the same transcript; quote text unchanged."),
    (341, "onenation_bradfield19",
     "What I've been pushing for is the Bradfield Scheme that comes from North Queensland, the Herbert, Tully, and the Burdekin Rivers, to actually direct it inland... Bring it from the Ord, water inland, Australia from the Ord Scheme as well, and bring water inland and flush out our river systems.",
     "Same root cause as node 119: quote text was already accurate, the archive file was dead. Re-verified via the same working mirror; quote text unchanged."),
    (132, "onenation_bradfield19",
     "Bring it from the Ord, water inland, Australia from the Ord Scheme as well, and bring water inland and flush out our river systems. That's it. That's what I'd be doing.",
     "Quote text was already accurate and even correctly described in-text as the Sky News Paul Murray Live interview, but was mis-cited to the generic [^onenation] hub page rather than the specific interview citation, and that citation's own archive file was separately dead. Re-pointed to the correct, now-working [^onenation_bradfield19] citation; quote text unchanged."),
    (334, "onenation_nativetitle_sunset",
     "One Nation advocates for a thorough review of the entire native title system and proposes a sunset clause on native title claims... Currently, over half of Australia is subject to native title claims, yet less than three percent of Australians have had a voice in this matter.",
     "Original quote claimed a verbatim 26 March 2024 Senate Hansard 'Statements by Senators' passage but was cited to tvfy (a voting-record aggregator with no such text) and could not be verified as written. The underlying claim -- Hanson pushing a native title sunset clause -- is real and well documented; replaced with a directly verified first-person party statement making the same argument, properly archived."),
]

for node_id, key, quote, note in node_fixes:
    old = conn.execute("SELECT status FROM nodes WHERE node_id=?", (node_id,)).fetchone()[0]
    conn.execute("""UPDATE nodes SET citation_key=?, quote_in_doc=?, is_literal_quote=1,
        status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=?""", (key, quote, now, node_id))
    conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
        VALUES (?, ?, 'verified', 'manual', ?, ?)""", (node_id, old, note, now))
    print(f"node {node_id}: {old} -> verified")

conn.commit()
conn.close()
