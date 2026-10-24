#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word Gluon Vector Inspector (Interactive Tool)
==============================================
Inspects any English word or set of words to reveal their full
Gluon Vertex architecture and relative vector associations:

  1. Ingress Tail (Antecedent requirements B & grounding roots).
  2. Egress Head (Forward obligations F & projected consequents).
  3. 8-Modal Flux Spread around [IS] (with ASCII visual gauge bar).
  4. CEFR Linguistic & Epistemic Tier (A1 to C2).
  5. 5-Tier Relative Vector Associations:
     - Guaranteed (+W, Blue: Invariable implications)
     - Possible (+A, Green/Magenta: Operational capability)
     - Metaphorical (+L, Constructive: Structural shape / physical analogy)
     - Forbidden (-X, Red: Axiomatic impossibility / contradiction)
     - Precluded (-N/-O: Distinct negations / abandoned baselines)
  6. Pairwise Directed Gluon Bonds (Color Force, Polarity +I/-E, Coupling Magnitude g_AB).
"""

import sys
import re
import json
import math
from pathlib import Path
from collections import defaultdict, Counter

# Ensure UTF-8 output encoding across Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
DICT_PATH = BASE_DIR / "agent_grandson_lexicon" / "semantic_gluon_dictionary.json"

# Load or initialize Grandson's dictionary
def load_dictionary():
    d = {}
    if DICT_PATH.exists():
        with open(DICT_PATH, "r", encoding="utf-8") as f:
            for item in json.load(f):
                d[item["word"].lower()] = item
    return d

GLUON_DICT = load_dictionary()

# Curated semantic field map for rich vector associations
SEMANTIC_FIELD_KNOWLEDGE = {
    "gravity": {
        "cefr": "B1",
        "tail": {"evidence": True, "definition": False, "weight": 1.8},
        "head": {"proof": True, "binding": True, "weight": 2.2},
        "modal": {"is_like": 0.20, "may_be": 0.05, "can_be": 0.25, "will_be": 0.40, "is_not": 0.03, "cant_be": 0.05, "wont_be": 0.01, "was_like": 0.01},
        "guaranteed": ["mass_attraction", "spacetime_curvature", "acceleration", "geodesic_motion"],
        "possible": ["orbit_capture", "gravitational_lensing", "tidal_locking", "singularity_collapse"],
        "metaphorical": ["weight", "inevitability", "anchor", "attractor_basin", "downward_pull"],
        "forbidden": ["spontaneous_antigravity", "massless_matter", "unbounded_infinite_energy"],
        "precluded": ["levitation_without_force", "frictionless_perpetual_flight"]
    },
    "substance": {
        "cefr": "C1",
        "tail": {"evidence": False, "definition": True, "weight": 2.5},
        "head": {"proof": False, "binding": True, "weight": 3.0},
        "modal": {"is_like": 0.35, "may_be": 0.05, "can_be": 0.20, "will_be": 0.30, "is_not": 0.05, "cant_be": 0.02, "wont_be": 0.01, "was_like": 0.02},
        "guaranteed": ["ontological_independence", "substratum", "self_conception", "persistence"],
        "possible": ["infinite_attributes", "modes_of_existence", "materialization", "crystallization"],
        "metaphorical": ["bedrock", "clay", "foundation", "canvas", "prime_matter"],
        "forbidden": ["pure_nothingness", "causation_by_external_void", "split_identity"],
        "precluded": ["ephemeral_illusion", "unanchored_drift"]
    },
    "algorithm": {
        "cefr": "B2",
        "tail": {"evidence": False, "definition": True, "weight": 1.5},
        "head": {"proof": True, "binding": True, "weight": 2.8},
        "modal": {"is_like": 0.15, "may_be": 0.05, "can_be": 0.35, "will_be": 0.40, "is_not": 0.02, "cant_be": 0.02, "wont_be": 0.00, "was_like": 0.01},
        "guaranteed": ["step_determinism", "computational_rules", "finite_termination", "input_mapping"],
        "possible": ["optimization", "heuristics", "recursion", "approximation", "parallelization"],
        "metaphorical": ["recipe", "clockwork", "pipeline", "railroad", "state_machine"],
        "forbidden": ["halting_incompleteness_bypass", "magic_without_steps", "infinite_loop_proof"],
        "precluded": ["ambiguous_decree", "uncomputable_instancy"]
    },
    "freedom": {
        "cefr": "B1",
        "tail": {"evidence": False, "definition": True, "weight": 2.0},
        "head": {"proof": False, "binding": False, "weight": 2.5},
        "modal": {"is_like": 0.25, "may_be": 0.30, "can_be": 0.30, "will_be": 0.05, "is_not": 0.05, "cant_be": 0.02, "wont_be": 0.01, "was_like": 0.02},
        "guaranteed": ["absence_of_coercion", "choice_horizon", "agency", "autonomy"],
        "possible": ["self_determination", "creation", "rebellion", "error", "moral_action"],
        "metaphorical": ["open_horizon", "unbroken_chain", "winged_flight", "frictionless_plane"],
        "forbidden": ["action_without_consequence", "absolute_vacuum_existence", "causal_annihilation"],
        "precluded": ["totalitarian_lock", "involuntary_predestination"]
    },
    "entropy": {
        "cefr": "C1",
        "tail": {"evidence": True, "definition": True, "weight": 2.4},
        "head": {"proof": True, "binding": True, "weight": 3.0},
        "modal": {"is_like": 0.15, "may_be": 0.05, "can_be": 0.15, "will_be": 0.55, "is_not": 0.02, "cant_be": 0.05, "wont_be": 0.01, "was_like": 0.02},
        "guaranteed": ["disorder_growth", "heat_dissipation", "irreversibility", "microstate_dispersion"],
        "possible": ["equilibrium_state", "information_loss", "phase_transition", "thermal_death"],
        "metaphorical": ["arrow_of_time", "decay", "rust", "dissolution", "noise"],
        "forbidden": ["perpetual_motion_second_kind", "spontaneous_systemic_cooldown", "reversal_without_work"],
        "precluded": ["absolute_zero_dissipation", "static_perfection"]
    },
    "zero": {
        "cefr": "A1",
        "tail": {"evidence": False, "definition": True, "weight": 1.0},
        "head": {"proof": False, "binding": True, "weight": 2.5},
        "modal": {"is_like": 0.30, "may_be": 0.05, "can_be": 0.25, "will_be": 0.25, "is_not": 0.05, "cant_be": 0.08, "wont_be": 0.01, "was_like": 0.01},
        "guaranteed": ["additive_identity", "null_state", "origin_coordinate", "boundary_threshold"],
        "possible": ["infinitesimal_limit", "absorber_element", "algebraic_root", "potential_field"],
        "metaphorical": ["void", "mirror", "calm_water", "fulcrum", "ground_zero"],
        "forbidden": ["division_in_field", "distinct_positive_value", "magnitude_without_sign"],
        "precluded": ["indeterminate_chaos_without_definition"]
    },
    "paradox": {
        "cefr": "B2",
        "tail": {"evidence": True, "definition": True, "weight": 2.2},
        "head": {"proof": True, "binding": False, "weight": 2.8},
        "modal": {"is_like": 0.10, "may_be": 0.15, "can_be": 0.10, "will_be": 0.05, "is_not": 0.25, "cant_be": 0.30, "wont_be": 0.03, "was_like": 0.02},
        "guaranteed": ["self_contradiction", "antinomy", "premise_clash", "axiom_fracture"],
        "possible": ["epistemic_breakthrough", "Gödelian_incompleteness", "category_redefinition"],
        "metaphorical": ["ouroboros", "knot", "short_circuit", "mirrored_chasm"],
        "forbidden": ["classical_consistency", "trivial_linear_resolution"],
        "precluded": ["unbroken_syllogism"]
    },
    "consciousness": {
        "cefr": "B2",
        "tail": {"evidence": False, "definition": False, "weight": 2.5},
        "head": {"proof": False, "binding": False, "weight": 3.0},
        "modal": {"is_like": 0.40, "may_be": 0.30, "can_be": 0.20, "will_be": 0.05, "is_not": 0.02, "cant_be": 0.01, "wont_be": 0.01, "was_like": 0.01},
        "guaranteed": ["subjective_experience", "observer_state", "intentionality", "qualia"],
        "possible": ["self_reflection", "model_building", "agency", "recursive_inversion"],
        "metaphorical": ["inner_light", "stage", "stream", "lens", "internal_mirror"],
        "forbidden": ["pure_objective_reductionism_without_remainder", "mechanistic_unconscious_mind"],
        "precluded": ["inert_blindness"]
    },
    "quantum": {
        "cefr": "C1",
        "tail": {"evidence": True, "definition": True, "weight": 2.6},
        "head": {"proof": True, "binding": True, "weight": 3.2},
        "modal": {"is_like": 0.15, "may_be": 0.35, "can_be": 0.30, "will_be": 0.10, "is_not": 0.03, "cant_be": 0.05, "wont_be": 0.01, "was_like": 0.01},
        "guaranteed": ["wavefunction_superposition", "discreteness", "nonlocality", "phase_coherence"],
        "possible": ["entanglement_swapping", "tunneling", "decoherence", "interference_pattern"],
        "metaphorical": ["dice_roll", "ghostly_smear", "resonance_ripple", "unseen_cat"],
        "forbidden": ["classical_local_realism", "simultaneous_precise_conjugates", "deterministic_trajectory"],
        "precluded": ["continuous_sub_planck_radiation"]
    },
    "whale": {
        "cefr": "A2",
        "tail": {"evidence": True, "definition": False, "weight": 1.2},
        "head": {"proof": False, "binding": False, "weight": 1.4},
        "modal": {"is_like": 0.30, "may_be": 0.10, "can_be": 0.25, "will_be": 0.25, "is_not": 0.05, "cant_be": 0.03, "wont_be": 0.01, "was_like": 0.01},
        "guaranteed": ["mammalian_biology", "oceanic_habitat", "lung_respiration", "finite_biomass"],
        "possible": ["deep_echolocation", "transoceanic_migration", "breaching", "song_transmission"],
        "metaphorical": ["leviathan", "submerged_giant", "ancient_monarch", "deep_depths_beacon"],
        "forbidden": ["gill_respiration", "terrestrial_locomotion", "weightless_flight"],
        "precluded": ["cold_blooded_reptilian_torpor"]
    },
    "whisper": {
        "cefr": "B1",
        "tail": {"evidence": True, "definition": False, "weight": 1.3},
        "head": {"proof": False, "binding": False, "weight": 1.5},
        "modal": {"is_like": 0.35, "may_be": 0.25, "can_be": 0.25, "will_be": 0.05, "is_not": 0.05, "cant_be": 0.03, "wont_be": 0.01, "was_like": 0.01},
        "guaranteed": ["sub-vocal_acoustic_vibration", "low_amplitude", "attenuated_pressure_wave", "proximity_requirement"],
        "possible": ["intimate_disclosure", "conspiracy", "subtle_misinterpretation", "secret_diffusion"],
        "metaphorical": ["rustling_leaves", "breath_of_wind", "shadow_voice", "covert_rumor"],
        "forbidden": ["acoustic_deafening_explosion", "unmediated_global_broadcast"],
        "precluded": ["stentorian_shout"]
    },
    "justice": {
        "cefr": "B2",
        "tail": {"evidence": True, "definition": True, "weight": 2.5},
        "head": {"proof": True, "binding": True, "weight": 3.0},
        "modal": {"is_like": 0.20, "may_be": 0.10, "can_be": 0.25, "will_be": 0.35, "is_not": 0.05, "cant_be": 0.03, "wont_be": 0.01, "was_like": 0.01},
        "guaranteed": ["normative_rectification", "proportional_balance", "impartial_reciprocity", "due_process"],
        "possible": ["restitution", "retributive_sentence", "institutional_reform", "amnesty"],
        "metaphorical": ["blindfolded_scales", "straight_level", "unflinching_sword", "moral_fulcrum"],
        "forbidden": ["arbitrary_tyranny_without_cause", "whimsical_disproportion", "privilege_immunity"],
        "precluded": ["blood_feud_anarchy"]
    },
    "revolution": {
        "cefr": "B2",
        "tail": {"evidence": True, "definition": True, "weight": 2.4},
        "head": {"proof": True, "binding": True, "weight": 3.1},
        "modal": {"is_like": 0.25, "may_be": 0.15, "can_be": 0.25, "will_be": 0.25, "is_not": 0.05, "cant_be": 0.03, "wont_be": 0.01, "was_like": 0.01},
        "guaranteed": ["regime_rupture", "structural_inversion", "legitimacy_collapse", "accelerated_transformation"],
        "possible": ["institutional_rebuilding", "civil_strife", "ideological_purging", "paradigm_shift"],
        "metaphorical": ["storm", "turning_wheel", "erupting_volcano", "fever_break"],
        "forbidden": ["unbroken_linear_status_quo", "frictionless_universal_agreement"],
        "precluded": ["static_complacency"]
    },
    "fire": {
        "cefr": "A1",
        "tail": {"evidence": True, "definition": False, "weight": 1.4},
        "head": {"proof": False, "binding": True, "weight": 2.2},
        "modal": {"is_like": 0.25, "may_be": 0.05, "can_be": 0.25, "will_be": 0.40, "is_not": 0.02, "cant_be": 0.02, "wont_be": 0.00, "was_like": 0.01},
        "guaranteed": ["rapid_oxidation", "thermal_emission", "combustion_plasma", "fuel_consumption"],
        "possible": ["wildfire_spread", "containment", "metallurgical_smelting", "smoke_asphyxiation"],
        "metaphorical": ["passion", "promethean_spark", "purifying_flame", "unbridled_wrath"],
        "forbidden": ["combustion_without_oxidizer_or_fuel", "cold_ash_flame", "endothermic_spontaneous_blaze"],
        "precluded": ["incombustible_freezing_burn"]
    }
}


def induce_word_gluon_profile(word: str) -> dict:
    w = word.lower().strip()
    if w in SEMANTIC_FIELD_KNOWLEDGE:
        return {**SEMANTIC_FIELD_KNOWLEDGE[w], "word": w}

    if w in GLUON_DICT:
        d_entry = GLUON_DICT[w]
        return {
            "word": w,
            "cefr": d_entry.get("cefr", "B1"),
            "tail": d_entry.get("tail_ingress", {"weight": 1.5, "evidence": False}),
            "head": d_entry.get("head_egress", {"weight": 1.5, "proof": False}),
            "modal": d_entry.get("modal_spread", {}),
            "guaranteed": d_entry.get("relative_vectors", {}).get("guaranteed", [f"invariant_{w}"]),
            "possible": d_entry.get("relative_vectors", {}).get("possible", [f"action_{w}"]),
            "metaphorical": d_entry.get("relative_vectors", {}).get("metaphorical", [f"model_{w}"]),
            "forbidden": d_entry.get("relative_vectors", {}).get("forbidden", [f"anti_{w}"]),
            "precluded": d_entry.get("relative_vectors", {}).get("precluded", [f"negation_{w}"])
        }

    # Dynamic Morphological Induction for any random unseen word
    length = len(w)
    cefr = "A2" if length <= 4 else ("B1" if length <= 7 else ("B2" if length <= 10 else "C1"))

    is_action = w.endswith("ing") or w.endswith("ize") or w.endswith("ate")
    is_state = w.endswith("tion") or w.endswith("ity") or w.endswith("ness") or w.endswith("ism")
    is_neg = w.startswith("un") or w.startswith("dis") or w.startswith("non") or w.startswith("in")

    spread = {
        "is_like": 0.30 if is_state else 0.15,
        "may_be": 0.25 if w.endswith("able") else 0.15,
        "can_be": 0.35 if is_action else 0.15,
        "will_be": 0.30 if length > 9 else 0.15,
        "is_not": 0.35 if is_neg else 0.05,
        "cant_be": 0.30 if (is_neg and length > 7) else 0.05,
        "wont_be": 0.05,
        "was_like": 0.25 if w.endswith("ed") else 0.05
    }
    tot = sum(spread.values()) or 1.0
    norm_spread = {k: round(v / tot, 3) for k, v in spread.items()}

    return {
        "word": w,
        "cefr": cefr,
        "tail": {"evidence": length > 8, "definition": length > 6, "weight": round(1.0 + length / 7.0, 1)},
        "head": {"proof": is_action or length > 8, "binding": True, "weight": round(1.0 + length / 6.0, 1)},
        "modal": norm_spread,
        "guaranteed": [f"essential_{w}_principle", f"structural_{w}"],
        "possible": [f"operational_{w}_behavior", f"contextual_{w}"],
        "metaphorical": [f"pattern_of_{w}", f"analog_{w}"],
        "forbidden": [f"annihilation_of_{w}", f"contradictory_{w}"],
        "precluded": [f"negated_{w}", f"opposite_of_{w}"]
    }


def render_modal_gauge_bar(spread: dict) -> str:
    # 8-Modal Visual Dispersion Gauge
    keys = ["will_be", "can_be", "is_like", "may_be", "is_not", "cant_be", "wont_be", "was_like"]
    labels = ["+W", "+A", "+L", "+M", "-N", "-X", "-O", "-H"]
    bar_parts = []
    for k, lbl in zip(keys, labels):
        val = spread.get(k, 0.0)
        ticks = int(val * 15)
        bar_parts.append(f"{lbl}:{val:.2f} [{'#' * ticks}{'.' * (15 - ticks)}]")
    return " | ".join(bar_parts[:4]) + "\n        " + " | ".join(bar_parts[4:])


def compute_pairwise_gluon_bond(word_a: str, word_b: str) -> dict:
    prof_a = induce_word_gluon_profile(word_a)
    prof_b = induce_word_gluon_profile(word_b)

    # Ingress Tail to Egress Head compatibility
    # A_head -> B_tail: does A obligate what B requires?
    head_a = prof_a["head"]["weight"]
    tail_b = prof_b["tail"]["weight"]
    head_b = prof_b["head"]["weight"]
    tail_a = prof_a["tail"]["weight"]

    forward_flow = round(min(head_a, tail_b), 2)
    backward_flow = round(min(head_b, tail_a), 2)

    # Color Force Determination
    # Red: will_be <-> cant_be (Paradigm opposition)
    # Green: can_be <-> is_not (Reality check / testing)
    # Blue: will_be <-> may_be (Proof / realization cascade)
    # Magenta: is_like <-> can_be (Metaphor to operator)
    red_charge = prof_a["modal"].get("will_be", 0.1) * prof_b["modal"].get("cant_be", 0.1) + prof_b["modal"].get("will_be", 0.1) * prof_a["modal"].get("cant_be", 0.1)
    green_charge = prof_a["modal"].get("can_be", 0.1) * prof_b["modal"].get("is_not", 0.1) + prof_b["modal"].get("can_be", 0.1) * prof_a["modal"].get("is_not", 0.1)
    blue_charge = prof_a["modal"].get("will_be", 0.1) * prof_b["modal"].get("may_be", 0.1) + prof_b["modal"].get("will_be", 0.1) * prof_a["modal"].get("may_be", 0.1)
    magenta_charge = prof_a["modal"].get("is_like", 0.1) * prof_b["modal"].get("can_be", 0.1) + prof_b["modal"].get("is_like", 0.1) * prof_a["modal"].get("can_be", 0.1)

    colors = {
        "🔴 Red (Opposition / Clash)": red_charge,
        "🟢 Green (Testing / Boundary)": green_charge,
        "🔵 Blue (Deductive / Proof)": blue_charge,
        "🟣 Magenta (Model / Isomorphism)": magenta_charge
    }
    dominant_color = max(colors.items(), key=lambda x: x[1])[0]

    # Polarity & Possibility Spectrum
    # Check if B is in A's forbidden or precluded list
    is_forbidden = any(word_b in f for f in prof_a["forbidden"]) or any(word_a in f for f in prof_b["forbidden"])
    is_guaranteed = any(word_b in g for g in prof_a["guaranteed"]) or any(word_a in g for g in prof_b["guaranteed"])
    is_metaphor = any(word_b in m for m in prof_a["metaphorical"]) or any(word_a in m for m in prof_b["metaphorical"])

    if is_forbidden or red_charge > 0.15:
        tier = "1_Impossible (Forbidden Gauge State)"
        polarity = "-E (Exclusion)"
    elif is_guaranteed:
        tier = "5_Certain (Invariable Implication)"
        polarity = "+I (Inclusion)"
    elif blue_charge > green_charge and blue_charge > 0.05:
        tier = "4_Probable (Convergent Bond)"
        polarity = "+I (Inclusion)"
    elif is_metaphor or magenta_charge > 0.05:
        tier = "3_Plausible (Structural Analogy)"
        polarity = "+I (Inclusion)"
    else:
        tier = "2_Improbable (Weak Coupling)"
        polarity = "Neutral"

    coupling_magnitude = round(math.sqrt(head_a * tail_b + head_b * tail_a), 2)

    return {
        "pair": f"{word_a} <===> {word_b}",
        "dominant_color_force": dominant_color,
        "polarity": polarity,
        "coupling_magnitude": coupling_magnitude,
        "possibility_tier": tier,
        "directed_flows": {
            f"{word_a}(Head) -> {word_b}(Tail)": forward_flow,
            f"{word_b}(Head) -> {word_a}(Tail)": backward_flow
        }
    }


def inspect_words(words: list):
    print("=" * 110)
    print(f"WORD GLUON VECTOR INSPECTOR — ANALYZING {len(words)} WORD(S)")
    print("=" * 110)

    profiles = {}
    for w in words:
        prof = induce_word_gluon_profile(w)
        profiles[w] = prof

        print(f"\n[GLUON VERTEX]: '{w.upper()}' (CEFR: {prof['cefr']})")
        print(f"  Ingress Tail  (B requirements): Weight={prof['tail']['weight']} | Prior Evidence Required: {prof['tail'].get('evidence', False)}")
        print(f"  Egress Head   (F obligations) : Weight={prof['head']['weight']} | Downstream Proof Obligated: {prof['head'].get('proof', False)}")
        print(f"  Modal Spread around [IS]:\n        {render_modal_gauge_bar(prof['modal'])}")
        print(f"  5-Tier Relative Vector Associations:")
        print(f"    🔵 Guaranteed  (+W): {', '.join(prof['guaranteed'][:4])}")
        print(f"    🟢 Possible    (+A): {', '.join(prof['possible'][:4])}")
        print(f"    🟣 Metaphorical(+L): {', '.join(prof['metaphorical'][:4])}")
        print(f"    🔴 Forbidden   (-X): {', '.join(prof['forbidden'][:4])}")
        print(f"    ⚪ Precluded   (-N): {', '.join(prof['precluded'][:4])}")

    if len(words) >= 2:
        print("\n" + "=" * 110)
        print("PAIRWISE DIRECTED GLUON BONDS ACROSS THE FIELD")
        print("=" * 110)
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                bond = compute_pairwise_gluon_bond(words[i], words[j])
                print(f"\n-> BOND: {bond['pair']}")
                print(f"   Color Force:        {bond['dominant_color_force']}")
                print(f"   Polarity:           {bond['polarity']} | Magnitude: {bond['coupling_magnitude']}")
                print(f"   Possibility Tier:   {bond['possibility_tier']}")
                for direction, flow in bond['directed_flows'].items():
                    print(f"   Flow: {direction:<28} = {flow}")

    print("\n" + "=" * 110)


def main():
    if len(sys.argv) > 1:
        target_words = sys.argv[1:]
    else:
        # Default diverse multi-genre demonstration words
        target_words = ["gravity", "freedom", "algorithm", "entropy", "paradox"]

    inspect_words(target_words)


if __name__ == "__main__":
    main()
