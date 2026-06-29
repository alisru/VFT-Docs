import os
import json
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sklearn.metrics.pairwise import cosine_similarity

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    QDRANT_URL = "https://182bf3c8-faf1-428e-a670-9fb5e705769f.australia-southeast1-0.gcp.cloud.qdrant.io"
    QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YjAwZDY4MjctNjZhZS00ZjQ2LWEwMDItMmNjODQzZTNhZTkyIn0.ZAQZ69ZNkSnX1pp_SAmU5_XSHEGqQsCmxEmjCALdJXs"
    COLLECTION_NAME = "vft_paragraphs"
    
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Let's query by file name filter
    print("Searching for paragraphs from 'proofs of QI.md' in Qdrant...", flush=True)
    
    # We will scroll points matching the filename proofs of QI.md
    res = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="file",
                    match=MatchValue(value="E:\\Vector Field Theory\\VFT Docs\\_VFT MD\\Actualism\\42\\proofs of QI.md")
                )
            ]
        ),
        limit=100,
        with_payload=True,
        with_vectors=True
    )
    
    points = res[0]
    print(f"Found {len(points)} paragraphs stored for 'proofs of QI.md'.", flush=True)
    
    target_query = "worldview math matrices proven unproven knowledge saddle shape hyperbolic paraboloid boxes spacetime entropy Answer Idea Resistance equilibrium"
    q_vec = model.encode(target_query).reshape(1, -1)
    
    for p in points:
        text = p.payload["text"]
        p_idx = p.payload["paragraph_index"]
        
        # Calculate cosine similarity manually
        p_vec = np.array(p.vector).reshape(1, -1)
        sim = cosine_similarity(p_vec, q_vec)[0][0]
        
        if "perfect self-awareness" in text:
            print(f"\n--- TARGET PARAGRAPH FOUND (Index: {p_idx}, Qdrant ID: {p.id}) ---")
            print(f"Text Snippet: '{text[:120]}...'")
            print(f"Cosine Similarity score against preprocessor query: {sim:.4f}")
            
if __name__ == "__main__":
    main()
