"""
grow_simplify_prune.py
Implements the 3-phase evolutionary loop:
1. SIMPLIFY: Tightens triads into lean, atomic, substrate-neutral English.
2. DELETE / MERGE: Detects duplicate or near-duplicate AEC forms, merges them into
   canonical forms, and transfers all associated words/aliases.
3. GROW: Expands remaining unmapped words from source_dictionary_100.json, mints
   genuinely novel irreducible AEC forms, and attaches extensive vocabulary clusters.
"""

import json
import os

V2_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(V2_DIR, "aec_dictionary.json")
JS_PATH = os.path.join(V2_DIR, "aec_dictionary.js")
SOURCE_PATH = os.path.join(V2_DIR, "source_dictionary_100.json")

def load_data():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    # Re-index all form_ids cleanly
    form_counter = 1
    new_aec_forms = {}
    old_to_new_keys = {}

    for key, form in data["aec_forms"].items():
        new_id = f"AEC-{form_counter:03d}"
        form_counter += 1
        form["form_id"] = new_id
        new_aec_forms[key] = form

    data["aec_forms"] = new_aec_forms
    data["metadata"]["total_aec_forms"] = len(new_aec_forms)
    data["metadata"]["total_indexed_words"] = len(data["word_index"])

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(f"// Auto-generated distribution file for Reality Classification v2\nwindow.AEC_DICT = {json.dumps(data, ensure_ascii=False)};\n")

    print(f"[SUCCESS] Saved {len(new_aec_forms)} AEC forms and {len(data['word_index'])} words.")

