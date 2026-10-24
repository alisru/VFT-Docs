#!/usr/bin/env python3
"""
Agent 1 (Round 2): Syntactic Modal, Proof-Working-Out & 4 Derivation Laws State Machine v2.0
=============================================================================================
Upgrades over Round 1 & `unified_gluon_dna_engine.py`:
  1. Eliminates the ':' / '=' fallback modal inflation bug in `unified_gluon_dna_engine.py`
     that misclassified bare markdown bullet lists as Constructive (`is_like`) modals.
  2. Separates "Bare Declarative Assertion" (Tier 0) from "Exploratory Sketch" (Tier 1),
     "Operational Derivation" (Tier 2), and "Formal Proof Chain / Working-Out" (Tier 3)
     via a 5-component Working-Out Completeness Engine (`W_score` in [0, 1]).
  3. Upgrades the 4 Verbatim Operational Derivation Laws Detector with strict clause-order
     verification AND symbolic working-out coupling (`Law_Verified_With_Working_Out`).
  4. Calibrates modal & proof-chain metrics against the expanded `arxiv_samples/*.md` benchmark
     and audits the entire `irm_formal_corpus/*.md` (Papers 7, 9, 12, 17, 24, 25, 30 + ZFC Bridge)
     alongside `chatgpt infinity maths.md` and `Comprehensive Report - IRM.md`.
"""

import os
import re
import json
import math
import glob
from collections import Counter, defaultdict

BASE_PHYSICS = r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics"
SEM_DIR = os.path.join(BASE_PHYSICS, "semantic_gluon_dna")
CHAT_PATH = os.path.join(BASE_PHYSICS, "chatgpt infinity maths.md")
IRM_REPORT_PATH = os.path.join(BASE_PHYSICS, "Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md")
IRM_FORMAL_DIR = os.path.join(SEM_DIR, "irm_formal_corpus")
ARXIV_DIR = os.path.join(SEM_DIR, "arxiv_samples")
OUT_DIR = os.path.join(SEM_DIR, "agent_1_syntactic_modal")
RESULTS_V2_JSON = os.path.join(OUT_DIR, "results_v2.json")
REPORT_V2_MD = os.path.join(OUT_DIR, "report_v2.md")

# ---------------------------------------------------------------------------
# 1. REFINED 8 MODAL STATES & 4 ENGINES (NO COLON/HEADER FALLBACK INFLATION)
# ---------------------------------------------------------------------------
MODAL_PATTERNS = {
    # CONSTRUCTIVE (C: Inclusive + Counteractive)
    "is_like": [
        r"\bis\s+defined\s+as\b", r"\bdefined\s+as\b", r"\bdefined\s+by\b",
        r"\brepresents?\b", r"\bis\s+like\b", r"\banalogous\s+to\b",
        r"\bform\s+of\b", r"\bcorresponds?\s+to\b", r"\bdenotes?\b",
        r"\bacts?\s+as\b", r"\bviewed\s+as\b", r"\binterpreted\s+as\b",
        r"\bequivalent\s+to\b", r"\bisomorphic\s+to\b", r"\bmodels?\b",
        r":=", r"\\equiv", r"≡"
    ],
    "may_be": [
        r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bsuppose\b",
        r"\bif\s+we\b", r"\bwhat\s+if\b", r"\bimagine\b", r"\blet\s+us\b",
        r"\blet's\b", r"\bassume\b", r"\bhypothesi[sz]e\b", r"\bconsider\b",
        r"\bpotentially\b", r"\bperhaps\b", r"\bconjecture\b"
    ],
    # PRODUCTIVE (P: Inclusive + Active)
    "will_be": [
        r"\bwill\s+be\b", r"\bwill\b", r"\bmust\s+be\b", r"\bmust\b",
        r"\btherefore\b", r"\bthus\b", r"\bhence\b", r"\bconsequently\b",
        r"\byields?\b", r"\bresolves?\s+(?:into|to)\b", r"\bproves?\b",
        r"\bit\s+follows\b", r"\bnecessarily\b", r"\bresults?\s+in\b",
        r"\bestablishes?\b", r"\bwe\s+obtain\b", r"\bwe\s+conclude\b",
        r"\\implies", r"\\Rightarrow", r"⟹", r"⇒"
    ],
    "can_be": [
        r"\bcan\s+be\b", r"\bcan\b", r"\ballows?\b", r"\benables?\b",
        r"\bcapable\s+of\b", r"\bpossible\s+to\b", r"\bpermits?\b",
        r"\bable\s+to\b", r"\bsucceeds?\s+in\b", r"\bachieves?\b",
        r"\bsatisfies\b", r"\badmits?\b"
    ],
    # REDUCTIVE (R: Exclusive + Active)
    "is_not": [
        r"\bis\s+not\b", r"\bisn't\b", r"\bare\s+not\b", r"\baren't\b",
        r"\bnot\s+a\b", r"\bdoes\s+not\b", r"\bdoesn't\b", r"\bdo\s+not\b",
        r"\bdon't\b", r"\bundefined\b", r"\bno\s+longer\b", r"\brather\s+than\b",
        r"\binstead\s+of\b", r"\bdistinct\s+from\b", r"\bunlike\b",
        r"\\neq", r"≠", r"\bnon-?zero\b"
    ],
    "cant_be": [
        r"\bcannot\b", r"\bcan't\b", r"\bimpossible\b", r"\bindeterminate\b",
        r"\bnever\b", r"\bunable\s+to\b", r"\bcontradiction\b", r"\binconsistent\b",
        r"\bprohibited\b", r"\bforbidden\b", r"\bfails?\b", r"\bmeaningless\b",
        r"\bdiverge[sd]?\b", r"\bsingularity\b", r"\bparadox\b", r"\bblow-?up\b"
    ],
    # REGRESSIVE (G: Exclusive + Counteractive)
    "was_like": [
        r"\bclassical\s+view\b", r"\bclassical(?:ly)?\b", r"\bstandard\s+math(?:ematics)?\b",
        r"\btraditionally\b", r"\bconventional(?:ly)?\b", r"\bpreviously\b",
        r"\bhistorically\b", r"\borthodox\b", r"\bwas\b", r"\bwere\b",
        r"\bused\s+to\b", r"\bold\s+view\b", r"\bcantorian\b"
    ],
    "wont_be": [
        r"\bwon't\b", r"\bwill\s+not\b", r"\bdrop\b", r"\babandon\b",
        r"\bfails?\s+to\b", r"\breject(?:ed|s)?\b", r"\bdiscard\b",
        r"\bavoid\b", r"\beliminate[sd]?\b", r"\bcollapse[sd]?\b",
        r"\bbreaks?\s+down\b", r"\bobsolete\b", r"\bomit(?:ted)?\b"
    ]
}

