import os
import sys
import json
import argparse
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Force stdout encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

HEGEMONY_POINTS = {
    "gg-gg": {
        "quadrant": "GG",
        "quadrant_name": "Greater Good",
        "node_name": "Reality / History",
        "isms": ["Realism", "Historicism"],
        "description": "Reality, History, Realism, Historicism. Objective reality, facts, historical trajectory, and structural evolution."
    },
    "gg-le": {
        "quadrant": "GG",
        "quadrant_name": "Greater Good",
        "node_name": "Language / Psychology",
        "isms": ["Relationalism", "Understanding"],
        "description": "Language, Psychology, Relationalism, Understanding. Communication, relational meaning, intersubjective understanding."
    },
    "gg-ge": {
        "quadrant": "GG",
        "quadrant_name": "Greater Good",
        "node_name": "Sociology / Society",
        "isms": ["Collectivism", "Communitarianism"],
        "description": "Sociology, Society, Collectivism, Communitarianism. Empathy, community, social cohesion, collective systems."
    },
    "gg-lg": {
        "quadrant": "GG",
        "quadrant_name": "Greater Good",
        "node_name": "Internal Judgment / Religion",
        "isms": ["Prudence", "Charity"],
        "description": "Internal Judgment, Religion, Prudence, Charity. Wisdom, careful judgment, benevolence, moral law, selfless love."
    },
    "lg-gg": {
        "quadrant": "LG",
        "quadrant_name": "Lesser Good",
        "node_name": "Learning / Emotional-physics",
        "isms": ["Empiricism", "Stoicism"],
        "description": "Learning, Emotional-physics, Empiricism, Stoicism. Learning, temperance, emotional resilience, empirical observation."
    },
    "lg-le": {
        "quadrant": "LG",
        "quadrant_name": "Lesser Good",
        "node_name": "Meta-Physics / Physics",
        "isms": ["Imagination", "Objectivity"],
        "description": "Meta-Physics, Physics, Imagination, Objectivity. Relationship between abstract ideas and physical laws, creative imagination."
    },
    "lg-ge": {
        "quadrant": "LG",
        "quadrant_name": "Lesser Good",
        "node_name": "Spirituality / Maths",
        "isms": ["Faith", "Order"],
        "description": "Spirituality, Maths, Faith, Order. Spiritual connection, divine mathematical order, structural symmetry."
    },
    "lg-lg": {
        "quadrant": "LG",
        "quadrant_name": "Lesser Good",
        "node_name": "Intelligence / Religion",
        "isms": ["Hope", "Charity"],
        "description": "Intelligence, Religion, Hope, Charity. Hopeful intelligence, spiritual aspiration, divine charity."
    },
    "le-gg": {
        "quadrant": "LE",
        "quadrant_name": "Lesser Evil",
        "node_name": "Maths / Spirituality",
        "isms": ["Chaos", "Nihilism"],
        "description": "Maths, Spirituality, Chaos, Nihilism. Mathematical chaos, active rejection of meaning, nihilistic worldview."
    },
    "le-le": {
        "quadrant": "LE",
        "quadrant_name": "Lesser Evil",
        "node_name": "Religion / Intelligence",
        "isms": ["Hatred", "Despair"],
        "description": "Religion, Intelligence, Hatred, Despair. Active malice, ideological hatred, despair, hopelessness."
    },
    "le-ge": {
        "quadrant": "LE",
        "quadrant_name": "Lesser Evil",
        "node_name": "Emotional-physics / Learning",
        "isms": ["Indulgence", "Folly"],
        "description": "Emotional-physics, Learning, Indulgence, Folly. Lack of self-control, folly, immediate gratification, emotional volatility."
    },
    "le-lg": {
        "quadrant": "LE",
        "quadrant_name": "Lesser Evil",
        "node_name": "Physics / Meta-Physics",
        "isms": ["Denial", "Dogma"],
        "description": "Physics, Meta-Physics, Denial, Dogma. Denial of facts, rigid dogma, closed-mindedness, ideological blindness."
    },
    "ge-gg": {
        "quadrant": "GE",
        "quadrant_name": "Greater Evil",
        "node_name": "Society / Sociology",
        "isms": ["Anarchy", "Apathy"],
        "description": "Society, Sociology, Anarchy, Apathy. Societal apathy, passive allowance of harm, anarchy, social collapse."
    },
    "ge-le": {
        "quadrant": "GE",
        "quadrant_name": "Greater Evil",
        "node_name": "Internal Judgment / The World",
        "isms": ["Corruption", "Cowardice"],
        "description": "Internal Judgment, The World, Corruption, Cowardice. Systemic corruption, personal cowardice, compromise, ethical failure."
    },
    "ge-ge": {
        "quadrant": "GE",
        "quadrant_name": "Greater Evil",
        "node_name": "History / Reality",
        "isms": ["Erasure", "Delusion"],
        "description": "History, Reality, Erasure, Delusion. Historical erasure, self-delusion, complete denial of reality, revisionism."
    },
    "ge-lg": {
        "quadrant": "GE",
        "quadrant_name": "Greater Evil",
        "node_name": "Psychology / Language",
        "isms": ["Confusion", "Deceit"],
        "description": "Psychology, Language, Confusion, Deceit. Deliberate deceit, manipulation, mental confusion, lying, gaslighting."
    }
}

