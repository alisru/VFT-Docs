import json
import os
import sys

# Set output encoding to utf-8 to avoid Unicode errors
sys.stdout.reconfigure(encoding='utf-8')

def find_content(target_file_part):
    directory = r'e:\Vector Field Theory\VFT Docs\_AI files and chat logs'
    for filename in os.listdir(directory):
        if filename.startswith('temp_ingest_') and filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if not isinstance(data, list):
                    continue
                
                for item in data:
                    payload = item.get('payload', {})
                    source_path = payload.get('source_path', '')
                    if target_file_part.lower() in source_path.lower():
                        print(f"FOUND in {filename}")
                        print(f"Source Path: {source_path}")
                        print("CONTENT START")
                        print(payload.get('full_content', 'NO CONTENT'))
                        print("CONTENT END")
                        return
            except Exception as e:
                # print(f"Error reading {filename}: {e}")
                pass

find_content("Hegemonic Stress Tensor.md")
