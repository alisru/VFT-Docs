import json
from pathlib import Path

json_path = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json")
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

plane_3 = [p for p in data['planes'] if p['plane_num'] == 3][0]
print(f"Plane 3 Name: {plane_3['plane_name']}")
for idx, v in enumerate(plane_3['vectors']):
    print(f"{idx+1}. {v['address']} - {v['name']} ({v['verdict']})")
    print(f"   Quote: {v.get('quote')}")
    print(f"   Actuality: {v.get('actuality')}")
    print("-" * 50)
