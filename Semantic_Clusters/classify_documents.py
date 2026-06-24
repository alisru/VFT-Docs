import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# 16-point Hegemony Map definitions with their 32 Philosophical Isms and descriptions
HEGEMONY_POINTS = {
    "gg-gg": {
        "quadrant": "GG",
        "quadrant_name": "Greater Good",
        "sub_vector": "gg-gg",
        "node_name": "Reality / History",
        "isms": ["Realism", "Historicism"],
        "description": "Reality, History, Realism, Historicism. Focuses on objective reality, historical development, objective truth, facts, historical trajectory, and structural evolution."
    },
    "gg-le": {
        "quadrant": "GG",
        "quadrant_name": "Greater Good",
        "sub_vector": "gg-le",
        "node_name": "Language / Psychology",
        "isms": ["Relationalism", "Understanding"],
        "description": "Language, Psychology, Relationalism, Understanding. Focuses on communication, intersubjective understanding, relational meaning, semantic shared structures, and human psychology in alignment with truth."
    },
    "gg-ge": {
        "quadrant": "GG",
        "quadrant_name": "Greater Good",
        "sub_vector": "gg-ge",
        "node_name": "Sociology / Society",
        "isms": ["Collectivism", "Communitarianism"],
        "description": "Sociology, Society, Collectivism, Communitarianism. Focuses on empathy, community, social cohesion, collective systems, mutual care, social justice, and fair societal structures."
    },
    "gg-lg": {
        "quadrant": "GG",
        "quadrant_name": "Greater Good",
        "sub_vector": "gg-lg",
        "node_name": "Internal Judgment / Religion",
        "isms": ["Prudence", "Charity"],
        "description": "Internal Judgment, Religion, Prudence, Charity. Focuses on wisdom, careful judgment, charitable works, ethical action, benevolence, moral law, and selfless love."
    },
    "lg-gg": {
        "quadrant": "LG",
        "quadrant_name": "Lesser Good",
        "sub_vector": "lg-gg",
        "node_name": "Learning / Emotional-physics",
        "isms": ["Empiricism", "Stoicism"],
        "description": "Learning, Emotional-physics, Empiricism, Stoicism. Focuses on learning, temperance, emotional resilience, empirical observation, sensory evidence, scientific method, and inner peace."
    },
    "lg-le": {
        "quadrant": "LG",
        "quadrant_name": "Lesser Good",
        "sub_vector": "lg-le",
        "node_name": "Meta-Physics / Physics",
        "isms": ["Imagination", "Objectivity"],
        "description": "Meta-Physics, Physics, Imagination, Objectivity. Focuses on the relationship between abstract ideas and physical laws, creative imagination, physical reality, and scientific objectivity."
    },
    "lg-ge": {
        "quadrant": "LG",
        "quadrant_name": "Lesser Good",
        "sub_vector": "lg-ge",
        "node_name": "Spirituality / Maths",
        "isms": ["Faith", "Order"],
        "description": "Spirituality, Maths, Faith, Order. Focuses on spiritual connection, divine mathematical order, structural symmetry, cosmic faith, harmony, and transcendental patterns."
    },
    "lg-lg": {
        "quadrant": "LG",
        "quadrant_name": "Lesser Good",
        "sub_vector": "lg-lg",
        "node_name": "Intelligence / Religion",
        "isms": ["Hope", "Charity"],
        "description": "Intelligence, Religion, Hope, Charity. Focuses on hopeful intelligence, spiritual aspiration, divine charity, ultimate hope, benevolence, and internal spiritual growth."
    },
    "le-gg": {
        "quadrant": "LE",
        "quadrant_name": "Lesser Evil",
        "sub_vector": "le-gg",
        "node_name": "Maths / Spirituality",
        "isms": ["Chaos", "Nihilism"],
        "description": "Maths, Spirituality, Chaos, Nihilism. Focuses on mathematical chaos, active rejection of meaning, nihilistic worldview, cosmic pointlessness, randomness, and destruction of order."
    },
    "le-le": {
        "quadrant": "LE",
        "quadrant_name": "Lesser Evil",
        "sub_vector": "le-le",
        "node_name": "Religion / Intelligence",
        "isms": ["Hatred", "Despair"],
        "description": "Religion, Intelligence, Hatred, Despair. Focuses on active malice, ideological hatred, despair, hopelessness, destructive intellect, and religious extremism or total cynicism."
    },
    "le-ge": {
        "quadrant": "LE",
        "quadrant_name": "Lesser Evil",
        "sub_vector": "le-ge",
        "node_name": "Emotional-physics / Learning",
        "isms": ["Indulgence", "Folly"],
        "description": "Emotional-physics, Learning, Indulgence, Folly. Focuses on lack of self-control, folly, foolishness, immediate gratification, emotional volatility, and intellectual neglect."
    },
    "le-lg": {
        "quadrant": "LE",
        "quadrant_name": "Lesser Evil",
        "sub_vector": "le-lg",
        "node_name": "Physics / Meta-Physics",
        "isms": ["Denial", "Dogma"],
        "description": "Physics, Meta-Physics, Denial, Dogma. Focuses on denial of facts, rigid dogma, closed-mindedness, ideological blindness, and rejection of empirical physical evidence."
    },
    "ge-gg": {
        "quadrant": "GE",
        "quadrant_name": "Greater Evil",
        "sub_vector": "ge-gg",
        "node_name": "Society / Sociology",
        "isms": ["Anarchy", "Apathy"],
        "description": "Society, Sociology, Anarchy, Apathy. Focuses on societal apathy, passive allowance of harm, anarchy, social collapse, systemic decay, and indifference to injustice."
    },
    "ge-le": {
        "quadrant": "GE",
        "quadrant_name": "Greater Evil",
        "sub_vector": "ge-le",
        "node_name": "Internal Judgment / The World",
        "isms": ["Corruption", "Cowardice"],
        "description": "Internal Judgment, The World, Corruption, Cowardice. Focuses on systemic corruption, personal cowardice, selling out principles, worldly compromise, and ethical failure."
    },
    "ge-ge": {
        "quadrant": "GE",
        "quadrant_name": "Greater Evil",
        "sub_vector": "ge-ge",
        "node_name": "History / Reality",
        "isms": ["Erasure", "Delusion"],
        "description": "History, Reality, Erasure, Delusion. Focuses on historical erasure, self-delusion, complete denial of reality, historical revisionism, propaganda, and destruction of historical records."
    },
    "ge-lg": {
        "quadrant": "GE",
        "quadrant_name": "Greater Evil",
        "sub_vector": "ge-lg",
        "node_name": "Psychology / Language",
        "isms": ["Confusion", "Deceit"],
        "description": "Psychology, Language, Confusion, Deceit. Focuses on deliberate deceit, manipulation, mental confusion, distortion of communication, lying, and psychological gaslighting."
    }
}

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mapping_path = os.path.join(script_dir, "cluster_mapping.json")
    output_path = os.path.join(script_dir, "doc_ism_mapping.json")

    print(f"Loading {mapping_path}...")
    with open(mapping_path, 'r', encoding='utf-8') as f:
        paragraphs = json.load(f)

    # Group paragraphs by file
    doc_paras = {}
    for p in paragraphs:
        file_path = p.get("file", "")
        if not file_path:
            continue
        doc_name = os.path.basename(file_path)
        if doc_name not in doc_paras:
            doc_paras[doc_name] = []
        doc_paras[doc_name].append(p)

    print(f"Grouped into {len(doc_paras)} documents.")

    # Initialize SentenceTransformer
    print("Loading SentenceTransformer ('all-MiniLM-L6-v2')...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Embed the 16 Hegemony Point descriptions
    point_keys = list(HEGEMONY_POINTS.keys())
    point_texts = [
        f"{HEGEMONY_POINTS[k]['quadrant_name']} ({HEGEMONY_POINTS[k]['quadrant']}) - "
        f"{HEGEMONY_POINTS[k]['node_name']} ({HEGEMONY_POINTS[k]['sub_vector']}). "
        f"Philosophical Isms: {' & '.join(HEGEMONY_POINTS[k]['isms'])}. "
        f"Details: {HEGEMONY_POINTS[k]['description']}"
        for k in point_keys
    ]
    print("Embedding Hegemony Point descriptions...")
    point_embeddings = model.encode(point_texts, show_progress_bar=False)

    doc_mappings = {}
    doc_names = list(doc_paras.keys())
    
    # Process documents
    print("Embedding and classifying documents...")
    # Prepare text for each document: filename + content of first 3 paragraphs
    doc_texts = []
    for doc in doc_names:
        paras = sorted(doc_paras[doc], key=lambda x: x.get("paragraph_index", 0))
        sample_text = " ".join([p.get("text", "") for p in paras[:3]])
        # Combine clean file title with text content
        clean_title = doc.replace(".md", "").replace("_", " ").replace("-", " ")
        combined_text = f"Title: {clean_title}. Content: {sample_text}"
        doc_texts.append(combined_text)

    # Batch encode document representations
    doc_embeddings = model.encode(doc_texts, show_progress_bar=True)

    # Compute similarity and classify
    for idx, doc in enumerate(doc_names):
        doc_emb = doc_embeddings[idx]
        
        # Calculate cosine similarities
        similarities = []
        for p_emb in point_embeddings:
            cos_sim = np.dot(doc_emb, p_emb) / (np.linalg.norm(doc_emb) * np.linalg.norm(p_emb))
            similarities.append(float(cos_sim))

        best_idx = np.argmax(similarities)
        best_point_key = point_keys[best_idx]
        best_point = HEGEMONY_POINTS[best_point_key]

        doc_mappings[doc] = {
            "assigned_point": best_point_key,
            "quadrant": best_point["quadrant"],
            "quadrant_name": best_point["quadrant_name"],
            "sub_vector": best_point["sub_vector"],
            "node_name": best_point["node_name"],
            "isms": best_point["isms"],
            "similarity": similarities[best_idx],
            "all_scores": {point_keys[i]: similarities[i] for i in range(len(point_keys))}
        }

    # Save mapping to json
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(doc_mappings, f, indent=2)
    print(f"Successfully classified all documents and saved to {output_path}")

if __name__ == "__main__":
    main()
