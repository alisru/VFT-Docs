#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Semantic Gluon & DNA Reading Head Engine (v3.5.0 — Dynamic Synthesis)
=============================================================================
Synthesizes all breakthroughs from the 5-agent evolutionary bake-off
across the 24-document corpus without any hardcoded document lookup tables:

  1. [The Son: 75M/25F]
     - Word-Level Causal Valence Shell Matrix (M_ij), tracking Antecedent
       Requirements (B) and Forward Obligations (F).
     - Strict conservation of syntactic obligations: Delta V -> 0 in formal proofs.
     - Semantic Optical Thickness (tau) and Luminescence (L = exp(-tau)).

  2. [The Daughter: 25M/75F]
     - Unsaid Horizon Boundary H(t) and 5-Tier Possibility Spectrum:
       (1_Impossible -> 2_Improbable -> 3_Plausible -> 4_Probable -> 5_Certain).
     - Topological Gauge Defect Closure (Delta_gauge) where unclosed strain forces
       specific defect-annihilating theorems into existence.

  3. [Agent 3 Patriarch: 85M/15F]
     - 3-Stage Ribosomal Splicing & Radiative Transfer:
       * Stage 1: Raw Un-spliced Pre-mRNA (tau_raw, L_raw = exp(-tau_raw))
       * Stage 2: Spliced Coding Exons (tau_spliced, Delta L_splice)
       * Stage 3: Mature Proof-Chained Operon (tau_mature, L_mature) with
                  stimulated optical clearing via contiguous proof operons.

  4. [Agent 5 Matriarch: 15M/85F]
     - Live [IS] Concept Graph & 4-Color Gluon Gauge Network.
     - Exact Signed Triangle Frustration (Phi_frust) computed by counting all
       3-cycles in the graph with negative parity (prod sign(e) = -1).
     - Dynamic Open Triadic Wedge Mining (u <-> v <-> w where u <-> w is unsaid).
     - Local-to-Global Proof Resolution Cascades (R_{R->BM}) inducing transparency.

  5. [Agent 1 Middle Kin: 60M/40F]
     - 4-Tier Working-Out Classification (Tier 0 Bare Assertion -> Tier 3 Formal Proof).
     - Derivation Law Valency Leakage (tracking Law 2 seeking can_be without closing).
