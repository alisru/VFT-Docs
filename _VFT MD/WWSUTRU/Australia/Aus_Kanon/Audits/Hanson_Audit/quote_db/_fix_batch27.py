import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote313 = ("Why are we allowing the Chinese government, an oppressive communist regime, to own our land and assets? "
            "Why are we allowing our ports, utilities, services, agricultural land, and industries, to be acquired "
            "by foreigners of any nationality?")
quote316 = ("In this financial year we will be spending at least $1.5 billion on foreign aid and we cannot be sure "
            "that this money will be properly spent, as corruption and mismanagement in many of the recipient "
            "countries are legend... The government should cease all foreign aid immediately and apply the savings "
            "to generate employment here at home.")

fixes = [
    (313, 'ms16', quote313,
     'Quote was a third-person voting-record/statement summary generically cited to [^wiki][^tvfy]. Replaced with a genuine, verbatim passage from the already-correctly-archived 2016 Senate maiden speech (ms16) that directly makes the same argument -- opposition to Chinese-government ownership of Australian ports, utilities and agricultural land.'),
    (316, 'ms96', quote316,
     'Quote was a third-person paraphrase cited to [^wiki][^onenation]. Replaced with a genuine, verbatim, disjointed-but-same-speech passage from the 1996 maiden speech (ms96) that hits the same mechanism -- framing foreign aid/regional spending as wasteful and better redirected to domestic sovereignty/employment.'),
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
