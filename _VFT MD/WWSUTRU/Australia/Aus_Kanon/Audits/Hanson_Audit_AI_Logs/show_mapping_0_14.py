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

# Print slots 0 to 14
for idx in range(15):
    hv = h_plane7['vectors'][idx]
    matching_cvs = [cv for cv in c_data if cv['address'] == hv['address']]
    print(f"Slot {idx:02d}: Address: {hv['address']}")
    print(f"  Hanson Name: {hv['name']}")
    print(f"  Hanson Meta Stated Name: {hv.get('meta', {}).get('stated_name')}")
    print(f"  Hanson Meta Stated Coords: {hv.get('meta', {}).get('stated_coordinates')}")
    for cv in matching_cvs:
        print(f"  Canonical Name: {cv['name']} | Canonical Coords: {cv['coordinates']}")
    print()
