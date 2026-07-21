import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
ARCH = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)


def read(fn):
    with open(fn, "r", encoding="utf-8") as f:
        return f.read()


text = read(ARCH + r"\inkl_canetoad19.txt")
conn.execute("""
    INSERT INTO hanson_sources (citation_key, archive_file, url, date_checked, full_text, source_type, status, node_count, last_checked)
    VALUES (?,?,?,?,?,?,?,?,?)
    ON CONFLICT(citation_key) DO UPDATE SET
        archive_file=excluded.archive_file, url=excluded.url, date_checked=excluded.date_checked,
        full_text=excluded.full_text, source_type=excluded.source_type, status=excluded.status, last_checked=excluded.last_checked
""", ("inkl_canetoad19", ARCH + r"\inkl_canetoad19.txt",
      "https://www.inkl.com/news/hanson-s-terrible-cash-for-cane-toads-idea-won-t-work-experts-say",
      now, text, "primary_letter_reported", "verified", 1, now))

fixes = [
    (218, "senate20jm",
     "Another infrastructure scheme worth analysing is Project Iron Boomerang, which would see the construction of steel smelters near the coalfields of Central Queensland and near the iron ore mines of Western Australia, with the two areas connected by rail... It would generate $72 billion in income per year, plus $21 billion in tax revenues annually, and create an estimated 75,000 jobs.",
     "Quote content was already essentially real, just cited to the wrong speech (senate18tax, a 2018 tax debate, which never mentions Iron Boomerang) and lightly paraphrased ('Pilbara and Bowen Basin' instead of the real 'coalfields of Central Queensland... iron ore mines of Western Australia'). The real source, her 10 Nov 2020 'Flawed Jobmaker falls short' speech (senate20jm), was already archived in full and contains this exact paragraph verbatim. Re-pointed citation and restored verbatim wording."),
    (125, "inkl_canetoad19",
     "When rabbits plagued our nation, a sizeable reward was posted for the biological control of the species.",
     "Original quote (the '200 million cane toads' line) was plausible but cited to the generic onenation.org.au hub, which does not contain it, and could not be independently verified as written. Replaced with a directly verified line from the same real Jan 2019 letter to PM Morrison, reported by inkl/news.com.au, which explicitly ties the cane toad crisis to the historical rabbit plague -- an even tighter mechanism match to this vector's own Description text."),
]

for node_id, key, quote, note in fixes:
    old = conn.execute("SELECT status FROM nodes WHERE node_id=?", (node_id,)).fetchone()[0]
    conn.execute("""UPDATE nodes SET citation_key=?, quote_in_doc=?, is_literal_quote=1,
        status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=?""", (key, quote, now, node_id))
    conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
        VALUES (?, ?, 'verified', 'manual', ?, ?)""", (node_id, old, note, now))
    print(f"node {node_id}: {old} -> verified")

conn.commit()
conn.close()
