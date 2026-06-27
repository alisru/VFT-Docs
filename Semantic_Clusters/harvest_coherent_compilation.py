import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def main():
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    cluster_mapping_path = os.path.join(script_dir, "cluster_mapping.json")
    topic_ism_path = os.path.join(script_dir, "topic_ism_mapping.json")
    output_doc_path = os.path.join(workspace_root, "_AI files and chat logs", "Compiled_Psochic_Hegemony.md")
    
    print("Loading indices...", flush=True)
    if not os.path.exists(cluster_mapping_path) or not os.path.exists(topic_ism_path):
        print(f"Error: Required index files missing in {script_dir}", flush=True)
        return
        
    with open(cluster_mapping_path, 'r', encoding='utf-8') as f:
        paragraphs = json.load(f)
        
    with open(topic_ism_path, 'r', encoding='utf-8') as f:
        topic_isms = json.load(f)
        
    # Step 1: Filter paragraphs relevant to "psochic hegemony"
    print("Filtering paragraphs based on keywords and topic alignments...", flush=True)
    relevant_keywords = {"hegemony", "psochic", "morality", "will", "quadrant", "attractor", "audit", "dissonance", "hypocrisy", "aletheia"}
    filtered_paras = []
    
    for p in paragraphs:
        path_lower = p["file"].lower()
        text_lower = p["text"].lower()
        tid = str(p["topic_id"])
        
        # Check relevance
        is_relevant = "hegemony" in path_lower or "hegemony" in text_lower or "psochic" in text_lower
        if not is_relevant and tid in topic_isms:
            topic_kw = set(topic_isms[tid]["keywords"])
            if topic_kw.intersection(relevant_keywords):
                is_relevant = True
                
        if is_relevant:
            filtered_paras.append(p)
            
    print(f"Found {len(filtered_paras)} potentially relevant paragraphs.", flush=True)
    
    if not filtered_paras:
        print("No relevant paragraphs found.", flush=True)
        return
        
    # Step 2: Semantic De-duplication
    print("Encoding filtered paragraphs to compute semantic similarity vectors...", flush=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    texts = [p["text"] for p in filtered_paras]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)
    
    print("Running cosine similarity de-duplication (threshold = 0.82)...", flush=True)
    sim_matrix = cosine_similarity(embeddings)
    
    kept_indices = []
    ignored_count = 0
    
    for i in range(len(filtered_paras)):
        is_duplicate = False
        for j in kept_indices:
            if sim_matrix[i][j] >= 0.82:
                is_duplicate = True
                break
        if not is_duplicate:
            kept_indices.append(i)
        else:
            ignored_count += 1
            
    print(f"Kept {len(kept_indices)} unique paragraphs. Deduplicated/ignored: {ignored_count}", flush=True)
    
    # Step 3: Organize / Sort
    # Group paragraphs by Hegemony Point or Quadrant for logical structure
    organized = {}
    for idx in kept_indices:
        p = filtered_paras[idx]
        tid = str(p["topic_id"])
        
        # Default category
        quadrant = "General / Overview"
        node_name = "Introduction to Hegemony"
        
        if tid in topic_isms:
            quadrant = topic_isms[tid]["quadrant_name"]
            node_name = topic_isms[tid]["node_name"]
            
        if quadrant not in organized:
            organized[quadrant] = {}
        if node_name not in organized[quadrant]:
            organized[quadrant][node_name] = []
            
        organized[quadrant][node_name].append(p)
        
    # Step 4: Write compiled document
    print(f"Writing compiled document to: {output_doc_path}", flush=True)
    with open(output_doc_path, 'w', encoding='utf-8') as f:
        f.write("# Compiled Treatise: The Psochic Hegemony Framework\n\n")
        f.write("This document is a synthesized, de-duplicated compilation of the core conceptual frameworks, audits, and theoretical foundations of the **Psochic Hegemony** extracted from the VFT repository.\n\n")
        
        # Sort quadrants to have a logical order: General -> GG -> LG -> LE -> GE
        quadrant_order = ["General / Overview", "Greater Good", "Lesser Good", "Lesser Evil", "Greater Evil"]
        
        for quad in quadrant_order:
            if quad not in organized:
                continue
            f.write(f"## {quad}\n\n")
            
            for node_name, paras in organized[quad].items():
                f.write(f"### {node_name}\n\n")
                for p in paras:
                    text = p["text"].strip()
                    # Convert absolute path to relative or filename for readability
                    src_file = os.path.basename(p["file"])
                    f.write(f"{text}\n\n*Source: [{src_file}](file:///{p['file'].replace('\\', '/')})*\n\n---\n\n")
                    
    print("Compilation complete!", flush=True)

if __name__ == "__main__":
    main()
