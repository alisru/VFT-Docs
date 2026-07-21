import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)
quote108 = ("If you're gonna have a royal commission into it, throw bloody climate change out the window and let's "
            "look at the pure facts of why we have had the bushfires, how they were handled, what we can do better, "
            "to stop it happening again.")
old = conn.execute("SELECT status FROM nodes WHERE node_id=108").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='sbs_bushfire20', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=108""", (quote108, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (108, ?, 'verified', 'manual',
    'Quote was cited generically to [^wiki] and slightly paraphrased. Re-verified verbatim against the same 13 Jan 2020 SBS/Today show source already archived for node 144 (sbs_bushfire20) and corrected wording/citation.', ?)""",
    (old, now))
conn.commit()
print("node 108:", old, "-> verified")
conn.close()
