import os
import re

def normalize_path(path):
    # Normalize slashes and remove leading/trailing whitespace
    path = path.replace('/', '\\').strip()
    # Remove leading \ if present
    if path.startswith('\\'):
        path = path[1:]
    # Remove leading "_VFT MD\" if present, as the summaries often omit it or use partial paths
    # actually, looking at the file, they use relative paths like "Actualism\..." 
    return path.lower()

def get_existing_summaries(summary_file_path):
    with open(summary_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract paths using regex
    # Pattern looks for "**Path:** <path>"
    paths = re.findall(r'\*\*Path:\*\*\s*(.*)', content)
    return set(normalize_path(p) for p in paths)

def get_all_md_files(root_dir):
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                # Create relative path from the doc root
                rel_path = os.path.relpath(full_path, root_dir)
                md_files.append(normalize_path(rel_path))
    return set(md_files)

def main():
    summary_file = r"E:\Vector Field Theory\VFT Docs\file_summaries_comprehensive.md"
    root_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD"
    
    existing = get_existing_summaries(summary_file)
    all_files = get_all_md_files(root_dir)
    
    missing = all_files - existing
    
    print(f"Found {len(existing)} existing summaries.")
    print(f"Found {len(all_files)} markdown files in directory.")
    print(f"Missing {len(missing)} files.")
    
    print("\n--- MISSING FILES ---")
    for f in sorted(missing):
        print(f)

if __name__ == "__main__":
    main()
