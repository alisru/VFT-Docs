#!/usr/bin/env python3
"""
Agent 5 (Round 2): Dynamic [IS] Concept-Bond Graph & 4-Color Gluon Gauge Physics v2
- Critique of Global Modal Aggregation vs. Local-to-Global Causal Force Cascades
- Red-to-Blue Proof Resolution Ratio (R_{R->BM}) & Cascade Conversion Tracking
- Signed Triangle Frustration Resolution (chat -> IRM Report -> Formal Papers & ORTHODOX_BRIDGE_ZFC)
- Multi-Paper Knowledge Graph Coverage across the Full IRM Formal Corpus & Expanded arXiv Suite
"""

import os
import re
import json
import math
from pathlib import Path
from collections import defaultdict, Counter

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics")
DNA_DIR = BASE_DIR / "semantic_gluon_dna"
OUT_DIR = DNA_DIR / "agent_5_graph_force_network"
ARXIV_DIR = DNA_DIR / "arxiv_samples"
IRM_CORPUS_DIR = DNA_DIR / "irm_formal_corpus"

CHAT_PATH = BASE_DIR / "chatgpt infinity maths.md"
IRM_PATH = BASE_DIR / "Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md"
UNIFIED_ENGINE_PATH = DNA_DIR / "unified_gluon_dna_engine.py"

# 8 Modal States around central [IS]
MODAL_PATTERNS = {
    "will_be": [
        r"\b(?:is defined as|equals|must be|will be|shall be|is identically|yields|defines|becomes|always equals|entails|fixes|establishes|proves|satisfies|holds)\b",
        r"==|:=|\\equiv|\baxiom\b|\btheorem\b|\blemma\b|\bcorollary\b|\blaw\b|\binvariant\b|\bproof\b|\bq\.e\.d\b"
    ],
    "can_be": [
        r"\b(?:can be|able to|capable of|allows|permits|enables|functions as|acts as|operates as|represented as|formulated as|expressible|admits|mapped to|constructed)\b"
    ],
    "is_not": [
        r"\b(?:is not|isn't|are not|aren't|differs from|distinct from|not equal to|never equals|unlike|non-standard|not a|not the|independent of|disjoint)\b",
        r"!=|\\neq|≠"
    ],
    "cant_be": [
        r"\b(?:cannot be|can't be|impossible|undefined|indeterminate|ill-defined|forbidden|contradiction|dividing by zero|unbounded|inconsistent|violates|singular|blow-up|diverges)\b"
    ],
    "wont_be": [
        r"\b(?:will not|won't be|refuses to|fails to|never converges|does not hold|rejected|abandoned|collapsed|breaks down|precludes|prevents)\b"
    ],
    "was_like": [
        r"\b(?:was|were|historically|classically|traditionally|standard math|conventional|previously|in classical|cantor|euclid|newton|leibniz|orthodox|zfc|standard analysis)\b"
    ],
    "is_like": [
        r"\b(?:is like|similar to|analogous to|resembles|corresponds to|mirrors|metaphor|heartbeat|shell|pulse|wave|lens|bridge|membrane|fabric|isomorphic)\b"
    ],
    "may_be": [
        r"\b(?:may be|might be|could be|perhaps|possibly|what if|suppose|hypothesize|conjecture|tentative|if we let|imagine|speculate|assume|consider)\b"
    ]
}

INCLUSION_TRIGGERS = [
    r"\b(?:includes|contains|builds|generates|implies|produces|comprises|integrates|unifies|synthesizes|extends|is a|forms|induces|couples|preserves|entails|satisfies)\b",
    r"->|\\rightarrow|⇒|⊂|⊆|\\implies"
]

EXCLUSION_TRIGGERS = [
    r"\b(?:excludes|discludes|opposes|contradicts|negates|rejects|eliminates|separates|cancels|annihilates|conflicts with|replaces|forbids|violates)\b",
    r"\\neq|≠|⊥"
]

