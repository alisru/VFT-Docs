import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote88 = ("My vision for Australia is that we're all Australians, regardless of race, colour, creed, "
           "where you are, we're all treated as Australians equally on an individual needs basis, not based on race.")

old = conn.execute("SELECT status FROM nodes WHERE node_id=88").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='netimes26', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=88""", (quote88, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (88, ?, 'verified', 'manual',
    'Quote was slightly paraphrased/truncated and mis-cited to [^npc26] (no NPC transcript archived). Located the exact quote, verbatim in quotation marks, in the already-archived netimes26.txt (Hanson Press Club speech crib-notes article, 17 June 2026) -- restored the full wording (including the clause \"where you are,\" that had been dropped) and re-cited to [^netimes26].', ?)""",
    (old, now))
conn.commit()
print("node 88:", old, "-> verified")
conn.close()
