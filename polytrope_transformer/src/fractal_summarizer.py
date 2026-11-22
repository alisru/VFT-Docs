"""
Fractal Polytrope Summarizer
Pure algorithmic & tensor-based extraction of a document's invariant core.
Zero external LLM API tokens required.

Pipeline:
1. Deconstructs document into Paragraphs and Sentences.
2. Classifies each block into the 7 Interrogative Planes:
   - Q1 Who (Agent / Subject)
   - Q2 What (Entity / Potential)
   - Q3 Where (Spatial Context / Matter)
   - Q4 Why (Purpose / Motive)
   - Q5 How (Mechanism / Action)
   - Q6 Cause (Historical Antecedent / Trigger)
   - Q7 Effect (Resolved State / Consequence)
3. Evaluates Optical Thickness (tau) and Luminescence (L):
   - High Luminescence = Balanced Action -> Strain -> Effect closure (The Invariant Joints).
   - Low Luminescence = Diffuse filler / ungrounded scatter.
4. Synthesizes Multi-Scale Summary:
   - Level 1: Invariant Singularity (1 sentence)
   - Level 2: 7-Plane Geodesic Summary (7 points)
   - Level 3: Section Invariant Backbone
"""

import sys
import re
import json
import time

def parse_markdown_sections(text):
    """Splits markdown into header-delimited sections and paragraphs."""
    lines = text.splitlines()
    sections = []
    current_sec = {"title": "Introduction", "paragraphs": []}
    curr_para = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            if curr_para:
                current_sec["paragraphs"].append(" ".join(curr_para))
                curr_para = []
            if current_sec["paragraphs"]:
                sections.append(current_sec)
            title = stripped.lstrip('#').strip()
            current_sec = {"title": title, "paragraphs": []}
        elif stripped == "" or stripped.startswith("---"):
            if curr_para:
                current_sec["paragraphs"].append(" ".join(curr_para))
                curr_para = []
        else:
            curr_para.append(stripped)
            
    if curr_para:
        current_sec["paragraphs"].append(" ".join(curr_para))
    if current_sec["paragraphs"]:
        sections.append(current_sec)
        
    return sections

def extract_planar_weights(sentence):
    """Calculates density of 7 Q-Planes in a sentence."""
    s_low = sentence.lower()
    
    # 7-Plane Lexical Anchors
    q1 = len(re.findall(r'\b(agent|author|we|they|person|doctor|human|researcher|i|you|who|observer|mind|god|sovereign)\b', s_low))
    q2 = len(re.findall(r'\b(word|formula|state|potential|options|entity|matter|structure|tool|concept|object|definition|what)\b', s_low))
    q3 = len(re.findall(r'\b(world|space|field|ground|place|body|coordinates|matter|distance|where|physical|box|plane)\b', s_low))
    q4 = len(re.findall(r'\b(to survive|to build|in order to|purpose|meaning|why|so that|reason|motive|intent|resonance)\b', s_low))
    q5 = len(re.findall(r'\b(moves|apply|effort|invented|repeat|coordinate|transmit|change|rule|how|process|work|method|mechanism|logic)\b', s_low))
    q6 = len(re.findall(r'\b(when|because|since|precedent|history|lineage|origin|cause|past|was|starting|genesis)\b', s_low))
    q7 = len(re.findall(r'\b(ordered state|state transition|survival|safe|clarity|order|effect|consequence|impact|peace|decay|loss)\b', s_low))
    
    return {
        "Q1": q1, "Q2": q2, "Q3": q3, "Q4": q4, "Q5": q5, "Q6": q6, "Q7": q7,
        "cause_weight": q1 + q2 + q3 + q6,
        "effect_weight": q4 + q5 + q7,
        "total_density": q1 + q2 + q3 + q4 + q5 + q6 + q7
    }

def calculate_luminescence(sentence, weights):
    """
    Computes Semantic Luminescence L:
    High when Action (Q5), Strain (Q2/Q6), and Effect (Q7) are present in single coherent bridge.
    L = Phi_0 / (1 + alpha * tau)
    """
    has_action = weights["Q5"] > 0
    has_context = (weights["Q1"] + weights["Q2"] + weights["Q3"]) > 0
    has_effect = weights["Q7"] > 0 or weights["Q4"] > 0
    
    # Optical thickness penalty (diffuse scatter if length is high but planar density is low)
    word_count = len(sentence.split())
    if word_count == 0:
        return 0.0
        
    density_ratio = weights["total_density"] / word_count
    
    # Complete AE-C closure bonus
    closure_bonus = 2.0 if (has_action and has_context and has_effect) else 1.0
    
    luminescence = (density_ratio * closure_bonus) / (1.0 + (word_count / 40.0))
    return luminescence

