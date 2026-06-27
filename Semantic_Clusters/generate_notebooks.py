import os
import sys
import math
import re

def classify_by_topic(rel_path, file_name):
    path_lower = rel_path.lower()
    name_lower = file_name.lower()
    
    # 1. Drafts, Archives, and Duplicates (Skip entirely)
    if "_archive" in path_lower or "duplicate" in path_lower or "temp" in name_lower or "draft" in path_lower or "backup" in path_lower:
        return "SKIP"
        
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
    parts = rel_path.split(os.sep)
    subfolder = "general"
    if len(parts) > 1:
        if parts[0].lower() == "_vft md" and len(parts) > 2:
            subfolder = parts[2]
        elif parts[0].lower() != "_vft md":
            subfolder = parts[1]
    return (subfolder.lower(), os.path.basename(rel_path).lower())

def normalize_filename(name):
    # Strip extension
    name = name.lower().replace(".md", "")
    # Remove common copy suffixes: _1, _2, (1), (2), - Copy, etc.
    name = re.sub(r'[\s_\-\(]+(1|2|3|4|copy)[\)]*$', '', name)
    # Strip non-alphanumeric to resolve slight punctuation differences
    name = "".join(c for c in name if c.isalnum())
    return name

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
    
    # Categorize files, checking for semantic name uniqueness
    notebooks = {
        "Metaphysics & Actualism": [],
        "Information Physics & Thermodynamics": [],
        "Ontological Auditing & Geopolitics": [],
        "System Protocols & Operational Guides": [],
        "Unstructured Notes & Chat Logs": []
    }
    
    seen_normalized_names = set()
    skipped_duplicates_count = 0
    
    # Sort files physically to prioritize main folders (e.g. Physics/, Actualism/) over temp io/ staging folders
    sorted_md_files = sorted(all_md_files, key=lambda x: (
        1 if "io" in x.lower() else 0, # Prioritize structured folders first
        x.lower()
    ))
    
    for file_path in sorted_md_files:
        rel_path = os.path.relpath(file_path, workspace_root)
        file_name = os.path.basename(file_path)
        
        category = classify_by_topic(rel_path, file_name)
        if category == "SKIP":
            continue
            
        norm_name = normalize_filename(file_name)
        if norm_name in seen_normalized_names:
            print(f"  Skipped duplicate document in listing: '{rel_path}' (already indexed under '{norm_name}')", flush=True)
            skipped_duplicates_count += 1
            continue
            
        seen_normalized_names.add(norm_name)
        notebooks[category].append(rel_path)
        
    print(f"Filtered out {skipped_duplicates_count} duplicate files from registry listing.", flush=True)
        
    # Split any category over 300 files and map to formal names
    final_notebooks = {}
    for name, file_list in notebooks.items():
        count = len(file_list)
        if count == 0:
            continue
        if count <= 300:
            final_notebooks[name] = file_list
        else:
            num_parts = math.ceil(count / 300)
            print(f"Notebook '{name}' has {count} files. Splitting into {num_parts} sub-notebooks with formal names...", flush=True)
            sorted_list = sorted(file_list, key=get_sorting_key)
            part_size = math.ceil(count / num_parts)
            for i in range(num_parts):
                part_files = sorted_list[i*part_size : (i+1)*part_size]
                
                # Formally map the split parts to descriptive names
                if name == "Metaphysics & Actualism":
                    formal_name = "Metaphysics: Linguistic Relationalism & Psychology" if i == 0 else "Metaphysics: Ontological Metaphysics & Theology"
                elif name == "Information Physics & Thermodynamics":
                    formal_name = "Information Physics: Mathematical Models & Price Tensors" if i == 0 else "Information Physics: Coordinate Fields & Attractors"
                elif name == "Ontological Auditing & Geopolitics":
                    formal_name = "Geopolitics: Factional Strategy & Geopolitics" if i == 0 else "Ontological Auditing & National Resonance"
                else:
                    formal_name = f"{name} (Part {i+1} of {num_parts})"
                    
                final_notebooks[formal_name] = part_files
                
    # Write to hypothetical_notebooks.md
    out_file = os.path.join(script_dir, "hypothetical_notebooks.md")
    print(f"Writing registry to {out_file}...", flush=True)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# The Hypothetical Notebooks Index\n\n")
        f.write("This index compiles all workspace markdown files (excluding the Bible) grouped into formal, semantic notebooks. Duplicate and archived files are excluded from this registry. Large categories are split logically to keep every list under 300 files.\n\n")
        
        f.write("## Notebook Breakdown Table\n\n")
        f.write("| Notebook Name | Document Count |\n|:---|:---|\n")
        for name in sorted(final_notebooks.keys()):
            f.write(f"| {name} | {len(final_notebooks[name])} |\n")
        f.write("\n---\n\n")
        
        for name in sorted(final_notebooks.keys()):
            files = final_notebooks[name]
            f.write(f"## {name} (Count: {len(files)})\n\n")
            for rel_path in sorted(files, key=get_sorting_key):
                full_path = os.path.join(workspace_root, rel_path).replace(os.sep, '/')
                f.write(f"* [{os.path.basename(rel_path)}](file:///{full_path})\n")
            f.write("\n")
            
    print("Registry generation complete!", flush=True)

if __name__ == "__main__":
    main()
