import os
import re
import collections

def normalize_path(path):
    path = path.replace('/', '\\').strip()
    if path.startswith('\\'):
        path = path[1:]
    return path.lower()

def get_existing_summaries(summary_file_path):
    with open(summary_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    paths = re.findall(r'\*\*Path:\*\*\s*(.*)', content)
    return set(normalize_path(p) for p in paths)

def get_all_md_files(root_dir):
    md_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                md_files.append(normalize_path(rel_path))
    return set(md_files)

def main():
    summary_file = r"E:\Vector Field Theory\VFT Docs\file_summaries_comprehensive.md"
    root_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD"
    output_file = r"E:\Vector Field Theory\VFT Docs\.agent\tools\missing_files_categorized.txt"
    
    try:
        existing = get_existing_summaries(summary_file)
        all_files = get_all_md_files(root_dir)
        missing = all_files - existing
        
        categories = collections.defaultdict(list)
        for f in missing:
            parts = f.split('\\')
            if len(parts) > 1:
                category = parts[0]
            else:
                category = "Root"
            categories[category].append(f)
            
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Total Missing: {len(missing)}\n")
            f.write("-" * 30 + "\n")
            
            for cat, files in sorted(categories.items()):
                f.write(f"\n[{cat.upper()}] - {len(files)} files\n")
                for file in sorted(files):
                    f.write(f"  - {file}\n")
                    
        print(f"Successfully analyzed {len(missing)} missing files.")
        print(f"Report saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
