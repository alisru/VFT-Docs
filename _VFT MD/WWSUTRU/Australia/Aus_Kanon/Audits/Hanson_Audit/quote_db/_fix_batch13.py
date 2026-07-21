import sqlite3, datetime

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
now = datetime.datetime.now().isoformat(timespec="seconds")
conn = sqlite3.connect(DB)

fixes = [
    (212, "npc26", "Put bluntly, these figures derive because of one policy, above all others, the hoax of global warming which is now climate change.",
     "Quote was real but cited to senate18prot (a 2018 immigration speech that never mentions climate) instead of the actual source, her 17 June 2026 National Press Club address. Re-cited to npc26 and expanded to the full real sentence."),
    (207, "ms16", "Australia needs a national government, not a corporate one, not a union one, and not an alternative lifestyle one.",
     "Quote was real but cited to ms96 (1996 House maiden speech); it actually appears in her 2016 Senate maiden speech (foreign-ownership passage). Re-cited to ms16."),
    (289, "ms96", "A truly multicultural country can never be strong or united.",
     "Quote was real but cited to ms16 (2016 Senate maiden speech); it actually appears in her 1996 House maiden speech. Re-cited to ms96."),
    (248, "npc26", "My overriding concern and that of the people I talk to, is that politicians today are good at talking but not listening; they will do anything to get your vote but when that has been achieved, the voter is ignored.",
     "Quote was cited to ms96 but does not appear in the 1996 speech; it is from her 17 June 2026 National Press Club address. Re-cited to npc26 and expanded to the full real sentence."),
    (294, "ms96", "Reduced tariffs on foreign goods that compete with local products seem only to cost Australians their jobs. We must look after our own before lining the pockets of overseas countries and investors at the expense of our living standards and future.",
     "Quote was real but cited to senate18tax (which does not contain this line); it actually appears in her 1996 House maiden speech. Re-cited to ms96."),
    (300, "senate20jm", "There is a handout mentality in the third and fourth generations of this nation—a handout mentality of people not working.",
     "Quote was real but cited to ms96 (not found there); it actually appears in her 10 Nov 2020 'Flawed Jobmaker Falls Short' speech. Re-cited to senate20jm and expanded to the full real sentence."),
    (312, "onenation_gas26", "We want more gas, more oil, and more energy to drive our economy forward, pay down our debts, and secure our energy future... This will be the first time that Australians have a genuine ownership stake in the nation's natural resources.",
     "Both segments are real and verbatim, but from the 9 June 2026 gas policy launch page (onenation_gas26), not the 21 May 2026 Adelaide pre-announcement (energy26) it was cited to. This is a disjointed-but-genuine quote (two real excerpts from the same speech/document, ellipsis-bridged), which is acceptable per standing instruction. Re-cited to onenation_gas26."),
    (272, "ms16", "My pride and patriotism were instilled in me from an early age when I watched the Australian flag raised every morning at school and sang the national anthem; watching our athletes compete on the world stage, proud to salute the Australian flag being raised to honour them as they took their place on podiums.",
     "Quote was cited to ms96 (1996) with slightly altered wording; the real, longer verbatim version is in her 2016 Senate maiden speech. Re-cited to ms16 and corrected wording to match exactly."),
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
