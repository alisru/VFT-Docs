import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote317 = ("In my first speech in 1996 I said we were in danger of being swamped by Asians. This was not said out "
            "of disrespect for Asians but was meant as a slap in the face to both the Liberal and Labor governments "
            "who opened the floodgates to immigration... Now we are in danger of being swamped by Muslims, who bear "
            "a culture and ideology that is incompatible with our own.")

old = conn.execute("SELECT status FROM nodes WHERE node_id=317").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='ms16', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=317""", (quote317, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (317, ?, 'verified', 'manual',
    'Quote was a third-person paraphrase generically cited to [^wiki]. Located her actual first-person explanation, verbatim, in the already-archived 2016 Senate maiden speech (ms16), where she directly makes this exact argument about the 1996 line and extends the same logic to Muslim immigration. Replaced the paraphrase with the genuine quote (disjointed within the same speech via ellipsis, per the no-paraphrase rule) and re-cited to ms16.', ?)""",
    (old, now))
conn.commit()
print("node 317:", old, "-> verified")
conn.close()
