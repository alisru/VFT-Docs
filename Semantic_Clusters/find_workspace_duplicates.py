import os
import hashlib
import json
import sys

# Force output stream to UTF-8 encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def get_file_hash(filepath):
    """Calculate MD5 hash of file content."""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        return None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", "_VFT MD"))
    
    print(f"Scanning workspace for duplicates under: {workspace_root}\n")
    
    hash_map = {}  # MD5 -> list of filepaths
    name_map = {}  # Normalized Name -> list of filepaths
    
    # Folders to ignore
    ignore_dirs = {'.git', '.gemini', 'node_modules', 'Semantic_Clusters', 'drawing_board', 'scratch'}
    
    for root, dirs, files in os.walk(workspace_root):
        # Prune ignored directories in-place
        dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
        
        for file in files:
            if not file.endswith('.md'):
                continue
                
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, workspace_root)
            
            # 1. Content Hash mapping
            file_hash = get_file_hash(filepath)
            if file_hash:
                if file_hash not in hash_map:
                    hash_map[file_hash] = []
                hash_map[file_hash].append(rel_path)
                
            # 2. Normalized Name mapping (strip extensions and lower case)
            stem = os.path.splitext(file)[0].strip().lower()
            if stem not in name_map:
                name_map[stem] = []
            name_map[stem].append(rel_path)

    # Filter out duplicates
    content_duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}
    name_duplicates = {name: paths for name, paths in name_map.items() if len(paths) > 1}
    
    # Deduplicate name matches that are already content duplicates to avoid redundancy
    unique_name_duplicates = {}
    for name, paths in name_duplicates.items():
        is_already_covered = False
        for h, c_paths in content_duplicates.items():
            if set(paths).issubset(set(c_paths)):
                is_already_covered = True
                break
        if not is_already_covered:
            unique_name_duplicates[name] = paths

    # Prepare report data
    report_data = {
        "content_hash_duplicates": [
            {"hash": h, "paths": sorted(paths)} for h, paths in content_duplicates.items()
        ],
        "filename_duplicates": [
            {"filename_stem": name, "paths": sorted(paths)} for name, paths in unique_name_duplicates.items()
        ]
    }

    report_path = os.path.join(script_dir, "workspace_duplicates.json")
    with open(report_path, 'w', encoding='utf-8') as rf:
        json.dump(report_data, rf, indent=2, ensure_ascii=False)

    print(f"Duplicate scan completed successfully.")
    print(f"Found {len(content_duplicates)} exact content duplicate groups.")
    print(f"Found {len(unique_name_duplicates)} filename duplicate groups.")
    print(f"Full untruncated report written to: {report_path}")

if __name__ == "__main__":
    main()
