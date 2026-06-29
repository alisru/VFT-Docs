import json

compact_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus Kanon\compact JSON\Plane_7_Result_compact.json"
hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(compact_path, "r", encoding="utf-8") as f:
    compact_data = json.load(f)

with open(hanson_path, "r", encoding="utf-8") as f:
    hanson_data = json.load(f)

# Find Plane 7 in Hanson
hanson_plane7 = None
for plane in hanson_data.get("planes", []):
    if plane.get("plane_num") == 7:
        hanson_plane7 = plane
        break

print(f"Compact vectors: {len(compact_data)}")
if hanson_plane7:
    print(f"Hanson plane 7 vectors: {len(hanson_plane7['vectors'])}")
    
    # Let's print the addresses of both to see if they match.
    compact_addresses = [v["address"] for v in compact_data]
    hanson_addresses = [v["address"] for v in hanson_plane7["vectors"]]
    
    print("Compact addresses:")
    print(compact_addresses)
    print("Hanson addresses:")
    print(hanson_addresses)
    
    # Are there any differences?
    diff1 = set(compact_addresses) - set(hanson_addresses)
    diff2 = set(hanson_addresses) - set(compact_addresses)
    print(f"In compact but not Hanson: {diff1}")
    print(f"In Hanson but not compact: {diff2}")
else:
    print("Hanson Plane 7 not found!")