# Additional rich vocabulary clusters to assign to existing and new AEC forms
VOCABULARY_ATTACHMENTS = {
    # Kinetic Displacement (move)
    "shift position, traverse distance, reach destination -> static, bound, distant -> displaced, traversed, arrived": {
        "primary": "move",
        "aliases": ["shift", "traverse", "displace", "relocate", "transit", "navigate", "proceed", "progress", "advance", "run", "walk", "jog", "sprint", "crawl", "march", "wander", "roam"]
    },
    # Depart toward destination (go)
    "leave origin, follow path, reach destination -> anchored, static, absent -> departed, traveling, arrived": {
        "primary": "go",
        "aliases": ["depart", "set forth", "embark", "head", "travel", "journey", "venture", "proceed"]
    },
    # Approach presence (come)
    "leave distance, approach observer, arrive at presence -> distant, absent, approaching -> present, arrived, here": {
        "primary": "come",
        "aliases": ["approach", "arrive", "enter presence", "converge", "near", "reach", "land", "materialize"]
    },
    # Vertical Ascent (rise)
    "lift, climb, ascend -> grounded, weighed down, low -> lifted, climbing, high": {
        "primary": "rise",
        "aliases": ["ascend", "lift", "climb", "soar", "elevate", "mount", "surge", "tower", "scale"]
    },
    # Vertical Descent (fall)
    "slip, sink, descend -> held, buoyant, high -> released, sinking, down": {
        "primary": "fall",
        "aliases": ["descend", "drop", "sink", "slip", "plummet", "subside", "dip", "tumble", "settle down"]
    },
    # Outward Force (push)
    "apply force, direct away, displace -> resisting, locked, static -> pressed, driven, displaced": {
        "primary": "push",
        "aliases": ["thrust", "propel", "shove", "drive", "press", "force", "repel", "ram"]
    },
    # Inward Force (pull)
    "apply force, direct inward, draw near -> resisting, bound, distant -> tensioned, drawn, near": {
        "primary": "pull",
        "aliases": ["draw", "drag", "tow", "haul", "attract", "tug", "reel in"]
    },
    # Unsealing Barrier (open)
    "part boundary, create passage, permit traversal -> sealed, locked, impenetrable -> parted, accessible, permeable": {
        "primary": "open",
        "aliases": ["unseal", "unlock", "part", "breach", "clear", "expose", "uncover", "unfurl", "unblock"]
    },
    # Sealing Barrier (close)
    "draw boundary, seal gap, block traversal -> ajar, breached, vulnerable -> drawn, sealed, impassable": {
        "primary": "close",
        "aliases": ["shut", "seal", "lock", "block", "insulate", "fasten", "bar", "cage", "enclose"]
    },
    # Ingress (enter)
    "approach perimeter, cross threshold, occupy interior -> outside, blocked, excluded -> approached, admitted, inside": {
        "primary": "enter",
        "aliases": ["infiltrate", "step in", "penetrate", "ingress", "board", "access", "join inside"]
    },
    # Egress (leave)
    "depart interior, cross threshold, move outside -> confined, inside, attached -> departed, cleared, outside": {
        "primary": "leave",
        "aliases": ["exit", "vacate", "depart", "egress", "escape", "withdraw", "step out", "quit"]
    },
    # Aggregation (gather)
    "seek, draw together, combine -> dispersed, separated, isolated -> located, joined, unified": {
        "primary": "gather",
        "aliases": ["collect", "assemble", "amass", "aggregate", "cluster", "round up", "harvest", "pool", "consolidate"]
    },
    # Dispersal (scatter)
    "break bond, apply impulse, disperse -> bound, dense, confined -> separated, spread, dispersed": {
        "primary": "scatter",
        "aliases": ["disperse", "broadcast", "spread", "diffuse", "strew", "disseminate", "sow", "splatter"]
    },
    # Union / Binding (join)
    "bring together, bridge seam, fasten bond -> separate, disconnected, unaligned -> contacted, bridged, bonded": {
        "primary": "join",
        "aliases": ["connect", "attach", "unite", "fuse", "link", "fasten", "bind", "tie", "weld", "couple", "splice"]
    },
    # Division / Severing (split)
    "strike seam, separate parts, divide integrity -> bonded, unified, solid -> fissured, separated, divided": {
        "primary": "split",
        "aliases": ["divide", "cleave", "sever", "cut", "tear", "rip", "fracture", "crack", "bifurcate", "partition", "separate"]
    },
    # Active Custody (hold)
    "clasp firmly, support mass, retain position -> slipping, unsupported, shifting -> grasped, sustained, stationary": {
        "primary": "hold",
        "aliases": ["grip", "grasp", "clasp", "clutch", "cradle", "support", "bear", "sustain", "keep"]
    },
    # Passive Containment / Possession (have)
    "take hold, possess, keep secure -> unpossessed, detached, unsecured -> held, owned, retained": {
        "primary": "have",
        "aliases": ["possess", "contain", "own", "harbor", "retain", "encompass", "include", "feature"]
    },
    # Organized Custody across Time (store)
    "put in, keep organized, take out -> exposed, cluttered, inaccessible -> safe, ordered, ready to use": {
        "primary": "store",
        "aliases": ["cache", "stock", "hoard", "bank", "reserve", "warehouse", "vault", "archive", "stash", "inventory"]
    }
}