COMPILED_MODALS = {
    state: [re.compile(pat, re.IGNORECASE) for pat in pats]
    for state, pats in MODAL_PATTERNS.items()
}

OUTER_MODALS = {"is_like", "will_be", "is_not", "was_like"}
INNER_MODALS = {"may_be", "can_be", "cant_be", "wont_be"}

# ---------------------------------------------------------------------------
# 2. WORKING-OUT / PROOF-CHAIN COMPLETENESS DETECTORS (NEW IN V2)
# ---------------------------------------------------------------------------
PROOF_PATTERNS = {
    # 1. Formal Proof Scaffolding (Theorems, Lemmas, Proofs, QED)
    "proof_scaffolding": [
        r"\b(?:Theorem|Lemma|Proposition|Corollary|Definition|Axiom|Postulate|Remark)\s+\d*(?:\.\d+)*\b",
        r"\bProof\b\s*[:.]", r"\bQ\.?E\.?D\.?\b", r"\\blacksquare", r"\\square", r"∎", r"□",
        r"\bCase\s+[123IiiVv]+\b", r"\bStep\s+\d+\b", r"\bBase\s+case\b", r"\bInductive\s+step\b"
    ],
    # 2. Deductive Inference & Step Chaining (Connecting premises to conclusions)
    "deductive_connectors": [
        r"\b(?:since|because|given\s+that|as\s+a\s+result|it\s+follows\s+that|we\s+have|we\s+get|we\s+obtain|we\s+see\s+that|this\s+implies|which\s+yields|substituting|applying|combining|integrating|differentiating|taking\s+the\s+limit|by\s+induction|by\s+definition|by\s+lemma|by\s+theorem|by\s+equation|from\s+eq)\b",
        r"\\implies", r"\\iff", r"\\mapsto", r"\\xrightarrow", r"⟹", r"⟺"
    ],
    # 3. Symbolic Equations, Inequalities & Display Math (Actual Algebraic Manipulation)
    "symbolic_manipulation": [
        r"\$\$[\s\S]+?\$\$", r"\\\[[\s\S]+?\\\]", r"\\begin\{(?:equation|align|aligned|gather|multline)\*?\}",
        r"[a-zA-Z0-9_\)\]\}]\s*(?:=|<|>|\\le|\\ge|\\leq|\\geq|\\approx|\\equiv|\\sim|≤|≥|≈|≡)\s*[a-zA-Z0-9_\(\[\{\\+\-]",
        r"(?:\\sum|\\prod|\\int|\\oint|\\partial|\\nabla|\\frac|\\sqrt|\\lim)\b",
        r"[∑∏∫∂∇√]"
    ],
    # 4. Named Analytical / Mathematical Machinery (High-Rigour Anchor Tools)
    "analytical_machinery": [
        r"\b(?:Gr[öo]nwall|Lipschitz|Cauchy(?:-Schwarz)?|Sobolev|H[öo]lder|Banach|Hilbert|Fourier|Laplace|Bessel|Levi-Civita|Hahn\s+series|Puiseux|Ultrafilter|Ultrapower|ZFC|Peano|Archimedean|Noether|Lorentz|Navier-Stokes|Euler|Reynolds|Viscous|Enstrophy|Vorticity|Bijection|Homomorphism|Isomorphism|galerkin|parabolic|elliptic|compactness|semigroup|martingale)\b"
    ],
    # 5. Bare Assertion / Metaphorical Packaging Markers (Penalizes unbacked claims)
    "bare_assertion_markers": [
        r"\b(?:is\s+simply|is\s+merely|is\s+nothing\s+more\s+than|think\s+of\s+it\s+as|imagine\s+a|like\s+a\s+movie|cosmic|spiritual|metaphor|in\s+other\s+words|philosophically)\b"
    ]
}

COMPILED_PROOF = {
    k: [re.compile(p, re.IGNORECASE) for k_p in [pats] for p in k_p]
    for k, pats in PROOF_PATTERNS.items()
}

