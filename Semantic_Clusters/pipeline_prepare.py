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
        
    # 2. Definition Heuristics (Calibrated to VFT glossary/domain terms)
    def_indicators = ["υ axis", "psi axis", "upsilon", "psi", "hēgemonikon", "psochic hegemony", "logos", "phronesis", "attractor", "is defined as", "refers to", "denotes", "is the", "derived from", "means", "constitutes", "concept of"]
    if any(ind in text_lower for ind in def_indicators):
        return "DEFINITION"
        
    # 3. Conditional Heuristics (Calibrated to logic/auditing parameters)
    cond_indicators = ["if ", "when ", "unless", "threshold", "limit", "gap", "dissonance", "rnet", "delta h", "hypocrisy gap", "depends on", "conditional", "where ", "requires"]
    if any(ind in text_lower for ind in cond_indicators):
        return "CONDITIONAL"
        
    # 4. Fallback to Assertion
    return "ASSERTION"

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    QDRANT_URL = "https://182bf3c8-faf1-428e-a670-9fb5e705769f.australia-southeast1-0.gcp.cloud.qdrant.io"
    QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YjAwZDY4MjctNjZhZS00ZjQ2LWEwMDItMmNjODQzZTNhZTkyIn0.ZAQZ69ZNkSnX1pp_SAmU5_XSHEGqQsCmxEmjCALdJXs"
    COLLECTION_NAME = "vft_paragraphs"
    
    print(f"Connecting to Qdrant Cloud at {QDRANT_URL}...", flush=True)
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    print("Loading SentenceTransformer ('all-MiniLM-L6-v2')...", flush=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Four target documents, each with multi-query splits to maximize semantic coverage
    doc_definitions = [
        {
            "id": "hegemonikon_philosophy",
            "title": "Stoic Hegemonikon & Foundations",
            "type": "concept",
            "queries": [
                "Hegemonikon Stoic ruling principle of the mind phronesis logos Epictetus nameless structure of meaning",
                "Epictetus dichotomy of control will psi axis management tool sovereign rational controller"
            ]
        },
        {
            "id": "worldview_construction_math",
            "title": "Worldview Construction & Physics of Ideas",
            "type": "concept",
            "queries": [
                "proven knowledge unproven knowledge matrices subtraction saddle shape hyperbolic paraboloid worldview math",
                "consciousness anti-entropic force ordering boxes spacetime negating potential entropy equilibrium"
            ]
        },
        {
            "id": "quadrant_attractors",
            "title": "Four Quadrants & 16 Point Attractors",
            "type": "concept",
            "queries": [
                "Psochic Hegemony four quadrants Greater Good Lesser Evil LG GE moral compass",
                "16 coordinate attractors gravity wells isms alignments point signatures"
            ]
        },
        {
            "id": "auditing_helixis_tensor",
            "title": "Ontological Auditing & Helixis Tensor",
            "type": "concept",
            "queries": [
                "7-vector audit rNet net reality ratio delta H hypocrisy gap social dissonance",
                "Helixis Tensor deception detection Bait Cover True Intent Grace Fall Delusion Redemption relationship"
            ]
        }
    ]
    
    # 1. Retrieve all candidates using Multi-Query merge
    all_retrieved = {}
    query_embeddings = {}
    
    for doc in doc_definitions:
        doc_id = doc["id"]
        print(f"\nQuerying fragments for document: '{doc['title']}'...", flush=True)
        
        merged_points = []
        seen_ids = set()
        
        # Save first query embedding as the primary centroid for this document topic
        primary_vector = model.encode(doc["queries"][0])
        query_embeddings[doc_id] = primary_vector
        
        for q_idx, q_str in enumerate(doc["queries"]):
            print(f"  Running sub-query {q_idx+1}: '{q_str}'", flush=True)
            q_vec = model.encode(q_str).tolist()
            
            search_result = client.query_points(
                collection_name=COLLECTION_NAME,
                query=q_vec,
                limit=35,
                with_payload=True,
                with_vectors=True
            )
            
            for p in search_result.points:
                if p.id not in seen_ids:
                    seen_ids.add(p.id)
                    merged_points.append(p)
                    
        print(f"Retrieved {len(merged_points)} raw paragraphs across sub-queries.", flush=True)
        
        # Apply 8-word noise filter
        filtered_points = []
        for p in merged_points:
            text = p.payload["text"].strip()
            word_count = len(text.split())
            if word_count >= 8:
                filtered_points.append(p)
            else:
                print(f"  Filtered noise fragment ({word_count} words): '{text[:60]}...'", flush=True)
                
        print(f"Kept {len(filtered_points)} paragraphs after noise filter.", flush=True)
        all_retrieved[doc_id] = filtered_points

    # 2. Extract Bridge Sentences (affinity >= 0.65 to BOTH query centroids simultaneously)
    print("\nRunning Bridge Sentence Extraction Pass...", flush=True)
    bridge_sentences = []
    
    unique_paras = {}
    for doc_id, points in all_retrieved.items():
        for p in points:
            text = p.payload["text"]
            if text not in unique_paras:
                unique_paras[text] = {
                    "payload": p.payload,
                    "vector": p.vector,
                    "similarities": {}
                }
                
    for text, data in unique_paras.items():
        para_vec = np.array(data["vector"]).reshape(1, -1)
        for doc_id, q_vec in query_embeddings.items():
            sim = cosine_similarity(para_vec, q_vec.reshape(1, -1))[0][0]
            data["similarities"][doc_id] = sim
            
    for text, data in unique_paras.items():
        high_affinity_docs = [doc_id for doc_id, sim in data["similarities"].items() if sim >= 0.65]
        if len(high_affinity_docs) >= 2:
            print(f"Bridge sentence detected (Affinity to {high_affinity_docs}): '{text[:60]}...'", flush=True)
            bridge_sentences.append({
                "text": text,
                "file": data["payload"]["file"],
                "paragraph_index": data["payload"]["paragraph_index"],
                "linked_clusters": high_affinity_docs,
                "similarities": {k: float(v) for k, v in data["similarities"].items()}
            })
            
    bridge_texts = {b["text"] for b in bridge_sentences}
    
    # 3. Local Deduplication at 0.92 Cosine Similarity & Write staged JSON files
    for doc in doc_definitions:
        doc_id = doc["id"]
        points = all_retrieved.get(doc_id, [])
        if not points:
            continue
            
        # Filter out bridge sentences
        points = [p for p in points if p.payload["text"] not in bridge_texts]
        
        # Deduplicate using strict 0.92 threshold
        vectors = np.array([p.vector for p in points])
        sim_matrix = cosine_similarity(vectors)
        
        kept_indices = []
        for i in range(len(points)):
            is_duplicate = False
            for j in kept_indices:
                if sim_matrix[i][j] >= 0.92:
                    is_duplicate = True
                    break
            if not is_duplicate:
                kept_indices.append(i)
                
        unique_points = [points[idx] for idx in kept_indices]
        print(f"\nDocument '{doc['title']}': Kept {len(unique_points)} unique paragraphs (discarded {len(points) - len(kept_indices)} duplicates).", flush=True)
        
        # Stratify into layers
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
            
        doc_bridges = [b for b in bridge_sentences if doc_id in b["linked_clusters"]]
        
        doc_staged = {
            "title": doc["title"],
            "type": doc["type"],
            "query": doc["queries"][0], # reference query
            "layers": layered_fragments,
            "bridges": doc_bridges
        }
        
        out_file_path = os.path.join(script_dir, f"staged_{doc_id}.json")
        print(f"Writing staged pool to {out_file_path}...", flush=True)
        with open(out_file_path, 'w', encoding='utf-8') as f:
            json.dump(doc_staged, f, indent=4, ensure_ascii=False)
            
    print("\nPreprocessing pass complete! Multi-Query staged JSON files generated.", flush=True)

if __name__ == "__main__":
    main()
