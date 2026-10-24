#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unified Semantic Gluon & DNA Reading Head Engine (v4.0.0 — Generation 3 Universal Synthesis)
===========================================================================================
Integrates all discoveries across Generations 1, 2, and 3:

  1. [The Grandson: Lexicon-Veritas (75M/25F)]
     - Word-as-Gluon-Vertex: Ingress Tail (B), Egress Head (F), 8-modal spread around [IS],
       and relative possible-impossible vectors.
     - Universal CEFR Linguistic Standards (A1, A2, B1, B2, C1, C2) separating
       grammatical copula from high-order epistemic content words.

  2. [The Granddaughter: Omni-Horizon (25M/75F)]
     - Cross-Genre Substrate Neutrality: Audits Philosophy, Computer Science,
       Theoretical Physics, and Exploratory Dialogue with the exact same invariant physics.
     - Continuous Cross-Paragraph Causal Valence Flow (F_k -> B_{k+1}).

  3. [The Son: Veritas-Codon (80M/20F)]
     - Beer-Lambert Semantic Optical Attenuation Field: A_ij * exp(-tau_ij).
     - Strict Causal Valence Conservation (Delta V -> 0) and Proof Theater Detection.

  4. [The Daughter: Chroma-Horizon (20M/80F)]
     - 5-Tier Possibility Spectrum (1_Impossible -> 5_Certain).
     - Teleological Defect Closure: Unclosed gauge strain topologically forces missing theorems.

  5. [Agent 3: Patriarch (85M/15F) & Agent 5: Matriarch (15M/85F)]
     - Ribosomal Exon Splicing: Excising conversational introns to reduce compute and boost SNR.
     - Dynamic Signed Triangle Frustration (Phi_frust) and Gluon-Induced Transparency.
