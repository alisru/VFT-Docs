import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(hanson_path, "r", encoding="utf-8") as f:
    h_data = json.load(f)

h_plane7 = next(p for p in h_data["planes"] if p["plane_num"] == 7)
h_vectors = h_plane7["vectors"]

for idx in [10, 22, 36, 47]:
    v = h_vectors[idx]
    print(f"--- Hanson Index {idx} ---")
    print(f"Address: {v['address']} | Name: {v['name']} | Stated Name: {v.get('meta', {}).get('stated_name')}")
    print(f"Quote: {v['quote']}")
    print(f"Description: {v['description']}")
    print(f"Justification: {v['justification']}")
    print()
