import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


# --- new source: x_cfmeu26 ---
text = read(ARCH + r"\x_cfmeu26.txt")
conn.execute("""
    INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT(citation_key) DO UPDATE SET
        archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
        full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
""", ("x_cfmeu26", ARCH + r"\x_cfmeu26.txt", "https://x.com/PaulineHansonOz/status/2073208752845820363",
      now, text, "primary_social_post", "verified", 1, now))

# --- node 81: Great Strikes ---
quote81 = ("The criminal CFMEU and other unions now have an effective chokehold on almost all government "
           "payments. It's no wonder that productivity is in freefall... One of our first priorities in "
           "Victoria will be to put in place the measures which will expose and end the CFMEU corruption "
           "enabled by Labor.")
old81 = conn.execute("SELECT status FROM nodes WHERE node_id=81").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='x_cfmeu26', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=81""", (quote81, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (81, ?, 'verified', 'manual',
    'Original quote cited a specific onenation.org.au article (16 Aug 2024) but was only backed by the generic /policies hub archive, which does not contain it. Replaced with a directly verified 4 July 2026 X post making the same anti-CFMEU/anti-union-corruption argument, fully archived.', ?)""",
    (old81, now))

conn.commit()
print("node 81:", old81, "-> verified")
conn.close()