# Expanded Canonical Concept Lexicon covering Chat, IRM Report, IRM Formal Papers (Navier-Stokes, Levi-Civita, ZFC, etc.), and arXiv
CANONICAL_CONCEPTS = {
    "infinity_hierarchy": [r"\binfinit(?:y|ies)\b", r"\\infty", r"∞", r"\bscaling level\b", r"\bn\+1\b", r"\btransfinite\b"],
    "unit_power_infinity": [r"1\^\{?\\infty\}?", r"1\^∞", r"\bone to the infinity\b", r"1_n", r"0_\{?n\+1\}?"],
    "zero_state": [r"\bzero\b", r"\bnull state\b", r"0\^\{?\\infty\}?", r"\bvoid\b", r"\binfinitesimal\b"],
    "indefinite_irm": [r"\bindefinite\b", r"\birm\b", r"\bindeterminate form\b", r"\bdefinitional\b"],
    "relative_horizon": [r"\bhorizon\b", r"\bboundary\b", r"\blimit\b", r"\basymptot(?:e|ic)\b", r"\bcutoff\b"],
    "shell_geometry": [r"\bshell\b", r"\bsphere\b", r"\bmanifold\b", r"\btopolog(?:y|ical)\b", r"\bsurface\b"],
    "heartbeat_oscillation": [r"\bheartbeat\b", r"\bpulse\b", r"\boscillat(?:e|ion)\b", r"\bcycle\b", r"\bfrequency\b"],
    "division_operator": [r"\bdivision\b", r"\bratio\b", r"\bquotient\b", r"\bfraction\b", r"\binverse\b"],
    "potential_field": [r"\bpotential\b", r"\bfield\b", r"\bvector\b", r"\btensor\b", r"\bgradient\b"],
    "axiom_foundation": [r"\baxiom(?:atic|s)?\b", r"\bpostulate\b", r"\bfoundation\b", r"\bdefinition\b", r"\btheorem\b"],
    "cantor_zfc_set": [r"\bcantor\b", r"\bzfc\b", r"\bcardinal(?:ity)?\b", r"\bordinal\b", r"\baleph\b", r"\bbijection\b", r"\bset theory\b"],
    "calculus_analysis": [r"\bcalculus\b", r"\bderivative\b", r"\bintegral\b", r"\bdifferential\b", r"\bl'hopital\b", r"\bseries\b"],
    "levi_civita_nonarchimedean": [r"\blevi-civita\b", r"\bnon-archimedean\b", r"\bhyperreal\b", r"\brobinson\b", r"\bsurreal\b", r"\bvaluation\b"],
    "navier_stokes_fluid": [r"\bnavier-stokes\b", r"\bvorticity\b", r"\bviscosity\b", r"\bturbulen(?:ce|t)\b", r"\bfluid\b", r"\breynolds\b", r"\benstrophy\b"],
    "quantum_vacuum": [r"\bquantum\b", r"\bvacuum\b", r"\bplanck\b", r"\bwavefunction\b", r"\bentrop(?:y|ic)\b", r"\bhamiltonian\b"],
    "spacetime_relativity": [r"\bspacetime\b", r"\brelativ(?:ity|istic)\b", r"\bmetric\b", r"\bcurvature\b", r"\blorentz\b", r"\bgravit(?:y|ational)\b"],
    "consciousness_observer": [r"\bobserver\b", r"\bconscious(?:ness)?\b", r"\bperception\b", r"\bmeasurement\b", r"\bframe\b"],
    "dimension_transition": [r"\bdimension(?:al|s)?\b", r"\btransition\b", r"\bphase\b", r"\bprojection\b", r"\bembedding\b"],
    "number_line_continuum": [r"\bcontinuum\b", r"\breal line\b", r"\bnumber line\b", r"\bdiscrete\b", r"\bdense\b"],
    "symmetry_conservation": [r"\bsymmetr(?:y|ic)\b", r"\bconservation\b", r"\binvariance\b", r"\bgauge\b", r"\bparity\b"],
    "energy_mass_action": [r"\benergy\b", r"\bmass\b", r"\baction\b", r"\bmomentum\b", r"\bforce\b", r"\bcoupling\b"],
    "duality_inversion": [r"\bdual(?:ity)?\b", r"\binversion\b", r"\breciprocal\b", r"\bmirror\b", r"\bconjugate\b"],
    "convergence_singularity": [r"\bconverg(?:e|ence|ent)\b", r"\bdiverg(?:e|ence|ent)\b", r"\bstabilit(?:y|ies)\b", r"\bsingularit(?:y|ies)\b", r"\bblow-up\b", r"\bregularity\b"],
    "information_encoding": [r"\binformation\b", r"\bencoding\b", r"\bstate\b", r"\bbit\b", r"\bcomplexity\b"],
    "algebraic_structure": [r"\balgebra(?:ic)?\b", r"\bgroup\b", r"\bring\b", r"\bisomorphi(?:sm|c)\b", r"\boperator\b", r"\bhomomorphism\b"],
    "euler_identity_complex": [r"\beuler\b", r"\bcomplex\b", r"\bimaginary\b", r"\bphase angle\b", r"\brotation\b"],
    "paradox_resolution": [r"\bparadox\b", r"\bzeno\b", r"\bhilbert\b", r"\bcontradiction\b", r"\banomaly\b"],
    "unit_identity_one": [r"\bunit\b", r"\bidentity\b", r"\bunity\b", r"\bwhole\b", r"\bcompleteness\b"],
    "fractional_fractal_scale": [r"\bfractional\b", r"\bfractal\b", r"\bself-similar\b", r"\bhausdorff\b", r"\bscaling\b"],
    "digit_base_arithmetic": [r"\bdigit(?:s)?\b", r"\binteger(?:s)?\b", r"\bradix\b", r"\bdecimal\b", r"\bplace value\b", r"\barithmetic\b"]
}

STOPWORDS = {
    "the", "and", "for", "that", "this", "with", "from", "have", "are", "was", "were",
    "will", "would", "could", "should", "can", "may", "might", "must", "not", "but",
    "what", "which", "when", "where", "who", "how", "why", "into", "onto", "upon",
    "about", "above", "below", "between", "through", "during", "before", "after",
    "then", "than", "also", "just", "only", "very", "more", "most", "some", "any",
    "each", "every", "other", "another", "such", "like", "same", "different", "new",
    "used", "using", "use", "make", "made", "does", "did", "done", "being", "been",
    "has", "had", "its", "their", "there", "here", "they", "them", "these", "those",
    "you", "your", "our", "out", "all", "one", "two", "three", "first", "second",
    "case", "way", "time", "part", "form", "system", "model", "paper", "section",
    "figure", "table", "equation", "result", "results", "show", "shown", "given"
}


def compile_patterns():
    modal_compiled = {
        k: [re.compile(p, re.IGNORECASE) for p in pats]
        for k, pats in MODAL_PATTERNS.items()
    }
    inc_compiled = [re.compile(p, re.IGNORECASE) for p in INCLUSION_TRIGGERS]
    exc_compiled = [re.compile(p, re.IGNORECASE) for p in EXCLUSION_TRIGGERS]
    concept_compiled = {
        k: [re.compile(p, re.IGNORECASE) for p in pats]
        for k, pats in CANONICAL_CONCEPTS.items()
    }
    return modal_compiled, inc_compiled, exc_compiled, concept_compiled


MODAL_RE, INC_RE, EXC_RE, CONCEPT_RE = compile_patterns()


def extract_dynamic_concepts(text, top_k=15):
    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9_\-]{3,24}\b", text.lower())
    counts = Counter(w for w in words if w not in STOPWORDS and not w.isdigit())
    canonical_tokens = set()
    for k in CANONICAL_CONCEPTS:
        canonical_tokens.update(k.split("_"))
    dynamic = {}
    for w, c in counts.most_common(top_k * 3):
        if c >= 4 and w not in canonical_tokens and len(dynamic) < top_k:
            dynamic[f"term_{w}"] = [re.compile(rf"\b{re.escape(w)}\b", re.IGNORECASE)]
    return dynamic


