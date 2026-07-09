import json
import os

resolved_path = "../../Plane_2_Definition.json"
print(f"Reading definitions from {resolved_path}...")

with open(resolved_path, "r", encoding="utf-8") as f:
    data = json.load(f)

target_keys = [
    "What.Cause.Cause",
    "What.Cause.Effect",
    "What.Effect.Who",
    "What.Effect.What",
    "What.Effect.Where",
    "What.Effect.Why",
    "What.Effect.How",
    "What.Effect.Cause",
    "What.Effect.Effect"
]

found_nodes = []
for item in data:
    if isinstance(item, dict) and item.get("address") in target_keys:
        found_nodes.append(item)

for fn in found_nodes:
    print(f"\n==================== Node: {fn.get('address')} ====================")
    print(f"Name: {fn.get('name')}")
    print(f"Coordinate: {fn.get('coordinates')}")
    print(f"Canonical Quote: {fn.get('canonical_quote')}")
    print(f"Attribution: {fn.get('attribution')} ({fn.get('source')})")
    print(f"Description: {fn.get('description')}")
    print(f"Establishes: {fn.get('establishes')}")
    shadow = fn.get("shadow", None)
    if shadow:
        print(f"Shadow: {json.dumps(shadow, indent=2)}")