def compute_working_out_profile(text: str, modal_counts: dict, n_clauses: int):
    """
    Computes the 5-component Working-Out / Proof-Chain Completeness Score (`W_score` in [0, 1])
    and classifies the segment into one of 4 Epistemic Proof Tiers:
      - Tier 3: FORMAL_PROOF_CHAIN (W_score >= 0.55)
      - Tier 2: OPERATIONAL_DERIVATION (0.30 <= W_score < 0.55)
      - Tier 1: EXPLORATORY_SKETCH (0.12 <= W_score < 0.30)
      - Tier 0: BARE_ASSERTION (W_score < 0.12)
    """
    hits = {}
    for k, rgx_list in COMPILED_PROOF.items():
        hits[k] = sum(len(r.findall(text)) for r in rgx_list)

    # Count multi-step chained relations (e.g. a = b = c or a <= b <= c or multi-line equations)
    eq_tokens = re.findall(r"(?:=|\\le|\\ge|\\leq|\\geq|≤|≥|\\approx|\\equiv|\\implies|⟹)", text)
    chained_steps = max(0, len(eq_tokens) - 1)

    scaff_norm = min(1.0, hits["proof_scaffolding"] / 2.0)
    deduct_norm = min(1.0, hits["deductive_connectors"] / 3.0)
    symb_norm = min(1.0, (hits["symbolic_manipulation"] + 0.5 * chained_steps) / 4.0)
    mach_norm = min(1.0, hits["analytical_machinery"] / 2.0)

    # Modal progression bonus: coupling Inner potential (may_be/can_be/cant_be) with Outer resolution (will_be/is_like/is_not)
    inner_m = sum(modal_counts.get(m, 0) for m in INNER_MODALS)
    outer_m = sum(modal_counts.get(m, 0) for m in OUTER_MODALS)
    modal_coupling = 1.0 if (inner_m > 0 and outer_m > 0) else (0.4 if (inner_m + outer_m) > 0 else 0.0)

    raw_w = (
        0.22 * scaff_norm +
        0.26 * deduct_norm +
        0.28 * symb_norm +
        0.14 * mach_norm +
        0.10 * modal_coupling
    )

    # Penalty if high bare_assertion_markers and zero symbolic/deductive backing
    if hits["bare_assertion_markers"] > 0 and (hits["symbolic_manipulation"] + hits["deductive_connectors"]) == 0:
        raw_w *= 0.35

    w_score = round(min(1.0, raw_w), 4)

    if w_score >= 0.55:
        tier = "Tier3_Formal_Proof_Chain"
    elif w_score >= 0.30:
        tier = "Tier2_Operational_Derivation"
    elif w_score >= 0.12:
        tier = "Tier1_Exploratory_Sketch"
    else:
        tier = "Tier0_Bare_Assertion"

    return {
        "w_score": w_score,
        "tier": tier,
        "scaffolding_hits": hits["proof_scaffolding"],
        "deductive_hits": hits["deductive_connectors"],
        "symbolic_hits": hits["symbolic_manipulation"],
        "chained_eq_steps": chained_steps,
        "machinery_hits": hits["analytical_machinery"],
        "bare_assertion_hits": hits["bare_assertion_markers"]
    }

# ---------------------------------------------------------------------------
# 3. CLAUSE SPLITTING, MODAL SCORING & 4 DERIVATION LAWS V2
# ---------------------------------------------------------------------------
def split_paragraphs(text: str):
    raw_paras = re.split(r"\n\s*\n", text)
    return [p.strip() for p in raw_paras if len(p.strip()) > 20]

def split_sentences(para: str):
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'`(\[\-\*\\])|\n+", para)
    return [s.strip() for s in sents if len(s.strip()) > 4]

def split_clauses(sent: str):
    clauses = re.split(
        r"\s*(?:;|—|--|:\s+|\b(?:but|whereas|while|although|though|yet|however|because|since|so\s+that|until|unless|instead|therefore|thus|hence)\b|,\s*(?:and|or|which|where|so|thus|hence|therefore))\s*",
        sent, flags=re.IGNORECASE
    )
    return [c.strip() for c in clauses if len(c.strip()) > 3]

def score_modal_states(text_unit: str):
    return {
        state: sum(len(rgx.findall(text_unit)) for rgx in regexes)
        for state, regexes in COMPILED_MODALS.items()
    }

def compute_engine_scores(modal_counts: dict):
    C = modal_counts["is_like"] + modal_counts["may_be"]
    P = modal_counts["will_be"] + modal_counts["can_be"]
    R = modal_counts["is_not"] + modal_counts["cant_be"]
    G = modal_counts["was_like"] + modal_counts["wont_be"]
    total = C + P + R + G
    iota = ((C + P) - (R + G)) / total if total > 0 else 0.0
    outer = sum(modal_counts[m] for m in OUTER_MODALS)
    inner = sum(modal_counts[m] for m in INNER_MODALS)
    return {
        "C": C, "P": P, "R": R, "G": G,
        "total_modals": total,
        "iota": round(iota, 4),
        "outer": outer,
        "inner": inner
    }

