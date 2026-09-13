"""
validate_v2.py
Comprehensive automated validator for Reality Classification v2 (Pure AEC-First Architecture).
Audits schema integrity, 1-to-1 lockstep, plane-collapse ban, topological closure,
and word index coherence.
"""

import json
import os
import re

V2_DIR = os.path.dirname(__file__)
AEC_DICT_PATH = os.path.join(V2_DIR, "aec_dictionary.json")

BANNED_JARGON = [
    "entropy", "state-matrix", "taxonomic", "o(1)", "latent capacity",
    "temporal horizon", "spatial partition", "ontological", "subjective awareness",
    "classification protocol", "biochemical", "glycolysis", "atp", "asphyxiation",
    "teleological", "valence", "transduction", "mitosis", "lysis", "karmic",
    "sensory overload", "fluidic", "indeterminacy", "delimit", "hypothermia",
    "restorative justice", "cohesion protocols", "cellular metabolism", "caloric",
    "dissociation", "metabolic"
]

BANNED_ROOT_PLANE_COLLAPSE = [
    "physical", "mental", "emotional", "biological", "historical", "social", "logical",
    "brain", "skull", "mouth", "eyeball", "computer"
]

PLANES = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7"]
PURPOSE_MARKERS = ["so that", "in order to", "in order that", "so as to", "so people can", "so you can", "to prevent", "preventing "]

def validate():
    with open(AEC_DICT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    aec_forms = data.get("aec_forms", {})
    word_index = data.get("word_index", {})

    print(f"Auditing Reality Classification v2 (Pure AEC-First Invariant Architecture)...")
    print(f"Total AEC Invariant Forms: {len(aec_forms)} | Total Mapped Words: {len(word_index)}\n")

    total_errors = 0

    for aec_key, node in aec_forms.items():
        errs = []
        form_id = node.get("form_id", "UNKNOWN_ID")
        triad = node.get("invariant_triad", {})
        actions = triad.get("action", [])
        strains = triad.get("strain", [])
        effects = triad.get("effect", [])

        # 1. Triad Structure Check
        if len(actions) != 3 or len(strains) != 3 or len(effects) != 3:
            errs.append(f"Triad count error: actions={len(actions)}, strains={len(strains)}, effects={len(effects)}")

        # 2. Key Match
        expected_key = f"{', '.join(actions)} -> {', '.join(strains)} -> {', '.join(effects)}"
        if aec_key != expected_key:
            errs.append(f"Key mismatch: '{aec_key}' != '{expected_key}'")

        # 3. Plane-Collapse Check on Root
        root_text = f"{' '.join(actions)} {' '.join(strains)} {' '.join(effects)} {node.get('definitive_process', '')}".lower()
        for banned in BANNED_ROOT_PLANE_COLLAPSE:
            if re.search(r'\b' + re.escape(banned) + r'\b', root_text):
                errs.append(f"Root contains plane-collapsing word: '{banned}'")

        # 4. Banned Jargon Check across node
        node_text = json.dumps(node, ensure_ascii=False).lower()
        for j in BANNED_JARGON:
            if re.search(r'\b' + re.escape(j) + r'\b', node_text):
                errs.append(f"Contains banned jargon: '{j}'")

        # 5. Topology Checks
        topo = node.get("topology", {})
        if "closure_level" not in topo or "boundary_type" not in topo:
            errs.append("Missing topology closure_level or boundary_type")

        # 6. Planes Check
        node_planes = node.get("planes", {})
        for p in PLANES:
            if p not in node_planes:
                errs.append(f"Missing plane {p}")
            else:
                p_obj = node_planes[p]
                ans = p_obj.get("manifestation_answer", "")
                ctx = p_obj.get("process_in_context", "")
                if not ans or not ctx:
                    errs.append(f"Plane {p} missing answer or context")
                
                # Check purposive bleed in non-Q4
                if p != "Q4":
                    for pm in PURPOSE_MARKERS:
                        if pm in ctx.lower():
                            errs.append(f"Plane {p} contains purpose clause '{pm}' (allowed in Q4 only)")

        if errs:
            total_errors += len(errs)
            print(f"[FAIL] {form_id} ({aec_key}):")
            for e in errs:
                print(f"   - {e}")

    # 7. Word Index Integrity Check
    index_errs = []
    for word, mapping in word_index.items():
        prim_key = mapping.get("aec_key")
        prim_id = mapping.get("form_id")
        if prim_key not in aec_forms:
            index_errs.append(f"Word '{word}' maps to nonexistent AEC key '{prim_key}'")
        elif aec_forms[prim_key]["form_id"] != prim_id:
            index_errs.append(f"Word '{word}' ID mismatch: mapping has '{prim_id}', form has '{aec_forms[prim_key]['form_id']}'")

    if index_errs:
        total_errors += len(index_errs)
        print("\n[FAIL] Word Index Errors:")
        for ie in index_errs:
            print(f"   - {ie}")

    print("-" * 60)
    if total_errors == 0:
        print(f"[SUCCESS] 100% PASS! All {len(aec_forms)} Pure AEC Invariant Forms and {len(word_index)} mapped words conform to v2 invariants!")
    else:
        print(f"[FAILED] Found {total_errors} total errors.")

if __name__ == "__main__":
    validate()
