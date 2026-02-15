import os
import re
import collections

# Common filenames that might appear multiple times and shouldn't be deduped solely by name
GENERIC_FILENAMES = {
    'readme.md', 'index.md', 'master_index.md', 'introduction.md', 'start.md',
    'todo.md', 'notes.md', 'template.md'
}

def normalize_path(path):
    path = path.replace('/', '\\').strip()
    if path.startswith('\\'):
        path = path[1:]
    return path.lower()

def get_existing_data(summary_file_path):
    with open(summary_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract paths
    paths = re.findall(r'\*\*Path:\*\*\s*(.*)', content)
    
    existing_paths = set()
    existing_filenames = set()
    
    for p in paths:
        norm_p = normalize_path(p)
        existing_paths.add(norm_p)
        existing_filenames.add(os.path.basename(norm_p))
        
    return existing_paths, existing_filenames

def get_all_md_files(root_dir):
    files_map = {} # path -> filename
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_dir)
                norm_path = normalize_path(rel_path)
                files_map[norm_path] = file.lower()
    return files_map

def main():
    summary_file = r"E:\Vector Field Theory\VFT Docs\file_summaries_comprehensive.md"
    root_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD"
    output_file = r"E:\Vector Field Theory\VFT Docs\.agent\tools\missing_files_smart_report.txt"
    
    try:
        existing_paths, existing_filenames = get_existing_data(summary_file)
        disk_files = get_all_md_files(root_dir)
        
        truly_missing = []
        moved_candidates = []
        
        for path, filename in disk_files.items():
            # 1. Exact path match?
            if path in existing_paths:
                continue # Covered
            
            # 2. Filename match (if not generic)?
            if filename in existing_filenames and filename not in GENERIC_FILENAMES:
                moved_candidates.append(path)
                continue # Likely moved, handled elsewhere or ignored primarily
            
            # 3. Truly missing
            truly_missing.append(path)
            
        # Categorize Missing
        categories = collections.defaultdict(list)
        for f in truly_missing:
            parts = f.split('\\')
            category = parts[0] if len(parts) > 1 else "Root"
            categories[category].append(f)
            
        # Write Report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"ANALYSIS REPORT\n")
            f.write(f"===============\n")
            f.write(f"Total Files on Disk: {len(disk_files)}\n")
            f.write(f"Existing Summaries: {len(existing_paths)}\n")
            f.write(f"Potentially Moved (Skipping): {len(moved_candidates)}\n")
            f.write(f"Truly Missing (To Process): {len(truly_missing)}\n\n")
            
            f.write("-" * 30 + "\n")
            f.write("MOVED CANDIDATES (Examples)\n")
            for m in moved_candidates[:10]:
                 f.write(f"  - {m}\n")
            f.write("-" * 30 + "\n\n")

            f.write("TRULY MISSING FILES\n")
            for cat, files in sorted(categories.items()):
                f.write(f"\n[{cat.upper()}] - {len(files)} files\n")
                for file in sorted(files):
                    f.write(f"  - {file}\n")
                    
        print(f"Analysis complete.")
        print(f"Truly Missing: {len(truly_missing)}")
        print(f"Moved/Renamed candidates skipped: {len(moved_candidates)}")
        print(f"Report saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
