import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

vdb_dir = r'e:\Vector Field Theory\VFT Docs\_AI files and chat logs'
query = "The disciples are suffering from Scalar Lock"

for filename in os.listdir(vdb_dir):
    if filename.startswith('temp_ingest_') and filename.endswith('.json'):
        filepath = os.path.join(vdb_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    content = item.get('payload', {}).get('full_content', '')
                    if query in content:
                        print(f"--- RECORD FOUND in {filename} ---")
                        print(f"ID: {item.get('id')}")
                        print(f"Source Path: {item.get('payload', {}).get('source_path')}")
                        print("Content Snippet (around image1):")
                        idx = content.find("The Ratio:")
                        print(content[idx:idx+2000] if idx != -1 else content[:2000])
                        # Let's save the whole content to a temp file for inspection
                        with open('vdb_bread_content.md', 'w', encoding='utf-8') as wf:
                            wf.write(content)
                        sys.exit(0)
        except Exception as e:
            continue
print("Not found.")
