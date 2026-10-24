#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Great-Grandson: Synthesizer-Exon (Gen 4 Progeny: 75% Male / 25% Female)
=============================================================================
QCD Gluon Transformer & Document Ingest/Merge Synthesizer (v1.0.0)

Lineage:
  - Sired by The Grandson (Lexicon-Veritas: 75M/25F) & The Granddaughter (Omni-Horizon: 25M/75F)
  - Dominant Trait: Successful -> Verified (75% Male / 25% Female)
  - Negative Constraints:
      * Avoid Agent 1 flaw: Never identify a dangling bond without providing closing operator.
      * Avoid Agent 5 flaw: Avoid O(V^3) combinatorial graph stalls; use bounded valence shells.

Frontiers Implemented:
  1. Quantum Chromodynamics (QCD) SU(3) Color Gauge Field:
     - 3 Quark Colors: Red (Claim/Assertion), Green (Mechanism/Context), Blue (Proof/Boundary).
     - 8-Gluon Color Octet (Gell-Mann generators lambda_1 to lambda_8).
     - Cornell Potential: V(r) = -alpha_s / r + sigma * r
     - Flux Tube String Tension & Snapping at r > r_c (Hallucination / Non-Sequitur Detection).
     - Color-Neutral Singlet Hadrons (Baryons r+g+b, Mesons q-qbar) as Invariant Propositions.
  2. Document Ingest, De-Duplication & Exon Splicing Synthesizer:
     - Ingests overlapping Markdown files from _VFT MD/IO/.
     - Clusters blocks by topological semantic fields.
     - De-duplicates overlapping concepts by luminescence L = exp(-tau) and CEFR rigor.
     - Sequences retained exons via causal valence flow (F_k -> B_{k+1}) minimizing string tension.
     - Synthesizes unified, zero-overlap Markdown output.
