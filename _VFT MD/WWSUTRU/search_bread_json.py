import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'e:\Vector Field Theory\VFT Docs\_AI files and chat logs\temp_ingest_69ebc04a.json'
keywords = ["5,000", "leaven", "disciples", "saturation", "Mark 8:14"]

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    content = item.get('payload', {}).get('full_content', '')
    count = sum(1 for kw in keywords if kw.lower() in content.lower())
    if count >= 1:
        print(f"--- MATCH IN {filepath} (Hits: {count}) ---")
        print(f"ID: {item.get('id')}")
        print(content)
        # sys.exit(0) # Keep searching to find the best match