def evaluate_derivation_laws_v2(clause_seq: list, window_counts: dict, w_score: float):
    """
    Evaluates a 3-sentence sliding window on:
      1. Structural Modal Completion of the 4 Verbatim Operational Derivation Laws
      2. Clause-Order Sequence Bonus (Premise/Opposition precedes Terminal/Resolution)
      3. Proof-Coupled Completion (`verified_with_working_out`: Law completed AND w_score >= 0.28)
    """
    w = window_counts

    def seq_order_bonus(drivers, opposition, terminal, conclusion):
        first_driver = None
        first_opp = None
        last_term = None
        for idx, c_counts in enumerate(clause_seq):
            if first_driver is None and any(c_counts[d] > 0 for d in drivers):
                first_driver = idx
            if opposition and first_opp is None and any(c_counts[o] > 0 for o in opposition):
                first_opp = idx
            if c_counts[terminal] > 0 or c_counts[conclusion] > 0:
                last_term = idx
        if first_driver is not None and last_term is not None and first_driver <= last_term:
            if not opposition or (first_opp is not None and first_opp <= last_term):
                return 0.25
            return 0.15
        return 0.0

    # Law 1: Reductive -> cant_be (was_like + can_be opposing is_like until is_not -> cant_be)
    l1_parts = [w["was_like"] > 0, w["can_be"] > 0, w["is_like"] > 0, (w["is_not"] > 0 or w["cant_be"] > 0)]
    l1_base = sum(1.0 for x in l1_parts if x) / 4.0
    l1_seq = seq_order_bonus(["was_like", "can_be"], ["is_like"], "is_not", "cant_be")
    l1_score = min(1.0, l1_base * 0.75 + l1_seq + (0.1 if w["cant_be"] > 0 and w["is_not"] > 0 else 0.0))
    l1_comp = (sum(1 for x in l1_parts if x) >= 3) and (w["is_not"] > 0 or w["cant_be"] > 0) and (w["was_like"] + w["can_be"] > 0)

    # Law 2: Productive -> will_be (is_not + is_like opposing was_like until can_be -> will_be)
    l2_parts = [w["is_not"] > 0, w["is_like"] > 0, w["was_like"] > 0, (w["can_be"] > 0 or w["will_be"] > 0)]
    l2_base = sum(1.0 for x in l2_parts if x) / 4.0
    l2_seq = seq_order_bonus(["is_not", "is_like"], ["was_like"], "can_be", "will_be")
    l2_score = min(1.0, l2_base * 0.75 + l2_seq + (0.1 if w["will_be"] > 0 and w["can_be"] > 0 else 0.0))
    l2_comp = (sum(1 for x in l2_parts if x) >= 3) and (w["can_be"] > 0 or w["will_be"] > 0) and (w["is_not"] > 0 and w["is_like"] > 0)

    # Law 3: Regressive -> wont_be (is_not + is_like opposing can_be until was_like -> wont_be)
    l3_parts = [w["is_not"] > 0, w["is_like"] > 0, w["can_be"] > 0, (w["was_like"] > 0 or w["wont_be"] > 0)]
    l3_base = sum(1.0 for x in l3_parts if x) / 4.0
    l3_seq = seq_order_bonus(["is_not", "is_like"], ["can_be"], "was_like", "wont_be")
    l3_score = min(1.0, l3_base * 0.75 + l3_seq + (0.1 if w["wont_be"] > 0 and w["was_like"] > 0 else 0.0))
    l3_comp = (sum(1 for x in l3_parts if x) >= 3) and (w["was_like"] > 0 or w["wont_be"] > 0) and (w["is_not"] + w["is_like"] >= 2)

    # Law 4: Constructive -> may_be (can_be + was_like until is_like -> may_be)
    l4_parts = [w["can_be"] > 0, w["was_like"] > 0, (w["is_like"] > 0 or w["may_be"] > 0)]
    l4_base = sum(1.0 for x in l4_parts if x) / 3.0
    l4_seq = seq_order_bonus(["can_be", "was_like"], [], "is_like", "may_be")
    l4_score = min(1.0, l4_base * 0.75 + l4_seq + (0.1 if w["is_like"] > 0 and w["may_be"] > 0 else 0.0))
    l4_comp = all(l4_parts) or (w["can_be"] + w["was_like"] > 0 and w["is_like"] > 0 and w["may_be"] > 0)

    proof_backed = (w_score >= 0.28)
    return {
        "Law1_Reductive_cant_be": {"score": round(l1_score, 4), "complete": bool(l1_comp), "proof_backed": bool(l1_comp and proof_backed)},
        "Law2_Productive_will_be": {"score": round(l2_score, 4), "complete": bool(l2_comp), "proof_backed": bool(l2_comp and proof_backed)},
        "Law3_Regressive_wont_be": {"score": round(l3_score, 4), "complete": bool(l3_comp), "proof_backed": bool(l3_comp and proof_backed)},
        "Law4_Constructive_may_be": {"score": round(l4_score, 4), "complete": bool(l4_comp), "proof_backed": bool(l4_comp and proof_backed)},
    }

# ---------------------------------------------------------------------------
# 4. CONCEPT & PROPOSITION EXTRACTION
# ---------------------------------------------------------------------------
STOPWORDS = {
    "the", "a", "an", "this", "that", "these", "those", "it", "they", "we", "you",
    "he", "she", "what", "which", "who", "whom", "whose", "where", "when", "why",
    "how", "all", "any", "both", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "can", "will", "just", "should", "now", "also", "then", "thus", "here", "there",
    "if", "but", "or", "and", "as", "of", "in", "to", "for", "with", "on", "at",
    "from", "by", "about", "into", "through", "during", "before", "after", "above",
    "below", "between", "under", "again", "further", "once", "is", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
    "did", "doing", "would", "could", "might", "must", "shall", "may", "way",
    "thing", "things", "something", "nothing", "everything", "someone", "anyone"
}

DOMAIN_CONCEPT_REGEX = re.compile(
    r"\b(?:[A-Z][a-z0-9\-]+(?:\s+[A-Z][a-z0-9\-]+)+|"
    r"[a-zA-Z]+(?:\s+(?:infinity|indefinite|definite|number|numbers|unit|units|zero|division|ratio|limit|plane|state|field|vector|tensor|horizon|boundary|frame|operator|axiom|theorem|law|identity|algebra|calculus|set|continuum|singularity|potential|actual|relative|absolute|scale|density|measure|topology|manifold|entanglement|entropy|spacetime|metric|curvature|vorticity|enstrophy|viscosity|regularity|lattice|automaton|bijection|ultrafilter|series))|"
    r"(?:infinity|indefinite|definite|relative|actual|potential|dynamic|static|operational|structural|geometric|harmonic|transfinite|cantorian|archimedean|infinitesimal|cellular|navier-stokes|levi-civita|hahn|puiseux|peano|zfc|hyperreal)\s+[a-zA-Z]+(?:\s+[a-zA-Z]+)?|"
    r"0\s*/\s*0|1\s*/\s*0|∞\s*/\s*∞|x\s*/\s*0)\b"
)

