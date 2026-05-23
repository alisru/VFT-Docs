import json

path = r"E:\Vector Field Theory\VFT Docs\_VFT MD\index_data.json"
try:
    with open(path, 'r', encoding='utf-8') as f:
        # Since it's large, let's read keys first or a snippet
        # Wait, if it is a JSON object, let's load it
        data = json.load(f)
        print("Keys in index_data.json:", list(data.keys()))
        if "files" in data:
            print("Number of files:", len(data["files"]))
            # Print a few file keys
            print("First 10 files:", list(data["files"].keys())[:10])
except Exception as e:
    print(f"Error: {e}")