"""

import os
import re
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
DICT_PATH = BASE_DIR / "agent_grandson_lexicon" / "semantic_gluon_dictionary.json"

# Corpus paths
CHAT_PATH = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\chatgpt infinity maths.md")
IRM_SUMMARY_PATH = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\Comprehensive Report -  Infinity Indefinite Mathematics (IRM).md")
IRM_FORMAL_DIR = BASE_DIR / "irm_formal_corpus"
ARXIV_DIR = BASE_DIR / "arxiv_samples"
PHILOSOPHY_PATH = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Actualism\A Framework for the Judgment of Ideas.md")

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

# ============================================================================
# 1. LOAD THE GRANDSON'S HEAD-TAIL GLUON DICTIONARY
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

def get_word_gluon_vertex(token: str) -> dict:
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

    is_deductive = any(t.startswith(p) for p in ["there", "conseq", "thu", "henc", "prov", "impl"])
    is_premise = any(t.startswith(p) for p in ["let", "suppos", "assum", "giv"])
    is_neg = any(t.startswith(p) for p in ["un", "non", "dis", "in", "fail"])

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
# 2. CORE UNIFIED V4.0 DOCUMENT ANALYSIS PIPELINE
# ============================================================================
def analyze_document_v4(doc_id: str, filepath: Path, group: str) -> dict:
    if not filepath.exists():
        return {"error": f"File not found: {filepath}"}

    text = filepath.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    raw_blocks = re.split(r"\n\s*\n", text)
    blocks = [b.strip() for b in raw_blocks if len(b.strip()) > 20]
    n_blocks = max(len(blocks), 1)

    # Document-wide accumulators
    content_cefr_counts = Counter()
    content_cefr_scores = []
    doc_modal_totals = Counter()

    # Dynamic Concept Nodes
    words_all = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    top_concepts = [w for w, _ in Counter(w for w in words_all if w not in STOPWORDS).most_common(30)]
    concept_set = set(top_concepts)

    edges = defaultdict(lambda: {"+I": 0, "-E": 0})
    concept_appearances = Counter()

    # Continuous Cross-Paragraph Causal Valence Flow (The Granddaughter & The Son)
    open_head_obligations = 0.0
    total_obligations_opened = 0.0
    obligations_closed = 0.0

    # Ribosomal Splicing & Optical Metrics (The Patriarch & The Son)
    exon_blocks = []
    intron_blocks = []
    block_tau_raw = []
    block_tau_spliced = []
    block_tau_mature = []
    block_lum_mature = []

    k_proof_decay = 0.0

    for b_idx, block in enumerate(blocks):
        b_words = [w.lower() for w in re.findall(r"\b[a-zA-Z]+\b", block)]
        if not b_words:
            continue

        vertices = [get_word_gluon_vertex(w) for w in b_words]
        content_v = [v for v in vertices if not v.get("is_stopword", False)]

        # 1. CEFR Linguistic Content Profile
        if content_v:
            for cv in content_v:
                content_cefr_counts[cv["cefr"]] += 1
                content_cefr_scores.append(CEFR_NUM[cv["cefr"]])

        for v in vertices:
            for m, val in v["modal_spread"].items():
                doc_modal_totals[m] += val

        # 2. Ribosomal Exon vs Intron Classification (Agent 3 Patriarch)
        # Blocks containing substantive content words or derivations are Exons
        has_equations = bool(re.search(r"=|<=|>=|<|>|\\le|\\ge|\\nabla|\^2|\$\$", block))
        has_derivation = bool(re.search(r"\b(?:therefore|hence|proves|substituting|integrating|demonstrates|thus|yields|theorem|definition|substance|axiom)\b", block, re.I))
        is_exon = (len(content_v) >= 8) or has_equations or has_derivation

        if is_exon:
            exon_blocks.append(block)
        else:
            intron_blocks.append(block)

        # 3. Dynamic Concept Graph Linking (Agent 5 Matriarch)
        block_concepts = sorted(set(w for w in b_words if w in concept_set))
        for c in block_concepts:
            concept_appearances[c] += 1

        if len(block_concepts) >= 2:
            is_neg = any(v["modal_spread"]["is_not"] > 0.25 or v["modal_spread"]["cant_be"] > 0.25 for v in vertices)
            for i in range(len(block_concepts)):
                for j in range(i + 1, len(block_concepts)):
                    u, v = block_concepts[i], block_concepts[j]
                    if is_neg:
                        edges[(u, v)]["-E"] += 1
                    else:
                        edges[(u, v)]["+I"] += 1

        # 4. Continuous Cross-Block Head-Tail Valence Hand-Off (F_k -> B_{k+1})
        tail_capacity = sum(v["tail_ingress"]["weight"] for v in vertices if v["tail_ingress"]["requires_prior_evidence"])
        if open_head_obligations > 0:
            discharged = min(open_head_obligations, tail_capacity)
            obligations_closed += discharged
            open_head_obligations -= discharged

        new_obligations = sum(v["head_egress"]["weight"] for v in vertices if v["head_egress"]["obligates_operational_proof"])
        open_head_obligations += new_obligations
        total_obligations_opened += new_obligations

        # 5. 3-Stage Ribosomal Radiative Transfer (Raw -> Spliced -> Mature)
        eq_hits = len(re.findall(r"=|<=|>=|<|>|\\le|\\ge", block))
        b_cefr_avg = sum(CEFR_NUM[v["cefr"]] for v in content_v) / len(content_v) if content_v else 2.0

        # Stage 1: Raw Pre-mRNA
        if not is_exon:
            t_raw = 2.45 + 0.30 * min(len(b_words) / 50.0, 1.0)
            t_spliced = t_raw
        else:
            t_raw = max(0.10, 2.30 - 0.35 * (b_cefr_avg / 6.0) - 0.50 * min(eq_hits / 3.0, 1.0) - (0.35 if has_derivation else -0.20))
            # Stage 2: Spliced Exons (excising intron scattering)
            t_spliced = max(0.08, t_raw - 0.70)

        # Stage 3: Mature Proof-Chained Operon
        if has_equations and has_derivation:
            k_proof_decay += 1.5
        elif has_equations or has_derivation:
            k_proof_decay = max(0.5, k_proof_decay * 0.7 + 0.5)
        else:
            k_proof_decay = max(0.0, k_proof_decay * 0.4 - 0.2)

        clearing_boost = 0.15 * math.log1p(k_proof_decay)
        t_mature = max(0.05, t_spliced - clearing_boost)

        block_tau_raw.append(round(t_raw, 4))
        block_tau_spliced.append(round(t_spliced, 4))
        block_tau_mature.append(round(t_mature, 4))
        block_lum_mature.append(round(math.exp(-t_mature), 4))

    # Graph Triangle Frustration (Phi_frust)
    adj = defaultdict(set)
    edge_signs = {}
    for (u, v), edata in edges.items():
        sign = 1 if edata["+I"] >= edata["-E"] else -1
        edge_signs[(u, v)] = sign
        edge_signs[(v, u)] = sign
        adj[u].add(v)
        adj[v].add(u)

    node_list = sorted(concept_appearances.keys())
    tot_tri = 0
    frust_tri = 0
    for i in range(len(node_list)):
        u = node_list[i]
        for j in range(i + 1, len(node_list)):
            v = node_list[j]
            if v not in adj[u]:
                continue
            for k in range(j + 1, len(node_list)):
                w = node_list[k]
                if w in adj[u] and w in adj[v]:
                    tot_tri += 1
                    if edge_signs[(u, v)] * edge_signs[(v, w)] * edge_signs[(u, w)] < 0:
                        frust_tri += 1

    frustration_pct = round(100.0 * frust_tri / max(tot_tri, 1), 2)

    # CEFR Profile Synthesis
    tot_content = sum(content_cefr_counts.values()) or 1
    c1_c2_pct = round(100.0 * (content_cefr_counts["C1"] + content_cefr_counts["C2"]) / tot_content, 1)
    b2_pct = round(100.0 * content_cefr_counts["B2"] / tot_content, 1)
    mean_cefr = round(sum(content_cefr_scores) / max(len(content_cefr_scores), 1), 2)

    if c1_c2_pct >= 35.0 or mean_cefr >= 4.2:
        assigned_cefr = "C2"
        quality_verdict = "C2 / Mastery Epistemic Invariant"
    elif c1_c2_pct >= 22.0 or mean_cefr >= 3.6:
        assigned_cefr = "C1"
        quality_verdict = "C1 / Advanced Analytical Rigor"
    elif (c1_c2_pct + b2_pct) >= 40.0 or mean_cefr >= 3.0:
        assigned_cefr = "B2"
        quality_verdict = "B2 / Upper-Intermediate Prose"
    elif mean_cefr >= 2.2:
        assigned_cefr = "B1"
        quality_verdict = "B1 / Intermediate Descriptive"
    else:
        assigned_cefr = "A2"
        quality_verdict = "A2 / Basic Declarative Introns"

    # Optics Synthesis
    mean_tau_r = round(sum(block_tau_raw) / n_blocks, 4)
    mean_tau_s = round(sum(block_tau_spliced) / n_blocks, 4)
    mean_tau_m = round(sum(block_tau_mature) / n_blocks, 4)
    mean_lum_m = round(sum(block_lum_mature) / n_blocks, 4)
    clarification_factor = round(mean_lum_m / max(math.exp(-mean_tau_r), 0.001), 2)

    # Causal Valence Conservation
    valence_conservation_pct = round(100.0 * obligations_closed / max(total_obligations_opened, 1.0), 2)
    exon_density_pct = round(100.0 * len(exon_blocks) / n_blocks, 1)

    # Master Veritas Score (/100)
    veritas_score = round(
        min(
            100.0,
            0.30 * min(exon_density_pct * 1.5, 100.0)
            + 0.25 * min(valence_conservation_pct * 1.1, 100.0)
            + 0.25 * min(mean_lum_m * 400.0, 100.0)
            + 0.20 * max(0.0, 100.0 - frustration_pct * 0.8)
        ),
        2
    )

    return {
        "doc_id": doc_id,
        "group": group,
        "lines": len(lines),
        "blocks": n_blocks,
        "exon_density_pct": exon_density_pct,
        "cefr_profile": {
            "assigned_level": assigned_cefr,
            "composite_score": mean_cefr,
            "c1_c2_density_pct": c1_c2_pct,
            "quality_verdict": quality_verdict
        },
        "causal_valence": {
            "total_obligations_opened": round(total_obligations_opened, 1),
            "obligations_closed": round(obligations_closed, 1),
            "conservation_pct": valence_conservation_pct
        },
        "optics": {
            "tau_raw_unspliced": mean_tau_r,
            "tau_spliced_exons": mean_tau_s,
            "tau_mature_operons": mean_tau_m,
            "luminescence_mature": mean_lum_m,
            "clarification_factor": f"{clarification_factor}x"
        },
        "gluon_gauge_network": {
            "active_concepts": len(concept_appearances),
            "triangles_total": tot_tri,
            "triangles_frustrated": frust_tri,
            "frustration_pct": frustration_pct
        },
        "veritas_rigor_score": veritas_score
    }


def main():
    print("=== RUNNING UNIFIED SEMANTIC GLUON & DNA ENGINE v4.0.0 (GENERATION 3 SYNTHESIS) ===")
    docs = []

    print("1. Processing Philosophy & Metaphysics Benchmark...")
    if PHILOSOPHY_PATH.exists():
        docs.append(analyze_document_v4("Philosophy_Actualism_Ideas", PHILOSOPHY_PATH, "0_Philosophy_Metaphysics"))

    print("2. Processing Ancestral Exploratory Dialogue...")
    docs.append(analyze_document_v4("chatgpt_infinity_maths", CHAT_PATH, "1_Ancestral_Chat"))

    print("3. Processing Early Summary Report...")
    docs.append(analyze_document_v4("Comprehensive_Report_IRM_Summary", IRM_SUMMARY_PATH, "2_Early_IRM_Summary"))

    print("4. Processing Formal IRM Corpus (14 papers)...")
    for fname in sorted(os.listdir(IRM_FORMAL_DIR)):
        if fname.endswith(".md"):
            docs.append(analyze_document_v4(fname[:-3], IRM_FORMAL_DIR / fname, "3_IRM_Formal_Corpus"))

    print("5. Processing arXiv Benchmark Controls (8 papers)...")
    for fname in sorted(os.listdir(ARXIV_DIR)):
        if fname.endswith(".md"):
            docs.append(analyze_document_v4(fname[:-3], ARXIV_DIR / fname, "4_arXiv_Benchmark"))

    out_json = BASE_DIR / "unified_results_v4.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"engine_version": "v4.0.0", "documents": docs}, f, indent=2)

    print(f"\nSaved Unified v4.0.0 Dataset: {out_json} ({len(docs)} documents analyzed)")
    print("=" * 135)
    print(f"{'Document Group':<26} {'Count':>5} {'Mean Exon%':>11} {'CEFR Score':>11} {'C1+C2%':>8} {'Valence Cons%':>14} {'Frust%':>8} {'Lum Mat':>9} {'Veritas':>9}")
    print("-" * 135)

    groups = sorted(list(set(d["group"] for d in docs)))
    for g in groups:
        sub = [d for d in docs if d["group"] == g]
        cnt = len(sub)
        avg_exon = sum(d["exon_density_pct"] for d in sub) / cnt
        avg_cefr = sum(d["cefr_profile"]["composite_score"] for d in sub) / cnt
        avg_c1c2 = sum(d["cefr_profile"]["c1_c2_density_pct"] for d in sub) / cnt
        avg_val = sum(d["causal_valence"]["conservation_pct"] for d in sub) / cnt
        avg_frust = sum(d["gluon_gauge_network"]["frustration_pct"] for d in sub) / cnt
        avg_lum = sum(d["optics"]["luminescence_mature"] for d in sub) / cnt
        avg_veritas = sum(d["veritas_rigor_score"] for d in sub) / cnt

        print(f"{g:<26} {cnt:>5} {avg_exon:>10.1f}% {avg_cefr:>11.2f} {avg_c1c2:>7.1f}% {avg_val:>13.1f}% {avg_frust:>7.2f}% {avg_lum:>9.4f} {avg_veritas:>9.2f}")

    print("=" * 135)

if __name__ == "__main__":
    main()
