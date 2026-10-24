#!/usr/bin/env python3
"""
Agent 1: Syntactic Modal & Derivation-Law State Machine
Semantic Gluon Transformer & DNA Reading Head
"""

import os
import re
import json
import math
import glob
from collections import Counter, defaultdict

# Paths
BASE_PHYSICS = r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics"
CHAT_PATH = os.path.join(BASE_PHYSICS, "chatgpt infinity maths.md")
IRM_PATH = os.path.join(BASE_PHYSICS, "Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md")
ARXIV_DIR = os.path.join(BASE_PHYSICS, "semantic_gluon_dna", "arxiv_samples")
OUT_DIR = os.path.join(BASE_PHYSICS, "semantic_gluon_dna", "agent_1_syntactic_modal")
RESULTS_JSON = os.path.join(OUT_DIR, "results.json")
REPORT_MD = os.path.join(OUT_DIR, "report.md")

# ---------------------------------------------------------------------------
# 1. 8 MODAL STATES & 4 ENGINES PATTERNS
# ---------------------------------------------------------------------------
MODAL_PATTERNS = {
    # Constructive (C: Inclusive + Counteractive)
    "is_like": [
        r"\bis defined as\b", r"\bdefined as\b", r"\brepresents\b", r"\bis like\b",
        r"\banalogous to\b", r"\bform of\b", r"\bis the\b", r"\bis a\b",
        r"\bcorresponds to\b", r"\bdenotes\b", r"\bacts as\b", r"\bviewed as\b",
        r"\binterpreted as\b", r"\bmeans that\b", r"\bequivalent to\b", r"\b:=|≡\b"
    ],
    "may_be": [
        r"\bmay\b", r"\bmight\b", r"\bcould\b", r"\bsuppose\b", r"\bif we\b",
        r"\bwhat if\b", r"\bimagine\b", r"\blet us\b", r"\blet's\b", r"\bassume\b",
        r"\bhypothesize\b", r"\bconsider\b", r"\bpotentially\b", r"\bperhaps\b"
    ],
    # Productive (P: Inclusive + Active)
    "will_be": [
        r"\bwill\b", r"\bmust\b", r"\btherefore\b", r"\byields\b",
        r"\bresolves into\b", r"\bresolves to\b", r"\bproves\b", r"\bthus\b",
        r"\bhence\b", r"\bconsequently\b", r"\bit follows\b", r"\bnecessarily\b",
        r"\bresults in\b", r"\bproduces\b", r"\bgives us\b", r"\bestablishes\b"
    ],
    "can_be": [
        r"\bcan\b", r"\ballows\b", r"\benables\b", r"\bcapable\b",
        r"\bpossible to\b", r"\bpermits\b", r"\bwe can\b", r"\bable to\b",
        r"\bsucceeds in\b", r"\bachieves\b", r"\boperates\b", r"\bfunctions as\b"
    ],
    # Reductive (R: Exclusive + Active)
    "is_not": [
        r"\bis not\b", r"\bisn't\b", r"\bare not\b", r"\baren't\b", r"\bnot a\b",
        r"\bdoes not\b", r"\bdoesn't\b", r"\bdo not\b", r"\bdon't\b",
        r"\bundefined\b", r"\bno longer\b", r"\brather than\b", r"\binstead of\b",
        r"\bdistinct from\b", r"\bunlike\b", r"\bneither\b", r"\bnor\b"
    ],
    "cant_be": [
        r"\bcannot\b", r"\bcan't\b", r"\bimpossible\b", r"\bindeterminate\b",
        r"\bnever\b", r"\bunable to\b", r"\bcontradiction\b", r"\binconsistent\b",
        r"\bprohibited\b", r"\bforbidden\b", r"\bfails\b", r"\bmeaningless\b",
        r"\bdiverge[sd]?\b", r"\bsingularity\b", r"\bparadox\b"
    ],
    # Regressive (G: Exclusive + Counteractive)
    "was_like": [
        r"\bclassical view\b", r"\bclassical\b", r"\bstandard math\b",
        r"\bstandard mathematics\b", r"\btraditionally\b", r"\bconventional\b",
        r"\bpreviously\b", r"\bhistorically\b", r"\borthodox\b", r"\bwas\b",
        r"\bwere\b", r"\bused to\b", r"\bold view\b", r"\btextbook\b", r"\bcantorian\b"
    ],
    "wont_be": [
        r"\bwon't\b", r"\bwill not\b", r"\bdrop\b", r"\babandon\b",
        r"\bfails to\b", r"\breject\b", r"\bdiscard\b", r"\bavoid\b",
        r"\beliminate\b", r"\bcollapse[sd]?\b", r"\bbreaks down\b", r"\bobsolete\b"
    ]
}

COMPILED_MODALS = {
    state: [re.compile(pat, re.IGNORECASE) for pat in pats]
    for state, pats in MODAL_PATTERNS.items()
}

ENGINE_MAP = {
    "C": ("is_like", "may_be"),
    "P": ("will_be", "can_be"),
    "R": ("is_not", "cant_be"),
    "G": ("was_like", "wont_be")
}

# ---------------------------------------------------------------------------
# 2. PROPOSITION & CONCEPT EXTRACTION PATTERNS
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

