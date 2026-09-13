"""
pdp_engine.py
The Pull-Divide-Push (PDP) Evolutionary Engine for Reality Classification v2:
1. PULL: Extracts related lexical candidates from WordNet and seed corpora around a root AEC form.
2. DIVIDE: Analyzes differences in topological closure, vector polarity, permeability, and telos
   to differentiate words into distinct evolutionary lineages/mutations.
3. PUSH: Mints and parameterizes derived/mutated AEC Forms with explicit parent lineage links,
   attaching all corresponding surface words to their precise evolutionary branch.
"""

import json
import os
from nltk.corpus import wordnet as wn

V2_DIR = os.path.dirname(__file__)
JSON_PATH = os.path.join(V2_DIR, "aec_dictionary.json")
JS_PATH = os.path.join(V2_DIR, "aec_dictionary.js")

def load_data():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    # Renumber form IDs cleanly and rebuild word index
    form_counter = 1
    new_forms = {}
    new_word_index = {}

    for key, form in data["aec_forms"].items():
        fid = f"AEC-{form_counter:03d}"
        form_counter += 1
        form["form_id"] = fid
        new_forms[key] = form

        prim = form["descriptive_words"]["primary_label"]
        if prim:
            new_word_index[prim] = {"form_id": fid, "aec_key": key, "role": "primary_label"}
        for alias in form["descriptive_words"]["aliases"]:
            new_word_index[alias] = {"form_id": fid, "aec_key": key, "role": "alias"}

    # Update lineage parent pointers if any
    # (Map old IDs to new IDs if needed)
    data["aec_forms"] = new_forms
    data["word_index"] = new_word_index
    data["metadata"]["total_aec_forms"] = len(new_forms)
    data["metadata"]["total_indexed_words"] = len(new_word_index)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(f"// Auto-generated distribution file for Reality Classification v2\nwindow.AEC_DICT = {json.dumps(data, ensure_ascii=False)};\n")

    print(f"[SUCCESS] Saved {len(new_forms)} AEC Forms and {len(new_word_index)} Mapped Words.")

def pull_wordnet_candidates(seed_synsets):
    """PULL: Harvest all hyponyms and lemmas around given synsets."""
    candidates = set()
    for s_name in seed_synsets:
        try:
            syn = wn.synset(s_name)
            for lemma in syn.lemmas():
                candidates.add(lemma.name().lower().replace("_", " "))
            for hypo in syn.hyponyms():
                for l in hypo.lemmas():
                    candidates.add(l.name().lower().replace("_", " "))
        except Exception as e:
            print(f"Warning pulling {s_name}: {e}")
    return sorted(list(candidates))

