#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent 3: Bioinformatics Codon & Smith-Waterman DNA Homology Aligner
Semantic Gluon Transformer & Ribosomal DNA Reading Head
"""

import os
import re
import json
import math
from pathlib import Path
from collections import Counter, defaultdict

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics")
OUT_DIR = BASE_DIR / "semantic_gluon_dna" / "agent_3_bio_dna_aligner"
CHAT_PATH = BASE_DIR / "chatgpt infinity maths.md"
IRM_PATH = BASE_DIR / "Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md"
ARXIV_DIR = BASE_DIR / "semantic_gluon_dna" / "arxiv_samples"

# ============================================================================
# 1. RIBOSOMAL GENETIC CODE DEFINITIONS
# ============================================================================

# Base 1: Engine Nucleotide (4 bases: C, P, R, G)
ENGINE_PATTERNS = {
    "C": [  # Constructive: definitions, axioms, structural framing, building
        r"\bdefine[ds]?\b", r"\bdefinition\b", r"\blet\s+", r"\bdenote[ds]?\b",
        r"\baxiom\b", r"\bstructure\b", r"\bframework\b", r"\brepresent[s]?\b",
        r"\bconsist[s]?\b", r"\bformally\b", r"\bconstruct\b", r"\bpostulate\b",
        r"\bnotation\b", r"\bidentity\b", r"\bis\s+defined\s+as\b", r"==="
    ],
    "P": [  # Productive: derivation, proof, implication, generation, operation
        r"\btherefore\b", r"\bthus\b", r"\bhence\b", r"\byields?\b",
        r"\bgenerates?\b", r"\bproduces?\b", r"\bderives?\b", r"\bfollows\s+that\b",
        r"\bimplies\b", r"\bcompute[ds]?\b", r"\bcalculate[ds]?\b", r"\btheorem\b",
        r"\bproof\b", r"\bcorollary\b", r"\bexpand[s]?\b", r"\btransform[s]?\b",
        r"\bevolve[s]?\b", r"\bconverge[s]?\b", r"\bmap[s]?\b", r"\\Rightarrow", r"\\implies"
    ],
    "R": [  # Reductive: critique, testing, falsification, boundary constraint, contrast
        r"\bhowever\b", r"\bbut\b", r"\bcontradict[s]?\b", r"\bfails?\b",
        r"\bcannot\b", r"\binvalid\b", r"\bparadox\b", r"\blimitation\b",
        r"\berror\b", r"\bmistake\b", r"\bproblem\b", r"\bbreakdown\b",
        r"\binconsistent\b", r"\bdiscard\b", r"\breject[s]?\b", r"\bunlike\b",
        r"\bwhereas\b", r"\bin\s+contrast\b"
    ],
    "G": [  # Regressive: recursive loopback, origin trace, meta-reflection, chat filler
        r"\brecall\b", r"\bearlier\b", r"\bpreviously\b", r"\bback\s+to\b",
        r"\brevisit\b", r"\bas\s+we\s+saw\b", r"\bin\s+summary\b", r"\bwait\b",
        r"\bhmm\b", r"\blet's\s+think\b", r"\brecap\b", r"\borigin\b",
        r"\bmeta\b", r"\bself-referential\b", r"\bquestion\b"
    ]
}

# Base 2: Modal & Inclusive/Exclusive Polarity Base (8 bases: 4 +I, 4 -E)
# Inclusive (+I): W (will be / necessary law), A (can be / operational capacity),
#                 M (may be / exploratory hypothesis), L (is like / structural isomorphism)
# Exclusive (-E): N (is not / direct negation), X (can't be / impossibility),
#                 O (won't be / asymptotic divergence/refusal), H (was like / superseded model)
MODAL_PATTERNS = {
    # Inclusive (+I)
    "W": [r"\bwill\s+be\b", r"\bmust\s+be\b", r"\bnecessarily\b", r"\balways\b", r"\binvariably\b", r"\bshall\b", r"\blaw\b", r"\binvariant\b"],
    "A": [r"\bcan\s+be\b", r"\bable\s+to\b", r"\ballows?\b", r"\benables?\b", r"\bcapable\b", r"\bpermits?\b", r"\bcan\s+write\b", r"\bcan\s+express\b"],
    "M": [r"\bmay\s+be\b", r"\bmight\b", r"\bcould\s+be\b", r"\bperhaps\b", r"\bpossibly\b", r"\bsuppose\b", r"\bwhat\s+if\b", r"\bhypothesis\b", r"\bconjecture\b", r"\bseems\b"],
    "L": [r"\bis\s+like\b", r"\banalogous\b", r"\bcorresponds?\s+to\b", r"\bisomorphic\b", r"\bequivalent\s+to\b", r"\bacts\s+as\b", r"\bmirrors?\b", r"\bresembles?\b", r"\bis\s+a\b"],
    # Exclusive (-E)
    "N": [r"\bis\s+not\b", r"\bare\s+not\b", r"\bnot\s+equal\b", r"\bneq\b", r"\\neq", r"\brather\s+than\b", r"\binstead\s+of\b", r"\bnever\b", r"\bno\s+longer\b", r"\bdistinct\s+from\b"],
    "X": [r"\bcannot\b", r"\bcan't\b", r"\bimpossible\b", r"\bforbidden\b", r"\bundefined\b", r"\billegal\b", r"\bno\s+solution\b", r"\bunsolvable\b", r"\bprohibit[s]?\b"],
    "O": [r"\bwon't\b", r"\bwill\s+not\b", r"\bdoes\s+not\s+converge\b", r"\bdiverges?\b", r"\bfails\s+to\b", r"\brefuses?\b", r"\basymptotic\b", r"\bnever\s+reaches\b"],
    "H": [r"\bwas\s+like\b", r"\bused\s+to\b", r"\bclassically\b", r"\btraditionally\b", r"\bstandard\s+view\b", r"\bold\s+model\b", r"\bconventionally\b", r"\bnaive\b", r"\borthodox\b"]
}

INCLUSIVE_BASES = {"W", "A", "M", "L"}
EXCLUSIVE_BASES = {"N", "X", "O", "H"}

# Base 3: Topic Gene Code (12 canonical genes + INT for non-coding intron)
TOPIC_GENES = {
    "SEQ": {
        "name": "Recursive Sequence Hierarchy (1^inf_n = 0^inf_{n+1})",
        "patterns": [
            r"1\^\{\\infty\}", r"0\^\{\\infty\}", r"1\^\\infty", r"0\^\\infty",
            r"1\^∞", r"0\^∞", r"\b_\{n\+1\}\b", r"\bhierarchy\s+of\s+infinit",
            r"\blevel\s+n\b", r"\btier[s]?\b", r"\brecursive\s+horizon\b", r"\bstep-index",
            r"\bn\+1\b", r"\bscale\s+level\b", r"\bunit\s+at\s+level\b"
        ]
    },
    "IND": {
        "name": "Indefinite Number Decomposition (X = [x] + x_eps)",
        "patterns": [
            r"\bindefinite\b", r"\bINDEF\b", r"x_\\varepsilon", r"x_\\epsilon",
            r"\[x\]", r"\bdefinite\s+part\b", r"\bindefinite\s+part\b",
            r"\binfinitesimal\b", r"\\varepsilon", r"\\epsilon", r"\bresidue\b",
            r"\bfluctuation\b", r"\bunresolved\s+part\b"
        ]
    },
    "CHI": {
        "name": "Holographic / Chi Vector & Tensor Geometry",
        "patterns": [
            r"\\chi\b", r"\bchi\b", r"\bholographic\b", r"\bvector\b",
            r"\btensor\b", r"\bprojection\b", r"\bmanifold\b", r"\bphase\s+space\b",
            r"\bdual\s+space\b", r"\borthogonal\b", r"\bmetric\b", r"\bcurvature\b",
            r"\bcoordinate\b", r"\bfield\b"
        ]
    },
    "PI": {
        "name": "Pi Exploration / Irrationality / Angular Closure",
        "patterns": [
            r"\\pi\b", r"\bpi\b", r"3\.1415", r"\birrational\b",
            r"\btranscendental\b", r"\bcircumference\b", r"\bangular\b",
            r"\bpolygon\b", r"\barchimedes\b", r"\binfinite\s+decimal\b",
            r"\bnon-repeating\b"
        ]
    },
    "EXP": {
        "name": "Exponential Growth Operator (e & Compounding)",
        "patterns": [
            r"\be\^x\b", r"\bexp\(", r"\\exp", r"\bexponential\b",
            r"\beuler\b", r"2\.718", r"\bcompound\b", r"\bgrowth\s+rate\b",
            r"\b\+\s*1/n\)\^n\b", r"\bln\b", r"\\ln\b", r"\blogarithm\b"
        ]
    },
    "CIR": {
        "name": "Circle Loop Formula & Rotational Periodicity",
        "patterns": [
            r"\bcircle\b", r"\bloop\b", r"\brotation\b", r"\bcycle\b",
            r"\bperiodic\b", r"\bradius\b", r"e\^\{i", r"\boscillat",
            r"\bclosed\s+path\b", r"\btorus\b", r"\bwinding\b", r"\b2\\pi\b"
        ]
    },
    "LIM": {
        "name": "Limits, Differential Calculus & Convergence",
        "patterns": [
            r"\\lim\b", r"\blimit[s]?\b", r"\bcalculus\b", r"\bderivative\b",
            r"\bintegral\b", r"\\int\b", r"\bd/dx\b", r"\\frac\{d",
            r"\btaylor\b", r"\bseries\b", r"\bcauchy\b", r"\bconverg"
        ]
    },
    "AXI": {
        "name": "Foundational Axioms, Peano, Cantor & Set Logic",
        "patterns": [
            r"\bpeano\b", r"\bcantor\b", r"\bset\s+theory\b", r"\bzfc\b",
            r"\bcardinal\b", r"\bordinal\b", r"\\aleph", r"\baleph\b",
            r"\bbijection\b", r"\bcountable\b", r"\buncountable\b",
            r"\bsuccessor\b", r"\brobinson\b", r"\bhyperreal\b", r"\bsurreal\b"
        ]
    },
    "DIV": {
        "name": "Division by Zero, Indeterminate Forms & Ratios",
        "patterns": [
            r"0/0", r"\\infty/\\infty", r"1/0", r"\bdivision\s+by\s+zero\b",
            r"\bindeterminate\s+form\b", r"\bl'hopital\b", r"\bquotient\b",
            r"\bratio\b", r"\breciprocal\b", r"\binverse\b", r"\bsingularity\b",
            r"\bpole\b"
        ]
    },
    "PHY": {
        "name": "Physical Observation, Quantum Shell & Measurement",
        "patterns": [
            r"\bquantum\b", r"\bplanck\b", r"\bphoton\b", r"\brelativity\b",
            r"\bspacetime\b", r"\bgravity\b", r"\bmass\b", r"\benergy\b",
            r"\bentropy\b", r"\bthermodynamic", r"\bobservable\b",
            r"\bmeasurement\b", r"\bshell\b", r"\bhorizon\b", r"\bcosmolog"
        ]
    },
    "ALG": {
        "name": "Algebraic Structure, Rings, Non-Archimedean Arithmetic",
        "patterns": [
            r"\bring\b", r"\bgroup\b", r"\balgebra\b", r"\bcommutative\b",
            r"\bassociative\b", r"\bdistributive\b", r"\bnon-archimedean\b",
            r"\bmodulo\b", r"\bpolynomial\b", r"\boperator\b", r"\bmatrix\b",
            r"\beigenvalue\b"
        ]
    }
}

CONCEPT_LEXICON = [
    ("1^inf=0^inf", r"1\^\{?\\infty\}?|0\^\{?\\infty\}?|1\^∞|0\^∞"),
    ("INDEF_X", r"\bindefinite\b|\bINDEF\b|\[x\]"),
    ("epsilon", r"\\varepsilon|\\epsilon|\binfinitesimal\b"),
    ("chi_vector", r"\\chi\b|\bchi\b|\bholographic\b"),
    ("pi_closure", r"\\pi\b|\bpi\b|\bcircumference\b"),
    ("euler_e", r"\be\^x\b|\\exp\b|\beuler\b|\bcompound"),
    ("circle_loop", r"\bcircle\b|\bloop\b|\brotation\b"),
    ("limit_calc", r"\\lim\b|\blimit\b|\bderivative\b|\bintegral\b"),
    ("cantor_set", r"\bcantor\b|\bcardinal\b|\bordinal\b|\\aleph"),
    ("peano_axiom", r"\bpeano\b|\baxiom\b|\bsuccessor\b"),
    ("div_zero", r"0/0|1/0|\bdivision\s+by\s+zero\b|\bindeterminate\b"),
    ("quantum_phy", r"\bquantum\b|\bplanck\b|\bspacetime\b|\bentropy\b"),
    ("scale_tier", r"\bn\+1\b|\bhierarchy\b|\bscale\b|\btier\b"),
    ("hyperreal", r"\bhyperreal\b|\brobinson\b|\bsurreal\b|\bnon-archimedean\b"),
    ("convergence", r"\bconverge[s]?\b|\bcauchy\b|\basymptot"),
    ("singularity", r"\bsingularity\b|\bdiverg\w+\b|\bbreakdown\b"),
]

# ============================================================================
# 2. SEGMENTATION & RIBOSOMAL TRANSCRIPTION HEAD
# ============================================================================

def segment_markdown(filepath: Path):
    """Segment markdown into blocks with exact 1-based line ranges and heading context."""
    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    blocks = []
    curr_lines = []
    curr_start = 1
    current_heading = "Root"
    in_code_or_math = False

    def flush(end_line):
        nonlocal curr_lines
        if not curr_lines:
            return
        raw = "\n".join(curr_lines).strip()
        if raw:
            blocks.append({
                "start_line": curr_start,
                "end_line": end_line,
                "heading": current_heading,
                "text": raw
            })
        curr_lines = []

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("$$"):
            in_code_or_math = not in_code_or_math

        if not in_code_or_math and re.match(r"^#{1,6}\s+", stripped):
            flush(idx - 1)
            current_heading = re.sub(r"^#{1,6}\s+", "", stripped).strip()[:90]
            curr_start = idx
            curr_lines = [line]
            flush(idx)
            curr_start = idx + 1
            continue

        if not in_code_or_math and stripped == "":
            flush(idx - 1)
            curr_start = idx + 1
        else:
            if not curr_lines:
                curr_start = idx
            curr_lines.append(line)

    flush(len(lines))
    return blocks, len(lines)


def transcribe_block(block, idx):
    """Ribosomal Reading Head: Transcribes a text block into a 3-base Semantic Codon + I/E sets."""
    text = block["text"]
    text_lower = text.lower()

    # 1. Score Engine Base (C, P, R, G)
    engine_scores = {b: 0 for b in "CPRG"}
    for base, patterns in ENGINE_PATTERNS.items():
        for pat in patterns:
            matches = re.findall(pat, text_lower)
            engine_scores[base] += len(matches)

    # Structural heuristics
    if re.match(r"^#{1,6}\s+", text.strip()):
        engine_scores["C"] += 2
    if "=" in text or "\\frac" in text or "\\sum" in text:
        engine_scores["P"] += 2
    if "?" in text:
        engine_scores["G"] += 1

    best_engine = max(["C", "P", "R", "G"], key=lambda b: (engine_scores[b], b == "C"))
    if sum(engine_scores.values()) == 0:
        best_engine = "C" if len(text) > 120 else "G"

    # 2. Score Modal & Polarity Base (W, A, M, L vs N, X, O, H)
    modal_scores = {b: 0 for b in "WAMLNXOH"}
    for base, patterns in MODAL_PATTERNS.items():
        for pat in patterns:
            matches = re.findall(pat, text_lower)
            modal_scores[base] += len(matches)

    if sum(modal_scores.values()) == 0:
        # Default modal assignment based on engine and definitive syntax
        if "is " in text_lower or "=" in text_lower:
            modal_scores["L"] += 1
        else:
            modal_scores["A"] += 1

    best_modal = max("WAMLNXOH", key=lambda b: modal_scores[b])
    polarity = "+I" if best_modal in INCLUSIVE_BASES else "-E"

    # 3. Score Topic Gene Code
    gene_scores = {g: 0 for g in TOPIC_GENES}
    for gene, info in TOPIC_GENES.items():
        for pat in info["patterns"]:
            matches = re.findall(pat, text_lower)
            gene_scores[gene] += len(matches)

    max_gene_score = max(gene_scores.values())
    if max_gene_score == 0:
        best_gene = "INT"  # Intron / non-coding conversational or formatting block
    else:
        best_gene = max(TOPIC_GENES.keys(), key=lambda g: gene_scores[g])

    # Secondary active genes (co-expressed operons)
    secondary_genes = [g for g, s in sorted(gene_scores.items(), key=lambda x: -x[1]) if s > 0 and g != best_gene][:2]

    # 4. Extract Included (I_i) and Discluded (E_i) concept sets at sentence level
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    included_set = set()
    discluded_set = set()
    negation_cue = re.compile(
        r"\b(not|never|cannot|can't|won't|impossible|invalid|false|fails?|reject\w*|neither|no\s+longer|rather\s+than|unlike|contradict\w*)\b|\\neq|!=",
        re.I
    )

    for sent in sentences:
        is_neg = bool(negation_cue.search(sent))
        for cname, cpat in CONCEPT_LEXICON:
            if re.search(cpat, sent, re.I):
                if is_neg:
                    discluded_set.add(cname)
                else:
                    included_set.add(cname)

    # Complexity score (coding density)
    word_count = len(re.findall(r"\w+", text))
    math_density = len(re.findall(r"[\$\\=\^\{\}\+\-\*/]|\\frac|\\infty|\\lim|\\pi|\\chi", text))
    complexity = round(
        (max_gene_score * 2.0) + sum(engine_scores.values()) * 0.5 + min(math_density, 25) * 0.4 + min(word_count, 150) * 0.03,
        2
    )

    codon_str = f"{best_engine}-{best_modal}:{best_gene}"

    return {
        "index": idx,
        "start_line": block["start_line"],
        "end_line": block["end_line"],
        "heading": block["heading"],
        "engine": best_engine,
        "modal": best_modal,
        "polarity": polarity,
        "gene": best_gene,
        "secondary_genes": secondary_genes,
        "codon": codon_str,
        "included_concepts": sorted(included_set),
        "discluded_concepts": sorted(discluded_set),
        "complexity": complexity,
        "word_count": word_count,
        "math_density": math_density,
        "snippet": re.sub(r"\s+", " ", text)[:180]
    }


def sequence_genome(filepath: Path, name: str):
    blocks, total_lines = segment_markdown(filepath)
    codons = [transcribe_block(b, i) for i, b in enumerate(blocks)]
    return {
        "name": name,
        "filepath": str(filepath),
        "total_lines": total_lines,
        "total_blocks": len(codons),
        "codons": codons
    }

# ============================================================================
# 3. SMITH-WATERMAN HOMOLOGY ALIGNER & SUBSTITUTION MATRIX
# ============================================================================

def score_codon_pair(c_chat, c_irm):
    """
    Custom Semantic Substitution Matrix between a chat codon and an irm codon.
    Returns (score, match_type, detail)
    """
    g1, g2 = c_chat["gene"], c_irm["gene"]
    e1, e2 = c_chat["engine"], c_irm["engine"]
    m1, m2 = c_chat["modal"], c_irm["modal"]
    p1, p2 = c_chat["polarity"], c_irm["polarity"]

    # Skip introns from positive homology scoring
    if g1 == "INT" or g2 == "INT":
        return -2.5, "INTRON_GAP", "Non-coding intron region"

    # Check primary or secondary gene homology
    same_primary_gene = (g1 == g2)
    shared_secondary = (g1 in c_irm["secondary_genes"]) or (g2 in c_chat["secondary_genes"])

    if not same_primary_gene and not shared_secondary:
        return -3.0, "MISMATCH", f"Divergent genes ({g1} vs {g2})"

    gene_bonus = 0.0 if same_primary_gene else -1.0

    # Concept set overlap & direct polarity clash check
    inc1, exc1 = set(c_chat["included_concepts"]), set(c_chat["discluded_concepts"])
    inc2, exc2 = set(c_irm["included_concepts"]), set(c_irm["discluded_concepts"])

    # Direct Polarity Clash on same concept (included in one, discluded in the other)
    clash_concepts = (inc1 & exc2) | (exc1 & inc2)
    shared_concepts = (inc1 & inc2) | (exc1 & exc2)
    concept_bonus = min(len(shared_concepts) * 0.6, 1.8)

    # 1. Exact Codon Match (Gene + Engine + Modal) = +5
    if same_primary_gene and e1 == e2 and m1 == m2:
        return 5.0 + concept_bonus, "EXACT_CODON_MATCH", f"Conserved {c_chat['codon']}"

    # 2. Maturation Shift Match = +4
    # Exploratory in chat (C/M, P/M, C/A, P/A, G/M, G/A) -> Matured law/definition in IRM (C/L, C/W, P/W, P/L)
    # Or Reductive test in chat (R/N, R/X, R/O, C/N) -> Formalized Exclusion/Boundary rule in IRM (R/N, R/X, C/N, P/N)
    exploratory_chat = (e1 in {"C", "P", "G"} and m1 in {"M", "A", "L"})
    matured_irm = (e2 in {"C", "P"} and m2 in {"L", "W", "A"})
    reductive_to_rule = (e1 == "R" or p1 == "-E") and (e2 in {"R", "C", "P"} and p2 == "-E")

    if same_primary_gene and ((exploratory_chat and matured_irm) or reductive_to_rule):
        return 4.0 + concept_bonus, "MATURATION_SHIFT", f"{c_chat['codon']} -> {c_irm['codon']}"

    # 3. Direct Polarity Clash (Point Mutation / Conflict)
    # Same primary gene, opposite modal polarity (+I vs -E), especially with concept inversion
    if same_primary_gene and p1 != p2:
        if clash_concepts or (e1 == e2):
            # In Smith-Waterman we still allow alignment across point mutations inside an operon (+1.5)
            # while flagging the exact mutation!
            return 1.5 + gene_bonus, "POINT_MUTATION_CLASH", f"Polarity inversion {c_chat['codon']} ({p1}) vs {c_irm['codon']} ({p2}); clashed={sorted(clash_concepts)}"
        elif e1 == "R" and p2 == "+I":
            return 2.5 + concept_bonus, "MATURATION_SHIFT", f"Critique resolved into positive law: {c_chat['codon']} -> {c_irm['codon']}"

    # 4. Homologous Gene Match (Same gene, compatible engine/modal shift)
    if same_primary_gene:
        return 3.0 + concept_bonus, "HOMOLOGOUS_GENE", f"Gene {g1} conserved ({e1}-{m1} -> {e2}-{m2})"

    # 5. Paralogous Match (Shared secondary gene)
    return 1.8 + concept_bonus, "PARALOG_MATCH", f"Paralog gene overlap ({g1}/{g2})"


def smith_waterman_operons(chat_codons, irm_codons, top_k=18, min_score=14.0):
    """
    Iterative Local Smith-Waterman alignment to extract the top non-overlapping Conserved Operons
    between chat_codons and irm_codons.
    """
    n = len(chat_codons)
    m = len(irm_codons)
    gap_penalty = -2.2

    # Precompute pairwise substitution matrix
    sub_scores = [[0.0] * m for _ in range(n)]
    sub_types = [[""] * m for _ in range(n)]
    sub_details = [[""] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            sc, st, sd = score_codon_pair(chat_codons[i], irm_codons[j])
            sub_scores[i][j] = sc
            sub_types[i][j] = st
            sub_details[i][j] = sd

    used_chat = [False] * n
    used_irm = [False] * m
    operons = []

    for operon_idx in range(1, top_k + 1):
        # Build DP table masking already-extracted operons
        H = [[0.0] * (m + 1) for _ in range(n + 1)]
        tb = [[0] * (m + 1) for _ in range(n + 1)]  # 1: diag, 2: up (chat gap), 3: left (irm gap)

        best_score = 0.0
        best_pos = (0, 0)

        for i in range(1, n + 1):
            if used_chat[i - 1]:
                continue
            for j in range(1, m + 1):
                if used_irm[j - 1]:
                    continue
                diag = H[i - 1][j - 1] + sub_scores[i - 1][j - 1]
                up = H[i - 1][j] + gap_penalty
                left = H[i][j - 1] + gap_penalty

                val = max(0.0, diag, up, left)
                H[i][j] = val
                if val > 0.0:
                    if val == diag:
                        tb[i][j] = 1
                    elif val == up:
                        tb[i][j] = 2
                    else:
                        tb[i][j] = 3

                if val > best_score:
                    best_score = val
                    best_pos = (i, j)

        if best_score < min_score:
            break

        # Traceback
        i, j = best_pos
        aligned_pairs = []
        while i > 0 and j > 0 and H[i][j] > 0:
            if used_chat[i - 1] or used_irm[j - 1]:
                break
            move = tb[i][j]
            if move == 1:
                aligned_pairs.append((i - 1, j - 1, sub_scores[i - 1][j - 1], sub_types[i - 1][j - 1], sub_details[i - 1][j - 1]))
                i -= 1
                j -= 1
            elif move == 2:
                aligned_pairs.append((i - 1, None, gap_penalty, "CHAT_INSERTION", "Unaligned chat step inside operon"))
                i -= 1
            elif move == 3:
                aligned_pairs.append((None, j - 1, gap_penalty, "IRM_INSERTION", "Synthesized IRM expansion inside operon"))
                j -= 1
            else:
                break

        aligned_pairs.reverse()
        chat_indices = [p[0] for p in aligned_pairs if p[0] is not None]
        irm_indices = [p[1] for p in aligned_pairs if p[1] is not None]

        if not chat_indices or not irm_indices:
            break

        for ci in chat_indices:
            used_chat[ci] = True
        for ij in irm_indices:
            used_irm[ij] = True

        c_start_idx, c_end_idx = min(chat_indices), max(chat_indices)
        i_start_idx, i_end_idx = min(irm_indices), max(irm_indices)

        # Summarize operon composition
        type_counts = Counter(p[3] for p in aligned_pairs)
        genes_involved = Counter(chat_codons[ci]["gene"] for ci in chat_indices if chat_codons[ci]["gene"] != "INT")
        dominant_gene = genes_involved.most_common(1)[0][0] if genes_involved else "MIX"

        mutations = []
        maturations = []
        for ci, ij, sc, mtype, detail in aligned_pairs:
            if ci is not None and ij is not None:
                if mtype == "POINT_MUTATION_CLASH":
                    mutations.append({
                        "chat_lines": f"L{chat_codons[ci]['start_line']}-L{chat_codons[ci]['end_line']}",
                        "irm_lines": f"L{irm_codons[ij]['start_line']}-L{irm_codons[ij]['end_line']}",
                        "chat_codon": chat_codons[ci]["codon"],
                        "irm_codon": irm_codons[ij]["codon"],
                        "detail": detail,
                        "chat_snippet": chat_codons[ci]["snippet"][:110],
                        "irm_snippet": irm_codons[ij]["snippet"][:110]
                    })
                elif mtype == "MATURATION_SHIFT":
                    maturations.append({
                        "chat_lines": f"L{chat_codons[ci]['start_line']}-L{chat_codons[ci]['end_line']}",
                        "irm_lines": f"L{irm_codons[ij]['start_line']}-L{irm_codons[ij]['end_line']}",
                        "shift": f"{chat_codons[ci]['codon']} -> {irm_codons[ij]['codon']}",
                        "chat_snippet": chat_codons[ci]["snippet"][:100],
                        "irm_snippet": irm_codons[ij]["snippet"][:100]
                    })

        operons.append({
            "operon_id": f"OP-{operon_idx:02d}",
            "alignment_score": round(best_score, 2),
            "dominant_gene": dominant_gene,
            "dominant_gene_name": TOPIC_GENES.get(dominant_gene, {}).get("name", "Mixed Operon"),
            "chat_block_range": [c_start_idx, c_end_idx],
            "chat_line_range": [chat_codons[c_start_idx]["start_line"], chat_codons[c_end_idx]["end_line"]],
            "chat_heading": chat_codons[c_start_idx]["heading"],
            "irm_block_range": [i_start_idx, i_end_idx],
            "irm_line_range": [irm_codons[i_start_idx]["start_line"], irm_codons[i_end_idx]["end_line"]],
            "irm_heading": irm_codons[i_start_idx]["heading"],
            "length_codons": len(aligned_pairs),
            "match_breakdown": dict(type_counts),
            "chat_codon_seq": " ".join(chat_codons[ci]["codon"] for ci in chat_indices[:10]) + (" ..." if len(chat_indices) > 10 else ""),
            "irm_codon_seq": " ".join(irm_codons[ij]["codon"] for ij in irm_indices[:10]) + (" ..." if len(irm_indices) > 10 else ""),
            "maturation_shifts": maturations[:5],
            "point_mutations": mutations[:5]
        })

    # Also scan globally for top high-significance Point Mutations / Direct Polarity Clashes across the whole matrix
    global_clashes = []
    for i, c_chat in enumerate(chat_codons):
        if c_chat["gene"] == "INT":
            continue
        for j, c_irm in enumerate(irm_codons):
            if c_chat["gene"] == c_irm["gene"] and c_chat["polarity"] != c_irm["polarity"]:
                inc1, exc1 = set(c_chat["included_concepts"]), set(c_chat["discluded_concepts"])
                inc2, exc2 = set(c_irm["included_concepts"]), set(c_irm["discluded_concepts"])
                clashed = (inc1 & exc2) | (exc1 & inc2)
                if clashed:
                    global_clashes.append({
                        "gene": c_chat["gene"],
                        "clashed_concepts": sorted(clashed),
                        "chat_lines": [c_chat["start_line"], c_chat["end_line"]],
                        "chat_codon": c_chat["codon"],
                        "chat_heading": c_chat["heading"],
                        "chat_snippet": c_chat["snippet"],
                        "irm_lines": [c_irm["start_line"], c_irm["end_line"]],
                        "irm_codon": c_irm["codon"],
                        "irm_heading": c_irm["heading"],
                        "irm_snippet": c_irm["snippet"]
                    })

    # Deduplicate global clashes by chat block
    seen_chat_clash = set()
    unique_clashes = []
    for cl in global_clashes:
        key = (cl["chat_lines"][0], cl["irm_lines"][0])
        if cl["chat_lines"][0] not in seen_chat_clash and len(unique_clashes) < 15:
            seen_chat_clash.add(cl["chat_lines"][0])
            unique_clashes.append(cl)

    return operons, used_chat, used_irm, unique_clashes


# ============================================================================
# 4. UNMERGED GENE ISLANDS (DELETED / MISSING DATA DISCOVERY)
# ============================================================================

def discover_unmerged_gene_islands(chat_codons, irm_codons, used_chat):
    """
    Find contiguous runs of high-complexity Constructive/Productive coding codons in chat
    that were NOT aligned to any conserved operon in IRM and have low homology to IRM.
    """
    # Compute max possible single-codon similarity to any IRM codon to confirm true deletion/loss
    max_irm_sim = []
    for i, c_chat in enumerate(chat_codons):
        if used_chat[i] or c_chat["gene"] == "INT":
            max_irm_sim.append(99.0 if used_chat[i] else 0.0)
            continue
        best_s = max(score_codon_pair(c_chat, c_irm)[0] for c_irm in irm_codons)
        max_irm_sim.append(best_s)

    islands = []
    curr_run = []

    def flush_run():
        nonlocal curr_run
        if not curr_run:
            return
        coding = [c for c in curr_run if c["gene"] != "INT" and c["engine"] in {"C", "P"}]
        total_comp = sum(c["complexity"] for c in curr_run)
        if len(coding) >= 3 and total_comp >= 18.0:
            genes = Counter(c["gene"] for c in coding)
            dom_gene = genes.most_common(1)[0][0]
            concepts = sorted(set(x for c in curr_run for x in c["included_concepts"]))
            snippets = [c["snippet"] for c in coding if len(c["snippet"]) > 45]
            islands.append({
                "chat_block_range": [curr_run[0]["index"], curr_run[-1]["index"]],
                "chat_line_range": [curr_run[0]["start_line"], curr_run[-1]["end_line"]],
                "line_span": curr_run[-1]["end_line"] - curr_run[0]["start_line"] + 1,
                "heading": curr_run[0]["heading"],
                "num_codons": len(curr_run),
                "coding_codons": len(coding),
                "total_complexity": round(total_comp, 2),
                "avg_complexity": round(total_comp / len(curr_run), 2),
                "dominant_gene": dom_gene,
                "dominant_gene_name": TOPIC_GENES.get(dom_gene, {}).get("name", dom_gene),
                "gene_distribution": dict(genes),
                "codon_sequence": " ".join(c["codon"] for c in curr_run[:12]) + (" ..." if len(curr_run) > 12 else ""),
                "concepts_present": concepts,
                "representative_snippet": snippets[0] if snippets else curr_run[0]["snippet"]
            })
        curr_run = []

    for i, c in enumerate(chat_codons):
        if not used_chat[i] and (
            (c["gene"] != "INT" and c["engine"] in {"C", "P", "R"} and c["complexity"] >= 3.0)
            or (curr_run and len(curr_run) >= 1 and c["complexity"] >= 2.2)
        ):
            curr_run.append(c)
        else:
            flush_run()
    flush_run()

    islands.sort(key=lambda x: -x["total_complexity"])
    for idx, isl in enumerate(islands, start=1):
        isl["island_id"] = f"UGI-{idx:02d}"
    return islands[:15]


# ============================================================================
# 5. GENOME MATURITY & BIOINFORMATICS HEALTH METRICS
# ============================================================================

def compute_genome_metrics(genome):
    codons = genome["codons"]
    total = max(len(codons), 1)
    coding = [c for c in codons if c["gene"] != "INT"]
    introns = [c for c in codons if c["gene"] == "INT"]

    engine_counts = Counter(c["engine"] for c in codons)
    modal_counts = Counter(c["modal"] for c in codons)
    polarity_counts = Counter(c["polarity"] for c in codons)
    gene_counts = Counter(c["gene"] for c in coding)
    triplet_counts = Counter(c["codon"] for c in coding)

    inc = polarity_counts["+I"]
    exc = polarity_counts["-E"]
    ie_ratio = round(inc / max(exc, 1), 3)
    gc_equiv_content = round((engine_counts["C"] + engine_counts["P"]) / total * 100.0, 2)

    # Maturation Index: ratio of crystallized (C/P + W/L) codons to exploratory/regressive (M/G) codons
    crystallized = sum(1 for c in coding if c["engine"] in {"C", "P"} and c["modal"] in {"W", "L", "A"})
    exploratory = sum(1 for c in codons if c["modal"] == "M" or c["engine"] == "G")
    maturation_index = round(crystallized / max(exploratory, 1), 3)

    # Operon Coherence: probability that adjacent coding blocks share the same primary or secondary Topic Gene
    same_gene_adj = 0
    for k in range(len(coding) - 1):
        g_curr = coding[k]["gene"]
        g_next = coding[k + 1]["gene"]
        if g_curr == g_next or g_curr in coding[k + 1]["secondary_genes"] or g_next in coding[k]["secondary_genes"]:
            same_gene_adj += 1
    operon_coherence = round(same_gene_adj / max(len(coding) - 1, 1) * 100.0, 2)

    # Shannon Codon Diversity Entropy (in bits)
    entropy = 0.0
    if coding:
        for cnt in triplet_counts.values():
            p = cnt / len(coding)
            entropy -= p * math.log2(p)

    intron_ratio = round(len(introns) / total * 100.0, 2)
    coding_density = round(100.0 - intron_ratio, 2)

    return {
        "name": genome["name"],
        "total_lines": genome["total_lines"],
        "total_codons": total,
        "coding_codons": len(coding),
        "intron_codons": len(introns),
        "coding_density_pct": coding_density,
        "intron_noise_pct": intron_ratio,
        "gc_equivalent_cp_pct": gc_equiv_content,
        "inclusive_exclusive_ratio": ie_ratio,
        "inclusive_pct": round(inc / total * 100.0, 2),
        "exclusive_pct": round(exc / total * 100.0, 2),
        "maturation_index": maturation_index,
        "operon_coherence_pct": operon_coherence,
        "shannon_codon_entropy_bits": round(entropy, 3),
        "avg_block_complexity": round(sum(c["complexity"] for c in codons) / total, 2),
        "engine_distribution": {k: round(engine_counts[k] / total * 100.0, 1) for k in "CPRG"},
        "modal_distribution": {k: round(modal_counts[k] / total * 100.0, 1) for k in "WAMLNXOH"},
        "top_genes": dict(gene_counts.most_common(8)),
        "top_triplet_codons": dict(triplet_counts.most_common(10))
    }


# ============================================================================
# 6. MAIN EXECUTION & REPORT GENERATION
# ============================================================================

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Sequence Genomes
    chat_genome = sequence_genome(CHAT_PATH, "chat_infinity_maths")
    irm_genome = sequence_genome(IRM_PATH, "irm_comprehensive_report")

    arxiv_genomes = []
    if ARXIV_DIR.exists():
        for md_file in sorted(ARXIV_DIR.glob("*.md")):
            arxiv_genomes.append(sequence_genome(md_file, md_file.stem))

    # 2. Compute Genome Maturity Metrics
    all_metrics = {
        "chat": compute_genome_metrics(chat_genome),
        "irm": compute_genome_metrics(irm_genome),
        "arxiv_controls": {g["name"]: compute_genome_metrics(g) for g in arxiv_genomes}
    }

    # 3. Smith-Waterman Operon Homology Alignment (chat vs irm)
    operons, used_chat, used_irm, point_mutations = smith_waterman_operons(
        chat_genome["codons"], irm_genome["codons"], top_k=16, min_score=14.0
    )

    # 4. Discover Unmerged Gene Islands in chat
    unmerged_islands = discover_unmerged_gene_islands(
        chat_genome["codons"], irm_genome["codons"], used_chat
    )

    # Coverage summary
    chat_coding_total = sum(1 for c in chat_genome["codons"] if c["gene"] != "INT")
    chat_aligned_coding = sum(1 for i, c in enumerate(chat_genome["codons"]) if used_chat[i] and c["gene"] != "INT")
    irm_coding_total = sum(1 for c in irm_genome["codons"] if c["gene"] != "INT")
    irm_aligned_coding = sum(1 for j, c in enumerate(irm_genome["codons"]) if used_irm[j] and c["gene"] != "INT")

    alignment_summary = {
        "conserved_operons_count": len(operons),
        "chat_coding_coverage_pct": round(chat_aligned_coding / max(chat_coding_total, 1) * 100.0, 2),
        "irm_coding_coverage_pct": round(irm_aligned_coding / max(irm_coding_total, 1) * 100.0, 2),
        "unmerged_gene_islands_count": len(unmerged_islands),
        "point_mutations_count": len(point_mutations)
    }

    # 5. Save results.json
    results_payload = {
        "agent": "Agent 3: Bioinformatics Codon & Smith-Waterman DNA Homology Aligner",
        "genetic_code_spec": {
            "base1_engines": {"C": "Constructive", "P": "Productive", "R": "Reductive", "G": "Regressive"},
            "base2_modals_inclusive": {"W": "will be", "A": "can be", "M": "may be", "L": "is like"},
            "base2_modals_exclusive": {"N": "is not", "X": "can't be", "O": "won't be", "H": "was like"},
            "base3_genes": {k: v["name"] for k, v in TOPIC_GENES.items()}
        },
        "alignment_summary": alignment_summary,
        "genome_maturity_metrics": all_metrics,
        "conserved_operons": operons,
        "unmerged_gene_islands": unmerged_islands,
        "point_mutation_clashes": point_mutations
    }

    results_path = OUT_DIR / "results.json"
    results_path.write_text(json.dumps(results_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # 6. Build Comprehensive Markdown Report
    cm = all_metrics["chat"]
    im = all_metrics["irm"]

    md = []
    md.append("# Agent 3: Ribosomal Codon Transcription & Smith–Waterman DNA Homology Report")
    md.append("")
    md.append("## 1. Architectural Synthesis: The Ribosomal Semantic Reading Head")
    md.append("Each paragraph/block $i$ across the target documents is scanned by a sliding **Ribosomal Reading Head** that transcribes natural language and mathematical equations into a **Triplet Semantic Codon** (`[Engine]-[Modal]:[Gene]`) alongside sentence-level **Included ($\\mathcal{I}_i$)** and **Discluded ($\\mathcal{E}_i$)** concept sets:")
    md.append("- **Base 1 (Engine Nucleotide)**: `C` (Constructive definition/axiom), `P` (Productive derivation/operator), `R` (Reductive critique/constraint), `G` (Regressive recursion/meta-reflection).")
    md.append("- **Base 2 (Modal & Polarity Base)**:")
    md.append("  - **Inclusive (`+I`)**: `W` (*will be* — invariant law), `A` (*can be* — operational capacity), `M` (*may be* — exploratory hypothesis), `L` (*is like* — structural isomorphism).")
    md.append("  - **Exclusive (`-E`)**: `N` (*is not* — taxonomic negation), `X` (*can't be* — impossibility/undefined), `O` (*won't be* — divergence/refusal), `H` (*was like* — superseded orthodox model).")
    md.append("- **Base 3 (Topic Gene Code)**: 11 coding mathematical genes (`SEQ`, `IND`, `CHI`, `PI`, `EXP`, `CIR`, `LIM`, `AXI`, `DIV`, `PHY`, `ALG`) + `INT` (non-coding conversational intron).")
    md.append("")

    md.append("## 2. Comparative Genome Health & Maturity Metrics (`chat` vs `irm` vs `arXiv` Controls)")
    md.append("| Metric | `chat` (Raw Transcript) | `irm` (Compiled Report) | " + " | ".join(f"`{k}`" for k in all_metrics["arxiv_controls"]) + " |")
    md.append("|---|---:|---:|" + "---:|" * len(all_metrics["arxiv_controls"]))

    arxiv_list = list(all_metrics["arxiv_controls"].values())
    rows = [
        ("Total Lines", "total_lines", ""),
        ("Total Transcribed Codons", "total_codons", ""),
        ("Coding Exon Codons", "coding_codons", ""),
        ("Coding Density (%)", "coding_density_pct", "%"),
        ("Intron / Noise Ratio (%)", "intron_noise_pct", "%"),
        ("GC-Equiv (`C+P` Engine %)", "gc_equivalent_cp_pct", "%"),
        ("Inclusive / Exclusive (`+I/-E`)", "inclusive_exclusive_ratio", ""),
        ("Maturation Index (Crystallized/Exploratory)", "maturation_index", ""),
        ("Operon Coherence (%)", "operon_coherence_pct", "%"),
        ("Shannon Codon Entropy (bits)", "shannon_codon_entropy_bits", " bits"),
        ("Mean Block Complexity", "avg_block_complexity", ""),
    ]
    for label, key, suffix in rows:
        arx_vals = " | ".join(f"{a[key]}{suffix}" for a in arxiv_list)
        md.append(f"| **{label}** | {cm[key]}{suffix} | {im[key]}{suffix} | {arx_vals} |")

    md.append("")
    md.append("### Engine & Modal Codon Bias Shift (`chat` $\\rightarrow$ `irm`)")
    md.append(f"- **Engine Distribution (`C / P / R / G`)**: `chat` = `{cm['engine_distribution']}` $\\rightarrow$ `irm` = `{im['engine_distribution']}`")
    md.append(f"- **Modal Distribution (`W / A / M / L / N / X / O / H`)**: `chat` = `{cm['modal_distribution']}` $\\rightarrow$ `irm` = `{im['modal_distribution']}`")
    md.append(f"- **Top Expressed Triplet Codons in `chat`**: `{cm['top_triplet_codons']}`")
    md.append(f"- **Top Expressed Triplet Codons in `irm`**: `{im['top_triplet_codons']}`")
    md.append("")

    md.append("## 3. Smith–Waterman Local Alignment: Conserved Operons (`chat` $\\leftrightarrow$ `irm`)")
    md.append(f"Using our custom Semantic Substitution Matrix (`+5.0` Exact Codon Match, `+4.0` Maturation Shift, `+3.0` Homologous Gene, `+1.5` Point Mutation Clash, `-2.2` Gap Penalty), iterative local Smith–Waterman alignment extracted **{len(operons)} high-scoring Conserved Operons**, accounting for **{alignment_summary['irm_coding_coverage_pct']}%** of `irm`'s coding exons and **{alignment_summary['chat_coding_coverage_pct']}%** of `chat`'s coding exons.")
    md.append("")
    md.append("| Operon ID | SW Score | Dominant Gene | `chat` Line Range | `irm` Line Range | `chat` Context / Heading | `irm` Section Heading | Breakdown (Exact / Maturation / Homolog / Clash) |")
    md.append("|---|---:|---|---|---|---|---|---|")
    for op in operons:
        mb = op["match_breakdown"]
        b_str = f"E:{mb.get('EXACT_CODON_MATCH',0)}, M:{mb.get('MATURATION_SHIFT',0)}, H:{mb.get('HOMOLOGOUS_GENE',0)}, C:{mb.get('POINT_MUTATION_CLASH',0)}"
        c_lr = f"L{op['chat_line_range'][0]}–L{op['chat_line_range'][1]}"
        i_lr = f"L{op['irm_line_range'][0]}–L{op['irm_line_range'][1]}"
        md.append(f"| **{op['operon_id']}** | `{op['alignment_score']}` | `{op['dominant_gene']}` ({op['dominant_gene_name'][:28]}) | `{c_lr}` | `{i_lr}` | {op['chat_heading'][:38]} | {op['irm_heading'][:38]} | {b_str} |")
    md.append("")

    md.append("### Detailed Operon Sequence Alignments & Maturation Shifts")
    for op in operons[:10]:
        md.append(f"#### {op['operon_id']}: `{op['dominant_gene']}` — Score `{op['alignment_score']}` (`chat` L{op['chat_line_range'][0]}–L{op['chat_line_range'][1]} $\\leftrightarrow$ `irm` L{op['irm_line_range'][0]}–L{op['irm_line_range'][1]})")
        md.append(f"- **`chat` Codon Strand**: `{op['chat_codon_seq']}`")
        md.append(f"- **`irm` Codon Strand**: `{op['irm_codon_seq']}`")
        if op["maturation_shifts"]:
            md.append("- **Key Maturation Shifts (`chat` exploratory $\\rightarrow$ `irm` formalized)**:")
            for ms in op["maturation_shifts"][:3]:
                md.append(f"  - `{ms['chat_lines']}` $\\rightarrow$ `{ms['irm_lines']}` (`{ms['shift']}`): *\"{ms['chat_snippet']}...\"* $\\rightarrow$ *\"{ms['irm_snippet']}...\"*")
        md.append("")

    md.append("## 4. Point Mutations & Direct Polarity Clashes (`+I` vs `-E` Conflicts)")
    md.append("The following loci exhibit **Direct Polarity Clashes** on the same Topic Gene and shared concept lexicon (where one genome asserts an Inclusive `+I` state while the other asserts an Exclusive `-E` state):")
    md.append("")
    if point_mutations:
        for idx, pm in enumerate(point_mutations[:10], start=1):
            md.append(f"{idx}. **Gene `{pm['gene']}` Clash on `{pm['clashed_concepts']}`**: `chat` L{pm['chat_lines'][0]}–L{pm['chat_lines'][1]} (`{pm['chat_codon']}`) vs `irm` L{pm['irm_lines'][0]}–L{pm['irm_lines'][1]} (`{pm['irm_codon']}`)")
            md.append(f"   - **`chat` ({pm['chat_heading'][:40]})**: *\"{pm['chat_snippet']}\"*")
            md.append(f"   - **`irm` ({pm['irm_heading'][:40]})**: *\"{pm['irm_snippet']}\"*")
    else:
        md.append("- No direct concept polarity inversions detected.")
    md.append("")

    md.append("## 5. Deleted Gene Discovery: Unmerged Gene Islands in `chat` (Missing from `irm`)")
    md.append("By scanning `chat` for contiguous stretches of high-complexity Constructive/Productive (`C`/`P`) coding codons that remained completely unaligned after Smith–Waterman operon extraction, we identified **Unmerged Gene Islands** — substantive mathematical derivations, physical shell models, and geometric explorations from the raw dialogue that were dropped or severely compressed during the synthesis of `irm`:")
    md.append("")
    md.append("| Island ID | `chat` Line Range | Codons (Coding) | Total Complexity | Dominant Gene | Heading / Topic Context | Key Included Concepts |")
    md.append("|---|---|---:|---:|---|---|---|")
    for isl in unmerged_islands:
        lr = f"L{isl['chat_line_range'][0]}–L{isl['chat_line_range'][1]}"
        md.append(f"| **{isl['island_id']}** | `{lr}` | {isl['num_codons']} ({isl['coding_codons']}) | `{isl['total_complexity']}` | `{isl['dominant_gene']}` | {isl['heading'][:42]} | `{', '.join(isl['concepts_present'][:5])}` |")
    md.append("")

    md.append("### Top Unmerged Gene Islands — Excerpt & Codon Forensics")
    for isl in unmerged_islands[:8]:
        lr = f"L{isl['chat_line_range'][0]}–L{isl['chat_line_range'][1]}"
        md.append(f"#### {isl['island_id']} (`chat` {lr}) — Gene `{isl['dominant_gene']}` ({isl['dominant_gene_name']})")
        md.append(f"- **Heading**: `{isl['heading']}` | **Complexity**: `{isl['total_complexity']}` | **Gene Mix**: `{isl['gene_distribution']}`")
        md.append(f"- **Codon Sequence**: `{isl['codon_sequence']}`")
        md.append(f"- **Representative Excerpt**: *\"{isl['representative_snippet']}\"*")
        md.append("")

    report_path = OUT_DIR / "report.md"
    report_path.write_text("\n".join(md), encoding="utf-8")

    print("=== AGENT 3 BIO-DNA ALIGNER SUMMARY ===")
    print(f"Chat lines/codons: {cm['total_lines']} lines / {cm['total_codons']} codons ({cm['coding_codons']} coding, {cm['intron_noise_pct']}% intron)")
    print(f"IRM lines/codons:  {im['total_lines']} lines / {im['total_codons']} codons ({im['coding_codons']} coding, {im['intron_noise_pct']}% intron)")
    print(f"Maturation Index:  chat={cm['maturation_index']} -> irm={im['maturation_index']}")
    print(f"GC-Equiv (C+P %):  chat={cm['gc_equivalent_cp_pct']}% -> irm={im['gc_equivalent_cp_pct']}%")
    print(f"Conserved Operons: {len(operons)} (IRM coding coverage: {alignment_summary['irm_coding_coverage_pct']}%, Chat coding coverage: {alignment_summary['chat_coding_coverage_pct']}%)")
    print(f"Unmerged Islands:  {len(unmerged_islands)} high-complexity dropped islands identified in chat")
    print(f"Point Mutations:   {len(point_mutations)} polarity clashes detected")
    print(f"Saved: {results_path} and {report_path}")

if __name__ == "__main__":
    main()