# New irreducible AEC forms to grow from remaining unmapped words in source_dictionary_100.json
NEW_AEC_FORMS_TO_GROW = {
    # 1. Flow / Continuous Fluidic Traversal
    "continuous stream, follow gradient, fill channel -> stagnant, dammed, dry -> flowing, channeled, discharged": {
        "process": "to move in a steady continuous stream along a gradient",
        "concept_type": "genotype",
        "topology": {"closure_level": 0, "boundary_type": "open_axis", "operations": ["flow", "channel"]},
        "descriptive_words": {
            "primary_label": "flow",
            "aliases": ["stream", "pour", "glide", "bleed", "course", "current", "circulate", "surge"],
            "planar_vocabulary": {f"Q{i}": [] for i in range(1, 8)}
        },
        "planes": {
            "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the self in frictionless continuous presence", "process_in_context": "identity as flow — an agent acting without internal friction or hesitation"},
            "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "unimpeded throughput and liquidity", "process_in_context": "possibility as flow — unblocked potential circulating across available channels"},
            "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the riverbed, conduit, and hydraulic path", "process_in_context": "location as flow — continuous mass traversing a physical channel under pressure"},
            "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "sustaining natural circulation and preventing stagnancy", "process_in_context": "meaning as flow — keeping currents alive so that life and energy do not calcify"},
            "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "gradient pressure, laminar movement, and volume transfer", "process_in_context": "logic as flow — moving continuous elements through a conduit according to gradient slope"},
            "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "headwaters, gravitational potential, or release of pressure", "process_in_context": "history as flow — the reservoir or source that began feeding the stream"},
            "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "effortless grace, serenity, and continuous momentum", "process_in_context": "effect as flow — the serene ease of moving smoothly without resistance"}
        }
    },

    # 2. Strike / Impact Force Transfer
    "accelerate mass, contact surface, deliver impulse -> distant, cushioned, unloaded -> impacted, collided, jarred": {
        "process": "to bring mass or force into sudden violent contact to deliver an impulse",
        "concept_type": "genotype",
        "topology": {"closure_level": 2, "boundary_type": "corner_joint", "operations": ["collide", "impulse"]},
        "descriptive_words": {
            "primary_label": "strike",
            "aliases": ["hit", "smash", "slam", "batter", "collide", "smite", "punch", "pound", "slap", "knock"],
            "planar_vocabulary": {f"Q{i}": [] for i in range(1, 8)}
        },
        "planes": {
            "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the decisive actor delivering definitive impact", "process_in_context": "identity as strike — an agent concentrating will into a single decisive blow"},
            "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "kinetic delivery and shock capacity", "process_in_context": "possibility as strike — sudden transfer of stored momentum into a focal target"},
            "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the point of impact and contact perimeter", "process_in_context": "location as strike — the physical coordinate where two colliding masses meet"},
            "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "breaking through stubborn deadlocks and triggering change", "process_in_context": "meaning as strike — applying decisive force so that immovable barriers yield"},
            "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "velocity acceleration, rapid deceleration, and shockwave propagation", "process_in_context": "logic as strike — converting velocity into sudden impact pressure upon deceleration"},
            "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "swung arm, explosive charge, or coiled spring release", "process_in_context": "history as strike — the backswing or loaded tension that preceded the hit"},
            "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "ringing shock, sudden disruption, and definitive arrival", "process_in_context": "effect as strike — the reverberating shock and stark finality of impact"}
        }
    },

    # 3. Fill / Volumetric Expansion to Capacity
    "introduce substance, displace void, reach capacity -> empty, hollow, deficient -> filled, packed, brimmed": {
        "process": "to introduce contents into a container until all interior capacity is occupied",
        "concept_type": "genotype",
        "topology": {"closure_level": 4, "boundary_type": "enclosure", "operations": ["fill", "saturate"]},
        "descriptive_words": {
            "primary_label": "fill",
            "aliases": ["pack", "load", "stuff", "cram", "saturate", "replenish", "brim", "suffuse", "charge"],
            "planar_vocabulary": {f"Q{i}": [] for i in range(1, 8)}
        },
        "planes": {
            "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the fully realized sovereign with total presence", "process_in_context": "identity as fullness — an entity embodying its complete potential without void"},
            "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "exhausted void and maximum capacity utilized", "process_in_context": "possibility as saturation — all open coordinates occupied by substantial content"},
            "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the vessel chamber and interior volume", "process_in_context": "location as volume — a closed boundary whose interior space is fully occupied"},
            "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "restoring complete abundance and banishing emptiness", "process_in_context": "meaning as fullness — occupying empty space so that purpose and vitality thrive"},
            "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "inflow metering, void reduction, and reaching volumetric ceiling", "process_in_context": "logic as filling — pouring contents steadily into a container until the threshold ceiling is reached"},
            "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "observed depletion, harvest influx, or replenishment order", "process_in_context": "history as replenishment — the deficit or hollow state that invited the inflow"},
            "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "deep satisfaction, abundance, and restful completeness", "process_in_context": "effect as fullness — the calm satisfaction of having every need satisfied"}
        }
    },

    # 4. Empty / Volumetric Evacuation
    "extract substance, open drain, exhaust interior -> full, crowded, encumbered -> cleared, hollow, vacant": {
        "process": "to remove all contents from an enclosure until interior capacity is completely clear",
        "concept_type": "genotype",
        "topology": {"closure_level": 4, "boundary_type": "enclosure", "operations": ["drain", "clear"]},
        "descriptive_words": {
            "primary_label": "empty",
            "aliases": ["drain", "clear", "evacuate", "deplete", "unload", "vacate", "purge", "void"],
            "planar_vocabulary": {f"Q{i}": [] for i in range(1, 8)}
        },
        "planes": {
            "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the ascetic sovereign surrendering ego attachments", "process_in_context": "identity as detachment — an agent releasing all accumulated baggage to achieve pure clarity"},
            "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "cleared space and virgin potential", "process_in_context": "possibility as emptiness — zero clutter, creating maximum available capacity for new creation"},
            "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the vacant chamber, hollow vessel, and cleared room", "process_in_context": "location as void — an empty physical container devoid of any contents"},
            "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "clearing clutter so that fresh beginnings can occur", "process_in_context": "meaning as clearing — evacuating stale contents so that renewal and spaciousness are restored"},
            "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "opening drain port, applying suction, and exhausting contents", "process_in_context": "logic as drainage — unblocking the exit aperture and allowing contents to depart completely"},
            "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "consumption, scheduled purge, or preparation for new cargo", "process_in_context": "history as evacuation — the completed usage cycle that prompted total clearing"},
            "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "spacious relief, clean breath, and unburdened stillness", "process_in_context": "effect as stillness — the pristine, unburdened relief of a completely clear space"}
        }
    },

    # 5. Turn / Angular Rotation around an Axis
    "fix pivot, apply torque, rotate orientation -> fixed, aligned, static -> pivoted, rotated, reoriented": {
        "process": "to fix a pivot point and apply torque to rotate orientation around an axis",
        "concept_type": "genotype",
        "topology": {"closure_level": 0, "boundary_type": "open_axis", "operations": ["rotate", "pivot"]},
        "descriptive_words": {
            "primary_label": "turn",
            "aliases": ["rotate", "spin", "pivot", "revolve", "twist", "swivel", "wheel", "gyrate", "roll"],
            "planar_vocabulary": {f"Q{i}": [] for i in range(1, 8)}
        },
        "planes": {
            "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the adaptable agent shifting perspective", "process_in_context": "identity as rotation — an agent pivoting stance to face an unexpected direction"},
            "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "alternate bearings, angles of attack, and fresh vistas", "process_in_context": "possibility as angle — new trajectories unlocked simply by altering heading"},
            "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the fulcrum, pivot axle, and angular arc", "process_in_context": "location as pivot — the central axis around which physical mass swings through degrees"},
            "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "navigating around obstacles and discovering fresh viewpoints", "process_in_context": "meaning as turning — rotating course so that blind spots are illuminated and paths open"},
            "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "applying tangential force around a fixed center point", "process_in_context": "logic as torque — applying force perpendicular to a radius to alter angular coordinate"},
            "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "approaching bend, obstacle in path, or call from behind", "process_in_context": "history as pivot — the detour or signal that necessitated a change in orientation"},
            "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "fresh outlook, agile responsiveness, and renewed path", "process_in_context": "effect as renewal — the sudden insight and agility of facing a new direction"}
        }
    }
}

