import os
import json
import sys

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    md_folder = os.path.join(workspace_root, "_VFT MD")
    output_path = os.path.join(script_dir, "corpus_manifest.json")

    # Force stdout encoding to UTF-8
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')

    if not os.path.exists(md_folder):
        print(f"Error: _VFT MD folder not found at: {md_folder}")
        sys.exit(1)

    print(f"Scanning documents in: {md_folder}")
    manifest = []
    
    # Files to exclude (e.g., system indices, templates, etc.)
    exclude_prefixes = ("index_", "Master_Index", "temp_", "draft_")
    exclude_folders = {"_AI_Project_Plans", "_chat_logs", ".gemini", ".git", ".agents"}

    for root, dirs, files in os.walk(md_folder):
        # Exclude hidden or build folders
        dirs[:] = [d for d in dirs if d not in exclude_folders and not d.startswith('.')]
        
        for file in files:
            if not file.endswith('.md'):
                continue
            if any(file.startswith(prefix) for prefix in exclude_prefixes):
                continue
                
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, md_folder)
            
            # Simple title extraction: try to read the first H1 header, otherwise use filename
            title = os.path.splitext(file)[0]
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        clean = line.strip()
                        if clean.startswith('# '):
                            title = clean[2:].strip()
                            break
            except Exception:
                pass

            manifest.append({
                "file_path": os.path.abspath(full_path),
                "relative_path": rel_path.replace('\\', '/'),
                "title": title
            })

    print(f"Found {len(manifest)} valid markdown files for ingestion.")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"Manifest written to {output_path}")

if __name__ == "__main__":
    main()
