"""
migrate_v1_to_v2.py
Migrates the 44 calibrated entries from Reality Class'ification project/qqci_dictionary.json
into the new inverted AEC-First schema in Reality Classification v2/aec_dictionary.json.
"""

import json
import os
import re

V1_PATH = os.path.join(os.path.dirname(__file__), "..", "Reality Class'ification project", "qqci_dictionary.json")
V2_PATH = os.path.join(os.path.dirname(__file__), "aec_dictionary.json")

def format_aec_key(action: str, strain: str, effect: str) -> str:
    """Format an atomic action-strain-effect triad into a canonical primary key."""
    clean_action = action.strip()
    clean_strain = strain.strip()
    clean_effect = effect.strip()
    return f"{clean_action} -> {clean_strain} -> {clean_effect}"

def infer_topology(word: str, concept_type: str, action: str) -> dict:
    """Infer the topological closure level and boundary dynamics from the triad."""
    # Enclosures / Chambers
    if word in ["store", "shop", "library", "book", "have", "contain", "shelter"]:
        return {
            "closure_level": 4,
            "boundary_type": "enclosure",
            "operations": ["in", "hold", "out"] if word in ["store", "shop"] else ["hold", "block"]
        }
    # Open Pockets / Channels
    if word in ["hold", "catch", "cradle"]:
        return {
            "closure_level": 3,
            "boundary_type": "pocket",
            "operations": ["hold", "receive"]
        }
    # Wall / Thresholds / Crossing
    if word in ["enter", "leave", "cross", "open", "close", "give", "take"]:
        return {
            "closure_level": 1,
            "boundary_type": "wall_threshold",
            "operations": ["cross", "transfer"]
        }
    # Open Axis / Traversal / Motion
    if word in ["move", "go", "come", "rise", "fall", "live", "die", "change"]:
        return {
            "closure_level": 0,
            "boundary_type": "open_axis",
            "operations": ["displace", "ascend", "descend", "transit"]
        }
    # 0D Locus / State
    return {
        "closure_level": 0,
        "boundary_type": "locus_state",
        "operations": ["be", "know", "perceive"]
    }

def migrate():
    with open(V1_PATH, "r", encoding="utf-8") as f:
        v1_data = json.load(f)

    v1_entries = v1_data.get("entries", {})
    primitives = {}
    word_index = {}

    aec_counter = 1

    for word, entry in v1_entries.items():
        action = entry.get("action", entry.get("current", ""))
        strain = entry.get("strain", "")
        effect = entry.get("effect", entry.get("ideal", ""))
        definitive_meaning = entry.get("definitive_meaning", "")
        concept_type = entry.get("concept_type", "genotype")
        parent_word = entry.get("parent")

        aec_key = format_aec_key(action, strain, effect)
        aec_id = f"AEC-{aec_counter:03d}"
        aec_counter += 1

        topology = infer_topology(word, concept_type, action)

        primitive_node = {
            "id": aec_id,
            "action": action,
            "strain": strain,
            "effect": effect,
            "definitive_meaning": definitive_meaning,
            "concept_type": concept_type,
            "parent_word": parent_word,
            "topology": topology,
            "surface_words": {
                "primary": word,
                "aliases": [],
                "plane_manifestations": {
                    "Q1": [],
                    "Q2": [],
                    "Q3": [],
                    "Q4": [],
                    "Q5": [],
                    "Q6": [],
                    "Q7": []
                }
            },
            "parts_of_speech": entry.get("parts_of_speech", []),
            "grammar": entry.get("grammar", {}),
            "planes": entry.get("planes", {}),
            "related": entry.get("related", [])
        }

        primitives[aec_key] = primitive_node

        # Populate word index
        word_index[word] = {
            "primitive_key": aec_key,
            "primitive_id": aec_id,
            "role": "primary",
            "concept_type": concept_type
        }

    v2_data = {
        "metadata": {
            "version": "2.0.0",
            "format": "aec_first",
            "description": "QQCI Reality Classification Semantic Dictionary (AEC-First Architecture)",
            "total_primitives": len(primitives),
            "total_indexed_words": len(word_index)
        },
        "primitives": primitives,
        "word_index": word_index
    }

    with open(V2_PATH, "w", encoding="utf-8") as f:
        json.dump(v2_data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Also auto-rebuild aec_dictionary.js for CORS-free viewing
    js_path = os.path.join(os.path.dirname(V2_PATH), "aec_dictionary.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(f"// Auto-generated distribution file for Reality Classification v2\nwindow.AEC_DICT = {json.dumps(v2_data, ensure_ascii=False)};\n")

    print(f"[SUCCESS] Migrated {len(primitives)} calibrated primitives from v1 to {V2_PATH}")
    print(f"[SUCCESS] Indexed {len(word_index)} words pointing to AEC invariant keys.")

if __name__ == "__main__":
    migrate()