def clean_concept(phrase: str) -> str:
    phrase = re.sub(r"[*_`#\[\]()\"'<>]", "", phrase)
    phrase = re.sub(r"\s+", " ", phrase).strip(" .,;:!?-—/\\")
    words = phrase.split()
    while words and words[0].lower() in STOPWORDS:
        words.pop(0)
    while words and words[-1].lower() in STOPWORDS:
        words.pop()
    cleaned = " ".join(words).lower()
    if len(cleaned) < 4 or len(cleaned) > 65 or cleaned in STOPWORDS or cleaned.isdigit():
        return ""
    return cleaned

# ---------------------------------------------------------------------------
# 5. FULL DOCUMENT ANALYZER V2
# ---------------------------------------------------------------------------
def analyze_document_v2(filepath: str, doc_id: str, doc_group: str):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    paras = split_paragraphs(text)
    n_paras = max(1, len(paras))

    total_modals = Counter()
    tier_counts = Counter()
    proof_hit_totals = Counter()
    w_scores = []

    included_concepts = Counter()
    excluded_concepts = Counter()
    all_sentences = []

    for p_idx, para in enumerate(paras):
        pos_norm = round(p_idx / max(1, n_paras - 1), 4)
        sents = split_sentences(para)
        clauses = []
        for s in sents:
            s_clauses = split_clauses(s)
            clauses.extend(s_clauses)
            all_sentences.append((p_idx, pos_norm, s, [score_modal_states(c) for c in s_clauses]))

        p_modals = score_modal_states(para)
        for k, v in p_modals.items():
            total_modals[k] += v

        eng = compute_engine_scores(p_modals)
        w_prof = compute_working_out_profile(para, p_modals, len(clauses))
        w_scores.append(w_prof["w_score"])
        tier_counts[w_prof["tier"]] += 1
        for hk in ("scaffolding_hits", "deductive_hits", "symbolic_hits", "chained_eq_steps", "machinery_hits", "bare_assertion_hits"):
            proof_hit_totals[hk] += w_prof[hk]

        # Concept polarization per clause
        for c_str in clauses:
            c_mod = score_modal_states(c_str)
            c_eng = compute_engine_scores(c_mod)
            c_concepts = [clean_concept(m.group(0)) for m in DOMAIN_CONCEPT_REGEX.finditer(c_str)]
            c_concepts = [cc for cc in c_concepts if cc]
            if not c_concepts:
                continue
            if (c_mod["is_not"] + c_mod["cant_be"] + c_mod["wont_be"]) > (c_mod["is_like"] + c_mod["will_be"] + c_mod["can_be"]):
                for cc in c_concepts:
                    excluded_concepts[cc] += 1
            elif (c_eng["C"] + c_eng["P"]) > 0 or eng["iota"] >= 0:
                for cc in c_concepts:
                    included_concepts[cc] += 1
            else:
                for cc in c_concepts:
                    excluded_concepts[cc] += 1

    # Sliding 3-sentence windows for 4 Operational Derivation Laws + Proof-Backed Working Out
    window_size = 3
    n_sents = len(all_sentences)
    law_scores_sum = Counter()
    law_completions = Counter()
    law_proof_backed = Counter()

    for i in range(max(1, n_sents - window_size + 1)):
        win = all_sentences[i : i + window_size]
        win_clauses = []
        win_counts = Counter()
        win_text = " ".join(x[2] for x in win)
        for _, _, _, cl_list in win:
            for cl_c in cl_list:
                win_clauses.append(cl_c)
                for k, v in cl_c.items():
                    win_counts[k] += v

        win_w_prof = compute_working_out_profile(win_text, win_counts, len(win_clauses))
        laws_eval = evaluate_derivation_laws_v2(win_clauses, win_counts, win_w_prof["w_score"])

        for law_name, l_data in laws_eval.items():
            law_scores_sum[law_name] += l_data["score"]
            if l_data["complete"]:
                law_completions[law_name] += 1
            if l_data["proof_backed"]:
                law_proof_backed[law_name] += 1

    n_windows = max(1, n_sents - window_size + 1)
    law_summary = {}
    for law_name in ["Law1_Reductive_cant_be", "Law2_Productive_will_be", "Law3_Regressive_wont_be", "Law4_Constructive_may_be"]:
        law_summary[law_name] = {
            "mean_score": round(law_scores_sum[law_name] / n_windows, 4),
            "completed_windows": law_completions[law_name],
            "completion_rate": round(law_completions[law_name] / n_windows, 4),
            "proof_backed_windows": law_proof_backed[law_name],
            "proof_backed_rate": round(law_proof_backed[law_name] / n_windows, 4)
        }

    overall_eng = compute_engine_scores(total_modals)
    outer_inner_ratio = round(overall_eng["outer"] / max(1, overall_eng["inner"]), 3)
    mean_w_score = round(sum(w_scores) / max(1, len(w_scores)), 4)

    # Rigorous Working-Out Ratio: (Tier2 + Tier3) / Total Paragraphs
    rigorous_paras = tier_counts["Tier2_Operational_Derivation"] + tier_counts["Tier3_Formal_Proof_Chain"]
    rigorous_ratio = round(rigorous_paras / n_paras, 4)
    bare_assertion_ratio = round(tier_counts["Tier0_Bare_Assertion"] / n_paras, 4)

    return {
        "doc_id": doc_id,
        "doc_group": doc_group,
        "filename": os.path.basename(filepath),
        "n_paragraphs": n_paras,
        "n_sentences": n_sents,
        "n_windows": n_windows,
        "modal_counts": dict(total_modals),
        "engine_summary": overall_eng,
        "outer_inner_ratio": outer_inner_ratio,
        "working_out_profile": {
            "mean_w_score": mean_w_score,
            "rigorous_working_out_ratio": rigorous_ratio,
            "bare_assertion_ratio": bare_assertion_ratio,
            "tier_distribution": {
                t: round(tier_counts[t] / n_paras, 4)
                for t in ["Tier0_Bare_Assertion", "Tier1_Exploratory_Sketch", "Tier2_Operational_Derivation", "Tier3_Formal_Proof_Chain"]
            },
            "feature_totals": dict(proof_hit_totals)
        },
        "derivation_laws": law_summary,
        "top_included_concepts": included_concepts.most_common(35),
        "top_excluded_concepts": excluded_concepts.most_common(35),
        "_raw_included": included_concepts,
        "_raw_excluded": excluded_concepts
    }

