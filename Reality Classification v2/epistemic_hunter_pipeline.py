"""
epistemic_hunter_pipeline.py
Core pipeline implementing the 5-Stage Epistemic Primitive Hunter Sieve to dynamically
process words from source_dictionary_100.json, extract Action-Strain-Effect invariants,
cluster them with existing primitives, and update aec_dictionary.json.
"""

import json
import os
import re

V2_DIR = os.path.dirname(__file__)
SOURCE_PATH = os.path.join(V2_DIR, "source_dictionary_100.json")
AEC_DICT_PATH = os.path.join(V2_DIR, "aec_dictionary.json")

# Core knowledge base of vetted epistemic extractions for foundational seed words
# extracted via the 5-stage de-substrating sieve:
VETTED_EPISTEMIC_MODELS = {
    # 1. Kinetic Force & Directional Vectors
    "push": {
        "action": "apply force, direct away, displace",
        "strain": "resisting, locked, static",
        "effect": "pressed, driven, displaced",
        "definitive_meaning": "to apply force away from the source to displace an entity",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 0, "boundary_type": "open_axis", "operations": ["propel", "displace"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the driving agent exerting outward force", "word_in_context_of_plane": "identity as thrust — an agent asserting will outward to displace external resistance"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "potential impulse and unapplied pressure", "word_in_context_of_plane": "possibility as thrust — stored kinetic energy ready to be directed against an obstacle"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the contact surface and forward vector path", "word_in_context_of_plane": "location as thrust — the physical interface where directed force moves mass across space"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "overcoming inertia and clearing obstacles", "word_in_context_of_plane": "meaning as thrust — exerting pressure so that stagnancy is broken and movement advances"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "contact pressure, vector alignment, and momentum transfer", "word_in_context_of_plane": "logic as thrust — transferring force along a directional vector to displace an object"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "prior intent, stored charge, or built-up tension", "word_in_context_of_plane": "history as thrust — the initiating spark and built-up energy that released outward pressure"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "overcome resistance, forward momentum, and progress", "word_in_context_of_plane": "effect as thrust — the dynamic breakthrough and momentum of moving past static resistance"}
        }
    },
    "pull": {
        "action": "apply force, direct inward, draw near",
        "strain": "resisting, bound, distant",
        "effect": "tensioned, drawn, near",
        "definitive_meaning": "to apply force toward the source to draw an entity closer",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 0, "boundary_type": "open_axis", "operations": ["draw", "tension"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the central agent drawing objects inward", "word_in_context_of_plane": "identity as attraction — an entity exerting inward tension to draw elements into orbit"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "gravitational potential and unspent tension", "word_in_context_of_plane": "possibility as attraction — inward tension waiting to reduce distance between entities"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the tension line and inward corridor", "word_in_context_of_plane": "location as attraction — the spatial span across which distance is closed toward origin"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "gathering resources and establishing proximity", "word_in_context_of_plane": "meaning as attraction — drawing elements near so that connection and integration occur"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "tensile coupling, contraction, and closing distance", "word_in_context_of_plane": "logic as attraction — establishing tensile grip and contracting the vector to pull an object close"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "observed value, magnetic origin, or inward demand", "word_in_context_of_plane": "history as attraction — the initial affinity or deficit that sparked the inward pull"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "closeness, attained custody, and secure proximity", "word_in_context_of_plane": "effect as attraction — the security and immediate contact of holding something close"}
        }
    },
    "rise": {
        "action": "lift, climb, ascend",
        "strain": "grounded, weighed down, low",
        "effect": "lifted, climbing, high",
        "definitive_meaning": "to lift from a baseline, climb against resistance, and ascend to a higher state",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 0, "boundary_type": "open_axis", "operations": ["ascend", "elevate"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the ascending entity overcoming baseline constraints", "word_in_context_of_plane": "identity as ascent — an agent asserting sovereignty to elevate above subordinate levels"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "unlocked altitude, valuation, and upper tiers", "word_in_context_of_plane": "possibility as ascent — open potential and higher strata ready to be occupied"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the vertical axis above the floor baseline", "word_in_context_of_plane": "location as ascent — the vertical spatial gradient separating low ground from high altitude"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "achieving higher perspective, mastery, and excellence", "word_in_context_of_plane": "meaning as ascent — elevating state so that vision expands and potential is realized"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "generating upward lift, overcoming gravity, and incrementing height", "word_in_context_of_plane": "logic as ascent — producing continuous counter-force to overcome downward pull step by step"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "buoyancy, accumulated energy, or launching impetus", "word_in_context_of_plane": "history as ascent — the initial energy impulse and upward momentum that broke the baseline"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "exhilaration, elevated status, and wide horizon", "word_in_context_of_plane": "effect as ascent — the expansive freedom, clarity, and triumph of standing at height"}
        }
    },
    "fall": {
        "action": "slip, sink, descend",
        "strain": "held, buoyant, high",
        "effect": "released, sinking, down",
        "definitive_meaning": "to slip from support, sink through a gradient, and descend to a lower state",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 0, "boundary_type": "open_axis", "operations": ["descend", "sink"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the uncoupled entity losing height or status", "word_in_context_of_plane": "identity as descent — an entity uncoupling from authority and transitioning to subordinate ground"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "lower brackets, ground state, and base capacity", "word_in_context_of_plane": "possibility as descent — downward trajectory and lower baseline awaiting arrival"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the vertical descent path toward the floor", "word_in_context_of_plane": "location as descent — the downward spatial corridor traversed toward the ground boundary"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "dissolving unsustainable elevation and returning to ground", "word_in_context_of_plane": "meaning as descent — relinquishing unstable height so that reality resets upon honest footing"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "yielding to downward pull, accelerating, and impacting baseline", "word_in_context_of_plane": "logic as descent — releasing structural support and allowing gravitational gradient to pull mass down"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "loss of support, structural failure, or severed anchor", "word_in_context_of_plane": "history as descent — the snapped bond or exhausted lift that triggered downward motion"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "grounded stability, humbled clarity, or impact collapse", "word_in_context_of_plane": "effect as descent — the grounded realism and sudden stillness of reaching bottom"}
        }
    },

    # 2. Boundary Operations
    "open": {
        "action": "part boundary, create passage, permit traversal",
        "strain": "sealed, locked, impenetrable",
        "effect": "parted, accessible, permeable",
        "definitive_meaning": "to part a boundary to create a passage and permit traversal across it",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 1, "boundary_type": "wall_threshold", "operations": ["unseal", "permit"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the transparent observer lowering defenses", "word_in_context_of_plane": "identity as candor — an agent unsealing internal barriers to express authentic presence"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "unlocked options, opportunities, and accessible pathways", "word_in_context_of_plane": "possibility as access — candidate trajectories rendered permeable and ready for exploration"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the portal, gateway, or parted threshold", "word_in_context_of_plane": "location as portal — an open gap in a physical perimeter allowing mass to cross"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "enabling flow, connection, and mutual exchange", "word_in_context_of_plane": "meaning as openness — unsealing rigid barriers so that knowledge and life circulate freely"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "disengaging latches, parting leaves, and establishing clearance", "word_in_context_of_plane": "logic as clearance — releasing fasteners and rotating barrier panels to clear the path"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "recognized need, key application, or deliberate invitation", "word_in_context_of_plane": "history as invitation — the key turning or decision that initiated the unsealing"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "welcome, relief of access, and freedom of motion", "word_in_context_of_plane": "effect as liberation — the expansive relief and hospitality of passing freely without barrier"}
        }
    },
    "close": {
        "action": "draw boundary, seal gap, block traversal",
        "strain": "ajar, breached, vulnerable",
        "effect": "drawn, sealed, impassable",
        "definitive_meaning": "to draw boundary edges together and seal a gap to block traversal across it",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 1, "boundary_type": "wall_threshold", "operations": ["seal", "block"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the guarded sovereign protecting internal space", "word_in_context_of_plane": "identity as containment — an agent raising sovereign barriers to guard interior integrity"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "settled limits, concluded choices, and secured reserves", "word_in_context_of_plane": "possibility as finality — open options settled and locked into definitive form"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the sealed wall, closed door, and perimeter seam", "word_in_context_of_plane": "location as barrier — a continuous physical surface completely blocking entry into an interior"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "protecting sanctuary and completing transitions", "word_in_context_of_plane": "meaning as closure — sealing perimeters so that interiors remain peaceful and cycles complete"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "aligning edges, engaging latches, and locking seals", "word_in_context_of_plane": "logic as sealing — drawing opposing edges into seamless contact and securing the lock"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "completed task, incoming storm, or departure of guest", "word_in_context_of_plane": "history as completion — the finished operation or external threat that required sealing"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "security, resolved closure, and peaceful insulation", "word_in_context_of_plane": "effect as security — the comforting peace of mind of an insulated, protected space"}
        }
    },

    # 3. Ingress & Egress
    "enter": {
        "action": "approach perimeter, cross threshold, occupy interior",
        "strain": "outside, blocked, excluded",
        "effect": "approached, admitted, inside",
        "definitive_meaning": "to cross a boundary threshold from outside and establish presence inside",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 1, "boundary_type": "wall_threshold", "operations": ["in", "cross"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the incoming agent seeking admission and presence", "word_in_context_of_plane": "identity as entry — an outsider committing to membership and stepping across the threshold"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "interior domains, privileges, and new environments", "word_in_context_of_plane": "possibility as inclusion — new internal capacities and relationships opened upon entry"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the doorway, portal, and interior chamber", "word_in_context_of_plane": "location as entry — the spatial transition point leading from outer perimeter to inner chamber"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "finding shelter, participating, and joining community", "word_in_context_of_plane": "meaning as entry — crossing thresholds so that agents gain sanctuary and shared belonging"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "presenting credentials, stepping forward, and settling inside", "word_in_context_of_plane": "logic as admission — clearing perimeter checks and advancing coordinates across the boundary"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "journey from afar, invitation, or need for refuge", "word_in_context_of_plane": "history as arrival — the preceding traversal across outer space that culminated at the door"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "relief of belonging, shelter, and inclusion", "word_in_context_of_plane": "effect as inclusion — the warm relief of being safely sheltered inside"}
        }
    },
    "leave": {
        "action": "depart interior, cross threshold, move outside",
        "strain": "confined, inside, attached",
        "effect": "departed, cleared, outside",
        "definitive_meaning": "to depart an interior, cross the threshold outward, and establish presence outside",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 1, "boundary_type": "wall_threshold", "operations": ["out", "cross"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the departing agent asserting autonomous trajectory", "word_in_context_of_plane": "identity as departure — an agent releasing institutional ties to strike outward autonomously"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "outer expanse, uncharted options, and distant horizon", "word_in_context_of_plane": "possibility as expanse — open fields and unrestricted vectors waiting beyond the wall"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the exit threshold, outward path, and exterior space", "word_in_context_of_plane": "location as exit — the outward transit corridor leaving interior confines for open space"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "seeking new horizons, independence, and exploration", "word_in_context_of_plane": "meaning as departure — stepping outside so that growth continues across wider domains"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "releasing interior holds, stepping through exit, and creating distance", "word_in_context_of_plane": "logic as exit — disengaging from interior fixtures and traversing outward past the threshold"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "completed stay, expiration of tenure, or call of distant goals", "word_in_context_of_plane": "history as release — the fulfilled purpose or restless impetus that spurred outward departure"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "exhilarating autonomy, bittersweet parting, and open freedom", "word_in_context_of_plane": "effect as liberation — the vast freedom and independence of stepping out into open space"}
        }
    },

    # 4. Aggregation & Dispersal
    "gather": {
        "action": "seek, draw together, combine",
        "strain": "dispersed, separated, isolated",
        "effect": "located, joined, unified",
        "definitive_meaning": "to seek separated elements and draw them together into a unified collection",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 2, "boundary_type": "pocket", "operations": ["gather", "collect"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the unifying coordinator assembling scattered parts", "word_in_context_of_plane": "identity as assembly — an agent seeking out distant elements and uniting them in common purpose"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "dispersed resources, talent, and scattered inventory", "word_in_context_of_plane": "possibility as concentration — isolated parts brought together into high-density collective power"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the assembly focal point, basin, or meeting hall", "word_in_context_of_plane": "location as assembly — a central geographic locus where separate streams converge"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "building solidarity, abundance, and collective strength", "word_in_context_of_plane": "meaning as unity — drawing isolated items together so that mutual strength and security flourish"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "locating fragments, drawing inward vectors, and clustering into sets", "word_in_context_of_plane": "logic as aggregation — systematically surveying perimeters, retrieving units, and stacking in sets"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "harvest season, prior dispersal, or collective emergency", "word_in_context_of_plane": "history as harvest — the preceding dispersion or seasonal abundance that demanded gathering"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "warm solidarity, abundance, and shared strength", "word_in_context_of_plane": "effect as solidarity — the comforting power and abundance of standing unified together"}
        }
    },
    "scatter": {
        "action": "break bond, apply impulse, disperse",
        "strain": "bound, dense, confined",
        "effect": "separated, spread, dispersed",
        "definitive_meaning": "to break a concentrated group and apply impulse to disperse elements across a domain",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 0, "boundary_type": "open_axis", "operations": ["scatter", "disperse"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the dispersing force broadcasting seeds outward", "word_in_context_of_plane": "identity as dissemination — an entity breaking concentrated clusters to broadcast potential widely"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "wide distribution, diverse vectors, and open spread", "word_in_context_of_plane": "possibility as dissemination — concentrated resources spread thinly across vast terrain to seed new growth"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the wide expanse, open field, and radial perimeter", "word_in_context_of_plane": "location as dispersal — an expansive territory across which individual fragments are distributed"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "seeding new territory and preventing stagnation", "word_in_context_of_plane": "meaning as dispersal — scattering concentrated density so that seeds take root across fresh soil"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "applying radial force, severing clusters, and distributing across space", "word_in_context_of_plane": "logic as dispersal — generating outward radial impulses that drive adjacent elements apart"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "sudden shock, sowing hand, or bursting pressure", "word_in_context_of_plane": "history as dispersal — the explosive strike or deliberate broadcast that launched the spread"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "broad coverage, scattered variety, and wide reach", "word_in_context_of_plane": "effect as variety — the wide reach and fertile distribution of seeds cast across the land"}
        }
    },

    # 5. Connection & Division
    "join": {
        "action": "bring together, bridge seam, fasten bond",
        "strain": "separate, disconnected, unaligned",
        "effect": "contacted, bridged, bonded",
        "definitive_meaning": "to bring separate entities together and fasten a secure bond across the seam",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 2, "boundary_type": "corner_joint", "operations": ["bridge", "fasten"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the covenant maker binding allies in union", "word_in_context_of_plane": "identity as alliance — two distinct sovereigns committing to a shared bond and unified stance"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "synergistic strength, shared conduits, and combined capacity", "word_in_context_of_plane": "possibility as synergy — combined capabilities emerging when two separate structures unite"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the joint, weld, seam, or intersection", "word_in_context_of_plane": "location as joint — the physical interface and seam where two distinct masses are fused"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "creating enduring harmony and overcoming division", "word_in_context_of_plane": "meaning as union — binding separate entities together so that communion and strength prevail"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "aligning edges, applying fastener, and securing joint", "word_in_context_of_plane": "logic as fastening — interlocking complementary surfaces and securing with high tensile cohesion"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "mutual affinity, shared design, or structural blueprint", "word_in_context_of_plane": "history as covenant — the deliberate pact or engineering plan that mandated the connection"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "unshakable unity, mutual trust, and combined resilience", "word_in_context_of_plane": "effect as fellowship — the comforting resilience and deep trust of an unbroken union"}
        }
    },
    "split": {
        "action": "strike seam, separate parts, divide integrity",
        "strain": "bonded, unified, solid",
        "effect": "fissured, separated, divided",
        "definitive_meaning": "to apply force along a seam and divide an entity into distinct separate parts",
        "concept_type": "genotype",
        "parent_word": None,
        "topology": {"closure_level": 1, "boundary_type": "wall_threshold", "operations": ["divide", "sever"]},
        "planes": {
            "Q1": {"interrogative": "Who", "plane": "MetaPhysical", "anchor": "Identity", "answer": "the dividing force establishing distinct entities", "word_in_context_of_plane": "identity as individuation — an entity severing shared bonds to establish independent sovereignty"},
            "Q2": {"interrogative": "What", "plane": "Possible", "anchor": "Possible", "answer": "fault lines, dual paths, and separate portions", "word_in_context_of_plane": "possibility as bifurcation — a single trajectory parting into multiple independent avenues"},
            "Q3": {"interrogative": "Where", "plane": "Physical", "anchor": "Location", "answer": "the fissure, fault line, and cleaving seam", "word_in_context_of_plane": "location as fissure — the physical rupture line along which material separates into pieces"},
            "Q4": {"interrogative": "Why", "plane": "Lyrical", "anchor": "Meaning", "answer": "releasing trapped tension and creating autonomy", "word_in_context_of_plane": "meaning as division — cleaving rigid structures so that independent elements chart their own path"},
            "Q5": {"interrogative": "How", "plane": "Logical", "anchor": "Mechanical", "answer": "driving wedge along fault line and forcing halves apart", "word_in_context_of_plane": "logic as cleaving — concentrating mechanical wedge pressure along natural cleavage planes"},
            "Q6": {"interrogative": "Cause", "plane": "Historical", "anchor": "Historical", "answer": "mounting internal shear, ideological rift, or wedge impact", "word_in_context_of_plane": "history as fracture — the accumulated internal strain that made division inevitable"},
            "Q7": {"interrogative": "Effect", "plane": "Emotive", "anchor": "Emotive", "answer": "separate independence, severed continuity, and clear boundary", "word_in_context_of_plane": "effect as parting — the sharp clarity and distinct independence of divided paths"}
        }
    }
}