"""

import os
import re
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
CHAT_PATH = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\chatgpt infinity maths.md")
IRM_SUMMARY_PATH = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md")
IRM_FORMAL_DIR = BASE_DIR / "irm_formal_corpus"
ARXIV_DIR = BASE_DIR / "arxiv_samples"

# ============================================================================
# 1. 8 MODAL STATES & 4 OPERATIONAL ENGINES (NO COLON INFLATION)
# ============================================================================
MODAL_PATTERNS = {
    # CONSTRUCTIVE (C: Inclusive + Counteractive)
    "is_like": [
        r"\bis\s+like\b", r"\brepresents?\b", r"\bis\s+defined\s+as\b", r"\bdefines?\b",
        r"\bform\s+of\b", r"\banalogous\s+to\b", r"\bcorresponds?\s+to\b",
        r"\bdenotes?\b", r"\bisomorphic\s+to\b", r"\bequivalent\s+to\b", r":="
    ],
    "may_be": [
        r"\bmay\s+be\b", r"\bmight\s+be\b", r"\bcould\s+be\b", r"\bsuppose\b",
        r"\bif\s+we\b", r"\bwhat\s+if\b", r"\bhypothes[ie]s\b", r"\bpotentially\b",
        r"\bimagine\b", r"\btentative(?:ly)?\b"
    ],
    # PRODUCTIVE (P: Inclusive + Active)
    "will_be": [
        r"\bwill\s+be\b", r"\bmust\s+be\b", r"\btherefore\b", r"\bthus\b",
        r"\byields?\b", r"\bresolves?\s+into\b", r"\bproves?\b", r"\bgenerates?\b",
        r"\bgives\b", r"\bresults?\s+in\b", r"\bnecessarily\b", r"\bit\s+follows\b",
        r"\bconsequently\b", r"\bhence\b", r"\\Rightarrow", r"\\implies", r"⟹"
    ],
    "can_be": [
        r"\bcan\s+be\b", r"\ballows?\b", r"\benables?\b", r"\bcapable\s+of\b",
        r"\bpossible\s+to\b", r"\bpermits?\b", r"\bsatisfies\b", r"\bobeys\b",
        r"\bbounded\s+by\b", r"\bconverges?\b", r"\badmits?\b"
    ],
    # REDUCTIVE (R: Exclusive + Active)
    "is_not": [
        r"\bis\s+not\b", r"\bisn't\b", r"\bare\s+not\b", r"\baren't\b",
        r"\bnot\s+a\b", r"\bdoes\s+not\b", r"\bdoesn't\b", r"\bdo\s+not\b",
        r"\bundefined\b", r"\brather\s+than\b", r"\binstead\s+of\b",
        r"\bdistinct\s+from\b", r"\bunlike\b", r"\\neq", r"!="
    ],
    "cant_be": [
        r"\bcannot\b", r"\bcan't\b", r"\bimpossible\b", r"\bindeterminate\b",
        r"\bnever\b", r"\bunable\s+to\b", r"\bcontradiction\b", r"\binconsistent\b",
        r"\bprohibited\b", r"\bforbidden\b", r"\bfails?\b", r"\bmeaningless\b",
        r"\bdiverge[sd]?\b", r"\bsingularity\b", r"\bparadox\b", r"\bblow-?up\b"
    ],
    # REGRESSIVE (G: Exclusive + Counteractive)
    "was_like": [
        r"\bclassical\s+view\b", r"\bclassically\b", r"\bstandard\s+math(?:ematics)?\b",
        r"\btraditionally\b", r"\bconventional(?:ly)?\b", r"\bpreviously\b",
        r"\bhistorically\b", r"\borthodox\b", r"\bused\s+to\b", r"\bold\s+view\b",
        r"\bcantorian\b", r"\bzfc\b"
    ],
    "wont_be": [
        r"\bwon't\b", r"\bwill\s+not\b", r"\bdrop(?:ped)?\b", r"\babandon(?:ed)?\b",
        r"\bdiscard(?:ed)?\b", r"\bomit(?:ted)?\b", r"\breject(?:ed)?\b", r"\bobsolete\b"
    ]
}

COMPILED_MODALS = {
    m: [re.compile(p, re.IGNORECASE) for p in pats]
    for m, pats in MODAL_PATTERNS.items()
}

# ============================================================================
# 2. CANONICAL CONCEPTS FOR LIVE GRAPH & TRIANGLE FRUSTRATION (AGENT 5)
# ============================================================================
CANONICAL_CONCEPTS = {
    "infinity_hierarchy": [r"\binfinit(?:y|ies)\b", r"\\infty", r"\bscaling level\b", r"\btransfinite\b"],
    "unit_power_infinity": [r"1\^\{?\\infty\}?", r"\bone to the infinity\b", r"1_n", r"0_\{?n\+1\}?"],
    "zero_state": [r"\bzero\b", r"\bnull state\b", r"0\^\{?\\infty\}?", r"\bvoid\b", r"\binfinitesimal\b"],
    "indefinite_irm": [r"\bindefinite\b", r"\birm\b", r"\bindeterminate form\b", r"\bdefinitional\b"],
    "relative_horizon": [r"\bhorizon\b", r"\bboundary\b", r"\basymptot(?:e|ic)\b", r"\bcutoff\b"],
    "shell_geometry": [r"\bshell\b", r"\bsphere\b", r"\bmanifold\b", r"\btopolog(?:y|ical)\b"],
    "heartbeat_oscillation": [r"\bheartbeat\b", r"\bpulse\b", r"\boscillat(?:e|ion)\b", r"\bfrequency\b"],
    "division_operator": [r"\bdivision\b", r"\bratio\b", r"\bquotient\b", r"\bfraction\b", r"0\s*/\s*0"],
    "potential_field": [r"\bpotential\b", r"\bvector field\b", r"\btensor\b", r"\bgradient\b"],
    "axiom_foundation": [r"\baxiom(?:atic|s)?\b", r"\bpostulate\b", r"\bfoundation\b", r"\bdefinition\b", r"\btheorem\b"],
    "digit_base_arithmetic": [r"\bradix\b", r"n\.d\.e\.f", r"\bcarry\b", r"\bdigit\b", r"\bbase[\s\-]b\b"],
    "calculus_analysis": [r"\bderivative\b", r"\bintegral\b", r"\blimit\b", r"\bcalculus\b", r"\bdifferential\b"],
    "algebraic_structure": [r"\bgroup\b", r"\bring\b", r"\bfield\b", r"\balgebra\b", r"\bisomorphism\b"],
    "cantor_zfc_set": [r"\bcantor\b", r"\bzfc\b", r"\bcardinal\b", r"\bpeano\b", r"\bultrafilter\b"],
    "levi_civita_nonarchimedean": [r"\blevi-civita\b", r"\bnon-archimedean\b", r"\bhahn\b", r"\bvaluation\b"],
    "navier_stokes_fluid": [r"\bnavier-stokes\b", r"\bvorticity\b", r"\benstrophy\b", r"\bviscosity\b", r"\blipschitz\b"]
}

COMPILED_CONCEPTS = {
    cname: [re.compile(p, re.IGNORECASE) for p in pats]
    for cname, pats in CANONICAL_CONCEPTS.items()
}

INCLUSION_PATTERNS = [
    re.compile(r"\b(?:includes|contains|implies|yields|produces|unifies|extends|forms|induces|couples|preserves|satisfies|is a)\b", re.I),
    re.compile(r"->|\\rightarrow|\\implies|=>|⟹", re.I)
]
EXCLUSION_PATTERNS = [
    re.compile(r"\b(?:excludes|contradicts|negates|rejects|eliminates|separates|annihilates|conflicts with|forbids|violates)\b", re.I),
    re.compile(r"!=|\\neq|≠", re.I)
]

# ============================================================================
# 3. 16 MATHEMATICAL TOPIC GENES (AGENT 3 PATRIARCH)
# ============================================================================
TOPIC_GENES_V3 = {
    "LCF": ("Levi-Civita Field, Hahn Series & Valuation", [
        r"levi-civita", r"hahn", r"valuation", r"non-archimedean",
        r"infinitesimal", r"d\^k", r"puiseux", r"ordered\s+field"
    ]),
    "BAI": ("Baire Space, Prefix Ultrametric & Tree Topology", [
        r"baire", r"ultrametric", r"prefix", r"p-adic",
        r"cauchy\s+completion", r"tree\s+topology", r"cylinder\s+set"
    ]),
    "RAD": ("Radix [base_n.d.e.f] Dictionary & Carry Normalization", [
        r"n\.d\.e\.f", r"radix", r"carry", r"normali[sz]ation",
        r"positional", r"digit\s+expansion", r"mantissa", r"base[\s\-]b"
    ]),
    "PLK": ("Planck Scale Cutoffs (c/l_P) & Cellular Horizon", [
        r"planck", r"l_p\b", r"cutoff", r"c/l_p", r"quantum\s+limit",
        r"physical\s+bound", r"horizon", r"maximum\s+frequency"
    ]),
    "NVS": ("3D Cellular Navier-Stokes PDEs & Dyadic Enstrophy", [
        r"navier-stokes", r"enstrophy", r"vorticity", r"dyadic",
        r"viscous", r"gr[oö]nwall", r"sobolev", r"leray", r"blow-?up"
    ]),
    "ZFC": ("ZFC Peano Axioms, Ultrafilters & Transfinite Bridge", [
        r"zfc", r"peano", r"ultrafilter", r"compactness\s+theorem",
        r"standard\s+analysis", r"cantor"
    ]),
    "SYM": ("Topological G-Bundles, Gauge Symmetry & Holonomy", [
        r"g-bundle", r"holonomy", r"gauge\s+symmetry", r"principal\s+bundle",
        r"connection\s+form", r"curvature\s+2-form", r"yang-mills"
    ]),
    "CIR": ("Circle Loop Formula, Trigonometric & Polar Dynamics", [
        r"loop\s+formula", r"polar\s+coordinate", r"angular\s+velocity",
        r"trigonometric", r"unit\s+circle"
    ]),
    "DIV": ("Division by Zero, Indeterminate Form & Algebraic Resolution", [
        r"0\s*/\s*0", r"1\s*/\s*0", r"division\s+by\s+zero",
        r"indeterminate\s+form", r"algebraic\s+resolution"
    ]),
    "COH": ("Simplicial Homology, Sheaf Cohomology & Betti Numbers", [
        r"cohomology", r"simplicial", r"betti\s+number", r"chain\s+complex",
        r"boundary\s+operator", r"exterior\s+derivative"
    ]),
    "RMN": ("Riemann Zeta, Spectral Realization & Fredholm Determinants", [
        r"riemann\s+zeta", r"critical\s+line", r"fredholm",
        r"eigenvalues?", r"spectral\s+realization", r"zeta\s+function"
    ])
}

COMPILED_GENES_V3 = {
    g_id: (name, [re.compile(p, re.IGNORECASE) for p in pats])
    for g_id, (name, pats) in TOPIC_GENES_V3.items()
}

# ============================================================================
# 4. PROOF SCAFFOLDING & CAUSAL VALENCE TOKENS (THE SON & AGENT 1)
# ============================================================================
PROOF_PATTERNS = {
    "scaffolding": [
        r"\b(?:Theorem|Lemma|Proposition|Corollary|Definition|Axiom|Proof)\b",
        r"\bQ\.?E\.?D\.?\b", r"\\blacksquare", r"\\square", r"∎", r"□",
        r"\bCase\s+\d+\b", r"\bStep\s+\d+\b"
    ],
    "deductive": [
        r"\b(?:since|because|it\s+follows\s+that|we\s+obtain|we\s+have|we\s+conclude)\b",
        r"\b(?:substituting|applying|integrating|differentiating|by\s+induction)\b",
        r"\\implies", r"\\iff", r"\\mapsto", r"⟹", r"⟺"
    ],
    "symbolic_eq": [
        r"\$\$[\s\S]+?\$\$", r"\\\[[\s\S]+?\\\]", r"\\begin\{(?:equation|align)\*?\}",
        r"[a-zA-Z0-9_\)\]\}]\s*(?:=|<|>|\\le|\\ge|\\leq|\\geq|\\approx|\\equiv)\s*[a-zA-Z0-9_\(\[\{]"
    ]
}

COMPILED_PROOF = {
    cat: [re.compile(p, re.IGNORECASE) for p in pats]
    for cat, pats in PROOF_PATTERNS.items()
}

FORWARD_VALENCE_TOKENS = {
    "will", "must", "shall", "let", "define", "suppose", "assume",
    "implies", "proves", "yields", "therefore", "hence", "thus"
}
BACKWARD_VALENCE_TOKENS = {
    "because", "since", "given", "by", "from", "using", "substituting",
    "applying", "recalling", "where", "as"
}

# ============================================================================
# 5. CORE ANALYSIS PIPELINE FOR A SINGLE DOCUMENT (ZERO HARDCODING)
# ============================================================================
def analyze_document_v3(doc_id: str, filepath: Path, group: str) -> dict:
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    lines = text.splitlines()
    total_lines = len(lines)

    # Segment into conceptual paragraphs / blocks
    raw_blocks = re.split(r"\n\s*\n", text)
    blocks = [b.strip() for b in raw_blocks if len(b.strip()) > 15]
    n_blocks = max(len(blocks), 1)

    codons = []
    w_work_values = []
    var_carryovers = []
    tau_raw_values = []
    tau_spliced_values = []
    lum_raw_values = []
    lum_spliced_values = []

    proof_state_totals = Counter()
    tier_totals = Counter()
    gene_totals = Counter()
    modal_totals = Counter()

    # Track symbols for variable carryover kappa_var
    doc_symbols_seen = set()

    # 4-Color Gluon Force registers
    color_charges = {"Red": 0.0, "Green": 0.0, "Blue": 0.0, "Magenta": 0.0}

    # Causal Valence Bookkeeping (The Son)
    total_forward_obligations = 0
    total_backward_requirements = 0
    forward_tokens_closed = 0
    backward_tokens_justified = 0

    # Contiguous proof chaining for stimulated optical clearing (Agent 3)
    k_proof_current = 0
    k_proof_max = 0

    # Incomplete Derivation Valency Leakage (Agent 1)
    law2_seeking_can_be_leaks = 0

    # Live Concept Graph for Signed Triangle Frustration (Agent 5)
    concept_mentions = Counter()
    edges = defaultdict(lambda: {"+I": 0, "-E": 0})
    chunk_concept_records = []

    for idx, block in enumerate(blocks):
        # 1. Gene Classification
        gene_matches = Counter()
        for g_id, (g_name, g_regexes) in COMPILED_GENES_V3.items():
            for rgx in g_regexes:
                cnt = len(rgx.findall(block))
                if cnt > 0:
                    gene_matches[g_id] += cnt

        dominant_gene = gene_matches.most_common(1)[0][0] if gene_matches else "INT"
        is_exon = (dominant_gene != "INT")
        gene_totals[dominant_gene] += 1

        # 2. Modal Evaluation
        m_counts = Counter()
        for m, regexes in COMPILED_MODALS.items():
            for rgx in regexes:
                cnt = len(rgx.findall(block))
                if cnt > 0:
                    m_counts[m] += cnt
                    modal_totals[m] += cnt

        # 3. Concept Graph Tracking (Agent 5)
        active_concepts = []
        for cname, regexes in COMPILED_CONCEPTS.items():
            if any(rgx.search(block) for rgx in regexes):
                active_concepts.append(cname)
                concept_mentions[cname] += 1

        chunk_concept_records.append({
            "block_idx": idx,
            "concepts": active_concepts,
            "modals": dict(m_counts)
        })

        if len(active_concepts) >= 2:
            inc_hits = sum(len(rgx.findall(block)) for rgx in INCLUSION_PATTERNS)
            exc_hits = sum(len(rgx.findall(block)) for rgx in EXCLUSION_PATTERNS)
            is_neg_modal = (m_counts["is_not"] + m_counts["cant_be"] + m_counts["wont_be"]) > 0

            for i in range(len(active_concepts)):
                for j in range(i + 1, len(active_concepts)):
                    u, v = sorted((active_concepts[i], active_concepts[j]))
                    if exc_hits > 0 or is_neg_modal:
                        edges[(u, v)]["-E"] += max(1, exc_hits)
                    if inc_hits > 0 or not is_neg_modal:
                        edges[(u, v)]["+I"] += max(1, inc_hits)

        # 4. Proof Scaffolding & Working Out
        scaff_hits = sum(len(rgx.findall(block)) for rgx in COMPILED_PROOF["scaffolding"])
        deduct_hits = sum(len(rgx.findall(block)) for rgx in COMPILED_PROOF["deductive"])
        symb_hits = sum(len(rgx.findall(block)) for rgx in COMPILED_PROOF["symbolic_eq"])

        # Extract mathematical variables/tokens
        block_symbols = set(re.findall(r"\b[a-zA-Z](?:_[a-zA-Z0-9]+)?\b", block))
        overlap = len(block_symbols & doc_symbols_seen)
        kappa_var = round(overlap / max(len(block_symbols), 1), 4)
        doc_symbols_seen.update(block_symbols)
        var_carryovers.append(kappa_var)

        # Working-Out Wave & Proof State
        eq_density = min(symb_hits / 3.0, 1.0)
        chain_density = min((scaff_hits + deduct_hits) / 2.0, 1.0)
        w_work = round(math.sqrt(eq_density * max(chain_density, 0.05)) * (0.5 + 0.5 * kappa_var), 4)
        w_work_values.append(w_work)

        if (symb_hits >= 2 and (deduct_hits >= 1 or scaff_hits >= 1)) or (symb_hits >= 3):
            proof_state = "W"  # Formal Working-Out Proof
            k_proof_current += 1.0 + 0.5 * min(symb_hits, 4)
        elif symb_hits >= 1 or scaff_hits >= 1:
            proof_state = "F"  # Formal Equation / Structural Lens
            k_proof_current = max(0.5, k_proof_current * 0.5 + 0.5)
        else:
            proof_state = "A"  # Prose Assertion / Fluff
            k_proof_current = 0

        k_proof_max = max(k_proof_max, k_proof_current)
        proof_state_totals[proof_state] += 1

        # 4-Tier Working-Out Classification (Agent 1)
        w_score = round(0.35 * eq_density + 0.35 * chain_density + 0.15 * min(scaff_hits, 2) / 2.0 + 0.15 * kappa_var, 4)
        if w_score >= 0.40 and symb_hits >= 2:
            tier = "Tier3_Formal_Proof"
        elif w_score >= 0.22 and symb_hits >= 1:
            tier = "Tier2_Operational_Derivation"
        elif w_score >= 0.10 or proof_state == "F":
            tier = "Tier1_Exploratory_Sketch"
        else:
            tier = "Tier0_Bare_Assertion"
        tier_totals[tier] += 1

        # Check Law 2 Dangling Syntactic Bond (is_not + is_like without can_be/will_be)
        if (m_counts["is_not"] >= 1 and m_counts["is_like"] >= 1) and (m_counts["can_be"] == 0 and m_counts["will_be"] == 0):
            law2_seeking_can_be_leaks += 1

        # 5. Causal Valence Bookkeeping (The Son)
        words = re.findall(r"\b[a-zA-Z]+\b", block.lower())
        for w in words:
            if w in FORWARD_VALENCE_TOKENS:
                total_forward_obligations += 1
                if proof_state in {"W", "F"}:
                    forward_tokens_closed += 1
            if w in BACKWARD_VALENCE_TOKENS:
                total_backward_requirements += 1
                if kappa_var > 0.3 or deduct_hits > 0:
                    backward_tokens_justified += 1

        # 6. 4-Color Gluon Forces (The Matriarch)
        color_charges["Red"] += (m_counts["will_be"] * m_counts["cant_be"] + m_counts["is_like"] * m_counts["wont_be"]) * 1.5
        color_charges["Green"] += (m_counts["can_be"] * m_counts["is_not"] + m_counts["may_be"] * m_counts["was_like"]) * 1.2
        color_charges["Blue"] += (m_counts["will_be"] * m_counts["may_be"] + m_counts["wont_be"] * m_counts["is_not"]) * 1.3
        color_charges["Magenta"] += (m_counts["is_like"] * m_counts["can_be"] + m_counts["was_like"] * m_counts["cant_be"]) * 1.1

        # 7. Optical Thickness (tau) & Luminescence (L = exp(-tau))
        if dominant_gene == "INT":
            t_raw = 2.45 + 0.30 * min(len(words) / 50.0, 1.0)
        else:
            t_raw = max(0.10, 2.10 - 1.20 * eq_density - 0.80 * chain_density + 0.35 * (1.0 if proof_state == "A" else 0.0))

        if is_exon:
            t_spliced = max(0.08, t_raw - 0.75 - 0.30 * kappa_var)
        else:
            t_spliced = t_raw

        tau_raw_values.append(round(t_raw, 4))
        tau_spliced_values.append(round(t_spliced, 4))
        lum_raw_values.append(round(math.exp(-t_raw), 4))
        lum_spliced_values.append(round(math.exp(-t_spliced), 4))

        codons.append({
            "block_idx": idx,
            "gene": dominant_gene,
            "is_exon": is_exon,
            "proof_state": proof_state,
            "tier": tier,
            "tau_raw": t_raw,
            "tau_spliced": t_spliced
        })

    # ========================================================================
    # DYNAMIC GRAPH TRIANGLE FRUSTRATION CALCULATION (ZERO HARDCODING)
    # ========================================================================
    adj = defaultdict(set)
    edge_signs = {}
    for (u, v), edata in edges.items():
        w_inc = edata["+I"]
        w_exc = edata["-E"]
        sign = 1 if w_inc >= w_exc else -1
        edge_signs[(u, v)] = sign
        edge_signs[(v, u)] = sign
        adj[u].add(v)
        adj[v].add(u)

    node_list = sorted(concept_mentions.keys())
    total_triangles = 0
    frustrated_triangles = 0
    triangles_list = []

    for i in range(len(node_list)):
        u = node_list[i]
        for j in range(i + 1, len(node_list)):
            v = node_list[j]
            if v not in adj[u]:
                continue
            for k in range(j + 1, len(node_list)):
                w = node_list[k]
                if w in adj[u] and w in adj[v]:
                    prod = edge_signs[(u, v)] * edge_signs[(v, w)] * edge_signs[(u, w)]
                    total_triangles += 1
                    if prod < 0:
                        frustrated_triangles += 1
                        triangles_list.append((u, v, w))

    if total_triangles > 0:
        frustration_pct = round(100.0 * frustrated_triangles / total_triangles, 2)
    else:
        # Fallback to local red strain if document has no closed 3-cycles
        frustration_pct = round(max(0.0, (color_charges["Red"] / max(sum(color_charges.values()), 1.0)) * 5.0), 2)

    # Dynamic Open Wedge Mining (The Daughter & Agent 5)
    open_wedges_count = 0
    total_possible_wedges = 0
    for v in node_list:
        neighbors = sorted(adj[v])
        for i in range(len(neighbors)):
            u = neighbors[i]
            for j in range(i + 1, len(neighbors)):
                w = neighbors[j]
                total_possible_wedges += 1
                if w not in adj[u]:
                    open_wedges_count += 1

    open_wedge_defect_pct = round(100.0 * open_wedges_count / max(total_possible_wedges, 1), 2)

    # Stage 3 Mature Proof Operon Optical Clearing (Agent 3 Patriarch)
    tau_mature_values = []
    lum_mature_values = []
    k_proof_decay = 0.0
    for c in codons:
        if c["proof_state"] == "W":
            k_proof_decay += 1.5
        elif c["proof_state"] == "F":
            k_proof_decay = max(0.5, k_proof_decay * 0.7 + 0.5)
        else:
            k_proof_decay = max(0.0, k_proof_decay * 0.4 - 0.2)

        clearing_boost = 0.15 * math.log1p(k_proof_decay)
        t_mature = max(0.05, c["tau_spliced"] - clearing_boost)
        tau_mature_values.append(round(t_mature, 4))
        lum_mature_values.append(round(math.exp(-t_mature), 4))

    mean_tau_raw = round(sum(tau_raw_values) / n_blocks, 4)
    mean_tau_spliced = round(sum(tau_spliced_values) / n_blocks, 4)
    mean_tau_mature = round(sum(tau_mature_values) / n_blocks, 4)

    mean_lum_raw = round(sum(lum_raw_values) / n_blocks, 4)
    mean_lum_spliced = round(sum(lum_spliced_values) / n_blocks, 4)
    mean_lum_mature = round(sum(lum_mature_values) / n_blocks, 4)

    clarification_factor = round(mean_lum_mature / max(mean_lum_raw, 0.001), 3)

    # Causal Valence Conservation (The Son)
    tot_valence_reqs = total_forward_obligations + total_backward_requirements
    tot_valence_justified = forward_tokens_closed + backward_tokens_justified
    valence_conservation_pct = round(100.0 * tot_valence_justified / max(tot_valence_reqs, 1), 2)
    delta_valence_deficit = max(0, tot_valence_reqs - tot_valence_justified)

    # 4-Color Normalization
    tot_color = max(sum(color_charges.values()), 1.0)
    norm_colors = {c: round(v / tot_color, 4) for c, v in color_charges.items()}
    red_strain = norm_colors["Red"]
    blue_green_bridge = norm_colors["Blue"] + norm_colors["Green"]

    # Gluon-Induced Transparency
    proof_resolution_rate = round(blue_green_bridge / max(red_strain + blue_green_bridge, 0.01), 3)
    tau_effective = round(max(0.05, mean_tau_mature * (1.0 - 0.35 * proof_resolution_rate) + 0.10 * (frustration_pct / 100.0)), 4)
    lum_effective = round(math.exp(-tau_effective), 4)
    optical_clearing_gain = round(lum_effective - mean_lum_raw, 4)

    # The Daughter's Unsaid Horizon Prediction Check
    delta_gauge_defect = round(red_strain * (1.0 - proof_resolution_rate) * 10.0 + (frustration_pct / 10.0), 2)
    if delta_gauge_defect >= 3.0:
        horizon_band = "5_Certain_Topologically_Forced"
    elif delta_gauge_defect >= 2.0:
        horizon_band = "4_Probable"
    elif delta_gauge_defect >= 1.0:
        horizon_band = "3_Plausible"
    elif delta_gauge_defect >= 0.4:
        horizon_band = "2_Improbable"
    else:
        horizon_band = "1_Equilibrium_Closed"

    # Exon and Tier Aggregates
    exon_codons = [c for c in codons if c["is_exon"]]
    n_exons = max(len(exon_codons), 1)
    exon_w_pct = round(100.0 * sum(1 for c in exon_codons if c["proof_state"] == "W") / n_exons, 2)
    exon_f_pct = round(100.0 * sum(1 for c in exon_codons if c["proof_state"] == "F") / n_exons, 2)
    exon_a_pct = round(100.0 * sum(1 for c in exon_codons if c["proof_state"] == "A") / n_exons, 2)
    coding_density_pct = round(100.0 * len(exon_codons) / n_blocks, 2)

    # Master Veritas Rigor Score (/100)
    veritas_score = round(
        min(
            100.0,
            0.30 * min(exon_w_pct * 2.0, 100.0)
            + 0.25 * min(valence_conservation_pct * 1.3, 100.0)
            + 0.25 * min(mean_lum_mature * 140.0, 100.0)
            + 0.20 * max(0.0, 100.0 - frustration_pct * 5.0)
        ),
        2
    )

    return {
        "doc_id": doc_id,
        "group": group,
        "lines": total_lines,
        "blocks": n_blocks,
        "coding_density_pct": coding_density_pct,
        "exon_w_proof_pct": exon_w_pct,
        "exon_f_eq_pct": exon_f_pct,
        "exon_a_prose_pct": exon_a_pct,
        "radiative_transfer": {
            "tau_raw_unspliced": mean_tau_raw,
            "tau_spliced_exons": mean_tau_spliced,
            "tau_mature_operons": mean_tau_mature,
            "tau_effective_post_proof": tau_effective,
            "luminescence_raw": mean_lum_raw,
            "luminescence_spliced": mean_lum_spliced,
            "luminescence_mature": mean_lum_mature,
            "luminescence_effective": lum_effective,
            "splicing_gain_pct": round(100.0 * (mean_lum_spliced - mean_lum_raw) / max(mean_lum_raw, 0.001), 1),
            "total_clarification_factor": clarification_factor,
            "optical_clearing_gain_delta_L": optical_clearing_gain
        },
        "causal_valence": {
            "forward_obligations": total_forward_obligations,
            "backward_requirements": total_backward_requirements,
            "obligations_conserved_pct": valence_conservation_pct,
            "valence_deficit": delta_valence_deficit,
            "law2_seeking_can_be_leaks": law2_seeking_can_be_leaks
        },
        "gluon_gauge_forces": {
            "normalized_colors": norm_colors,
            "graph_vertices_count": len(concept_mentions),
            "graph_edges_count": len(edges),
            "graph_triangles_total": total_triangles,
            "graph_triangles_frustrated": frustrated_triangles,
            "triangle_frustration_pct": frustration_pct,
            "open_wedge_defect_pct": open_wedge_defect_pct,
            "proof_resolution_rate": proof_resolution_rate,
            "gauge_defect_tension": delta_gauge_defect,
            "unsaid_horizon_band": horizon_band
        },
        "tier_distribution": dict(tier_totals),
        "gene_totals": dict(gene_totals),
        "veritas_rigor_score": veritas_score
    }


def main():
    docs = []
    print("=== RUNNING DYNAMIC UNIFIED SEMANTIC GLUON & DNA ENGINE v3.5.0 ===")
    print("Processing Ancestral Dialogue...")
    docs.append(analyze_document_v3("chatgpt_infinity_maths", CHAT_PATH, "1_Ancestral_Chat"))

    print("Processing Early Summary Report...")
    docs.append(analyze_document_v3("Comprehensive_Report_IRM_Summary", IRM_SUMMARY_PATH, "2_Early_IRM_Summary"))

    print("Processing Formal IRM Corpus (14 papers)...")
    for fname in sorted(os.listdir(IRM_FORMAL_DIR)):
        if fname.endswith(".md"):
            docs.append(analyze_document_v3(fname[:-3], IRM_FORMAL_DIR / fname, "3_IRM_Formal_Corpus"))

    print("Processing arXiv Benchmark Controls (8 papers)...")
    for fname in sorted(os.listdir(ARXIV_DIR)):
        if fname.endswith(".md"):
            docs.append(analyze_document_v3(fname[:-3], ARXIV_DIR / fname, "4_arXiv_Benchmark"))

    out_json = BASE_DIR / "unified_results_v3.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"engine_version": "v3.5.0", "documents": docs}, f, indent=2)

    print(f"\nSaved Fully Dynamic Dataset: {out_json} ({len(docs)} documents analyzed)")
    print("=" * 125)
    print(f"{'Document Group':<26} {'Count':>5} {'Mean Exon%':>11} {'Proof W%':>9} {'Tau Mature':>11} {'Lum Mature':>11} {'Valence Cons%':>14} {'Frust%':>8} {'Wedge%':>8} {'Veritas':>9}")
    print("-" * 125)

    for g in ["1_Ancestral_Chat", "2_Early_IRM_Summary", "3_IRM_Formal_Corpus", "4_arXiv_Benchmark"]:
        sub = [d for d in docs if d["group"] == g]
        cnt = len(sub)
        avg_exon = sum(d["coding_density_pct"] for d in sub) / cnt
        avg_w = sum(d["exon_w_proof_pct"] for d in sub) / cnt
        avg_tau = sum(d["radiative_transfer"]["tau_mature_operons"] for d in sub) / cnt
        avg_lum = sum(d["radiative_transfer"]["luminescence_mature"] for d in sub) / cnt
        avg_val = sum(d["causal_valence"]["obligations_conserved_pct"] for d in sub) / cnt
        avg_frust = sum(d["gluon_gauge_forces"]["triangle_frustration_pct"] for d in sub) / cnt
        avg_wedge = sum(d["gluon_gauge_forces"]["open_wedge_defect_pct"] for d in sub) / cnt
        avg_veritas = sum(d["veritas_rigor_score"] for d in sub) / cnt

        print(f"{g:<26} {cnt:>5} {avg_exon:>10.1f}% {avg_w:>8.1f}% {avg_tau:>11.4f} {avg_lum:>11.4f} {avg_val:>13.1f}% {avg_frust:>7.2f}% {avg_wedge:>7.1f}% {avg_veritas:>9.2f}")

    print("=" * 125)

if __name__ == "__main__":
    main()
