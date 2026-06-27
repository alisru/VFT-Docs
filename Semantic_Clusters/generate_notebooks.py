import os
import sys
import math

def classify_by_topic(rel_path, file_name):
    path_lower = rel_path.lower()
    name_lower = file_name.lower()
    
    # 1. Drafts, Archives, and Duplicates
    if "_archive" in path_lower or "duplicate" in path_lower or "temp" in name_lower or "draft" in path_lower or "backup" in path_lower:
        return "Drafts, Archives & Duplicates"
        
    # 2. Unstructured Notes & Chat Logs
    if "chatlog" in path_lower or "muses" in path_lower or "drawing_board" in path_lower or "notes" in name_lower or "temporary" in name_lower or "chat logs" in path_lower:
        return "Unstructured Notes & Chat Logs"
        
    # 3. Information Physics & Thermodynamics
    phys_keywords = ["physics", "thermodynamic", "entropy", "lattice", "equation", "price", "geometry", "tensor", "amplitude", "gravity", "dimension"]
    if any(k in name_lower or k in path_lower for k in phys_keywords):
        return "Information Physics & Thermodynamics"
        
    # 4. Ontological Auditing & Geopolitics
    geo_keywords = ["audit", "hegemony", "greens", "albanese", "dutton", "epstein", "australia", "influence", "geopolitics", "hanson", "rudd", "minimis", "polic"]
    if any(k in name_lower or k in path_lower for k in geo_keywords):
        return "Ontological Auditing & Geopolitics"
        
    # 5. Metaphysics & Actualism
    meta_keywords = ["soul", "theology", "metaphysics", "planes", "jesus", "christ", "god", "kingdom", "actualism", "spirit", "bible", "aletheia", "apocrypha"]
    if any(k in name_lower or k in path_lower for k in meta_keywords):
        return "Metaphysics & Actualism"
        
    # 6. System Protocols & Operational Guides
    sys_keywords = ["protocol", "directive", "viewer", "run", "instructions", "workflow", "rule", "command", "task", "walkthrough", "plan", "memory"]
    if any(k in name_lower or k in path_lower for k in sys_keywords):
        return "System Protocols & Operational Guides"
        
    # Fallback/Default depending on location
    if "io" in path_lower:
        return "Unstructured Notes & Chat Logs"
    return "Metaphysics & Actualism"

def get_sorting_key(rel_path):
    path_lower = rel_path.lower()
    file_name = os.path.basename(rel_path).lower()
    parts = rel_path.split(os.sep)
    
    # Extract sub-folder name (e.g. actualism/philosophy -> philosophy)
    subfolder = "general"
    if len(parts) > 1:
        # If the file is inside _VFT MD, look at the third part
        if parts[0].lower() == "_vft md" and len(parts) > 2:
            subfolder = parts[2]
        elif parts[0].lower() != "_vft md":
            subfolder = parts[1]
            
    # For temporary io files, route their subfolders semantically by filename keywords
    if "io" in path_lower:
        phys_keywords = ["physics", "thermodynamic", "entropy", "lattice", "price", "geometry", "tensor", "amplitude", "gravity"]
        geo_keywords = ["audit", "hegemony", "greens", "albanese", "dutton", "epstein", "australia", "hanson", "rudd", "minimis"]
        meta_keywords = ["soul", "theology", "metaphysics", "planes", "jesus", "christ", "god", "kingdom", "actualism"]
        
        if any(k in file_name for k in phys_keywords):
            subfolder = "io-physics"
        elif any(k in file_name for k in geo_keywords):
            subfolder = "io-geopolitics"
        elif any(k in file_name for k in meta_keywords):
            subfolder = "io-metaphysics"
        else:
            subfolder = "io-unstaged"
            
    # Return (subfolder, filename) tuple to sort by subfolder first, then file name
    return (subfolder.lower(), file_name)

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
    
    # Categorize files
    notebooks = {
        "Metaphysics & Actualism": [],
        "Information Physics & Thermodynamics": [],
        "Ontological Auditing & Geopolitics": [],
        "System Protocols & Operational Guides": [],
        "Drafts, Archives & Duplicates": [],
        "Unstructured Notes & Chat Logs": []
    }
    
    for file_path in all_md_files:
        rel_path = os.path.relpath(file_path, workspace_root)
        file_name = os.path.basename(file_path)
        
        category = classify_by_topic(rel_path, file_name)
        notebooks[category].append(rel_path)
        
    # Calibrate chunks sorted by sub-categorization
    final_notebooks = {}
    for name, file_list in notebooks.items():
        count = len(file_list)
        if count == 0:
            continue
        if count <= 300:
            final_notebooks[name] = file_list
        else:
            num_parts = math.ceil(count / 300)
            print(f"Notebook '{name}' has {count} files. Splitting into {num_parts} sub-notebooks sorted by sub-categories...", flush=True)
            
            # Sort file list by sub-categorization key
            sorted_list = sorted(file_list, key=get_sorting_key)
            part_size = math.ceil(count / num_parts)
            for i in range(num_parts):
                part_files = sorted_list[i*part_size : (i+1)*part_size]
                final_notebooks[f"{name} (Part {i+1} of {num_parts})"] = part_files
                
    # Write to hypothetical_notebooks.md
    out_file = os.path.join(script_dir, "hypothetical_notebooks.md")
    print(f"Writing registry to {out_file}...", flush=True)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# The Hypothetical Notebooks Index\n\n")
        f.write("This index compiles all workspace markdown files (excluding the Bible) grouped into 6 logical semantic topics. Large books are split into parts grouped by their physical sub-folders and semantic categories.\n\n")
        
        f.write("## Notebook Breakdown Table\n\n")
        f.write("| Notebook Name | Document Count |\n|:---|:---|\n")
        for name, files in final_notebooks.items():
            f.write(f"| {name} | {len(files)} |\n")
        f.write("\n---\n\n")
        
        for name, files in final_notebooks.items():
            f.write(f"## {name} (Count: {len(files)})\n\n")
            for rel_path in sorted(files, key=get_sorting_key):
                full_path = os.path.join(workspace_root, rel_path).replace(os.sep, '/')
                f.write(f"* [{os.path.basename(rel_path)}](file:///{full_path})\n")
            f.write("\n")
            
    print("Registry generation complete!", flush=True)

if __name__ == "__main__":
    main()