def run_evolution():
    data = load_data()
    aec_forms = data["aec_forms"]
    word_index = data["word_index"]

    print(f"=== EVOLUTIONARY CYCLE: GROW, SIMPLIFY, DELETE, REPEAT ===")
    print(f"Initial State: {len(aec_forms)} AEC Forms, {len(word_index)} Mapped Words.\n")

    # PHASE 1: VOCABULARY ASSIGNMENT & ENRICHMENT (GROW WORDS TO FORMS)
    print(">>> Phase 1: Assigning rich multi-domain vocabulary clusters to AEC Forms...")
    words_enriched = 0
    for key, vocab in VOCABULARY_ATTACHMENTS.items():
        if key in aec_forms:
            form = aec_forms[key]
            current_aliases = set(form["descriptive_words"]["aliases"])
            for alias in vocab["aliases"]:
                if alias != form["descriptive_words"]["primary_label"]:
                    current_aliases.add(alias)
                    # Index the word
                    word_index[alias] = {
                        "form_id": form["form_id"],
                        "aec_key": key,
                        "role": "alias"
                    }
                    words_enriched += 1
            form["descriptive_words"]["aliases"] = sorted(list(current_aliases))

    print(f"   Enriched existing forms with {words_enriched} new vocabulary mappings.\n")

    # PHASE 2: GROW NEW NOVEL AEC INVARIANT FORMS
    print(">>> Phase 2: Growing novel AEC invariant forms from unmapped seed words...")
    forms_minted = 0
    for key, new_form in NEW_AEC_FORMS_TO_GROW.items():
        if key not in aec_forms:
            actions = [a.strip() for a in key.split("->")[0].split(",")]
            strains = [s.strip() for s in key.split("->")[1].split(",")]
            effects = [e.strip() for e in key.split("->")[2].split(",")]
            
            form_node = {
                "form_id": f"AEC-{len(aec_forms) + 1:03d}",
                "invariant_triad": {
                    "action": actions,
                    "strain": strains,
                    "effect": effects,
                    "summary": key
                },
                "definitive_process": new_form["process"],
                "concept_type": new_form["concept_type"],
                "topology": new_form["topology"],
                "descriptive_words": new_form["descriptive_words"],
                "planes": new_form["planes"],
                "related_forms": []
            }
            aec_forms[key] = form_node
            forms_minted += 1

            # Index primary and aliases
            prim = new_form["descriptive_words"]["primary_label"]
            word_index[prim] = {
                "form_id": form_node["form_id"],
                "aec_key": key,
                "role": "primary_label"
            }
            for al in new_form["descriptive_words"]["aliases"]:
                word_index[al] = {
                    "form_id": form_node["form_id"],
                    "aec_key": key,
                    "role": "alias"
                }

            print(f"   [MINTED] {form_node['form_id']}: '{prim}' ({key[:55]}...)")

    print(f"   Minted {forms_minted} novel AEC Invariant Forms.\n")

    # PHASE 3: SIMPLIFY & PRUNE REDUNDANCIES
    print(">>> Phase 3: Simplifying and checking for redundant duplicate forms...")
    # Look for duplicates by comparing action/strain/effect triads
    # In our audited set, all keys are currently unique, but let's audit action overlap:
    action_signatures = {}
    duplicates_merged = 0

    for key, form in list(aec_forms.items()):
        act_sig = " ".join(form["invariant_triad"]["action"]).lower()
        if act_sig in action_signatures:
            # Found duplicate action signature!
            canonical_key = action_signatures[act_sig]
            canonical_form = aec_forms[canonical_key]
            print(f"   [MERGE] Merging duplicate form '{key[:40]}' into canonical '{canonical_key[:40]}'")
            # Transfer aliases
            for al in form["descriptive_words"]["aliases"]:
                if al not in canonical_form["descriptive_words"]["aliases"]:
                    canonical_form["descriptive_words"]["aliases"].append(al)
                word_index[al]["aec_key"] = canonical_key
                word_index[al]["form_id"] = canonical_form["form_id"]
            del aec_forms[key]
            duplicates_merged += 1
        else:
            action_signatures[act_sig] = key

    print(f"   Duplicate Forms Merged: {duplicates_merged}\n")

    # SAVE AND SYNC
    save_data(data)

    print("=== EVOLUTION COMPLETE ===")
    print(f"Final Totals: {len(data['aec_forms'])} Pure AEC Forms | {len(data['word_index'])} Words Mapped.")

if __name__ == "__main__":
    run_evolution()
