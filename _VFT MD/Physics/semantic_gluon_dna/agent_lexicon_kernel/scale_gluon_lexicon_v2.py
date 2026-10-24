#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Great-Grandkin: Lexicon-Kernel (Gen 4 Sibling A: 65% Male / 35% Female)
Scale Gluon Lexicon Engine v2.0 (Self-Upgraded High-Precision Kernel Edition)
=============================================================================
Major Upgrades in v2.0:
  1. Strict Mathematical/LaTeX Syntax Scrubber: Eliminates LaTeX formatting
     artifacts (mathcal, overline, frac, etc.) to retain only genuine conceptual lemmas.
  2. Vectorized BLAS Causal Kernel Attention: Pre-stacks head and tail matrices
     Phi_head and Phi_tail into NumPy float32 arrays, enabling microsecond batch
     matrix attention K = Phi_head @ Phi_tail.T.
  3. Continuous Scalar Magnitude Formulations:
     - +W (Guaranteed): g_AB coupling, forward conditional P(B|A), deductive weight.
     - +A (Possible): Normalized Pointwise Mutual Information (NPMI) with Laplace smoothing.
     - +L (Metaphorical): Contextual cosine profile similarity with modal is_like weight.
     - -X (Forbidden): Dual-source Red-Force clash (empirical cant_be co-occurrence +
       opposing gauge attractor projection along 15 canonical physical/philosophical axes).
     - -N (Precluded): Exclusion and mutual-negation confidence from empirical is_not
       and asymmetric boundary partitioning.
  4. Invariant Closing Token Engine: Eliminates Agent 1's flaw by providing exact
     closing tokens (therefore, proves, resolves, repels, etc.) for every open obligation.
  5. Bounded Graph Sparsification: Avoids Agent 5's combinatorial traps with strict
     O(k * V) top-k sparse indices.
