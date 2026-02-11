import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'e:\Vector Field Theory\VFT Docs\_AI files and chat logs\temp_ingest_69ebc04a.json'
query = "leaven"

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    content = item.get('payload', {}).get('full_content', '')
    if query.lower() in content.lower():
        if "The Divine Coefficient" in content:
            print(f"--- MATCH IN {filepath} ---")
            print(content)
            sys.exit(0)
print("Not found.")
