import json

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"
hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(compact_path, "r", encoding="utf-8") as f:
    compact_data = json.load(f)

with open(hanson_path, "r", encoding="utf-8") as f:
    hanson_data = json.load(f)

hanson_plane7 = next(p for p in hanson_data["planes"] if p["plane_num"] == 7)

print("--- COMPACT PLANE 7 VECTORS ---")
for idx, v in enumerate(compact_data):
    print(f"{idx:02d}: Address: {v['address']} | Name: {v['name']} | Coords: {v['coordinates']}")

print("\n--- HANSON PLANE 7 VECTORS ---")
for idx, v in enumerate(hanson_plane7["vectors"]):
    # Match by index or address? Let's print the Hanson one
    print(f"{idx:02d}: Address: {v['address']} | Name: {v['name']} | Coords: {v.get('coordinates')} | Meta Name: {v.get('meta', {}).get('stated_name')}")
