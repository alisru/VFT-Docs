import subprocess
import json
import os
import sys
import time

# Import classification logic from generate_notebooks
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from generate_notebooks import classify_by_topic

def get_notebook_sources(notebook_id):
    print(f"Connecting to MCP to fetch details for notebook: {notebook_id}...", flush=True)
    
    # Inject chrome path so the subprocess finds the auth profile
    env = os.environ.copy()
    env["CHROME_PATH"] = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    
    p = subprocess.Popen(
        ['E:\\Python\\Scripts\\notebooklm-mcp.exe'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        text=True
    )
    
    # 1. Send initialize request
    init_req = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "notebooklm-cli-client", "version": "1.0.0"}
        },
        "id": 1
    }
    p.stdin.write(json.dumps(init_req) + '\n')
    p.stdin.flush()
    
    # Skip init response
    while True:
        line = p.stdout.readline()
        if not line:
            break
        if line.strip().startswith("{"):
            break
            
    # Send initialized notification
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    p.stdin.write(json.dumps(initialized_notification) + '\n')
    p.stdin.flush()
    
    # Send notebook_get request
    get_req = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "notebook_get",
            "arguments": {
                "notebook_id": notebook_id
            }
        },
        "id": 2
    }
    p.stdin.write(json.dumps(get_req) + '\n')
    p.stdin.flush()
    
    # Read get response
    get_res = None
    while True:
        line = p.stdout.readline()
        if not line:
            break
        if line.strip().startswith("{"):
            get_res = json.loads(line)
            break
            
    p.terminate()
    return get_res

def extract_source_names_from_json(data):
    if not data or ("result" not in data and "notebook" not in data):
        return []
        
    if "result" in data:
        result = data.get("result", {})
        content_blocks = result.get("content", [])
        if not content_blocks:
            return []
        text = content_blocks[0].get("text", "")
        try:
            nb_data = json.loads(text)
        except Exception:
            return []
    else:
        nb_data = data
            
    notebook_list = nb_data.get("notebook", [])
    if not notebook_list:
        return []
        
    first_item = notebook_list[0]
    if len(first_item) < 2:
        return []
        
    sources = first_item[1]
    filenames = []
    for src in sources:
        if len(src) > 1:
            filenames.append(src[1])
    return filenames

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Load Geometry of Definition (already fetched)
    geom_def_path = "C:\\Users\\hungh\\.gemini\\antigravity\\brain\\3f750c65-1029-439c-a228-78d05acbe166\\.system_generated\\steps\\2121\\output.txt"
    print("Loading pre-fetched Geometry of Definition sources...", flush=True)
    with open(geom_def_path, 'r', encoding='utf-8') as f:
        geom_def_raw = json.load(f)
    
    geom_def_sources = extract_source_names_from_json(geom_def_raw)
    print(f"Loaded {len(geom_def_sources)} sources for Geometry of Definition.", flush=True)
    
    # Sleep to clear any leftover Chrome processes
    time.sleep(2)
    
    # 2. Fetch Vector Field Theory sources
    vft_raw = get_notebook_sources("79d71291-8c03-4ad4-91fd-35e2832ab76f")
    vft_sources = extract_source_names_from_json(vft_raw)
    print(f"Fetched {len(vft_sources)} sources for Vector Field Theory.", flush=True)
    
    # Sleep to clear Chrome port 9222
    time.sleep(4)
    
    # 3. Fetch WWSUTRU sources
    wwsutru_raw = get_notebook_sources("b1d9ab6a-4994-4070-b49f-ad9668bb17fd")
    wwsutru_sources = extract_source_names_from_json(wwsutru_raw)
    print(f"Fetched {len(wwsutru_sources)} sources for WWSUTRU.", flush=True)
    
    # Group analyze how they map to hypothetical notebooks
    target_notebooks = {
        "Geometry of Definition": geom_def_sources,
        "Vector Field Theory": vft_sources,
        "WWSUTRU": wwsutru_sources
    }
    
    # Write complete list to Markdown
    output_md_path = os.path.join(script_dir, "google_notebooks_file_list.md")
    print(f"Writing source list to {output_md_path}...", flush=True)
    
    with open(output_md_path, 'w', encoding='utf-8') as md:
        md.write("# Google NotebookLM Source File Registry\n\n")
        md.write("This file contains the complete list of files imported into your main Google NotebookLM notebooks, classified by notebook.\n\n")
        
        for name, sources in sorted(target_notebooks.items()):
            md.write(f"## {name} ({len(sources)} files)\n\n")
            
            # Sort sources alphabetically
            for src in sorted(sources):
                md.write(f"* {src}\n")
            md.write("\n")
            
    print("Done writing markdown registry!", flush=True)

if __name__ == "__main__":
    main()
