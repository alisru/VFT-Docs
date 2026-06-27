import os
import json
import sys
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from sklearn.metrics.pairwise import cosine_similarity

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
    # Paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)
    output_doc_path = os.path.join(workspace_root, "_AI files and chat logs", "Compiled_Psochic_Hegemony.md")
    
    QDRANT_URL = "https://182bf3c8-faf1-428e-a670-9fb5e705769f.australia-southeast1-0.gcp.cloud.qdrant.io"
    QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6YjAwZDY4MjctNjZhZS00ZjQ2LWEwMDItMmNjODQzZTNhZTkyIn0.ZAQZ69ZNkSnX1pp_SAmU5_XSHEGqQsCmxEmjCALdJXs"
    COLLECTION_NAME = "vft_paragraphs"
    
    print(f"Connecting to Qdrant Cloud at {QDRANT_URL}...", flush=True)
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    print("Loading SentenceTransformer ('all-MiniLM-L6-v2')...", flush=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # 4 Structured sections and their respective semantic search queries
    sections = [
        {
            "title": "Section 1: Foundational Philosophy (The Hēgemonikon)",
            "query": "Hegemonikon Stoic ruling principle of the mind phronesis logos Epictetus nameless structure of meaning",
            "intro": "The Psochic Hegemony is defined as the Hēgemonikon---the ruling principle of the mind. Rooted in Stoic philosophy, it acts as the primary moral and perceptual compass through which consciousness filters and judges reality."
        },
        {
            "title": "Section 2: Worldview Construction & The Physics of Ideas",
            "query": "worldview math matrices proven unproven knowledge saddle shape hyperbolic paraboloid boxes spacetime entropy Answer Idea Resistance",
            "intro": "Worldviews are constructed through the mathematical interaction of two independent matrices: Proven Knowledge vs. Unproven Knowledge. This section details how consciousness, an anti-entropic ordering force, structures reality, and how the mind calculates truth and lies based on conceptual resistance."
        },
        {
            "title": "Section 3: The Four Macro Quadrants & 16 Point Attractors",
            "query": "Greater Good GG Lesser Good LG Lesser Evil LE Greater Evil GE attractors gravity wells",
            "intro": "The landscape of the Psochic Hegemony is divided into four main quadrants, hosting 16 distinct point attractors. These coordinate wells represent stable philosophical positions and orientations of the mind."
        },
        {
            "title": "Section 4: Ontological Auditing & The Helixis Tensor",
            "query": "7-vector audit rNet delta H hypocrisy gap Helixis Tensor Bait Cover True Intent Grace Fall Delusion Redemption",
            "intro": "To evaluate the integrity of worldviews and detect deceptive 'fake maximizers,' the framework employs rigorous auditing metrics (rNet, Delta H, 7-Vector Audit) and deconstructs narrative structures using the Helixis Tensor."
        }
    ]
    
    compiled_data = {}
    
    for sec in sections:
        title = sec["title"]
        query = sec["query"]
        print(f"\nRunning semantic query for '{title}'...", flush=True)
        
        # Encode query
        query_vector = model.encode(query).tolist()
        
        # Retrieve points
        search_result = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=45,
            with_payload=True,
            with_vectors=True
        )
        
        points = search_result.points
        print(f"Retrieved {len(points)} matching paragraph nodes from Qdrant.", flush=True)
        
        if not points:
            continue
            
        # De-duplicate locally using cosine similarity
        texts = [p.payload["text"] for p in points]
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
                
        print(f"Kept {len(kept_indices)} unique paragraphs (discarded {len(points) - len(kept_indices)} duplicates).", flush=True)
        
        compiled_data[title] = {
            "intro": sec["intro"],
            "paragraphs": [points[idx].payload for idx in kept_indices]
        }
        
    # Write compiled treatise
    print(f"\nWriting final compiled treatise to {output_doc_path}...", flush=True)
    with open(output_doc_path, 'w', encoding='utf-8') as f:
        f.write("# Compiled Treatise: The Psochic Hegemony & The Hēgemonikon\n\n")
        f.write("This document is a synthesized, de-duplicated compilation of the core conceptual frameworks, audits, and theoretical foundations of the **Psochic Hegemony (The Ruling Principle of the Mind)**, extracted semantically from the VFT vector repository using Qdrant Cloud.\n\n")
        f.write("---\n\n")
        
        for title, content in compiled_data.items():
            f.write(f"## {title}\n\n")
            f.write(f"*{content['intro']}*\n\n")
            
            for p in content["paragraphs"]:
                text = p["text"].strip()
                # Clean path
                raw_path = p["file"]
                # Convert backslash to forward slash for clean visual paths
                clean_path = raw_path.replace('\\', '/')
                src_file = os.path.basename(raw_path)
                
                f.write(f"{text}\n\n*Source: [{src_file}](file:///{clean_path})*\n\n---\n\n")
                
    print("Compilation complete!", flush=True)

if __name__ == "__main__":
    main()
