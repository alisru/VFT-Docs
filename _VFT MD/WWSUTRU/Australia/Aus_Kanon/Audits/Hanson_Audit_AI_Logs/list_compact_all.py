import json

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"

with open(compact_path, "r", encoding="utf-8") as f:
    compact_data = json.load(f)

for idx, v in enumerate(compact_data):
    print(f"{idx:02d}: Address: {v['address']} | Name: {v['name']} | Coords: {v['coordinates']}")
