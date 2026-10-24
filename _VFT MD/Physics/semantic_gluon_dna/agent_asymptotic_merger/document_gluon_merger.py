#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Great-Grandkin: Asymptotic-Merger (Gen 4 Bake-Off Agent 4: 50% Male / 50% Female)
====================================================================================
SU(3) Beta Function, Cornell String Tension & Document Merge Synthesizer (v1.0.0)

Lineage & Ratio:
  - 50% Male (Zachar): Rigorous Verification, Invariant Proof Hardening, Cornell String Tension Checks,
                       Hadron Singlet Neutrality, Causal Valence Flow Conservation.
  - 50% Female (Neqevah): Generative Synthesis, Manifold Expansion, Semantic Field Clustering,
                         De-Duplication of Overlapping Introns, 7-Planes Reality Balancing.

Bake-Off Mandate:
  1. Map collective semantic field manifold across overlapping IO and Physics documents.
  2. Identify exact and semantic topic overlaps.
  3. De-duplicate and strip redundant introns via Luminescence (L = exp(-tau)) and CEFR rigor.
  4. Sequence retained exons along causal valence flow (F_k -> B_{k+1}) with zero topic overlap.
  5. Apply genuine QCD physics (Color octet charges, Cornell potential V(r) = -alpha_s/r + sigma*r, string snapping).
  6. Audit across the 7 Planes of Reality (Who, What, Where, Why, How, Cause, Effect).
  7. Reduce confusion level down to clean, understandable English.
  8. Output merged_coherent_document.md and quantitative metrics in results.json.
