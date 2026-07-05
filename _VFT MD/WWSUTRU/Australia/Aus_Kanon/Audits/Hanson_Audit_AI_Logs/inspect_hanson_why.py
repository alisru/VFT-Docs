import json

hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(hanson_path, "r", encoding="utf-8") as f:
    hanson_data = json.load(f)

hanson_plane7 = next(p for p in hanson_data["planes"] if p["plane_num"] == 7)

why_vectors = [v for v in hanson_plane7["vectors"] if v["address"] == "Effect.Effect.Why"]
for idx, v in enumerate(why_vectors):
    print(f"--- Vector {idx} ---")
    print(json.dumps(v, indent=2))
