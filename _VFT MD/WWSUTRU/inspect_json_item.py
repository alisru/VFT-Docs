import json
import os

def inspect_json(file_path):
    print(f"Inspecting {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not isinstance(data, list):
        print("Not a list")
        return
    
    for item in data:
        source_path = item.get('source_path', 'N/A')
        id_val = item.get('id', 'N/A')
        print(f"ID: {id_val}")
        print(f"Source Path: {source_path}")
        if 'payload' in item:
            headers = [k for k in item['payload'].keys() if k != 'full_content']
            print(f"Payload keys (excl full_content): {headers}")
        print("-" * 20)

directory = r'e:\Vector Field Theory\VFT Docs\_AI files and chat logs'
for filename in os.listdir(directory):
    if filename.startswith('temp_ingest_') and filename.endswith('.json'):
        inspect_json(os.path.join(directory, filename))
