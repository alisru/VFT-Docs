"""
rebuild_aec_first_true.py
Rebuilds aec_dictionary.json and aec_dictionary.js into a purely AEC-First Architecture:
- Primary entities are AEC Invariant Forms (Action -> Strain -> Effect)
- ZERO English lexical grammar tables (no parts of speech tables)
- Words are descriptors attached to AEC forms across the 7 planes
"""

import json
import os

V2_DIR = os.path.dirname(__file__)
SOURCE_V2_JSON = os.path.join(V2_DIR, "aec_dictionary.json")
OUTPUT_JSON = os.path.join(V2_DIR, "aec_dictionary.json")
OUTPUT_JS = os.path.join(V2_DIR, "aec_dictionary.js")

def rebuild():
    with open(SOURCE_V2_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    old_primitives = data.get("primitives", {})
    new_aec_forms = {}
    word_to_aec_index = {}

    form_counter = 1

    for key, node in old_primitives.items():
        form_id = f"AEC-{form_counter:03d}"
        form_counter += 1

        action_triad = [a.strip() for a in node.get("action", "").split(",")]
        strain_triad = [s.strip() for s in node.get("strain", "").split(",")]
        effect_triad = [e.strip() for e in node.get("effect", "").split(",")]

        primary_word = node.get("surface_words", {}).get("primary", "")
        aliases = node.get("surface_words", {}).get("aliases", [])

        # Clean plane representations
        clean_planes = {}
        planar_vocab = {f"Q{i}": [] for i in range(1, 8)}

        for q_id, p_data in node.get("planes", {}).items():
            ans = p_data.get("answer", "")
            ctx = p_data.get("word_in_context_of_plane", "")
            clean_planes[q_id] = {
                "interrogative": p_data.get("interrogative", ""),
                "dimension": p_data.get("plane", ""),
                "anchor": p_data.get("anchor", ""),
                "manifestation_answer": ans,
                "process_in_context": ctx
            }

        # Build clean AEC Form node
        aec_form_node = {
            "form_id": form_id,
            "invariant_triad": {
                "action": action_triad,
                "strain": strain_triad,
                "effect": effect_triad,
                "summary": key
            },
            "definitive_process": node.get("definitive_meaning", ""),
            "concept_type": node.get("concept_type", "genotype"),
            "topology": node.get("topology", {
                "closure_level": 0,
                "boundary_type": "open_axis",
                "operations": []
            }),
            "descriptive_words": {
                "primary_label": primary_word,
                "aliases": aliases,
                "planar_vocabulary": planar_vocab
            },
            "planes": clean_planes,
            "related_forms": node.get("related", [])
        }

        new_aec_forms[key] = aec_form_node

        # Map words to this AEC form
        if primary_word:
            word_to_aec_index[primary_word] = {
                "form_id": form_id,
                "aec_key": key,
                "role": "primary_label"
            }
        for alias in aliases:
            word_to_aec_index[alias] = {
                "form_id": form_id,
                "aec_key": key,
                "role": "alias"
            }

    rebuilt_data = {
        "metadata": {
            "version": "2.1.0",
            "architecture": "pure_aec_invariant_forms",
            "description": "True AEC-First Reality Invariant Dictionary. Primary entries are Action-Strain-Effect processes. Words are descriptive labels.",
            "total_aec_forms": len(new_aec_forms),
            "total_indexed_words": len(word_to_aec_index)
        },
        "aec_forms": new_aec_forms,
        "word_index": word_to_aec_index
    }

    # Save clean JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(rebuilt_data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # Save clean JS for CORS-free browser loading
    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write(f"// Auto-generated distribution file for Reality Classification v2 (Pure AEC Architecture)\nwindow.AEC_DICT = {json.dumps(rebuilt_data, ensure_ascii=False)};\n")

    print(f"[SUCCESS] Rebuilt {len(new_aec_forms)} Pure AEC Invariant Forms into {OUTPUT_JSON} and {OUTPUT_JS}")

if __name__ == "__main__":
    rebuild()
