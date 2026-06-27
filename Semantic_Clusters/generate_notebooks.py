import os
import sys
import math

def classify_to_notebook(rel_path, file_name):
    path_lower = rel_path.lower()
    name_lower = file_name.lower()
    parts = rel_path.split(os.sep)
    
    subfolder = "general"
    if len(parts) > 1:
        if parts[0].lower() == "_vft md" and len(parts) > 2:
            subfolder = parts[2].lower()
        elif parts[0].lower() != "_vft md":
            subfolder = parts[1].lower()
            
    # 1. Drafts, Archives, and Duplicates
    if "_archive" in path_lower or "duplicate" in path_lower or "temp" in name_lower or "draft" in path_lower or "backup" in path_lower or "chatlog" in path_lower or "muses" in path_lower or "drawing_board" in path_lower or "notes" in name_lower or "temporary" in name_lower or "chat logs" in path_lower or "io" in path_lower:
        return "Drafts, Archives & Duplicates"
        
    # 2. System Protocols & Operations
    sys_keywords = ["protocol", "directive", "viewer", "run", "instructions", "workflow", "rule", "command", "task", "walkthrough", "plan", "memory"]
    if any(k in name_lower or k in path_lower for k in sys_keywords) or "protocols" in path_lower:
        return "System Protocols & Operations"
        
    # 3. Metaphysics & Actualism Splits
    if "actualism" in path_lower:
        theology_keywords = ["theology", "spirit", "bible", "god", "kingdom", "jesus", "christ", "apocrypha", "truth", "decalogue"]
        if subfolder in ["theology & spirituality", "truth"] or any(k in name_lower for k in theology_keywords):
            return "Metaphysics: Ontological Metaphysics & Theology"
        else:
            return "Metaphysics: Linguistic Relationalism & Psychology"
            
    # 4. Information Physics Splits
    if "physics" in path_lower:
        math_keywords = ["equation", "price", "tensor", "matrix", "matrices", "lattice", "born", "amplitude", "entropy"]
        if any(k in name_lower for k in math_keywords):
            return "Information Physics: Mathematical Models & Price Tensors"
        else:
            return "Information Physics: Coordinate Fields & Attractors"
            
    # 5. Geopolitics & Auditing Splits
    if "wwsutru" in path_lower:
        audit_keywords = ["audit", "hanson", "rudd", "indicator", "helixis", "helxis", "epstein"]
        if any(k in name_lower for k in audit_keywords) or "alethekanonreports" in path_lower:
            return "Ontological Auditing & National Resonance"
        else:
            return "Geopolitics: Factional Strategy & Geopolitics"
            
    # Fallbacks
    phys_keywords = ["physics", "thermodynamic", "entropy", "lattice", "equation", "price", "geometry", "tensor", "amplitude", "gravity"]
    if any(k in name_lower for k in phys_keywords):
        return "Information Physics: Mathematical Models & Price Tensors"
        
    geo_keywords = ["audit", "hegemony", "greens", "albanese", "dutton", "epstein", "australia", "influence", "geopolitics", "hanson", "rudd"]
    if any(k in name_lower for k in geo_keywords):
        return "Geopolitics: Factional Strategy & Geopolitics"
        
    meta_keywords = ["soul", "theology", "metaphysics", "planes", "jesus", "christ", "god", "kingdom", "actualism"]
    if any(k in name_lower for k in meta_keywords):
        return "Metaphysics: Ontological Metaphysics & Theology"
        
    return "Metaphysics: Linguistic Relationalism & Psychology"

def get_sorting_key(rel_path):
    parts = rel_path.split(os.sep)
    subfolder = "general"
    if len(parts) > 1:
        if parts[0].lower() == "_vft md" and len(parts) > 2:
            subfolder = parts[2]
        elif parts[0].lower() != "_vft md":
            subfolder = parts[1]
    return (subfolder.lower(), os.path.basename(rel_path).lower())

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
        "Metaphysics: Linguistic Relationalism & Psychology": [],
        "Metaphysics: Ontological Metaphysics & Theology": [],
        "Information Physics: Mathematical Models & Price Tensors": [],
        "Information Physics: Coordinate Fields & Attractors": [],
        "Geopolitics: Factional Strategy & Geopolitics": [],
        "Ontological Auditing & National Resonance": [],
        "System Protocols & Operations": [],
        "Drafts, Archives & Duplicates": []
    }
    
    for file_path in all_md_files:
        rel_path = os.path.relpath(file_path, workspace_root)
        file_name = os.path.basename(file_path)
        
        category = classify_to_notebook(rel_path, file_name)
        notebooks[category].append(rel_path)
        
    # Split any category over 300 files
    final_notebooks = {}
    for name, file_list in notebooks.items():
        count = len(file_list)
        if count == 0:
            continue
        if count <= 300:
            final_notebooks[name] = file_list
        else:
            num_parts = math.ceil(count / 300)
            print(f"Notebook '{name}' has {count} files. Splitting into {num_parts} sub-notebooks...", flush=True)
            sorted_list = sorted(file_list, key=get_sorting_key)
            part_size = math.ceil(count / num_parts)
            for i in range(num_parts):
                part_files = sorted_list[i*part_size : (i+1)*part_size]
                final_notebooks[f"{name} (Part {i+1} of {num_parts})"] = part_files
                
    # Write to hypothetical_notebooks.md
    out_file = os.path.join(script_dir, "hypothetical_notebooks.md")
    print(f"Writing formal registry to {out_file}...", flush=True)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# The Hypothetical Notebooks Index\n\n")
        f.write("This index compiles all workspace markdown files (excluding the Bible) grouped into formal, semantic notebooks. Large categories are split logically to keep every notebook under 300 files.\n\n")
        
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
