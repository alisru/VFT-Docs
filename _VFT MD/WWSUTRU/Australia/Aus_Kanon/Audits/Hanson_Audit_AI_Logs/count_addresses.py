import json
from collections import Counter

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"
hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(compact_path, "r", encoding="utf-8") as f:
    compact_data = json.load(f)

with open(hanson_path, "r", encoding="utf-8") as f:
    hanson_data = json.load(f)

hanson_plane7 = next(p for p in hanson_data["planes"] if p["plane_num"] == 7)

compact_addrs = [v["address"] for v in compact_data]
hanson_addrs = [v["address"] for v in hanson_plane7["vectors"]]

print("Compact addresses count:", Counter(compact_addrs))
print("Hanson addresses count:", Counter(hanson_addrs))
