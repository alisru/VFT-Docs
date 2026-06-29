import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from batch_upload_notebooks import NotebookLMClient

def main():
    executable = r"E:\Python\Scripts\notebooklm-mcp.exe"
    client = NotebookLMClient(executable)
    
    notebook_id = "664250dd-ceed-4703-bc87-b46059bcb25e"
    print(f"Calling notebook_get for {notebook_id}...", flush=True)
    res = client.call_tool("notebook_get", {"notebook_id": notebook_id})
    
    print("\n--- RESPONSE ---")
    print(json.dumps(res, indent=2))
    
    client.close()

if __name__ == "__main__":
    main()
