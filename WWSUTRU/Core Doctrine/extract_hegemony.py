import re
import json
import os
import sys

def parse_hegemony_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Flexible Regex to capture: category: { id: { v:..., p:..., j:"..." } }
    # This is tricky with nested braces. We might treat it as text data.
    
    # Let's find all occurrences of pattern: key:{v:...,p:...,j:"..."}
    # Pattern for the inner object: (\d+):\{v:([\d.-]+),p:([\d.-]+),j:"(.*?)"\}
    
    pattern = r'(\d+)\s*:\s*\{\s*v\s*:\s*([\d.-]+)\s*,\s*p\s*:\s*([\d.-]+)\s*,\s*j\s*:\s*"(.*?)"\s*\}'
    matches = re.findall(pattern, content, re.DOTALL)
    
    # We also want to know which category (natural, goodTruth) they belong to.
    # We can split the file by category keys first.
    
    categories = ["natural", "goodTruth", "badTruth", "goodLie", "badLie", "goodPref", "badPref"]
    results = []
    
    for category in categories:
        # Find the block for this category
        # Assumes structure: category: { ... }
        cat_start = content.find(category + ":")
        if cat_start == -1: continue
        
        # Find the end of this block (simple heuristic: look for next category or end of file)
        # Better: just look for matches after this index, until next category index
        
        # Actually, let's just find all matches and assign heuristics or just treat IDs as unique enough combined with context.
        # But we really want the category.
        
        # Let's verify if the regex works on the whole file and we just attribute category by range.
        pass

    # New Approach: Iterate matches and find which category block they are in.
    # Find indices of categories
    cat_indices = sorted([(cat, content.find(cat + ":")) for cat in categories if content.find(cat + ":") != -1], key=lambda x: x[1])
    
    nodes = []
    
    for i, (cat, start_idx) in enumerate(cat_indices):
        end_idx = cat_indices[i+1][1] if i+1 < len(cat_indices) else len(content)
        block = content[start_idx:end_idx]
        
        block_matches = re.findall(pattern, block)
        
        for state_id, v, p, j in block_matches:
            node_id = f"node_heg_{cat}_{state_id}"
            
            node = {
                "id": node_id,
                "origin": { "chat_id": "hegemonyContexts", "timestamp": "Unknown", "stream_index": int(state_id) },
                "meta": {
                    "type_1_domain": "Ethics",
                    "type_2_class": "Moral State",
                    "type_3_instance": f"{cat} {state_id}",
                    "primary_coordinate": { "plane": "Null", "vector": "Null", "collapse_state": "Null" } 
                },
                "fractal_edges": {
                    "cause": [], "effect": [],
                    "who": [], "what": ["v: " + v, "p: " + p], "where": [cat], "why": [], "how": []
                },
                "payload": {
                    "summary": j,
                    "full_content": f"Category: {cat}\nState ID: {state_id}\nMoral Vector (v): {v}\nWill Vector (p): {p}\nJudgment: {j}"
                }
            }
            nodes.append(node)
            
    return nodes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_hegemony.py <filepath>")
        sys.exit(1)
        
    target_file = sys.argv[1]
    nodes = parse_hegemony_file(target_file)
    
    output_path = os.path.join(os.path.dirname(target_file), "graphs", "hegemony_contexts_graph.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(nodes, f, indent=2)
        
    print(f"Generated {len(nodes)} nodes in {output_path}")
