import os
import json
import sys
import subprocess
import numpy as np
from sentence_transformers import SentenceTransformer
import umap
import hdbscan

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    md_folder = os.path.join(workspace_root, "_VFT MD")
    output_path = os.path.join(script_dir, "cluster_mapping.json")

    # Force stdout encoding to UTF-8
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')

    if not os.path.exists(md_folder):
        print(f"Error: _VFT MD folder not found at: {md_folder}", flush=True)
        return

    print(f"Scanning markdown files in: {md_folder}", flush=True)
    paragraph_records = []
    file_count = 0

    for root, dirs, files in os.walk(md_folder):
        for file in files:
            if file.endswith('.md') and not file.startswith('index_'):
                file_count += 1
                full_path = os.path.join(root, file)
                
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Chunk to Paragraphs
                paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 15]
                
                for p_idx, p_text in enumerate(paragraphs):
                    paragraph_records.append({
                        "text": p_text,
                        "file": full_path,
                        "paragraph_index": p_idx,
                        "topic_id": -1
                    })

    total_paragraphs = len(paragraph_records)
    print(f"Parsed {file_count} documents. Found {total_paragraphs} paragraphs.", flush=True)
    
    if total_paragraphs == 0:
        print("No paragraphs found to cluster.", flush=True)
        return

    print("Loading SentenceTransformer model...", flush=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')

    print("Generating paragraph embeddings (this may take 1-2 minutes on GPU)...", flush=True)
    texts = [p["text"] for p in paragraph_records]
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=256)

    print("Running UMAP dimensionality reduction (converting 384 dims -> 5 dims for HDBSCAN)...", flush=True)
    # n_neighbors=15, n_components=5, metric='cosine', random_state=42
    reducer = umap.UMAP(
        n_neighbors=15, 
        n_components=5, 
        metric='cosine', 
        random_state=42,
        low_memory=True
    )
    embeddings_reduced = reducer.fit_transform(embeddings)
    print("UMAP reduction complete.", flush=True)

    print("Running HDBSCAN clustering (min_cluster_size=15, min_samples=5)...", flush=True)
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=15, 
        min_samples=5, 
        metric='euclidean', 
        cluster_selection_method='eom'
    )
    labels = clusterer.fit_predict(embeddings_reduced)
    print("HDBSCAN clustering complete.", flush=True)

    # Assign labels back
    unique_labels = set(labels)
    num_clusters = len([l for l in unique_labels if l != -1])
    noise_count = len([l for l in labels if l == -1])
    print(f"Identified {num_clusters} semantic topics. Noise paragraphs: {noise_count} ({noise_count/total_paragraphs*100:.1f}%)", flush=True)

    for i in range(total_paragraphs):
        paragraph_records[i]["topic_id"] = int(labels[i])

    print(f"Writing cluster mappings to: {output_path}", flush=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(paragraph_records, f, indent=2, ensure_ascii=False)

    print("Successfully mapped all paragraphs to topics.", flush=True)

    # Now run classify_documents.py to regenerate topic_ism_mapping.json
    classify_script = os.path.join(script_dir, "classify_documents.py")
    if os.path.exists(classify_script):
        print("Running classify_documents.py to regenerate topic attractor mappings...", flush=True)
        try:
            subprocess.run(["python", classify_script], check=True, cwd=script_dir)
            print("Successfully regenerated topic_ism_mapping.json.", flush=True)
        except Exception as e:
            print(f"Error running classify_documents.py: {e}", flush=True)
    else:
        print("Warning: classify_documents.py not found, skipping topic attraction categorization.", flush=True)

if __name__ == "__main__":
    main()
