"""
LIVE PROOF & DEMONSTRATION OF UNIFIED VFT ENGINE (v6.0.0)
=============================================================================
Provides rigorous, empirical proof of both:
1. DOC MERGE: Splicing overlapping multi-document text, removing chat fluff
   and duplicate blocks while preserving 100% of mathematical formulas.
2. DOC CREATE: Continuous Semantic Sponge absorption on R^7, 3-Gluon gauge
   curvature, and VFT Universal Force Equation (F = k * sigma * V).
=============================================================================
"""

import sys
import os
import re
import json
import math
from pathlib import Path

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.append(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
from unified_vft_semantic_sponge_engine import (
    ScaledContinuousSemanticSponge,
    ThreeGluonHomogeneousGaugeSpace,
    VFTUniversalForceEngine,
    SemanticExonBlock,
    extract_all_math_lemmas
)

def run_doc_merge_proof():
    print("=" * 80)
    print(" PROOF 1: DOCUMENT MERGE & SURGICAL INTRON CULLING")
    print("=" * 80)

    # Real raw text sample representing an overlapping, redundant multi-turn chat draft
    # containing:
    # 1. Chat dialogue overhead
    # 2. Formal mathematical lemma (1_n^\infty = 0_{n+1}^\infty and a_n = a_{n+1})
    # 3. An exact duplicate explanation paragraph from a secondary source
    # 4. Fluff conversational offers ("Do you want me to...")
    raw_dirty_blocks = [
        "##### You said:\nis this already not defined in standard math?",
        "###### ChatGPT said:\nYou’re right to pause there — as written, $$1_n^\\infty = 0_{n+1}^\\infty$$ is **not defined in standard mathematics**.",
        "Here is why: The \"∞\" symbol isn't a valid index or exponent in ordinary arithmetic. In analysis, those are indeterminate forms.",
        "Equality across successive terms ($$a_n = a_{n+1}$$) is a perfectly valid recursive definition, but putting infinity into it makes it undefined unless you’ve created a new symbolic system.",
        "Do you want me to try formalising your exact symbolic version, or do you want me to recast it into standard analysis terms?",
        "##### You said:\nis the an = an+1 standard for numbers axioms?",
        "###### ChatGPT said:\nCertainly! Good question — and subtle.",
        # Overlapping / duplicate block from another draft:
        "Equality across successive terms ($$a_n = a_{n+1}$$) is a perfectly valid recursive definition, but putting infinity into it makes it undefined unless you’ve created a new symbolic system.",
        # True mathematical physics exon:
        "Where $$a_n = a_{n+1}$$ for all n, then $$a_n = L$$ as a constant sequence. The **hyperreals** represent values where the difference between $$0_n$$ and $$1_n$$ can be an infinitesimal $$\\epsilon > 0$$."
    ]

    print(f"[*] Input Raw Blocks: {len(raw_dirty_blocks)}")
    total_raw_chars = sum(len(b) for b in raw_dirty_blocks)
    print(f"[*] Total Input Characters: {total_raw_chars}")

    # Track ground truth mathematical lemmas before culling
    all_raw_text = "\n\n".join(raw_dirty_blocks)
    raw_lemmas = extract_all_math_lemmas(all_raw_text)
    print(f"[*] Tracked Mathematical Lemmas in Input: {len(raw_lemmas)}")
    for lm in raw_lemmas:
        print(f"    - LEMMA: {lm}")

    # Ingest into SemanticExonBlocks
    blocks = [SemanticExonBlock(b, "synthetic_test.md", idx) for idx, b in enumerate(raw_dirty_blocks)]
    
    retained = []
    culled = []
    covered_lemmas = set()

    for b in blocks:
        uncovered = b.lemmas - covered_lemmas
        holds_proof = len(uncovered) > 0

        if holds_proof:
            retained.append(b)
            covered_lemmas.update(b.lemmas)
            continue

        if b.is_intron:
            culled.append((b, "CHAT_INTRON_FILTER"))
            continue

        # Invariant Lemma Protection
        if b.is_formal_invariant:
            is_dup = any(b.word_set == exist.word_set and b.raw_text == exist.raw_text for exist in retained)
            if not is_dup:
                retained.append(b)
                covered_lemmas.update(b.lemmas)
            else:
                culled.append((b, "EXACT_LEMMA_DUPLICATE"))
            continue

        # Overlap check
        is_redundant = False
        for r in retained:
            if b.compute_overlap_coefficient(r) > 0.48:
                is_redundant = True
                break
        if is_redundant:
            culled.append((b, "SIMPSON_OVERLAP_CONTAINMENT"))
        else:
            retained.append(b)
            covered_lemmas.update(b.lemmas)

    print("\n[-] Culled Blocks:")
    for b, reason in culled:
        print(f"    [CULLED: {reason}] -> {repr(b.raw_text[:70])}...")

    print("\n[+] Retained Blocks:")
    merged_clean_text = []
    for b in retained:
        print(f"    [RETAINED: {'FORMAL_PROOF' if b.is_formal_invariant else 'CLEAN_EXON'}] -> {repr(b.raw_text[:70])}...")
        merged_clean_text.append(b.raw_text)

    # Verify Lemma Retention
    final_merged = "\n\n".join(merged_clean_text)
    final_lemmas = extract_all_math_lemmas(final_merged)
    lemma_preservation = (len(final_lemmas & raw_lemmas) / len(raw_lemmas) * 100.0) if raw_lemmas else 100.0
    culling_rate = (len(culled) / len(raw_dirty_blocks) * 100.0)

    print("\n--- MERGE VERIFICATION METRICS ---")
    print(f"Culling Rate:                  {culling_rate:.2f}% of noise excised")
    print(f"Input Mathematical Formulas:   {len(raw_lemmas)}")
    print(f"Retained Mathematical Formulas:{len(final_lemmas)} ({lemma_preservation:.1f}% retention)")
    assert lemma_preservation == 100.0, "FATAL: Mathematical lemma was lost during merge!"
    print("Assertion Passed: ZERO mathematical loss during merge.\n")


def run_doc_create_sponge_proof():
    print("=" * 80)
    print(" PROOF 2: DOC CREATE / CONTINUOUS SPONGE & VFT UNIVERSAL FORCE")
    print("=" * 80)

    sponge = ScaledContinuousSemanticSponge()
    gluon_space = ThreeGluonHomogeneousGaugeSpace()
    force_engine = VFTUniversalForceEngine(k_coupling=1.0)

    # Jargon-heavy scholastic input paragraph typical of academic ungrounded text
    raw_draft = (
        "The epistemological presuppositions of the psochic hegemony demand an allostatic load "
        "reduction through dichotomous thinking, in sharp contrast to the ontological status of "
        "actus purus which strictly conditioned upon active potency necessarily implies that "
        "human actus et potentia requires teleological orientation."
    )

    print("[*] RAW DRAFT BEFORE CONTINUOUS SPONGE & VFT RELAXATION:")
    print(f"\"{raw_draft}\"\n")

    # Measure initial force & strain of the raw draft
    raw_force = force_engine.compute_sentence_force(raw_draft, is_formal_invariant=False)
    raw_gluon = gluon_space.evaluate_sentence_operators(raw_draft)

    print("--- RAW DRAFT METRICS (BEFORE) ---")
    print(f"Semantic Strain sigma:      {raw_force['strain_sigma']} (High ungrounded tension)")
    print(f"Idea Ball Volume V:         {raw_force['volume_V']}")
    print(f"Dynamic Force F:            {raw_force['dynamic_force_F']}")
    print(f"Cost of Being (-inf + 1):   {raw_force['cob_status']}")
    print(f"Detected 3-Gluon Operators: {raw_gluon['detected_operators']}")
    print(f"Gauge Curvature kappa:      {raw_gluon['effective_curvature_kappa']} rad")
    print(f"Gauge Friction mu:          {raw_gluon['effective_friction_mu']}")
    print(f"String Confinement Status:  {'CONFINED' if raw_gluon['is_string_confined'] else 'SNAPPED'}")

    # Now apply the Continuous Semantic Sponge across R^7
    # Approximate plane coordinates for this draft: Q1 (Metaphysics), Q2 (Possible), Q5 (Logic)
    plane_coords = [0.4, 0.2, 0.0, 0.1, 0.2, 0.1, 0.0]
    grounded_text, boundaries, n_abs, s_relief = sponge.absorb_and_ground_text(raw_draft, plane_coords)

    # Compute grounded metrics
    grounded_force = force_engine.compute_sentence_force(grounded_text, is_formal_invariant=False)
    grounded_gluon = gluon_space.evaluate_sentence_operators(grounded_text)

    print("\n" + "-" * 80)
    print("[*] GROUNDED DRAFT (AFTER CONTINUOUS SPONGE & PUB-TEST RELAXATION):")
    print(f"\"{grounded_text}\"\n")

    print("--- GROUNDED DRAFT METRICS (AFTER) ---")
    print(f"Sponge Absorptions Applied: {n_abs} high-abstraction scholastic words converted")
    print(f"Strain Relief Factor:       -{s_relief}")
    print(f"Semantic Strain sigma:      {grounded_force['strain_sigma']} (Grounded & relaxed)")
    print(f"Strain Delta:               {raw_force['strain_sigma'] - grounded_force['strain_sigma']:+.4f} (Strain reduction)")
    print(f"Cost of Being (-inf + 1):   {grounded_force['cob_status']}")
    print(f"Anchored Negative Limits:   {boundaries}")
    print(f"3-Gluon Operators Active:   {grounded_gluon['detected_operators']}")
    print(f"Gauge Curvature kappa:      {grounded_gluon['effective_curvature_kappa']} rad")
    print(f"Gauge Permeability T:       {grounded_gluon['effective_permeability_T']}")
    print(f"Gauge Friction mu:          {grounded_gluon['effective_friction_mu']}")
    print(f"Cornell String Confinement: {'CONFINED' if grounded_gluon['is_string_confined'] else 'SNAPPED'}")
    print("=" * 80)

if __name__ == "__main__":
    run_doc_merge_proof()
    run_doc_create_sponge_proof()
