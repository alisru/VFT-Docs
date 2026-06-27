import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cluster_mapping_path = os.path.join(script_dir, "cluster_mapping.json")
    topic_ism_path = os.path.join(script_dir, "topic_ism_mapping.json")
    
    QDRANT_URL = "https://182bf3c8-faf1-428e-a670-9fb5e705769f.australia-southeast1-0.gcp.cloud.qdrant.io"
    QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YjAwZDY4MjctNjZhZS00ZjQ2LWEwMDItMmNjODQzZTNhZTkyIn0.ZAQZ69ZNkSnX1pp_SAmU5_XSHEGqQsCmxEmjCALdJXs"
    COLLECTION_NAME = "vft_paragraphs"
    
    print("Loading local semantic mappings...", flush=True)
    if not os.path.exists(cluster_mapping_path) or not os.path.exists(topic_ism_path):
        print(f"Error: Required index files missing in {script_dir}", flush=True)
        return
        
    with open(cluster_mapping_path, 'r', encoding='utf-8') as f:
        paragraphs = json.load(f)
    with open(topic_ism_path, 'r', encoding='utf-8') as f:
        topic_isms = json.load(f)
        
    print(f"Connecting to Qdrant Cloud at {QDRANT_URL}...", flush=True)
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # 1. Recreate collection (re-using 384 dims for all-MiniLM-L6-v2)
    print(f"Checking if collection '{COLLECTION_NAME}' exists...", flush=True)
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)
    
    if exists:
        print(f"Collection '{COLLECTION_NAME}' already exists. Recreating to ensure clean sync...", flush=True)
        client.delete_collection(collection_name=COLLECTION_NAME)
        
    print(f"Creating collection '{COLLECTION_NAME}' with 384-dimensional Cosine vector config...", flush=True)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )
    
    # 2. Embedding paragraphs
    print("Loading SentenceTransformer ('all-MiniLM-L6-v2')...", flush=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    texts = [p["text"] for p in paragraphs]
    print(f"Generating embeddings for {len(texts)} paragraphs...", flush=True)
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=256)
    
    # 3. Prepare upload points
    print("Preparing Qdrant points with semantic metadata payload...", flush=True)
    points = []
    for idx, p in enumerate(paragraphs):
        tid = str(p["topic_id"])
        
        # Enrich payload with Topic Hegemony coordinate details if available
        payload = {
            "text": p["text"],
            "file": p["file"],
            "paragraph_index": p["paragraph_index"],
            "topic_id": p["topic_id"],
            "assigned_point": "none",
            "quadrant": "none",
            "node_name": "none",
            "isms": []
        }
        
        if tid in topic_isms:
            t_meta = topic_isms[tid]
            payload["assigned_point"] = t_meta["assigned_point"]
            payload["quadrant"] = t_meta["quadrant"]
            payload["node_name"] = t_meta["node_name"]
            payload["isms"] = t_meta["isms"]
            
        points.append(PointStruct(
            id=idx,
            vector=embeddings[idx].tolist(),
            payload=payload
        ))
        
    # 4. Upload to Qdrant in chunks of 500
    chunk_size = 500
    total_points = len(points)
    print(f"Uploading {total_points} points in chunks of {chunk_size}...", flush=True)
    
    for i in range(0, total_points, chunk_size):
        chunk = points[i:i+chunk_size]
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=chunk
        )
        print(f"Uploaded points {i} to {min(i+chunk_size, total_points)}...", flush=True)
        
    print("Qdrant synchronization complete!", flush=True)

if __name__ == "__main__":
    main()