# Contrastive & Definition regex patterns for explicit (+I) vs (-E) propositions
CONTRAST_PATTERNS = [
    # "X is not A, (it/X) is B" or "not A, but B"
    (re.compile(r"([A-Za-z0-9_\-\s/∞÷×\+\=]{3,45}?)\s+(?:is not|isn't|are not|does not mean)\s+([A-Za-z0-9_\-\s/∞÷×\+\=]{3,50}?)\s*[,;—]\s*(?:but|rather|instead|it is|they are)\s+([A-Za-z0-9_\-\s/∞÷×\+\=]{3,60})", re.I),
     "contrast_not_but"),
    # "rather than A, B" or "instead of A, we have B"
    (re.compile(r"(?:rather than|instead of)\s+([A-Za-z0-9_\-\s/∞÷×\+\=]{3,50}?)\s*,\s*(?:we have|it is|this is|irm uses|we define|we get)?\s*([A-Za-z0-9_\-\s/∞÷×\+\=]{3,60})", re.I),
     "rather_than"),
    # "X is defined as Y" / "define X as Y" / "X represents Y"
    (re.compile(r"([A-Za-z0-9_\-\s/∞÷×\+\=]{3,45}?)\s+(?:is defined as|defined as|represents|denotes|is the ratio of|resolves into)\s+([A-Za-z0-9_\-\s/∞÷×\+\=]{3,65})", re.I),
     "definition_inc"),
    # "X is undefined / impossible / indeterminate in standard math"
    (re.compile(r"([A-Za-z0-9_\-\s/∞÷×\+\=]{3,45}?)\s+(?:is|are|was|were|remains)\s+(?:undefined|indeterminate|impossible|meaningless|a contradiction|rejected|abandoned)(?:\s+in\s+[A-Za-z0-9_\-\s]{3,35})?", re.I),
     "negation_exc"),
]

