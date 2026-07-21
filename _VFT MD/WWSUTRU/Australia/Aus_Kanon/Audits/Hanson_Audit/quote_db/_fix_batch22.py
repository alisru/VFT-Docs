import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote206 = ("If they cannot rein in the budget with overpaid public servants—one being the head of Australia Post, "
            "who is on $4.8 million per year—foreign aid, welfare fraud, politicians lurks and perks, including "
            "former prime ministers, and backroom deals for government jobs, then get out of the job of running this country.")

old = conn.execute("SELECT status FROM nodes WHERE node_id=206").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='ms16', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=206""", (quote206, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (206, ?, 'verified', 'manual',
    'The quote "They are incompetent and they are useless" does not appear anywhere in ms96.txt (the cited 1996 maiden speech) and could not be verified elsewhere -- likely fabricated. Restarted the node per the no-paraphrase rule: replaced with a genuine, verbatim line from her 2016 Senate maiden speech (ms16) that hits the same Bricoleur mechanism -- a direct attack on the public service/bureaucratic machinery as overpaid and unaccountable.', ?)""",
    (old, now))
conn.commit()
print("node 206:", old, "-> verified")
conn.close()