def compute_4color_gluons(modal_counts):
    """Explicit 4-Color Gluon Gauge calculation from 8 Modal States."""
    wb = modal_counts.get("will_be", 0.0)
    cb = modal_counts.get("can_be", 0.0)
    isn = modal_counts.get("is_not", 0.0)
    cntb = modal_counts.get("cant_be", 0.0)
    wntb = modal_counts.get("wont_be", 0.0)
    wasl = modal_counts.get("was_like", 0.0)
    isl = modal_counts.get("is_like", 0.0)
    mayb = modal_counts.get("may_be", 0.0)

    red = (
        2.0 * math.sqrt((wb + 0.5) * (cntb + 0.5)) - 1.0
        + 1.8 * math.sqrt((isl + 0.5) * (wntb + 0.5)) - 0.9
        + 0.35 * (wb + cntb + isl + wntb)
    )
    green = (
        2.0 * math.sqrt((cb + 0.5) * (isn + 0.5)) - 1.0
        + 1.8 * math.sqrt((mayb + 0.5) * (wasl + 0.5)) - 0.9
        + 0.35 * (cb + isn + mayb + wasl)
    )
    blue = (
        2.0 * math.sqrt((wb + 0.5) * (mayb + 0.5)) - 1.0
        + 1.8 * math.sqrt((wntb + 0.5) * (isn + 0.5)) - 0.9
        + 0.45 * wb + 0.25 * (mayb + wntb + isn)
    )
    magenta = (
        2.0 * math.sqrt((isl + 0.5) * (cb + 0.5)) - 1.0
        + 1.8 * math.sqrt((wasl + 0.5) * (cntb + 0.5)) - 0.9
        + 0.40 * (isl + cb + wasl + cntb)
    )

    raw = {
        "Red": round(max(0.0, red), 4),
        "Green": round(max(0.0, green), 4),
        "Blue": round(max(0.0, blue), 4),
        "Magenta": round(max(0.0, magenta), 4)
    }
    total = sum(raw.values()) or 1.0
    norm = {k: round(v / total, 4) for k, v in raw.items()}
    dominant = max(raw.items(), key=lambda x: x[1])[0] if sum(raw.values()) > 0 else "Neutral"
    crystallization = round((norm["Blue"] + norm["Magenta"]) - (norm["Red"] + norm["Green"]), 4)

    return {
        "raw": raw,
        "normalized": norm,
        "total_gluon_flux": round(total, 4),
        "dominant_color": dominant,
        "crystallization_index": crystallization
    }


def compute_local_to_global_proof_resolution(chunk_records, node_trajectory, n_chunks):
    """
    NEW IN V2: Local-to-Global Force Resolution & Red-to-Blue Proof Resolution Ratio (R_{R->BM}).
    Addresses the flaw in `unified_gluon_dna_engine.py` where global modal summation ignores
    whether early Red opposition (`will_be <-> cant_be`) is actually resolved downstream via
    Green testing (`can_be / may_be`) into Blue/Magenta working-out proofs (`will_be / can_be`).
    """
    window_span = max(3, min(25, int(n_chunks * 0.12)))
    red_events = 0
    resolved_via_green_to_bm = 0
    direct_bm_resolutions = 0
    unresolved_red_spikes = 0

    # Track per-concept local cascade resolution
    concept_red_events = Counter()
    concept_resolved_events = Counter()

    for idx, rec in enumerate(chunk_records):
        modals = rec["modals"]
        active_nodes = rec["concepts"]
        # A local Red contradiction event occurs when impossibility/opposition modals fire
        is_red_spike = (modals.get("cant_be", 0) + modals.get("wont_be", 0)) > 0 and (
            modals.get("will_be", 0) + modals.get("is_like", 0) + modals.get("cant_be", 0) >= 1
        )
        if not is_red_spike:
            continue

        red_events += 1
        for c in active_nodes:
            concept_red_events[c] += 1

        # Look ahead in local causal window [idx+1, idx+window_span] for shared concepts (or local thread)
        downstream = chunk_records[idx + 1 : min(n_chunks, idx + 1 + window_span)]
        green_hits = 0
        blue_magenta_hits = 0
        for d_rec in downstream:
            # Prefer causal continuity where at least 1 concept overlaps, or immediate neighborhood
            overlap = bool(set(active_nodes) & set(d_rec["concepts"])) or (len(active_nodes) == 0)
            weight = 1.0 if overlap else 0.35
            dm = d_rec["modals"]
            green_hits += weight * (dm.get("can_be", 0) + dm.get("may_be", 0))
            blue_magenta_hits += weight * (dm.get("will_be", 0) + 0.8 * dm.get("can_be", 0) + 0.6 * dm.get("is_like", 0))

        if green_hits >= 1.0 and blue_magenta_hits >= 1.5:
            resolved_via_green_to_bm += 1
            for c in active_nodes:
                concept_resolved_events[c] += 1
        elif blue_magenta_hits >= 2.0:
            direct_bm_resolutions += 1
            for c in active_nodes:
                concept_resolved_events[c] += 0.75
        else:
            unresolved_red_spikes += 1

    total_red = max(red_events, 1)
    cascade_resolution_rate = round((resolved_via_green_to_bm + 0.8 * direct_bm_resolutions) / total_red, 4)
    full_green_bridge_rate = round(resolved_via_green_to_bm / total_red, 4)
    unresolved_rate = round(unresolved_red_spikes / total_red, 4)

    # Node-level Early-Red -> Late-Blue/Magenta Trajectory Resolution
    node_resolutions = {}
    resolved_nodes_count = 0
    strained_nodes_count = 0
    for cname, bins in node_trajectory.items():
        early_m = bins[0] + bins[1]
        mid_m = bins[2]
        late_m = bins[3] + bins[4]
        eg = compute_4color_gluons(early_m)
        mg = compute_4color_gluons(mid_m)
        lg = compute_4color_gluons(late_m)

        early_red_raw = eg["raw"]["Red"]
        mid_green_raw = mg["raw"]["Green"] + eg["raw"]["Green"]
        late_bm_raw = lg["raw"]["Blue"] + lg["raw"]["Magenta"]
        late_red_raw = lg["raw"]["Red"]

        # Proof Resolution Ratio for concept c:
        # Measures how much Late (Blue+Magenta) + Mid Green working-out outweighs residual Late Red strain
        denom = max(early_red_raw + late_red_raw, 0.5)
        node_pr_ratio = round((late_bm_raw + 0.35 * mid_green_raw) / denom, 4)
        c_red_ev = concept_red_events[cname]
        c_res_rate = round(concept_resolved_events[cname] / max(c_red_ev, 1), 4) if c_red_ev > 0 else 1.0

        if early_red_raw > 0.5 or c_red_ev > 0:
            strained_nodes_count += 1
            if node_pr_ratio >= 0.85 or c_res_rate >= 0.65:
                resolved_nodes_count += 1

        node_resolutions[cname] = {
            "early_red_flux": round(early_red_raw, 3),
            "mid_green_flux": round(mid_green_raw, 3),
            "late_bm_flux": round(late_bm_raw, 3),
            "late_red_flux": round(late_red_raw, 3),
            "node_proof_resolution_ratio": node_pr_ratio,
            "local_cascade_resolution_rate": c_res_rate,
            "red_spike_count": c_red_ev
        }

    node_resolution_fraction = round(resolved_nodes_count / max(strained_nodes_count, 1), 4)

    # Composite Red-to-Blue Proof Resolution Ratio (R_{R->BM})
    avg_node_pr = sum(v["node_proof_resolution_ratio"] for v in node_resolutions.values()) / max(len(node_resolutions), 1)
    composite_r_rbm = round(0.45 * cascade_resolution_rate + 0.35 * min(avg_node_pr, 2.0) / 2.0 + 0.20 * node_resolution_fraction, 4)

    return {
        "red_contradiction_events": red_events,
        "resolved_via_green_to_bm": resolved_via_green_to_bm,
        "direct_bm_resolutions": direct_bm_resolutions,
        "unresolved_red_spikes": unresolved_red_spikes,
        "cascade_resolution_rate": cascade_resolution_rate,
        "full_green_bridge_rate": full_green_bridge_rate,
        "unresolved_strain_rate": unresolved_rate,
        "strained_nodes_count": strained_nodes_count,
        "resolved_nodes_count": resolved_nodes_count,
        "node_resolution_fraction": node_resolution_fraction,
        "avg_node_proof_resolution_ratio": round(avg_node_pr, 4),
        "composite_proof_resolution_score": composite_r_rbm,
        "node_resolutions": node_resolutions
    }


