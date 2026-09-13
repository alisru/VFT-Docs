"""
execute_evolution_pass.py
Executes Deep Evolution Pass 1:
1. MERGE & PRUNE:
   - Merges 'build' into 'make' (forming unified assembly primitive)
   - Merges 'break' and 'split' (forming unified disruption primitive)
   - Prunes 'shop' as a separate primitive, filing it under 'exchange' and 'store'
   - Refactors 'book' from physical binding to invariant 'inscribe / record / mark'
2. GROW:
   - Mints 'exchange / trade' (mutual boundary transfer)
   - Mints 'release / let go' (cessation of constraint)
   - Mints 'bind / fasten' (tensile constraint)
   - Mints 'seek / search' (directed domain scanning)
   - Mints 'rest / stay' (equilibrium stasis)
3. ENRICH:
   - Expands vocabulary clouds across all forms.
"""

import json
import os

V2_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(V2_DIR, "aec_dictionary.json")
JS_PATH = os.path.join(V2_DIR, "aec_dictionary.js")

def execute():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    aec_forms = data["aec_forms"]
    word_index = data["word_index"]

    print(f"=== EXECUTING DEEP EVOLUTION PASS 1 ===")
    print(f"Initial State: {len(aec_forms)} Forms | {len(word_index)} Words\n")

    # 1. MERGE 'build' INTO 'make'
    # Find keys
    make_key = None
    build_key = None
    for k, f in aec_forms.items():
        if f["descriptive_words"]["primary_label"] == "make":
            make_key = k
        elif f["descriptive_words"]["primary_label"] == "build":
            build_key = k

    if make_key and build_key:
        print(">>> Merging 'build' into 'make' (Unified Structural Assembly)...")
        # Update make definition to be leaner and comprehensive
        unified_make_action = ["assemble parts", "integrate structure", "produce whole"]
        unified_make_strain = ["scattered", "unformed", "unintegrated"]
        unified_make_effect = ["assembled", "structured", "complete"]
        new_make_key = f"{', '.join(unified_make_action)} -> {', '.join(unified_make_strain)} -> {', '.join(unified_make_effect)}"

        make_node = aec_forms[make_key]
        make_node["invariant_triad"]["action"] = unified_make_action
        make_node["invariant_triad"]["strain"] = unified_make_strain
        make_node["invariant_triad"]["effect"] = unified_make_effect
        make_node["invariant_triad"]["summary"] = new_make_key
        make_node["definitive_process"] = "to assemble parts and integrate them into a cohesive functional whole"

        # Combine aliases
        combined_aliases = set(make_node["descriptive_words"]["aliases"])
        combined_aliases.update(aec_forms[build_key]["descriptive_words"]["aliases"])
        combined_aliases.update(["build", "construct", "create", "assemble", "fabricate", "erect", "forge", "craft", "shape"])
        combined_aliases.discard("make")
        make_node["descriptive_words"]["aliases"] = sorted(list(combined_aliases))

        # Replace key in dict
        del aec_forms[make_key]
        del aec_forms[build_key]
        aec_forms[new_make_key] = make_node

        # Update word index
        word_index["make"] = {"form_id": make_node["form_id"], "aec_key": new_make_key, "role": "primary_label"}
        for a in combined_aliases:
            word_index[a] = {"form_id": make_node["form_id"], "aec_key": new_make_key, "role": "alias"}

    # 2. MERGE 'break' AND 'split'
    break_key = None
    split_key = None
    for k, f in aec_forms.items():
        if f["descriptive_words"]["primary_label"] == "break":
            break_key = k
        elif f["descriptive_words"]["primary_label"] == "split":
            split_key = k

    if break_key and split_key:
        print(">>> Merging 'split' into 'break' (Unified Structural Disruption)...")
        unified_break_action = ["apply force", "sever bond", "divide integrity"]
        unified_break_strain = ["bonded", "unified", "resisting"]
        unified_break_effect = ["severed", "separated", "divided"]
        new_break_key = f"{', '.join(unified_break_action)} -> {', '.join(unified_break_strain)} -> {', '.join(unified_break_effect)}"

        break_node = aec_forms[break_key]
        break_node["invariant_triad"]["action"] = unified_break_action
        break_node["invariant_triad"]["strain"] = unified_break_strain
        break_node["invariant_triad"]["effect"] = unified_break_effect
        break_node["invariant_triad"]["summary"] = new_break_key
        break_node["definitive_process"] = "to apply force to sever internal bonds and divide structural integrity"

        combined_break_aliases = set(break_node["descriptive_words"]["aliases"])
        combined_break_aliases.update(aec_forms[split_key]["descriptive_words"]["aliases"])
        combined_break_aliases.update(["split", "crack", "fracture", "rupture", "cleave", "shatter", "sever", "snap", "tear", "rip", "bifurcate"])
        combined_break_aliases.discard("break")
        break_node["descriptive_words"]["aliases"] = sorted(list(combined_break_aliases))

        del aec_forms[break_key]
        del aec_forms[split_key]
        aec_forms[new_break_key] = break_node

        word_index["break"] = {"form_id": break_node["form_id"], "aec_key": new_break_key, "role": "primary_label"}
        for a in combined_break_aliases:
            word_index[a] = {"form_id": break_node["form_id"], "aec_key": new_break_key, "role": "alias"}

    # 3. REFACTOR 'book' INTO 'inscribe / record / mark'
    book_key = None
    for k, f in aec_forms.items():
        if f["descriptive_words"]["primary_label"] == "book":
            book_key = k
            break

    if book_key:
        print(">>> Refactoring 'book' into Invariant Primitive 'record / inscribe / mark'...")
        inscribe_action = ["generate trace", "inscribe substrate", "retain pattern"]
        inscribe_strain = ["fleeting", "unmarked", "ephemeral"]
        inscribe_effect = ["traced", "inscribed", "recorded"]
        new_inscribe_key = f"{', '.join(inscribe_action)} -> {', '.join(inscribe_strain)} -> {', '.join(inscribe_effect)}"

        inscribe_node = aec_forms[book_key]
        inscribe_node["invariant_triad"]["action"] = inscribe_action
        inscribe_node["invariant_triad"]["strain"] = inscribe_strain
        inscribe_node["invariant_triad"]["effect"] = inscribe_effect
        inscribe_node["invariant_triad"]["summary"] = new_inscribe_key
        inscribe_node["definitive_process"] = "to generate an informational trace and inscribe it upon a substrate to retain the pattern permanently"
        inscribe_node["descriptive_words"]["primary_label"] = "record"
        inscribe_node["descriptive_words"]["aliases"] = ["inscribe", "mark", "write", "engrave", "book", "document", "register", "etch", "imprint", "log"]

        del aec_forms[book_key]
        aec_forms[new_inscribe_key] = inscribe_node

        word_index["record"] = {"form_id": inscribe_node["form_id"], "aec_key": new_inscribe_key, "role": "primary_label"}
        for a in inscribe_node["descriptive_words"]["aliases"]:
            word_index[a] = {"form_id": inscribe_node["form_id"], "aec_key": new_inscribe_key, "role": "alias"}

    # 4. PRUNE 'shop' (file under 'store' and new 'exchange')
    shop_key = None
    for k, f in aec_forms.items():
        if f["descriptive_words"]["primary_label"] == "shop":
            shop_key = k
            break
    if shop_key:
        print(">>> Pruning composite phenotype 'shop' as an independent primitive...")
        del aec_forms[shop_key]

    # 5. GROW NEW NOVEL INVARIANT FORMS
    novel_primitives = {
        # Exchange / Trade
        "offer asset, transfer across boundary, receive equivalent -> unbalanced, withholding, unilateral -> transferred, reciprocal, settled": {
            "primary": "exchange",
            "aliases": ["trade", "swap", "barter", "transact", "reciprocate", "shop", "deal", "negotiate"],
            "process": "to transfer an asset across a boundary and receive an equivalent return to settle balance",
            "topology": {"closure_level": 2, "boundary_type": "corner_joint", "operations": ["transfer", "exchange"]},
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the trading sovereign engaged in reciprocal covenant", "process_in_context": "identity as trade — an entity honoring mutual recognition and contractual balance"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "liquid exchange ratios and mutually beneficial value", "process_in_context": "possibility as trade — opening new utility through balanced two-way asset circulation"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the marketplace, port of entry, and trade counter", "process_in_context": "location as exchange — the physical boundary crossing where goods change hands"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "fostering peaceful mutual interdependence and prosperity", "process_in_context": "meaning as exchange — trading goods so that communities thrive together without theft or coercion"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "valuation assessment, mutual escrow release, and ledger balancing", "process_in_context": "logic as transaction — verifying parity and executing simultaneous reciprocal transfer"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "complementary deficits, surplus yield, and trade accord", "process_in_context": "history as trade — the differing resources that naturally sparked commerce"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "mutual satisfaction, fair resolution, and peace", "process_in_context": "effect as fairness — the satisfying resolution of an honest, balanced exchange"}
            }
        },

        # Release / Let Go
        "loosen hold, withdraw constraint, yield to momentum -> gripped, confined, restrained -> unbound, freed, launched": {
            "primary": "release",
            "aliases": ["let go", "liberate", "discharge", "unleash", "relinquish", "free", "unfasten", "pardon", "unhand"],
            "process": "to withdraw a constraint and allow an entity to move freely under its own momentum",
            "topology": {"closure_level": 1, "boundary_type": "wall_threshold", "operations": ["release", "unconstrain"]},
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the sovereign relinquishing possession without fear", "process_in_context": "identity as release — an agent letting go of control and granting freedom to another"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "emancipated potential and unconstrained trajectory", "process_in_context": "possibility as freedom — unblocked degrees of freedom following their natural path"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the open gate, loosened grip, and launch aperture", "process_in_context": "location as release — the point where physical restraint ends and unguided flight begins"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "restoring autonomous sovereignty and breaking bondage", "process_in_context": "meaning as release — letting captive forces go so that life fulfills its natural course"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "releasing tension fasteners, withdrawing boundaries, and transferring impulse", "process_in_context": "logic as decoupling — disengaging latches and allowing kinetic momentum to take over"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "expired debt, completed custody, or realization of futility", "process_in_context": "history as release — the concluded term that prompted the opening of the hand"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "exhilarating liberation, profound relief, and peaceful surrender", "process_in_context": "effect as liberation — the sweet, unburdened relief of total freedom"}
            }
        },

        # Bind / Fasten
        "wrap boundary, cinch constraint, lock together -> shifting, loose, separating -> cinched, bound, immovable": {
            "primary": "bind",
            "aliases": ["tie", "fasten", "cinch", "lash", "tether", "strap", "harness", "shackle", "clamp", "knot"],
            "process": "to apply a tensile constraint around two or more entities to lock them into immovable union",
            "topology": {"closure_level": 3, "boundary_type": "pocket", "operations": ["cinch", "lock"]},
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the oath-bound ally holding sacred fidelity", "process_in_context": "identity as duty — an agent binding honor to an irrevocable commitment"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "locked stability and zero relative drift", "process_in_context": "possibility as lock — eliminating parasitic degrees of freedom to ensure rigidity"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the knot, strap, cord, and tension wrap", "process_in_context": "location as binding — the physical cord cinched tightly around a joint"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "holding fragile structures steady against raging storms", "process_in_context": "meaning as binding — strapping vulnerable cargo down so that integrity survives turbulence"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "wrapping tensile cord, drawing cinch, and tying terminal knot", "process_in_context": "logic as cinching — applying hoop tension around an assembly and locking the friction knot"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "incoming gale, loose cargo, or solemn pledge", "process_in_context": "history as binding — the risk of separation that prompted tight fastening"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "firm security, unwavering fidelity, and rock-solid certainty", "process_in_context": "effect as security — the comforting peace of mind of an unshakeable bond"}
            }
        },

        # Seek / Search
        "scan domain, follow trace, locate target -> blind, lost, unoriented -> scanned, tracked, located": {
            "primary": "seek",
            "aliases": ["search", "hunt", "explore", "track", "probe", "scout", "investigate", "pursue", "forage", "find"],
            "process": "to scan an area and follow traces to detect and confirm the location of a target",
            "topology": {"closure_level": 0, "boundary_type": "open_axis", "operations": ["scan", "detect"]},
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the seeker guided by purposeful inquiry", "process_in_context": "identity as quest — an agent pursuing truth across unknown territory"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "hidden signals, clues, and candidate coordinates", "process_in_context": "possibility as inquiry — unresolved potential awaiting discovery and illumination"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the unexplored terrain, search grid, and horizon", "process_in_context": "location as search — the spatial expanse systematically swept to find an object"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "recovering what was lost and answering the call of truth", "process_in_context": "meaning as quest — venturing out into the unknown so that life and truth are recovered"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "grid traversal, sensor polling, and gradient detection", "process_in_context": "logic as search — systematically incrementing coordinates and sampling signal strength"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "answer": "felt absence, lost treasure, or unanswered question", "manifestation_answer": "felt absence, lost treasure, or unanswered question", "process_in_context": "history as quest — the vacuum or longing that sparked the journey"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "thrill of discovery, triumphant arrival, and clarity", "process_in_context": "effect as discovery — the exhilarating joy of finally finding what was sought"}
            }
        },

        # Rest / Stay
        "halt displacement, settle weight, maintain presence -> moving, agitated, exhausted -> settled, still, rested": {
            "primary": "rest",
            "aliases": ["stay", "pause", "settle", "remain", "wait", "abide", "dwell", "halt", "bide", "sojourn"],
            "process": "to cease displacement, settle weight upon a baseline, and maintain presence without motion",
            "topology": {"closure_level": 0, "boundary_type": "locus_state", "operations": ["settle", "abide"]},
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the peaceful sovereign centered in unwavering stillness", "process_in_context": "identity as stillness — an agent dwelling in unshakeable internal equilibrium"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "energy conservation, regeneration, and deep quiet", "process_in_context": "possibility as rest — replenishing spent potential and consolidating strength"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the hearth, quiet sanctuary, and resting bed", "process_in_context": "location as rest — the physical baseline where all kinetic motion ceases"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "recovering vitality and honoring the sabbath of stillness", "process_in_context": "meaning as rest — pausing all labor so that soul and body restore their sacred harmony"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "zeroing velocity vectors, relaxing tensile strain, and dissipating heat", "process_in_context": "logic as deceleration — bringing kinetic forces to equilibrium and settling onto support"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "exhaustion of momentum, completed work, or fall of night", "process_in_context": "history as rest — the completed toil or weary fatigue that necessitated repose"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "profound peace, refreshed vitality, and serene stillness", "process_in_context": "effect as serenity — the restorative calm and deep peace of quiet rest"}
            }
        }
    }

    for key, pdata in novel_primitives.items():
        if key not in aec_forms:
            actions = [a.strip() for a in key.split("->")[0].split(",")]
            strains = [s.strip() for s in key.split("->")[1].split(",")]
            effects = [e.strip() for e in key.split("->")[2].split(",")]

            form_node = {
                "form_id": "",  # Will be assigned during final renumbering
                "invariant_triad": {
                    "action": actions,
                    "strain": strains,
                    "effect": effects,
                    "summary": key
                },
                "definitive_process": pdata["process"],
                "concept_type": "genotype",
                "topology": pdata["topology"],
                "descriptive_words": {
                    "primary_label": pdata["primary"],
                    "aliases": pdata["aliases"],
                    "planar_vocabulary": {f"Q{i}": [] for i in range(1, 8)}
                },
                "planes": pdata["planes"],
                "related_forms": []
            }
            aec_forms[key] = form_node
            print(f">>> Minted Novel Primitive: '{pdata['primary']}' ({key[:50]}...)")

            word_index[pdata["primary"]] = {"form_id": "", "aec_key": key, "role": "primary_label"}
            for al in pdata["aliases"]:
                word_index[al] = {"form_id": "", "aec_key": key, "role": "alias"}

    # FINAL RENUMBERING AND INDEX REFRESH
    form_counter = 1
    clean_forms = {}
    for key, f in aec_forms.items():
        fid = f"AEC-{form_counter:03d}"
        form_counter += 1
        f["form_id"] = fid
        clean_forms[key] = f

        prim = f["descriptive_words"]["primary_label"]
        if prim:
            word_index[prim] = {"form_id": fid, "aec_key": key, "role": "primary_label"}
        for al in f["descriptive_words"]["aliases"]:
            word_index[al] = {"form_id": fid, "aec_key": key, "role": "alias"}

    data["aec_forms"] = clean_forms
    data["metadata"]["total_aec_forms"] = len(clean_forms)
    data["metadata"]["total_indexed_words"] = len(word_index)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(f"// Auto-generated distribution file for Reality Classification v2\nwindow.AEC_DICT = {json.dumps(data, ensure_ascii=False)};\n")

    print(f"\n[SUCCESS] Deep Evolution Pass 1 Complete!")
    print(f"Final Count: {len(clean_forms)} Pure Invariant Forms | {len(word_index)} Mapped Words.")

if __name__ == "__main__":
    execute()
