import json
from pathlib import Path

compact_path = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus Kanon/compact JSON/Plane_4_Drive_compact.json")
audit_path = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json")

with open(compact_path, 'r', encoding='utf-8') as f:
    compact_data = json.load(f)

with open(audit_path, 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

plane_4_audit = next(p for p in audit_data['planes'] if p['plane_num'] == 4)

print(f"Compact vectors count: {len(compact_data)}")
print(f"Audit vectors count: {len(plane_4_audit['vectors'])}")

compact_by_addr = {v['address']: v for v in compact_data}
audit_by_addr = {v['address']: v for v in plane_4_audit['vectors']}

mismatches = []
for addr, cv in compact_by_addr.items():
    if addr not in audit_by_addr:
        print(f"Address {addr} ({cv['name']}) missing in Audit!")
        continue
    av = audit_by_addr[addr]
    # check name
    if cv['name'] != av['name']:
        print(f"Name mismatch for {addr}: Compact = {cv['name']}, Audit = {av['name']}")
    # check coords
    cc = cv['coordinates']
    ac = av['coordinates']
    if abs(cc['v'] - ac['v']) > 1e-5 or abs(cc['psi'] - ac['psi']) > 1e-5:
        print(f"Coordinate mismatch for {addr} ({cv['name']}): Compact = {cc}, Audit = {ac}")
