"""
aec_vector_field.py
Vectorizes all AEC Invariant Forms into a 384-dimensional semantic manifold.
Treats each AEC Form as a "Gravitational Attractor Well".
Tests incoming words to determine which attractor basin they fall into,
or detects gravitational voids indicating undiscovered AEC Forms.
"""

import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

V2_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(V2_DIR, "aec_dictionary.json")

def load_data():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def build_vector_field():
    print("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    data = load_data()
    aec_forms = data["aec_forms"]

    form_keys = []
    form_ids = []
    form_labels = []
    form_texts = []

    for key, form in aec_forms.items():
        form_keys.append(key)
        form_ids.append(form["form_id"])
        prim = form["descriptive_words"]["primary_label"]
        form_labels.append(prim)

        # Construct the rich invariant signal text
        action_str = " ".join(form["invariant_triad"]["action"])
        strain_str = " ".join(form["invariant_triad"]["strain"])
        effect_str = " ".join(form["invariant_triad"]["effect"])
        process_str = form.get("definitive_process", "")
        topo = f"Level {form.get('topology', {}).get('closure_level', 0)} {form.get('topology', {}).get('boundary_type', '')}"

        signal_text = f"Action: {action_str}. Overcomes strain: {strain_str}. Resolves to: {effect_str}. Process: {process_str}. Topology: {topo}."
        form_texts.append(signal_text)

    print(f"Vectorizing {len(form_texts)} AEC Invariant Forms...")
    embeddings = model.encode(form_texts, normalize_embeddings=True, show_progress_bar=False)
    print(f"[SUCCESS] Vector field created! Shape: {embeddings.shape}")

    return model, form_keys, form_ids, form_labels, embeddings

def test_attractor_gravity(model, form_keys, form_ids, form_labels, embeddings, test_words):
    print("\n=== TESTING GRAVITATIONAL ATTRACTION OF CANDIDATE WORDS ===")
    
    test_texts = [f"{word}: {desc}" for word, desc in test_words.items()]
    word_embeddings = model.encode(test_texts, normalize_embeddings=True, show_progress_bar=False)

    # Compute cosine similarity matrix: (num_words, num_forms)
    sim_matrix = np.dot(word_embeddings, embeddings.T)

    for i, (word, desc) in enumerate(test_words.items()):
        sims = sim_matrix[i]
        top_idx = np.argsort(sims)[::-1][:3]
        
        best_idx = top_idx[0]
        best_score = sims[best_idx]
        best_id = form_ids[best_idx]
        best_label = form_labels[best_idx]
        best_key = form_keys[best_idx]

        print(f"\nTarget Word: '{word.upper()}' ({desc})")
        print(f"  --> Captured by Attractor: {best_id} [{best_label.upper()}] (Pull Gravity: {best_score:.3f})")
        print(f"      Invariant Process: {best_key[:65]}...")
        print(f"  --> 2nd Closest: {form_ids[top_idx[1]]} [{form_labels[top_idx[1]]}] ({sims[top_idx[1]]:.3f}) | 3rd: {form_ids[top_idx[2]]} [{form_labels[top_idx[2]]}] ({sims[top_idx[2]]:.3f})")

if __name__ == "__main__":
    model, form_keys, form_ids, form_labels, embeddings = build_vector_field()

    # Test candidate words with diverse physical/topological mechanics
    test_cases = {
        "dungeon": "an underground prison cell used to confine captives",
        "crib": "a small enclosed bed with high barred sides to safely hold an infant",
        "sieve": "a utensil with a mesh bottom used to separate coarse particles from liquid or powder",
        "vault": "a secure reinforced room used to store valuables and money against theft",
        "drain": "a channel, pipe, or aperture through which liquid is evacuated or emptied",
        "stroll": "to move and walk slowly in a relaxed, unhurried manner along an open path",
        "barter": "to exchange goods or property for other goods without using money",
        "tether": "a rope or chain with which an animal or vessel is tied to restrict movement"
    }

    test_attractor_gravity(model, form_keys, form_ids, form_labels, embeddings, test_cases)
