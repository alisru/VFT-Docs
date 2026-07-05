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

print("--- Retiree in Compact ---")
for v in c_data:
    if "Retiree" in v["name"] or "Grey Nomad" in v["name"]:
        print(json.dumps(v, indent=2))

print("--- Retiree in Hanson ---")
for v in h_plane7["vectors"]:
    if "Retiree" in v["name"] or ("meta" in v and "Retiree" in v["meta"].get("stated_name", "")):
        print(json.dumps(v, indent=2))
