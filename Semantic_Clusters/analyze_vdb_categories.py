import os
import json
import sys
from collections import Counter

def load_json(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    
    print("Loading VDB topic and cluster mappings...", flush=True)
    cluster_mapping = load_json(os.path.join(script_dir, "cluster_mapping.json"))
    topic_ism = load_json(os.path.join(script_dir, "topic_ism_mapping.json"))
    
    if not cluster_mapping or not topic_ism:
        print("Error: Missing mapping files in Semantic_Clusters.", flush=True)
        return
        
    # Group paragraphs by root folder
    folder_topics = {}
    
    for item in cluster_mapping:
        file_path = item.get("file", "")
        if not file_path:
            continue
            
        rel_path = os.path.relpath(file_path, workspace_root)
        parts = rel_path.split(os.sep)
        first_part = parts[0]
        
        # Unwrap _VFT MD
        if first_part == "_VFT MD" and len(parts) > 1:
            first_part = parts[1]
            
        folder_name = first_part
        topic_id = str(item.get("topic_id", ""))
        
        if topic_id in topic_ism:
            if folder_name not in folder_topics:
                folder_topics[folder_name] = []
            folder_topics[folder_name].append(topic_id)
            
    # For each key folder, analyze VDB nodes and ISMs
    print("\n--- VECTOR DATABASE SEMANTIC TOPIC ANALYSIS ---\n", flush=True)
    
    target_folders = ["Actualism", "Physics", "WWSUTRU", "io"]
    
    for folder in target_folders:
        topics = folder_topics.get(folder, [])
        if not topics:
            continue
            
        print(f"==================================================", flush=True)
        print(f"Folder: {folder} (Total Paragraphs: {len(topics)})", flush=True)
        print(f"==================================================", flush=True)
        
        # Aggregate Node Names
        nodes = [topic_ism[t].get("node_name", "Unlabeled") for t in topics]
        node_counts = Counter(nodes).most_common(6)
        
        print("\nDominant Semantic Nodes (Categories):", flush=True)
        for node, count in node_counts:
            pct = (count / len(topics)) * 100
            print(f"  * {node:<30} | Count: {count:<5} | Percentage: {pct:.1f}%", flush=True)
            
        # Aggregate Isms / Concepts
        all_isms = []
        for t in topics:
            all_isms.extend(topic_ism[t].get("isms", []))
        ism_counts = Counter(all_isms).most_common(8)
        
        print("\nDominant Isms / Sub-Categories:", flush=True)
        for ism, count in ism_counts:
            pct = (count / len(all_isms)) * 100
            print(f"  * {ism:<30} | Count: {count:<5} | Percentage: {pct:.1f}%", flush=True)
        print("\n", flush=True)

if __name__ == "__main__":
    main()
