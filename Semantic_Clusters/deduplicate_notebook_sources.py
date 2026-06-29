import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from batch_upload_notebooks import NotebookLMClient

CATEGORIES_SLUGS = {
    "Information Physics & Thermodynamics": "physics-thermodynamics",
    "Metaphysics: Linguistic Relationalism & Psychology": "metaphysics-linguistic-psychology",
    "Metaphysics: Ontological Metaphysics & Theology": "metaphysics-ontological-theology",
    "Ontological Auditing & Geopolitics": "ontological-auditing-geopolitics",
    "System Protocols & Operational Guides": "system-protocols-operational-guides",
    "Unstructured Notes & Chat Logs": "unstructured-notes-chat-logs"
}

def main():
    executable = r"E:\Python\Scripts\notebooklm-mcp.exe"
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))

    print("Spawning NotebookLM MCP server for source deduplication...", flush=True)
    client = NotebookLMClient(executable)

    # First, list all online notebooks to match them
    print("Listing online notebooks...", flush=True)
    list_res = client.call_tool("notebook_list", {})
    
    online_notebooks = {}
    content_list = list_res.get("content", [])
    for item in content_list:
        text = item.get("text", "")
        if text.strip().startswith("{"):
            try:
                raw_json = json.loads(text)
                notebooks = raw_json.get("notebooks")
                if isinstance(notebooks, list):
                    for nb in notebooks:
                        title = nb.get("title") or nb.get("name")
                        uuid = nb.get("id") or nb.get("notebook_id")
                        if title and uuid:
                            online_notebooks[title.strip().lower()] = uuid.strip()
            except Exception:
                pass

    for cat_name, slug in CATEGORIES_SLUGS.items():
        manifest_path = os.path.join(script_dir, f"notebook-{slug}-filelist.json")
        if not os.path.exists(manifest_path):
            continue

        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest_data = json.load(f)

        notebook_id = manifest_data.get("notebook_id")
        if not notebook_id:
            # Fallback to online matching
            notebook_id = online_notebooks.get(cat_name.lower())
            if not notebook_id:
                print(f"\nNo online notebook found for category '{cat_name}', skipping deduplication.")
                continue
            manifest_data["notebook_id"] = notebook_id

        print(f"\n--- Deduplicating sources in notebook '{cat_name}' (ID: {notebook_id}) ---", flush=True)

        # Get existing sources inside this notebook
        try:
            get_res = client.call_tool("notebook_get", {"notebook_id": notebook_id})
            sources_list = []
            
            for content_item in get_res.get("content", []):
                text = content_item.get("text", "")
                if text.strip().startswith("{"):
                    try:
                        raw_json = json.loads(text)
                        nb_data = raw_json.get("notebook")
                        if isinstance(nb_data, list) and len(nb_data) > 0:
                            inner_nb = nb_data[0]
                            if isinstance(inner_nb, list) and len(inner_nb) > 1:
                                sources_list = inner_nb[1]
                                break
                    except Exception as parse_e:
                        print(f"Failed to parse inner notebook json: {parse_e}")

            if not sources_list:
                print(f"No sources detected online for '{cat_name}'.")
                continue

            # Group sources by title
            grouped_sources = {}
            for src in sources_list:
                if isinstance(src, list) and len(src) > 1:
                    src_id_container = src[0]
                    src_title = src[1]
                    
                    src_id = None
                    if isinstance(src_id_container, list) and len(src_id_container) > 0:
                        src_id = src_id_container[0]
                    elif isinstance(src_id_container, str):
                        src_id = src_id_container
                        
                    if src_title and src_id:
                        norm_title = src_title.strip().lower()
                        if norm_title not in grouped_sources:
                            grouped_sources[norm_title] = []
                        grouped_sources[norm_title].append({"id": src_id, "title": src_title})

            print(f"Found {len(grouped_sources)} unique source names in notebook. Scanning for duplicates...")

            # Track updated IDs for local manifest
            manifest_updated = False
            files_entry = manifest_data.get("files", [])

            for norm_title, sources in grouped_sources.items():
                if len(sources) > 1:
                    print(f"  Duplicate detected for '{sources[0]['title']}': found {len(sources)} occurrences.")
                    # Keep the first one, delete all others
                    keep_src = sources[0]
                    delete_srcs = sources[1:]
                    
                    print(f"    KEEPING source ID: {keep_src['id']}")
                    for del_item in delete_srcs:
                        print(f"    DELETING duplicate source ID: {del_item['id']}...", end="", flush=True)
                        try:
                            client.call_tool("source_delete", {"source_id": del_item['id'], "confirm": True})
                            print(" Success.")
                        except Exception as del_e:
                            print(f" Failed: {del_e}")

                    # Update manifest entry for this file
                    for file_entry in files_entry:
                        # Extract clean title from relative path to match normalized label
                        file_base = os.path.basename(file_entry["relative_path"])
                        # Simple alphanumeric title builder to match make_human_readable_label
                        file_title = os.path.splitext(file_base)[0].replace('_', ' ').replace('-', ' ').strip().lower()
                        
                        if file_title == norm_title:
                            file_entry["source_id"] = keep_src["id"]
                            file_entry["status"] = "uploaded"
                            manifest_updated = True
                else:
                    # Single occurrence - update local manifest with the correct online ID
                    single_src = sources[0]
                    for file_entry in files_entry:
                        file_base = os.path.basename(file_entry["relative_path"])
                        file_title = os.path.splitext(file_base)[0].replace('_', ' ').replace('-', ' ').strip().lower()
                        if file_title == norm_title:
                            if file_entry.get("source_id") != single_src["id"] or file_entry.get("status") != "uploaded":
                                file_entry["source_id"] = single_src["id"]
                                file_entry["status"] = "uploaded"
                                manifest_updated = True

            if manifest_updated:
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    json.dump(manifest_data, f, indent=2)
                print(f"Updated local manifest file list tracking for: {slug}")

        except Exception as e:
            print(f"Error processing category {cat_name}: {e}")

    client.close()
    print("\nDeduplication cleanup complete!")

if __name__ == "__main__":
    main()