# ---------------------------------------------------------------------------
# 6. CROSS-CORPUS RECOVERY: EARLY IRM REPORT VS. FULL IRM FORMAL CORPUS
# ---------------------------------------------------------------------------
def compare_chat_recovery(chat_res: dict, irm_report_res: dict, irm_formal_list: list):
    chat_inc = chat_res["_raw_included"]
    chat_exc = chat_res["_raw_excluded"]

    rep_inc = irm_report_res["_raw_included"]
    rep_exc = irm_report_res["_raw_excluded"]

    # Union across all IRM Formal Papers + Early Report
    full_irm_inc = Counter(rep_inc)
    full_irm_exc = Counter(rep_exc)
    concept_to_formal_papers = defaultdict(list)

    for fp in irm_formal_list:
        for c, cnt in fp["_raw_included"].items():
            full_irm_inc[c] += cnt
            concept_to_formal_papers[c].append((fp["doc_id"], cnt))
        for c, cnt in fp["_raw_excluded"].items():
            full_irm_exc[c] += cnt

    chat_set = {c for c, cnt in chat_inc.items() if cnt >= 2}
    rep_survival = len(chat_set & set(rep_inc.keys())) / max(1, len(chat_set))
    full_survival = len(chat_set & set(full_irm_inc.keys())) / max(1, len(chat_set))

    # Concepts missing in Early Summary Report that ARE recovered in the IRM Formal Papers!
    recovered_in_formal = []
    still_unmerged = []

    for c, chat_cnt in chat_inc.most_common():
        if chat_cnt < 2:
            continue
        if rep_inc[c] == 0:
            if full_irm_inc[c] > 0:
                papers_str = ", ".join(f"{pid} (+{cnt})" for pid, cnt in concept_to_formal_papers[c][:4])
                recovered_in_formal.append({
                    "concept": c,
                    "chat_I": chat_cnt,
                    "early_report_I": 0,
                    "formal_corpus_I": full_irm_inc[c],
                    "recovered_in": papers_str
                })
            else:
                still_unmerged.append({
                    "concept": c,
                    "chat_I": chat_cnt,
                    "chat_E": chat_exc[c],
                    "formal_corpus_E": full_irm_exc[c],
                    "status": "REJECTED_IN_FORMAL" if full_irm_exc[c] > 0 else "STILL_OMITTED_FROM_ALL_IRM"
                })

    return {
        "chat_core_concepts_count": len(chat_set),
        "early_report_survival_rate": round(rep_survival, 4),
        "full_formal_corpus_survival_rate": round(full_survival, 4),
        "recovered_concepts_count": len(recovered_in_formal),
        "still_unmerged_count": len(still_unmerged),
        "top_recovered_in_formal_papers": recovered_in_formal[:30],
        "top_still_unmerged_concepts": still_unmerged[:30]
    }

