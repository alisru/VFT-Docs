import os
import json
import sys
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
    QDRANT_URL = "https://182bf3c8-faf1-428e-a670-9fb5e705769f.australia-southeast1-0.gcp.cloud.qdrant.io"
    QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YjAwZDY4MjctNjZhZS00ZjQ2LWEwMDItMmNjODQzZTNhZTkyIn0.ZAQZ69ZNkSnX1pp_SAmU5_XSHEGqQsCmxEmjCALdJXs"
    COLLECTION_NAME = "vft_paragraphs"
    
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    query = "worldview math matrices proven unproven knowledge saddle shape hyperbolic paraboloid boxes spacetime entropy Answer Idea Resistance equilibrium"
    print(f"Querying Qdrant Cloud for: '{query}'...", flush=True)
    
    query_vector = model.encode(query).tolist()
    
    search_result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=45,
        with_payload=True
    )
    
    for idx, p in enumerate(search_result.points):
        print(f"\nResult #{idx+1} (Score: {p.score:.4f}):")
        print(f"File: {p.payload['file']} (Para: {p.payload['paragraph_index']})")
        print(p.payload['text'][:200] + "...")

if __name__ == "__main__":
    main()