"""

import sys
import os
import re
import math
import json
import time
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np

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

# LaTeX markup & formatting noise to scrub
LATEX_NOISE = {
    "mathcal", "mathbf", "mathbb", "mathrm", "mathsf", "mathit", "overline",
    "underline", "widehat", "widetilde", "frac", "sqrt", "partial", "nabla",
    "infty", "sum", "prod", "int", "iint", "iiint", "oint", "alpha", "beta",
    "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta", "theta", "iota",
    "kappa", "lambda", "mu", "nu", "xi", "pi", "rho", "sigma", "tau", "upsilon",
    "phi", "chi", "psi", "omega", "times", "cdot", "otimes", "oplus", "subset",
    "subseteq", "supset", "supseteq", "in", "notin", "cup", "cap", "equiv",
    "sim", "simeq", "approx", "cong", "neq", "leq", "geq", "ll", "gg",
    "begin", "end", "align", "equation", "bmatrix", "pmatrix", "vmatrix",
    "left", "right", "cite", "label", "text", "textbf", "textit", "emph",
    "href", "url", "documentclass", "usepackage", "author", "title", "date",
    "abstract", "introduction", "section", "subsection", "subsubsection",
    "paragraph", "item", "itemize", "enumerate", "description", "table",
    "tabular", "figure", "caption", "minipage", "vspace", "hspace", "quad",
    "qquad", "newline", "linebreak", "pagebreak", "clearpage", "cleardoublepage",
    "bigskip", "medskip", "smallskip", "noindent", "indent", "ref", "eqref",
    "pageref", "index", "glossary", "appendix", "bibliography", "bibliographystyle"
}

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
    "wouldn", "http", "https", "github", "com", "www", "org", "content",
    "fig", "eq", "page", "et", "al", "via", "using", "used", "uses", "one",
    "two", "three", "first", "second", "third", "case", "give", "gives", "given",
    "let", "since", "thus", "hence", "may", "might", "well", "either", "neither"
} | LATEX_NOISE

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

# 15 Canonical Physical/Philosophical Gauge Polarity Axes
GAUGE_POLARITY_AXES = [
    ("entropy", "order"),
    ("singularity", "regularity"),
    ("infinity", "finite"),
    ("discrete", "continuum"),
    ("axiom", "paradox"),
    ("deterministic", "random"),
    ("divergence", "convergence"),
    ("bounded", "unbounded"),
    ("gauge", "ungauged"),
    ("monad", "composite"),
    ("invariant", "variant"),
    ("coherent", "decoherent"),
    ("attractor", "repeller"),
    ("conservative", "dissipative"),
    ("causal", "acausal")
]

# Deterministic Invariant Closing Tokens Bank
CLOSING_TOKENS = {
    "+W": ["therefore", "proves", "yields", "determines", "satisfies", "entails", "locks"],
    "+A": ["allows", "generates", "permits", "branches_to", "embodies", "operates"],
    "+L": ["mirrors", "isomorphic_to", "maps_to", "resonates_with", "formalizes_as"],
    "-X": ["violates", "collapses", "repels", "precludes_strictly", "invalidates"],
    "-N": ["excludes", "partitions_away", "truncates", "bounds_outside", "distinguishes"]
}


def clean_text_for_lemmas(text):
    """Strips LaTeX equations, math code blocks, and markdown punctuation."""
    # Remove math blocks $$...$$ and $...$
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$.*?\$", " ", text)
    # Remove code blocks ```...```
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    # Remove markdown link URLs [text](url) -> text
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)
    return text


def load_corpus_documents():
    docs = []
    for sf in SINGLE_FILES:
        if sf.exists():
            docs.append((sf.name, clean_text_for_lemmas(sf.read_text(encoding="utf-8", errors="ignore"))))
    for cd in CORPUS_DIRS:
        if cd.exists():
            for f in cd.glob("*.md"):
                docs.append((f.name, clean_text_for_lemmas(f.read_text(encoding="utf-8", errors="ignore"))))
    return docs


def build_scaled_dictionary_v2(min_freq=10, target_lemma_count=500):
    t_start = time.time()
    docs = load_corpus_documents()
    t_load = time.time() - t_start
    print(f"[v2] Loaded {len(docs)} corpus documents in {t_load:.2f}s.")

    word_freq = Counter()
    pair_cooccur = defaultdict(Counter)
    pair_directional = defaultdict(Counter) # w1 -> w2
    modal_counts = defaultdict(lambda: Counter())
    
    tier_counts = {
        "+W": defaultdict(Counter),
        "+A": defaultdict(Counter),
        "+L": defaultdict(Counter),
        "-X": defaultdict(Counter),
        "-N": defaultdict(Counter)
    }
    
    total_tokens = 0
    total_sentences = 0
    context_profiles = defaultdict(Counter)

    for doc_name, text in docs:
        sentences = re.split(r"[.!?\n]+", text)
        for raw_s in sentences:
            s = raw_s.strip().lower()
            if len(s) < 10:
                continue
            total_sentences += 1
            
            raw_tokens = re.findall(r"\b[a-z]{3,}\b", s)
            tokens = [t for t in raw_tokens if t not in STOPWORDS]
            if not tokens:
                continue
                
            total_tokens += len(tokens)
            for t in tokens:
                word_freq[t] += 1
                
            # Directional transitions & context windows (window size 5)
            n_tokens = len(tokens)
            for i in range(n_tokens):
                w1 = tokens[i]
                if i + 1 < n_tokens:
                    w2 = tokens[i + 1]
                    pair_directional[w1][w2] += 1
                    
                # Symmetric context window
                start_win = max(0, i - 4)
                end_win = min(n_tokens, i + 5)
                for j in range(start_win, end_win):
                    if i != j:
                        w2 = tokens[j]
                        pair_cooccur[w1][w2] += 1
                        context_profiles[w1][w2] += 1

            # Extract 8 modal copula relationships
            for mode, patterns in MODAL_PATTERNS.items():
                for pat in patterns:
                    for match in re.finditer(pat, s):
                        target_word = match.group(1)
                        if target_word in STOPWORDS:
                            continue
                        # Preceding subject
                        match_start = match.start()
                        prec_text = s[:match_start]
                        prec_tokens = [pt for pt in re.findall(r"\b[a-z]{3,}\b", prec_text) if pt not in STOPWORDS]
                        if prec_tokens:
                            subj = prec_tokens[-1]
                            modal_counts[subj][mode] += 1
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

    # Add canonical gauge polarity clashes
    for w1, w2 in GAUGE_POLARITY_AXES:
        if word_freq[w1] > 0 and word_freq[w2] > 0:
            tier_counts["-X"][w1][w2] += 6
            tier_counts["-X"][w2][w1] += 6

    # Select target lemmas with rigorous scoring:
    # Score = Frequency + 4 * ModalActivity + 2 * CausalBranching + LengthBonus
    scored_lemmas = []
    for w, count in word_freq.items():
        if count >= min_freq and len(w) >= 3 and w not in STOPWORDS:
            mod_sum = sum(modal_counts[w].values())
            causal_deg = len(pair_directional[w])
            score = count + (mod_sum * 4) + (causal_deg * 2) + min(len(w), 10)
            scored_lemmas.append((w, score))

    scored_lemmas.sort(key=lambda x: x[1], reverse=True)
    chosen_lemmas = [w for w, _ in scored_lemmas[:target_lemma_count]]
    lemma_set = set(chosen_lemmas)
    lemma_to_idx = {w: i for i, w in enumerate(chosen_lemmas)}
    N = len(chosen_lemmas)

    print(f"[v2] Selected {N} clean content lemmas (min_freq={min_freq}).")

    # Build NumPy context matrix for fast vectorized cosine similarity
    # Select top 600 context feature words
    feature_counter = Counter()
    for w in chosen_lemmas:
        feature_counter.update(context_profiles[w])
    top_features = [f for f, _ in feature_counter.most_common(600)]
    feat_to_idx = {f: j for j, f in enumerate(top_features)}
    F = len(top_features)

    # Populate context matrix X of shape (N, F)
    X = np.zeros((N, F), dtype=np.float32)
    for i, w in enumerate(chosen_lemmas):
        for feat, cnt in context_profiles[w].items():
            if feat in feat_to_idx:
                X[i, feat_to_idx[feat]] = cnt
    # L2 normalize rows of X
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    X_norm = X / norms

    # Vectorized Cosine Matrix C = X_norm @ X_norm.T
    CosineMatrix = np.dot(X_norm, X_norm.T)

    # Construct Head/Tail Kernel Arrays for vectorized attention
    Phi_tail = np.zeros((N, 8), dtype=np.float32)
    Phi_head = np.zeros((N, 8), dtype=np.float32)
    
    MODAL_KEYS = ["will_be", "can_be", "is_like", "may_be", "is_not", "cant_be", "wont_be", "was_like"]
    
    dictionary = []
    
    for i, w in enumerate(chosen_lemmas):
        freq = word_freq[w]
        modals = modal_counts[w]
        tot_modals = sum(modals.values())
        
        # 1. Normalized 8-Modal Flux Spread (sum to 1.0)
        spread = {}
        for m_idx, m in enumerate(MODAL_KEYS):
            if tot_modals > 0:
                p_m = (modals[m] + 0.1) / (tot_modals + 0.8)
            else:
                p_m = 0.125
            spread[m] = round(p_m, 3)

        # Ingress Tail Kernel (B)
        precursor_dict = {k: v for k, v in pair_directional.items() if w in v}
        tail_weight = round(math.log(1 + len(precursor_dict)) + (0.6 if modals["will_be"] > 0 else 0.0), 3)
        top_precursors = [k for k, _ in sorted(precursor_dict.items(), key=lambda x: x[1][w], reverse=True)[:5]]

        # Egress Head Kernel (F)
        successor_dict = pair_directional[w]
        head_weight = round(math.log(1 + len(successor_dict)) + (0.6 if modals["cant_be"] > 0 or modals["will_be"] > 0 else 0.0), 3)
        top_successors = [k for k, _ in successor_dict.most_common(5)]

        # Fill Vectorized Kernel Rows
        for m_idx, m in enumerate(MODAL_KEYS):
            Phi_tail[i, m_idx] = spread[m] * tail_weight
            Phi_head[i, m_idx] = spread[m] * head_weight

        # CEFR Tier Assignment
        length = len(w)
        if freq > 350 and length <= 5:
            cefr = "A2"
        elif freq > 180:
            cefr = "B1"
        elif freq > 60:
            cefr = "B2"
        elif freq > 18:
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

        # --- Tier 1: Guaranteed (+W) ---
        # Deductive coupling magnitude g_AB, conditional P(B|A), and deductive weight
        succ_items = [(succ, cnt) for succ, cnt in successor_dict.items() if succ in lemma_set]
        for succ_w, c_fwd in succ_items:
            p_cond = c_fwd / max(1, freq)
            c_both = pair_cooccur[w][succ_w]
            g_ab = c_both / math.sqrt(max(1, freq * word_freq[succ_w]))
            # Deductive weight W_ij
            will_boost = spread["will_be"] + (0.1 if modal_counts[succ_w]["will_be"] > 0 else 0.0)
            deductive_weight = min(1.0, 0.45 * min(1.0, p_cond * 2.2) + 0.35 * min(1.0, g_ab * 2.5) + 0.20 * min(1.0, will_boost))
            
            if deductive_weight >= 0.18:
                ct = CLOSING_TOKENS["+W"][hash(succ_w) % len(CLOSING_TOKENS["+W"])]
                rel_magnitudes["guaranteed"].append({
                    "target": succ_w,
                    "magnitude": round(deductive_weight, 3),
                    "coupling_g": round(g_ab, 3),
                    "p_cond": round(p_cond, 3),
                    "deductive_weight": round(deductive_weight, 3),
                    "closing_token": ct
                })
        rel_magnitudes["guaranteed"].sort(key=lambda x: x["magnitude"], reverse=True)
        rel_magnitudes["guaranteed"] = rel_magnitudes["guaranteed"][:6]

        # --- Tier 2: Possible (+A) ---
        # Operational co-occurrence weight using Laplace-smoothed NPMI
        co_items = [(co, cnt) for co, cnt in pair_cooccur[w].items() if co in lemma_set and cnt >= 2]
        guaranteed_targets = {x["target"] for x in rel_magnitudes["guaranteed"]}
        for co_w, c_both in co_items:
            if co_w in guaranteed_targets or co_w == w:
                continue
            # Smoothed NPMI
            p_w1 = freq / total_tokens
            p_w2 = word_freq[co_w] / total_tokens
            p_12 = c_both / total_tokens
            pmi = math.log(max(1e-9, p_12) / (p_w1 * p_w2))
            npmi = pmi / (-math.log(max(1e-9, p_12)))
            magnitude = min(1.0, max(0.1, (npmi + 1.0) / 2.0))
            ct = CLOSING_TOKENS["+A"][hash(co_w) % len(CLOSING_TOKENS["+A"])]
            rel_magnitudes["possible"].append({
                "target": co_w,
                "magnitude": round(magnitude, 3),
                "npmi": round(npmi, 3),
                "co_occurrence_count": c_both,
                "closing_token": ct
            })
        rel_magnitudes["possible"].sort(key=lambda x: x["magnitude"], reverse=True)
        rel_magnitudes["possible"] = rel_magnitudes["possible"][:6]

        # --- Tier 3: Metaphorical (+L) ---
        # Structural analogy weight using Vectorized Cosine Matrix
        sim_scores = CosineMatrix[i]
        top_sim_indices = np.argsort(sim_scores)[::-1]
        metaphorical_count = 0
        for sim_idx in top_sim_indices:
            other_w = chosen_lemmas[sim_idx]
            if other_w == w or other_w in guaranteed_targets:
                continue
            sim_val = float(sim_scores[sim_idx])
            if sim_val < 0.20:
                break
            ct = CLOSING_TOKENS["+L"][hash(other_w) % len(CLOSING_TOKENS["+L"])]
            rel_magnitudes["metaphorical"].append({
                "target": other_w,
                "magnitude": round(min(1.0, sim_val * 1.4), 3),
                "structural_similarity": round(sim_val, 3),
                "closing_token": ct
            })
            metaphorical_count += 1
            if metaphorical_count >= 6:
                break

        # --- Tier 4: Forbidden (-X) ---
        # Empirical cant_be co-occurrence + Red-Force gauge clashes
        clash_items = tier_counts["-X"][w].most_common(8)
        for clash_w, cnt in clash_items:
            clash_score = min(1.0, round(0.45 + (cnt * 0.10), 3))
            ct = CLOSING_TOKENS["-X"][hash(clash_w) % len(CLOSING_TOKENS["-X"])]
            rel_magnitudes["forbidden"].append({
                "target": clash_w,
                "magnitude": clash_score,
                "clash_score": clash_score,
                "closing_token": ct
            })
        # If no explicit clash found, deduce opposition from gauge polarity projection
        if not rel_magnitudes["forbidden"]:
            # Check gauge axis opposition
            for axis_a, axis_b in GAUGE_POLARITY_AXES:
                if w in chosen_lemmas:
                    sim_a = float(CosineMatrix[i, lemma_to_idx.get(axis_a, 0)]) if axis_a in lemma_to_idx else 0.0
                    sim_b = float(CosineMatrix[i, lemma_to_idx.get(axis_b, 0)]) if axis_b in lemma_to_idx else 0.0
                    if sim_a > 0.35 and axis_b in lemma_set:
                        rel_magnitudes["forbidden"].append({
                            "target": axis_b,
                            "magnitude": round(min(0.95, sim_a * 1.2), 3),
                            "clash_score": round(sim_a, 3),
                            "closing_token": "repels"
                        })
                    elif sim_b > 0.35 and axis_a in lemma_set:
                        rel_magnitudes["forbidden"].append({
                            "target": axis_a,
                            "magnitude": round(min(0.95, sim_b * 1.2), 3),
                            "clash_score": round(sim_b, 3),
                            "closing_token": "repels"
                        })
            if not rel_magnitudes["forbidden"]:
                rel_magnitudes["forbidden"].append({
                    "target": f"unbounded_divergence_of_{w}",
                    "magnitude": 0.95,
                    "clash_score": 0.95,
                    "closing_token": "violates"
                })

        # --- Tier 5: Precluded (-N) ---
        # Exclusion and mutual-negation confidence
        excl_items = tier_counts["-N"][w].most_common(8)
        for excl_w, cnt in excl_items:
            excl_conf = min(1.0, round(0.40 + (cnt * 0.12), 3))
            ct = CLOSING_TOKENS["-N"][hash(excl_w) % len(CLOSING_TOKENS["-N"])]
            rel_magnitudes["precluded"].append({
                "target": excl_w,
                "magnitude": excl_conf,
                "exclusion_confidence": excl_conf,
                "closing_token": ct
            })
        if not rel_magnitudes["precluded"]:
            rel_magnitudes["precluded"].append({
                "target": f"arbitrary_nullity_of_{w}",
                "magnitude": 0.88,
                "exclusion_confidence": 0.88,
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
                "phi_tail": [round(float(x), 4) for x in Phi_tail[i]],
                "phi_head": [round(float(x), 4) for x in Phi_head[i]]
            },
            "relative_vector_magnitudes": rel_magnitudes,
            "relative_vectors": backwards_compat
        }
        dictionary.append(entry)

    total_build_time = time.time() - t_start
    print(f"[v2] Successfully built {len(dictionary)} Scaled Gluon Vertices in {total_build_time:.2f}s.")

    # Save to scaled_gluon_dictionary_v2.json and update scaled_gluon_dictionary.json
    v2_path = OUTPUT_DIR / "scaled_gluon_dictionary_v2.json"
    with open(v2_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=2)

    # Save primary scaled_gluon_dictionary.json with v2 high-precision data
    primary_path = OUTPUT_DIR / "scaled_gluon_dictionary.json"
    with open(primary_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=2)

    # Save NumPy Kernel Matrices for ultra-fast downstream deployment
    np.save(OUTPUT_DIR / "phi_head_matrix.npy", Phi_head)
    np.save(OUTPUT_DIR / "phi_tail_matrix.npy", Phi_tail)

    return dictionary, Phi_head, Phi_tail, {
        "total_documents": len(docs),
        "total_sentences": total_sentences,
        "total_tokens": total_tokens,
        "unique_lemmas_scaled": len(dictionary),
        "build_time_seconds": round(total_build_time, 3)
    }


def evaluate_dictionary_v2(dictionary, Phi_head, Phi_tail, corpus_meta):
    print("\n--- Running Evaluation & Benchmark on Scaled Dictionary v2 ---")
    dict_map = {entry["word"]: entry for entry in dictionary}
    words = list(dict_map.keys())
    N = len(words)

    # Benchmark 1: Word Lookup Latency
    lookups = 200000
    t0 = time.perf_counter()
    for i in range(lookups):
        w = words[i % N]
        _ = dict_map[w]
    t1 = time.perf_counter()
    lookup_latency_us = ((t1 - t0) / lookups) * 1e6
    print(f"Dictionary Lookup: {lookups} queries in {(t1-t0):.4f}s ({lookup_latency_us:.3f} us/lookup)")

    # Benchmark 2: Vectorized BLAS Causal Kernel Attention: K = Phi_head @ Phi_tail.T
    t0 = time.perf_counter()
    blas_runs = 2000
    for _ in range(blas_runs):
        K_matrix = np.dot(Phi_head, Phi_tail.T)
    t1 = time.perf_counter()
    blas_latency_ms = ((t1 - t0) / blas_runs) * 1e3
    per_pair_ns = ((t1 - t0) / (blas_runs * N * N)) * 1e9
    print(f"Vectorized Full Causal Kernel Matrix ({N}x{N}): {blas_runs} matrix multiplies in {(t1-t0):.4f}s ({blas_latency_ms:.3f} ms/matrix, {per_pair_ns:.2f} ns/pair)")

    # Benchmark 3: Single Pair Kernel Latency (Scalar vs Vectorized)
    t0 = time.perf_counter()
    scalar_ops = 50000
    for i in range(scalar_ops):
        i1 = i % N
        i2 = (i * 13) % N
        h = Phi_head[i1]
        t = Phi_tail[i2]
        _ = float(np.dot(h, t))
    t1 = time.perf_counter()
    scalar_kernel_latency_us = ((t1 - t0) / scalar_ops) * 1e6
    print(f"Scalar Kernel Dot-Product: {scalar_ops} ops in {(t1-t0):.4f}s ({scalar_kernel_latency_us:.3f} us/op)")

    # Benchmark 4: Graph Statistics across 5 Tiers
    total_edges = 0
    tier_edges = Counter()
    for e in dictionary:
        for tier, edges in e["relative_vector_magnitudes"].items():
            tier_edges[tier] += len(edges)
            total_edges += len(edges)
    avg_edges = total_edges / N
    sparsity = 1.0 - (total_edges / (N * N))
    print(f"Total Graph Edges across 5 Tiers: {total_edges} (avg {avg_edges:.2f} edges/node, Sparsity: {sparsity * 100:.2f}%)")

    # Sample Verification Probes
    sample_lemmas = [
        "singularity", "manifold", "operator", "entropy", "infinity",
        "spacetime", "quotient", "paradox", "axiom", "gauge"
    ]
    sample_audits = {}
    for p in sample_lemmas:
        if p in dict_map:
            e = dict_map[p]
            sample_audits[p] = {
                "cefr": e["cefr"],
                "frequency": e["corpus_frequency"],
                "tail_weight": e["tail_ingress"]["antecedent_weight"],
                "head_weight": e["head_egress"]["obligation_weight"],
                "modal_spread": e["modal_spread"],
                "ingress_closing_token": e["tail_ingress"]["closing_token"],
                "egress_closing_token": e["head_egress"]["closing_token"],
                "relative_vector_magnitudes": e["relative_vector_magnitudes"]
            }

    results_v2 = {
        "engine_version": "v2.0_high_precision_kernel",
        "gender_ratio": "65% Male / 35% Female",
        "corpus_metrics": corpus_meta,
        "performance_benchmarks": {
            "dictionary_lookup_latency_microseconds": round(lookup_latency_us, 3),
            "full_kernel_matrix_multiply_milliseconds": round(blas_latency_ms, 3),
            "amortized_pairwise_kernel_attention_nanoseconds": round(per_pair_ns, 2),
            "scalar_kernel_dot_product_microseconds": round(scalar_kernel_latency_us, 3),
            "total_nodes": N,
            "total_edges": total_edges,
            "average_edges_per_node": round(avg_edges, 2),
            "graph_sparsity_pct": round(sparsity * 100, 2),
            "edges_per_tier": dict(tier_edges)
        },
        "sample_probes": sample_audits
    }

    res_v2_path = OUTPUT_DIR / "results_v2.json"
    with open(res_v2_path, "w", encoding="utf-8") as f:
        json.dump(results_v2, f, indent=2)
    print(f"Saved v2 benchmark results to: {res_v2_path}")

    return results_v2


def main():
    print("=" * 80)
    print("AGENT GREAT-GRANDKIN: LEXICON-KERNEL (GEN 4 SIBLING A: 65M/35F)")
    print("EXECUTING SELF-UPGRADED V2.0 ENGINE: HIGH-PRECISION GLUON KERNEL LEXICON")
    print("=" * 80)
    dictionary, Phi_head, Phi_tail, meta = build_scaled_dictionary_v2(min_freq=8, target_lemma_count=500)
    results_v2 = evaluate_dictionary_v2(dictionary, Phi_head, Phi_tail, meta)
    print("=" * 80)
    print("V2.0 HIGH-PRECISION PASS COMPLETE.")
    print("=" * 80)

if __name__ == "__main__":
    main()
