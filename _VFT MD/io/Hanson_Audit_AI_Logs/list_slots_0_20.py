import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"
hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(compact_path, "r", encoding="utf-8") as f:
    compact_data = json.load(f)

with open(hanson_path, "r", encoding="utf-8") as f:
    hanson_data = json.load(f)

hanson_plane7 = next(p for p in hanson_data["planes"] if p["plane_num"] == 7)

print("--- Slots 00 to 20 ---")
for idx in range(0, 21):
    hv = hanson_plane7['vectors'][idx]
    print(f"Hanson Slot {idx:02d}: Address: {hv['address']}")
    print(f"  Hanson Name: {hv['name']}")
    print(f"  Hanson Meta Stated Name: {hv.get('meta', {}).get('stated_name')}")
    print(f"  Hanson Coords: {hv.get('coordinates')}")
    print(f"  Hanson Quote: {hv.get('quote')}")
    print("-" * 60)
