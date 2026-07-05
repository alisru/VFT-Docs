import json

output_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Hanson_Audit_AI_Logs\remediated_plane_7.json"

with open(output_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total vectors: {len(data)}")
for idx, v in enumerate(data):
    # Check keys
    required_keys = {"address", "name", "coordinates", "verdict", "quote", "description", "justification", "actuality"}
    keys = set(v.keys())
    missing = required_keys - keys
    extra = keys - required_keys
    if missing or extra:
        print(f"Index {idx} ({v.get('address')}): Missing keys {missing}, Extra keys {extra}")
    
    # Check coordinates are floats
    coords = v.get("coordinates")
    if not isinstance(coords, dict) or "v" not in coords or "psi" not in coords:
        print(f"Index {idx} ({v.get('address')}): Invalid coordinates structure {coords}")
    else:
        if not isinstance(coords["v"], (float, int)) or not isinstance(coords["psi"], (float, int)):
            print(f"Index {idx} ({v.get('address')}): Coordinates are not numbers {coords}")
            
    # Check actuality length and presence of placeholders
    act = v.get("actuality", "")
    if "placeholder" in act.lower() or "stubs" in act.lower() or "the subject's actual output over time" in act.lower():
        print(f"Index {idx} ({v.get('address')}): Contains placeholder text in actuality")
    if len(act.split()) < 20:
        print(f"Index {idx} ({v.get('address')}): Actuality is too short ({len(act.split())} words)")

print("Validation complete.")
