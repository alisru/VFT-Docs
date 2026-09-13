"""
find_semantic_voids.py
The Python Scout:
1. Loads all existing AEC Invariant Forms and encodes them into 384-d vectors.
2. Ingests a broad, diverse batch of foundational English verbs from WordNet.
3. Computes the maximum gravitational pull (cosine similarity) of each word against all AEC forms.
4. Identifies ORPHANS (words falling into gravitational voids with low affinity to all existing forms).
5. Clusters the orphans using Agglomerative Clustering to find the top semantic voids (the missing AEC basins).
"""

import json
import os
import numpy as np
from nltk.corpus import wordnet as wn
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering

V2_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(V2_DIR, "aec_dictionary.json")

def load_aec_forms():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["aec_forms"]

def sample_wordnet_verbs(num_verbs=250):
    """Harvest diverse foundational verbs from WordNet."""
    verbs = {}
    
    # Target high-yield synset domains
    target_domains = [
        "change.v.01", "motion.n.03", "perception.n.01", "cognition.n.01",
        "communication.n.02", "contact.n.01", "creation.n.02", "emotion.n.01",
        "stative.a.01", "consumption.n.01", "competition.n.01", "social.a.01"
    ]

    all_verb_synsets = list(wn.all_synsets(pos=wn.VERB))
    # Sample evenly across the corpus
    step = max(1, len(all_verb_synsets) // num_verbs)
    sampled = all_verb_synsets[::step][:num_verbs]

    for s in sampled:
        lemma = s.lemma_names()[0].lower().replace("_", " ")
        if len(lemma) > 2 and lemma.isalpha() and lemma not in verbs:
            defn = s.definition()
            verbs[lemma] = defn

    print(f"[SCOUT] Harvested {len(verbs)} diverse candidate verbs from WordNet.")
    return verbs

def scan_for_voids(min_orphan_dist=0.36, top_k_clusters=3):
    print("Loading embedding model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    aec_forms = load_aec_forms()
    form_keys = list(aec_forms.keys())
    form_ids = [f["form_id"] for f in aec_forms.values()]
    form_labels = [f["descriptive_words"]["primary_label"] for f in aec_forms.values()]

    # Encode AEC forms
    aec_texts = []
    for f in aec_forms.values():
        act = " ".join(f["invariant_triad"]["action"])
        strn = " ".join(f["invariant_triad"]["strain"])
        eff = " ".join(f["invariant_triad"]["effect"])
        proc = f.get("definitive_process", "")
        topo = f"Level {f.get('topology', {}).get('closure_level', 0)} {f.get('topology', {}).get('boundary_type', '')}"
        aec_texts.append(f"{act}. Resisting {strn}. Resolving to {eff}. {proc}. {topo}")

    print(f"Encoding {len(aec_texts)} existing AEC Attractor Wells...")
    aec_embeddings = model.encode(aec_texts, normalize_embeddings=True, show_progress_bar=False)

    # Harvest candidate words
    candidate_words = sample_wordnet_verbs(300)
    word_list = list(candidate_words.keys())
    word_texts = [f"{w}: {candidate_words[w]}" for w in word_list]

    print(f"Projecting {len(word_texts)} candidate words into semantic vector field...")
    word_embeddings = model.encode(word_texts, normalize_embeddings=True, show_progress_bar=False)

    # Compute similarity matrix: (num_words, num_aec)
    sim_matrix = np.dot(word_embeddings, aec_embeddings.T)
    max_sims = np.max(sim_matrix, axis=1)

    # Filter orphans: words falling into gravitational voids
    orphan_indices = np.where(max_sims < min_orphan_dist)[0]
    print(f"\n[SCOUT RESULTS] Out of {len(word_list)} candidate verbs:")
    print(f"  - Captured by existing AEC basins: {len(word_list) - len(orphan_indices)} words")
    print(f"  - Orphans falling into Gravitational Voids: {len(orphan_indices)} words")

    if len(orphan_indices) < 5:
        print("Very few orphans found at this threshold. Adjusting threshold upward...")
        orphan_indices = np.where(max_sims < 0.40)[0]

    orphan_embeddings = word_embeddings[orphan_indices]
    orphan_words = [word_list[i] for i in orphan_indices]
    orphan_sims = max_sims[orphan_indices]

    # Cluster the orphans to find the epicenters of the missing AEC basins
    clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=0.58, metric="cosine", linkage="average")
    cluster_labels = clustering.fit_predict(orphan_embeddings)

    clusters = {}
    for idx, c_id in enumerate(cluster_labels):
        if c_id not in clusters:
            clusters[c_id] = []
        clusters[c_id].append({
            "word": orphan_words[idx],
            "definition": candidate_words[orphan_words[idx]],
            "max_existing_pull": float(orphan_sims[idx])
        })

    # Sort clusters by size (largest semantic voids first)
    sorted_clusters = sorted([c for c in clusters.values() if len(c) >= 3], key=lambda c: len(c), reverse=True)

    results = {
        "total_scanned": len(word_list),
        "total_orphans": len(orphan_indices),
        "total_void_families": len(sorted_clusters),
        "top_voids": sorted_clusters[:top_k_clusters]
    }

    output_path = os.path.join(V2_DIR, "scouted_semantic_voids.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] Scouted semantic voids saved to {output_path}\n")

    # Print summary to stdout
    for i, void in enumerate(sorted_clusters[:top_k_clusters]):
        print(f"============================================================")
        print(f"SEMANTIC VOID #{i+1} (Missing Invariant Basin with {len(void)} words):")
        print(f"Words: {', '.join([item['word'] for item in void])}")
        print("Sample Definitions:")
        for item in void[:3]:
            print(f"  - {item['word']}: {item['definition']} (Max AEC Pull: {item['max_existing_pull']:.3f})")
        print("============================================================\n")

if __name__ == "__main__":
    scan_for_voids()
