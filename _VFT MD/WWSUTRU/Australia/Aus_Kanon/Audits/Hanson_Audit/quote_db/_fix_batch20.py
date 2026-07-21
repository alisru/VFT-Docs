import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote230 = "If we are to maintain social cohesion and economic prosperity we need people to read, write and speak English."

old = conn.execute("SELECT status FROM nodes WHERE node_id=230").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='senate18prot', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=230""", (quote230, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (230, ?, 'verified', 'manual',
    'Fetched the full text of senate18prot.txt directly -- the quote "We are one united nation: one law for all, one language, one flag" does not appear anywhere in that speech. This is the same known-fabricated line already flagged in ms96.txt''s own verification log as a prior confirmed fabrication under a different citation key; this was a second, separate instance. Restarted the node per the no-paraphrase rule: replaced with a genuine verbatim line from the correctly-cited senate18prot speech itself that fits the node''s cultural-homogeneity/assimilation mechanism.', ?)""",
    (old, now))
conn.commit()
print("node 230:", old, "-> verified")
conn.close()
