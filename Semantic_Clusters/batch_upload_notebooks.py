import os
import sys
import subprocess
import json
import time
import re

# Categories mapping
CATEGORIES_SLUGS = {
    "Information Physics & Thermodynamics": "physics-thermodynamics",
    "Metaphysics: Linguistic Relationalism & Psychology": "metaphysics-linguistic-psychology",
    "Metaphysics: Ontological Metaphysics & Theology": "metaphysics-ontological-theology",
    "Ontological Auditing & Geopolitics": "ontological-auditing-geopolitics",
    "System Protocols & Operational Guides": "system-protocols-operational-guides",
    "Unstructured Notes & Chat Logs": "unstructured-notes-chat-logs"
}

class NotebookLMClient:
    def __init__(self, executable_path):
        self.proc = subprocess.Popen(
            [executable_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            bufsize=1
        )
        self.request_id = 1
        self._initialize()

    def _initialize(self):
        # Step 1: initialize request
        init_req = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "batch-uploader", "version": "1.0.0"}
            },
            "id": self.request_id
        }
        self.request_id += 1
        self._send(init_req)
        self._read_response(1) # wait for ID 1

        # Step 2: initialized notification
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        self._send(initialized_notification)
        print("[Client] Handshake complete and initialized.")

    def _send(self, payload):
        self.proc.stdin.write(json.dumps(payload) + '\n')
        self.proc.stdin.flush()

    def _read_response(self, req_id):
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("Subprocess exited unexpectedly.")
            if line.strip().startswith("{"):
                res = json.loads(line)
                if res.get("id") == req_id:
                    return res

    def call_tool(self, tool_name, arguments):
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": self.request_id
        }
        curr_id = self.request_id
        self.request_id += 1
        self._send(payload)
        response = self._read_response(curr_id)
        
        if "error" in response:
            raise RuntimeError(f"Tool call error: {response['error']}")
        return response.get("result", {})

    def close(self):
        self.proc.terminate()