def summarize_document(file_path):
    t_start = time.time()
    
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
        
    raw_word_count = len(text.split())
    sections = parse_markdown_sections(text)
    
    total_paragraphs = sum(len(sec["paragraphs"]) for sec in sections)
    all_sentences = []
    
    scored_sentences = []
    
    for sec_idx, sec in enumerate(sections):
        for p_idx, p in enumerate(sec["paragraphs"]):
            s_list = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if len(s.strip()) > 15]
            for s in s_list:
                weights = extract_planar_weights(s)
                lum = calculate_luminescence(s, weights)
                scored_sentences.append({
                    "sentence": s,
                    "section": sec["title"],
                    "weights": weights,
                    "luminescence": lum,
                    "para_idx": p_idx
                })
                
    # Sort by Luminescence
    sorted_by_lum = sorted(scored_sentences, key=lambda x: x["luminescence"], reverse=True)
    
    t_end = time.time()
    elapsed_ms = (t_end - t_start) * 1000.0
    
    # --- LEVEL 1: Invariant Singularity (Highest Luminescence Sentence) ---
    singularity = sorted_by_lum[0]["sentence"] if sorted_by_lum else "N/A"
    
    # --- LEVEL 2: 7-Plane Geodesic Summary (Top sentence for each plane) ---
    geodesic = {}
    for plane in ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]:
        best = max(scored_sentences, key=lambda x: x["weights"][plane] * (1.0 + x["luminescence"]))
        geodesic[plane] = best["sentence"]
        
    # --- LEVEL 3: Invariant Structural Spine (Best sentence per major section) ---
    spine = []
    for sec in sections:
        sec_sentences = [s for s in scored_sentences if s["section"] == sec["title"]]
        if sec_sentences:
            best_sec_s = max(sec_sentences, key=lambda x: x["luminescence"])
            spine.append({"section": sec["title"], "key_invariant": best_sec_s["sentence"]})
            
    return {
        "file": file_path,
        "metrics": {
            "raw_word_count": raw_word_count,
            "total_sections": len(sections),
            "total_paragraphs": total_paragraphs,
            "total_sentences": len(scored_sentences),
            "external_api_tokens": 0,
            "runtime_ms": elapsed_ms
        },
        "level_1_singularity": singularity,
        "level_2_geodesic": geodesic,
        "level_3_spine": spine
    }

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else r"e:\Vector Field Theory\VFT Docs\_VFT MD\Treatise_on_How_Words_Work.md"
    result = summarize_document(target)
    
    print("=" * 80)
    print(f"FRACTAL POLYTROPE SUMMARY FOR: {result['file']}")
    print("=" * 80)
    print(f"Execution Transparency:")
    print(f"  • Source Word Count:       {result['metrics']['raw_word_count']} words")
    print(f"  • Sections Analyzed:       {result['metrics']['total_sections']}")
    print(f"  • Sentences Evaluated:     {result['metrics']['total_sentences']}")
    print(f"  • External API Tokens Used: 0 (100% Local Invariant Extraction)")
    print(f"  • Execution Runtime:       {result['metrics']['runtime_ms']:.2f} ms")
    print("-" * 80)
    
    print("\nLEVEL 1: INVARIANT SINGULARITY (Core Locked [IS] Statement):")
    print(f"\"{result['level_1_singularity']}\"")
    
    print("\n" + "-" * 80)
    print("LEVEL 2: 7-PLANE COGNITIVE GEODESIC SUMMARY (One Invariant per Reality Plane):")
    labels = {
        "Q1": "Q1 (Who / Agentic Will):    ",
        "Q2": "Q2 (What / Potential State): ",
        "Q3": "Q3 (Where / Spatial Ground): ",
        "Q4": "Q4 (Why / Purpose & Meaning):",
        "Q5": "Q5 (How / Action Mechanism): ",
        "Q6": "Q6 (Cause / Origin Lineage): ",
        "Q7": "Q7 (Effect / Resolved State):"
    }
    for q, sent in result["level_2_geodesic"].items():
        print(f"  {labels[q]} \"{sent}\"")
        
    print("\n" + "-" * 80)
    print("LEVEL 3: STRUCTURAL INVARIANT SPINE (Section-by-Section Anchors):")
    for s in result["level_3_spine"][:8]: # Show top 8
        print(f"\n[ {s['section']} ]")
        print(f"  -> \"{s['key_invariant']}\"")
