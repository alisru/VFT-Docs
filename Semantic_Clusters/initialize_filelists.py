import os
import sys
import re
import json
import math

# Setup sys.path to import generate_notebooks helpers
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_notebooks import classify_by_topic, normalize_filename, extract_version, get_sorting_key
from subtraction_test_notebooks import normalize_name

def should_exclude(rel_path, file_name):
    path_lower = rel_path.lower()
    name_lower = file_name.lower()
    
    # Exclude directories related to AI project planning or chat logs
    plan_dirs = ['_ai_plans', '_ai_project_plans', '_chat_logs', '.agent', 'drawing board', 'scratch']
    if any(pd in path_lower for pd in plan_dirs):
        return True
        
    # Exclude files that are implementation plans, tasks, or walkthroughs
    plan_keywords = ['implementation_plan', 'task.md', 'walkthrough.md', 'beehive_workflow_analysis', 'plan_orchestrator']
    if any(pk in name_lower for pk in plan_keywords):
        return True
        
    return False

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    # 1. Scan local workspace
    print("Scanning workspace for markdown files...", flush=True)
    all_md_files = []
    
    for root, dirs, files in os.walk(workspace_root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in ['venv', 'env', 'bible', 'node_modules', 'geometry of definitions', 'scratch', 'drawing board']]
        for file in files:
            if file.lower().endswith('.md'):
                full_path = os.path.abspath(os.path.join(root, file))
                if "bible" not in full_path.lower():
                    all_md_files.append(full_path)
                    
    # 2. Resolve duplicates
    unique_registry = {}
    for file_path in all_md_files:
        rel_path = os.path.relpath(file_path, workspace_root)
        file_name = os.path.basename(file_path)
        
        # Check exclusion rules first
        if should_exclude(rel_path, file_name):
            continue
            
        category = classify_by_topic(rel_path, file_name)
        if category == "SKIP":
            continue
            
        norm_name = normalize_filename(file_name)
        ver = extract_version(file_name)
        mtime = os.path.getmtime(file_path)
        
        if norm_name in unique_registry:
            existing_path, existing_rel, existing_ver, existing_mtime, existing_cat = unique_registry[norm_name]
            
            if ver > existing_ver:
                unique_registry[norm_name] = (file_path, rel_path, ver, mtime, category)
            elif ver < existing_ver:
                pass
            else:
                if mtime > existing_mtime:
                    unique_registry[norm_name] = (file_path, rel_path, ver, mtime, category)
        else:
            unique_registry[norm_name] = (file_path, rel_path, ver, mtime, category)
            
    print(f"Deduplicated to {len(unique_registry)} unique local files after filtering out plan/task logs.", flush=True)
    
    # 3. Group files into broad categories
    grouped = {
        "Information Physics & Thermodynamics": [],
        "Metaphysics & Actualism": [],
        "Ontological Auditing & Geopolitics": [],
        "System Protocols & Operational Guides": [],
        "Unstructured Notes & Chat Logs": []
    }
    
    for norm_name, (file_path, rel_path, ver, mtime, category) in unique_registry.items():
        if category in grouped:
            grouped[category].append((file_path, rel_path))

    # 4. Map to formal 6-notebook structure (splitting Metaphysics & Actualism in half)
    notebook_files = {
        "Information Physics & Thermodynamics": grouped["Information Physics & Thermodynamics"],
        "Metaphysics: Linguistic Relationalism & Psychology": [],
        "Metaphysics: Ontological Metaphysics & Theology": [],
        "Ontological Auditing & Geopolitics": grouped["Ontological Auditing & Geopolitics"],
        "System Protocols & Operational Guides": grouped["System Protocols & Operational Guides"],
        "Unstructured Notes & Chat Logs": grouped["Unstructured Notes & Chat Logs"]
    }
    
    # Handle split for Metaphysics
    metaphysics_all = grouped["Metaphysics & Actualism"]
    # Sort them using the same get_sorting_key helper
    metaphysics_all.sort(key=lambda item: get_sorting_key(item[1]))
    
    count = len(metaphysics_all)
    part_size = math.ceil(count / 2)
    
    notebook_files["Metaphysics: Linguistic Relationalism & Psychology"] = metaphysics_all[0:part_size]
    notebook_files["Metaphysics: Ontological Metaphysics & Theology"] = metaphysics_all[part_size:]
    
    # 5. Load already uploaded files from Google Notebook list
    google_files = set()
    file_list_path = os.path.join(script_dir, "google_notebooks_file_list.md")
    if os.path.exists(file_list_path):
        with open(file_list_path, 'r', encoding='utf-8') as f:
            content = f.read()
            bullets = re.findall(r'^\*\s+(.+)$', content, re.MULTILINE)
            google_files.update(bullets)
            
    normalized_google_files = {normalize_name(f) for f in google_files}
    
    # Slugs registry for 6 categories
    categories_slugs = {
        "Information Physics & Thermodynamics": "physics-thermodynamics",
        "Metaphysics: Linguistic Relationalism & Psychology": "metaphysics-linguistic-psychology",
        "Metaphysics: Ontological Metaphysics & Theology": "metaphysics-ontological-theology",
        "Ontological Auditing & Geopolitics": "ontological-auditing-geopolitics",
        "System Protocols & Operational Guides": "system-protocols-operational-guides",
        "Unstructured Notes & Chat Logs": "unstructured-notes-chat-logs"
    }
    
    # Write JSONs
    for cat_name, file_entries in notebook_files.items():
        slug = categories_slugs[cat_name]
        data = {
            "notebook_name": cat_name,
            "notebook_id": None,
            "files": []
        }
        
        for file_path, rel_path in file_entries:
            norm = normalize_name(os.path.basename(file_path))
            is_uploaded = norm in normalized_google_files
            
            data["files"].append({
                "relative_path": rel_path.replace("\\", "/"),
                "status": "uploaded" if is_uploaded else "pending",
                "source_id": None
            })
            
        out_path = os.path.join(script_dir, f"notebook-{slug}-filelist.json")
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Generated {out_path} with {len(data['files'])} entries.", flush=True)

if __name__ == "__main__":
    main()
