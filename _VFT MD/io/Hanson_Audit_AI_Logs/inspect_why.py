import json

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"

with open(compact_path, "r", encoding="utf-8") as f:
    compact_data = json.load(f)

why_vectors = [v for v in compact_data if v["address"] == "Effect.Effect.Why"]
for idx, v in enumerate(why_vectors):
    print(f"--- Vector {idx} ---")
    print(json.dumps(v, indent=2))