DOMAIN_CONCEPT_REGEX = re.compile(
    r"\b(?:[A-Z][a-z0-9\-]+(?:\s+[A-Z][a-z0-9\-]+)+|"
    r"[a-zA-Z]+(?:\s+(?:infinity|indefinite|definite|number|numbers|unit|units|zero|division|ratio|limit|plane|state|field|vector|tensor|horizon|boundary|frame|operator|axiom|theorem|law|identity|algebra|calculus|set|continuum|singularity|potential|actual|relative|absolute|scale|density|measure|topology|manifold|entanglement|entropy|spacetime|metric|curvature))|"
    r"(?:infinity|indefinite|definite|relative|actual|potential|dynamic|static|operational|structural|geometric|harmonic|transfinite|cantorian|archimedean|infinitesimal)\s+[a-zA-Z]+(?:\s+[a-zA-Z]+)?|"
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
    if len(cleaned) < 4 or len(cleaned) > 65:
        return ""
    if cleaned in STOPWORDS or cleaned.isdigit():
        return ""
    return cleaned

# ---------------------------------------------------------------------------
# 3. CLAUSE & SENTENCE SPLITTING + MODAL SCORING
# ---------------------------------------------------------------------------
def split_paragraphs(text: str):
    raw_paras = re.split(r"\n\s*\n", text)
    paras = []
    for p in raw_paras:
        p_clean = p.strip()
        if len(p_clean) > 20:
            paras.append(p_clean)
    return paras

def split_sentences(para: str):
    # Split on sentence boundaries while keeping formulas intact
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'`(\[\-\*])|\n+", para)
    return [s.strip() for s in sents if len(s.strip()) > 5]

def split_clauses(sent: str):
    # Split sentence into syntactic clauses on conjunctions, semicolons, colons, dashes, or comma-conjunctions
    clauses = re.split(
        r"\s*(?:;|—|--|:\s+|\b(?:but|whereas|while|although|though|yet|however|because|since|so that|until|unless|whereas|instead)\b|,\s*(?:and|or|which|where|so|thus|hence|therefore))\s*",
        sent, flags=re.IGNORECASE
    )
    return [c.strip() for c in clauses if len(c.strip()) > 3]

def score_modal_states(text_unit: str):
    counts = {}
    for state, regexes in COMPILED_MODALS.items():
        c = 0
        for rgx in regexes:
            c += len(rgx.findall(text_unit))
        counts[state] = c
    return counts

def compute_engine_scores(modal_counts: dict):
    C = modal_counts["is_like"] + modal_counts["may_be"]
    P = modal_counts["will_be"] + modal_counts["can_be"]
    R = modal_counts["is_not"] + modal_counts["cant_be"]
    G = modal_counts["was_like"] + modal_counts["wont_be"]
    total = C + P + R + G
    iota = ((C + P) - (R + G)) / total if total > 0 else 0.0
    # Outer vs Inner balance
    outer = modal_counts["is_like"] + modal_counts["will_be"] + modal_counts["is_not"] + modal_counts["was_like"]
    inner = modal_counts["may_be"] + modal_counts["can_be"] + modal_counts["cant_be"] + modal_counts["wont_be"]
    return {
        "C": C, "P": P, "R": R, "G": G,
        "total_modals": total,
        "iota": round(iota, 4),
        "outer": outer,
        "inner": inner
    }

# ---------------------------------------------------------------------------
# 4. THE 4 VERBATIM OPERATIONAL DERIVATION LAWS DETECTOR
# ---------------------------------------------------------------------------
def evaluate_derivation_laws_window(clause_seq: list, window_Counts: dict):
    """
    Evaluates a multi-sentence window on how well it completes the 4 Verbatim Operational Derivation Laws.
    Both structural presence (ingredients + target state) and sequential ordering bonus (ingredients -> target)
    are combined into a continuous completion score in [0, 1] and a boolean 'completed' flag.

    - Law 1 (Reductive -> cant_be): Uses was_like + can_be opposing is_like until is_not (-> cant_be).
    - Law 2 (Productive -> will_be): Uses is_not + is_like opposing was_like until can_be (-> will_be).
    - Law 3 (Regressive -> wont_be): Uses is_not + is_like opposing can_be until was_like (-> wont_be).
    - Law 4 (Constructive -> may_be): Uses can_be + was_like until is_like (-> may_be).
    """
    w = window_Counts

    def seq_order_bonus(drivers, opposition, terminal, conclusion):
        """Checks if drivers/opposition appear before or at terminal/conclusion across clauses."""
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

    # Law 1: Reductive -> cant_be
    # Ingredients: was_like, can_be, opposing is_like, until is_not -> cant_be
    l1_parts = [
        1.0 if w["was_like"] > 0 else 0.0,
        1.0 if w["can_be"] > 0 else 0.0,
        1.0 if w["is_like"] > 0 else 0.0,
        1.0 if (w["is_not"] > 0 or w["cant_be"] > 0) else 0.0,
    ]
    l1_base = sum(l1_parts) / 4.0
    l1_seq = seq_order_bonus(["was_like", "can_be"], ["is_like"], "is_not", "cant_be")
    l1_score = min(1.0, l1_base * 0.8 + l1_seq + (0.1 if w["cant_be"] > 0 and w["is_not"] > 0 else 0.0))
    l1_complete = (sum(l1_parts) >= 3.0) and (w["is_not"] > 0 or w["cant_be"] > 0) and (w["was_like"] + w["can_be"] > 0)

    # Law 2: Productive -> will_be
    # Ingredients: is_not, is_like, opposing was_like, until can_be -> will_be
    l2_parts = [
        1.0 if w["is_not"] > 0 else 0.0,
        1.0 if w["is_like"] > 0 else 0.0,
        1.0 if w["was_like"] > 0 else 0.0,
        1.0 if (w["can_be"] > 0 or w["will_be"] > 0) else 0.0,
    ]
    l2_base = sum(l2_parts) / 4.0
    l2_seq = seq_order_bonus(["is_not", "is_like"], ["was_like"], "can_be", "will_be")
    l2_score = min(1.0, l2_base * 0.8 + l2_seq + (0.1 if w["will_be"] > 0 and w["can_be"] > 0 else 0.0))
    l2_complete = (sum(l2_parts) >= 3.0) and (w["can_be"] > 0 or w["will_be"] > 0) and (w["is_not"] > 0 and w["is_like"] > 0)

    # Law 3: Regressive -> wont_be
    # Ingredients: is_not, is_like, opposing can_be, until was_like -> wont_be
    l3_parts = [
        1.0 if w["is_not"] > 0 else 0.0,
        1.0 if w["is_like"] > 0 else 0.0,
        1.0 if w["can_be"] > 0 else 0.0,
        1.0 if (w["was_like"] > 0 or w["wont_be"] > 0) else 0.0,
    ]
    l3_base = sum(l3_parts) / 4.0
    l3_seq = seq_order_bonus(["is_not", "is_like"], ["can_be"], "was_like", "wont_be")
    l3_score = min(1.0, l3_base * 0.8 + l3_seq + (0.1 if w["wont_be"] > 0 and w["was_like"] > 0 else 0.0))
    l3_complete = (sum(l3_parts) >= 3.0) and (w["was_like"] > 0 or w["wont_be"] > 0) and (w["is_not"] + w["is_like"] >= 2)

    # Law 4: Constructive -> may_be
    # Ingredients: can_be + was_like until is_like (-> may_be)
    l4_parts = [
        1.0 if w["can_be"] > 0 else 0.0,
        1.0 if w["was_like"] > 0 else 0.0,
        1.0 if (w["is_like"] > 0 or w["may_be"] > 0) else 0.0,
    ]
    l4_base = sum(l4_parts) / 3.0
    l4_seq = seq_order_bonus(["can_be", "was_like"], [], "is_like", "may_be")
    l4_score = min(1.0, l4_base * 0.8 + l4_seq + (0.1 if w["is_like"] > 0 and w["may_be"] > 0 else 0.0))
    l4_complete = (sum(l4_parts) == 3.0) or (w["can_be"] + w["was_like"] > 0 and w["is_like"] > 0 and w["may_be"] > 0)

    return {
        "Law1_Reductive_cant_be": {"score": round(l1_score, 4), "complete": bool(l1_complete)},
        "Law2_Productive_will_be": {"score": round(l2_score, 4), "complete": bool(l2_complete)},
        "Law3_Regressive_wont_be": {"score": round(l3_score, 4), "complete": bool(l3_complete)},
        "Law4_Constructive_may_be": {"score": round(l4_score, 4), "complete": bool(l4_complete)},
    }

# ---------------------------------------------------------------------------
# 5. DOCUMENT ANALYZER
# ---------------------------------------------------------------------------
def analyze_document(filepath: str, doc_id: str, doc_type: str):
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()

    paras = split_paragraphs(text)
    n_paras = len(paras)

    total_modals = Counter()
    total_engines = Counter()
    para_trajectory = []
    included_concepts = Counter()
    excluded_concepts = Counter()
    explicit_propositions = []

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
        for k in ("C", "P", "R", "G"):
            total_engines[k] += eng[k]

        # Extract explicit contrast/definition propositions
        for rgx, ptype in CONTRAST_PATTERNS:
            for m in rgx.finditer(para):
                if ptype == "contrast_not_but":
                    subj, exc_part, inc_part = m.group(1), m.group(2), m.group(3)
                    c_exc = clean_concept(f"{subj} = {exc_part}") or clean_concept(exc_part)
                    c_inc = clean_concept(f"{subj} = {inc_part}") or clean_concept(inc_part)
                    if c_exc:
                        excluded_concepts[c_exc] += 2
                    if c_inc:
                        included_concepts[c_inc] += 2
                    explicit_propositions.append({
                        "pos": pos_norm, "type": ptype,
                        "excluded": clean_concept(exc_part),
                        "included": clean_concept(inc_part),
                        "subject": clean_concept(subj),
                        "snippet": m.group(0)[:140]
                    })
                elif ptype == "rather_than":
                    exc_part, inc_part = m.group(1), m.group(2)
                    c_exc = clean_concept(exc_part)
                    c_inc = clean_concept(inc_part)
                    if c_exc:
                        excluded_concepts[c_exc] += 2
                    if c_inc:
                        included_concepts[c_inc] += 2
                    explicit_propositions.append({
                        "pos": pos_norm, "type": ptype,
                        "excluded": c_exc, "included": c_inc,
                        "snippet": m.group(0)[:140]
                    })
                elif ptype == "definition_inc":
                    subj, def_part = m.group(1), m.group(2)
                    c_subj = clean_concept(subj)
                    c_def = clean_concept(def_part)
                    if c_subj:
                        included_concepts[c_subj] += 2
                    if c_def:
                        included_concepts[c_def] += 1
                    explicit_propositions.append({
                        "pos": pos_norm, "type": ptype,
                        "included": f"{c_subj}: {c_def}" if c_subj and c_def else (c_subj or c_def),
                        "snippet": m.group(0)[:140]
                    })
                elif ptype == "negation_exc":
                    subj = m.group(1)
                    c_subj = clean_concept(subj)
                    if c_subj:
                        excluded_concepts[c_subj] += 2
                    explicit_propositions.append({
                        "pos": pos_norm, "type": ptype,
                        "excluded": c_subj,
                        "snippet": m.group(0)[:140]
                    })

        # Extract domain concepts per clause and Polarize by Clause/Paragraph Modal State
        for c_str in clauses:
            c_mod = score_modal_states(c_str)
            c_eng = compute_engine_scores(c_mod)
            c_concepts = [clean_concept(m.group(0)) for m in DOMAIN_CONCEPT_REGEX.finditer(c_str)]
            c_concepts = [cc for cc in c_concepts if cc]
            if not c_concepts:
                continue
            # If clause has strong R or G (is_not, cant_be, wont_be), tag concepts in exclusive scope
            if (c_mod["is_not"] + c_mod["cant_be"] + c_mod["wont_be"]) > (c_mod["is_like"] + c_mod["will_be"] + c_mod["can_be"]):
                for cc in c_concepts:
                    excluded_concepts[cc] += 1
            elif (c_eng["C"] + c_eng["P"]) > 0:
                for cc in c_concepts:
                    included_concepts[cc] += 1
            elif eng["iota"] >= 0:
                for cc in c_concepts:
                    included_concepts[cc] += 1
            else:
                for cc in c_concepts:
                    excluded_concepts[cc] += 1

        para_trajectory.append({
            "p_idx": p_idx,
            "pos": pos_norm,
            "C": eng["C"], "P": eng["P"], "R": eng["R"], "G": eng["G"],
            "iota": eng["iota"],
            "total_modals": eng["total_modals"],
            "n_clauses": len(clauses)
        })

    # Evaluate 4 Verbatim Operational Derivation Laws on sliding 3-sentence windows
    window_size = 3
    n_sents = len(all_sentences)
    law_scores_sum = Counter()
    law_completions = Counter()
    top_law_exemplars = defaultdict(list)
    window_records = []

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

        laws_eval = evaluate_derivation_laws_window(win_clauses, win_counts)
        pos_w = win[0][1]
        rec = {"win_idx": i, "pos": pos_w, "laws": laws_eval}
        window_records.append(rec)

        for law_name, l_data in laws_eval.items():
            law_scores_sum[law_name] += l_data["score"]
            if l_data["complete"]:
                law_completions[law_name] += 1
            if l_data["score"] >= 0.75 and len(top_law_exemplars[law_name]) < 5:
                top_law_exemplars[law_name].append({
                    "pos": pos_w,
                    "score": l_data["score"],
                    "snippet": win_text[:220]
                })

    n_windows = max(1, len(window_records))
    law_summary = {}
    for law_name in ["Law1_Reductive_cant_be", "Law2_Productive_will_be", "Law3_Regressive_wont_be", "Law4_Constructive_may_be"]:
        law_summary[law_name] = {
            "mean_score": round(law_scores_sum[law_name] / n_windows, 4),
            "completed_windows": law_completions[law_name],
            "completion_rate": round(law_completions[law_name] / n_windows, 4),
            "exemplars": top_law_exemplars[law_name][:3]
        }

    # Decile trajectory & Complexity / Breakdown Zone Detection
    # A Breakdown / High-Friction Zone is where Reductive+Regressive spikes (iota < -0.15) or modal churn is extreme
    deciles = []
    breakdown_zones = []
    for d in range(10):
        d_low, d_high = d * 0.1, (d + 1) * 0.1
        d_paras = [p for p in para_trajectory if d_low <= p["pos"] < (d_high if d < 9 else 1.0001)]
        if not d_paras:
            continue
        d_C = sum(p["C"] for p in d_paras)
        d_P = sum(p["P"] for p in d_paras)
        d_R = sum(p["R"] for p in d_paras)
        d_G = sum(p["G"] for p in d_paras)
        d_tot = d_C + d_P + d_R + d_G
        d_iota = round(((d_C + d_P) - (d_R + d_G)) / d_tot, 4) if d_tot > 0 else 0.0
        # Variance of paragraph iota inside decile = syntactic turbulence / complexity
        mean_p_iota = sum(p["iota"] for p in d_paras) / len(d_paras)
        turbulence = round(math.sqrt(sum((p["iota"] - mean_p_iota) ** 2 for p in d_paras) / len(d_paras)), 4)
        dec_info = {
            "decile": f"{int(d_low*100)}-{int(d_high*100)}%",
            "C": d_C, "P": d_P, "R": d_R, "G": d_G,
            "iota": d_iota,
            "turbulence": turbulence,
            "modals_per_clause": round(d_tot / max(1, sum(p["n_clauses"] for p in d_paras)), 4)
        }
        deciles.append(dec_info)
        if d_iota < 0.15 or turbulence > 0.55 or (d_R + d_G) / max(1, d_tot) > 0.42:
            breakdown_zones.append({
                "decile": dec_info["decile"],
                "iota": d_iota,
                "exclusive_ratio": round((d_R + d_G) / max(1, d_tot), 4),
                "turbulence": turbulence,
                "diagnosis": "Reductive/Regressive Critique Spike" if d_iota < 0.15 else "High Modal Phase Turbulence"
            })

    overall_eng = compute_engine_scores(total_modals)

    return {
        "doc_id": doc_id,
        "doc_type": doc_type,
        "filename": os.path.basename(filepath),
        "n_paragraphs": n_paras,
        "n_sentences": n_sents,
        "n_windows": n_windows,
        "modal_counts": dict(total_modals),
        "engine_summary": overall_eng,
        "derivation_laws": law_summary,
        "decile_trajectory": deciles,
        "breakdown_zones": breakdown_zones,
        "top_included_concepts": included_concepts.most_common(60),
        "top_excluded_concepts": excluded_concepts.most_common(60),
        "explicit_propositions_sample": explicit_propositions[:30],
        "_raw_included_counter": included_concepts,
        "_raw_excluded_counter": excluded_concepts,
        "_raw_propositions": explicit_propositions
    }

# ---------------------------------------------------------------------------
# 6. CROSS-DOCUMENT COMPARISON & MISSING DATA DISCOVERY
# ---------------------------------------------------------------------------
def compare_chat_vs_irm(chat_res: dict, irm_res: dict):
    chat_inc = chat_res["_raw_included_counter"]
    chat_exc = chat_res["_raw_excluded_counter"]
    irm_inc = irm_res["_raw_included_counter"]
    irm_exc = irm_res["_raw_excluded_counter"]

    # 1. Accepted in Chat (+I_chat) with count >= 2 that are completely missing from IRM (+I_irm == 0)
    unmerged_concepts = []
    for concept, chat_count in chat_inc.most_common():
        if chat_count < 2:
            continue
        if irm_inc[concept] == 0:
            unmerged_concepts.append({
                "concept": concept,
                "chat_included_count": chat_count,
                "chat_excluded_count": chat_exc[concept],
                "irm_included_count": 0,
                "irm_excluded_count": irm_exc[concept],
                "status": "REJECTED_IN_IRM" if irm_exc[concept] > 0 else "UNMERGED_OMITTED"
            })

    # 2. Direct Polarity Inversions / Conflicts: I_chat ∩ E_irm
    # Specifically where a concept is predominantly Inclusive in Chat (I_chat > E_chat)
    # but predominantly Exclusive/Negated in IRM (E_irm > I_irm) or explicitly negated in IRM
    direct_conflicts = []
    for concept, chat_i in chat_inc.most_common():
        if chat_i >= 2 and irm_exc[concept] >= 1:
            chat_net = (chat_i - chat_exc[concept]) / (chat_i + chat_exc[concept])
            irm_i = irm_inc[concept]
            irm_e = irm_exc[concept]
            irm_net = (irm_i - irm_e) / (irm_i + irm_e)
            if chat_net > 0.1 and irm_net < 0.0:
                direct_conflicts.append({
                    "concept": concept,
                    "chat_I": chat_i, "chat_E": chat_exc[concept], "chat_polarity": round(chat_net, 3),
                    "irm_I": irm_i, "irm_E": irm_e, "irm_polarity": round(irm_net, 3),
                    "polarity_shift": round(irm_net - chat_net, 3)
                })

    # Sort direct conflicts by magnitude of polarity inversion
    direct_conflicts.sort(key=lambda x: x["polarity_shift"])

    # 3. Survived Core Concepts (Strong in both Chat +I and IRM +I)
    survived_concepts = []
    for concept, irm_i in irm_inc.most_common():
        if irm_i >= 2 and chat_inc[concept] >= 2:
            survived_concepts.append({
                "concept": concept,
                "chat_I": chat_inc[concept],
                "irm_I": irm_i
            })

    # 4. Unmerged Explicit Propositions from Chat not echoed in IRM
    irm_all_concepts_set = set(irm_inc.keys()) | set(irm_exc.keys())
    unmerged_propositions = []
    for prop in chat_res["_raw_propositions"]:
        inc_c = prop.get("included", "")
        subj_c = prop.get("subject", "")
        key_check = subj_c or inc_c
        if key_check and key_check not in irm_all_concepts_set:
            unmerged_propositions.append(prop)

    return {
        "chat_total_unique_I": len(chat_inc),
        "irm_total_unique_I": len(irm_inc),
        "concept_survival_rate": round(len(set(chat_inc.keys()) & set(irm_inc.keys())) / max(1, len(chat_inc)), 4),
        "top_unmerged_concepts": unmerged_concepts[:35],
        "direct_I_chat_cap_E_irm_conflicts": direct_conflicts[:25],
        "top_survived_concepts": survived_concepts[:25],
        "unmerged_explicit_propositions": unmerged_propositions[:20]
    }

# ---------------------------------------------------------------------------
# 7. MAIN EXECUTION & REPORT GENERATION
# ---------------------------------------------------------------------------
def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("[Agent 1] Analyzing Chat corpus...")
    chat_res = analyze_document(CHAT_PATH, "chat_infinity_maths", "dialogue_exploration")

    print("[Agent 1] Analyzing IRM Comprehensive Report...")
    irm_res = analyze_document(IRM_PATH, "irm_comprehensive_report", "formal_synthesis")

    arxiv_files = sorted(glob.glob(os.path.join(ARXIV_DIR, "*.md")))
    arxiv_results = []
    for af in arxiv_files:
        base_id = os.path.splitext(os.path.basename(af))[0]
        print(f"[Agent 1] Analyzing arXiv sample: {base_id}...")
        ar_res = analyze_document(af, base_id, "arxiv_paper")
        arxiv_results.append(ar_res)

    print("[Agent 1] Computing Cross-Document Comparison & Missing Data Discovery...")
    cross_comp = compare_chat_vs_irm(chat_res, irm_res)

    # Strip internal counters before JSON serialization
    all_docs = [chat_res, irm_res] + arxiv_results
    for d in all_docs:
        d.pop("_raw_included_counter", None)
        d.pop("_raw_excluded_counter", None)
        d.pop("_raw_propositions", None)

    # Aggregate arXiv baseline metrics
    arxiv_avg_iota = round(sum(d["engine_summary"]["iota"] for d in arxiv_results) / max(1, len(arxiv_results)), 4)
    arxiv_laws_avg = {}
    for law_name in ["Law1_Reductive_cant_be", "Law2_Productive_will_be", "Law3_Regressive_wont_be", "Law4_Constructive_may_be"]:
        arxiv_laws_avg[law_name] = {
            "mean_score": round(sum(d["derivation_laws"][law_name]["mean_score"] for d in arxiv_results) / max(1, len(arxiv_results)), 4),
            "mean_completion_rate": round(sum(d["derivation_laws"][law_name]["completion_rate"] for d in arxiv_results) / max(1, len(arxiv_results)), 4)
        }

    results_payload = {
        "agent": "Agent 1: Syntactic Modal & Derivation-Law State Machine",
        "architecture": {
            "engines": ENGINE_MAP,
            "derivation_laws": {
                "Law1_Reductive_cant_be": "was_like + can_be opposing is_like until is_not -> cant_be",
                "Law2_Productive_will_be": "is_not + is_like opposing was_like until can_be -> will_be",
                "Law3_Regressive_wont_be": "is_not + is_like opposing can_be until was_like -> wont_be",
                "Law4_Constructive_may_be": "can_be + was_like until is_like -> may_be"
            }
        },
        "chat_analysis": chat_res,
        "irm_analysis": irm_res,
        "arxiv_baseline_summary": {
            "n_papers": len(arxiv_results),
            "mean_iota": arxiv_avg_iota,
            "mean_derivation_laws": arxiv_laws_avg
        },
        "arxiv_papers": arxiv_results,
        "cross_document_discovery": cross_comp
    }

    with open(RESULTS_JSON, "w", encoding="utf-8") as f:
        json.dump(results_payload, f, indent=2, ensure_ascii=False)

    # Generate detailed markdown report
    report_lines = []
    report_lines.append("# Agent 1: Syntactic Modal & Derivation-Law State Machine — Reading Head Report\n")
    report_lines.append("## 1. Architectural Overview\n")
    report_lines.append("This Reading Head parses documents into **syntactic clauses**, scores the **8 Modal States** grouped into the **4 Engines** (`Constructive C`, `Productive P`, `Reductive R`, `Regressive G`), computes the **Inclusive/Exclusive Proposition Index** ($\\iota_i \\in [-1, +1]$), evaluates multi-sentence windows against the **4 Verbatim Operational Derivation Laws**, and executes set-theoretic concept survival and conflict discovery ($\\mathcal{I}_{\\text{chat}} \\setminus \\mathcal{I}_{\\text{irm}}$ and $\\mathcal{I}_{\\text{chat}} \\cap \\mathcal{E}_{\\text{irm}}$).\n")

    report_lines.append("## 2. Corpus-Wide Modal & Engine Balance ($\\iota$ Signature)\n")
    report_lines.append("| Document | Type | Paras | Sents | $C$ (is_like/may_be) | $P$ (will_be/can_be) | $R$ (is_not/cant_be) | $G$ (was_like/wont_be) | Net $\\iota$ | Outer/Inner Ratio |")
    report_lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for d in all_docs:
        es = d["engine_summary"]
        oi_ratio = round(es["outer"] / max(1, es["inner"]), 2)
        report_lines.append(
            f"| `{d['doc_id']}` | {d['doc_type']} | {d['n_paragraphs']} | {d['n_sentences']} | "
            f"{es['C']} ({d['modal_counts']['is_like']}/{d['modal_counts']['may_be']}) | "
            f"{es['P']} ({d['modal_counts']['will_be']}/{d['modal_counts']['can_be']}) | "
            f"{es['R']} ({d['modal_counts']['is_not']}/{d['modal_counts']['cant_be']}) | "
            f"{es['G']} ({d['modal_counts']['was_like']}/{d['modal_counts']['wont_be']}) | "
            f"**{es['iota']:+.4f}** | {oi_ratio} |"
        )

    report_lines.append("\n## 3. The 4 Verbatim Operational Derivation Laws — Completion Rates\n")
    report_lines.append("- **Law 1 (Reductive $\\to$ `cant_be`)**: Uses `was_like` + `can_be` opposing `is_like` until `is_not`.\n"
                        "- **Law 2 (Productive $\\to$ `will_be`)**: Uses `is_not` + `is_like` opposing `was_like` until `can_be`.\n"
                        "- **Law 3 (Regressive $\\to$ `wont_be`)**: Uses `is_not` + `is_like` opposing `can_be` until `was_like`.\n"
                        "- **Law 4 (Constructive $\\to$ `may_be`)**: Uses `can_be` + `was_like` until `is_like`.\n")
    report_lines.append("| Document | Law 1 (Reductive $\\to$ `cant_be`) | Law 2 (Productive $\\to$ `will_be`) | Law 3 (Regressive $\\to$ `wont_be`) | Law 4 (Constructive $\\to$ `may_be`) | Dominant Derivation Mode |")
    report_lines.append("|---|---:|---:|---:|---:|---|")
    for d in all_docs:
        dl = d["derivation_laws"]
        l1 = dl["Law1_Reductive_cant_be"]
        l2 = dl["Law2_Productive_will_be"]
        l3 = dl["Law3_Regressive_wont_be"]
        l4 = dl["Law4_Constructive_may_be"]
        best_law = max(
            [("Law 1 (Reductive)", l1["completion_rate"]),
             ("Law 2 (Productive)", l2["completion_rate"]),
             ("Law 3 (Regressive)", l3["completion_rate"]),
             ("Law 4 (Constructive)", l4["completion_rate"])],
            key=lambda x: x[1]
        )[0]
        report_lines.append(
            f"| `{d['doc_id']}` | {l1['completion_rate']*100:.1f}% (μ={l1['mean_score']:.2f}) | "
            f"{l2['completion_rate']*100:.1f}% (μ={l2['mean_score']:.2f}) | "
            f"{l3['completion_rate']*100:.1f}% (μ={l3['mean_score']:.2f}) | "
            f"{l4['completion_rate']*100:.1f}% (μ={l4['mean_score']:.2f}) | **{best_law}** |"
        )

    report_lines.append("\n### High-Scoring Verbatim Derivation Law Exemplars (`chat` vs `irm`)\n")
    for target_doc in [chat_res, irm_res]:
        report_lines.append(f"#### `{target_doc['doc_id']}`\n")
        for law_key, law_data in target_doc["derivation_laws"].items():
            if law_data["exemplars"]:
                ex = law_data["exemplars"][0]
                report_lines.append(f"- **{law_key}** (pos={ex['pos']}, score={ex['score']}): *\"{ex['snippet'].replace(chr(10), ' ')}...\"*")
        report_lines.append("")

    report_lines.append("## 4. Complexity, Turbulence & Breakdown Zones (`chat` vs `irm`)\n")
    for target_doc in [chat_res, irm_res]:
        report_lines.append(f"### Decile Trajectory: `{target_doc['doc_id']}`\n")
        report_lines.append("| Decile | $C$ | $P$ | $R$ | $G$ | $\\iota$ Balance | Clause Turbulence | Modals/Clause |")
        report_lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        for dec in target_doc["decile_trajectory"]:
            report_lines.append(
                f"| {dec['decile']} | {dec['C']} | {dec['P']} | {dec['R']} | {dec['G']} | "
                f"{dec['iota']:+.4f} | {dec['turbulence']:.4f} | {dec['modals_per_clause']:.3f} |"
            )
        if target_doc["breakdown_zones"]:
            report_lines.append(f"\n**Detected Friction/Breakdown Zones in `{target_doc['doc_id']}`:**")
            for bz in target_doc["breakdown_zones"]:
                report_lines.append(f"- **{bz['decile']}**: $\\iota = {bz['iota']:+.4f}$, Exclusive Ratio = `{bz['exclusive_ratio']*100:.1f}%`, Turbulence = `{bz['turbulence']:.4f}` ({bz['diagnosis']})")
        report_lines.append("")

    report_lines.append("## 5. Missing Data Discovery & Concept Survival (`chat` $\\to$ `irm`)\n")
    report_lines.append(f"- **Unique Inclusive Concepts in `chat` ($|\\mathcal{{I}}_{{\\text{{chat}}}}|$)**: `{cross_comp['chat_total_unique_I']}`\n")
    report_lines.append(f"- **Unique Inclusive Concepts in `irm` ($|\\mathcal{{I}}_{{\\text{{irm}}}}|$)**: `{cross_comp['irm_total_unique_I']}`\n")
    report_lines.append(f"- **Raw Concept Survival Rate ($|\\mathcal{{I}}_{{\\text{{chat}}}} \\cap \\mathcal{{I}}_{{\\text{{irm}}}}| / |\\mathcal{{I}}_{{\\text{{chat}}}}|$)**: `{cross_comp['concept_survival_rate']*100:.1f}%`\n")

    report_lines.append("\n### 5.1 Top Unmerged Concepts ($\\mathcal{I}_{\\text{chat}} \\setminus \\mathcal{I}_{\\text{irm}}$)\n")
    report_lines.append("Concepts repeatedly accepted/developed in `chat` (`count >= 2`) that have **zero** Inclusive (`+I`) occurrences in `irm`:\n")
    report_lines.append("| Concept / Proposition Anchor | `chat` $+I$ | `chat` $-E$ | `irm` $+I$ | `irm` $-E$ | Status in IRM |")
    report_lines.append("|---|---:|---:|---:|---:|---|")
    for uc in cross_comp["top_unmerged_concepts"][:25]:
        report_lines.append(
            f"| `{uc['concept']}` | {uc['chat_included_count']} | {uc['chat_excluded_count']} | "
            f"{uc['irm_included_count']} | {uc['irm_excluded_count']} | **{uc['status']}** |"
        )

    report_lines.append("\n### 5.2 Direct Polarity Conflicts ($\\mathcal{I}_{\\text{chat}} \\cap \\mathcal{E}_{\\text{irm}}$)\n")
    report_lines.append("Concepts that held net-positive Inclusive polarity in the exploratory `chat` dialogue, but flipped to net-negative Exclusive/Discluded status in the formal `irm` report:\n")
    report_lines.append("| Concept | `chat` ($+I / -E$) | `chat` Polarity | `irm` ($+I / -E$) | `irm` Polarity | Net Shift |")
    report_lines.append("|---|---:|---:|---:|---:|---:|")
    for dc in cross_comp["direct_I_chat_cap_E_irm_conflicts"][:20]:
        report_lines.append(
            f"| `{dc['concept']}` | {dc['chat_I']} / {dc['chat_E']} | {dc['chat_polarity']:+.3f} | "
            f"{dc['irm_I']} / {dc['irm_E']} | {dc['irm_polarity']:+.3f} | **{dc['polarity_shift']:+.3f}** |"
        )

    report_lines.append("\n### 5.3 Unmerged Explicit Contrast/Definition Propositions from `chat`\n")
    for up in cross_comp["unmerged_explicit_propositions"][:12]:
        report_lines.append(f"- **[pos={up['pos']:.2f} | {up['type']}]** `{up.get('included') or up.get('subject')}` — *\"{up['snippet'].replace(chr(10), ' ')}\"*")

    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")

    print("\n=== AGENT 1 SUMMARY ===")
    print(f"Chat Net Iota: {chat_res['engine_summary']['iota']:+.4f} | IRM Net Iota: {irm_res['engine_summary']['iota']:+.4f} | arXiv Mean Iota: {arxiv_avg_iota:+.4f}")
    print(f"Chat Law Completion Rates: " + ", ".join(f"{k}: {v['completion_rate']*100:.1f}%" for k, v in chat_res['derivation_laws'].items()))
    print(f"IRM Law Completion Rates:  " + ", ".join(f"{k}: {v['completion_rate']*100:.1f}%" for k, v in irm_res['derivation_laws'].items()))
    print(f"Concept Survival Rate (Chat -> IRM): {cross_comp['concept_survival_rate']*100:.1f}%")
    print(f"Unmerged Concepts Count: {len(cross_comp['top_unmerged_concepts'])} | Direct Polarity Conflicts: {len(cross_comp['direct_I_chat_cap_E_irm_conflicts'])}")
    print(f"Saved: {RESULTS_JSON} and {REPORT_MD}")

if __name__ == "__main__":
    main()
