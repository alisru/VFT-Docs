import os
import sys
import math

def get_root_category(rel_path):
    parts = rel_path.split(os.sep)
    if not parts:
        return "Unclassified"
        
    first_part = parts[0]
    # If the file is inside _VFT MD, look at the second part for classification
    if first_part == "_VFT MD" and len(parts) > 1:
        first_part = parts[1]
        
    # Map to primary folders
    normalized = first_part.lower()
    if normalized == "wwsutru":
        return "Geopolitics (WWSUTRU)"
    elif normalized == "actualism":
        return "Actualism & Theology"
    elif normalized == "physics":
        return "Physics & Ethical Geometry"
    elif normalized == "muses":
        return "Muses & Creative"
    elif normalized == "protocols":
        return "Protocols & Systems"
    elif normalized == "io":
        return "Inbox & Raw Inputs (io)"
    elif normalized in ["_archive", "_archive/drafts", "duplicates"]:
        return "Archive & Backups"
    elif normalized in ["_ai files and chat logs", "semantic_clusters", "bluesky_bot", "drawing_board"]:
        return "System Logs & Workspace Scripts"
        
    return "Other / Miscellaneous"

def get_sub_category(rel_path, parent_cat):
    parts = rel_path.split(os.sep)
    # Check if the path begins with _VFT MD
    start_idx = 1 if parts[0] == "_VFT MD" else 0
    
    # If we have subdirectories, return the next level folder
    if len(parts) > start_idx + 1:
        return parts[start_idx + 1]
    return "General"

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    
    print("Scanning workspace for markdown files...", flush=True)
    all_md_files = []
    
    for root, dirs, files in os.walk(workspace_root):
        dirs[:] = [d for d in dirs if d.lower() not in ['.git', '.agent', 'bible', 'node_modules', 'venv', 'env']]
        for file in files:
            if file.lower().endswith('.md'):
                full_path = os.path.abspath(os.path.join(root, file))
                if "bible" not in full_path.lower():
                    all_md_files.append(full_path)
                    
    print(f"Found {len(all_md_files)} markdown documents.", flush=True)
    
    # Group by physical root folder
    raw_notebooks = {}
    for file_path in all_md_files:
        rel_path = os.path.relpath(file_path, workspace_root)
        cat = get_root_category(rel_path)
        if cat not in raw_notebooks:
            raw_notebooks[cat] = []
        raw_notebooks[cat].append(rel_path)
        
    # Process notebooks to ensure each is under 300 files
    final_notebooks = {}
    
    for cat_name, file_list in raw_notebooks.items():
        count = len(file_list)
        if count <= 300:
            final_notebooks[cat_name] = file_list
        else:
            print(f"Root notebook '{cat_name}' has {count} files. Splitting by physical subdirectories...", flush=True)
            # Group by sub-folders
            sub_groups = {}
            for rel_path in file_list:
                sub = get_sub_category(rel_path, cat_name)
                sub_name = f"{cat_name} — {sub}"
                if sub_name not in sub_groups:
                    sub_groups[sub_name] = []
                sub_groups[sub_name].append(rel_path)
                
            # Iterate through sub-folders and verify count
            for sub_name, sub_files in sub_groups.items():
                sub_count = len(sub_files)
                if sub_count <= 300:
                    final_notebooks[sub_name] = sub_files
                else:
                    # If a sub-folder is still >300, chunk it into parts
                    num_parts = math.ceil(sub_count / 300)
                    print(f"  Sub-notebook '{sub_name}' still has {sub_count} files. Splitting into {num_parts} parts...", flush=True)
                    sorted_sub = sorted(sub_files, key=lambda x: x.lower())
                    part_size = math.ceil(sub_count / num_parts)
                    for p in range(num_parts):
                        final_notebooks[f"{sub_name} (Part {p+1} of {num_parts})"] = sorted_sub[p*part_size : (p+1)*part_size]
                        
    # Write to hypothetical_notebooks.md
    out_file = os.path.join(script_dir, "hypothetical_notebooks.md")
    print(f"Writing physical directory index to {out_file}...", flush=True)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# The Hypothetical Notebooks Index (Directory Structure Map)\n\n")
        f.write("This index compiles all workspace markdown files (excluding the Bible) categorized by their **physical folder structure** (the primary divide between Geopolitics/WWSUTRU and the other domains). Subdirectories are used to keep each notebook under 300 files.\n\n")
        
        f.write("## Notebook Breakdown Table\n\n")
        f.write("| Notebook Name | Document Count |\n|:---|:---|\n")
        # Sort keys to present cleanly
        for name in sorted(final_notebooks.keys()):
            f.write(f"| {name} | {len(final_notebooks[name])} |\n")
        f.write("\n---\n\n")
        
        for name in sorted(final_notebooks.keys()):
            files = final_notebooks[name]
            f.write(f"## {name} (Count: {len(files)})\n\n")
            for rel_path in sorted(files):
                full_path = os.path.join(workspace_root, rel_path).replace(os.sep, '/')
                f.write(f"* [{os.path.basename(rel_path)}](file:///{full_path})\n")
            f.write("\n")
            
    print("Notebook generation complete!", flush=True)

if __name__ == "__main__":
    main()
