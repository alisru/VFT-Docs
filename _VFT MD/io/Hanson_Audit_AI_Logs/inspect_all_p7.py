import json
import sys

# Set standard output encoding to utf-8
sys.stdout.reconfigure(encoding='utf-8')

hanson_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hegemonic Audit_ Pauline Hanson.json"

with open(hanson_path, "r", encoding="utf-8") as f:
    hanson_data = json.load(f)

hanson_plane7 = next(p for p in hanson_data["planes"] if p["plane_num"] == 7)

for idx, v in enumerate(hanson_plane7["vectors"]):
    print(f"Index: {idx:02d}")
    print(f"  Address: {v.get('address')}")
    print(f"  Name in JSON: {v.get('name')}")
    print(f"  Meta Stated Name: {v.get('meta', {}).get('stated_name')}")
    print(f"  Coordinates: {v.get('coordinates')}")
    print(f"  Verdict: {v.get('verdict')}")
    print(f"  Quote: {v.get('quote')}")
    print(f"  Description Snippet: {v.get('description', '').replace('\n', ' ')[:100]}...")
    print(f"  Justification Snippet: {v.get('justification', '').replace('\n', ' ')[:100]}...")
    print("-" * 50)
