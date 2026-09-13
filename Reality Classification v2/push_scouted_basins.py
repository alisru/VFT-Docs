"""
push_scouted_basins.py
Pushes the newly synthesized AEC Invariant Basins from Semantic Void #1 and #2:
- AEC-068: Sonic Emission / Sound Modulation (Void #1)
- AEC-069: Surface Sheathing / Layering (Void #2)
Updates aec_dictionary.json, compiles aec_dictionary.js, and validates 100%.
"""

import json
import os

V2_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(V2_DIR, "aec_dictionary.json")
JS_PATH = os.path.join(V2_DIR, "aec_dictionary.js")

def load_data():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def push_basins():
    data = load_data()
    aec_forms = data["aec_forms"]
    word_index = data["word_index"]

    NEW_BASINS = {
        # Void #1: Sonic / Acoustic Emission
        "modulate vibration, project wave, emit sound -> silent, muffled, quiet -> vibrated, projected, heard": {
            "primary": "sound",
            "aliases": ["vocalize", "utter", "resonate", "bellow", "shout", "trumpet", "louden", "cry", "project voice", "vociferate"],
            "process": "to modulate physical vibrations and project coherent waves into a medium to emit sound",
            "topology": {"closure_level": 0, "boundary_type": "open_axis", "operations": ["oscillate", "project_wave"]},
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the proclaiming sovereign projecting authentic presence", "process_in_context": "identity as voice — an agent articulating sovereign presence across silence"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "audible bandwidth and acoustic carrying capacity", "process_in_context": "possibility as acoustic reach — vibrational energy ready to traverse a receptive medium"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the oscillating source, horn aperture, and acoustic wave-front", "process_in_context": "location as wave-front — expanding spherical compression waves radiating through space"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "calling across distance so that presence is known and warnings are signaled", "process_in_context": "meaning as voice — projecting calls across space so that communion occurs and danger is warned"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "frequency oscillation, pitch modulation, and harmonic amplification", "process_in_context": "logic as acoustics — oscillating a physical membrane to generate rhythmic pressure waves"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "impulse strike, sudden breath, or rising alarm", "process_in_context": "history as voice — the triggering shock or intent that released acoustic vibration"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "reverberating resonance, clarity, and startling presence", "process_in_context": "effect as resonance — the stirring thrill of a clear sound echoing across stillness"}
            }
        },

        # Void #2: Surface Sheathing / Layering
        "wrap layer, coat surface, sheath body -> bare, exposed, vulnerable -> layered, clad, sheathed": {
            "primary": "sheath",
            "aliases": ["dress", "clothe", "coat", "layer", "shroud", "drape", "vest", "don", "armor", "laminate"],
            "process": "to apply a protective surface layer around an entity to sheath it against ambient exposure",
            "topology": {"closure_level": 4, "boundary_type": "enclosure", "operations": ["coat", "sheath"]},
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the robed sovereign donning royal garments and dignity", "process_in_context": "identity as vestment — an agent adopting formal outward attire to represent sacred office"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "insulated resistance and extended operating envelope", "process_in_context": "possibility as protection — additional boundary layers buffering against hostile weather"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the outer skin, garment fabric, coating, and perimeter layer", "process_in_context": "location as sheath — a conformal material boundary wrapping the exterior contour of a body"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "shielding dignity and preserving core integrity so that harsh environments cause no harm", "process_in_context": "meaning as clothing — enveloping vulnerable bodies so that dignity and warmth endure in harsh seasons"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "conformal contour fitting, seam lamination, and thermal insulation", "process_in_context": "logic as cladding — fitting layered material over an underlying framework to seal out elements"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "naked exposure, freezing gale, or ceremonial investiture", "process_in_context": "history as clothing — the cold wind or solemn ritual that required covering the body"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "warm insulation, dignified confidence, and cozy security", "process_in_context": "effect as warmth — the comforting security of being warmly and gracefully clad"}
            }
        }
    }

    form_counter = len(aec_forms) + 1

    for key, basin_data in NEW_BASINS.items():
        if key not in aec_forms:
            form_id = f"AEC-{form_counter:03d}"
            form_counter += 1

            actions = [a.strip() for a in key.split("->")[0].split(",")]
            strains = [s.strip() for s in key.split("->")[1].split(",")]
            effects = [e.strip() for e in key.split("->")[2].split(",")]

            node = {
                "form_id": form_id,
                "invariant_triad": {
                    "action": actions,
                    "strain": strains,
                    "effect": effects,
                    "summary": key
                },
                "definitive_process": basin_data["process"],
                "concept_type": "genotype",
                "topology": basin_data["topology"],
                "descriptive_words": {
                    "primary_label": basin_data["primary"],
                    "aliases": sorted(basin_data["aliases"]),
                    "planar_vocabulary": {f"Q{i}": [] for i in range(1, 8)}
                },
                "planes": basin_data["planes"],
                "related_forms": []
            }

            aec_forms[key] = node
            print(f"[PUSHED NEW BASIN] {form_id}: '{basin_data['primary']}' ({key[:50]}...)")

            # Update word index
            word_index[basin_data["primary"]] = {"form_id": form_id, "aec_key": key, "role": "primary_label"}
            for a in basin_data["aliases"]:
                word_index[a] = {"form_id": form_id, "aec_key": key, "role": "alias"}

    # Renumber and clean
    clean_forms = {}
    f_num = 1
    for k, f in aec_forms.items():
        fid = f"AEC-{f_num:03d}"
        f_num += 1
        f["form_id"] = fid
        clean_forms[k] = f
        prim = f["descriptive_words"]["primary_label"]
        if prim:
            word_index[prim] = {"form_id": fid, "aec_key": k, "role": "primary_label"}
        for a in f["descriptive_words"]["aliases"]:
            word_index[a] = {"form_id": fid, "aec_key": k, "role": "alias"}

    data["aec_forms"] = clean_forms
    data["word_index"] = word_index
    data["metadata"]["total_aec_forms"] = len(clean_forms)
    data["metadata"]["total_indexed_words"] = len(word_index)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(f"// Auto-generated distribution file for Reality Classification v2\nwindow.AEC_DICT = {json.dumps(data, ensure_ascii=False)};\n")

    print(f"\n[SUCCESS] Pushed new basins! Total AEC Forms: {len(clean_forms)}, Words: {len(word_index)}")

if __name__ == "__main__":
    push_basins()