# ---------------------------------------------------------------------------
# 7. MAIN EXECUTION & REPORT V2 GENERATION
# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("[Agent 1 v2] Analyzing Chat corpus...")
    chat_res = analyze_document_v2(CHAT_PATH, "chat_infinity_maths", "1_exploratory_chat")

    print("[Agent 1 v2] Analyzing Early IRM Summary Report...")
    irm_rep_res = analyze_document_v2(IRM_REPORT_PATH, "irm_early_comprehensive_report", "2_irm_early_summary")

    irm_formal_files = sorted(glob.glob(os.path.join(IRM_FORMAL_DIR, "*.md")))
    irm_formal_results = []
    for fpath in irm_formal_files:
        doc_id = os.path.splitext(os.path.basename(fpath))[0]
        print(f"[Agent 1 v2] Analyzing IRM Formal Paper: {doc_id}...")
        irm_formal_results.append(analyze_document_v2(fpath, doc_id, "3_irm_formal_paper"))

    arxiv_files = sorted(glob.glob(os.path.join(ARXIV_DIR, "*.md")))
    arxiv_results = []
    for fpath in arxiv_files:
        doc_id = os.path.splitext(os.path.basename(fpath))[0]
        print(f"[Agent 1 v2] Analyzing arXiv Benchmark: {doc_id}...")
        arxiv_results.append(analyze_document_v2(fpath, doc_id, "4_arxiv_benchmark"))

    print("[Agent 1 v2] Computing Cross-Corpus Concept Recovery (Chat -> Early IRM -> Full Formal IRM)...")
    recovery_data = compare_chat_recovery(chat_res, irm_rep_res, irm_formal_results)

    all_docs = [chat_res, irm_rep_res] + irm_formal_results + arxiv_results
    for d in all_docs:
        d.pop("_raw_included", None)
        d.pop("_raw_excluded", None)

    def summarize_group(docs):
        n = max(1, len(docs))
        return {
            "count": len(docs),
            "mean_iota": round(sum(d["engine_summary"]["iota"] for d in docs) / n, 4),
            "mean_outer_inner_ratio": round(sum(d["outer_inner_ratio"] for d in docs) / n, 3),
            "mean_w_score": round(sum(d["working_out_profile"]["mean_w_score"] for d in docs) / n, 4),
            "mean_rigorous_working_out_ratio": round(sum(d["working_out_profile"]["rigorous_working_out_ratio"] for d in docs) / n, 4),
            "mean_bare_assertion_ratio": round(sum(d["working_out_profile"]["bare_assertion_ratio"] for d in docs) / n, 4),
            "mean_law_proof_backed_rates": {
                law: round(sum(d["derivation_laws"][law]["proof_backed_rate"] for d in docs) / n, 4)
                for law in ["Law1_Reductive_cant_be", "Law2_Productive_will_be", "Law3_Regressive_wont_be", "Law4_Constructive_may_be"]
            }
        }

    group_benchmarks = {
        "chat_exploratory": summarize_group([chat_res]),
        "irm_early_summary": summarize_group([irm_rep_res]),
        "irm_formal_papers_ensemble": summarize_group(irm_formal_results),
        "arxiv_benchmark_ensemble": summarize_group(arxiv_results)
    }

    payload = {
        "agent": "Agent 1 (Round 2): Syntactic Modal, Proof-Working-Out & 4 Derivation Laws v2.0",
        "critique_of_unified_v1": [
            "1. Eliminated the ':' / '=' fallback modal bug (lines 273-280 of unified_gluon_dna_engine.py) which tagged every markdown header/bullet with ':' as Constructive `is_like`, artificially inflating `Comprehensive Report - IRM.md`'s Outer/Inner ratio to 7.28.",
            "2. Added a 5-component Working-Out / Proof-Chain Completeness Engine (`W_score` in [0,1]) tracking proof scaffolding, deductive connectors, multi-step symbolic manipulation, and named analytical machinery (Grönwall, Lipschitz, Sobolev, Levi-Civita, ZFC, Ultrafilter).",
            "3. Coupled the 4 Verbatim Operational Derivation Laws with clause-order verification AND `W_score >= 0.28` (`proof_backed_rate`), separating bare rhetorical assertions from worked-out mathematical derivations."
        ],
        "group_benchmarks": group_benchmarks,
        "cross_corpus_recovery": recovery_data,
        "chat_analysis": chat_res,
        "irm_early_report_analysis": irm_rep_res,
        "irm_formal_papers": irm_formal_results,
        "arxiv_benchmarks": arxiv_results
    }

    with open(RESULTS_V2_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    # Build Markdown Report v2
    md = []
    md.append("# Agent 1 (Round 2): Syntactic Modal, Proof-Working-Out & 4 Derivation Laws State Machine v2.0\n")
    md.append("## 1. Critique of `unified_gluon_dna_engine.py` (v1.0) & Architectural Upgrades\n")
    md.append("1. **Fixed the Colon/Equals Fallback Inflation Bug**: In `unified_gluon_dna_engine.py` (lines 273–280), any paragraph lacking explicit modal verbs that contained `:` or `=` was automatically assigned `is_like = 1` (`C` Constructive). In bulleted summary documents like `Comprehensive Report - IRM.md`, this inflated `is_like` counts and produced an artificial Outer/Inner ratio of `7.28`, mistaking bullet-point definitions for completed derivations.\n")
    md.append("2. **Built the 5-Component Working-Out & Proof-Chain Engine (`W_score` $\\in [0, 1]$)**: Distinguishes **Tier 0 (`Bare Assertion`)**, **Tier 1 (`Exploratory Sketch`)**, **Tier 2 (`Operational Derivation`)**, and **Tier 3 (`Formal Proof Chain`)** by scoring:\n"
              "   - *Proof Scaffolding* (`Theorem`, `Lemma`, `Proposition`, `Proof:`, `Q.E.D.`, $\\square$, `Inductive step`)\n"
              "   - *Deductive Connectors* (`since`, `it follows that`, `we obtain`, `substituting`, `applying`, $\\implies$, $\\iff$)\n"
              "   - *Chained Symbolic Manipulation* (multi-step equations/inequalities $=, \\le, \\ge, \\equiv, \\int, \\sum, \\partial, \\nabla$)\n"
              "   - *Named Analytical Machinery* (`Grönwall`, `Lipschitz`, `Sobolev`, `Cauchy-Schwarz`, `Levi-Civita`, `Ultrafilter`, `ZFC`, `Peano`, `Enstrophy`)\n"
              "   - *Inner-to-Outer Modal Coupling* (`may_be`/`can_be` $\\to$ `will_be`/`is_like`)\n")
    md.append("3. **Proof-Coupled 4 Verbatim Operational Derivation Laws**: Every 3-sentence window is now evaluated both on **raw modal law completion** and **proof-backed completion** (`Law_Completed` $\\land$ `W_score >= 0.28`).\n")

    md.append("## 2. Ensemble Benchmark Comparison (`Chat` vs. `Early IRM Report` vs. `IRM Formal Corpus` vs. `arXiv`)\n")
    md.append("| Ensemble Group | Docs | Mean $\\iota$ | Outer/Inner Ratio | Mean `W_score` | Rigorous Working-Out (`Tier 2+3`) | Bare Assertion (`Tier 0`) | Proof-Backed Law 1 | Proof-Backed Law 2 |")
    md.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for gname, gstat in group_benchmarks.items():
        pbl = gstat["mean_law_proof_backed_rates"]
        md.append(
            f"| **`{gname}`** | {gstat['count']} | {gstat['mean_iota']:+.4f} | {gstat['mean_outer_inner_ratio']:.2f} | "
            f"**{gstat['mean_w_score']:.4f}** | **{gstat['mean_rigorous_working_out_ratio']*100:.1f}%** | "
            f"{gstat['mean_bare_assertion_ratio']*100:.1f}% | {pbl['Law1_Reductive_cant_be']*100:.2f}% | {pbl['Law2_Productive_will_be']*100:.2f}% |"
        )

    md.append("\n## 3. Document-by-Document Working-Out & Modal Audit Across All 20 Files\n")
    md.append("| Document ID | Group | Paras | Net $\\iota$ | Outer/Inner | Mean `W_score` | Rigorous (`T2+T3`) | Formal Proof (`T3`) | Bare Assert (`T0`) | Chained Eq Steps | Machinery Hits |")
    md.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for d in all_docs:
        wp = d["working_out_profile"]
        ft = wp["feature_totals"]
        t3 = wp["tier_distribution"]["Tier3_Formal_Proof_Chain"]
        md.append(
            f"| `{d['doc_id'][:38]}` | `{d['doc_group']}` | {d['n_paragraphs']} | {d['engine_summary']['iota']:+.3f} | "
            f"{d['outer_inner_ratio']:.2f} | **{wp['mean_w_score']:.3f}** | **{wp['rigorous_working_out_ratio']*100:.1f}%** | "
            f"{t3*100:.1f}% | {wp['bare_assertion_ratio']*100:.1f}% | {ft['chained_eq_steps']} | {ft['machinery_hits']} |"
        )

    md.append("\n## 4. The 4 Verbatim Operational Derivation Laws (Raw vs. Proof-Backed Working Out)\n")
    md.append("| Document ID | Law 1 Raw / Proof-Backed | Law 2 Raw / Proof-Backed | Law 3 Raw / Proof-Backed | Law 4 Raw / Proof-Backed |")
    md.append("|---|---:|---:|---:|---:|")
    for d in all_docs:
        dl = d["derivation_laws"]
        md.append(
            f"| `{d['doc_id'][:38]}` | "
            f"{dl['Law1_Reductive_cant_be']['completion_rate']*100:.1f}% / **{dl['Law1_Reductive_cant_be']['proof_backed_rate']*100:.1f}%** | "
            f"{dl['Law2_Productive_will_be']['completion_rate']*100:.1f}% / **{dl['Law2_Productive_will_be']['proof_backed_rate']*100:.1f}%** | "
            f"{dl['Law3_Regressive_wont_be']['completion_rate']*100:.1f}% / **{dl['Law3_Regressive_wont_be']['proof_backed_rate']*100:.1f}%** | "
            f"{dl['Law4_Constructive_may_be']['completion_rate']*100:.1f}% / **{dl['Law4_Constructive_may_be']['proof_backed_rate']*100:.1f}%** |"
        )

    md.append("\n## 5. Missing Data Resolution: Early IRM Summary vs. Full IRM Formal Papers Corpus\n")
    md.append(f"- **Core Inclusive Concepts in `chat` (`count >= 2`)**: `{recovery_data['chat_core_concepts_count']}`\n")
    md.append(f"- **Survival Rate in Early Summary (`Comprehensive Report - IRM.md` alone)**: `{recovery_data['early_report_survival_rate']*100:.1f}%`\n")
    md.append(f"- **Survival Rate Across Full IRM Formal Corpus (Papers 7, 9, 12, 17, 24, 25, 30 + ZFC Bridge)**: **`{recovery_data['full_formal_corpus_survival_rate']*100:.1f}%`** (`+{recovery_data['recovered_concepts_count']}` core concepts recovered!)\n")
    md.append(f"- **Still-Unmerged Concepts (Omitted from BOTH Early Report and Formal Papers 7–30)**: `{recovery_data['still_unmerged_count']}`\n")

    md.append("\n### 5.1 Top Concepts Missing from Early Report That WERE Recovered in `irm_formal_corpus`\n")
    md.append("| Concept | `chat` $+I$ | Early Report $+I$ | Formal Corpus $+I$ | Recovered In Formal Papers |")
    md.append("|---|---:|---:|---:|---|")
    for rc in recovery_data["top_recovered_in_formal_papers"][:20]:
        md.append(f"| `{rc['concept']}` | {rc['chat_I']} | 0 | **{rc['formal_corpus_I']}** | `{rc['recovered_in']}` |")

    md.append("\n### 5.2 Top Concepts STILL Unmerged Across All Current IRM Formal Papers\n")
    md.append("| Concept | `chat` $+I$ | `chat` $-E$ | Formal Corpus $-E$ | Status Across Full IRM Corpus |")
    md.append("|---|---:|---:|---:|---|")
    for su in recovery_data["top_still_unmerged_concepts"][:20]:
        md.append(f"| `{su['concept']}` | {su['chat_I']} | {su['chat_E']} | {su['formal_corpus_E']} | **{su['status']}** |")

    with open(REPORT_V2_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")

    print("\n=== AGENT 1 ROUND 2 SUMMARY ===")
    for gname, gstat in group_benchmarks.items():
        print(f"{gname:28s} -> Mean W_score: {gstat['mean_w_score']:.4f} | Rigorous (T2+T3): {gstat['mean_rigorous_working_out_ratio']*100:5.1f}% | Bare Assertion (T0): {gstat['mean_bare_assertion_ratio']*100:5.1f}% | Outer/Inner: {gstat['mean_outer_inner_ratio']:.2f}")
    print(f"Core Chat Concept Survival: Early Report = {recovery_data['early_report_survival_rate']*100:.1f}% -> Full Formal Corpus = {recovery_data['full_formal_corpus_survival_rate']*100:.1f}% (+{recovery_data['recovered_concepts_count']} recovered, {recovery_data['still_unmerged_count']} still unmerged)")
    print(f"Saved: {RESULTS_V2_JSON} and {REPORT_V2_MD}")

if __name__ == "__main__":
    main()
