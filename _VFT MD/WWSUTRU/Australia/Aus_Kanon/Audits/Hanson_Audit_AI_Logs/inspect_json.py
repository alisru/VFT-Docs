import json
from pathlib import Path

json_path = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json")
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data['planes']:
    p_num = p['plane_num']
    p_name = p['plane_name']
    vectors = p['vectors']
    print(f"Plane {p_num}: {p_name}")
    if vectors:
        print(f"  Keys: {list(vectors[0].keys())}")
        print(f"  Sample vector (first 3 keys/values):")
        for k, v in list(vectors[0].items())[:5]:
            print(f"    {k}: {repr(v)}")
    print()
