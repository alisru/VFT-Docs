import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from batch_upload_notebooks import NotebookLMClient, make_human_readable_label

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

    print("Spawning NotebookLM MCP server to re-align manifests...", flush=True)
    client = NotebookLMClient(executable)

    # Fetch online notebooks list to find notebook IDs
    print("Fetching online notebooks list...", flush=True)
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

        # Match notebook ID
        notebook_id = manifest_data.get("notebook_id")
        if not notebook_id:
            notebook_id = online_notebooks.get(cat_name.lower())
            if not notebook_id:
                print(f"No online notebook found for '{cat_name}', resetting all files to pending.")
                for file_entry in manifest_data.get("files", []):
                    file_entry["status"] = "pending"
                    file_entry["source_id"] = None
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    json.dump(manifest_data, f, indent=2)
                continue
            manifest_data["notebook_id"] = notebook_id

        print(f"\n--- Aligning manifest for '{cat_name}' (ID: {notebook_id}) ---", flush=True)

        # Get actual online sources inside this notebook
        online_sources = {}
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
                    except Exception:
                        pass

            if isinstance(sources_list, list):
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
                            online_sources[src_title.strip().lower()] = src_id.strip()

            print(f"Online sources found: {len(online_sources)}")

            # Align each file in manifest
            aligned_count = 0
            pending_count = 0
            
            for file_entry in manifest_data.get("files", []):
                file_base = os.path.basename(file_entry["relative_path"])
                human_title = make_human_readable_label(file_base).strip().lower()
                
                if human_title in online_sources:
                    online_id = online_sources[human_title]
                    file_entry["status"] = "uploaded"
                    file_entry["source_id"] = online_id
                    aligned_count += 1
                else:
                    file_entry["status"] = "pending"
                    file_entry["source_id"] = None
                    pending_count += 1

            print(f"Manifest Aligned: {aligned_count} matches online, {pending_count} reset to pending.")
            
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest_data, f, indent=2)

        except Exception as e:
            print(f"Error aligning category {cat_name}: {e}")

    client.close()
    print("\nAlignment complete!")

if __name__ == "__main__":
    main()