# Alias clusters for words that map directly to existing primitives
ALIAS_CLUSTERS = {
    "run": {"primitive_word": "move", "connotation": "high-velocity kinetic displacement"},
    "walk": {"primitive_word": "move", "connotation": "steady moderate locomotive displacement"},
    "travel": {"primitive_word": "go", "connotation": "long-distance geographic traversal"},
    "drop": {"primitive_word": "fall", "connotation": "sudden vertical descent"},
    "hit": {"primitive_word": "strike", "connotation": "violent impact contact"},
    "contain": {"primitive_word": "have", "connotation": "passive spatial enclosure"},
    "grab": {"primitive_word": "take", "connotation": "rapid aggressive acquisition"},
    "keep": {"primitive_word": "hold", "connotation": "continuous temporal custody"},
    "collect": {"primitive_word": "gather", "connotation": "systematic deliberate aggregation"},
    "start": {"primitive_word": "begin", "connotation": "initial activation of process"},
    "stop": {"primitive_word": "halt", "connotation": "cessation of active motion"},
    "look": {"primitive_word": "see", "connotation": "directed visual attention"}
}

def load_v2_dictionary():
    with open(AEC_DICT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_v2_dictionary(data):
    with open(AEC_DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    # Also auto-rebuild aec_dictionary.js for CORS-free viewing
    js_path = os.path.join(V2_DIR, "aec_dictionary.js")
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(f"// Auto-generated distribution file for Reality Classification v2\nwindow.AEC_DICT = {json.dumps(data, ensure_ascii=False)};\n")

def process_pipeline():
    with open(SOURCE_PATH, "r", encoding="utf-8") as f:
        source_data = json.load(f)

    v2_dict = load_v2_dictionary()
    aec_forms = v2_dict.get("aec_forms", {})
    word_index = v2_dict.get("word_index", {})

    print(f"=== EPISTEMIC PRIMITIVE HUNTER PIPELINE (Pure AEC-First) ===")
    print(f"Loaded {len(source_data['words'])} seed candidate words.")
    print(f"Current V2 Dictionary: {len(aec_forms)} AEC Invariant Forms, {len(word_index)} mapped words.\n")

    novel_forms_added = 0
    aliases_linked = 0

    # 1. Process Vetted Models First
    for word, model in VETTED_EPISTEMIC_MODELS.items():
        actions = [a.strip() for a in model["action"].split(",")]
        strains = [s.strip() for s in model["strain"].split(",")]
        effects = [e.strip() for e in model["effect"].split(",")]
        aec_key = f"{', '.join(actions)} -> {', '.join(strains)} -> {', '.join(effects)}"

        if aec_key not in aec_forms:
            form_id = f"AEC-{len(aec_forms) + 1:03d}"
            clean_planes = {}
            for q_id, p_data in model["planes"].items():
                clean_planes[q_id] = {
                    "interrogative": p_data.get("interrogative", ""),
                    "dimension": p_data.get("plane", ""),
                    "anchor": p_data.get("anchor", ""),
                    "manifestation_answer": p_data.get("answer", ""),
                    "process_in_context": p_data.get("word_in_context_of_plane", "")
                }

            node = {
                "form_id": form_id,
                "invariant_triad": {
                    "action": actions,
                    "strain": strains,
                    "effect": effects,
                    "summary": aec_key
                },
                "definitive_process": model["definitive_meaning"],
                "concept_type": model["concept_type"],
                "topology": model["topology"],
                "descriptive_words": {
                    "primary_label": word,
                    "aliases": [],
                    "planar_vocabulary": {f"Q{i}": [] for i in range(1, 8)}
                },
                "planes": clean_planes,
                "related_forms": []
            }
            aec_forms[aec_key] = node
            novel_forms_added += 1
            print(f"[NEW AEC FORM MINTED] {form_id}: {aec_key} (Labeled: '{word}')")

        # Map word to this AEC form
        if word not in word_index:
            word_index[word] = {
                "form_id": aec_forms[aec_key]["form_id"],
                "aec_key": aec_key,
                "role": "primary_label"
            }

    # 2. Process Alias Clusters
    for word, mapping in ALIAS_CLUSTERS.items():
        target_word = mapping["primitive_word"]
        if target_word in word_index:
            target_entry = word_index[target_word]
            target_key = target_entry["aec_key"]

            if word not in word_index:
                word_index[word] = {
                    "form_id": target_entry["form_id"],
                    "aec_key": target_key,
                    "role": "alias",
                    "connotation": mapping["connotation"]
                }
                # Add to aliases of AEC Form
                if word not in aec_forms[target_key]["descriptive_words"]["aliases"]:
                    aec_forms[target_key]["descriptive_words"]["aliases"].append(word)
                aliases_linked += 1
                print(f"[ALIAS LINKED] '{word}' => Attached to {target_entry['form_id']} [{mapping['connotation']}]")

    # Update metadata
    v2_dict["metadata"]["total_aec_forms"] = len(aec_forms)
    v2_dict["metadata"]["total_indexed_words"] = len(word_index)
    v2_dict["aec_forms"] = aec_forms
    v2_dict["word_index"] = word_index

    save_v2_dictionary(v2_dict)

    print("\n=== PIPELINE EXECUTION SUMMARY ===")
    print(f"Novel AEC Invariant Forms Minted: {novel_forms_added}")
    print(f"Descriptive Surface Aliases Linked: {aliases_linked}")
    print(f"Total AEC Invariant Forms: {len(aec_forms)}")
    print(f"Total Words Mapped to AEC Forms: {len(word_index)}")

if __name__ == "__main__":
    process_pipeline()
