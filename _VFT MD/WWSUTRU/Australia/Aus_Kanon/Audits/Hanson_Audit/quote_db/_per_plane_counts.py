import sqlite3

DB = r"E:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\quote_db\quote_verification.db"
conn = sqlite3.connect(DB)

plane_names = {1: "Identity", 2: "Definition", 3: "Land", 4: "Drive", 5: "Method", 6: "Foundation", 7: "Result"}

total_hit = 0
total_fail = 0
total_n = 0
lines = []
for p in range(1, 8):
    rows = conn.execute("SELECT hit_fail FROM nodes WHERE plane=?", (p,)).fetchall()
    n = len(rows)
    hit = sum(1 for r in rows if r[0] == 'HIT')
    fail = sum(1 for r in rows if r[0] == 'FAIL')
    net = hit - fail
    total_hit += hit
    total_fail += fail
    total_n += n
    lines.append(f"Plane {p} ({plane_names[p]}): {n} vectors, {hit} HIT, {fail} FAIL, Net {'+' if net>=0 else ''}{net}")

for l in lines:
    print(l)

net_total = total_hit - total_fail
score = net_total / total_n * 100
print()
print(f"Summed: {total_n} vectors, {total_hit} HIT, {total_fail} FAIL, Net {'+' if net_total>=0 else ''}{net_total}, alignment {net_total}/{total_n} = {score:.1f}%")
conn.close()
