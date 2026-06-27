import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

# 16 Hegemony points definitions
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
    output_path = os.path.join(script_dir, "topic_ism_mapping.json")

    print(f"Loading {mapping_path}...")
    with open(mapping_path, 'r', encoding='utf-8') as f:
        paragraphs = json.load(f)

    # Group paragraphs by Topic ID to extract consolidated keywords
    topic_paras = {}
    for p in paragraphs:
        tid = p.get("topic_id", -1)
        if tid == -1:
            continue
        if tid not in topic_paras:
            topic_paras[tid] = []
        topic_paras[tid].append(p)

    print(f"Found {len(topic_paras)} semantic topics.")

    # Consolidate keywords for each topic
    stop_words = {'with', 'this', 'that', 'from', 'they', 'have', 'were', 'about', 'their', 'which', 'there', 'what'}
    topic_keywords = {}
    for tid, paras in topic_paras.items():
        word_counts = {}
        for p in paras:
            words = p.get("text", "").lower().split()
            # simple alphanumeric cleanup
            for w in words:
                cleaned = "".join([c for c in w if c.isalpha()])
                if len(cleaned) >= 4 and cleaned not in stop_words:
                    word_counts[cleaned] = word_counts.get(cleaned, 0) + 1
        
        # Take top 15 words as semantic fingerprint
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:15]
        topic_keywords[tid] = [w[0] for w in sorted_words]

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

    # Embed the Topic Keyword signatures
    tids = sorted(list(topic_keywords.keys()))
    topic_signatures = [
        f"Topic keywords: {', '.join(topic_keywords[tid])}"
        for tid in tids
    ]
    print("Embedding semantic Topic keyword signatures...")
    topic_embeddings = model.encode(topic_signatures, show_progress_bar=True)

    # Classify Topics
    topic_mappings = {}
    for idx, tid in enumerate(tids):
        topic_emb = topic_embeddings[idx]
        
        similarities = []
        for p_emb in point_embeddings:
            cos_sim = np.dot(topic_emb, p_emb) / (np.linalg.norm(topic_emb) * np.linalg.norm(p_emb))
            similarities.append(float(cos_sim))

        best_idx = np.argmax(similarities)
        best_point_key = point_keys[best_idx]
        best_point = HEGEMONY_POINTS[best_point_key]

        topic_mappings[str(tid)] = {
            "assigned_point": best_point_key,
            "quadrant": best_point["quadrant"],
            "quadrant_name": best_point["quadrant_name"],
            "sub_vector": best_point["sub_vector"],
            "node_name": best_point["node_name"],
            "isms": best_point["isms"],
            "similarity": similarities[best_idx],
            "keywords": topic_keywords[tid]
        }

    # Save Topic mapping to json
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(topic_mappings, f, indent=2)
    print(f"Successfully classified all topics and saved to {output_path}")

if __name__ == "__main__":
    main()
