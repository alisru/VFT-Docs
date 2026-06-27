import os
import json
import sys
import math

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    
    print("Loading topic mappings...", flush=True)
    cluster_mapping = load_json(os.path.join(script_dir, "cluster_mapping.json"))
    topic_ism = load_json(os.path.join(script_dir, "topic_ism_mapping.json"))
    
    if not cluster_mapping or not topic_ism:
        print("Error: Missing mapping files in Semantic_Clusters.", flush=True)
        return
        
    print("Processing document paragraphs to compute coordinates...", flush=True)
    doc_coords = {}
    for item in cluster_mapping:
        file_path = item.get("file", "")
        if not file_path:
            continue
        norm_path = os.path.abspath(file_path)
        topic_id = str(item.get("topic_id", ""))
        if topic_id in topic_ism:
            coord_data = topic_ism[topic_id]
            u = coord_data.get("u", 0.0)
            psi = coord_data.get("psi", 0.0)
            if norm_path not in doc_coords:
                doc_coords[norm_path] = []
            doc_coords[norm_path].append((u, psi))
            
    print("Scanning workspace for markdown files...", flush=True)
    all_md_files = []
    for root, dirs, files in os.walk(workspace_root):
        dirs[:] = [d for d in dirs if d.lower() not in ['.git', '.agent', 'bible', 'node_modules', 'venv', 'env', '_archive', 'drawing_board']]
        for file in files:
            if file.lower().endswith('.md'):
                full_path = os.path.abspath(os.path.join(root, file))
                if "bible" not in full_path.lower():
                    all_md_files.append(full_path)
                    
    print(f"Found {len(all_md_files)} candidate markdown documents.", flush=True)
    
    categories = {
        "Greater Good (+u, +psi)": [],
        "Lesser Good (+u, -psi)": [],
        "Greatest Lie (-u, +psi)": [],
        "Greater Evil (-u, -psi)": [],
        "Neutral / Unclassified": []
    }
    
    for file_path in all_md_files:
        rel_path = os.path.relpath(file_path, workspace_root)
        coords = doc_coords.get(file_path, [])
        if not coords:
            categories["Neutral / Unclassified"].append((rel_path, (0.0, 0.0)))
            continue
            
        avg_u = sum(c[0] for c in coords) / len(coords)
        avg_psi = sum(c[1] for c in coords) / len(coords)
        
        if avg_u >= 0.0 and avg_psi >= 0.0:
            categories["Greater Good (+u, +psi)"].append((rel_path, (avg_u, avg_psi)))
        elif avg_u >= 0.0 and avg_psi < 0.0:
            categories["Lesser Good (+u, -psi)"].append((rel_path, (avg_u, avg_psi)))
        elif avg_u < 0.0 and avg_psi >= 0.0:
            categories["Greatest Lie (-u, +psi)"].append((rel_path, (avg_u, avg_psi)))
        else:
            categories["Greater Evil (-u, -psi)"].append((rel_path, (avg_u, avg_psi)))
            
    calibrated_categories = {}
    for cat_name, file_list in categories.items():
        count = len(file_list)
        if count == 0:
            continue
        if count <= 300:
            calibrated_categories[cat_name] = file_list
        else:
            # Calculate number of parts needed to keep each under 300 files
            num_parts = math.ceil(count / 300)
            print(f"Category '{cat_name}' has {count} files. Splitting into {num_parts} parts...", flush=True)
            
            # Sort files by coordinate to keep similar files together
            # Sorting by u first, then psi
            sorted_files = sorted(file_list, key=lambda x: (x[1][0], x[1][1]))
            
            part_size = math.ceil(count / num_parts)
            for i in range(num_parts):
                part_files = sorted_files[i*part_size : (i+1)*part_size]
                calibrated_categories[f"{cat_name} (Part {i+1} of {num_parts})"] = part_files
                
    out_file = os.path.join(script_dir, "categorized_file_list.md")
    print(f"Writing categorized list to {out_file}...", flush=True)
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# Categorized Markdown File Registry\n\n")
        f.write("This index registers all repository markdown documents (excluding the Bible) categorized by their dominant Psochic Hegemony coordinates. Each category contains fewer than 300 files.\n\n")
        
        f.write("## Category Summary Table\n\n")
        f.write("| Category Name | File Count |\n|:---|:---|\n")
        for name, files in calibrated_categories.items():
            f.write(f"| {name} | {len(files)} |\n")
        f.write("\n---\n\n")
        
        for name, files in calibrated_categories.items():
            f.write(f"## {name} (Count: {len(files)})\n\n")
            for rel_path, (u, psi) in sorted(files, key=lambda x: x[0]):
                f.write(f"* [{os.path.basename(rel_path)}](file:///{os.path.join(workspace_root, rel_path).replace(os.sep, '/')}) — Coordinate: `({u:.2f}, {psi:.2f})`\n")
            f.write("\n")
            
    print("File list categorization complete!", flush=True)

if __name__ == "__main__":
    main()