def scan_document(doc_id, category, file_path):
    text = file_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    raw_chunks = re.split(r"(?<=[.!?])\s+|\n+", text)
    chunks = [c.strip() for c in raw_chunks if len(c.strip()) > 15]
    n_chunks = max(len(chunks), 1)

    dynamic_concepts = extract_dynamic_concepts(text, top_k=12)
    all_concepts = {**CONCEPT_RE, **dynamic_concepts}

    node_modals = defaultdict(lambda: Counter())
    node_mentions = Counter()
    node_first_t = {}
    node_last_t = {}
    node_trajectory = defaultdict(lambda: [Counter() for _ in range(5)])
    edges = defaultdict(lambda: {"+I": 0, "-E": 0, "t_samples": []})
    timeline_modals = [Counter() for _ in range(10)]
    chunk_records = []

    for idx, chunk in enumerate(chunks):
        t = idx / n_chunks
        t_bin5 = min(int(t * 5), 4)
        t_bin10 = min(int(t * 10), 9)

        active_nodes = []
        for cname, pats in all_concepts.items():
            if any(p.search(chunk) for p in pats):
                active_nodes.append(cname)
                node_mentions[cname] += 1
                if cname not in node_first_t:
                    node_first_t[cname] = round(t, 4)
                node_last_t[cname] = round(t, 4)

        active_modals = {}
        for mname, pats in MODAL_RE.items():
            hits = sum(len(p.findall(chunk)) for p in pats)
            if hits > 0:
                active_modals[mname] = hits
                timeline_modals[t_bin10][mname] += hits

        if active_nodes and not active_modals:
            if re.search(r"\b(?:is|are|represents|means|equals|=)\b", chunk, re.IGNORECASE):
                active_modals["will_be"] = 1
                timeline_modals[t_bin10]["will_be"] += 1

        chunk_records.append({
            "t": round(t, 4),
            "concepts": active_nodes,
            "modals": active_modals
        })

        for cname in active_nodes:
            for mname, count in active_modals.items():
                node_modals[cname][mname] += count
                node_trajectory[cname][t_bin5][mname] += count

        if len(active_nodes) >= 2:
            inc_hits = sum(len(p.findall(chunk)) for p in INC_RE)
            exc_hits = sum(len(p.findall(chunk)) for p in EXC_RE)
            is_neg_modal = (active_modals.get("is_not", 0) + active_modals.get("cant_be", 0) + active_modals.get("wont_be", 0)) > 0

            for i in range(len(active_nodes)):
                for j in range(i + 1, len(active_nodes)):
                    u, v = sorted((active_nodes[i], active_nodes[j]))
                    key = (u, v)
                    if exc_hits > 0 or is_neg_modal:
                        edges[key]["-E"] += max(1, exc_hits)
                    if inc_hits > 0 or not is_neg_modal:
                        edges[key]["+I"] += max(1, inc_hits)
                    if len(edges[key]["t_samples"]) < 4:
                        edges[key]["t_samples"].append(round(t, 3))

    # Build graph and compute signed triangles
    adj = defaultdict(set)
    degree_map = Counter()
    total_inc_edges = 0
    total_exc_edges = 0
    edge_list = []
    edge_sign = {}

    for (u, v), edata in edges.items():
        w_inc = edata["+I"]
        w_exc = edata["-E"]
        total_inc_edges += w_inc
        total_exc_edges += w_exc
        adj[u].add(v)
        adj[v].add(u)
        degree_map[u] += (w_inc + w_exc)
        degree_map[v] += (w_inc + w_exc)
        net_polarity = round((w_inc - w_exc) / max(w_inc + w_exc, 1), 4)
        sign = 1 if w_inc >= w_exc else -1
        edge_sign[(u, v)] = sign
        edge_sign[(v, u)] = sign
        edge_list.append({
            "source": u,
            "target": v,
            "inclusion_weight": w_inc,
            "exclusion_weight": w_exc,
            "total_weight": w_inc + w_exc,
            "net_polarity": net_polarity,
            "sign": sign,
            "bond_type": "+I (Inclusion)" if sign > 0 else "-E (Exclusion)"
        })

    edge_list.sort(key=lambda x: x["total_weight"], reverse=True)

    # Compute local-to-global proof resolution metrics
    proof_res = compute_local_to_global_proof_resolution(chunk_records, node_trajectory, n_chunks)

    max_deg = max(degree_map.values(), default=1) or 1
    nodes_dict = {}
    for cname, mentions in node_mentions.items():
        m_counts = dict(node_modals[cname])
        gluons = compute_4color_gluons(m_counts)
        deg = degree_map[cname]
        centrality = round(0.6 * (deg / max_deg) + 0.4 * min(mentions / 40.0, 1.0), 4)
        nodes_dict[cname] = {
            "concept": cname,
            "is_canonical": cname in CANONICAL_CONCEPTS,
            "mentions": mentions,
            "degree_weighted": deg,
            "centrality": centrality,
            "modal_states": m_counts,
            "gluon_forces": gluons,
            "proof_resolution": proof_res["node_resolutions"].get(cname, {})
        }

    # Connected components & signed triangles
    visited = set()
    components = 0
    for n in nodes_dict:
        if n not in visited:
            components += 1
            q = [n]
            visited.add(n)
            while q:
                curr = q.pop(0)
                for nxt in adj[curr]:
                    if nxt in nodes_dict and nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)

    V = len(nodes_dict)
    E = len(edge_list)
    betti_0 = components
    betti_1 = max(0, E - V + betti_0)

    triangles_all = {}
    frustrated_list = []
    balanced_list = []
    node_list = sorted(nodes_dict.keys())
    for i in range(len(node_list)):
        u = node_list[i]
        for j in range(i + 1, len(node_list)):
            v = node_list[j]
            if v not in adj[u]:
                continue
            for k in range(j + 1, len(node_list)):
                w = node_list[k]
                if w in adj[u] and w in adj[v]:
                    s_uv = edge_sign[(u, v)]
                    s_vw = edge_sign[(v, w)]
                    s_uw = edge_sign[(u, w)]
                    prod = s_uv * s_vw * s_uw
                    tri_key = (u, v, w)
                    triangles_all[tri_key] = prod
                    if prod < 0:
                        frustrated_list.append(tri_key)
                    else:
                        balanced_list.append(tri_key)

    total_tri = len(triangles_all)
    frust_count = len(frustrated_list)
    frust_ratio = round(frust_count / max(total_tri, 1), 4)

    # Epistemic Hygiene Score: combines low triangle frustration + high Red-to-Blue proof resolution
    epistemic_hygiene = round(
        0.50 * (1.0 - frust_ratio) + 0.50 * proof_res["composite_proof_resolution_score"],
        4
    )

    global_modals = Counter()
    for t_c in timeline_modals:
        global_modals.update(t_c)
    global_gluons = compute_4color_gluons(dict(global_modals))

    return {
        "doc_id": doc_id,
        "category": category,
        "file_name": file_path.name,
        "char_count": len(text),
        "line_count": len(lines),
        "chunk_count": n_chunks,
        "global_modals": dict(global_modals),
        "global_gluon_forces": global_gluons,
        "proof_resolution_metrics": {
            k: v for k, v in proof_res.items() if k != "node_resolutions"
        },
        "topology_homology": {
            "vertices_V": V,
            "edges_E": E,
            "betti_0_components": betti_0,
            "betti_1_cycles": betti_1,
            "total_inclusion_flux": total_inc_edges,
            "total_exclusion_flux": total_exc_edges,
            "inclusion_exclusion_ratio": round(total_inc_edges / max(total_exc_edges, 1), 4),
            "triangles_total": total_tri,
            "frustrated_triangles": frust_count,
            "frustration_ratio": frust_ratio,
            "epistemic_hygiene_score": epistemic_hygiene
        },
        "nodes": nodes_dict,
        "top_edges": edge_list[:40],
        "all_edges": edge_list,
        "triangles_map": triangles_all,
        "frustrated_triangles_list": [list(t) for t in frustrated_list[:50]]
    }


