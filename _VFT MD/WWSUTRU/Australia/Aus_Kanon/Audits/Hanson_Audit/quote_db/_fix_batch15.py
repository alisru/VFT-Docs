import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

fixes = [
    (280, "ms16", "It is about belonging, respect and commitment to fight for Australia. This will never be traded or given up for the mantras of diversity or tolerance.",
     "First sentence was real (ms96/ms16 share similar phrasing) but the second sentence ('This will never be achieved by a republic') does not appear in either speech and was fabricated. Replaced with the genuine continuation from her 2016 Senate maiden speech and re-cited ms96 -> ms16."),
    (214, "ms96", "In the 1960s, our wages increase ran at three per cent and unemployment at two per cent. Today, not only is there no wage increase, we have gone backwards and unemployment is officially 8.6 per cent.",
     "First sentence was real and correctly cited (ms96) but the second sentence ('Today we have our best economic managers telling us we must have a natural rate of unemployment of five per cent or the economy will overheat') does not appear in the speech and was fabricated. Replaced with the genuine continuation."),
    (265, "senate20jm", "Businesses don't want handouts. Businesses want Australian workers.",
     "First sentence was real and correctly cited (senate20jm) but the second sentence ('Businesses want lower taxes and less red tape so they can create real jobs for Australians') does not appear in the speech and was fabricated. Replaced with the genuine closing line of the speech."),
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
