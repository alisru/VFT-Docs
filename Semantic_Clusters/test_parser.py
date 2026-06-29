import sys
import os
import json

def main():
    log_path = r"C:\Users\hungh\.gemini\antigravity\brain\3f750c65-1029-439c-a228-78d05acbe166\.system_generated\tasks\task-2913.log"
    if not os.path.exists(log_path):
        print(f"Log not found at {log_path}")
        return
        
    with open(log_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    start = False
    json_lines = []
    for line in lines:
        if "--- RESPONSE ---" in line:
            start = True
            continue
        if start:
            json_lines.append(line)
            
    res_str = "".join(json_lines).strip()
    if "isError" in res_str:
        idx = res_str.rfind("}")
        if idx != -1:
            res_str = res_str[:idx+1]
            
    try:
        get_res = json.loads(res_str)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        return
        
    sources_list = []
    existing_sources = {}
    
    for content_item in get_res.get("content", []):
        text = content_item.get("text", "")
        if text.strip().startswith("{"):
            try:
                raw_json = json.loads(text)
                nb_data = raw_json.get("notebook")
                # Parse array: notebook is [[title, [sources]]]
                if isinstance(nb_data, list) and len(nb_data) > 0:
                    inner_nb = nb_data[0]
                    if isinstance(inner_nb, list) and len(inner_nb) > 1:
                        sources_list = inner_nb[1]
                        break
            except Exception as parse_e:
                print(f"Failed to parse: {parse_e}")
                
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
                    
    print(f"TEST PARSER RESULT: Successfully extracted {len(existing_sources)} online sources.")
    sample = list(existing_sources.items())[:5]
    print("Sample:")
    for k, v in sample:
        print(f"  - '{k}': {v}")

if __name__ == "__main__":
    main()