def analyze_frustration_resolution_and_ecosystem_coverage(docs):
    """
    1. Track exact frustrated triangles in `chat` and `irm` and check how `ORTHODOX_BRIDGE_ZFC`,
       `Formal Paper 17 Navier-Stokes`, `Formal Paper 12 Levi-Civita`, etc. resolve them.
    2. Track Multi-Paper Knowledge Graph Coverage across the entire `irm_formal_corpus`.
    """
    chat = docs["chat"]
    irm = docs["irm"]
    formal_docs = {k: v for k, v in docs.items() if v["category"] == "irm_formal"}

    chat_frust = {tuple(k) for k, s in chat["triangles_map"].items() if s < 0}
    irm_frust = {tuple(k) for k, s in irm["triangles_map"].items() if s < 0}
    combined_seed_frust = chat_frust | irm_frust

    paper_triangle_audits = []
    resolved_across_any_formal = set()

    for fk, fd in formal_docs.items():
        f_tris = fd["triangles_map"]
        shared_with_seed = set(f_tris.keys()) & combined_seed_frust
        resolved_in_paper = [t for t in shared_with_seed if f_tris[t] > 0]
        still_frustrated = [t for t in shared_with_seed if f_tris[t] < 0]
        resolved_across_any_formal.update(resolved_in_paper)

        paper_triangle_audits.append({
            "doc_id": fk,
            "file_name": fd["file_name"],
            "own_triangles_total": fd["topology_homology"]["triangles_total"],
            "own_frustrated_triangles": fd["topology_homology"]["frustrated_triangles"],
            "own_frustration_ratio": fd["topology_homology"]["frustration_ratio"],
            "seed_frustrated_triangles_encountered": len(shared_with_seed),
            "seed_frustrated_triangles_resolved": len(resolved_in_paper),
            "seed_resolution_rate": round(len(resolved_in_paper) / max(len(shared_with_seed), 1), 4),
            "sample_resolved_triads": [" <-> ".join(t) for t in resolved_in_paper[:6]]
        })

    paper_triangle_audits.sort(key=lambda x: (x["seed_frustrated_triangles_resolved"], -x["own_frustration_ratio"]), reverse=True)

    # Multi-Paper Knowledge Graph Coverage of `chat` Concepts & Bonds
    chat_nodes = chat["nodes"]
    irm_nodes = irm["nodes"]

    concept_coverage_matrix = []
    rescued_by_formal_corpus = []
    genuinely_unmerged_across_ecosystem = []

    for cname, cn in sorted(chat_nodes.items(), key=lambda x: x[1]["centrality"] * math.log1p(x[1]["mentions"]), reverse=True):
        chat_m = cn["mentions"]
        irm_m = irm_nodes[cname]["mentions"] if cname in irm_nodes else 0
        formal_hits = {}
        total_formal_m = 0
        best_paper = None
        best_paper_m = 0

        for fk, fd in formal_docs.items():
            if cname in fd["nodes"]:
                m = fd["nodes"][cname]["mentions"]
                formal_hits[fk] = m
                total_formal_m += m
                if m > best_paper_m:
                    best_paper_m = m
                    best_paper = fd["file_name"]

        irm_ret = round(irm_m / max(chat_m, 1), 4)
        ecosystem_ret = round((irm_m + total_formal_m) / max(chat_m, 1), 4)

        status = "COVERED_IN_IRM_REPORT"
        if irm_m == 0 or irm_ret < 0.20:
            if total_formal_m >= max(3, int(chat_m * 0.20)):
                status = "RESCUED_BY_FORMAL_CORPUS"
            else:
                status = "UNMERGED_ECOSYSTEM_GAP"

        rec = {
            "concept": cname,
            "is_canonical": cn["is_canonical"],
            "chat_mentions": chat_m,
            "chat_centrality": cn["centrality"],
            "irm_report_mentions": irm_m,
            "formal_corpus_total_mentions": total_formal_m,
            "papers_covering_count": len(formal_hits),
            "top_formal_paper": best_paper or "None",
            "top_formal_paper_mentions": best_paper_m,
            "irm_retention_ratio": irm_ret,
            "full_ecosystem_retention_ratio": ecosystem_ret,
            "status": status
        }
        concept_coverage_matrix.append(rec)
        if status == "RESCUED_BY_FORMAL_CORPUS":
            rescued_by_formal_corpus.append(rec)
        elif status == "UNMERGED_ECOSYSTEM_GAP":
            genuinely_unmerged_across_ecosystem.append(rec)

    # Edge-level coverage across the entire IRM ecosystem
    ecosystem_edges = defaultdict(lambda: {"+I": 0, "-E": 0, "papers": set()})
    for d in [irm] + list(formal_docs.values()):
        for e in d["all_edges"]:
            u, v = sorted((e["source"], e["target"]))
            ecosystem_edges[(u, v)]["+I"] += e["inclusion_weight"]
            ecosystem_edges[(u, v)]["-E"] += e["exclusion_weight"]
            ecosystem_edges[(u, v)]["papers"].add(d["doc_id"])

    rescued_edges = []
    truly_missing_edges = []
    irm_direct_edges = {tuple(sorted((e["source"], e["target"]))) for e in irm["all_edges"]}

    for ce in chat["all_edges"]:
        if ce["total_weight"] < 3:
            continue
        key = tuple(sorted((ce["source"], ce["target"])))
        in_irm_report = key in irm_direct_edges
        eco = ecosystem_edges.get(key)
        if not in_irm_report:
            if eco and (eco["+I"] + eco["-E"]) >= 2:
                rescued_edges.append({
                    "source": key[0],
                    "target": key[1],
                    "chat_weight": ce["total_weight"],
                    "ecosystem_weight": eco["+I"] + eco["-E"],
                    "covered_by_papers": sorted(list(eco["papers"]))
                })
            else:
                truly_missing_edges.append({
                    "source": key[0],
                    "target": key[1],
                    "chat_weight": ce["total_weight"],
                    "chat_polarity": ce["net_polarity"],
                    "bond_type": ce["bond_type"]
                })

    return {
        "chat_frustrated_triangles_count": len(chat_frust),
        "irm_frustrated_triangles_count": len(irm_frust),
        "combined_seed_frustrated_count": len(combined_seed_frust),
        "resolved_across_formal_corpus_count": len(resolved_across_any_formal),
        "formal_corpus_triangle_resolution_rate": round(len(resolved_across_any_formal) / max(len(combined_seed_frust), 1), 4),
        "paper_triangle_audits": paper_triangle_audits,
        "concept_coverage_matrix": concept_coverage_matrix,
        "rescued_by_formal_corpus": rescued_by_formal_corpus,
        "genuinely_unmerged_across_ecosystem": genuinely_unmerged_across_ecosystem,
        "rescued_edges": rescued_edges[:25],
        "truly_missing_edges": truly_missing_edges[:25]
    }