def clean_paragraph(p):
    # Strip markdown headings, lists, links
    p = p.strip()
    # Remove leading '#', '*' or '-'
    while p.startswith(('#', '*', '-', ' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.')):
        p = p.lstrip('#*- .0123456789')
    # Simple regex-less link stripping or clean text
    return p

def main():
    parser = argparse.ArgumentParser(description="Analyze document coherence, core points, topic direction, and semantic clusters.")
    parser.add_argument("file", help="Path to the markdown file to analyze")
    parser.add_argument("--threshold", type=float, default=0.35, help="Coherence threshold for fragmentation")
    args = parser.parse_args()

    file_path = args.file
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    print(f"Reading file: {os.path.basename(file_path)}...")
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split into paragraphs and filter
    raw_paras = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 30]
    cleaned_paras = [clean_paragraph(p) for p in raw_paras]
    # Filter empty ones
    paras = []
    for i, cp in enumerate(cleaned_paras):
        if len(cp) > 30:
            paras.append((raw_paras[i], cp))

    n_paras = len(paras)
    if n_paras < 2:
        print(f"Document must have at least 2 paragraphs. Found {n_paras}.")
        return

    print(f"Parsed {n_paras} text paragraphs for analysis.")

    # Load Model
    print("Loading SentenceTransformer model ('all-MiniLM-L6-v2')...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Embed paragraphs
    print("Embedding paragraphs...")
    para_texts = [p[1] for p in paras]
    embs = model.encode(para_texts, show_progress_bar=False)

    # 1. COHERENCE ANALYSIS
    print("Computing coherence metrics...")
    sims = []
    for i in range(n_paras - 1):
        sim = cosine_similarity([embs[i]], [embs[i+1]])[0][0]
        sims.append(float(sim))

    avg_coherence = np.mean(sims)
    std_coherence = np.std(sims)
    drift = cosine_similarity([embs[0]], [embs[-1]])[0][0]
    
    # Fragmentation Index: fraction of consecutive transitions below threshold
    frag_count = sum(1 for s in sims if s < args.threshold)
    frag_index = frag_count / len(sims)

    print("\n" + "="*50)
    print("           DOCUMENT COHERENCE ANALYSIS")
    print("="*50)
    print(f"Average Local Coherence (Consecutive Similarity): {avg_coherence:.4f}")
    print(f"Coherence Standard Deviation (Variance):        {std_coherence:.4f}")
    print(f"Semantic Drift (First vs. Last Paragraph):      {drift:.4f}")
    print(f"Fragmentation Index (Transitions < {args.threshold}):      {frag_index:.2%} ({frag_count}/{len(sims)} transitions)")
    
    # Interpretation of coherence
    if avg_coherence >= 0.60:
        status = "EXCELLENT - Highly fluid transitions, logical thematic flow."
    elif avg_coherence >= 0.45:
        status = "GOOD - Strong thematic flow with moderate transition variances."
    elif avg_coherence >= 0.35:
        status = "MODERATE - Somewhat disjointed transitions or abrupt subject switches."
    else:
        status = "POOR - High semantic fragmentation. Abrupt changes or lacks unified structure."
    print(f"Coherence Verdict: {status}")

    # Transition breakdown
    print("\nTransition Details:")
    for i in range(len(sims)):
        # print snippet of para i and i+1
        p_curr = para_texts[i][:40].replace('\n', ' ') + "..."
        p_next = para_texts[i+1][:40].replace('\n', ' ') + "..."
        marker = "⚠ [FRAGILE]" if sims[i] < args.threshold else "  [SMOOTH]"
        print(f"  Transition {i:02d} -> {i+1:02d}: Sim={sims[i]:.3f} {marker} (\"{p_curr}\" -> \"{p_next}\")")

    # 2. CORE POINTS (Semantic Centrality)
    print("\n" + "="*50)
    print("               IDENTIFYING CORE POINTS")
    print("="*50)
    
    # Compute centrality: average similarity to all other paragraphs
    centralities = []
    all_sims = cosine_similarity(embs)
    for i in range(n_paras):
        # Exclude self-similarity in average
        avg_sim = (sum(all_sims[i]) - 1.0) / (n_paras - 1)
        centralities.append(avg_sim)

    sorted_indices = np.argsort(centralities)[::-1]
    
    print("Top 3 Core Paragraphs (Highest Centrality):")
    for rank, idx in enumerate(sorted_indices[:3]):
        raw_text = paras[idx][0]
        # truncate
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        display_text = " ".join(lines[:3])
        if len(display_text) > 280:
            display_text = display_text[:280] + "..."
        
        print(f"\n  #{rank+1} (Para {idx}, Centrality={centralities[idx]:.3f}):")
        print(f"    \"{display_text}\"")

    # 3. TOPIC DIRECTION / TRAJECTORY
    print("\n" + "="*50)
    print("             TOPIC DIRECTION & TRAJECTORY")
    print("="*50)
    
    # Embed Hegemony Points
    hp_keys = list(HEGEMONY_POINTS.keys())
    hp_texts = [f"{HEGEMONY_POINTS[k]['node_name']} ({HEGEMONY_POINTS[k]['sub_vector']}) - {HEGEMONY_POINTS[k]['description']}" for k in hp_keys]
    hp_embs = model.encode(hp_texts, show_progress_bar=False)

    # Project paragraphs to Hegemony Points
    para_attractors = []
    print("Tracing Hegemony Attractors sequence:")
    for i in range(n_paras):
        p_emb = embs[i]
        sims_hp = []
        for hp_emb in hp_embs:
            sims_hp.append(cosine_similarity([p_emb], [hp_emb])[0][0])
        best_hp_idx = np.argmax(sims_hp)
        best_hp = hp_keys[best_hp_idx]
        para_attractors.append((best_hp, sims_hp[best_hp_idx]))
        
        hp_info = HEGEMONY_POINTS[best_hp]
        print(f"  Para {i:02d}: {hp_info['quadrant_name']} ({best_hp}) -> {hp_info['node_name']} (Sim={sims_hp[best_hp_idx]:.3f})")

    # Thematic stages of the document
    print("\nThematic Trajectory Summary:")
    if n_paras >= 3:
        stages = np.array_split(range(n_paras), 3)
        stage_names = ["Beginning (Intro/Setup)", "Middle (Elaboration/Core)", "End (Conclusion/Resolve)"]
        for s_idx, stage_paras in enumerate(stages):
            if len(stage_paras) == 0: continue
            stage_hps = [para_attractors[p][0] for p in stage_paras]
            # find most common
            unique_hps, counts = np.unique(stage_hps, return_counts=True)
            dominant_hp = unique_hps[np.argmax(counts)]
            dominant_info = HEGEMONY_POINTS[dominant_hp]
            print(f"  * {stage_names[s_idx]}: Dominant Attractor is {dominant_info['quadrant_name']} [{dominant_hp}] ({dominant_info['node_name']})")
            print(f"    Represented by isms: {', '.join(dominant_info['isms'])}")

    # 4. GLOBAL SEMANTIC CLUSTERS
    script_dir = os.path.dirname(os.path.abspath(__file__))
    topic_ism_path = os.path.join(script_dir, "topic_ism_mapping.json")
    
    if os.path.exists(topic_ism_path):
        print("\n" + "="*50)
        print("          GLOBAL SEMANTIC CLUSTER MAPPING")
        print("="*50)
        print("Loading global topic definitions...")
        with open(topic_ism_path, 'r', encoding='utf-8') as f:
            topic_isms = json.load(f)

        # We will embed the topic keyword list for all topics and map each paragraph to the closest topic
        topic_keys = sorted(list(topic_isms.keys()), key=lambda x: int(x))
        topic_kw_texts = [f"Topic keywords: {', '.join(topic_isms[tk]['keywords'])}" for tk in topic_keys]
        
        print(f"Embedding {len(topic_keys)} topic signature vectors...")
        topic_embs = model.encode(topic_kw_texts, show_progress_bar=False)

        # For each paragraph, find nearest topic
        assigned_topics = []
        for i in range(n_paras):
            p_emb = embs[i]
            sims_t = []
            for t_emb in topic_embs:
                sims_t.append(cosine_similarity([p_emb], [t_emb])[0][0])
            best_t_idx = np.argmax(sims_t)
            best_t_key = topic_keys[best_t_idx]
            assigned_topics.append((best_t_key, sims_t[best_t_idx]))

        # Group topics
        topic_counts = {}
        for t_key, sim in assigned_topics:
            topic_counts[t_key] = topic_counts.get(t_key, 0) + 1

        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        print("\nDominant Global Semantic Clusters identified in this document:")
        for t_key, count in sorted_topics[:3]:
            pct = count / n_paras
            t_info = topic_isms[t_key]
            kws = ", ".join(t_info["keywords"][:8])
            print(f"  * Topic #{t_key} ({count} paragraphs, {pct:.1%}):")
            print(f"    - Keywords: {kws}...")
            print(f"    - Aligned Attractor: {t_info['quadrant_name']} [{t_info['assigned_point']}] ({t_info['node_name']})")
            print(f"    - Associated Isms: {', '.join(t_info['isms'])}")
    else:
        print("\nNote: topic_ism_mapping.json not found. Skipping global semantic cluster mapping.")

if __name__ == "__main__":
    main()
