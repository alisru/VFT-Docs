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

print(f"Compact vectors: {len(compact_data)}")
print(f"Hanson Plane 7 vectors: {len(hanson_plane7['vectors'])}")

print("\nDetail of Mismatches/Alignments:")
for idx, hv in enumerate(hanson_plane7['vectors']):
    # Find matching address in compact
    matching_cvs = [cv for cv in compact_data if cv['address'] == hv['address']]
    print(f"Hanson Slot {idx:02d}: Address: {hv['address']}")
    print(f"  Hanson Name: {hv['name']}")
    print(f"  Hanson Meta Stated Name: {hv.get('meta', {}).get('stated_name')}")
    print(f"  Hanson Coords: {hv.get('coordinates')}")
    print(f"  Hanson Quote: {hv.get('quote')}")
    if len(matching_cvs) == 1:
        cv = matching_cvs[0]
        print(f"  Compact Name: {cv['name']}")
        print(f"  Compact Coords: {cv['coordinates']}")
    else:
        print(f"  Multiple Compact Matches ({len(matching_cvs)}):")
        for cv in matching_cvs:
            print(f"    - Name: {cv['name']} | Coords: {cv['coordinates']}")
    print("-" * 60)