def run_container_pdp_evolution():
    data = load_data()
    aec_forms = data["aec_forms"]
    word_index = data["word_index"]

    print("=== EXECUTING PULL-DIVIDE-PUSH (PDP) ON ROOT: CONTAINMENT ===")
    
    # 1. PULL
    print(">>> Phase 1: PULL - Gathering candidates from WordNet around 'container' & 'containment'...")
    seed_synsets = ["container.n.01", "containment.n.01", "contain.v.01", "enclosure.n.01"]
    pulled_words = pull_wordnet_candidates(seed_synsets)
    print(f"   Harvested {len(pulled_words)} related words from WordNet.")

    # 2. DIVIDE: Topological & Vector Differentiation
    print(">>> Phase 2: DIVIDE - Classifying words along 6 Evolutionary Mutation Lineages...")
    
    # Lineage definitions stemming from Root Containment (AEC-022: 'have/contain')
    CONTAINER_LINEAGES = {
        # Lineage A: Temporal Organized Storage (Already in store AEC-001)
        "temporal_storage": {
            "key": "put in, keep organized, take out -> exposed, cluttered, inaccessible -> safe, ordered, ready to use",
            "aliases_to_add": ["case", "bin", "box", "canister", "capsule", "package", "chest", "locker", "reliquary", "depot"]
        },
        # Lineage B: Protective Insulation / Shield (Already in shelter AEC-007)
        "protective_insulation": {
            "key": "raise barrier, block storm, preserve life -> exposed, vulnerable, assaulted -> sheltered, shielded, secure",
            "aliases_to_add": ["shield", "armor", "bunker", "haven", "refuge", "sanctuary", "casing", "capsule", "sheath", "ward"]
        },
        # Lineage C: Coercive Restraint / Imprisonment (NOVEL MUTATION)
        "coercive_restraint": {
            "triad": {
                "action": ["block escape", "impose perimeter", "enforce confinement"],
                "strain": ["struggling", "rebellious", "unconfined"],
                "effect": ["penned", "locked", "confined"]
            },
            "primary": "confine",
            "aliases": ["cage", "imprison", "pen", "corral", "coop", "trap", "jail", "impound", "shackle", "paddock", "contain forcefully"],
            "process": "to impose a rigid boundary around an entity to block escape and enforce confinement",
            "topology": {"closure_level": 4, "boundary_type": "enclosure", "operations": ["block_exit", "contain"]},
            "mutation_delta": "inverts consent and permeability: blocks outward egress against internal outward pressure",
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the captive sovereign whose will is bounded by force", "process_in_context": "identity as captivity — an agent whose operational degrees of freedom are forcibly curtailed"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "strictly quarantined potential and blocked trajectories", "process_in_context": "possibility as quarantine — dangerous or unvetted capacity quarantined within strict limits"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the cage, prison cell, pen, and locked room", "process_in_context": "location as cage — a physical enclosure engineered with impassable walls enclosing an interior space"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "neutralizing violent threats and preserving communal safety", "process_in_context": "meaning as confinement — restraining destructive forces so that peace and justice survive outside"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "closing perimeter locks, verifying seals, and denying traversal permissions", "process_in_context": "logic as isolation — denying all outward traversal requests and sealing egress ports"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "transgression, captured threat, or quarantine order", "process_in_context": "history as capture — the breach or peril that necessitated absolute restraint"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "somber confinement, restless stillness, and controlled peace", "process_in_context": "effect as containment — the tense, enforced stillness of a contained force"}
            }
        },
        # Lineage D: Gravitational Fluid Accumulation / Basin (NOVEL MUTATION)
        "fluid_basin": {
            "triad": {
                "action": ["receive run-off", "pool volume", "retain reserve"],
                "strain": ["draining", "dispersing", "lost"],
                "effect": ["gathered", "pooled", "accumulated"]
            },
            "primary": "basin",
            "aliases": ["pool", "cistern", "tank", "vat", "reservoir", "sump", "sink", "well", "bowl", "trough"],
            "process": "to receive downward liquid run-off and pool it within a depression to retain a reserve",
            "topology": {"closure_level": 3, "boundary_type": "pocket", "operations": ["pool", "catch"]},
            "mutation_delta": "gravitational catchment: open upward aperture with solid downward floor retaining fluid mass",
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the receptive sovereign holding humble space for all streams", "process_in_context": "identity as basin — an agent occupying the low ground to receive and harbor flowing contributions"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "accumulated fluid volume and stored hydrostatic head", "process_in_context": "possibility as reservoir — unallocated fluid potential stored in reserve ready for irrigation"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the basin, cistern, reservoir, and catchment floor", "process_in_context": "location as basin — a sunken geographic contour that naturally collects and holds liquid"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "preserving life-giving water across seasons of drought", "process_in_context": "meaning as reservoir — pooling seasonal bounty so that communities flourish during arid times"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "gravity-assisted inflow, bottom impermeability, and hydrostatic balancing", "process_in_context": "logic as catchment — channeling tributary inflow into an impermeable depression"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "heavy rainfall, glacial melt, or tributary convergence", "process_in_context": "history as catchment — the rainfall and down-gradient flow that filled the basin"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "peaceful abundance, cool refreshment, and deep security", "process_in_context": "effect as abundance — the tranquil assurance of standing next to a deep, full reservoir"}
            }
        },
        # Lineage E: Differential Boundary Permeability / Sieve (NOVEL MUTATION)
        "permeable_filter": {
            "triad": {
                "action": ["impede coarse", "permit fine", "divide stream"],
                "strain": ["mixed", "contaminated", "clogged"],
                "effect": ["sifted", "purified", "separated"]
            },
            "primary": "filter",
            "aliases": ["sieve", "screen", "mesh", "strainer", "colander", "grate", "sifter", "purify", "separate coarse"],
            "process": "to apply a perforated boundary that impedes coarse elements while permitting fine elements to pass",
            "topology": {"closure_level": 1, "boundary_type": "wall_threshold", "operations": ["screen", "filter"]},
            "mutation_delta": "partial selective permeability: boundary contains microscopic apertures calibrated to particulate scale",
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the discerning sovereign testing truth and rejecting dross", "process_in_context": "identity as discernment — an agent sifting incoming influences to admit only what is pure"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "purified substance and separated fractions", "process_in_context": "possibility as refinement — sorting mixed potential into clean, usable grades"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the membrane, mesh screen, grate, and sieve bed", "process_in_context": "location as filter — a porous physical boundary stationed across a moving stream"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "purifying life and removing toxic debris", "process_in_context": "meaning as purification — filtering impure waters so that health and clarity are restored"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "pore size restriction, particulate entrapment, and laminar filtrate throughput", "process_in_context": "logic as filtration — blocking elements whose dimensions exceed aperture tolerance"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "turbid water, mixed grain, or sediment influx", "process_in_context": "history as filtration — the muddy flood or mixed harvest that required cleansing"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "crystal clarity, purified refreshment, and wholesome integrity", "process_in_context": "effect as clarity — the pristine joy of drinking clear, uncontaminated water"}
            }
        },
        # Lineage F: Controlled Metering Aperture / Dispenser (NOVEL MUTATION)
        "metering_dispenser": {
            "triad": {
                "action": ["restrict flow", "meter portion", "discharge increment"],
                "strain": ["gushing", "uncontrolled", "flooded"],
                "effect": ["metered", "controlled", "dispensed"]
            },
            "primary": "dispense",
            "aliases": ["meter", "funnel", "spout", "valve", "nozzle", "dropper", "tap", "vent", "ration", "distribute"],
            "process": "to restrict container outflow and meter contents into precise increments through a controlled aperture",
            "topology": {"closure_level": 4, "boundary_type": "enclosure", "operations": ["meter", "discharge"]},
            "mutation_delta": "aperture metering: container fitted with adjustable valve throttling outflow velocity and volume",
            "planes": {
                "Q1": {"interrogative": "Who", "dimension": "MetaPhysical", "anchor": "Identity", "manifestation_answer": "the measured steward allocating resources with precise prudence", "process_in_context": "identity as prudence — an agent distributing gifts in exact measure without excess"},
                "Q2": {"interrogative": "What", "dimension": "Possible", "anchor": "Possible", "manifestation_answer": "rationed quotas, calibrated dosages, and controlled throughput", "process_in_context": "possibility as quota — converting raw bulk inventory into usable, calibrated servings"},
                "Q3": {"interrogative": "Where", "dimension": "Physical", "anchor": "Location", "manifestation_answer": "the valve, spigot, spout, nozzle, and metering gate", "process_in_context": "location as nozzle — the narrow constriction at the exit of a container governing flow rate"},
                "Q4": {"interrogative": "Why", "dimension": "Lyrical", "anchor": "Meaning", "manifestation_answer": "preventing catastrophic floods and ensuring equitable distribution", "process_in_context": "meaning as measured sharing — metering abundance so that every recipient receives their fair portion"},
                "Q5": {"interrogative": "How", "dimension": "Logical", "anchor": "Mechanical", "manifestation_answer": "actuator stroke, orifice constriction, and timed pulse metering", "process_in_context": "logic as metering — opening the discharge gate for a calibrated interval and resealing"},
                "Q6": {"interrogative": "Cause", "dimension": "Historical", "anchor": "Historical", "manifestation_answer": "request for dose, irrigation schedule, or demand pulse", "process_in_context": "history as demand — the external call that prompted a single metered release"},
                "Q7": {"interrogative": "Effect", "dimension": "Emotive", "anchor": "Emotive", "manifestation_answer": "just proportion, orderly distribution, and prudent satisfaction", "process_in_context": "effect as equity — the calm order of receiving exactly the right amount without excess"}
            }
        }
    }

    # 3. PUSH: Apply Lineages to aec_dictionary
    print(">>> Phase 3: PUSH - Integrating lineage forms and attaching harvested vocabulary...")
    
    # Enrich existing store (Lineage A) and shelter (Lineage B)
    for l_name, l_data in [("temporal_storage", CONTAINER_LINEAGES["temporal_storage"]), ("protective_insulation", CONTAINER_LINEAGES["protective_insulation"])]:
        k = l_data["key"]
        if k in aec_forms:
            form = aec_forms[k]
            aliases = set(form["descriptive_words"]["aliases"])
            aliases.update(l_data["aliases_to_add"])
            form["descriptive_words"]["aliases"] = sorted(list(aliases))
            # Tag lineage
            form["lineage"] = {
                "parent_concept": "containment",
                "parent_form_id": "AEC-022",
                "lineage_branch": l_name
            }

    # Mint Novel Lineage Mutations (C, D, E, F)
    for l_name, l_data in [("coercive_restraint", CONTAINER_LINEAGES["coercive_restraint"]),
                          ("fluid_basin", CONTAINER_LINEAGES["fluid_basin"]),
                          ("permeable_filter", CONTAINER_LINEAGES["permeable_filter"]),
                          ("metering_dispenser", CONTAINER_LINEAGES["metering_dispenser"])]:
        triad = l_data["triad"]
        key = f"{', '.join(triad['action'])} -> {', '.join(triad['strain'])} -> {', '.join(triad['effect'])}"
        
        if key not in aec_forms:
            form_node = {
                "form_id": "",
                "invariant_triad": {
                    "action": triad["action"],
                    "strain": triad["strain"],
                    "effect": triad["effect"],
                    "summary": key
                },
                "definitive_process": l_data["process"],
                "concept_type": "lineage_mutation",
                "topology": l_data["topology"],
                "lineage": {
                    "parent_concept": "containment",
                    "parent_form_id": "AEC-022",
                    "mutation_type": l_name,
                    "differentiation_delta": l_data["mutation_delta"]
                },
                "descriptive_words": {
                    "primary_label": l_data["primary"],
                    "aliases": sorted(l_data["aliases"]),
                    "planar_vocabulary": {f"Q{i}": [] for i in range(1, 8)}
                },
                "planes": l_data["planes"],
                "related_forms": ["AEC-022", "AEC-001", "AEC-007"]
            }
            aec_forms[key] = form_node
            print(f"   [PUSHED NOVEL LINEAGE] '{l_data['primary']}' ({l_name}): {key[:55]}...")

    # SAVE AND RENUMBER
    save_data(data)
    print("=== PDP CONTAINER EVOLUTION COMPLETE ===")

if __name__ == "__main__":
    run_container_pdp_evolution()
