import json

hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(hanson_path, "r", encoding="utf-8") as f:
    h_data = json.load(f)

h_plane7 = next(p for p in h_data["planes"] if p["plane_num"] == 7)

for idx, hv in enumerate(h_plane7['vectors']):
    if "Transition" in hv['name'] or "Transition" in hv.get("description", "") or "Transition" in hv.get("justification", "") or "Transition" in hv.get("meta", {}).get("stated_name", ""):
        print(f"{idx:02d}: Address: {hv['address']} | Name: {hv['name']} | Stated Name: {hv.get('meta', {}).get('stated_name')}")
