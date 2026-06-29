import json

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"
hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(compact_path, "r", encoding="utf-8") as f:
    c_data = json.load(f)

with open(hanson_path, "r", encoding="utf-8") as f:
    h_data = json.load(f)

h_plane7 = next(p for p in h_data["planes"] if p["plane_num"] == 7)
h_vectors = h_plane7["vectors"]

# Let's see if we can find for each compact vector cv a matching hv in h_vectors
matched_h_idx = set()
mapping = {}

for cv in c_data:
    # Try matching by address first
    # But wait, the address in hv is sometimes the same but the content is shifted.
    # Let's see if we can match by comparing cv['name'] to hv['meta']['stated_name']
    found = False
    for idx, hv in enumerate(h_vectors):
        meta_name = hv.get("meta", {}).get("stated_name")
        if meta_name == cv["name"] or hv["name"] == cv["name"]:
            mapping[cv["address"]] = (cv["name"], idx, hv.get("meta", {}).get("stated_name"))
            matched_h_idx.add(idx)
            found = True
            break
    if not found:
        print(f"No match for canonical vector: {cv['address']} | {cv['name']}")

print(f"\nMatched {len(mapping)} out of {len(c_data)} canonical vectors.")
print(f"Unmatched Hanson vectors indices: {set(range(len(h_vectors))) - matched_h_idx}")
for idx in (set(range(len(h_vectors))) - matched_h_idx):
    hv = h_vectors[idx]
    print(f"  Hanson Index {idx}: Address {hv['address']} | Name {hv['name']} | Meta Name {hv.get('meta', {}).get('stated_name')}")
