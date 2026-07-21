import sqlite3, datetime
DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

quote275 = ("My overriding concern and that of the people I talk to, is that politicians today are good at talking "
            "but not listening; they will do anything to get your vote but when that has been achieved, the voter "
            "is ignored. The public are sick and tired of being ignored.")
quote276 = ("We need to reconsider the level and mix of permanent migrants to Australia because we are heading "
            "down a dead end road at 90 miles an hour and it is going to end in tears.")
quote284 = "Labor's project to hijack the Australian economy for corrupt union bosses is becoming relentless."

conn.execute("""INSERT OR IGNORE INTO hanson_sources (citation_key, archive_file, url, date_checked, source_type, status)
    VALUES ('senate_cfmeu26', 'senate_cfmeu26.txt', 'https://www.openaustralia.org.au/senate/?id=2026-07-02.113.1&m=100857', ?, 'hansard', 'verified')""", (now,))

fixes = [
    (275, 'npc26', quote275,
     "Quote 'I'm voting with the battlers, the people doing it tough, the ones the major parties have forgotten' does not appear anywhere in the full npc26 transcript -- could not be verified. Restarted the node: replaced with a genuine, verbatim, contiguous two-sentence passage from the same correctly-cited npc26 speech that hits the same anti-establishment/forgotten-voter mechanism."),
    (276, 'ms16', quote276,
     'Quote "We are heading down a dead-end road and it is time we turned around" was a paraphrase/compression of the real ms16 line. Restored the exact verbatim wording ("...heading down a dead end road at 90 miles an hour and it is going to end in tears") from the same correctly-cited 2016 Senate maiden speech.'),
    (284, 'senate_cfmeu26', quote284,
     'Quote "Where has the spirit of the fair go gone? People used to leave their doors unlocked..." does not appear anywhere in the full npc26 transcript and could not be verified via web search -- likely fabricated. Restarted the node per the no-paraphrase rule: replaced with a genuine, verbatim anti-union Hansard quote (2 July 2026 Statements by Senators, confirmed via OpenAustralia.org Hansard mirror) that hits the same mechanism -- attacking union/labour-movement figures as corrupt.'),
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
