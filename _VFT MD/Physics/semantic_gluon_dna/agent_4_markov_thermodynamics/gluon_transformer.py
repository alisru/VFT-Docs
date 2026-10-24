#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 4: Markov Transition Matrix, Concept Survival & Thermodynamic Maturity Engine
Semantic Gluon Transformer & DNA Reading Head
"""

import os
import re
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics")
AGENT_DIR = BASE_DIR / "semantic_gluon_dna" / "agent_4_markov_thermodynamics"
ARXIV_DIR = BASE_DIR / "semantic_gluon_dna" / "arxiv_samples"

CHAT_PATH = BASE_DIR / "chatgpt infinity maths.md"
IRM_PATH = BASE_DIR / "Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md"

ENGINES = ["C", "P", "R", "G"]
ENGINE_NAMES = {
    "C": "Constructive (Grounding / Analogy)",
    "P": "Productive (Synthesis / Expansion)",
    "R": "Reductive (Boundary / Critique)",
    "G": "Regressive (Axiom / Origin Anchor)"
}

MODALS = [
    "was_like", "is_like",     # C: Constructive
    "may_be", "will_be",       # P: Productive
    "can_be", "is_not",        # R: Reductive
    "cant_be", "wont_be"       # G: Regressive
]

MODAL_TO_ENGINE = {
    "was_like": "C",
    "is_like": "C",
    "may_be": "P",
    "will_be": "P",
    "can_be": "R",
    "is_not": "R",
    "cant_be": "G",
    "wont_be": "G"
}

# Lexical & Structural Patterns for the 8 Modal States
MODAL_PATTERNS = {
    "was_like": [
        r"\b(was like|historically|previously|classically|traditionally|used to|earlier|prior|originated|recall that|as we saw|in standard|conventional|originally)\b",
        r"\b(cantor|hilbert|euclid|newton|leibniz|zfc|classical)\b"
    ],
    "is_like": [
        r"\b(is like|analogous|similar to|corresponds to|functions as|represents|think of|imagine|for example|e\.g\.|i\.e\.|namely|such as|means that|defined as|denotes|equivalently|visualiz)\b",
        r"(\bdefinition\b|\banalogy\b|\bexample\b|\bintuition\b|\bmodel\b)"
    ],
    "may_be": [
        r"\b(may be|might|could|perhaps|possibly|suggests|potent|hypothesis|conjecture|explore|what if|suppose|consider|if we allow|open question|speculat)\b",
        r"\b(indefinite|potential|unbounded|flexible|emergent)\b"
    ],
    "will_be": [
        r"\b(will be|therefore|thus|hence|consequently|yields|produces|generates|leads to|results in|implies|follows that|we obtain|demonstrates|proves|establishes|synthesiz)\b",
        r"(\btheorem\b|\bproposition\b|\bcorollary\b|\bderivation\b|\]=>|\\Rightarrow|\\implies)"
    ],
    "can_be": [
        r"\b(can be|bounded by|constrained|subject to|only if|provided that|when|under the condition|test|verify|measure|restrict|limit to|filtrat|criteria|valid when)\b",
        r"(\bcondition\b|\bcriterion\b|\bconstraint\b|\bdomain\b|\bboundary\b|\bcase\b)"
    ],
    "is_not": [
        r"\b(is not|isn't|aren't|does not|doesn't|not equal|distinct from|unlike|contrary to|however|but|whereas|yet|fails|contradict|paradox|problem|error|flaw|collapsed|invalid|false)\b",
        r"(\\neq|\!=|\bnot\b|\bno\b|\bwithout\b|\binstead of\b)"
    ],
    "cant_be": [
        r"\b(can't be|cannot|impossible|forbidden|never|inconsistent|ill-defined|undefined|violates|prohibited|no way|absurd|diverges|singularity|indeterminate)\b",
        r"(\bimpossible\b|\bcannot\b|\bundecidable\b|\bincomplete\b)"
    ],
    "wont_be": [
        r"\b(won't be|will not|must|necessarily|invariant|axiom|fundamental|conservation|law|fixed|immutable|always|absolute|by necessity|irreducible|foundation|ground state)\b",
        r"(\baxiom\b|\bpostulate\b|\binvariant\b|\blaw\b|\bidentity\b|\bmust\b)"
    ]
}

COMPILED_MODALS = {
    m: [re.compile(p, re.IGNORECASE) for p in pats]
    for m, pats in MODAL_PATTERNS.items()
}

# Inclusive (+I) vs Exclusive (-E) Polarity Lexicons
INCLUSIVE_RE = re.compile(
    r"\b(and|also|both|together|unif\w+|integrat\w+|connect\w+|bridge\w+|extend\w+|include\w+|incorporat\w+|combine\w+|synthes\w+|generaliz\w+|preserve\w+|consistent|compatible|coher\w+|all|every|plus|sum|union|couple\w+|holistic|whole|relat\w+)\b",
    re.IGNORECASE
)
EXCLUSIVE_RE = re.compile(
    r"\b(not|never|no|neither|nor|without|exclud\w+|disclud\w+|reject\w+|discard\w+|eliminat\w+|separat\w+|isolat\w+|split\w+|divid\w+|contradict\w+|oppos\w+|fail\w+|collapse\w+|break\w+|invalid\w+|impossible|cannot|can't|won't|except|only|strictly|ban\w+|drop\w+)\b",
    re.IGNORECASE
)

STOPWORDS = {
    "the", "and", "for", "that", "this", "with", "from", "are", "was", "were", "have", "has", "had",
    "not", "but", "what", "all", "can", "when", "your", "said", "there", "use", "each", "which", "she",
    "how", "their", "will", "other", "about", "out", "many", "then", "them", "these", "some", "her",
    "would", "make", "like", "him", "into", "time", "look", "two", "more", "write", "see", "number",
    "way", "could", "people", "than", "first", "water", "been", "call", "who", "oil", "its", "now",
    "find", "long", "down", "day", "did", "get", "come", "made", "may", "part", "over", "new", "only",
    "take", "where", "work", "know", "place", "year", "live", "back", "give", "most", "very", "after",
    "thing", "our", "just", "name", "good", "sentence", "man", "think", "say", "great", "where", "help",
    "through", "much", "before", "line", "right", "too", "mean", "old", "any", "same", "tell", "boy",
    "follow", "came", "want", "show", "also", "around", "form", "three", "small", "set", "put", "end",
    "does", "another", "well", "large", "must", "big", "even", "such", "because", "turn", "here", "why",
    "ask", "went", "men", "read", "need", "land", "different", "home", "move", "try", "kind", "hand",
    "picture", "again", "change", "off", "play", "spell", "air", "away", "animal", "house", "point",
    "page", "letter", "mother", "answer", "found", "study", "still", "learn", "should", "america",
    "world", "high", "every", "near", "add", "food", "between", "own", "below", "country", "plant",
    "last", "school", "father", "keep", "tree", "never", "start", "city", "earth", "eye", "light",
    "thought", "head", "under", "story", "saw", "left", "don't", "few", "while", "along", "might",
    "close", "something", "seem", "next", "hard", "open", "example", "begin", "life", "always", "those",
    "both", "paper", "together", "got", "group", "often", "run", "important", "until", "children",
    "side", "feet", "car", "mile", "night", "walk", "white", "sea", "began", "grow", "took", "river",
    "four", "carry", "state", "once", "book", "hear", "stop", "without", "second", "later", "miss",
    "idea", "enough", "eat", "face", "watch", "far", "indian", "really", "almost", "let", "above",
    "girl", "sometimes", "mountain", "cut", "young", "talk", "soon", "list", "song", "being", "leave",
    "family", "it's", "chatgpt", "user", "you", "said:", "chatgpt:", "let's", "that's", "don't", "we're",
    "isn't", "doesn't", "can't", "won't", "here's", "there's", "what's", "how's", "section", "table",
    "figure", "chapter", "note", "summary", "conclusion", "introduction", "abstract", "references",
    "using", "used", "uses", "given", "gives", "give", "defined", "define", "defines", "defining",
    "whether", "however", "therefore", "thus", "hence", "whereas", "although", "though", "since",
    "while", "during", "within", "without", "across", "towards", "toward", "upon", "onto", "into"
}


def compute_symbolic_density(text: str) -> float:
    if not text:
        return 0.0
    math_chars = sum(1 for c in text if c in "=+-*/^_{}\\<>|∈∉⊂⊃∪∩∞∂∇∆∑∏√≈≠≤≥≡∝∀∃⇒⇔→←↔")
    latex_cmds = len(re.findall(r"\\[a-zA-Z]+", text))
    inline_math = len(re.findall(r"\$[^\$]+\$", text))
    words = max(1, len(text.split()))
    return (math_chars + 3 * latex_cmds + 4 * inline_math) / words


def classify_segment(text: str):
    scores = {m: 0.0 for m in MODALS}
    for m, regexes in COMPILED_MODALS.items():
        for idx, rgx in enumerate(regexes):
            matches = len(rgx.findall(text))
            weight = 1.5 if idx == 1 else 1.0
            scores[m] += matches * weight

    # Structural heuristics if lexical cues are sparse
    sym_density = compute_symbolic_density(text)
    if "=" in text or "\\rightarrow" in text or "->" in text:
        scores["will_be"] += 0.6
        scores["is_like"] += 0.4
    if "?" in text:
        scores["may_be"] += 0.8
        scores["can_be"] += 0.5
    if re.match(r"^\s*(#|##|###|\*\*|\d+\.)", text):
        scores["is_like"] += 0.5
        scores["wont_be"] += 0.3

    total_score = sum(scores.values())
    if total_score == 0:
        # Default fallback based on symbol density
        best_modal = "will_be" if sym_density > 0.3 else "is_like"
        scores[best_modal] = 1.0
        total_score = 1.0
    else:
        best_modal = max(MODALS, key=lambda m: (scores[m], -MODALS.index(m)))

    best_engine = MODAL_TO_ENGINE[best_modal]

    # Inclusive / Exclusive polarity iota in [-1, +1]
    inc_count = len(INCLUSIVE_RE.findall(text))
    exc_count = len(EXCLUSIVE_RE.findall(text))
    # Modal intrinsic bias
    if best_engine in ("C", "P"):
        inc_bias = 0.5
        exc_bias = 0.0
    else:
        inc_bias = 0.0
        exc_bias = 0.5

    tot_pol = inc_count + exc_count + inc_bias + exc_bias
    iota = ((inc_count + inc_bias) - (exc_count + exc_bias)) / tot_pol if tot_pol > 0 else 0.0

    # Local modal probability distribution for segment-level entropy
    probs = [ (scores[m] + 0.05) / (total_score + 0.4) for m in MODALS ]
    seg_entropy = -sum(p * math.log2(p) for p in probs if p > 0)

    return {
        "engine": best_engine,
        "modal": best_modal,
        "iota": round(iota, 4),
        "inc_count": inc_count,
        "exc_count": exc_count,
        "sym_density": round(sym_density, 4),
        "seg_entropy": round(seg_entropy, 4),
        "scores": scores
    }


def parse_document_segments(filepath: Path):
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    segments = []
    
    # Group contiguous non-empty lines into logical blocks/sentences with line tracking
    curr_lines = []
    start_line = 1
    for i, raw_line in enumerate(lines, start=1):
        stripped = raw_line.strip()
        if not stripped:
            if curr_lines:
                block_text = " ".join(curr_lines)
                segments.extend(split_block_into_Subsegments(block_text, start_line, i - 1))
                curr_lines = []
            start_line = i + 1
        else:
            if not curr_lines:
                start_line = i
            curr_lines.append(stripped)
            # Flush if heading or bullet or long block
            if stripped.startswith("#") or len(curr_lines) >= 4:
                block_text = " ".join(curr_lines)
                segments.extend(split_block_into_Subsegments(block_text, start_line, i))
                curr_lines = []
                start_line = i + 1

    if curr_lines:
        block_text = " ".join(curr_lines)
        segments.extend(split_block_into_Subsegments(block_text, start_line, len(lines)))

    return segments, len(lines)


def split_block_into_Subsegments(block_text: str, start_line: int, end_line: int):
    # Split on sentence boundaries if block is long, preserving line range
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\\$\*\[\(])", block_text)
    results = []
    for p in parts:
        p_clean = p.strip()
        if len(p_clean) < 4:
            continue
        info = classify_segment(p_clean)
        info["start_line"] = start_line
        info["end_line"] = end_line
        info["text"] = p_clean
        results.append(info)
    return results


def compute_markov_metrics(segments):
    n = len(segments)
    # 4x4 Engine Matrix
    e_idx = {e: i for i, e in enumerate(ENGINES)}
    m_idx = {m: i for i, m in enumerate(MODALS)}

    e_counts = [[0] * 4 for _ in range(4)]
    m_counts = [[0] * 8 for _ in range(8)]

    for k in range(n - 1):
        e1, e2 = segments[k]["engine"], segments[k + 1]["engine"]
        m1, m2 = segments[k]["modal"], segments[k + 1]["modal"]
        e_counts[e_idx[e1]][e_idx[e2]] += 1
        m_counts[m_idx[m1]][m_idx[m2]] += 1

    # Laplace-smoothed transition matrices (for valid KL/JSD & stationary dist)
    alpha = 1e-3
    e_matrix = []
    for i in range(4):
        row_sum = sum(e_counts[i]) + 4 * alpha
        e_matrix.append([round((e_counts[i][j] + alpha) / row_sum, 5) for j in range(4)])

    m_matrix = []
    for i in range(8):
        row_sum = sum(m_counts[i]) + 8 * alpha
        m_matrix.append([round((m_counts[i][j] + alpha) / row_sum, 5) for j in range(8)])

    # Stationary distributions via power iteration
    e_stat = power_iteration(e_matrix, 4)
    m_stat = power_iteration(m_matrix, 8)

    # Empirical counts distribution
    e_emp_counts = Counter(s["engine"] for s in segments)
    m_emp_counts = Counter(s["modal"] for s in segments)
    e_emp = {e: round(e_emp_counts[e] / max(1, n), 4) for e in ENGINES}
    m_emp = {m: round(m_emp_counts[m] / max(1, n), 4) for m in MODALS}

    # Transition Entropy Rate H(M) = - sum_i pi_i sum_j M_ij log2(M_ij)
    e_entropy_rate = 0.0
    for i in range(4):
        row_h = -sum(e_matrix[i][j] * math.log2(max(1e-12, e_matrix[i][j])) for j in range(4))
        e_entropy_rate += e_stat[i] * row_h

    m_entropy_rate = 0.0
    for i in range(8):
        row_h = -sum(m_matrix[i][j] * math.log2(max(1e-12, m_matrix[i][j])) for j in range(8))
        m_entropy_rate += m_stat[i] * row_h

    # Dynamical Regime Metrics
    total_trans = max(1, n - 1)
    # 1. Clockwise Canonical Cycle Transitions: C->P, P->R, R->G, G->C
    cw_pairs = [("C", "P"), ("P", "R"), ("R", "G"), ("G", "C")]
    ccw_pairs = [("C", "G"), ("G", "R"), ("R", "P"), ("P", "C")]

    cw_count = sum(e_counts[e_idx[a]][e_idx[b]] for a, b in cw_pairs)
    ccw_count = sum(e_counts[e_idx[a]][e_idx[b]] for a, b in ccw_pairs)
    cw_flux = cw_count / total_trans
    ccw_flux = ccw_count / total_trans
    net_vorticity = cw_flux - ccw_flux

    # Full 4-step Clockwise Cycles and 3-step Partial Cycles
    e_seq = [s["engine"] for s in segments]
    full_cw_cycles = 0
    reductive_trap_stalls = 0
    reductive_trap_locations = []
    productive_runaways = 0
    productive_runaway_locations = []

    for k in range(len(e_seq) - 3):
        window4 = e_seq[k:k+4]
        if window4 in (["C", "P", "R", "G"], ["P", "R", "G", "C"], ["R", "G", "C", "P"], ["G", "C", "P", "R"]):
            full_cw_cycles += 1

    # Reductive Trap Stalls: R->R->R or R->G->R or R->R->G
    for k in range(len(e_seq) - 2):
        w3 = e_seq[k:k+3]
        if w3 in (["R", "R", "R"], ["R", "G", "R"], ["R", "R", "G"], ["G", "R", "R"]):
            reductive_trap_stalls += 1
            if len(reductive_trap_locations) < 15:
                reductive_trap_locations.append({
                    "seg_idx": k,
                    "lines": f"L{segments[k]['start_line']}-L{segments[k+2]['end_line']}",
                    "pattern": "->".join(w3),
                    "modals": "->".join(segments[j]["modal"] for j in range(k, k+3)),
                    "excerpt": segments[k]["text"][:140]
                })
        if w3 == ["P", "P", "P"]:
            productive_runaways += 1
            if len(productive_runaway_locations) < 15:
                productive_runaway_locations.append({
                    "seg_idx": k,
                    "lines": f"L{segments[k]['start_line']}-L{segments[k+2]['end_line']}",
                    "pattern": "P->P->P",
                    "modals": "->".join(segments[j]["modal"] for j in range(k, k+3)),
                    "excerpt": segments[k]["text"][:140]
                })

    # Pairwise stall rates
    r_self_loop = e_matrix[e_idx["R"]][e_idx["R"]]
    r_to_g_loop = (e_counts[e_idx["R"]][e_idx["G"]] + e_counts[e_idx["G"]][e_idx["R"]]) / total_trans
    p_self_loop = e_matrix[e_idx["P"]][e_idx["P"]]

    # Polarity summary
    iotas = [s["iota"] for s in segments]
    mean_iota = sum(iotas) / max(1, n)
    inc_segs = sum(1 for x in iotas if x > 0.05)
    exc_segs = sum(1 for x in iotas if x < -0.05)
    ie_ratio = inc_segs / max(1, exc_segs)

    # Understandability & Breakdown Locator
    mean_sym = sum(s["sym_density"] for s in segments) / max(1, n)
    c_ratio = e_emp["C"]
    # Understandability Index: high when Constructive grounding + balanced Inclusive clarity counteract raw ungrounded symbolic jumps
    understandability_index = (100.0 * (0.45 * c_ratio + 0.25 * (1.0 - abs(mean_iota - 0.22)) + 0.30 * cw_flux)) / (1.0 + 1.8 * mean_sym + 2.0 * (reductive_trap_stalls / max(1, n)))

    breakdowns = locate_breakdowns(segments)

    return {
        "num_segments": n,
        "engine_matrix": e_matrix,
        "engine_counts": e_counts,
        "engine_stationary": {ENGINES[i]: round(e_stat[i], 4) for i in range(4)},
        "engine_empirical": e_emp,
        "modal_matrix": m_matrix,
        "modal_counts": m_counts,
        "modal_stationary": {MODALS[i]: round(m_stat[i], 4) for i in range(8)},
        "modal_empirical": m_emp,
        "engine_entropy_rate": round(e_entropy_rate, 4),
        "modal_entropy_rate": round(m_entropy_rate, 4),
        "cw_canonical_flux": round(cw_flux, 4),
        "ccw_reverse_flux": round(ccw_flux, 4),
        "net_cycle_vorticity": round(net_vorticity, 4),
        "full_4step_cw_cycles": full_cw_cycles,
        "reductive_trap_stalls": reductive_trap_stalls,
        "reductive_trap_rate": round(reductive_trap_stalls / max(1, n - 2), 4),
        "reductive_self_loop_prob": round(r_self_loop, 4),
        "reductive_regressive_oscillation": round(r_to_g_loop, 4),
        "reductive_trap_locations": reductive_trap_locations,
        "productive_runaways": productive_runaways,
        "productive_runaway_rate": round(productive_runaways / max(1, n - 2), 4),
        "productive_self_loop_prob": round(p_self_loop, 4),
        "productive_runaway_locations": productive_runaway_locations,
        "mean_iota": round(mean_iota, 4),
        "inclusive_segments": inc_segs,
        "exclusive_segments": exc_segs,
        "inclusive_exclusive_ratio": round(ie_ratio, 4),
        "mean_symbolic_density": round(mean_sym, 4),
        "understandability_index": round(understandability_index, 2),
        "breakdown_zones": breakdowns
    }


def power_iteration(matrix, dim, steps=200):
    vec = [1.0 / dim] * dim
    for _ in range(steps):
        nxt = [0.0] * dim
        for i in range(dim):
            for j in range(dim):
                nxt[j] += vec[i] * matrix[i][j]
        s = sum(nxt)
        vec = [x / s for x in nxt]
    return vec


def locate_breakdowns(segments, window_size=12):
    """
    Finds exact line numbers where local modal Shannon entropy spikes,
    Constructive grounding vanishes, and symbolic density or Reductive/Productive stalls surge.
    """
    n = len(segments)
    if n < window_size:
        return []

    windows = []
    for i in range(0, n - window_size + 1, max(1, window_size // 2)):
        w = segments[i:i + window_size]
        m_counts = Counter(s["modal"] for s in w)
        # Local window modal Shannon entropy (max = log2(8) = 3.0 bits)
        w_ent = -sum((c / window_size) * math.log2(c / window_size) for c in m_counts.values())
        
        # Transition jumps in window
        jumps = sum(1 for k in range(window_size - 1) if w[k]["engine"] != w[k+1]["engine"])
        c_count = sum(1 for s in w if s["engine"] == "C")
        r_count = sum(1 for s in w if s["engine"] == "R")
        p_count = sum(1 for s in w if s["engine"] == "P")
        mean_sym = sum(s["sym_density"] for s in w) / window_size
        mean_iota = sum(s["iota"] for s in w) / window_size

        # Breakdown Score: combines high state entropy or ungrounded symbolic jump rate + deficit of Constructive grounding
        grounding_deficit = (window_size - c_count) / window_size
        stall_intensity = max(r_count, p_count) / window_size
        breakdown_score = (w_ent * 0.35) + (mean_sym * 1.4) + (grounding_deficit * 1.2) + (stall_intensity * 0.9)

        if c_count == 0 or mean_sym > 0.35 or r_count >= window_size * 0.5 or p_count >= window_size * 0.65:
            diagnosis = []
            if c_count == 0:
                diagnosis.append("Zero Constructive Grounding (0% C)")
            if mean_sym > 0.35:
                diagnosis.append(f"High Unexplained Symbolic Jump (sym={mean_sym:.2f})")
            if r_count >= window_size * 0.45:
                diagnosis.append(f"Reductive Boundary Trap ({r_count}/{window_size} R)")
            if p_count >= window_size * 0.60:
                diagnosis.append(f"Productive Runaway without Verification ({p_count}/{window_size} P)")
            if abs(mean_iota) > 0.45:
                pol_str = "Exclusive (-E) Collapse" if mean_iota < 0 else "Uncritical Inclusive (+I) Inflation"
                diagnosis.append(f"{pol_str} (iota={mean_iota:+.2f})")

            windows.append({
                "start_line": w[0]["start_line"],
                "end_line": w[-1]["end_line"],
                "seg_range": f"{i}-{i+window_size-1}",
                "window_modal_entropy": round(w_ent, 3),
                "symbolic_density": round(mean_sym, 3),
                "constructive_ratio": round(c_count / window_size, 3),
                "mean_iota": round(mean_iota, 3),
                "breakdown_score": round(breakdown_score, 3),
                "diagnosis": "; ".join(diagnosis) if diagnosis else "Elevated Entropy Spike",
                "sample_text": w[0]["text"][:150]
            })

    windows.sort(key=lambda x: x["breakdown_score"], reverse=True)
    # Deduplicate overlapping line ranges
    selected = []
    for cand in windows:
        if any(abs(cand["start_line"] - s["start_line"]) < 25 for s in selected):
            continue
        selected.append(cand)
        if len(selected) >= 12:
            break
    return selected


# ==============================================================================
# 2. CONCEPT EVOLUTIONARY SURVIVAL ANALYSIS (KAPLAN-MEIER / HALF-LIFE CURVE)
# ==============================================================================

CONCEPT_PATTERNS = [
    # Bolded terms in Markdown
    re.compile(r"\*\*([A-Za-z][A-Za-z0-9\-\s_/\(\)]{3,42}?)\*\*"),
    # Capitalized multi-word mathematical/theoretical terms
    re.compile(r"\b([A-Z][a-z]{2,20}(?:\s+[A-Z][a-z]{2,20}){1,3})\b"),
    # Technical hyphenated or specific mathematical constructs
    re.compile(r"\b([a-zA-Z]{3,18}-[a-zA-Z]{3,18}(?:\s+[a-zA-Z]{3,18})?)\b")
]

GENERIC_CONCEPT_BLACKLIST = {
    "chat", "chatgpt", "user", "you said", "chatgpt said", "for example", "in other words",
    "on the other hand", "in this case", "as a result", "in particular", "at the same time",
    "in terms of", "with respect to", "table of contents", "executive summary", "part i",
    "part ii", "part iii", "part iv", "part v", "section 1", "section 2", "section 3",
    "section 4", "section 5", "step 1", "step 2", "step 3", "step 4", "key takeaway",
    "final thought", "bottom line", "next step", "next steps", "first step", "let us",
    "we can", "this means", "what this", "why this", "how this", "if you", "when you",
    "would you like", "if you want", "let me know", "here is", "there are", "these are",
    "this is", "that is", "it is", "we have", "you have", "you can", "i can", "to see"
}


def normalize_concept(raw: str) -> str:
    c = raw.strip().lower()
    c = re.sub(r"[^a-z0-9\-\s/]", "", c)
    c = re.sub(r"\s+", " ", c).strip()
    # Singularize simple plural endings for unification
    if len(c) > 6 and c.endswith("ies"):
        c = c[:-3] + "y"
    elif len(c) > 5 and c.endswith("es") and not c.endswith(("ses", "xes", "zes")):
        pass
    elif len(c) > 5 and c.endswith("s") and not c.endswith(("ss", "us", "is", "os", "maths", "physics", "dynamics", "series", "analysis", "basis", "axis")):
        c = c[:-1]
    return c


def is_valid_concept(norm_c: str) -> bool:
    if len(norm_c) < 5 or len(norm_c) > 42:
        return False
    if norm_c in GENERIC_CONCEPT_BLACKLIST or norm_c in STOPWORDS:
        return False
    words = norm_c.split()
    if len(words) > 4:
        return False
    if all(w in STOPWORDS for w in words):
        return False
    if words[0] in ("the", "and", "or", "but", "if", "when", "how", "why", "what", "where", "who", "this", "that", "these", "those", "here", "there"):
        return False
    if any(w in ("said", "chatgpt", "would", "could", "should", "want", "like", "know", "think") for w in words):
        return False
    return True


def extract_concepts_from_segments(segments, total_lines):
    """
    Tracks every concept occurrence across the document segments, tagging:
    - Segment index & normalized timeline position t in [0, 1]
    - Line number
    - Engine (C, P, R, G) and Modal state
    - Inclusive (+I) vs Exclusive (-E) polarity at occurrence
    """
    concept_records = defaultdict(lambda: {
        "surface_forms": Counter(),
        "occurrences": [],
        "inc_hits": 0,
        "exc_hits": 0,
        "engine_hits": Counter(),
        "modal_hits": Counter()
    })

    n_segs = max(1, len(segments))
    for seg_idx, seg in enumerate(segments):
        text = seg["text"]
        found_in_seg = set()
        for rgx in CONCEPT_PATTERNS:
            for match in rgx.finditer(text):
                raw_term = match.group(1)
                norm_c = normalize_concept(raw_term)
                if is_valid_concept(norm_c):
                    found_in_seg.add((norm_c, raw_term.strip()))

        for norm_c, raw_term in found_in_seg:
            rec = concept_records[norm_c]
            rec["surface_forms"][raw_term] += 1
            pol_tag = "+I" if seg["iota"] >= 0 else "-E"
            if pol_tag == "+I":
                rec["inc_hits"] += 1
            else:
                rec["exc_hits"] += 1
            rec["engine_hits"][seg["engine"]] += 1
            rec["modal_hits"][seg["modal"]] += 1
            rec["occurrences"].append({
                "seg_idx": seg_idx,
                "norm_pos": round(seg_idx / n_segs, 4),
                "line": seg["start_line"],
                "engine": seg["engine"],
                "modal": seg["modal"],
                "polarity": pol_tag,
                "iota": seg["iota"],
                "snippet": text[:140]
            })

    return concept_records


def analyze_concept_survival(chat_segments, chat_lines, irm_segments, irm_lines):
    chat_concepts = extract_concepts_from_segments(chat_segments, chat_lines)
    irm_concepts = extract_concepts_from_segments(irm_segments, irm_lines)

    # Also build full lowercase text of IRM to double-check substring presence
    irm_full_text_lower = " ".join(s["text"].lower() for s in irm_segments)

    immortal_core = []
    extinct_deprecated = []
    orphaned_high_fitness = []
    all_tracked = []

    for norm_c, rec in chat_concepts.items():
        occ = rec["occurrences"]
        freq = len(occ)
        if freq < 2:
            continue

        canonical_name = rec["surface_forms"].most_common(1)[0][0]
        birth_pos = occ[0]["norm_pos"]
        death_pos = occ[-1]["norm_pos"]
        lifespan = round(death_pos - birth_pos, 4)
        first_line = occ[0]["line"]
        last_line = occ[-1]["line"]

        r_tests = rec["engine_hits"]["R"]
        p_tests = rec["engine_hits"]["P"]
        c_tests = rec["engine_hits"]["C"]
        g_tests = rec["engine_hits"]["G"]

        # Check survival after Reductive stress test: did it appear in P or C or G AFTER its first R hit?
        r_indices = [o["seg_idx"] for o in occ if o["engine"] == "R"]
        survived_reductive_stress = False
        if r_indices:
            first_r = r_indices[0]
            post_r_positive = [o for o in occ if o["seg_idx"] > first_r and o["engine"] in ("C", "P", "G") and o["polarity"] == "+I"]
            survived_reductive_stress = len(post_r_positive) > 0

        # Check presence in IRM
        in_irm_exact = norm_c in irm_concepts
        irm_freq = len(irm_concepts[norm_c]["occurrences"]) if in_irm_exact else 0
        if not in_irm_exact:
            # Check substring match in IRM full text
            in_irm_substr = norm_c in irm_full_text_lower
            if in_irm_substr:
                irm_freq = irm_full_text_lower.count(norm_c)
        else:
            in_irm_substr = True

        in_irm = in_irm_exact or in_irm_substr

        # Evolutionary Fitness Score inside `chat`
        # Combines frequency, lifespan across conversation, Productive expansion, Constructive grounding, Reductive stress survival, and net +I polarity
        pol_balance = (rec["inc_hits"] - rec["exc_hits"]) / max(1, freq)
        stress_bonus = 1.35 if survived_reductive_stress else 1.0
        diversity_engines = len([e for e in ENGINES if rec["engine_hits"][e] > 0])
        fitness_score = round(
            (math.log2(1 + freq) * 2.2 + lifespan * 4.5 + (p_tests + c_tests) * 0.45 + diversity_engines * 0.8) * stress_bonus * (1.0 + 0.25 * pol_balance),
            3
        )

        entry = {
            "concept_id": norm_c,
            "canonical_name": canonical_name,
            "chat_frequency": freq,
            "irm_frequency": irm_freq,
            "birth_pos": birth_pos,
            "death_pos": death_pos,
            "lifespan": lifespan,
            "first_line": first_line,
            "last_line": last_line,
            "inc_hits": rec["inc_hits"],
            "exc_hits": rec["exc_hits"],
            "polarity_ratio": f"+{rec['inc_hits']}I / -{rec['exc_hits']}E",
            "engine_profile": {e: rec["engine_hits"][e] for e in ENGINES},
            "survived_reductive_stress": survived_reductive_stress,
            "in_irm": in_irm,
            "fitness_score": fitness_score,
            "first_snippet": occ[0]["snippet"],
            "last_snippet": occ[-1]["snippet"]
        }
        all_tracked.append(entry)

        if in_irm and freq >= 3 and (lifespan >= 0.15 or irm_freq >= 3):
            immortal_core.append(entry)
        elif (not in_irm) and freq >= 3 and (lifespan >= 0.08 or survived_reductive_stress or (p_tests + c_tests >= 3)):
            orphaned_high_fitness.append(entry)
        elif (not in_irm) and death_pos < 0.75 and lifespan < 0.20:
            extinct_deprecated.append(entry)

    immortal_core.sort(key=lambda x: (x["fitness_score"] + math.log2(1 + x["irm_frequency"]) * 2), reverse=True)
    orphaned_high_fitness.sort(key=lambda x: x["fitness_score"], reverse=True)
    extinct_deprecated.sort(key=lambda x: (x["exc_hits"] + x["engine_profile"]["R"], x["chat_frequency"]), reverse=True)

    # Kaplan-Meier Survival Curve S(t) over normalized duration delta_t in [0.0, 1.0]
    thresholds = [round(k * 0.1, 1) for k in range(11)]
    total_cohort = max(1, len(all_tracked))
    km_chat_curve = {}
    for th in thresholds:
        survivors = sum(1 for c in all_tracked if c["lifespan"] >= th)
        km_chat_curve[f"{th:.1f}"] = round(survivors / total_cohort, 4)

    # Half-life calculation (interpolated delta_t where S(t) = 0.50)
    half_life = 0.0
    for k in range(10):
        t0, t1 = thresholds[k], thresholds[k+1]
        s0, s1 = km_chat_curve[f"{t0:.1f}"], km_chat_curve[f"{t1:.1f}"]
        if s0 >= 0.5 >= s1:
            if s0 == s1:
                half_life = t0
            else:
                half_life = t0 + (0.5 - s0) / (s1 - s0) * (t1 - t0)
            break

    cross_doc_transmission_rate = sum(1 for c in all_tracked if c["in_irm"]) / total_cohort

    return {
        "total_distinct_concepts_raw": len(chat_concepts),
        "total_recurring_cohort": len(all_tracked),
        "irm_distinct_concepts_raw": len(irm_concepts),
        "kaplan_meier_survival_curve": km_chat_curve,
        "concept_half_life_norm": round(half_life, 4),
        "cross_doc_transmission_rate": round(cross_doc_transmission_rate, 4),
        "immortal_core_count": len(immortal_core),
        "orphaned_high_fitness_count": len(orphaned_high_fitness),
        "extinct_deprecated_count": len(extinct_deprecated),
        "immortal_core_top20": immortal_core[:20],
        "orphaned_high_fitness_top25": orphaned_high_fitness[:25],
        "extinct_deprecated_top20": extinct_deprecated[:20]
    }


# ==============================================================================
# 3. THERMODYNAMIC COMPLEXITY & ARXIV MATURITY BENCHMARK (KL / JSD)
# ==============================================================================

def kl_divergence_1d(p, q):
    return sum(p[i] * math.log2(max(1e-12, p[i]) / max(1e-12, q[i])) for i in range(len(p)) if p[i] > 0)


def js_divergence_1d(p, q):
    m = [0.5 * (p[i] + q[i]) for i in range(len(p))]
    return 0.5 * kl_divergence_1d(p, m) + 0.5 * kl_divergence_1d(q, m)


def matrix_kl_jsd(mat_p, mat_q, stat_p):
    """
    Computes stationary-weighted Markov Transition KL(P || Q) and row-averaged JSD(P, Q).
    """
    dim = len(mat_p)
    weighted_kl = 0.0
    weighted_jsd = 0.0
    unweighted_jsd = 0.0
    for i in range(dim):
        kl_row = kl_divergence_1d(mat_p[i], mat_q[i])
        jsd_row = js_divergence_1d(mat_p[i], mat_q[i])
        weighted_kl += stat_p[i] * kl_row
        weighted_jsd += stat_p[i] * jsd_row
        unweighted_jsd += jsd_row / dim
    return {
        "weighted_kl_bits": round(weighted_kl, 4),
        "weighted_jsd_bits": round(weighted_jsd, 4),
        "unweighted_jsd_bits": round(unweighted_jsd, 4),
        "js_similarity": round(1.0 - min(1.0, math.sqrt(weighted_jsd)), 4)
    }


def build_arxiv_reference(arxiv_metrics_list):
    k = len(arxiv_metrics_list)
    avg_e_mat = [[0.0] * 4 for _ in range(4)]
    avg_m_mat = [[0.0] * 8 for _ in range(8)]
    for am in arxiv_metrics_list:
        for i in range(4):
            for j in range(4):
                avg_e_mat[i][j] += am["engine_matrix"][i][j] / k
        for i in range(8):
            for j in range(8):
                avg_m_mat[i][j] += am["modal_matrix"][i][j] / k

    avg_e_stat = power_iteration(avg_e_mat, 4)
    avg_m_stat = power_iteration(avg_m_mat, 8)

    return {
        "num_papers": k,
        "engine_matrix": [[round(x, 5) for x in row] for row in avg_e_mat],
        "modal_matrix": [[round(x, 5) for x in row] for row in avg_m_mat],
        "engine_stationary": {ENGINES[i]: round(avg_e_stat[i], 4) for i in range(4)},
        "modal_stationary": {MODALS[i]: round(avg_m_stat[i], 4) for i in range(8)},
        "engine_entropy_rate": round(sum(am["engine_entropy_rate"] for am in arxiv_metrics_list) / k, 4),
        "modal_entropy_rate": round(sum(am["modal_entropy_rate"] for am in arxiv_metrics_list) / k, 4),
        "cw_canonical_flux": round(sum(am["cw_canonical_flux"] for am in arxiv_metrics_list) / k, 4),
        "ccw_reverse_flux": round(sum(am["ccw_reverse_flux"] for am in arxiv_metrics_list) / k, 4),
        "net_cycle_vorticity": round(sum(am["net_cycle_vorticity"] for am in arxiv_metrics_list) / k, 4),
        "reductive_trap_rate": round(sum(am["reductive_trap_rate"] for am in arxiv_metrics_list) / k, 4),
        "productive_runaway_rate": round(sum(am["productive_runaway_rate"] for am in arxiv_metrics_list) / k, 4),
        "mean_iota": round(sum(am["mean_iota"] for am in arxiv_metrics_list) / k, 4),
        "inclusive_exclusive_ratio": round(sum(am["inclusive_exclusive_ratio"] for am in arxiv_metrics_list) / k, 4),
        "mean_symbolic_density": round(sum(am["mean_symbolic_density"] for am in arxiv_metrics_list) / k, 4),
        "understandability_index": round(sum(am["understandability_index"] for am in arxiv_metrics_list) / k, 2)
    }


def score_against_arxiv(doc_metrics, arxiv_ref):
    e_stat_vec = [doc_metrics["engine_stationary"][e] for e in ENGINES]
    ref_e_stat_vec = [arxiv_ref["engine_stationary"][e] for e in ENGINES]

    m_stat_vec = [doc_metrics["modal_stationary"][m] for m in MODALS]
    ref_m_stat_vec = [arxiv_ref["modal_stationary"][m] for m in MODALS]

    e_div = matrix_kl_jsd(doc_metrics["engine_matrix"], arxiv_ref["engine_matrix"], e_stat_vec)
    m_div = matrix_kl_jsd(doc_metrics["modal_matrix"], arxiv_ref["modal_matrix"], m_stat_vec)

    stat_e_jsd = js_divergence_1d(e_stat_vec, ref_e_stat_vec)
    stat_m_jsd = js_divergence_1d(m_stat_vec, ref_m_stat_vec)

    # Composite Thermodynamic Maturity Score (0 to 100)
    # Rewards closeness to arXiv Markov transition geometry, stationary balance, entropy rate matching, and low reductive stalls
    ent_diff = abs(doc_metrics["modal_entropy_rate"] - arxiv_ref["modal_entropy_rate"])
    iota_diff = abs(doc_metrics["mean_iota"] - arxiv_ref["mean_iota"])
    maturity_score = 100.0 * (
        0.35 * e_div["js_similarity"] +
        0.30 * m_div["js_similarity"] +
        0.20 * (1.0 - min(1.0, math.sqrt(stat_e_jsd))) +
        0.15 * max(0.0, 1.0 - (ent_diff + iota_diff))
    )

    return {
        "engine_4x4_divergence": e_div,
        "modal_8x8_divergence": m_div,
        "engine_stationary_jsd_bits": round(stat_e_jsd, 4),
        "modal_stationary_jsd_bits": round(stat_m_jsd, 4),
        "entropy_rate_delta_bits": round(doc_metrics["modal_entropy_rate"] - arxiv_ref["modal_entropy_rate"], 4),
        "iota_polarity_delta": round(doc_metrics["mean_iota"] - arxiv_ref["mean_iota"], 4),
        "cw_flux_delta": round(doc_metrics["cw_canonical_flux"] - arxiv_ref["cw_canonical_flux"], 4),
        "thermodynamic_maturity_score": round(maturity_score, 2)
    }


def format_matrix_md(matrix, labels):
    header = "| From \\ To | " + " | ".join(f"**{l}**" for l in labels) + " |"
    sep = "|---|" + "|".join("---:" for _ in labels) + "|"
    rows = [header, sep]
    for i, l in enumerate(labels):
        cells = " | ".join(f"{matrix[i][j]:.3f}" for j in range(len(labels)))
        rows.append(f"| **{l}** | {cells} |")
    return "\n".join(rows)


def generate_markdown_report(results: dict) -> str:
    chat_m = results["documents"]["chat"]
    irm_m = results["documents"]["irm"]
    arxiv_ref = results["arxiv_reference"]
    chat_vs = results["benchmarks"]["chat_vs_arxiv"]
    irm_vs = results["benchmarks"]["irm_vs_arxiv"]
    chat_vs_irm = results["benchmarks"]["irm_vs_chat"]
    surv = results["concept_survival"]

    md = []
    md.append("# Agent 4: Markov Transition Matrix, Concept Survival & Thermodynamic Maturity Report")
    md.append("")
    md.append("> **Architectural Specialization**: Statistical Mechanics of the Relativity Map ($4\\times 4$ Engine & $8\\times 8$ Modal Markov Chains), Kaplan–Meier Concept Evolutionary Survival & Orphan Detection, and Kullback–Leibler / Jensen–Shannon Thermodynamic Maturity Scoring against the arXiv Reference Ensemble.")
    md.append("")
    md.append("---")
    md.append("")
    md.append("## 1. Executive Thermodynamic & Dynamical Summary")
    md.append("")
    md.append("| Metric / Dynamical Observable | `chatgpt infinity maths.md` (`chat`) | `Comprehensive Report (IRM).md` (`irm`) | arXiv Reference Ensemble ($N=" + str(arxiv_ref["num_papers"]) + "$) |")
    md.append("|---|---:|---:|---:|")
    md.append(f"| **Total Segments Analyzed** | {chat_m['num_segments']} | {irm_m['num_segments']} | {results['arxiv_avg_segments']:.1f} (avg) |")
    md.append(f"| **Thermodynamic Maturity Score (vs arXiv)** | **{chat_vs['thermodynamic_maturity_score']:.2f} / 100** | **{irm_vs['thermodynamic_maturity_score']:.2f} / 100** | **100.00 / 100** |")
    md.append(f"| **Understandability Index** | **{chat_m['understandability_index']:.2f}** | **{irm_m['understandability_index']:.2f}** | **{arxiv_ref['understandability_index']:.2f}** |")
    md.append(f"| **Engine Entropy Rate $H(M_{{4\\times 4}})$ (bits/step)** | {chat_m['engine_entropy_rate']:.4f} | {irm_m['engine_entropy_rate']:.4f} | {arxiv_ref['engine_entropy_rate']:.4f} |")
    md.append(f"| **Modal Entropy Rate $H(M_{{8\\times 8}})$ (bits/step)** | {chat_m['modal_entropy_rate']:.4f} | {irm_m['modal_entropy_rate']:.4f} | {arxiv_ref['modal_entropy_rate']:.4f} |")
    md.append(f"| **Clockwise Canonical Flux ($C\\to P\\to R\\to G\\to C$)** | {chat_m['cw_canonical_flux']:.4f} | {irm_m['cw_canonical_flux']:.4f} | {arxiv_ref['cw_canonical_flux']:.4f} |")
    md.append(f"| **Counter-Clockwise Reverse Flux** | {chat_m['ccw_reverse_flux']:.4f} | {irm_m['ccw_reverse_flux']:.4f} | {arxiv_ref['ccw_reverse_flux']:.4f} |")
    md.append(f"| **Net Cycle Vorticity ($\\Omega = J_{{CW}} - J_{{CCW}}$)** | {chat_m['net_cycle_vorticity']:+.4f} | {irm_m['net_cycle_vorticity']:+.4f} | {arxiv_ref['net_cycle_vorticity']:+.4f} |")
    md.append(f"| **Full 4-Step Canonical Cycles ($C\\to P\\to R\\to G$)** | {chat_m['full_4step_cw_cycles']} | {irm_m['full_4step_cw_cycles']} | — |")
    md.append(f"| **Reductive Trap Stall Rate ($R\\to R\\to G / R\\to R\\to R$)** | {chat_m['reductive_trap_rate']:.4f} ({chat_m['reductive_trap_stalls']}) | {irm_m['reductive_trap_rate']:.4f} ({irm_m['reductive_trap_stalls']}) | {arxiv_ref['reductive_trap_rate']:.4f} |")
    md.append(f"| **Productive Runaway Rate ($P\\to P\\to P$ unverified)** | {chat_m['productive_runaway_rate']:.4f} ({chat_m['productive_runaways']}) | {irm_m['productive_runaway_rate']:.4f} ({irm_m['productive_runaways']}) | {arxiv_ref['productive_runaway_rate']:.4f} |")
    md.append(f"| **Mean Inclusive/Exclusive Polarity $\\langle \\iota \\rangle \\in [-1,+1]$** | {chat_m['mean_iota']:+.4f} | {irm_m['mean_iota']:+.4f} | {arxiv_ref['mean_iota']:+.4f} |")
    md.append(f"| **Inclusive / Exclusive Segment Ratio ($+I / -E$)** | {chat_m['inclusive_exclusive_ratio']:.2f} | {irm_m['inclusive_exclusive_ratio']:.2f} | {arxiv_ref['inclusive_exclusive_ratio']:.2f} |")
    md.append(f"| **Mean Symbolic Density** | {chat_m['mean_symbolic_density']:.4f} | {irm_m['mean_symbolic_density']:.4f} | {arxiv_ref['mean_symbolic_density']:.4f} |")
    md.append("")

    md.append("### Stationary Distribution Comparison ($\\pi_C, \\pi_P, \\pi_R, \\pi_G$)")
    md.append("| Engine State | `chat` Stationary $\\pi$ | `irm` Stationary $\\pi$ | arXiv Reference $\\pi$ | Dynamical Role |")
    md.append("|---|---:|---:|---:|---|")
    for e in ENGINES:
        md.append(f"| **{e}** ({ENGINE_NAMES[e].split('(')[0].strip()}) | {chat_m['engine_stationary'][e]:.4f} | {irm_m['engine_stationary'][e]:.4f} | {arxiv_ref['engine_stationary'][e]:.4f} | {ENGINE_NAMES[e]} |")
    md.append("")

    md.append("---")
    md.append("")
    md.append("## 2. Markov Transition Matrices ($4\\times 4$ Engine & $8\\times 8$ Modal)")
    md.append("")
    md.append("### 2.1 `chatgpt infinity maths.md` (`chat`) — $4\\times 4$ Engine Transition Matrix $M_{ij}$")
    md.append(format_matrix_md(chat_m["engine_matrix"], ENGINES))
    md.append("")
    md.append("### 2.2 `Comprehensive Report (IRM).md` (`irm`) — $4\\times 4$ Engine Transition Matrix $M_{ij}$")
    md.append(format_matrix_md(irm_m["engine_matrix"], ENGINES))
    md.append("")
    md.append("### 2.3 arXiv Reference Ensemble — $4\\times 4$ Engine Transition Matrix $M_{ij}$")
    md.append(format_matrix_md(arxiv_ref["engine_matrix"], ENGINES))
    md.append("")
    md.append("### 2.4 `chatgpt infinity maths.md` (`chat`) — $8\\times 8$ Modal Transition Matrix")
    md.append(format_matrix_md(chat_m["modal_matrix"], MODALS))
    md.append("")
    md.append("### 2.5 `Comprehensive Report (IRM).md` (`irm`) — $8\\times 8$ Modal Transition Matrix")
    md.append(format_matrix_md(irm_m["modal_matrix"], MODALS))
    md.append("")
    md.append("### 2.6 arXiv Reference Ensemble — $8\\times 8$ Modal Transition Matrix")
    md.append(format_matrix_md(arxiv_ref["modal_matrix"], MODALS))
    md.append("")

    md.append("### 2.7 Dynamical Pathologies: Reductive Trap Stalls vs. Productive Runaways")
    md.append("#### Top Reductive Trap Stalls in `chat` ($R\\to R\\to R$ or $R\\to G\\to R$)")
    md.append("| Lines | Engine Pattern | Modal Sequence | Context Excerpt |")
    md.append("|---|---|---|---|")
    for loc in chat_m["reductive_trap_locations"][:8]:
        excerpt_clean = loc["excerpt"].replace("|", "\\|")
        md.append(f"| `{loc['lines']}` | `{loc['pattern']}` | `{loc['modals']}` | {excerpt_clean} |")
    md.append("")

    md.append("#### Top Productive Runaways in `irm` ($P\\to P\\to P$ without Reductive Boundary Testing)")
    md.append("| Lines | Engine Pattern | Modal Sequence | Context Excerpt |")
    md.append("|---|---|---|---|")
    for loc in irm_m["productive_runaway_locations"][:8]:
        excerpt_clean = loc["excerpt"].replace("|", "\\|")
        md.append(f"| `{loc['lines']}` | `{loc['pattern']}` | `{loc['modals']}` | {excerpt_clean} |")
    md.append("")

    md.append("---")
    md.append("")
    md.append("## 3. Concept Evolutionary Survival Analysis (Kaplan–Meier & Orphan Audit)")
    md.append("")
    md.append(f"- **Total Distinct Concept Candidates Extracted in `chat`**: `{surv['total_distinct_concepts_raw']}`")
    md.append(f"- **Recurring Evolutionary Cohort ($\\ge 2$ occurrences in `chat`)**: `{surv['total_recurring_cohort']}`")
    md.append(f"- **Concept Evolutionary Half-Life ($S(\\Delta t) = 0.50$)**: `{surv['concept_half_life_norm']:.4f}` (normalized document lifespan)")
    md.append(f"- **Cross-Document Transmission Rate (`chat` $\\to$ `irm`)**: `{surv['cross_doc_transmission_rate']*100:.2f}%`")
    md.append(f"- **Immortal / Core Concepts**: `{surv['immortal_core_count']}` | **Orphaned High-Fitness Concepts**: `{surv['orphaned_high_fitness_count']}` | **Extinct / Deprecated Concepts**: `{surv['extinct_deprecated_count']}`")
    md.append("")
    md.append("### 3.1 Kaplan–Meier Concept Survival Curve $S(\\Delta t)$ in `chat`")
    md.append("| Normalized Lifespan $\\Delta t$ | `0.0` | `0.1` | `0.2` | `0.3` | `0.4` | `0.5` | `0.6` | `0.7` | `0.8` | `0.9` | `1.0` |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    km = surv["kaplan_meier_survival_curve"]
    md.append("| **Survival Probability $S(\\Delta t)$** | " + " | ".join(f"{km[f'{k*0.1:.1f}']:.3f}" for k in range(11)) + " |")
    md.append("")

    md.append("### 3.2 Immortal / Core Concepts (Survived `chat` Reductive Stress & Transmitted into `irm`)")
    md.append("| Concept | `chat` Freq | `irm` Freq | Lifespan (`chat`) | Lines (`chat`) | Polarity (`+I/-E`) | Engine Profile (`C/P/R/G`) | Survived $R$-Test | Fitness |")
    md.append("|---|---:|---:|---:|---|---|---|---:|---:|")
    for c in surv["immortal_core_top20"][:15]:
        ep = c["engine_profile"]
        md.append(f"| **{c['canonical_name']}** | {c['chat_frequency']} | {c['irm_frequency']} | {c['lifespan']:.3f} | L{c['first_line']}–L{c['last_line']} | `{c['polarity_ratio']}` | `{ep['C']}/{ep['P']}/{ep['R']}/{ep['G']}` | {'YES' if c['survived_reductive_stress'] else 'NO'} | **{c['fitness_score']:.2f}** |")
    md.append("")

    md.append("### 3.3 Orphaned / Unmerged High-Fitness Concepts (High Survival & Fitness in `chat`, **ABSENT** from `irm`)")
    md.append("> [!IMPORTANT]")
    md.append("> These concepts achieved strong evolutionary persistence, Productive expansion, or Reductive stress survival in `chatgpt infinity maths.md`, but were **dropped/unmerged** when compiling `Comprehensive Report - Infinity Indefinite Mathematics (IRM).md`.")
    md.append("")
    md.append("| Orphaned Concept | `chat` Freq | Lifespan | Line Span (`chat`) | Polarity (`+I/-E`) | Engine (`C/P/R/G`) | Survived $R$-Test | Fitness | Context Snippet |")
    md.append("|---|---:|---:|---|---|---|---|---:|---:|---|")
    for c in surv["orphaned_high_fitness_top25"][:20]:
        ep = c["engine_profile"]
        snip = c["first_snippet"].replace("|", "\\|")[:95]
        md.append(f"| **{c['canonical_name']}** | {c['chat_frequency']} | {c['lifespan']:.3f} | L{c['first_line']}–L{c['last_line']} | `{c['polarity_ratio']}` | `{ep['C']}/{ep['P']}/{ep['R']}/{ep['G']}` | {'YES' if c['survived_reductive_stress'] else 'NO'} | **{c['fitness_score']:.2f}** | {snip}... |")
    md.append("")

    md.append("### 3.4 Extinct / Deprecated Concepts (Introduced in `chat`, Hit Reductive/Regressive Walls & Died Early)")
    md.append("| Extinct Concept | `chat` Freq | Birth–Death Pos | Line Span (`chat`) | Polarity (`+I/-E`) | Engine (`C/P/R/G`) | Terminal Context Snippet |")
    md.append("|---|---:|---|---|---|---|---|")
    for c in surv["extinct_deprecated_top20"][:15]:
        ep = c["engine_profile"]
        snip = c["last_snippet"].replace("|", "\\|")[:95]
        md.append(f"| **{c['canonical_name']}** | {c['chat_frequency']} | {c['birth_pos']:.2f}–{c['death_pos']:.2f} | L{c['first_line']}–L{c['last_line']} | `{c['polarity_ratio']}` | `{ep['C']}/{ep['P']}/{ep['R']}/{ep['G']}` | {snip}... |")
    md.append("")

    md.append("---")
    md.append("")
    md.append("## 4. Thermodynamic Complexity & arXiv Maturity Benchmark")
    md.append("")
    md.append("### 4.1 Individual arXiv Reference Papers Profile")
    md.append("| arXiv Paper | Segments | $H(M_{4\\times 4})$ | $H(M_{8\\times 8})$ | CW Flux | Trap Rate | Runaway Rate | Mean $\\iota$ | Understandability |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, am in results["arxiv_papers"].items():
        md.append(f"| `{name}` | {am['num_segments']} | {am['engine_entropy_rate']:.4f} | {am['modal_entropy_rate']:.4f} | {am['cw_canonical_flux']:.4f} | {am['reductive_trap_rate']:.4f} | {am['productive_runaway_rate']:.4f} | {am['mean_iota']:+.4f} | {am['understandability_index']:.2f} |")
    md.append("")

    md.append("### 4.2 Kullback–Leibler ($D_{KL}$) & Jensen–Shannon ($D_{JS}$) Divergence vs. arXiv Reference")
    md.append("| Divergence / Similarity Metric | `chat` vs. arXiv Ref | `irm` vs. arXiv Ref | `irm` vs. `chat` (Distillation Shift) |")
    md.append("|---|---:|---:|---:|")
    md.append(f"| **$4\\times 4$ Engine Transition $D_{{KL}}(P \\parallel Q)$ (bits)** | {chat_vs['engine_4x4_divergence']['weighted_kl_bits']:.4f} | {irm_vs['engine_4x4_divergence']['weighted_kl_bits']:.4f} | {chat_vs_irm['engine_4x4_divergence']['weighted_kl_bits']:.4f} |")
    md.append(f"| **$4\\times 4$ Engine Transition $D_{{JS}}(P, Q)$ (bits)** | {chat_vs['engine_4x4_divergence']['weighted_jsd_bits']:.4f} | {irm_vs['engine_4x4_divergence']['weighted_jsd_bits']:.4f} | {chat_vs_irm['engine_4x4_divergence']['weighted_jsd_bits']:.4f} |")
    md.append(f"| **$4\\times 4$ Engine JS Similarity ($1 - \\sqrt{{D_{{JS}}}}$)** | **{chat_vs['engine_4x4_divergence']['js_similarity']:.4f}** | **{irm_vs['engine_4x4_divergence']['js_similarity']:.4f}** | **{chat_vs_irm['engine_4x4_divergence']['js_similarity']:.4f}** |")
    md.append(f"| **$8\\times 8$ Modal Transition $D_{{KL}}(P \\parallel Q)$ (bits)** | {chat_vs['modal_8x8_divergence']['weighted_kl_bits']:.4f} | {irm_vs['modal_8x8_divergence']['weighted_kl_bits']:.4f} | {chat_vs_irm['modal_8x8_divergence']['weighted_kl_bits']:.4f} |")
    md.append(f"| **$8\\times 8$ Modal Transition $D_{{JS}}(P, Q)$ (bits)** | {chat_vs['modal_8x8_divergence']['weighted_jsd_bits']:.4f} | {irm_vs['modal_8x8_divergence']['weighted_jsd_bits']:.4f} | {chat_vs_irm['modal_8x8_divergence']['weighted_jsd_bits']:.4f} |")
    md.append(f"| **$8\\times 8$ Modal JS Similarity ($1 - \\sqrt{{D_{{JS}}}}$)** | **{chat_vs['modal_8x8_divergence']['js_similarity']:.4f}** | **{irm_vs['modal_8x8_divergence']['js_similarity']:.4f}** | **{chat_vs_irm['modal_8x8_divergence']['js_similarity']:.4f}** |")
    md.append(f"| **Engine Stationary $D_{{JS}}(\\pi_P, \\pi_Q)$ (bits)** | {chat_vs['engine_stationary_jsd_bits']:.4f} | {irm_vs['engine_stationary_jsd_bits']:.4f} | {chat_vs_irm['engine_stationary_jsd_bits']:.4f} |")
    md.append(f"| **Modal Stationary $D_{{JS}}(\\pi_P, \\pi_Q)$ (bits)** | {chat_vs['modal_stationary_jsd_bits']:.4f} | {irm_vs['modal_stationary_jsd_bits']:.4f} | {chat_vs_irm['modal_stationary_jsd_bits']:.4f} |")
    md.append(f"| **Modal Entropy Rate Shift $\\Delta H$ (bits/step)** | {chat_vs['entropy_rate_delta_bits']:+.4f} | {irm_vs['entropy_rate_delta_bits']:+.4f} | {chat_vs_irm['entropy_rate_delta_bits']:+.4f} |")
    md.append(f"| **Composite Thermodynamic Maturity Score** | **{chat_vs['thermodynamic_maturity_score']:.2f} / 100** | **{irm_vs['thermodynamic_maturity_score']:.2f} / 100** | — |")
    md.append("")

    md.append("---")
    md.append("")
    md.append("## 5. Breakdown Locator (Exact Line Numbers of Entropy Spikes & Readability Collapse)")
    md.append("")
    md.append("### 5.1 Readability Breakdown & Ungrounded Jump Zones in `Comprehensive Report (IRM).md` (`irm`)")
    md.append("| Line Range | Window Entropy | Sym Density | Constructive % | Mean $\\iota$ | Score | Structural Diagnosis | Sample Opening Text |")
    md.append("|---|---:|---:|---:|---:|---:|---|---|")
    for b in irm_m["breakdown_zones"][:10]:
        samp = b["sample_text"].replace("|", "\\|")[:85]
        md.append(f"| **L{b['start_line']}–L{b['end_line']}** | {b['window_modal_entropy']:.3f} | {b['symbolic_density']:.3f} | {b['constructive_ratio']*100:.1f}% | {b['mean_iota']:+.2f} | **{b['breakdown_score']:.2f}** | {b['diagnosis']} | {samp}... |")
    md.append("")

    md.append("### 5.2 Readability Breakdown & Reductive Trap Zones in `chatgpt infinity maths.md` (`chat`)")
    md.append("| Line Range | Window Entropy | Sym Density | Constructive % | Mean $\\iota$ | Score | Structural Diagnosis | Sample Opening Text |")
    md.append("|---|---:|---:|---:|---:|---:|---|---|")
    for b in chat_m["breakdown_zones"][:10]:
        samp = b["sample_text"].replace("|", "\\|")[:85]
        md.append(f"| **L{b['start_line']}–L{b['end_line']}** | {b['window_modal_entropy']:.3f} | {b['symbolic_density']:.3f} | {b['constructive_ratio']*100:.1f}% | {b['mean_iota']:+.2f} | **{b['breakdown_score']:.2f}** | {b['diagnosis']} | {samp}... |")
    md.append("")

    md.append("---")
    md.append("")
    md.append("## 6. Key Analytical Findings & Actionable Synthesis Recommendations")
    md.append("")
    md.append("1. **Markov Regime Shift (`chat` $\\to$ `irm` vs. `arXiv`)**:")
    md.append(f"   - `chat` operates in a high-exploration dialectical regime (`C={chat_m['engine_stationary']['C']:.1%}`, `P={chat_m['engine_stationary']['P']:.1%}`, `R={chat_m['engine_stationary']['R']:.1%}`, `G={chat_m['engine_stationary']['G']:.1%}`), periodically hitting **Reductive Trap Stalls** ({chat_m['reductive_trap_stalls']} instances) when classical ZFC/Cantorian definitions clash with dynamic infinity.")
    md.append(f"   - `irm` compresses the dialogue into an assertive formal treatise (`C={irm_m['engine_stationary']['C']:.1%}`, `P={irm_m['engine_stationary']['P']:.1%}`, `R={irm_m['engine_stationary']['R']:.1%}`, `G={irm_m['engine_stationary']['G']:.1%}`), achieving a Thermodynamic Maturity Score of **{irm_vs['thermodynamic_maturity_score']:.2f}/100** vs. arXiv (**{chat_vs['thermodynamic_maturity_score']:.2f}/100** for `chat`), but suffers from **Productive Runaways** ({irm_m['productive_runaways']} instances) where definitions and theorems cascade (`P\\to P\\to P`) without sufficient Constructive (`is_like`) intuition or Reductive (`can_be`/`is_not`) counter-example testing.")
    md.append("2. **Concept Survival & Critical Orphan Recovery**:")
    md.append(f"   - Only **{surv['cross_doc_transmission_rate']*100:.1f}%** of recurring concepts in `chat` survived transmission into `irm`.")
    md.append(f"   - **{surv['orphaned_high_fitness_count']} high-fitness concepts** survived multiple turns and Reductive stress tests in `chat` yet were **orphaned** in `irm`. Re-integrating the top orphaned pedagogical bridges and physical/geometric analogies into `irm` at the exact breakdown line ranges identified in Section 5.1 will restore Constructive grounding and raise both the Understandability Index and arXiv Maturity alignment.")
    md.append("")
    return "\n".join(md)


def main():
    AGENT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Parse and analyze chat and irm
    chat_segs, chat_lines = parse_document_segments(CHAT_PATH)
    irm_segs, irm_lines = parse_document_segments(IRM_PATH)

    chat_metrics = compute_markov_metrics(chat_segs)
    chat_metrics["total_lines"] = chat_lines

    irm_metrics = compute_markov_metrics(irm_segs)
    irm_metrics["total_lines"] = irm_lines

    # 2. Parse and analyze all arXiv papers
    arxiv_papers = {}
    arxiv_metrics_list = []
    for p in sorted(ARXIV_DIR.glob("*.md")):
        a_segs, a_lines = parse_document_segments(p)
        a_m = compute_markov_metrics(a_segs)
        a_m["total_lines"] = a_lines
        arxiv_papers[p.name] = a_m
        arxiv_metrics_list.append(a_m)

    arxiv_ref = build_arxiv_reference(arxiv_metrics_list)

    # 3. Concept Evolutionary Survival Analysis
    survival_results = analyze_concept_survival(chat_segs, chat_lines, irm_segs, irm_lines)

    # 4. Benchmarks (KL / JSD Maturity)
    chat_vs_arxiv = score_against_arxiv(chat_metrics, arxiv_ref)
    irm_vs_arxiv = score_against_arxiv(irm_metrics, arxiv_ref)
    irm_vs_chat = score_against_arxiv(irm_metrics, chat_metrics)

    results = {
        "agent": "Agent 4: Markov Transition Matrix, Concept Survival & Thermodynamic Maturity Engine",
        "documents": {
            "chat": chat_metrics,
            "irm": irm_metrics
        },
        "arxiv_papers": arxiv_papers,
        "arxiv_avg_segments": sum(m["num_segments"] for m in arxiv_metrics_list) / max(1, len(arxiv_metrics_list)),
        "arxiv_reference": arxiv_ref,
        "benchmarks": {
            "chat_vs_arxiv": chat_vs_arxiv,
            "irm_vs_arxiv": irm_vs_arxiv,
            "irm_vs_chat": irm_vs_chat
        },
        "concept_survival": survival_results
    }

    results_path = AGENT_DIR / "results.json"
    report_path = AGENT_DIR / "report.md"

    results_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    report_md = generate_markdown_report(results)
    report_path.write_text(report_md, encoding="utf-8")

    # Print concise summary to stdout
    print("=== AGENT 4: MARKOV, SURVIVAL & THERMODYNAMIC MATURITY ENGINE COMPLETE ===")
    print(f"Chat Segments: {chat_metrics['num_segments']} (Lines: {chat_lines}) | IRM Segments: {irm_metrics['num_segments']} (Lines: {irm_lines}) | arXiv Papers: {len(arxiv_papers)}")
    print(f"Stationary Engine Dist (C/P/R/G):")
    print(f"  chat : {chat_metrics['engine_stationary']}")
    print(f"  irm  : {irm_metrics['engine_stationary']}")
    print(f"  arXiv: {arxiv_ref['engine_stationary']}")
    print(f"CW Canonical Flux: chat={chat_metrics['cw_canonical_flux']:.4f}, irm={irm_metrics['cw_canonical_flux']:.4f}, arXiv={arxiv_ref['cw_canonical_flux']:.4f}")
    print(f"Reductive Trap Rate: chat={chat_metrics['reductive_trap_rate']:.4f} ({chat_metrics['reductive_trap_stalls']}), irm={irm_metrics['reductive_trap_rate']:.4f} ({irm_metrics['reductive_trap_stalls']}), arXiv={arxiv_ref['reductive_trap_rate']:.4f}")
    print(f"Productive Runaway Rate: chat={chat_metrics['productive_runaway_rate']:.4f} ({chat_metrics['productive_runaways']}), irm={irm_metrics['productive_runaway_rate']:.4f} ({irm_metrics['productive_runaways']}), arXiv={arxiv_ref['productive_runaway_rate']:.4f}")
    print(f"Thermodynamic Maturity Score (vs arXiv): chat={chat_vs_arxiv['thermodynamic_maturity_score']:.2f}/100 | irm={irm_vs_arxiv['thermodynamic_maturity_score']:.2f}/100")
    print(f"Understandability Index: chat={chat_metrics['understandability_index']:.2f} | irm={irm_metrics['understandability_index']:.2f} | arXiv={arxiv_ref['understandability_index']:.2f}")
    print(f"Concept Survival: Cohort={survival_results['total_recurring_cohort']}, Half-Life={survival_results['concept_half_life_norm']:.3f}, Transmission={survival_results['cross_doc_transmission_rate']*100:.1f}%")
    print(f"  Immortal={survival_results['immortal_core_count']} | Orphaned High-Fitness={survival_results['orphaned_high_fitness_count']} | Extinct={survival_results['extinct_deprecated_count']}")
    print(f"Top 5 Orphaned Concepts: {[c['canonical_name'] for c in survival_results['orphaned_high_fitness_top25'][:5]]}")
    print(f"Outputs saved to: {results_path} and {report_path}")


if __name__ == "__main__":
    main()