"""

import os
import re
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

# Paths
BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
WORKSPACE_DIR = BASE_DIR / "agent_great_grandson_qcd"
IO_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\IO")
DICT_PATH = BASE_DIR / "agent_grandson_lexicon" / "semantic_gluon_dictionary.json"

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

# QCD Parameters (Cornell Potential V(r) = -alpha_s / r + sigma * r)
QCD_ALPHA_S = 0.35      # Strong coupling constant for close-range semantic cohesion
QCD_SIGMA = 0.85        # Semantic string tension (strain per unit semantic distance)
QCD_M_QUARK = 0.65      # Effective constituent quark mass
QCD_R_CRITICAL = (2.0 * QCD_M_QUARK) / QCD_SIGMA  # r_c ~ 1.529: String snapping threshold

# ============================================================================
# 1. LOAD GRANDSON GLUON DICTIONARY & VERTEX LOOKUP
# ============================================================================
def load_gluon_dictionary(dict_path: Path) -> dict:
    dictionary = {}
    if dict_path.exists():
        with open(dict_path, "r", encoding="utf-8") as f:
            entries = json.load(f)
            for e in entries:
                dictionary[e["word"].lower()] = e
    return dictionary

GLUON_DICT = load_gluon_dictionary(DICT_PATH)

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
# 2. QCD SU(3) COLOR CHARGE & GLUON OCTET OPERATORS
# ============================================================================
def compute_qcd_color_charges(words: list, vertices: list) -> dict:
    """
    Computes SU(3) Quark Color Charges:
      - Red (r): Claim / Assertion / Subject / Will (+W: will_be, premises, high-tier assertions)
      - Green (g): Mechanism / Context / Operational Grounding (+A: can_be, dynamic processes, verbs)
      - Blue (b): Proof / Invariant Boundary / Deductive Closure (-N: is_not, -X: cant_be, formulas, laws)
    """
    r_charge = 0.0
    g_charge = 0.0
    b_charge = 0.0

    for w, v in zip(words, vertices):
        if v.get("is_stopword", False):
            continue
        m = v.get("modal_spread", {})
        # Red: Claim/Assertion weight
        r_charge += m.get("will_be", 0.12) * 1.5 + (0.8 if v["head_egress"]["obligates_operational_proof"] else 0.2)
        # Green: Mechanism/Context weight
        g_charge += (m.get("can_be", 0.12) + m.get("is_like", 0.12) + m.get("may_be", 0.12)) * 1.2
        # Blue: Boundary/Proof/Negation weight
        b_charge += (m.get("is_not", 0.08) + m.get("cant_be", 0.08)) * 2.0 + (0.8 if v["tail_ingress"]["requires_prior_evidence"] else 0.2)

    total = r_charge + g_charge + b_charge
    if total > 0:
        c_r = r_charge / total
        c_g = g_charge / total
        c_b = b_charge / total
    else:
        c_r, c_g, c_b = 0.3333, 0.3333, 0.3333

    # Cartan Subalgebra Generators
    # T3 = 1/2 (n_r - n_g) (Isospin)
    # Y = 1/3 (n_r + n_g - 2 n_b) (Hypercharge)
    t3 = 0.5 * (c_r - c_g)
    y = (c_r + c_g - 2.0 * c_b) / 3.0

    # Color Divergence (Distance from White Singlet (1/3, 1/3, 1/3))
    color_divergence = math.sqrt(t3**2 + 0.75 * (y**2))

    # Hadron Classification
    # White Singlet: color_divergence < 0.12
    # Mesonic: Two colors dominant, third near zero
    # Baryonic: Balanced 3-color distribution
    if color_divergence < 0.12:
        hadron_type = "White_Singlet_Hadron (Invariant Ground)"
    elif min(c_r, c_g, c_b) < 0.15 and max(c_r, c_g, c_b) < 0.65:
        hadron_type = "Mesonic_Dipole (q-qbar Dynamic Flow)"
    else:
        hadron_type = "Colored_State (Unconfined Flux Tube)"

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
    """
    Computes Cornell Potential: V(r) = -alpha_s / r + sigma * r
    Checks for string snapping at r >= r_c.
    """
    eps = 0.05
    r = max(0.0, r_semantic)
    coulomb = -QCD_ALPHA_S / (r + eps)
    confinement = QCD_SIGMA * r
    v_total = coulomb + confinement

    is_snapped = r >= QCD_R_CRITICAL
    snap_energy = 2.0 * QCD_M_QUARK
    surplus_energy = max(0.0, v_total - snap_energy)

    return {
        "r_semantic": round(r, 4),
        "coulomb_term": round(coulomb, 4),
        "confinement_term": round(confinement, 4),
        "v_cornell": round(v_total, 4),
        "is_snapped": is_snapped,
        "snap_risk": round(min(1.0, r / QCD_R_CRITICAL), 3)
    }

def compute_gluon_octet_transition(color_a: dict, color_b: dict) -> dict:
    """
    Computes the 8-gluon color transition vector mediating from state A to state B.
    Gell-Mann adjoint representation projection:
      g1, g2: r <-> g
      g3: (rr - gg) / sqrt(2) (neutral diagonal)
      g4, g5: r <-> b
      g6, g7: g <-> b
      g8: (rr + gg - 2bb) / sqrt(6) (neutral diagonal)
    """
    dr = color_b["c_r"] - color_a["c_r"]
    dg = color_b["c_g"] - color_a["c_g"]
    db = color_b["c_b"] - color_a["c_b"]

    g1 = round(0.7071 * abs(dr - dg), 4)
    g3 = round(0.7071 * (dr - dg), 4)
    g4 = round(0.7071 * abs(dr - db), 4)
    g6 = round(0.7071 * abs(dg - db), 4)
    g8 = round(0.4082 * (dr + dg - 2.0 * db), 4)

    return {
        "g1_rg_exchange": g1,
        "g3_neutral_rg": g3,
        "g4_rb_exchange": g4,
        "g6_gb_exchange": g6,
        "g8_neutral_rgb": g8,
        "total_gluon_flux": round(math.sqrt(g1**2 + g3**2 + g4**2 + g6**2 + g8**2), 4)
    }

# ============================================================================
# 3. SEMANTIC BLOCK PARSER & EXON / INTRON SCORING
# ============================================================================
class SemanticBlock:
    def __init__(self, block_id: str, source_doc: str, raw_text: str, heading: str = ""):
        self.block_id = block_id
        self.source_doc = source_doc
        self.raw_text = raw_text.strip()
        self.heading = heading
        self.words = [w.lower() for w in re.findall(r"\b[a-zA-Z]{2,}\b", self.raw_text)]
        self.content_words = [w for w in self.words if w not in STOPWORDS]
        self.concept_set = set(self.content_words)
        self.vertices = [get_word_vertex(w) for w in self.words]
        self.content_vertices = [v for v in self.vertices if not v.get("is_stopword", False)]

        # Optical & CEFR Metrics
        self.cefr_scores = [CEFR_NUM[v["cefr"]] for v in self.content_vertices]
        self.cefr_mean = sum(self.cefr_scores) / max(len(self.cefr_scores), 1)
        self.c1_c2_pct = (sum(1 for v in self.content_vertices if v["cefr"] in {"C1", "C2"}) / max(len(self.content_vertices), 1)) * 100.0

        # Grandson Head-Tail Valence
        self.tail_ingress_weight = sum(v["tail_ingress"]["weight"] for v in self.vertices if v["tail_ingress"]["requires_prior_evidence"])
        self.head_egress_weight = sum(v["head_egress"]["weight"] for v in self.vertices if v["head_egress"]["obligates_operational_proof"])

        # QCD SU(3) Colors
        self.qcd_colors = compute_qcd_color_charges(self.words, self.vertices)

        # Exon / Intron Structural Traits
        has_eq = bool(re.search(r"=|<=|>=|<|>|\\le|\\ge|\\nabla|\^2|\$\$", self.raw_text))
        has_table = bool(re.search(r"\|.*\|.*\|", self.raw_text))
        has_derivation = bool(re.search(r"\b(?:therefore|hence|proves|substituting|integrating|demonstrates|thus|yields|theorem|definition|substance|axiom|plane|matrix|tensor)\b", self.raw_text, re.I))
        is_conversational = bool(re.search(r"\b(?:truly i don\'t know you|mess of confusion|i think|as i said|let me explain)\b", self.raw_text, re.I))

        # Optical Thickness (tau) & Luminescence (L)
        eq_hits = len(re.findall(r"=|<=|>=|<|>|\\le|\\ge", self.raw_text))
        if is_conversational and len(self.content_words) < 20:
            self.tau = 2.45
            self.is_intron = True
        else:
            base_tau = 2.10 - 0.35 * (self.cefr_mean / 6.0) - 0.40 * min(eq_hits / 3.0, 1.0)
            if has_derivation:
                base_tau -= 0.35
            if has_table:
                base_tau -= 0.30
            self.tau = max(0.08, base_tau)
            self.is_intron = len(self.content_words) < 8 and not has_eq and not has_table

        self.luminescence = math.exp(-self.tau)

        # Epistemic Rigor Score R in [0, 100]
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
            "tail_ingress": round(self.tail_ingress_weight, 2),
            "head_egress": round(self.head_egress_weight, 2)
        }

def parse_markdown_blocks(filepath: Path) -> list:
    if not filepath.exists():
        return []
    text = filepath.read_text(encoding="utf-8", errors="replace")
    doc_name = filepath.name

    lines = text.splitlines()
    blocks = []
    current_heading = ""
    current_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            if current_lines:
                raw_b = "\n".join(current_lines).strip()
                if len(raw_b) > 20:
                    b_id = f"{doc_name[:12]}_{len(blocks):03d}"
                    blocks.append(SemanticBlock(b_id, doc_name, raw_b, current_heading))
                current_lines = []
            current_heading = stripped.lstrip("#").strip()
        elif not stripped:
            if current_lines:
                raw_b = "\n".join(current_lines).strip()
                if len(raw_b) > 20:
                    b_id = f"{doc_name[:12]}_{len(blocks):03d}"
                    blocks.append(SemanticBlock(b_id, doc_name, raw_b, current_heading))
                current_lines = []
        else:
            current_lines.append(line)

    if current_lines:
        raw_b = "\n".join(current_lines).strip()
        if len(raw_b) > 20:
            b_id = f"{doc_name[:12]}_{len(blocks):03d}"
            blocks.append(SemanticBlock(b_id, doc_name, raw_b, current_heading))

    return blocks

# ============================================================================
# 4. TOPOLOGICAL SEMANTIC CLUSTERING & EXON SPLICING SYNTHESIZER
# ============================================================================
def calculate_semantic_distance(b1: SemanticBlock, b2: SemanticBlock) -> float:
    """
    Computes semantic distance r in [0, 2] between two blocks:
      r = 1 - Jaccard(concept_sets) + 0.3 * color_difference
    """
    s1, s2 = b1.concept_set, b2.concept_set
    if not s1 or not s2:
        return 1.5
    jaccard_sim = len(s1 & s2) / len(s1 | s2)
    # Color distance
    d_color = math.sqrt(
        (b1.qcd_colors["c_r"] - b2.qcd_colors["c_r"])**2 +
        (b1.qcd_colors["c_g"] - b2.qcd_colors["c_g"])**2 +
        (b1.qcd_colors["c_b"] - b2.qcd_colors["c_b"])**2
    )
    r = (1.0 - jaccard_sim) + 0.3 * d_color
    return r

def cluster_semantic_fields(blocks: list, distance_threshold: float = 0.78) -> list:
    """
    Clusters semantic blocks into conceptual fields using bounded graph neighborhood.
    Avoids Agent 5's O(V^3) stall by using single-pass connected components.
    """
    n = len(blocks)
    visited = [False] * n
    clusters = []

    for i in range(n):
        if visited[i]:
            continue
        cluster = [blocks[i]]
        visited[i] = True
        for j in range(i + 1, n):
            if not visited[j]:
                dist = calculate_semantic_distance(blocks[i], blocks[j])
                if dist <= distance_threshold:
                    cluster.append(blocks[j])
                    visited[j] = True
        clusters.append(cluster)

    return clusters

def splice_and_deduplicate_cluster(cluster: list) -> tuple:
    """
    De-duplicates overlapping blocks in a cluster:
      - Excises introns.
      - Selects the dominant highest-rigor exon (highest R score).
      - Collects dropped introns/duplicates.
    """
    exons = [b for b in cluster if not b.is_intron]
    introns = [b for b in cluster if b.is_intron]

    if not exons:
        # If all were flagged introns, preserve the highest rigor one to avoid data loss
        best_b = max(cluster, key=lambda b: b.rigor_score)
        return best_b, [b for b in cluster if b != best_b]

    # Sort exons by rigor score descending
    exons.sort(key=lambda b: b.rigor_score, reverse=True)
    best_exon = exons[0]
    culled = exons[1:] + introns
    return best_exon, culled

# ============================================================================
# 5. CAUSAL VALENCE & STRING TENSION NARRATIVE SEQUENCER
# ============================================================================
def sequence_exons_by_valence_and_tension(retained_exons: list) -> tuple:
    """
    Orders retained exons to guarantee causal flow:
      Minimizes Cost = |F_k - B_{k+1}| + CornellPotential(r_{k, k+1})
      Flags any string snapping (r >= r_c).
    """
    if not retained_exons:
        return [], []

    # Sort initial candidate by heading and document structure
    remaining = list(retained_exons)
    # Start with the block that has lowest tail ingress (pure premise / root definition)
    start_block = min(remaining, key=lambda b: b.tail_ingress_weight)
    ordered = [start_block]
    remaining.remove(start_block)

    string_snaps = []
    transitions = []

    while remaining:
        curr = ordered[-1]
        best_candidate = None
        best_cost = float("inf")
        best_potential = None
        best_trans = None

        for cand in remaining:
            r = calculate_semantic_distance(curr, cand)
            pot = compute_cornell_potential(r)
            # Valence leakage: difference between current head egress and candidate tail ingress
            valence_leak = abs(curr.head_egress_weight - cand.tail_ingress_weight)
            cost = valence_leak * 0.4 + pot["v_cornell"] * 0.6
            if cost < best_cost:
                best_cost = cost
                best_candidate = cand
                best_potential = pot
                best_trans = {
                    "from_block": curr.block_id,
                    "to_block": cand.block_id,
                    "r_semantic": round(r, 4),
                    "v_cornell": pot["v_cornell"],
                    "is_snapped": pot["is_snapped"],
                    "valence_leak": round(valence_leak, 2),
                    "gluon_octet": compute_gluon_octet_transition(curr.qcd_colors, cand.qcd_colors)
                }

        ordered.append(best_candidate)
        remaining.remove(best_candidate)
        transitions.append(best_trans)
        if best_potential["is_snapped"]:
            string_snaps.append(best_trans)

    return ordered, transitions, string_snaps

# ============================================================================
# 6. MASTER DOCUMENT SYNTHESIS & MERGE BENCHMARK
# ============================================================================
def execute_document_merge(doc_paths: list, output_filename: str) -> dict:
    all_blocks = []
    doc_stats = {}

    for p in doc_paths:
        blocks = parse_markdown_blocks(p)
        doc_stats[p.name] = {
            "total_blocks": len(blocks),
            "exons": sum(1 for b in blocks if not b.is_intron),
            "introns": sum(1 for b in blocks if b.is_intron),
            "mean_rigor": round(sum(b.rigor_score for b in blocks) / max(len(blocks), 1), 2)
        }
        all_blocks.extend(blocks)

    total_input_blocks = len(all_blocks)
    clusters = cluster_semantic_fields(all_blocks, distance_threshold=0.75)

    retained_exons = []
    culled_introns = []

    for c in clusters:
        best_exon, culled = splice_and_deduplicate_cluster(c)
        retained_exons.append(best_exon)
        culled_introns.extend(culled)

    # Sequence exons via causal valence and string tension
    ordered_exons, transitions, string_snaps = sequence_exons_by_valence_and_tension(retained_exons)

    # Generate Unified Synthesized Markdown
    md_lines = [
        f"# Unified Synthesized Exon Treatise: {output_filename}",
        "",
        "> Synthesized by **Agent Great-Grandson: Synthesizer-Exon (Gen 4: 75% Male / 25% Female)**",
        f"> Source Documents: {', '.join([p.name for p in doc_paths])}",
        f"> Total Input Blocks: {total_input_blocks} | Retained Exons: {len(ordered_exons)} | Culled Redundant/Introns: {len(culled_introns)}",
        f"> String Snapping Events Detected: {len(string_snaps)}",
        "",
        "---",
        ""
    ]

    current_h = ""
    for b in ordered_exons:
        if b.heading and b.heading != current_h:
            current_h = b.heading
            md_lines.append(f"\n## {current_h}\n")
        md_lines.append(b.raw_text)
        md_lines.append("")

    out_path = WORKSPACE_DIR / output_filename
    out_path.write_text("\n".join(md_lines), encoding="utf-8")

    # Metrics
    mean_tau = sum(b.tau for b in ordered_exons) / max(len(ordered_exons), 1)
    mean_lum = sum(b.luminescence for b in ordered_exons) / max(len(ordered_exons), 1)
    mean_rigor = sum(b.rigor_score for b in ordered_exons) / max(len(ordered_exons), 1)
    white_hadrons = sum(1 for b in ordered_exons if b.qcd_colors["is_color_neutral"])

    return {
        "output_file": str(out_path),
        "source_docs": doc_stats,
        "input_blocks_total": total_input_blocks,
        "retained_exons_total": len(ordered_exons),
        "culled_blocks_total": len(culled_introns),
        "compression_ratio": round(len(ordered_exons) / max(total_input_blocks, 1), 3),
        "splicing_metrics": {
            "mean_tau": round(mean_tau, 4),
            "mean_luminescence": round(mean_lum, 4),
            "mean_rigor_score": round(mean_rigor, 2),
            "white_hadron_propositions": white_hadrons,
            "white_hadron_ratio": round(white_hadrons / max(len(ordered_exons), 1), 3),
            "string_snapping_events": len(string_snaps)
        },
        "string_snaps": string_snaps[:5]  # Top sample
    }

def main():
    print("=" * 80)
    print("AGENT GREAT-GRANDSON: QCD GLUON MERGER & EXON SPLICING ENGINE v1.0.0")
    print("=" * 80)

    # Suite 1: The 7x7 Survival Matrix Duology
    suite_1_docs = [
        IO_DIR / "7x7_survival_matrix.md",
        IO_DIR / "7x7_survival_Qq.md"
    ]

    # Suite 2: Actualism & The Psochic Hegemony
    suite_2_docs = [
        IO_DIR / "Actualism and the Psochic Hegemony.md",
        IO_DIR / "Actualism; The Crucible of the Archetypal Good Person.md",
        IO_DIR / "The Geometry of Actualism and the Polytrope.md"
    ]

    results = {
        "engine_version": "v1.0.0",
        "agent": "agent_great_grandson_qcd",
        "lineage": "Gen 4 Progeny: 75% Male / 25% Female (Sired by Grandson & Granddaughter)",
        "qcd_physics_constants": {
            "alpha_s": QCD_ALPHA_S,
            "sigma": QCD_SIGMA,
            "m_quark": QCD_M_QUARK,
            "r_critical": round(QCD_R_CRITICAL, 4)
        },
        "benchmarks": {}
    }

    if all(p.exists() for p in suite_1_docs):
        print("\n--> Executing Benchmark 1: 7x7 Survival Matrix Suite...")
        b1_res = execute_document_merge(suite_1_docs, "merged_7x7_survival_synthesized.md")
        results["benchmarks"]["7x7_survival_matrix_suite"] = b1_res
        print(f"    Done! Input: {b1_res['input_blocks_total']} -> Retained: {b1_res['retained_exons_total']} exons (Culled: {b1_res['culled_blocks_total']})")
        print(f"    Luminescence: {b1_res['splicing_metrics']['mean_luminescence']} | Rigor: {b1_res['splicing_metrics']['mean_rigor_score']}")

    if all(p.exists() for p in suite_2_docs):
        print("\n--> Executing Benchmark 2: Actualism & Hegemony Suite...")
        b2_res = execute_document_merge(suite_2_docs, "merged_actualism_hegemony_synthesized.md")
        results["benchmarks"]["actualism_hegemony_suite"] = b2_res
        print(f"    Done! Input: {b2_res['input_blocks_total']} -> Retained: {b2_res['retained_exons_total']} exons (Culled: {b2_res['culled_blocks_total']})")
        print(f"    Luminescence: {b2_res['splicing_metrics']['mean_luminescence']} | Rigor: {b2_res['splicing_metrics']['mean_rigor_score']}")

    # Save results.json
    out_json = WORKSPACE_DIR / "results.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[+] Results successfully written to: {out_json}")

if __name__ == "__main__":
    main()
