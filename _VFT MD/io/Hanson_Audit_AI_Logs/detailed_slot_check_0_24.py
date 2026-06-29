import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"
hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(compact_path, "r", encoding="utf-8") as f:
    c_data = json.load(f)

with open(hanson_path, "r", encoding="utf-8") as f:
    h_data = json.load(f)

h_plane7 = next(p for p in h_data["planes"] if p["plane_num"] == 7)
h_vectors = h_plane7["vectors"]

# Create mapping of address to compact vector
c_by_addr = {}
for cv in c_data:
    if cv["address"] not in c_by_addr:
        c_by_addr[cv["address"]] = []
    c_by_addr[cv["address"]].append(cv)

for idx in range(25):
    hv = h_vectors[idx]
    print(f"Hanson Slot {idx:02d}: Address: {hv['address']} | Name in JSON: {hv['name']}")
    print(f"  Meta Stated Name: {hv.get('meta', {}).get('stated_name')}")
    print(f"  Meta Stated Coords: {hv.get('meta', {}).get('stated_coordinates')}")
    print(f"  Canonical occupants for this address:")
    occupants = c_by_addr.get(hv["address"], [])
    for occ in occupants:
        print(f"    - Name: {occ['name']} | Coords: {occ['coordinates']}")
    print("-" * 60)
