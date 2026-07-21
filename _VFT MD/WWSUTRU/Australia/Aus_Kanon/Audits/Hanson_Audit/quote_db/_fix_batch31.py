import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

old = conn.execute("SELECT status FROM nodes WHERE node_id=221").fetchone()[0]
conn.execute("""UPDATE nodes SET is_literal_quote=0,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=221""", (now,))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (221, ?, 'verified', 'manual',
    'This node describes an aggregate voting pattern (37% weighted agreement score, "voted generally against increasing workplace protections"), not a single utterance -- no genuine first-person quote applies. Re-fetched the cited They Vote For You page (policies/251) directly and confirmed the citation, wording, and score are already accurate as a documented-action statement. No text change needed; DB status corrected from paraphrased to verified, is_literal_quote confirmed 0.', ?)""",
    (old, now))
conn.commit()
print("node 221:", old, "-> verified")
conn.close()