def make_human_readable_label(filename):
    # Match the label normalization from generate_notebooks
    name = os.path.splitext(filename)[0]
    name = name.replace("_", " ").replace("-", " ")
    # Replace multiple spaces
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')

    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    executable = r"E:\Python\Scripts\notebooklm-mcp.exe"
    if not os.path.exists(executable):
        print(f"Error: Could not find notebooklm-mcp executable at {executable}")
        sys.exit(1)

    print("Spawning NotebookLM MCP server...", flush=True)
    client = NotebookLMClient(executable)

    # 1. Fetch existing online notebooks
    print("Fetching existing notebooks from account...", flush=True)
    try:
        notebook_list_res = client.call_tool("notebook_list", {})
        # Result content is usually a list of text describing the notebooks, 
        # or structured data inside the result. Let's see:
        print(f"Notebook List Result: {json.dumps(notebook_list_res, indent=2)}")
    except Exception as e:
        print(f"Error listing notebooks: {e}")
        client.close()
        sys.exit(1)

    # Parse notebooks if returned in result
    # Depending on how the notebooklm-mcp server formats results, it might return them in "content"
    # Parse notebooks if returned in result
    # Supports both nested JSON string inside content text, structured JSON notebooks, and plaintext Name/ID lists
    online_notebooks = {}
    
    content_list = notebook_list_res.get("content", [])
    
    # 1. Try parsing double-serialized JSON string inside content text
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
                            online_notebooks[title.strip()] = uuid.strip()
            except Exception:
                pass

    # 2. Try structured JSON extraction from root if present
    if not online_notebooks:
        notebooks = notebook_list_res.get("notebooks")
        if isinstance(notebooks, list):
            for nb in notebooks:
                title = nb.get("title") or nb.get("name")
                uuid = nb.get("id") or nb.get("notebook_id")
                if title and uuid:
                    online_notebooks[title.strip()] = uuid.strip()
    
    # 3. Fallback to plaintext regex parsing
    if not online_notebooks:
        for item in content_list:
            text = item.get("text", "")
            matches = re.findall(r'Name:\s*(.*?)\r?\nID:\s*([a-f0-9\-]{36})', text, re.IGNORECASE)
            for name, uuid in matches:
                online_notebooks[name.strip()] = uuid.strip()

    print(f"Detected online notebooks: {online_notebooks}", flush=True)

    # 2. Iterate through categories and process manifests
    for cat_name, slug in CATEGORIES_SLUGS.items():
        manifest_path = os.path.join(script_dir, f"notebook-{slug}-filelist.json")
        if not os.path.exists(manifest_path):
            print(f"Manifest not found for {cat_name}, skipping.")
            continue

        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"\nProcessing category: {cat_name}...", flush=True)

        # Ensure we have a notebook ID
        notebook_id = data.get("notebook_id")
        if not notebook_id:
            # Check if it already exists online (case-insensitive check)
            matched_uuid = None
            for online_name, online_uuid in online_notebooks.items():
                if online_name.strip().lower() == cat_name.strip().lower():
                    matched_uuid = online_uuid
                    break

            if matched_uuid:
                notebook_id = matched_uuid
                print(f"Found existing online notebook UUID for '{cat_name}': {notebook_id}")
            else:
                print(f"Creating new notebook online: '{cat_name}'...")
                try:
                    create_res = client.call_tool("notebook_create", {"title": cat_name})
                    # Try structured ID extraction
                    notebook_id = create_res.get("id") or create_res.get("notebook_id")
                    
                    if not notebook_id:
                        create_text = "".join([c.get("text", "") for c in create_res.get("content", [])])
                        uuid_match = re.search(r'(?:ID|UUID):\s*([a-f0-9\-]{36})|([a-f0-9\-]{36})', create_text, re.IGNORECASE)
                        if uuid_match:
                            notebook_id = uuid_match.group(1) or uuid_match.group(2)
                    
                    if notebook_id:
                        print(f"Successfully created notebook. UUID: {notebook_id}")
                    else:
                        print(f"Failed to extract UUID from create response: {create_res}")
                        continue
                except Exception as e:
                    print(f"Error creating notebook: {e}")
                    continue

            # Save the UUID back to the JSON manifest
            data["notebook_id"] = notebook_id
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)

        # 3. Fetch existing sources in this notebook to guarantee zero file title duplication
        print(f"Fetching existing sources inside notebook {notebook_id}...", flush=True)
        existing_sources = {}
        try:
            get_res = client.call_tool("notebook_get", {"notebook_id": notebook_id})
            sources_list = []
            
            # Try parsing double-serialized JSON string inside content text
            for content_item in get_res.get("content", []):
                text = content_item.get("text", "")
                if text.strip().startswith("{"):
                    try:
                        raw_json = json.loads(text)
                        nb_data = raw_json.get("notebook")
                        # Positional array parsing: notebook is [[title, [sources]]]
                        if isinstance(nb_data, list) and len(nb_data) > 0:
                            inner_nb = nb_data[0]
                            if isinstance(inner_nb, list) and len(inner_nb) > 1:
                                sources_list = inner_nb[1]
                                break
                    except Exception as parse_e:
                        print(f"Failed to parse inner notebook json: {parse_e}")
            
            # Parse sources from positional arrays: src is [[id], title, ...]
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
                            existing_sources[src_title.strip().lower()] = src_id.strip()
            print(f"Detected {len(existing_sources)} existing online sources in notebook.", flush=True)
        except Exception as e:
            print(f"Warning: Could not check existing sources: {e}. Proceeding carefully.")

        # Iterate files in manifest
        files = data.get("files", [])
        for i, file_entry in enumerate(files):
            status = file_entry.get("status")
            rel_path = file_entry.get("relative_path")
            source_id = file_entry.get("source_id")

            if status not in ["pending", "update_requested"]:
                continue

            full_path = os.path.join(workspace_root, rel_path)
            if not os.path.exists(full_path):
                print(f"Warning: Local file not found: {full_path}. Skipping.")
                continue

            human_label = make_human_readable_label(os.path.basename(full_path))

            # Strictly verify if a source with this title already exists in the notebook
            normalized_label = human_label.strip().lower()
            if normalized_label in existing_sources:
                online_id = existing_sources[normalized_label]
                print(f"[{i+1}/{len(files)}] Source '{human_label}' already exists online (ID: {online_id}). Skipping duplicate upload.", flush=True)
                # Keep source tracking updated
                file_entry["status"] = "uploaded"
                file_entry["source_id"] = online_id
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                continue

            # Handle deletion first if update is requested
            if status == "update_requested" and source_id:
                print(f"[{i+1}/{len(files)}] Deleting old source {source_id} for {rel_path}...", flush=True)
                try:
                    client.call_tool("source_delete", {"source_id": source_id, "confirm": True})
                    file_entry["source_id"] = None
                    file_entry["status"] = "pending"
                    # Flush intermediate state
                    with open(manifest_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                except Exception as e:
                    print(f"Error deleting source {source_id}: {e}. Will attempt upload anyway.")

            # Perform the upload
            print(f"[{i+1}/{len(files)}] Uploading {rel_path} to '{cat_name}'...", flush=True)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                upload_res = client.call_tool("notebook_add_text", {
                    "notebook_id": notebook_id,
                    "text": content,
                    "title": human_label
                })

                # Parse new source ID from output text if returned
                upload_text = "".join([c.get("text", "") for c in upload_res.get("content", [])])
                source_match = re.search(r'source\s+([a-f0-9\-]{36})|([a-f0-9\-]{36})', upload_text, re.IGNORECASE)
                
                new_source_id = None
                if source_match:
                    new_source_id = source_match.group(1) or source_match.group(2)
                
                file_entry["status"] = "uploaded"
                file_entry["source_id"] = new_source_id
                print(f"Successfully uploaded: {human_label} (Source UUID: {new_source_id})")

                # Flush manifest immediately
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)

                # Cooldown limit to prevent API spamming
                time.sleep(3)

            except Exception as e:
                print(f"Error uploading {rel_path}: {e}")
                # Safe fallback: leave as is so we can retry later
                continue

    print("\nBatch upload process run completed.", flush=True)
    client.close()

if __name__ == "__main__":
    main()
