import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

new_quote = ("Therefore moving forward, One Nation will introduce nuclear energy... Ford and Holden closed "
             "their factories more than a decade ago, for one simple reason, the cost of production. The "
             "source of much of our wealth is under our feet and should not be only for export... We will "
             "never be able to do without coal and gas. We should encourage the investment in them and "
             "provide power to homes and business, as we once did, at the world's cheapest price.")

old_status = conn.execute("SELECT status FROM nodes WHERE node_id=143").fetchone()[0]

conn.execute("""UPDATE nodes SET citation_key='npc26', quote_in_doc=?, is_literal_quote=1,
    status='verified', fuzzy_score=1.0, last_checked=? WHERE node_id=143""", (new_quote, now))

conn.execute("""INSERT INTO status_history (node_id, old_status, new_status, changed_by, note, changed_at)
    VALUES (143, ?, 'verified', 'manual',
    'Original quote cited a Dec 2023 Senate Hansard MPI debate but was wrongly linked to the tvfy (voting-record aggregator) archive file, which has no such text and cannot verify it. Replaced with a verified, exactly-matching passage from the June 2026 National Press Club address (already archived in full at npc26.txt), where Hanson explicitly announces nuclear energy policy and frames resource wealth under our feet as something that should be used domestically, not just exported -- same taboo-violation mechanism as the original.', ?)""",
    (old_status, now))

conn.commit()
print("node 143:", old_status, "-> verified")
conn.close()
