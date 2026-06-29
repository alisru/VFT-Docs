import os
import json

def normalize_name(filename):
    # Match the key normalization from doc_ism_mapping.json
    return os.path.basename(filename).strip()

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    
    # Slugs registry for 6 categories
    categories_slugs = {
        "Information Physics & Thermodynamics": "physics-thermodynamics",
        "Metaphysics: Linguistic Relationalism & Psychology": "metaphysics-linguistic-psychology",
        "Metaphysics: Ontological Metaphysics & Theology": "metaphysics-ontological-theology",
        "Ontological Auditing & Geopolitics": "ontological-auditing-geopolitics",
        "System Protocols & Operational Guides": "system-protocols-operational-guides",
        "Unstructured Notes & Chat Logs": "unstructured-notes-chat-logs"
    }
    
    # Load doc_ism_mapping.json
    mapping_path = os.path.join(script_dir, "doc_ism_mapping.json")
    if not os.path.exists(mapping_path):
        print("Error: doc_ism_mapping.json not found!")
        return
        
    with open(mapping_path, 'r', encoding='utf-8') as f:
        doc_mapping = json.load(f)
        
    # Build a lookup map of normalized basenames to their semantic data
    lookup_map = {}
    for filename, data in doc_mapping.items():
        lookup_map[filename.lower()] = data

    report_path = os.path.join(script_dir, "notebook_semantic_analysis.md")
    
    with open(report_path, 'w', encoding='utf-8') as rep:
        rep.write("# Semantic Topic Analysis of the 6 Hypothetical Notebooks\n\n")
        rep.write("This document provides a detailed breakdown of the macro and micro semantic topics detected for the documents inside each of the 6 hypothetical notebooks, based on their Psochic Hegemony mapping.\n\n")
        
        for notebook_name, slug in categories_slugs.items():
            manifest_path = os.path.join(script_dir, f"notebook-{slug}-filelist.json")
            if not os.path.exists(manifest_path):
                continue
                
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest_data = json.load(f)
                
            files = manifest_data.get("files", [])
            rep.write(f"## {notebook_name} (Count: {len(files)})\n\n")
            
            # Group files in this notebook by Macro Topic (node_name)
            macro_groups = {}
            unclassified = []
            
            for file_entry in files:
                rel_path = file_entry["relative_path"]
                base_name = os.path.basename(rel_path)
                
                # Try to lookup
                match_data = lookup_map.get(base_name.lower())
                if match_data:
                    macro_topic = match_data.get("node_name", "Unclassified")
                    if macro_topic not in macro_groups:
                        macro_groups[macro_topic] = []
                    macro_groups[macro_topic].append((base_name, match_data))
                else:
                    unclassified.append(base_name)
                    
            # Write Macro Topics
            for macro_topic, items in sorted(macro_groups.items()):
                rep.write(f"### Macro Topic: {macro_topic} (Count: {len(items)})\n\n")
                
                # Group by micro topics (isms) within this macro topic
                micro_groups = {}
                for base_name, match_data in items:
                    isms_tuple = tuple(sorted(match_data.get("isms", [])))
                    if not isms_tuple:
                        isms_tuple = ("General",)
                    if isms_tuple not in micro_groups:
                        micro_groups[isms_tuple] = []
                    micro_groups[isms_tuple].append((base_name, match_data))
                    
                for isms_tuple, file_items in sorted(micro_groups.items(), key=lambda x: len(x[1]), reverse=True):
                    isms_str = ", ".join(isms_tuple)
                    rep.write(f"* **Micro-Topics (Isms):** `{isms_str}` (Count: {len(file_items)})\n")
                    for base_name, match_data in file_items:
                        u = match_data.get("all_scores", {}).get("ge-gg", 0.0) # placeholder if we want to print coordinate
                        rep.write(f"  - [{base_name}](file:///{os.path.join(workspace_root, slug, base_name).replace(os.sep, '/')})\n")
                    rep.write("\n")
                    
            if unclassified:
                rep.write(f"### Macro Topic: Unclassified (Count: {len(unclassified)})\n\n")
                for base_name in sorted(unclassified):
                    rep.write(f"  - {base_name}\n")
                rep.write("\n")
                
            rep.write("---\n\n")
            
    print(f"Generated semantic topic analysis report at {report_path}")

if __name__ == "__main__":
    main()
