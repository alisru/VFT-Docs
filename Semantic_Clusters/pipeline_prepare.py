import os
import json
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from sklearn.metrics.pairwise import cosine_similarity

def classify_layer(text):
    text_lower = text.lower()
    
    # 1. Example Heuristics
    example_indicators = ["for example", "for instance", "such as", "case study", "e.g.", "specifically", "illustration", "case p", "case n", "taylor", "hanson", "dutton", "medicare"]
    if any(ind in text_lower for ind in example_indicators):
        return "EXAMPLE"
        
    # 2. Definition Heuristics
    def_indicators = ["is defined as", "refers to", "denotes", "is the", "derived from", "means", "constitutes", "concept of", "axiom of", "hegemonikon is", "psochic hegemony is"]
    if any(ind in text_lower for ind in def_indicators):
        return "DEFINITION"
        
    # 3. Conditional Heuristics
    cond_indicators = ["if ", "when ", "unless", "depends on", "conditional", "where ", "threshold", "limit", "requires"]
    if any(ind in text_lower for ind in cond_indicators):
        return "CONDITIONAL"
        
    # 4. Fallback to Assertion
    return "ASSERTION"

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_json_path = os.path.join(script_dir, "staged_fragments.json")
    
    QDRANT_URL = "https://182bf3c8-faf1-428e-a670-9fb5e705769f.australia-southeast1-0.gcp.cloud.qdrant.io"
    QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YjAwZDY4MjctNjZhZS00ZjQ2LWEwMDItMmNjODQzZTNhZTkyIn0.ZAQZ69ZNkSnX1pp_SAmU5_XSHEGqQsCmxEmjCALdJXs"
    COLLECTION_NAME = "vft_paragraphs"
    
    print(f"Connecting to Qdrant Cloud at {QDRANT_URL}...", flush=True)
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    print("Loading SentenceTransformer ('all-MiniLM-L6-v2')...", flush=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Define our four distinct document targets
    doc_definitions = [
        {
            "id": "hegemonikon_philosophy",
            "title": "Stoic Hegemonikon & Foundations",
            "type": "concept",
            "query": "Hegemonikon Stoic ruling principle of the mind phronesis logos Epictetus nameless structure of meaning soul rational controller"
        },
        {
            "id": "worldview_construction_math",
            "title": "Worldview Construction & Physics of Ideas",
            "type": "axiom",
            "query": "worldview math matrices proven unproven knowledge saddle shape hyperbolic paraboloid boxes spacetime entropy Answer Idea Resistance equilibrium"
        },
        {
            "id": "quadrant_attractors",
            "title": "Four Quadrants & 16 Point Attractors",
            "type": "concept",
            "query": "Greater Good GG Lesser Good LG Lesser Evil LE Greater Evil GE attractors gravity wells coordinate alignments isms"
        },
        {
            "id": "auditing_helixis_tensor",
            "title": "Ontological Auditing & Helixis Tensor",
            "type": "concept",
            "query": "7-vector audit rNet delta H hypocrisy gap Helixis Tensor Bait Cover True Intent Grace Fall Delusion Redemption"
        }
    ]
    
    staged_data = {}
    
    for doc in doc_definitions:
        doc_id = doc["id"]
        print(f"\nQuerying fragments for document: '{doc['title']}'...", flush=True)
        
        query_vector = model.encode(doc["query"]).tolist()
        
        search_result = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=40,
            with_payload=True,
            with_vectors=True
        )
        
        points = search_result.points
        if not points:
            print(f"No points returned for {doc_id}", flush=True)
            continue
            
        print(f"Retrieved {len(points)} raw paragraphs.", flush=True)
        
        # De-duplicate using cosine similarity threshold 0.82
        vectors = np.array([p.vector for p in points])
        sim_matrix = cosine_similarity(vectors)
        
        kept_indices = []
        for i in range(len(points)):
            is_duplicate = False
            for j in kept_indices:
                if sim_matrix[i][j] >= 0.82:
                    is_duplicate = True
                    break
            if not is_duplicate:
                kept_indices.append(i)
                
        unique_points = [points[idx] for idx in kept_indices]
        print(f"Kept {len(unique_points)} unique paragraphs (discarded {len(points) - len(kept_indices)} duplicates).", flush=True)
        
        # Categorize by layer
        layered_fragments = {
            "DEFINITION": [],
            "ASSERTION": [],
            "CONDITIONAL": [],
            "EXAMPLE": []
        }
        
        for p in unique_points:
            text = p.payload["text"]
            file_path = p.payload["file"]
            para_idx = p.payload["paragraph_index"]
            
            layer = classify_layer(text)
            layered_fragments[layer].append({
                "text": text,
                "file": file_path,
                "paragraph_index": para_idx
            })
            
        print(f"Layer distribution: DEF={len(layered_fragments['DEFINITION'])}, ASSERT={len(layered_fragments['ASSERTION'])}, COND={len(layered_fragments['CONDITIONAL'])}, EX={len(layered_fragments['EXAMPLE'])}", flush=True)
        
        staged_data[doc_id] = {
            "title": doc["title"],
            "type": doc["type"],
            "query": doc["query"],
            "layers": layered_fragments
        }
        
    print(f"\nWriting staged fragments to {output_json_path}...", flush=True)
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(staged_data, f, indent=4, ensure_ascii=False)
        
    print("Done! staged_fragments.json is ready for the reconstruction pass.", flush=True)

if __name__ == "__main__":
    main()
