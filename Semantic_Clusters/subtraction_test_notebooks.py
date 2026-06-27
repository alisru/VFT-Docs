import os
import sys
import re
import json

# Import helpers from generate_notebooks
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_notebooks import classify_by_topic, normalize_filename, extract_version, make_human_readable_label
from analyze_google_notebooks import extract_source_names_from_json

def normalize_name(filename):
    name = os.path.basename(filename)
    name = name.lower()
    # Strip common file extensions
    name = re.sub(r'\.md$|\.pdf$|\.html$|\.txt$', '', name, flags=re.IGNORECASE)
    # Strip version suffix (e.g., v1, v2)
    name = re.sub(r'[\s_\-\(]+v\d+(?:[.,]\d+)*[\)]*$', '', name)
    # Strip copy suffix (e.g., _1, (1), copy)
    name = re.sub(r'[\s_\-\(]+(1|2|3|4|copy)[\)]*$', '', name)
    # Clean non-alphanumeric
    name = "".join(c for c in name if c.isalnum())
    return name

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    # 1. Scan local workspace
    print("Scanning workspace for markdown files...", flush=True)
    all_md_files = []
    
    for root, dirs, files in os.walk(workspace_root):
        dirs[:] = [d for d in dirs if d.lower() not in ['.git', '.agent', 'bible', 'node_modules', 'venv', 'env', 'geometry of definitions']]
        for file in files:
            if file.lower().endswith('.md'):
                full_path = os.path.abspath(os.path.join(root, file))
                if "bible" not in full_path.lower():
                    all_md_files.append(full_path)
                    
    print(f"Found {len(all_md_files)} markdown documents locally.", flush=True)
    
    # 2. Resolve duplicates
    unique_registry = {}
    for file_path in all_md_files:
        rel_path = os.path.relpath(file_path, workspace_root)
        file_name = os.path.basename(file_path)
        
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
            
    print(f"Deduplicated to {len(unique_registry)} unique local files.", flush=True)
    
    # Group local files by hypothetical category
    local_notebooks = {}
    for norm_name, (file_path, rel_path, ver, mtime, category) in unique_registry.items():
        if category not in local_notebooks:
            local_notebooks[category] = []
        local_notebooks[category].append(file_path)
        
    # 3. Load all uploaded files in Google Notebooks
    print("Loading Google NotebookLM file lists...", flush=True)
    google_files = set()
    
    # Load Geometry of Definition output
    geom_def_path = "C:\\Users\\hungh\\.gemini\\antigravity\\brain\\3f750c65-1029-439c-a228-78d05acbe166\\.system_generated\\steps\\2121\\output.txt"
    if os.path.exists(geom_def_path):
        with open(geom_def_path, 'r', encoding='utf-8') as f:
            try:
                raw = json.load(f)
                google_files.update(extract_source_names_from_json(raw))
            except Exception:
                pass
                
    # Load google_notebooks_file_list.md contents
    file_list_path = os.path.join(script_dir, "google_notebooks_file_list.md")
    if os.path.exists(file_list_path):
        with open(file_list_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract bullet points
            bullets = re.findall(r'^\*\s+(.+)$', content, re.MULTILINE)
            google_files.update(bullets)
            
    # Normalize Google files for lookup
    normalized_google_files = {normalize_name(f) for f in google_files}
    print(f"Loaded {len(google_files)} unique uploaded sources from Google (normalized: {len(normalized_google_files)}).", flush=True)
    
    # 4. Perform Subtraction Test
    output_report_path = os.path.join(script_dir, "subtraction_test_report.md")
    print(f"Writing Subtraction Test report to {output_report_path}...", flush=True)
    
    with open(output_report_path, 'w', encoding='utf-8') as rep:
        rep.write("# Hypothetical Notebooks: Subtraction Test (Non-Duplicate Upload Guide)\n\n")
        rep.write("This guide shows which local files **have NOT yet been uploaded** to Google NotebookLM, grouped by your hypothetical notebooks.\n\n")
        
        overall_missing = 0
        overall_uploaded = 0
        
        category_summaries = []
        
        for cat, filepaths in sorted(local_notebooks.items()):
            missing_files = []
            uploaded_files = []
            
            for path in filepaths:
                name = os.path.basename(path)
                norm = normalize_name(name)
                
                if norm in normalized_google_files:
                    uploaded_files.append(path)
                else:
                    missing_files.append(path)
                    
            overall_missing += len(missing_files)
            overall_uploaded += len(uploaded_files)
            
            category_summaries.append((cat, len(filepaths), len(uploaded_files), len(missing_files), missing_files))
            
        # Summary Table
        rep.write("## Executive Summary\n\n")
        rep.write("| Hypothetical Notebook | Total Local | Already Uploaded | Pending Upload (New) | % Synced |\n")
        rep.write("| :--- | :---: | :---: | :---: | :---: |\n")
        for cat, total, uploaded, missing, _ in category_summaries:
            pct = (uploaded / total * 100) if total > 0 else 0
            rep.write(f"| {cat} | {total} | {uploaded} | {missing} | {pct:.1f}% |\n")
        rep.write(f"| **TOTAL** | **{overall_uploaded + overall_missing}** | **{overall_uploaded}** | **{overall_missing}** | **{(overall_uploaded/(overall_uploaded+overall_missing)*100):.1f}%** |\n\n")
        
        # Detailed Lists of Missing Files
        rep.write("## Pending Upload Lists (Non-Duplicate Files)\n\n")
        for cat, total, uploaded, missing, missing_list in category_summaries:
            rep.write(f"### {cat} ({len(missing_list)} files pending)\n\n")
            if not missing_list:
                rep.write("*All files in this category have already been uploaded.*\n\n")
                continue
                
            for path in sorted(missing_list):
                rel = os.path.relpath(path, workspace_root)
                label = make_human_readable_label(os.path.basename(path))
                rep.write(f"* [{label}](file:///{path.replace('\\', '/')})\n")
            rep.write("\n")
            
    print("Done writing subtraction report!", flush=True)

if __name__ == "__main__":
    main()