def generate_report_v2(docs, eco_audit):
    lines = [
        "# Agent 5 (Round 2): 4-Color Gluon Gauge Physics, Proof Resolution Ratio & Full IRM Corpus Graph Audit",
        "",
        "## 1. Critique of `unified_gluon_dna_engine.py` & V2 Architectural Upgrades",
        "",
        "### 1.1 Architectural Flaw Identified in `unified_gluon_dna_engine.py`",
        "In Round 1's `unified_gluon_dna_engine.py`, the 4-Color Gluon forces (`Red`, `Green`, `Blue`, `Magenta`) were calculated by **globally summing modal counts across the entire document** (`wb = m.get('will_be', 0)`, `cntb = m.get('cant_be', 0)`, etc.) and taking a single static square-root cross-term:",
        "1. **Temporal & Causal Blindness**: Global aggregation cannot distinguish between a paper that *introduces* a 🔴 **Red** contradiction (`will_be <-> cant_be`) in Section 1 and *successfully resolves* it via 🟢 **Green** hypothesis testing (`can_be / may_be`) into 🔵 **Blue** / 🟣 **Magenta** theorem proofs by Section 5, versus a paper that leaves 🔴 **Red** contradictions unresolved right up to the conclusion.",
        "2. **Conflation of Co-Occurrence with Resolution**: In a rigorous proof (such as `ORTHODOX_BRIDGE_ZFC.md` or `Formal Paper 17 Navier-Stokes`), stating a classical impossibility theorem (`cant_be` / blow-up singularity) alongside an affirmative resolution (`will_be`) inflates the global Red score even when every single Red collision is immediately discharged by a formal derivation.",
        "",
        "### 1.2 The V2 Upgrade: Local-to-Global Causal Force Cascades & Proof Resolution Ratio ($\\mathcal{R}_{R \\to BM}$)",
        "In `gluon_transformer_v2.py`, we upgrade the Reading Head with a **2-tier Causal Gauge Tracker**:",
        "- **Local Sliding-Window Cascade Tracker**: Whenever a concept node triggers a local 🔴 **Red** contradiction spike at chunk $k$, the Reading Head scans the downstream causal window $[k+1, k+W]$ ($\\Delta t \\le 0.12$) on shared concept nodes to verify whether the spike is mediated by 🟢 **Green** operational testing (`can_be`, `may_be`) and locked into 🔵 **Blue** / 🟣 **Magenta** axiomatic proof (`will_be`, `theorem`, `proof`, `can_be`).",
        "- **Node-Level Early-to-Late Proof Resolution Ratio ($\\rho_i$)**:",
        "  $$\\rho_i = \\frac{\\text{Flux}_{\\text{Blue+Magenta}}^{\\text{late}}(i) + 0.35 \\cdot \\text{Flux}_{\\text{Green}}^{\\text{mid}}(i)}{\\max\\left(\\text{Flux}_{\\text{Red}}^{\\text{early}}(i) + \\text{Flux}_{\\text{Red}}^{\\text{late}}(i),\\, 0.5\\right)}$$",
        "- **Composite Epistemic Hygiene Score ($\\mathcal{H}_{\\text{epistemic}}$)**:",
        "  $$\\mathcal{H}_{\\text{epistemic}} = 0.50 \\cdot (1 - \\Phi_{\\text{frust}}) + 0.50 \\cdot \\mathcal{R}_{R \\to BM}$$",
        "  where $\\Phi_{\\text{frust}}$ is the **Signed Triangle Frustration Ratio** of the `[IS]` graph and $\\mathcal{R}_{R \\to BM}$ is the **Composite Proof Resolution Score**.",
        "",
        "---",
        "",
        "## 2. Master Benchmark Table: Chat vs. IRM Report vs. Full IRM Formal Corpus vs. Expanded arXiv Suite",
        "",
        "| Document ID | Category | Chars | $V$ | $E$ | $+I/-E$ | Frustrated $\\Delta$ ($\\Phi_{\\text{frust}}$) | 🔴 Red | 🟢 Green | 🔵 Blue | 🟣 Mag | Red Events | Cascade Resolved % | Node Proof Ratio $\\bar{\\rho}$ | Proof Score $\\mathcal{R}_{R\\to BM}$ | Epistemic Hygiene $\\mathcal{H}$ |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ]

    # Sort order: chat, irm, irm_formal, arxiv
    cat_order = {"dialogue": 0, "irm_synthesis": 1, "irm_formal": 2, "arxiv": 3}
    sorted_docs = sorted(docs.values(), key=lambda d: (cat_order.get(d["category"], 9), d["doc_id"]))

    for d in sorted_docs:
        th = d["topology_homology"]
        gf = d["global_gluon_forces"]["normalized"]
        pr = d["proof_resolution_metrics"]
        lines.append(
            f"| **{d['doc_id']}** | `{d['category']}` | {d['char_count']:,} | {th['vertices_V']} | {th['edges_E']} | "
            f"{th['inclusion_exclusion_ratio']:.1f} | **{th['frustration_ratio']:.2%}** ({th['frustrated_triangles']}/{th['triangles_total']}) | "
            f"{gf['Red']:.3f} | {gf['Green']:.3f} | {gf['Blue']:.3f} | {gf['Magenta']:.3f} | "
            f"{pr['red_contradiction_events']} | **{pr['cascade_resolution_rate']:.1%}** | `{pr['avg_node_proof_resolution_ratio']:.2f}` | "
            f"**`{pr['composite_proof_resolution_score']:.3f}`** | **`{th['epistemic_hygiene_score']:.3f}`** |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Red-to-Blue Proof Resolution & Signed Triangle Frustration Audit",
        "",
        "### 3.1 How the IRM Formal Papers Resolve Frustrated Triangles from `chat` and `Comprehensive Report - IRM`",
        f"- **Total Frustrated Triangles in `chat`**: `{eco_audit['chat_frustrated_triangles_count']}`",
        f"- **Total Frustrated Triangles in `Comprehensive Report - IRM`**: `{eco_audit['irm_frustrated_triangles_count']}`",
        f"- **Combined Seed Frustrated Triads (`chat` $\\cup$ `irm`)**: `{eco_audit['combined_seed_frustrated_count']}`",
        f"- **Seed Frustrated Triads Formally Resolved Across `irm_formal_corpus`**: **`{eco_audit['resolved_across_formal_corpus_count']}` (`{eco_audit['formal_corpus_triangle_resolution_rate']:.1%}` of all encountered triads)**",
        "",
        "| IRM Formal Paper | Own Triangles | Own Frustrated $\\Delta$ | Own Frustration % | Seed Frustrated Encountered | Seed Frustrated Resolved | Seed Resolution Rate | Sample Resolved Concept Triads ($+I/+I/+I$) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"
    ])

    for pa in eco_audit["paper_triangle_audits"]:
        samples = "; ".join(f"`{s}`" for s in pa["sample_resolved_triads"][:3]) or "—"
        lines.append(
            f"| **{pa['doc_id']}** (`{pa['file_name'][:30]}`) | {pa['own_triangles_total']} | {pa['own_frustrated_triangles']} | "
            f"**{pa['own_frustration_ratio']:.2%}** | {pa['seed_frustrated_triangles_encountered']} | "
            f"**{pa['seed_frustrated_triangles_resolved']}** | **{pa['seed_resolution_rate']:.1%}** | {samples} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 4. Multi-Paper Knowledge Graph Coverage: What the Formal Corpus Rescued vs. True Remaining Gaps",
        "",
        "### 4.1 Concepts Attenuated/Missing in `Comprehensive Report - IRM` that are **RESCUED** by `irm_formal_corpus`",
        "| Concept Node | Chat Mentions | IRM Report Mentions | Formal Corpus Mentions | Papers Covering | Top Formal Paper | Full Ecosystem Retention | Status |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |"
    ])

    for r in eco_audit["rescued_by_formal_corpus"]:
        lines.append(
            f"| `{r['concept']}` | {r['chat_mentions']} | {r['irm_report_mentions']} | **{r['formal_corpus_total_mentions']}** | "
            f"{r['papers_covering_count']} | `{r['top_formal_paper'][:32]}` ({r['top_formal_paper_mentions']}) | "
            f"**{r['full_ecosystem_retention_ratio']:.1%}** | `{r['status']}` |"
        )

    lines.extend([
        "",
        "### 4.2 Genuinely Unmerged Concepts Across the **Entire IRM Ecosystem** (True Residual Merge Candidates)",
        "| Concept Node | Chat Mentions | Chat Centrality | IRM Report Mentions | Formal Corpus Mentions | Full Ecosystem Retention | Status |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: |"
    ])

    for u in eco_audit["genuinely_unmerged_across_ecosystem"]:
        lines.append(
            f"| `{u['concept']}` | {u['chat_mentions']} | {u['chat_centrality']:.3f} | {u['irm_report_mentions']} | "
            f"{u['formal_corpus_total_mentions']} | {u['full_ecosystem_retention_ratio']:.1%} | **`{u['status']}`** |"
        )

    lines.extend([
        "",
        "### 4.3 Concept Bonds (`+I / -E` Edges) Rescued by `irm_formal_corpus` vs. Truly Missing Bonds",
        "#### A. Top Concept Bonds Missing in `IRM Report` but **Rescued** by `irm_formal_corpus`",
        "| Source Concept | Target Concept | Chat Weight | Formal Ecosystem Weight | Covered By Formal Papers |",
        "| :--- | :--- | :---: | :---: | :--- |"
    ])

    for re_edge in eco_audit["rescued_edges"][:12]:
        papers_str = ", ".join(f"`{p}`" for p in re_edge["covered_by_papers"][:4])
        lines.append(
            f"| `{re_edge['source']}` | `{re_edge['target']}` | {re_edge['chat_weight']} | **{re_edge['ecosystem_weight']}** | {papers_str} |"
        )

    lines.extend([
        "",
        "#### B. Top Concept Bonds **Truly Missing** Across the Entire IRM Ecosystem",
        "| Source Concept | Bond Type | Target Concept | Chat Weight | Chat Net Polarity |",
        "| :--- | :---: | :--- | :---: | :---: |"
    ])

    for me in eco_audit["truly_missing_edges"][:12]:
        lines.append(
            f"| `{me['source']}` | `{me['bond_type']}` | `{me['target']}` | **{me['chat_weight']}** | `{me['chat_polarity']:+.3f}` |"
        )

    lines.append("")
    return "\n".join(lines)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    docs = {}

    print("1. Scanning dialogue & synthesis baselines...")
    docs["chat"] = scan_document("chat", "dialogue", CHAT_PATH)
    docs["irm"] = scan_document("irm", "irm_synthesis", IRM_PATH)

    print("2. Scanning full IRM Formal Corpus...")
    if IRM_CORPUS_DIR.exists():
        for md_file in sorted(IRM_CORPUS_DIR.glob("*.md")):
            # Clean short doc_id
            stem = md_file.stem
            short_id = re.sub(r"[^a-zA-Z0-9_]+", "_", stem)[:28].strip("_")
            doc_key = f"irm_{short_id}"
            print(f"   -> {md_file.name} as [{doc_key}]")
            docs[doc_key] = scan_document(doc_key, "irm_formal", md_file)

    print("3. Scanning expanded arXiv benchmark suite...")
    if ARXIV_DIR.exists():
        for md_file in sorted(ARXIV_DIR.glob("*.md")):
            stem = md_file.stem.replace("arxiv_", "")
            doc_key = f"arxiv_{stem}"
            print(f"   -> {md_file.name} as [{doc_key}]")
            docs[doc_key] = scan_document(doc_key, "arxiv", md_file)

    print("4. Running Multi-Paper Triangle Frustration Resolution & Ecosystem Coverage Audit...")
    eco_audit = analyze_frustration_resolution_and_ecosystem_coverage(docs)

    # Strip bulk internal structures before saving JSON
    json_docs = {}
    for k, d in docs.items():
        d_copy = dict(d)
        d_copy.pop("all_edges", None)
        d_copy.pop("triangles_map", None)
        json_docs[k] = d_copy

    payload = {
        "agent": "Agent 5 (Round 2): 4-Color Gluon Gauge Physics, Proof Resolution Ratio & Cross-Corpus Graph Diffing v2",
        "documents": json_docs,
        "ecosystem_frustration_and_coverage_audit": eco_audit
    }

    results_v2_path = OUT_DIR / "results_v2.json"
    report_v2_path = OUT_DIR / "report_v2.md"

    results_v2_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    report_v2_path.write_text(generate_report_v2(docs, eco_audit), encoding="utf-8")

    print("\n=== AGENT 5 V2 SUMMARY ===")
    for k, d in docs.items():
        th = d["topology_homology"]
        pr = d["proof_resolution_metrics"]
        gf = d["global_gluon_forces"]["normalized"]
        print(
            f"[{k:32s}] V={th['vertices_V']:2d} E={th['edges_E']:3d} Frust={th['frustration_ratio']:6.2%} | "
            f"R={gf['Red']:.3f} G={gf['Green']:.3f} B={gf['Blue']:.3f} M={gf['Magenta']:.3f} | "
            f"CascadeRes={pr['cascade_resolution_rate']:5.1%} NodePR={pr['avg_node_proof_resolution_ratio']:.2f} "
            f"ProofScore={pr['composite_proof_resolution_score']:.3f} Hygiene={th['epistemic_hygiene_score']:.3f}"
        )

    print(f"\nSeed Frustrated Triangles (chat U irm): {eco_audit['combined_seed_frustrated_count']}")
    print(f"Resolved Across IRM Formal Corpus: {eco_audit['resolved_across_formal_corpus_count']} ({eco_audit['formal_corpus_triangle_resolution_rate']:.1%})")
    print(f"Rescued Concepts by IRM Formal Corpus: {[x['concept'] for x in eco_audit['rescued_by_formal_corpus']]}")
    print(f"Genuinely Unmerged Concepts Across Ecosystem: {[x['concept'] for x in eco_audit['genuinely_unmerged_across_ecosystem']]}")
    print(f"Saved: {results_v2_path} and {report_v2_path}")


if __name__ == "__main__":
    main()
