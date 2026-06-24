import json
import os

def main():
    mapping_path = "cluster_mapping.json"
    if not os.path.exists(mapping_path):
        print("cluster_mapping.json not found")
        return
        
    with open(mapping_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Total paragraphs: {len(data)}")
    
    unique_files = set()
    for item in data:
        file_path = item.get("file", "")
        if file_path:
            # Get relative path or basename
            unique_files.add(os.path.basename(file_path))
            
    print(f"Total unique files: {len(unique_files)}")
    print("Files list (first 30):")
    for f in sorted(list(unique_files))[:30]:
        print(f" - {f}")

if __name__ == "__main__":
    main()
