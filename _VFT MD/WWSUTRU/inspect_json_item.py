
import json
from pathlib import Path

TARGET_JSON = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia_Kanon.json")

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def inspect_item(target_id):
    data = load_json(TARGET_JSON)
    found_count = 0
    print(f"--- Inspecting ID: {target_id} ---")
    for plane in data.get("planes", []):
        for sense in plane.get("senses", []):
            for item in sense.get("items", []):
                if item.get("id") == target_id:
                    print(json.dumps(item, indent=2))
                    found_count += 1
    
    if found_count == 0:
        print(f"Item {target_id} not found.")
    else:
        print(f"Found {found_count} occurrences.")

if __name__ == "__main__":
    inspect_item("(Effect.Why.What)")
    inspect_item("(Effect.Effect.Why)")
