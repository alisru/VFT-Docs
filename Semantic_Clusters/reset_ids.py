import os
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
categories_slugs = [
    "physics-thermodynamics",
    "metaphysics-actualism",
    "ontological-auditing-geopolitics",
    "system-protocols-operational-guides",
    "unstructured-notes-chat-logs"
]

for slug in categories_slugs:
    path = os.path.join(script_dir, f"notebook-{slug}-filelist.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Reset notebook_id so the script pulls the valid UUID from the online list
        data["notebook_id"] = None
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Reset notebook_id for {slug}")
