import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


text = read(ARCH + r"\stockandland26.txt")
conn.execute("""
    INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT(citation_key) DO UPDATE SET
        archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
        full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
""", ("stockandland26", ARCH + r"\stockandland26.txt",
      "https://www.stockandland.com.au/story/9256154/pauline-hanson-demands-a-total-ban-on-foreign-farmland-ownership",
      now, text, "primary_interview_reported", "verified", 1, now))

quote225 = ("I don't believe foreigners should own any housing in Australia or our farming land... My attitude "
            "is, I would stop them and I'd give you two years to sell your product. If you don't, it will be "
            "repossessed by the government.")
old225 = conn.execute("SELECT status FROM nodes WHERE node_id=225").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='stockandland26', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, hit_fail='HIT', last_checked=? WHERE node_id=225""", (quote225, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (225, ?, 'verified', 'manual',
    'Deeper problem than a bad citation: the original node reused a quote about Chinese-government land purchases wrongly cited to senate18prot (a 2018 immigration speech that never mentions foreign ownership), AND its Description/Justification paragraphs were about the state education system -- copy-pasted from an unrelated node -- while the Actuality paragraph was correctly about the wool/pastoral economy and already said HIT, contradicting the header FAIL verdict. Rewrote the full node: verdict corrected to HIT (matching the real Actuality evidence), Description/Justification rewritten on-topic, quote replaced with a verified 24 May 2026 interview where Hanson demands a total foreign farmland ownership ban with government repossession.', ?)""",
    (old225, now))

conn.commit()
print("node 225:", old225, "-> verified (verdict corrected FAIL->HIT)")
conn.close()
