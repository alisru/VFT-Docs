import subprocess
import json
import time
import sys

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    print("Launching notebooklm-mcp server and performing protocol handshake...", flush=True)
    p = subprocess.Popen(
        ['E:\\Python\\Scripts\\notebooklm-mcp.exe'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 1. Send initialize request
    init_req = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "notebooklm-cli-client",
                "version": "1.0.0"
            }
        },
        "id": 1
    }
    p.stdin.write(json.dumps(init_req) + '\n')
    p.stdin.flush()
    
    # Read initialize response (skip fastmcp server startup logging banner on stdout/stderr if any)
    init_res = None
    while True:
        line = p.stdout.readline()
        if not line:
            break
        if line.strip().startswith("{"):
            init_res = json.loads(line)
            break
            
    if not init_res:
        print("Error: Did not receive initialization response.")
        p.terminate()
        return
        
    print("Initialization response received! Sending initialized notification...", flush=True)
    
    # 2. Send initialized notification
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    p.stdin.write(json.dumps(initialized_notification) + '\n')
    p.stdin.flush()
    
    # 3. Send tools/list request
    print("Requesting tools list...", flush=True)
    tools_req = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    }
    p.stdin.write(json.dumps(tools_req) + '\n')
    p.stdin.flush()
    
    # Read tools response
    tools_res = None
    while True:
        line = p.stdout.readline()
        if not line:
            break
        if line.strip().startswith("{"):
            tools_res = json.loads(line)
            break
            
    if tools_res:
        print("\n--- AVAILABLE TOOLS ---\n", flush=True)
        tools = tools_res.get("result", {}).get("tools", [])
        for tool in tools:
            print(f"Tool Name: {tool.get('name')}")
            print(f"Description: {tool.get('description')}")
            print("Arguments:")
            input_schema = tool.get("inputSchema", {})
            properties = input_schema.get("properties", {})
            required = input_schema.get("required", [])
            for prop_name, prop_val in properties.items():
                req_str = " (Required)" if prop_name in required else ""
                print(f"  * {prop_name}: {prop_val.get('type')}{req_str} - {prop_val.get('description', '')}")
            print("-" * 50, flush=True)
    else:
        print("Error: Could not retrieve tools list.")
        
    p.terminate()

if __name__ == "__main__":
    main()
