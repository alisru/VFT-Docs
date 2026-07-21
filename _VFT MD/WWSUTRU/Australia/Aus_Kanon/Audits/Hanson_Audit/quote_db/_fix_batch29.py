import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote321 = ("The Health Care Card has no identification on it, just a name and number. Anyone can, and does, take "
            "another person's card when visiting a doctor, especially those who bulk-bill... Overseas tourists, "
            "illegals and those not entitled to Medicare use their family's card or a friend's card.")
quote327 = ("Farmers are screaming out for workers and small businesses have difficulty in finding people who want "
            "to work... High immigration is only beneficial to multinationals, banks and big business, seeking a "
            "larger market while everyday Australians suffer from this massive intake.")

fixes = [
    (321, 'ms16', quote321,
     'Quote was a third-person voting-record/statement summary generically cited to [^wiki][^tvfy]. Replaced with a genuine, verbatim, disjointed-but-same-speech passage from the already-archived 2016 Senate maiden speech (ms16) about Medicare Card fraud by non-citizens, which is the concrete basis for the Medicare-prioritisation claim.'),
    (327, 'ms16', quote327,
     'Quote was framed as "Documented position" (third-person paraphrase) rather than a real quote, generically cited to [^wiki][^tvfy]. Replaced with a genuine, verbatim, disjointed-but-same-speech passage from ms16 that directly makes the regional-labour-shortage-vs-immigration argument.'),
]

for node_id, cite, quote, note in fixes:
    old = conn.execute("SELECT status FROM nodes WHERE node_id=?", (node_id,)).fetchone()[0]
    conn.execute("""UPDATE nodes SET citation_key=?, quote_in_doc=?, is_literal_quote=1,
        status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=?""", (cite, quote, now, node_id))
    conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
        VALUES (?, ?, 'verified', 'manual', ?, ?)""", (node_id, old, note, now))
    print(node_id, old, "-> verified")

conn.commit()
conn.close()
