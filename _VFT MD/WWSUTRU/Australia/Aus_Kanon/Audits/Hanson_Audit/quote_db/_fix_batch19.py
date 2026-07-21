import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote216 = ("My view on issues is based on commonsense, and my experience as a mother of four children, "
            "as a sole parent, and as a businesswoman running a fish and chip shop.")

old = conn.execute("SELECT status FROM nodes WHERE node_id=216").fetchone()[0]
conn.execute("""UPDATE nodes SET citation_key='ms96', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=216""", (quote216, now))
conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (216, ?, 'verified', 'manual',
    'The quote (\"I built my own business from nothing. I know what it takes to meet a payroll...\") does not appear in ms16.txt (2016 Senate maiden speech, the cited source) or any other archived speech -- could not be verified and was likely fabricated/composited. Restarted the node per the no-paraphrase rule: replaced with a genuine, verbatim line from her 1996 House maiden speech (already archived as ms96) that hits the same Hard Yakka mechanism -- her small-business background (fish and chip shop) as the qualifying credential for her views.', ?)""",
    (old, now))
conn.commit()
print("node 216:", old, "-> verified")
conn.close()
