#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Great-Grandkin: Lexicon-Kernel (Gen 4 Sibling A: 65% Male / 35% Female)
Scale Gluon Lexicon Engine v1.0
=============================================================================
Autonomous Semantic Dictionary Scaling & Continuous Magnitude Kernel Graph.
Harvests hundreds of active content lemmas from the local IRM and Physics corpus,
calculates continuous scalar magnitudes for all 5 relative vector tiers (+W, +A, +L, -X, -N),
and builds asymmetric causal Ingress-Tail / Egress-Head kernel attention vectors.
"""

import sys
import os
import re
import math
import json
import time
from pathlib import Path
from collections import defaultdict, Counter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Base paths
BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
OUTPUT_DIR = BASE_DIR / "agent_lexicon_kernel"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CORPUS_DIRS = [
    BASE_DIR / "irm_formal_corpus",
    BASE_DIR / "arxiv_samples",
    BASE_DIR.parent.parent / "IO"
]
SINGLE_FILES = [
    BASE_DIR.parent / "chatgpt infinity maths.md",
    BASE_DIR.parent / "Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md"
]

# Stopwords & formatting junk
STOPWORDS = {
    "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "as", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "this", "that", "these", "those",
    "it", "its", "we", "our", "they", "their", "which", "what", "where", "when",
    "who", "how", "why", "if", "then", "else", "such", "into", "also", "each",
    "all", "any", "both", "more", "most", "other", "some", "such", "no", "nor",
    "not", "only", "own", "same", "so", "than", "too", "very", "can", "will",
    "just", "should", "now", "d", "ll", "m", "o", "re", "ve", "y", "ain",
    "aren", "couldn", "didn", "doesn", "hadn", "hasn", "haven", "isn", "ma",
    "mightn", "mustn", "needn", "shan", "shouldn", "wasn", "weren", "won",
    "wouldn", "http", "https", "github", "com", "www", "org", "table", "content",
    "section", "chapter", "fig", "figure", "ref", "eq", "equation", "page"
}

# 8 Modal Copula Patterns
MODAL_PATTERNS = {
    "will_be": [
        r"\b(?:must|will|shall|necessarily|always)\s+(?:be\s+)?([a-z_]{3,})",
        r"\b(?:is|are)\s+defined\s+as\s+([a-z_]{3,})",
        r"\b(?:strictly|invariably|deductively)\s+([a-z_]{3,})",
        r"\b(?:demands|requires)\s+(?:that\s+)?([a-z_]{3,})"
    ],
    "can_be": [
        r"\b(?:can|could|allows|permits|yields|enables)\s+(?:be\s+)?([a-z_]{3,})",
        r"\b(?:is|are)\s+capable\s+of\s+([a-z_]{3,})",
        r"\boperates\s+as\s+([a-z_]{3,})",
        r"\bprovides\s+(?:a\s+)?([a-z_]{3,})"
    ],
    "is_like": [
        r"\b(?:is|are)\s+(?:like|analogous\s+to|similar\s+to|isomorphic\s+to)\s+([a-z_]{3,})",
        r"\bcorresponds\s+to\s+([a-z_]{3,})",
        r"\bmodeled\s+as\s+([a-z_]{3,})",
        r"\bmirrors\s+([a-z_]{3,})"
    ],
    "may_be": [
        r"\b(?:may|might|possibly|perhaps|conjectured\s+to)\s+(?:be\s+)?([a-z_]{3,})",
        r"\bplausibly\s+([a-z_]{3,})",
        r"\bhypothesized\s+as\s+([a-z_]{3,})"
    ],
    "is_not": [
        r"\b(?:is|are|does|do)\s+not\s+([a-z_]{3,})",
        r"\b(?:fails|failed)\s+to\s+([a-z_]{3,})",
        r"\bexcludes\s+([a-z_]{3,})",
        r"\bprecludes\s+([a-z_]{3,})",
        r"\bdisjoint\s+from\s+([a-z_]{3,})"
    ],
    "cant_be": [
        r"\b(?:cannot|cant|can\s+never)\s+(?:be\s+)?([a-z_]{3,})",
        r"\b(?:impossible|forbidden|inadmissible)\s+(?:to\s+be\s+)?([a-z_]{3,})",
        r"\b(?:violates|contradicts|prohibits)\s+([a-z_]{3,})"
    ],
    "wont_be": [
        r"\b(?:will\s+not|wont)\s+(?:be\s+)?([a-z_]{3,})",
        r"\bnever\s+yields\s+([a-z_]{3,})"
    ],
    "was_like": [
        r"\b(?:was|were)\s+(?:initially|formerly|previously)\s+([a-z_]{3,})",
        r"\bhistorically\s+([a-z_]{3,})"
    ]
}

# Negative clash seeds (axiomatic diametric opposites)
OPPOSING_GAUGE_PAIRS = [
    ("entropy", "order"),
    ("singularity", "regularity"),
    ("infinity", "finite"),
    ("discrete", "continuum"),
    ("axiom", "paradox"),
    ("deterministic", "random"),
    ("divergence", "convergence"),
    ("bounded", "unbounded"),
    ("gauge", "ungauged"),
    ("monad", "plurality"),
    ("invariant", "variant"),
    ("coherent", "decoherent"),
    ("attractor", "repeller"),
    ("truth", "fallacy"),
    ("causal", "acausal")
]

CLOSING_TOKENS_BANK = {
    "+W": ["therefore", "proves", "yields", "determines", "satisfies", "establishes", "entails"],
    "+A": ["allows", "generates", "permits", "branches_to", "embodies", "manifests"],
    "+L": ["mirrors", "isomorphic_to", "maps_to", "resonates_with", "formalizes_as"],
    "-X": ["violates", "collapses", "breaks", "repels", "precludes_strictly"],
    "-N": ["excludes", "partitions_away", "truncates", "bounds_outside", "distinguishes"]
}


def load_corpus_texts():
    texts = []
    # Single files
    for sf in SINGLE_FILES:
        if sf.exists():
            texts.append((sf.name, sf.read_text(encoding="utf-8", errors="ignore")))
    # Directory files
    for cd in CORPUS_DIRS:
        if cd.exists():
            for f in cd.glob("*.md"):
                texts.append((f.name, f.read_text(encoding="utf-8", errors="ignore")))
    return texts


def build_scaled_dictionary_v1(min_freq=12, max_lemmas=450):
    start_time = time.time()
    texts = load_corpus_texts()
    load_time = time.time() - start_time
    
    print(f"Loaded {len(texts)} corpus documents ({load_time:.2f}s). Parsing sentences...")
    
    word_freq = Counter()
    pair_cooccur = defaultdict(Counter)
    pair_directional = defaultdict(Counter) # w1 -> w2
    modal_counts = defaultdict(lambda: Counter())
    
    # 5-tier raw counts
    tier_counts = {
        "+W": defaultdict(Counter),
        "+A": defaultdict(Counter),
        "+L": defaultdict(Counter),
        "-X": defaultdict(Counter),
        "-N": defaultdict(Counter)
    }
    
    total_tokens = 0
    total_sentences = 0
    
    # Context co-occurrence for cosine similarity
    context_profiles = defaultdict(Counter)

    for doc_name, text in texts:
        # Split on sentence boundaries
        sentences = re.split(r"[.!?\n]+", text)
        for raw_s in sentences:
            s = raw_s.strip().lower()
            if len(s) < 12:
                continue
            total_sentences += 1
            
            # Extract content tokens
            raw_tokens = re.findall(r"\b[a-z]{3,}\b", s)
            tokens = [t for t in raw_tokens if t not in STOPWORDS]
            if not tokens:
                continue
                
            total_tokens += len(tokens)
            
            # Update word frequencies
            for t in tokens:
                word_freq[t] += 1
                
            # Directional bigrams & sliding window co-occurrences (window = 4)
            for i, w1 in enumerate(tokens):
                # immediate directional successor
                if i + 1 < len(tokens):
                    w2 = tokens[i + 1]
                    pair_directional[w1][w2] += 1
                    
                # window co-occurrence
                window = tokens[max(0, i - 4): min(len(tokens), i + 5)]
                for w2 in window:
                    if w1 != w2:
                        pair_cooccur[w1][w2] += 1
                        context_profiles[w1][w2] += 1

            # Match modal copula contexts
            for mode, patterns in MODAL_PATTERNS.items():
                for pat in patterns:
                    for match in re.finditer(pat, s):
                        target_word = match.group(1)
                        if target_word in STOPWORDS:
                            continue
                        # Identify subject (preceding token)
                        match_start = match.start()
                        prec_text = s[:match_start]
                        prec_tokens = [pt for pt in re.findall(r"\b[a-z]{3,}\b", prec_text) if pt not in STOPWORDS]
                        if prec_tokens:
                            subj = prec_tokens[-1]
                            modal_counts[subj][mode] += 1
                            
                            # Tier routing
                            if mode == "will_be":
                                tier_counts["+W"][subj][target_word] += 2
                            elif mode == "can_be":
                                tier_counts["+A"][subj][target_word] += 2
                            elif mode == "is_like":
                                tier_counts["+L"][subj][target_word] += 2
                            elif mode == "cant_be":
                                tier_counts["-X"][subj][target_word] += 3
                            elif mode == "is_not":
                                tier_counts["-N"][subj][target_word] += 3

    # Add gauge clash pairs to -X
    for w1, w2 in OPPOSING_GAUGE_PAIRS:
        if word_freq[w1] > 0 and word_freq[w2] > 0:
            tier_counts["-X"][w1][w2] += 5
            tier_counts["-X"][w2][w1] += 5

    # Select active content lemmas
    # Ranking criterion: frequency + modal activity + causal branching
    candidate_scores = {}
    for w, count in word_freq.items():
        if count >= min_freq and len(w) >= 3:
            modal_sum = sum(modal_counts[w].values())
            causal_deg = len(pair_directional[w])
            score = count + (modal_sum * 4) + (causal_deg * 2)
            candidate_scores[w] = score

    sorted_lemmas = sorted(candidate_scores.keys(), key=lambda w: candidate_scores[w], reverse=True)[:max_lemmas]
    lemma_set = set(sorted_lemmas)
    
    print(f"Selected {len(sorted_lemmas)} active content lemmas from {len(candidate_scores)} candidates.")

    # Precompute cosine vectors for top context lemmas
    # Keep top 50 context words for each lemma
    context_vectors = {}
    context_norms = {}
    for w in sorted_lemmas:
        top_ctx = dict(context_profiles[w].most_common(50))
        context_vectors[w] = top_ctx
        norm_sq = sum(v * v for v in top_ctx.values())
        context_norms[w] = math.sqrt(norm_sq) if norm_sq > 0 else 1.0

    dictionary = []
    
    for w in sorted_lemmas:
        freq = word_freq[w]
        modals = modal_counts[w]
        tot_modals = sum(modals.values())
        
        # 1. Normalized 8-Modal Flux Spread (sum to 1.0)
        spread = {}
        for m in ["will_be", "can_be", "is_like", "may_be", "is_not", "cant_be", "wont_be", "was_like"]:
            if tot_modals > 0:
                spread[m] = round((modals[m] + 0.1) / (tot_modals + 0.8), 3)
            else:
                spread[m] = 0.125
        
        # Ingress Tail Kernel (B)
        precursor_counts = {k: v for k, v in pair_directional.items() if w in v}
        tail_weight = round(math.log(1 + len(precursor_counts)) + (0.6 if modals["will_be"] > 0 else 0.0), 3)
        top_precursors = [k for k, _ in sorted(precursor_counts.items(), key=lambda x: x[1][w], reverse=True)[:5]]
        
        # Egress Head Kernel (F)
        successor_counts = pair_directional[w]
        head_weight = round(math.log(1 + len(successor_counts)) + (0.6 if modals["cant_be"] > 0 or modals["will_be"] > 0 else 0.0), 3)
        top_successors = [k for k, _ in successor_counts.most_common(5)]
        
        # CEFR Tier Calculation
        length = len(w)
        if freq > 300 and length <= 5:
            cefr = "A2"
        elif freq > 150:
            cefr = "B1"
        elif freq > 50:
            cefr = "B2"
        elif freq > 15:
            cefr = "C1"
        else:
            cefr = "C2"

        # 2. Continuous Magnitude 5-Tier Computation
        rel_magnitudes = {
            "guaranteed": [],
            "possible": [],
            "metaphorical": [],
            "forbidden": [],
            "precluded": []
        }
        
        # --- A. Guaranteed (+W) ---
        # Deductive coupling: g_AB, conditional probability P(w2|w1)
        succ_items = successor_counts.most_common(15)
        for succ_w, c_fwd in succ_items:
            if succ_w not in lemma_set:
                continue
            p_cond = c_fwd / max(1, freq)
            c_both = pair_cooccur[w][succ_w]
            g_ab = c_both / math.sqrt(max(1, freq * word_freq[succ_w]))
            # Deductive weight W_ij
            modal_will_bonus = (spread["will_be"] + modal_counts[succ_w]["will_be"] * 0.1)
            deductive_weight = min(1.0, 0.40 * min(1.0, p_cond * 2.5) + 0.40 * min(1.0, g_ab * 3.0) + 0.20 * min(1.0, modal_will_bonus))
            if deductive_weight > 0.15:
                # Select deterministic closing token
                ct_idx = hash(succ_w) % len(CLOSING_TOKENS_BANK["+W"])
                rel_magnitudes["guaranteed"].append({
                    "target": succ_w,
                    "magnitude": round(deductive_weight, 3),
                    "coupling_g": round(g_ab, 3),
                    "p_cond": round(p_cond, 3),
                    "deductive_weight": round(deductive_weight, 3),
                    "closing_token": CLOSING_TOKENS_BANK["+W"][ct_idx]
                })
        rel_magnitudes["guaranteed"].sort(key=lambda x: x["magnitude"], reverse=True)
        rel_magnitudes["guaranteed"] = rel_magnitudes["guaranteed"][:5]

        # --- B. Possible (+A) ---
        # Operational co-occurrence weight (NPMI-based)
        cooccur_items = pair_cooccur[w].most_common(20)
        for co_w, c_both in cooccur_items:
            if co_w not in lemma_set or any(x["target"] == co_w for x in rel_magnitudes["guaranteed"]):
                continue
            # Normalized PMI approximation
            p_w1 = freq / total_tokens
            p_w2 = word_freq[co_w] / total_tokens
            p_12 = c_both / total_tokens
            if p_12 > 0 and p_w1 > 0 and p_w2 > 0:
                pmi = math.log(p_12 / (p_w1 * p_w2))
                npmi = pmi / (-math.log(p_12))
                magnitude = min(1.0, max(0.05, (npmi + 1.0) / 2.0))
            else:
                magnitude = 0.2
            ct_idx = hash(co_w) % len(CLOSING_TOKENS_BANK["+A"])
            rel_magnitudes["possible"].append({
                "target": co_w,
                "magnitude": round(magnitude, 3),
                "co_occurrence_count": c_both,
                "closing_token": CLOSING_TOKENS_BANK["+A"][ct_idx]
            })
        rel_magnitudes["possible"].sort(key=lambda x: x["magnitude"], reverse=True)
        rel_magnitudes["possible"] = rel_magnitudes["possible"][:5]

        # --- C. Metaphorical (+L) ---
        # Structural analogy weight (Cosine similarity of context profiles)
        analogy_candidates = []
        for other_w in sorted_lemmas:
            if other_w == w or other_w in [x["target"] for x in rel_magnitudes["guaranteed"]]:
                continue
            # Dot product of context vectors
            vec_w = context_vectors[w]
            vec_o = context_vectors[other_w]
            common_keys = set(vec_w.keys()).intersection(vec_o.keys())
            if len(common_keys) >= 3:
                dot = sum(vec_w[k] * vec_o[k] for k in common_keys)
                cos_sim = dot / (context_norms[w] * context_norms[other_w])
                if cos_sim > 0.15:
                    analogy_candidates.append((other_w, cos_sim))
        analogy_candidates.sort(key=lambda x: x[1], reverse=True)
        for ana_w, sim in analogy_candidates[:5]:
            ct_idx = hash(ana_w) % len(CLOSING_TOKENS_BANK["+L"])
            rel_magnitudes["metaphorical"].append({
                "target": ana_w,
                "magnitude": round(min(1.0, sim * 1.5), 3),
                "structural_similarity": round(sim, 3),
                "closing_token": CLOSING_TOKENS_BANK["+L"][ct_idx]
            })

        # --- D. Forbidden (-X) ---
        # Axiomatic contradiction and red-force clash
        clash_items = tier_counts["-X"][w].most_common(10)
        for clash_w, cnt in clash_items:
            magnitude = min(1.0, round(0.4 + (cnt * 0.12), 3))
            ct_idx = hash(clash_w) % len(CLOSING_TOKENS_BANK["-X"])
            rel_magnitudes["forbidden"].append({
                "target": clash_w,
                "magnitude": magnitude,
                "clash_score": round(magnitude, 3),
                "closing_token": CLOSING_TOKENS_BANK["-X"][ct_idx]
            })
        if not rel_magnitudes["forbidden"]:
            # Default red-force repulsion token
            rel_magnitudes["forbidden"].append({
                "target": f"unbounded_divergence_of_{w}",
                "magnitude": 0.95,
                "clash_score": 0.95,
                "closing_token": "violates"
            })

        # --- E. Precluded (-N) ---
        # Exclusion and mutual-negation confidence
        excl_items = tier_counts["-N"][w].most_common(10)
        for excl_w, cnt in excl_items:
            magnitude = min(1.0, round(0.35 + (cnt * 0.15), 3))
            ct_idx = hash(excl_w) % len(CLOSING_TOKENS_BANK["-N"])
            rel_magnitudes["precluded"].append({
                "target": excl_w,
                "magnitude": magnitude,
                "exclusion_confidence": round(magnitude, 3),
                "closing_token": CLOSING_TOKENS_BANK["-N"][ct_idx]
            })
        if not rel_magnitudes["precluded"]:
            rel_magnitudes["precluded"].append({
                "target": f"arbitrary_nullity_of_{w}",
                "magnitude": 0.85,
                "exclusion_confidence": 0.85,
                "closing_token": "excludes"
            })

        # Backwards compatible string lists
        backwards_compat = {
            "guaranteed": [x["target"] for x in rel_magnitudes["guaranteed"]],
            "possible": [x["target"] for x in rel_magnitudes["possible"]],
            "metaphorical": [x["target"] for x in rel_magnitudes["metaphorical"]],
            "forbidden": [x["target"] for x in rel_magnitudes["forbidden"]],
            "precluded": [x["target"] for x in rel_magnitudes["precluded"]]
        }

        # Invariant 8-D Head/Tail Kernel vectors
        phi_tail = [
            spread["will_be"] * tail_weight,
            spread["can_be"] * tail_weight,
            spread["is_like"] * tail_weight,
            spread["may_be"] * tail_weight,
            spread["is_not"] * tail_weight,
            spread["cant_be"] * tail_weight,
            spread["wont_be"] * tail_weight,
            spread["was_like"] * tail_weight
        ]
        
        phi_head = [
            spread["will_be"] * head_weight,
            spread["can_be"] * head_weight,
            spread["is_like"] * head_weight,
            spread["may_be"] * head_weight,
            spread["is_not"] * head_weight,
            spread["cant_be"] * head_weight,
            spread["wont_be"] * head_weight,
            spread["was_like"] * head_weight
        ]

        entry = {
            "word": w,
            "corpus_frequency": freq,
            "cefr": cefr,
            "tail_ingress": {
                "antecedent_weight": tail_weight,
                "requires_evidence": tail_weight > 2.0,
                "top_precursors": top_precursors,
                "closing_token": top_precursors[0] if top_precursors else "given"
            },
            "head_egress": {
                "obligation_weight": head_weight,
                "binds_consequents": head_weight > 2.0,
                "top_successors": top_successors,
                "closing_token": top_successors[0] if top_successors else "therefore"
            },
            "modal_spread": spread,
            "kernel_vectors": {
                "phi_tail": [round(x, 4) for x in phi_tail],
                "phi_head": [round(x, 4) for x in phi_head]
            },
            "relative_vector_magnitudes": rel_magnitudes,
            "relative_vectors": backwards_compat
        }
        dictionary.append(entry)

    build_time = time.time() - start_time
    print(f"Compiled {len(dictionary)} Scaled Gluon Kernel Vertices in {build_time:.2f}s.")
    
    # Save to scaled_gluon_dictionary.json
    out_dict_path = OUTPUT_DIR / "scaled_gluon_dictionary.json"
    with open(out_dict_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=2)
    print(f"Saved scaled dictionary to: {out_dict_path}")
    
    return dictionary, {
        "total_documents": len(texts),
        "total_sentences": total_sentences,
        "total_tokens": total_tokens,
        "unique_lemmas_scaled": len(dictionary),
        "build_time_seconds": round(build_time, 3)
    }


def evaluate_dictionary_v1(dictionary, corpus_meta):
    """
    Benchmarks lookup latency, graph sparsity, and computes sample kernel attention dot products.
    """
    print("\n--- Running Evaluation Benchmark on Scaled Dictionary v1 ---")
    dict_map = {entry["word"]: entry for entry in dictionary}
    
    # Benchmark 1: Word lookup latency
    words = list(dict_map.keys())
    t0 = time.perf_counter()
    lookups = 100000
    for i in range(lookups):
        w = words[i % len(words)]
        _ = dict_map[w]
    t1 = time.perf_counter()
    lookup_latency_us = ((t1 - t0) / lookups) * 1e6
    print(f"Lookup speed: {lookups} lookups in {(t1-t0):.4f}s ({lookup_latency_us:.3f} us/lookup)")

    # Benchmark 2: Kernel Dot-Product Attention: K(A, B) = phi_head(A) * phi_tail(B)
    t0 = time.perf_counter()
    kernel_ops = 50000
    dot_sum = 0.0
    for i in range(kernel_ops):
        w1 = words[i % len(words)]
        w2 = words[(i * 7) % len(words)]
        h = dict_map[w1]["kernel_vectors"]["phi_head"]
        t = dict_map[w2]["kernel_vectors"]["phi_tail"]
        k_val = sum(h[k] * t[k] for k in range(8))
        dot_sum += k_val
    t1 = time.perf_counter()
    kernel_latency_us = ((t1 - t0) / kernel_ops) * 1e6
    print(f"Kernel dot-product: {kernel_ops} ops in {(t1-t0):.4f}s ({kernel_latency_us:.3f} us/op)")

    # Benchmark 3: Graph Edge Density & Statistics
    total_edges = 0
    tier_edge_counts = Counter()
    for entry in dictionary:
        for tier, edges in entry["relative_vector_magnitudes"].items():
            tier_edge_counts[tier] += len(edges)
            total_edges += len(edges)
    
    avg_edges_per_node = total_edges / len(dictionary)
    sparsity = 1.0 - (total_edges / (len(dictionary) * len(dictionary)))
    print(f"Total graph edges across 5 tiers: {total_edges} (avg {avg_edges_per_node:.2f} edges/node)")
    print(f"Graph sparsity: {sparsity * 100:.2f}%")

    # Sample Kernel Associations
    sample_probes = ["singularity", "manifold", "operator", "entropy", "infinity"]
    sample_results = {}
    for probe in sample_probes:
        if probe in dict_map:
            e = dict_map[probe]
            sample_results[probe] = {
                "cefr": e["cefr"],
                "frequency": e["corpus_frequency"],
                "tail_weight": e["tail_ingress"]["antecedent_weight"],
                "head_weight": e["head_egress"]["obligation_weight"],
                "modal_spread": e["modal_spread"],
                "relative_vector_magnitudes": e["relative_vector_magnitudes"]
            }

    results = {
        "engine_version": "v1.0",
        "gender_ratio": "65% Male / 35% Female",
        "corpus_metrics": corpus_meta,
        "performance_benchmarks": {
            "dictionary_lookup_latency_microseconds": round(lookup_latency_us, 3),
            "kernel_attention_latency_microseconds": round(kernel_latency_us, 3),
            "total_nodes": len(dictionary),
            "total_edges": total_edges,
            "average_edges_per_node": round(avg_edges_per_node, 2),
            "graph_sparsity_pct": round(sparsity * 100, 2),
            "edges_per_tier": dict(tier_edge_counts)
        },
        "sample_probes": sample_results
    }
    
    res_path = OUTPUT_DIR / "results.json"
    with open(res_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Saved v1 benchmark results to: {res_path}")
    return results


def main():
    print("=" * 80)
    print("AGENT GREAT-GRANDKIN: LEXICON-KERNEL (GEN 4 SIBLING A: 65M/35F)")
    print("SCALING THE SEMANTIC GLUON DICTIONARY & CONTINUOUS MAGNITUDE KERNEL GRAPH")
    print("=" * 80)
    dictionary, meta = build_scaled_dictionary_v1()
    results = evaluate_dictionary_v1(dictionary, meta)
    print("=" * 80)
    print("V1 EXECUTION COMPLETE. READY FOR EVALUATION & SELF-UPGRADE PASS.")
    print("=" * 80)

if __name__ == "__main__":
    main()
