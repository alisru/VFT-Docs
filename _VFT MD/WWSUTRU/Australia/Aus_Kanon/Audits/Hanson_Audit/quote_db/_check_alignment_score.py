import sqlite3

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
conn = sqlite3.connect(DB)

rows = conn.execute("SELECT hit_fail FROM nodes").fetchall()
total = len(rows)
hits = sum(1 for r in rows if r[0] == 'HIT')
fails = sum(1 for r in rows if r[0] == 'FAIL')
other = total - hits - fails

print("total nodes:", total)
print("HIT:", hits)
print("FAIL:", fails)
print("other/blank:", other)
scored = hits + fails
if scored:
    score = (hits - fails) / scored * 100
    print(f"Alignment score (HIT-FAIL)/scored: {score:.1f}%")
    print(f"Raw HIT rate (HIT/scored): {hits/scored*100:.1f}%")
conn.close()