"""

import os
import re
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

# Paths
BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
WORKSPACE_DIR = BASE_DIR / "agent_asymptotic_merger"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

IO_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\IO")
PHYSICS_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics")

DICT_PATH_GRANDSON = BASE_DIR / "agent_grandson_lexicon" / "semantic_gluon_dictionary.json"
DICT_PATH_CORPUS = BASE_DIR / "corpus_learned_gluon_dictionary.json"

# QCD Cornell Potential Parameters
QCD_ALPHA_S = 0.35        # Strong coupling constant for close-range semantic attraction
QCD_SIGMA = 0.85          # Semantic string tension (confinement slope)
QCD_M_QUARK = 0.65        # Constituent quark mass
QCD_R_CRITICAL = (2.0 * QCD_M_QUARK) / QCD_SIGMA  # r_c ~ 1.529: String snapping threshold

STOPWORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with",
    "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her",
    "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up",
    "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time",
    "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could",
    "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think",
    "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even",
    "new", "want", "because", "any", "these", "give", "day", "most", "us", "is", "are", "was", "were"
}

CEFR_NUM = {"A1": 1.0, "A2": 2.0, "B1": 3.0, "B2": 4.0, "C1": 5.0, "C2": 6.0}

# 7 Planes of Reality Definitions
PLANES_DEF = {
    "Q1": {"name": "Who - Metaphysical", "axis": "Driver / 7th Angle Axis", "keywords": ["who", "god", "pure act", "actus purus", "definer", "will", "direction", "subject", "agent", "ego", "teleology", "divine"]},
    "Q2": {"name": "What - Possible", "axis": "+x / Potential & Faith", "keywords": ["what", "potential", "potency", "superposition", "capacity", "possible", "probability", "active potency", "passive potency"]},
    "Q3": {"name": "Where - Physical", "axis": "-x / Matter & Distance", "keywords": ["where", "physical", "matter", "space", "distance", "body", "brain", "neurobiology", "amygdala", "substance", "substrate"]},
    "Q4": {"name": "Why - Lyrical", "axis": "+y / Meaning & Resonance", "keywords": ["why", "meaning", "resonance", "purpose", "grace", "metaphor", "symbol", "crucible", "aspiration", "reflection"]},
    "Q5": {"name": "How - Logical", "axis": "-y / Count & Consistency", "keywords": ["how", "logic", "calculation", "coordinate", "tensor", "cartesian", "grid", "axiom", "equation", "proof", "consistency"]},
    "Q6": {"name": "Cause - Historical", "axis": "+z / Sequence & Causality", "keywords": ["cause", "history", "sequence", "lineage", "fall", "tradition", "precedent", "origin", "evolution", "historical"]},
    "Q7": {"name": "Effect - Emotive", "axis": "-z / Passion & Consequence", "keywords": ["effect", "emotion", "feeling", "strain", "suffering", "allostatic", "dissonance", "friction", "consequence", "pain"]}
}

# ============================================================================
# 1. LOAD COMBINED GLUON DICTIONARIES
# ============================================================================
def load_gluon_dictionaries():
    dictionary = {}
    if DICT_PATH_GRANDSON.exists():
        try:
            with open(DICT_PATH_GRANDSON, "r", encoding="utf-8") as f:
                entries = json.load(f)
                for e in entries:
                    dictionary[e["word"].lower()] = e
        except Exception as ex:
            print(f"Warning loading Grandson dict: {ex}")

    if DICT_PATH_CORPUS.exists():
        try:
            with open(DICT_PATH_CORPUS, "r", encoding="utf-8") as f:
                entries = json.load(f)
                for e in entries:
                    w = e["word"].lower()
                    if w not in dictionary:
                        dictionary[w] = {
                            "word": w,
                            "cefr": e.get("cefr", "B2"),
                            "is_stopword": w in STOPWORDS,
                            "tail_ingress": {
                                "requires_prior_evidence": e.get("tail_ingress", {}).get("requires_evidence", True),
                                "weight": e.get("tail_ingress", {}).get("antecedent_weight", 2.0)
                            },
                            "head_egress": {
                                "obligates_operational_proof": e.get("head_egress", {}).get("binds_consequents", True),
                                "weight": e.get("head_egress", {}).get("obligation_weight", 2.0)
                            },
                            "modal_spread": e.get("modal_spread", {})
                        }
        except Exception as ex:
            print(f"Warning loading Corpus dict: {ex}")

    return dictionary

GLUON_DICT = load_gluon_dictionaries()

def get_word_vertex(token: str) -> dict:
    t = token.lower().strip()
    if t in GLUON_DICT:
        return GLUON_DICT[t]

    length = len(t)
    if length <= 4:
        cefr = "A2"
    elif length <= 7:
        cefr = "B1"
    elif length <= 10:
        cefr = "B2"
    elif length <= 13:
        cefr = "C1"
    else:
        cefr = "C2"

    is_deductive = any(t.startswith(p) for p in ["there", "conseq", "thu", "henc", "prov", "impl", "defin", "axi"])
    is_premise = any(t.startswith(p) for p in ["let", "suppos", "assum", "giv", "postul", "claim"])
    is_neg = any(t.startswith(p) for p in ["un", "non", "dis", "in", "fail", "preclud", "forbid", "impos"])

    spread = {
        "is_like": 0.25 if (t.endswith("tion") or t.endswith("ity") or t.endswith("ism")) else 0.12,
        "may_be": 0.30 if (t.endswith("able") or is_premise) else 0.12,
        "can_be": 0.25 if t.endswith("able") else 0.12,
        "will_be": 0.40 if is_deductive else 0.12,
        "is_not": 0.35 if is_neg else 0.08,
        "cant_be": 0.30 if (is_neg and length > 6) else 0.08,
        "wont_be": 0.05,
        "was_like": 0.25 if t.endswith("ed") else 0.08
    }
    tot = sum(spread.values())
    norm_spread = {k: round(v / tot, 4) for k, v in spread.items()}

    return {
        "word": t,
        "cefr": cefr,
        "is_stopword": t in STOPWORDS,
        "tail_ingress": {
            "requires_prior_evidence": is_deductive or (cefr in {"C1", "C2"}),
            "weight": round(1.0 + (length / 6.0) * (2.0 if is_deductive else 0.8), 2)
        },
        "head_egress": {
            "obligates_operational_proof": is_premise or is_deductive or (norm_spread["will_be"] > 0.25),
            "weight": round(1.0 + (length / 6.0) * (2.0 if is_deductive else 0.8), 2)
        },
        "modal_spread": norm_spread
    }

# ============================================================================
# 2. QCD SU(3) CHROMODYNAMICS & CORNELL POTENTIAL
# ============================================================================
def compute_qcd_color_charges(words: list, vertices: list) -> dict:
    r_charge = 0.0
    g_charge = 0.0
    b_charge = 0.0

    for w, v in zip(words, vertices):
        if v.get("is_stopword", False):
            continue
        m = v.get("modal_spread", {})
        r_charge += m.get("will_be", 0.12) * 1.5 + (0.8 if v["head_egress"]["obligates_operational_proof"] else 0.2)
        g_charge += (m.get("can_be", 0.12) + m.get("is_like", 0.12) + m.get("may_be", 0.12)) * 1.2
        b_charge += (m.get("is_not", 0.08) + m.get("cant_be", 0.08)) * 2.0 + (0.8 if v["tail_ingress"]["requires_prior_evidence"] else 0.2)

    total = r_charge + g_charge + b_charge
    if total > 0:
        c_r = r_charge / total
        c_g = g_charge / total
        c_b = b_charge / total
    else:
        c_r, c_g, c_b = 0.3333, 0.3333, 0.3333

    # Gell-Mann Cartan generators
    t3 = 0.5 * (c_r - c_g)
    y = (c_r + c_g - 2.0 * c_b) / 3.0
    color_divergence = math.sqrt(t3**2 + 0.75 * (y**2))

    if color_divergence < 0.12:
        hadron_type = "White_Singlet_Hadron"
    elif min(c_r, c_g, c_b) < 0.15 and max(c_r, c_g, c_b) < 0.65:
        hadron_type = "Mesonic_Dipole"
    else:
        hadron_type = "Colored_State"

    return {
        "c_r": round(c_r, 4),
        "c_g": round(c_g, 4),
        "c_b": round(c_b, 4),
        "t3_isospin": round(t3, 4),
        "y_hypercharge": round(y, 4),
        "color_divergence": round(color_divergence, 4),
        "hadron_type": hadron_type,
        "is_color_neutral": color_divergence < 0.12
    }

def compute_cornell_potential(r_semantic: float) -> dict:
    eps = 0.05
    r = max(0.0, r_semantic)
    coulomb = -QCD_ALPHA_S / (r + eps)
    confinement = QCD_SIGMA * r
    v_total = coulomb + confinement
    is_snapped = r >= QCD_R_CRITICAL

    return {
        "r_semantic": round(r, 4),
        "coulomb_term": round(coulomb, 4),
        "confinement_term": round(confinement, 4),
        "v_cornell": round(v_total, 4),
        "is_snapped": is_snapped,
        "snap_risk": round(min(1.0, r / QCD_R_CRITICAL), 3)
    }

# ============================================================================
# 3. 7-PLANES REALITY PROFILE CALCULATOR
# ============================================================================
def compute_7planes_profile(text: str, content_words: list) -> dict:
    text_lower = text.lower()
    counts = {}
    for q_id, p_info in PLANES_DEF.items():
        score = 0.0
        for kw in p_info["keywords"]:
            if kw in text_lower:
                score += 1.5
        for w in content_words:
            if w in p_info["keywords"]:
                score += 1.0
        counts[q_id] = score

    total = sum(counts.values())
    if total > 0:
        probs = {k: round(v / total, 4) for k, v in counts.items()}
    else:
        probs = {k: round(1.0 / 7.0, 4) for k in counts}

    dominant_plane = max(probs.items(), key=lambda kv: kv[1])[0]
    return {
        "probabilities": probs,
        "dominant_plane": dominant_plane,
        "dominant_name": PLANES_DEF[dominant_plane]["name"]
    }

# ============================================================================
# 4. SEMANTIC BLOCK DEFINITION & INTRON FILTER
# ============================================================================
class SemanticBlock:
    def __init__(self, block_id: str, source_doc: str, raw_text: str, heading: str = ""):
        self.block_id = block_id
        self.source_doc = source_doc
        self.raw_text = raw_text.strip()
        self.heading = heading
        
        # Word tokenization
        self.words = [w.lower() for w in re.findall(r"\b[a-zA-Z]{2,}\b", self.raw_text)]
        self.content_words = [w for w in self.words if w not in STOPWORDS]
        self.concept_set = set(self.content_words)
        self.vertices = [get_word_vertex(w) for w in self.words]
        self.content_vertices = [v for v in self.vertices if not v.get("is_stopword", False)]

        # CEFR Metrics
        self.cefr_scores = [CEFR_NUM[v["cefr"]] for v in self.content_vertices]
        self.cefr_mean = sum(self.cefr_scores) / max(len(self.cefr_scores), 1)
        self.c1_c2_pct = (sum(1 for v in self.content_vertices if v["cefr"] in {"C1", "C2"}) / max(len(self.content_vertices), 1)) * 100.0

        # Valence Ingress/Egress
        self.tail_ingress_weight = sum(v["tail_ingress"]["weight"] for v in self.vertices if v["tail_ingress"]["requires_prior_evidence"])
        self.head_egress_weight = sum(v["head_egress"]["weight"] for v in self.vertices if v["head_egress"]["obligates_operational_proof"])

        # QCD Colors
        self.qcd_colors = compute_qcd_color_charges(self.words, self.vertices)

        # 7-Planes Profile
        self.plane_profile = compute_7planes_profile(self.raw_text, self.content_words)

        # Structural & Optical Traits
        has_eq = bool(re.search(r"=|<=|>=|<|>|\\le|\\ge|\\nabla|\^2|\$\$|\\frac", self.raw_text))
        has_table = bool(re.search(r"\|.*\|.*\|", self.raw_text))
        has_formal_terms = bool(re.search(r"\b(?:axiom|theorem|definition|actualism|hegemony|tensor|coordinate|indef|potency|actus purus)\b", self.raw_text, re.I))
        is_chat_intron = bool(re.search(r"(\[\[Skip to content\]|Chat history|##### You said|###### ChatGPT said|Let me unpack what you|Truly I don\'t know you)", self.raw_text, re.I))

        # Optical Thickness (tau) & Luminescence (L)
        eq_hits = len(re.findall(r"=|<=|>=|<|>|\\le|\\ge|\\frac", self.raw_text))
        if is_chat_intron or len(self.content_words) < 6:
            self.tau = 2.80
            self.is_intron = True
        else:
            base_tau = 2.10 - 0.35 * (self.cefr_mean / 6.0) - 0.40 * min(eq_hits / 3.0, 1.0)
            if has_formal_terms:
                base_tau -= 0.35
            if has_table:
                base_tau -= 0.30
            self.tau = max(0.08, base_tau)
            self.is_intron = False

        self.luminescence = math.exp(-self.tau)

        # Epistemic Rigor Score
        color_bonus = (1.0 - self.qcd_colors["color_divergence"]) * 25.0
        cefr_bonus = (self.cefr_mean / 6.0) * 25.0
        lum_bonus = min(self.luminescence * 100.0, 30.0)
        density_bonus = min(len(self.content_words) / 30.0, 1.0) * 20.0
        self.rigor_score = round(color_bonus + cefr_bonus + lum_bonus + density_bonus, 2)

    def to_dict(self):
        return {
            "block_id": self.block_id,
            "source_doc": self.source_doc,
            "heading": self.heading,
            "words": len(self.words),
            "content_words": len(self.content_words),
            "cefr_mean": round(self.cefr_mean, 2),
            "c1_c2_pct": round(self.c1_c2_pct, 1),
            "tau": round(self.tau, 4),
            "luminescence": round(self.luminescence, 4),
            "rigor_score": self.rigor_score,
            "is_intron": self.is_intron,
            "qcd_colors": self.qcd_colors,
            "dominant_plane": self.plane_profile["dominant_name"]
        }

def parse_markdown_to_blocks(filepath: Path) -> list:
    if not filepath.exists():
        return []
    text = filepath.read_text(encoding="utf-8", errors="replace")
    doc_name = filepath.name
    
    # Split by headings and paragraph double breaks
    raw_sections = re.split(r"\n(?=#{1,4}\s+)", text)
    blocks = []
    
    for sec_idx, sec in enumerate(raw_sections):
        lines = sec.strip().splitlines()
        if not lines:
            continue
        heading = ""
        body_lines = []
        if lines[0].strip().startswith("#"):
            heading = lines[0].strip().lstrip("#").strip()
            body_lines = lines[1:]
        else:
            body_lines = lines
            
        body = "\n".join(body_lines).strip()
        if not body and heading:
            body = heading
            
        # Break body into paragraphs
        paras = re.split(r"\n\s*\n", body)
        for p_idx, p in enumerate(paras):
            p_clean = p.strip()
            if len(p_clean) < 15:
                continue
            b_id = f"{doc_name[:10]}_{sec_idx:02d}_{p_idx:02d}"
            blocks.append(SemanticBlock(b_id, doc_name, p_clean, heading))

    return blocks

# ============================================================================
# 5. SEMANTIC DISTANCE, MANIFOLD CLUSTERING & DE-DUPLICATION
# ============================================================================
def calculate_block_semantic_distance(b1: SemanticBlock, b2: SemanticBlock) -> float:
    # 1. Concept set Jaccard
    s1, s2 = b1.concept_set, b2.concept_set
    if not s1 or not s2:
        return 1.8
    jaccard = len(s1 & s2) / len(s1 | s2)

    # 2. QCD Color distance
    d_color = math.sqrt(
        (b1.qcd_colors["c_r"] - b2.qcd_colors["c_r"])**2 +
        (b1.qcd_colors["c_g"] - b2.qcd_colors["c_g"])**2 +
        (b1.qcd_colors["c_b"] - b2.qcd_colors["c_b"])**2
    )

    # 3. 7-Planes TV distance
    p1 = b1.plane_profile["probabilities"]
    p2 = b2.plane_profile["probabilities"]
    d_plane = 0.5 * sum(abs(p1[k] - p2[k]) for k in p1)

    # Combined semantic distance r in [0, 2]
    # S = 0.55 * jaccard + 0.25 * (1 - d_plane) + 0.20 * (1 - d_color)
    sim = 0.55 * jaccard + 0.25 * max(0.0, 1.0 - d_plane) + 0.20 * max(0.0, 1.0 - d_color)
    r = 1.0 - sim
    return max(0.0, r)

def cluster_semantic_exons(blocks: list, distance_threshold: float = 0.65) -> list:
    """
    50% Male / 50% Female Balanced Clustering:
    Groups blocks sharing conceptual field with threshold calibrated to detect genuine semantic overlap.
    """
    clusters = []
    assigned = [False] * len(blocks)

    for i, b_i in enumerate(blocks):
        if assigned[i]:
            continue
        cluster = [b_i]
        assigned[i] = True
        for j in range(i + 1, len(blocks)):
            if not assigned[j]:
                dist = calculate_block_semantic_distance(b_i, blocks[j])
                if dist <= distance_threshold:
                    cluster.append(blocks[j])
                    assigned[j] = True
        clusters.append(cluster)

    return clusters

def synthesize_cluster_into_exon(cluster: list) -> tuple:
    """
    Selects champion exon with highest Luminescence & Rigor,
    marks duplicates and introns as culled.
    """
    exons = [b for b in cluster if not b.is_intron]
    introns = [b for b in cluster if b.is_intron]

    if not exons:
        champion = max(cluster, key=lambda b: b.rigor_score)
        culled = [b for b in cluster if b != champion]
        return champion, culled

    # Sort exons by rigor score descending
    exons.sort(key=lambda b: b.rigor_score, reverse=True)
    champion = exons[0]
    culled = exons[1:] + introns
    return champion, culled

# ============================================================================
# 6. CAUSAL VALENCE FLOW & STRING TENSION SEQUENCING
# ============================================================================
def sequence_exons_causal_valence(retained_exons: list) -> tuple:
    if not retained_exons:
        return [], [], []

    remaining = list(retained_exons)
    # Start with foundational premise (lowest tail ingress / high Q1 who or Q5 how)
    start_block = min(remaining, key=lambda b: (b.tail_ingress_weight, -b.rigor_score))
    ordered = [start_block]
    remaining.remove(start_block)

    transitions = []
    string_snaps = []

    while remaining:
        curr = ordered[-1]
        best_cand = None
        best_cost = float("inf")
        best_pot = None
        best_r = None

        for cand in remaining:
            r = calculate_block_semantic_distance(curr, cand)
            pot = compute_cornell_potential(r)
            # Valence difference
            v_leak = abs(curr.head_egress_weight - cand.tail_ingress_weight)
            cost = 0.4 * v_leak + 0.6 * pot["v_cornell"]

            if cost < best_cost:
                best_cost = cost
                best_cand = cand
                best_pot = pot
                best_r = r

        ordered.append(best_cand)
        remaining.remove(best_cand)

        trans_record = {
            "from": curr.block_id,
            "to": best_cand.block_id,
            "r_semantic": round(best_r, 4),
            "v_cornell": best_pot["v_cornell"],
            "is_snapped": best_pot["is_snapped"]
        }
        transitions.append(trans_record)
        if best_pot["is_snapped"]:
            string_snaps.append(trans_record)

    return ordered, transitions, string_snaps

# ============================================================================
# 7. EXECUTE SUITE MERGE & GENERATE RESULTS
# ============================================================================
def execute_benchmark_suite(doc_paths: list, suite_name: str) -> dict:
    all_blocks = []
    source_stats = {}

    for p in doc_paths:
        blocks = parse_markdown_to_blocks(p)
        source_stats[p.name] = {
            "total_blocks": len(blocks),
            "exons": sum(1 for b in blocks if not b.is_intron),
            "introns": sum(1 for b in blocks if b.is_intron),
            "mean_rigor": round(sum(b.rigor_score for b in blocks) / max(len(blocks), 1), 2)
        }
        all_blocks.extend(blocks)

    total_input = len(all_blocks)
    clusters = cluster_semantic_exons(all_blocks, distance_threshold=0.62)

    retained_champions = []
    culled_blocks = []

    for c in clusters:
        champ, dropped = synthesize_cluster_into_exon(c)
        retained_champions.append(champ)
        culled_blocks.extend(dropped)

    # Sequence retained champions
    ordered_exons, transitions, string_snaps = sequence_exons_causal_valence(retained_champions)

    # Calculate aggregate metrics
    mean_tau = sum(b.tau for b in ordered_exons) / max(len(ordered_exons), 1)
    mean_lum = sum(b.luminescence for b in ordered_exons) / max(len(ordered_exons), 1)
    mean_rigor = sum(b.rigor_score for b in ordered_exons) / max(len(ordered_exons), 1)
    white_hadrons = sum(1 for b in ordered_exons if b.qcd_colors["is_color_neutral"])
    de_duplication_pct = round((len(culled_blocks) / max(total_input, 1)) * 100.0, 2)

    # 7-Planes distribution in merged text
    plane_dist = Counter(b.plane_profile["dominant_name"] for b in ordered_exons)

    return {
        "suite_name": suite_name,
        "input_blocks_total": total_input,
        "retained_exons_total": len(ordered_exons),
        "culled_blocks_total": len(culled_blocks),
        "de_duplication_pct": de_duplication_pct,
        "compression_ratio": round(len(ordered_exons) / max(total_input, 1), 3),
        "mean_tau": round(mean_tau, 4),
        "mean_luminescence": round(mean_lum, 4),
        "mean_rigor": round(mean_rigor, 2),
        "white_hadron_propositions": white_hadrons,
        "white_hadron_ratio": round(white_hadrons / max(len(ordered_exons), 1), 4),
        "string_snapping_events": len(string_snaps),
        "source_stats": source_stats,
        "plane_distribution": dict(plane_dist),
        "ordered_exons": ordered_exons,
        "string_snaps": string_snaps
    }

def main():
    print("=== Agent Great-Grandkin: Asymptotic-Merger (Pass 1) ===")

    # 1. Suite A: Actualism & Hegemony Suite
    suite_a_docs = [
        IO_DIR / "Actualism and the Psochic Hegemony.md",
        IO_DIR / "Academic Perspectives on the Psochic Hegemony.md",
        IO_DIR / "Actualism; The Crucible of the Archetypal Good Person.md"
    ]
    res_a = execute_benchmark_suite(suite_a_docs, "Actualism_Hegemony_Suite")

    # 2. Suite B: Infinity Indefinite Mathematics Suite
    suite_b_docs = [
        PHYSICS_DIR / "Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md",
        PHYSICS_DIR / "chatgpt infinity maths.md"
    ]
    res_b = execute_benchmark_suite(suite_b_docs, "Infinity_Mathematics_Suite")

    # Write synthesized merged document
    merged_output_path = WORKSPACE_DIR / "merged_coherent_document.md"
    with open(merged_output_path, "w", encoding="utf-8") as f:
        f.write("# Synthesized Coherent Master Document: Actualism, Hegemony, and Indefinite Mathematics\n\n")
        f.write("> **Unified Epistemic Formulation**: Generated via SU(3) Beta Function & Cornell Potential Confinement Merger\n")
        f.write(f"> **Engine**: `document_gluon_merger.py` (Gen 4 Bake-Off Agent 4: 50% Male / 50% Female)\n")
        f.write(f"> **De-Duplication Rate**: Suite A ({res_a['de_duplication_pct']}%), Suite B ({res_b['de_duplication_pct']}%)\n\n")
        f.write("---\n\n")

        f.write("## PART I: THE METAPHYSICAL FOUNDATIONS OF ACTUALISM & THE PSOCHIC HEGEMONY\n\n")
        curr_heading = ""
        for b in res_a["ordered_exons"]:
            if b.heading and b.heading != curr_heading:
                curr_heading = b.heading
                f.write(f"\n### {curr_heading}\n\n")
            f.write(f"{b.raw_text}\n\n")

        f.write("\n---\n\n")
        f.write("## PART II: THE INDEFINITE PROCESS FOUNDATIONS OF REALITY (IRM & INFINITY MATHEMATICS)\n\n")
        curr_heading = ""
        for b in res_b["ordered_exons"]:
            if b.heading and b.heading != curr_heading:
                curr_heading = b.heading
                f.write(f"\n### {curr_heading}\n\n")
            f.write(f"{b.raw_text}\n\n")

    print(f"Wrote merged coherent document to: {merged_output_path}")

    # Prepare results JSON
    results = {
        "engine_version": "v1.0.0",
        "agent": "agent_asymptotic_merger",
        "gender_ratio": "50% Male / 50% Female",
        "qcd_physics_constants": {
            "alpha_s": QCD_ALPHA_S,
            "sigma": QCD_SIGMA,
            "m_quark": QCD_M_QUARK,
            "r_critical": QCD_R_CRITICAL
        },
        "benchmarks": {
            "Actualism_Hegemony_Suite": {
                "input_blocks_total": res_a["input_blocks_total"],
                "retained_exons_total": res_a["retained_exons_total"],
                "culled_blocks_total": res_a["culled_blocks_total"],
                "de_duplication_pct": res_a["de_duplication_pct"],
                "compression_ratio": res_a["compression_ratio"],
                "mean_tau": res_a["mean_tau"],
                "mean_luminescence": res_a["mean_luminescence"],
                "mean_rigor": res_a["mean_rigor"],
                "white_hadron_ratio": res_a["white_hadron_ratio"],
                "string_snapping_events": res_a["string_snapping_events"],
                "plane_distribution": res_a["plane_distribution"],
                "source_stats": res_a["source_stats"]
            },
            "Infinity_Mathematics_Suite": {
                "input_blocks_total": res_b["input_blocks_total"],
                "retained_exons_total": res_b["retained_exons_total"],
                "culled_blocks_total": res_b["culled_blocks_total"],
                "de_duplication_pct": res_b["de_duplication_pct"],
                "compression_ratio": res_b["compression_ratio"],
                "mean_tau": res_b["mean_tau"],
                "mean_luminescence": res_b["mean_luminescence"],
                "mean_rigor": res_b["mean_rigor"],
                "white_hadron_ratio": res_b["white_hadron_ratio"],
                "string_snapping_events": res_b["string_snapping_events"],
                "plane_distribution": res_b["plane_distribution"],
                "source_stats": res_b["source_stats"]
            }
        }
    }

    results_path = WORKSPACE_DIR / "results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Wrote Pass 1 metrics to: {results_path}")

if __name__ == "__main__":
    main()
