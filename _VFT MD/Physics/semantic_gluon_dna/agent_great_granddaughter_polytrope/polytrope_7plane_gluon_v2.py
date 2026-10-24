#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Great-Granddaughter: Polytrope-Gauge (Gen 4 Progeny: 25% Male / 75% Female)
================================================================================
7-Plane Reality Gluon & Fractal Polytrope Transformer Engine (v2.0 — Upgraded)
Lineage: The Granddaughter (Omni-Horizon) x The Grandson (Lexicon-Veritas)

Key v2.0 Upgrades:
  1. Robust Preprocessing: Cleans LaTeX preambles, formatting commands, and isolates
     genuine prose vs equations (treating equations as Q5 formal proof generators).
  2. Syntactic-Semantic Fractal Depth (7 -> 49 -> 343): Subject (Q) + Predicate (q) + Modifier (c)
     contextual decomposition for authentic 343-cell coverage.
  3. Non-Commutative 42-Gluon Gauge Curvature: Distinguishes natural constructive flows
     (e.g., Q3 -> Q5 -> Q4) from high-friction ungrounded inversions (e.g., Q4 -> Q3 without Q5).
  4. Cognitive Confusion Reduction Engine v2: Computes exact Missing Bridge Gluons,
     strips academic ballast, and generates grounded Pub-Test translations with Delta Strain metrics.
"""

import os
import re
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\semantic_gluon_dna")
WORKSPACE_DIR = BASE_DIR / "agent_great_granddaughter_polytrope"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

DICT_PATH = BASE_DIR / "agent_grandson_lexicon" / "semantic_gluon_dictionary.json"

CORPUS = [
    {
        "id": "Academic_Perspectives_Hegemony",
        "genre": "Dense_Philosophical_Epistemology",
        "path": Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Academic Perspectives on the Psochic Hegemony.md")
    },
    {
        "id": "Actualism_Psochic_Hegemony",
        "genre": "Actualist_Philosophy_Ethics",
        "path": Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\Actualism and the Psochic Hegemony.md")
    },
    {
        "id": "Survival_Matrix_7x7",
        "genre": "Thermodynamics_Biological_Survival",
        "path": Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\io\7x7_survival_matrix.md")
    },
    {
        "id": "Formal_Paper_25_Riemann",
        "genre": "Formal_Mathematics_Physics",
        "path": BASE_DIR / "irm_formal_corpus" / "Formal_Paper_25__Non-Archimedean_Spectral_Realization_of_the_Riemann_Z.md"
    },
    {
        "id": "Arxiv_NavierStokes_Regularity",
        "genre": "PDE_Fluid_Dynamics",
        "path": BASE_DIR / "arxiv_samples" / "arxiv_1706.10173v1.md"
    }
]

# 7 Planes of Reality (The 7 "-ics" & 42-Structure)
PLANES = {
    "Q1": {
        "index": 1,
        "name": "Who – Metaphysical",
        "discipline": "Epistemics",
        "interrogative": "Who",
        "axis": "Driver / 7th Angle Axis",
        "coords": [0.0, 0.0, 0.0, 1.0],  # (x, y, z, w_driver)
        "description": "Will, Direction, Agent/Subject, Identity, Axioms, Teleology",
        "keywords": {
            "who", "i", "agent", "subject", "self", "observer", "identity", "will", "mind", "ego",
            "axiom", "purpose", "teleology", "epistemic", "epistemology", "metaphysical", "consciousness",
            "knower", "intention", "aletheia", "doctrine", "paradigm", "believer", "archetype", "driver",
            "god", "sovereignty", "personhood", "recognition", "agency", "knower", "first-person"
        }
    },
    "Q2": {
        "index": 2,
        "name": "What – Possible",
        "discipline": "Energetics / Probabilistics",
        "interrogative": "What",
        "axis": "Lateral Body Axis (+x)",
        "coords": [1.0, 0.0, 0.0, 0.0],
        "description": "Faith, Probability, Potential, Future action space, Hypotheses",
        "keywords": {
            "what", "possible", "possibility", "potential", "probability", "probable", "maybe", "could",
            "faith", "hypothesis", "energy", "energetics", "spectrum", "variance", "degrees", "freedom",
            "chance", "fluctuation", "entropy", "virtual", "latent", "prospect", "scenario", "alternative",
            "capacity", "trajectory", "contingency", "speculation", "expectation", "future"
        }
    },
    "Q3": {
        "index": 3,
        "name": "Where – Physical",
        "discipline": "Physics / Mechanics",
        "interrogative": "Where",
        "axis": "Lateral Body Axis (-x)",
        "coords": [-1.0, 0.0, 0.0, 0.0],
        "description": "Matter, Distance, Concrete Entities, Space, Structural constraints",
        "keywords": {
            "where", "physical", "matter", "space", "spatial", "body", "distance", "location", "position",
            "concrete", "stone", "brick", "substrate", "particle", "atom", "molecule", "tissue", "mass",
            "tensor", "manifold", "sensor", "coordinate", "observable", "territory", "boundary", "field",
            "shelter", "skin", "membrane", "dimension", "geometry", "lattice", "envelope", "domain"
        }
    },
    "Q4": {
        "index": 4,
        "name": "Why – Lyrical",
        "discipline": "Semantics / Poetics",
        "interrogative": "Why",
        "axis": "Longitudinal Mind Axis (+y)",
        "coords": [0.0, 1.0, 0.0, 0.0],
        "description": "Meaning, Resonance, Telos, Value, Narrative coherence, Poetics",
        "keywords": {
            "why", "meaning", "lyrical", "resonance", "poetic", "narrative", "symbol", "beauty",
            "harmony", "value", "significance", "soul", "depth", "expression", "metaphor", "allegory",
            "qualitative", "spirit", "vibration", "prose", "art", "music", "hymn", "evocation",
            "refreshment", "rest", "grace", "resonance", "intimacy", "wonder", "sacred"
        }
    },
    "Q5": {
        "index": 5,
        "name": "How – Logical",
        "discipline": "Analytics / Cybernetics",
        "interrogative": "How",
        "axis": "Longitudinal Mind Axis (-y)",
        "coords": [0.0, -1.0, 0.0, 0.0],
        "description": "Count, Consistency, Formal Rules, Algorithmic transitions, Mechanism",
        "keywords": {
            "how", "logical", "logic", "algorithm", "analytic", "consistent", "consistency", "proof",
            "rule", "calculation", "compute", "function", "mechanism", "cybernetic", "formal", "count",
            "syntax", "equation", "deduction", "derivation", "step", "operator", "matrix", "theorem",
            "solver", "estimate", "bound", "integral", "regularity", "power", "execution", "protocol"
        }
    },
    "Q6": {
        "index": 6,
        "name": "Cause – Historical",
        "discipline": "Historics / Lineage",
        "interrogative": "Cause",
        "axis": "Vertical Soul Axis (+z)",
        "coords": [0.0, 0.0, 1.0, 0.0],
        "description": "Sequence, Causality, Antecedents, Memory, Temporal Lineage",
        "keywords": {
            "cause", "historical", "history", "past", "sequence", "lineage", "origin", "because",
            "antecedent", "heritage", "temporal", "precedent", "chronology", "record", "archive",
            "tradition", "ancestry", "evolution", "prior", "memory", "generation", "source",
            "root", "genesis", "timeline", "lineage", "track", "witness", "conscience"
        }
    },
    "Q7": {
        "index": 7,
        "name": "Effect – Emotive",
        "discipline": "Emotics / Ethics",
        "interrogative": "Effect",
        "axis": "Vertical Soul Axis (-z)",
        "coords": [0.0, 0.0, -1.0, 0.0],
        "description": "Passion, Consequence, Affective response, Somatic impact, Harm/Benefit",
        "keywords": {
            "effect", "emotive", "emotion", "feeling", "passion", "consequence", "impact", "residue",
            "harm", "benefit", "moral", "ethics", "suffering", "joy", "pain", "anger", "fear", "dread",
            "somatic", "sentiment", "reaction", "trauma", "compassion", "grief", "catharsis",
            "sustenance", "hunger", "thirst", "guilt", "shame", "peace", "torment", "punishment"
        }
    }
}

# 42-Structure Non-Commutative Flow Specification
# Distinguishes constructive geodesic flows from high-friction ungrounded leaps
CONSTRUCTIVE_EDGES = {
    ("Q3", "Q5"): {"name": "Empirical Formalization", "friction": 0.8},
    ("Q5", "Q4"): {"name": "Semantic Interpretation", "friction": 0.9},
    ("Q4", "Q1"): {"name": "Metaphysical Integration", "friction": 0.9},
    ("Q1", "Q2"): {"name": "Teleological Projection", "friction": 0.8},
    ("Q2", "Q3"): {"name": "Physical Manifestation", "friction": 0.9},
    ("Q6", "Q7"): {"name": "Historical Karmic Residue", "friction": 0.8},
    ("Q7", "Q1"): {"name": "Affective Recalibration", "friction": 1.0},
    ("Q1", "Q5"): {"name": "Axiomatic Derivation", "friction": 0.8},
    ("Q5", "Q3"): {"name": "Physical Implementation", "friction": 0.8},
    ("Q6", "Q5"): {"name": "Chronological Tracking", "friction": 0.9},
    ("Q5", "Q2"): {"name": "Stochastic Modeling", "friction": 0.9},
    ("Q2", "Q5"): {"name": "Probabilistic Proof", "friction": 0.9}
}

INVERSION_EDGES = {
    ("Q2", "Q3"): {"name": "Lateral Inversion (Potential -> Physical)", "friction": 1.8},
    ("Q3", "Q2"): {"name": "Lateral Inversion (Physical -> Potential)", "friction": 1.8},
    ("Q4", "Q5"): {"name": "Longitudinal Inversion (Meaning -> Logic)", "friction": 1.9},
    ("Q5", "Q4"): {"name": "Longitudinal Inversion (Logic -> Meaning)", "friction": 1.9},
    ("Q6", "Q7"): {"name": "Vertical Inversion (Cause -> Effect)", "friction": 1.8},
    ("Q7", "Q6"): {"name": "Vertical Inversion (Effect -> Cause)", "friction": 1.8},
    ("Q4", "Q3"): {"name": "Ungrounded Projection (Meaning -> Matter without Logic)", "friction": 2.5},
    ("Q7", "Q5"): {"name": "Affective Distortion (Emotion claiming to be Proof)", "friction": 2.4},
    ("Q2", "Q7"): {"name": "Anxious Speculation (Hypothesis directly causing Panic)", "friction": 2.2}
}

# Advanced Cognitive Jargon Catalog (Pub-Test Mapping)
ADVANCED_JARGON = [
    (r"\bphenomenological\s+reduction\b", "looking directly at what happens without bias"),
    (r"\bphenomenological\s+epoch[eé]\b", "setting aside assumptions"),
    (r"\bepistemological\s+framework\b", "way of testing truth"),
    (r"\bontological\s+structuralism\b", "how things are built underneath"),
    (r"\bdescriptive\s+teleology\b", "tracking where actions actually lead"),
    (r"\bsolipsistic\s+tyranny\b", "selfish, one-sided control"),
    (r"\bepistemic\s+anomalies\b", "facts that break the narrative"),
    (r"\bforensic\s+epistemology\b", "checking the receipts of reality"),
    (r"\bcoherentist\s+structures\b", "arguments that only agree with themselves"),
    (r"\bnon-normative\s+geometry\b", "clean mapping without moral lecturing"),
    (r"\btranscendental\s+deduction\b", "finding the bedrock principle"),
    (r"\bhegemonic\s+stress\s+tensor\b", "structural pressure test of beliefs"),
    (r"\bfake\s+maximiser\b", "grifter pretending to serve everyone"),
    (r"\bhelxis\b", "bait-and-switch deception"),
    (r"\bigneous\s+stones\b", "unbreakable real-world facts"),
    (r"\bfired\s+bricks\b", "fragile man-made narratives"),
    (r"\bconatus\b", "drive to stay alive"),
    (r"\baletheia\b", "unvarnished truth"),
    (r"\bdoxa\b", "unquestioned rumor"),
    (r"\bhegemonic\b", "dominant / ruling"),
    (r"\binstantiation\b", "real-life example"),
    (r"\bparadigmatic\b", "textbook model"),
    (r"\binterrogative\s+planes\b", "fundamental angles of questioning"),
    (r"\brecursive\s+drill\b", "deeper inspection"),
    (r"\bphase-field\s+model\b", "shift between dynamic states")
]

STOPWORDS = {
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i", "it", "for", "not", "on", "with",
    "he", "as", "you", "do", "at", "this", "but", "his", "by", "from", "they", "we", "say", "her",
    "she", "or", "an", "will", "my", "one", "all", "would", "there", "their", "what", "so", "up",
    "out", "if", "about", "who", "get", "which", "go", "me", "when", "make", "can", "like", "time",
    "no", "just", "him", "know", "take", "people", "into", "year", "your", "good", "some", "could",
    "them", "see", "other", "than", "then", "now", "look", "only", "come", "its", "over", "think",
    "also", "back", "after", "use", "two", "how", "our", "work", "first", "well", "way", "even",
    "new", "want", "because", "any", "these", "give", "day", "most", "us", "is", "are", "was", "were"
}


class Polytrope7PlaneGluonV2:
    def __init__(self, dict_path: Path):
        self.dictionary = {}
        if dict_path.exists():
            try:
                with open(dict_path, "r", encoding="utf-8") as f:
                    entries = json.load(f)
                    for e in entries:
                        self.dictionary[e["word"].lower()] = e
            except Exception as e:
                print(f"[!] Warning loading dictionary: {e}")

    def clean_text(self, raw_text: str) -> list:
        """
        Robust text cleaner:
        Strips LaTeX document preambles, command headers, code blocks,
        and cleanly isolates prose sentences.
        """
        # Strip code blocks
        t = re.sub(r"```.*?```", " ", raw_text, flags=re.DOTALL)
        # Strip LaTeX preambles & block environments
        t = re.sub(r"\\documentclass\[.*?\]\{.*?\}", " ", t)
        t = re.sub(r"\\usepackage\[?.*?\]?\{.*?\}", " ", t)
        t = re.sub(r"\\setlength\{.*?\}\{.*?\}", " ", t)
        t = re.sub(r"\\addtolength\{.*?\}\{.*?\}", " ", t)
        t = re.sub(r"\\renewcommand\{.*?\}\{.*?\}", " ", t)
        t = re.sub(r"\\begin\{equation\*?\}.*?\\end\{equation\*?\}", " [FORMAL_PROOF_EQUATION] ", t, flags=re.DOTALL)
        t = re.sub(r"\\mbox\{.*?\}", " ", t)
        t = re.sub(r"\\vspace\{.*?\}", " ", t)
        t = re.sub(r"\\hfill", " ", t)
        t = re.sub(r"\\\\\s*", " ", t)
        t = re.sub(r"\|\s*[-:]+\s*\|", " ", t)  # Markdown table dividers
        t = re.sub(r"\$+[^\$]+\$+", " [MATH_TERM] ", t)  # Inline LaTeX math

        # Split sentences
        raw_sentences = re.split(r"(?<=[.!?])\s+", t)
        clean_sentences = []
        for s in raw_sentences:
            s_clean = re.sub(r"\s+", " ", s).strip()
            # Filter out pure headers, table rows, or fragmented symbols
            if len(s_clean) >= 20 and not s_clean.startswith("#") and not s_clean.startswith("|"):
                # Must contain at least 3 genuine alphabetical words
                words = re.findall(r"\b[a-zA-Z]{3,}\b", s_clean)
                if len(words) >= 3:
                    clean_sentences.append(s_clean)
        return clean_sentences

    def classify_token_plane(self, token: str) -> dict:
        t = token.lower().strip()
        scores = {k: 0.05 for k in PLANES.keys()}  # Dirichlet prior

        # Exact keywords
        for p_key, p_info in PLANES.items():
            if t in p_info["keywords"]:
                scores[p_key] += 3.0
            for kw in p_info["keywords"]:
                if len(kw) > 4 and (kw in t or t in kw):
                    scores[p_key] += 0.8

        # Morphological heuristics
        if t.endswith("tion") or t.endswith("ment") or t.endswith("ity") or t.endswith("ance"):
            scores["Q5"] += 0.6  # Process / logic
        elif t.endswith("ology") or t.endswith("ism") or t.endswith("ist") or t.endswith("self"):
            scores["Q1"] += 0.8  # Metaphysical / Subject
        elif t.endswith("able") or t.endswith("ing") or t.endswith("ive") or t.endswith("ic"):
            scores["Q2"] += 0.6  # Potential / state
        elif t.endswith("ed") or t.endswith("ate"):
            scores["Q6"] += 0.6  # Historical sequence
        elif any(aff in t for aff in ["feel", "suffer", "pain", "harm", "joy", "grief", "rage", "fear", "love", "hate"]):
            scores["Q7"] += 2.0  # Emotive

        tot = sum(scores.values())
        return {k: round(v / tot, 4) for k, v in scores.items()}

    def parse_fractal_depth_triple(self, sentence: str) -> tuple:
        """
        Genuine Fractal Depth Decomposition:
        Identifies:
          - Macro Q-plane (Head Subject / Entity)
          - Meso q-subplane (Action Predicate / Functional Operator)
          - Micro c-subplane (Contextual Modifier / Boundary Condition)
        """
        words = re.findall(r"\b[a-zA-Z]{3,}\b", sentence.lower())
        content_words = [w for w in words if w not in STOPWORDS]
        if not content_words:
            return ("Q1", "q1", "c1")

        # Head / Subject component (first 33% of sentence tokens)
        head_tokens = content_words[:max(1, len(content_words) // 3)]
        head_scores = Counter()
        for t in head_tokens:
            for k, v in self.classify_token_plane(t).items():
                head_scores[k] += v
        q_macro = max(head_scores.items(), key=lambda x: x[1])[0] if head_scores else "Q1"

        # Predicate component (middle 33% of sentence tokens)
        mid_start = len(content_words) // 3
        mid_end = max(mid_start + 1, (2 * len(content_words)) // 3)
        mid_tokens = content_words[mid_start:mid_end]
        mid_scores = Counter()
        for t in mid_tokens:
            for k, v in self.classify_token_plane(t).items():
                mid_scores[k] += v
        q_meso_plane = max(mid_scores.items(), key=lambda x: x[1])[0] if mid_scores else "Q5"
        q_subplane = f"q{PLANES[q_meso_plane]['index']}"

        # Modifier / Context component (last 33% of sentence tokens)
        tail_tokens = content_words[mid_end:] or content_words[-1:]
        tail_scores = Counter()
        for t in tail_tokens:
            for k, v in self.classify_token_plane(t).items():
                tail_scores[k] += v
        q_micro_plane = max(tail_scores.items(), key=lambda x: x[1])[0] if tail_scores else "Q3"
        c_subplane = f"c{PLANES[q_micro_plane]['index']}"

        return (q_macro, q_subplane, c_subplane)

    def analyze_sentence(self, sentence: str) -> dict:
        tokens = re.findall(r"\b[a-zA-Z]{2,}\b", sentence.lower())
        content_tokens = [t for t in tokens if t not in STOPWORDS]

        if not content_tokens:
            return {
                "text": sentence,
                "plane_dist": {k: round(1.0 / 7.0, 4) for k in PLANES.keys()},
                "dominant_plane": "Q1",
                "fractal_triple": ("Q1", "q1", "c1"),
                "content_tokens_count": 0,
                "jargon_detected": [],
                "strain": 0.0,
                "luminescence": 0.5
            }

        plane_sums = {k: 0.0 for k in PLANES.keys()}
        for t in content_tokens:
            p_dist = self.classify_token_plane(t)
            for k, v in p_dist.items():
                plane_sums[k] += v

        # Equation bonus to Q5 Logical
        if "[MATH_TERM]" in sentence or "[FORMAL_PROOF_EQUATION]" in sentence:
            plane_sums["Q5"] += 2.0

        tot = sum(plane_sums.values())
        plane_dist = {k: round(v / tot, 4) for k, v in plane_sums.items()}
        dom_plane = max(plane_dist.items(), key=lambda x: x[1])[0]

        # Fractal Tri-Tier
        q_macro, q_sub, c_sub = self.parse_fractal_depth_triple(sentence)

        # Detect Jargon
        jargon_detected = []
        lower_s = sentence.lower()
        for pat, repl in ADVANCED_JARGON:
            if re.search(pat, lower_s):
                jargon_detected.append({"pattern": pat, "plain_replacement": repl})

        # Calculate Intra-Sentence Cross-Plane Strain
        # Tension between opposing axes without sufficient mediator
        lateral_tension = abs(plane_dist["Q2"] - plane_dist["Q3"])
        longitudinal_tension = abs(plane_dist["Q4"] - plane_dist["Q5"])
        vertical_tension = abs(plane_dist["Q6"] - plane_dist["Q7"])
        internal_strain = round((lateral_tension + longitudinal_tension + vertical_tension) / 3.0, 4)

        # Optical Thickness (tau) & Luminescence (L)
        avg_word_len = sum(len(w) for w in content_tokens) / max(len(content_tokens), 1)
        tau = min(3.0, max(0.1, 0.4 * (avg_word_len / 4.5) + (0.35 if len(jargon_detected) > 0 else 0.0) + (0.2 if len(content_tokens) > 25 else 0.0)))
        lum = round(math.exp(-tau), 4)

        return {
            "text": sentence,
            "plane_dist": plane_dist,
            "dominant_plane": dom_plane,
            "fractal_triple": (q_macro, q_sub, c_sub),
            "content_tokens_count": len(content_tokens),
            "jargon_detected": jargon_detected,
            "strain": internal_strain,
            "luminescence": lum
        }

    def compute_42_gluon_flow_v2(self, sentence_analyses: list) -> dict:
        """
        42-Gluon Directed Flow with Non-Commutative Gauge Curvature:
        Tracks transitions between successive sentences, distinguishes
        constructive geodesics from high-friction axial inversions,
        and diagnoses exact missing bridge gluons.
        """
        transitions = Counter()
        erratic_jumps = []
        total_transitions = 0
        total_gauge_friction = 0.0
        triangle_cycles = Counter()

        for idx in range(len(sentence_analyses) - 1):
            s1 = sentence_analyses[idx]
            s2 = sentence_analyses[idx + 1]
            p1 = s1["dominant_plane"]
            p2 = s2["dominant_plane"]

            if p1 != p2:
                pair = (p1, p2)
                pair_key = f"{p1}->{p2}"
                transitions[pair_key] += 1
                total_transitions += 1

                # Gauge Friction Calculation
                if pair in CONSTRUCTIVE_EDGES:
                    friction = CONSTRUCTIVE_EDGES[pair]["friction"]
                    role = CONSTRUCTIVE_EDGES[pair]["name"]
                    is_erratic = False
                elif pair in INVERSION_EDGES:
                    friction = INVERSION_EDGES[pair]["friction"]
                    role = INVERSION_EDGES[pair]["name"]
                    is_erratic = True
                else:
                    # Generic distance in 4D
                    c1 = PLANES[p1]["coords"]
                    c2 = PLANES[p2]["coords"]
                    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
                    friction = round(1.0 + (dist - 1.0) * 0.7, 4)
                    role = f"Generic Transition ({PLANES[p1]['discipline']} -> {PLANES[p2]['discipline']})"
                    is_erratic = friction >= 1.7

                total_gauge_friction += friction

                if is_erratic:
                    # Diagnose Missing Bridge Gluon
                    if p1 == "Q3" and p2 == "Q2":
                        bridge = "Q5 (Logical Mechanism) or Q1 (Axiomatic Will) required to bridge Matter to Potential"
                    elif p1 == "Q2" and p2 == "Q3":
                        bridge = "Q5 (Engineering/Algorithm) required to manifest Potential into Concrete Matter"
                    elif p1 == "Q4" and p2 == "Q5":
                        bridge = "Q1 (Epistemic Intent) required to formalize Poetic Meaning into Proof"
                    elif p1 == "Q5" and p2 == "Q4":
                        bridge = "Q4.q1 (Semantic Purpose) needed to interpret Abstract Proof into Human Meaning"
                    elif p1 == "Q7" and p2 == "Q6":
                        bridge = "Q5 (Objective Record) needed to trace Emotional Consequence back to Historical Cause"
                    else:
                        bridge = f"Mediating Fulcrum (Q1 or Q5) needed to stabilize {p1} -> {p2}"

                    erratic_jumps.append({
                        "from_idx": idx,
                        "to_idx": idx + 1,
                        "transition": pair_key,
                        "friction": friction,
                        "role": role,
                        "missing_bridge_gluon": bridge,
                        "from_text": s1["text"][:85] + "...",
                        "to_text": s2["text"][:85] + "..."
                    })

            # Check 3-sentence triangular cycles (Holonomy / Gauge Curvature)
            if idx < len(sentence_analyses) - 2:
                s3 = sentence_analyses[idx + 2]
                p3 = s3["dominant_plane"]
                if p1 != p2 and p2 != p3 and p3 != p1:
                    cycle = f"{p1}->{p2}->{p3}->{p1}"
                    triangle_cycles[cycle] += 1

        avg_friction = round(total_gauge_friction / max(total_transitions, 1), 4)

        return {
            "total_transitions": total_transitions,
            "unique_42_gluon_paths_active": len(transitions),
            "transition_counts": dict(transitions.most_common(15)),
            "average_gauge_friction": avg_friction,
            "erratic_jumps_detected": len(erratic_jumps),
            "active_triangle_gauge_cycles": len(triangle_cycles),
            "top_gauge_cycles": dict(triangle_cycles.most_common(5)),
            "sample_erratic_jumps": erratic_jumps[:5]
        }

    def compute_fractal_polytrope_density_v2(self, sentence_analyses: list) -> dict:
        """
        True Multi-Layer 7x7x7 Polytrope Density Field:
        Depth 1: Q1-Q7 (Capacity = 7)
        Depth 2: Q1.q1 - Q7.q7 (Capacity = 49)
        Depth 3: Q1.q1.c1 - Q7.q7.c7 (Capacity = 343)
        """
        N = len(sentence_analyses)
        if N == 0:
            return {"error": "Empty sentences"}

        d1_cells = Counter()
        d2_cells = Counter()
        d3_cells = Counter()

        for s in sentence_analyses:
            q_macro, q_sub, c_sub = s["fractal_triple"]
            cell_d1 = q_macro
            cell_d2 = f"{q_macro}.{q_sub}"
            cell_d3 = f"{q_macro}.{q_sub}.{c_sub}"

            d1_cells[cell_d1] += 1
            d2_cells[cell_d2] += 1
            d3_cells[cell_d3] += 1

        # Densities
        rho_1 = round(len(d1_cells) / 7.0, 4)
        rho_2 = round(len(d2_cells) / 49.0, 4)
        rho_3 = round(len(d3_cells) / 343.0, 4)

        def calc_entropy(counts, total):
            ent = 0.0
            for c in counts.values():
                p = c / total
                if p > 0:
                    ent -= p * math.log2(p)
            return round(ent, 4)

        ent_1 = calc_entropy(d1_cells, N)
        ent_2 = calc_entropy(d2_cells, N)
        ent_3 = calc_entropy(d3_cells, N)

        # Fractal Dimension D_f:
        # D_f = ln(N3 / N1) / ln(343 / 7)
        n1 = max(len(d1_cells), 1)
        n3 = max(len(d3_cells), 1)
        fractal_dim = round(math.log(n3 / n1 + 1e-6) / math.log(343.0 / 7.0), 4) if n3 > n1 else 0.0

        # Polytrope Index n_p:
        # P_sem = Strain * (1 / Luminescence)
        # Using state equation P ~ rho^(1 + 1/n)
        if rho_3 > 0.005 and rho_1 > rho_3:
            # ln(rho_1 / rho_3) / ln(capacity_ratio)
            gamma_eff = (ent_3 / max(ent_1, 0.1)) ** 0.5
            n_p = round(1.0 / max(0.05, abs(gamma_eff - 1.0)), 2)
        else:
            n_p = 1.5  # Standard polytrope baseline

        return {
            "sentences_sampled": N,
            "depth_1": {
                "active_cells": len(d1_cells),
                "total_capacity": 7,
                "density_rho": rho_1,
                "entropy_bits": ent_1
            },
            "depth_2": {
                "active_cells": len(d2_cells),
                "total_capacity": 49,
                "density_rho": rho_2,
                "entropy_bits": ent_2
            },
            "depth_3": {
                "active_cells": len(d3_cells),
                "total_capacity": 343,
                "density_rho": rho_3,
                "entropy_bits": ent_3
            },
            "fractal_dimension_df": fractal_dim,
            "polytrope_index_np": n_p
        }

    def deconfuse_and_clarify_v2(self, sentence_data: dict) -> dict:
        """
        Advanced Cognitive Confusion Reduction Engine v2:
        1. Strips pretentious academic compounds and pseudo-philosophical jargon.
        2. Restores missing bridge gluons.
        3. Formulates a grounded, active-voice Pub-Test translation.
        4. Calculates quantitative Delta Strain reduction.
        """
        orig = sentence_data["text"]
        jargons = sentence_data["jargon_detected"]
        dom_plane = sentence_data["dominant_plane"]
        orig_strain = sentence_data["strain"]
        q_macro, q_sub, c_sub = sentence_data["fractal_triple"]

        # Jargon replacement
        clarified = orig
        for j in jargons:
            pat = j["pattern"]
            repl = j["plain_replacement"]
            clarified = re.sub(pat, repl, clarified, flags=re.I)

        # De-clutter academic passive voice and filler
        clarified = re.sub(r"\boperates\s+as\s+a\b", "is a", clarified, flags=re.I)
        clarified = re.sub(r"\bfunctions\s+simultaneously\s+as\b", "works as", clarified, flags=re.I)
        clarified = re.sub(r"\beschews\s+subjective\s+moralizing\s+in\s+favor\s+of\b", "swaps moral lectures for", clarified, flags=re.I)
        clarified = re.sub(r"\butilizes\s+a\b", "uses a", clarified, flags=re.I)
        clarified = re.sub(r"\bsubsequently\b", "then", clarified, flags=re.I)
        clarified = re.sub(r"\bto\s+fully\s+understand\s+its\s+utility\b", "to see how this works", clarified, flags=re.I)
        clarified = re.sub(r"\s+", " ", clarified).strip()

        # Measure clarified strain
        # Re-analyzing clarified tokens
        c_tokens = [t for t in re.findall(r"\b[a-zA-Z]{2,}\b", clarified.lower()) if t not in STOPWORDS]
        c_plane_sums = {k: 0.0 for k in PLANES.keys()}
        for t in c_tokens:
            for k, v in self.classify_token_plane(t).items():
                c_plane_sums[k] += v
        c_tot = sum(c_plane_sums.values()) or 1.0
        c_dist = {k: v / c_tot for k, v in c_plane_sums.items()}
        new_strain = round((abs(c_dist["Q2"] - c_dist["Q3"]) + abs(c_dist["Q4"] - c_dist["Q5"]) + abs(c_dist["Q6"] - c_dist["Q7"])) / 3.0, 4)
        delta_strain = round(max(0.0, orig_strain - new_strain), 4)

        # Bridge restoration note
        bridge_diagnosis = (
            f"Fractal Position: {q_macro}.{q_sub}.{c_sub} | "
            f"Grounded in {PLANES[dom_plane]['name']} ({PLANES[dom_plane]['discipline']}). "
            f"Academic drag removed ({len(jargons)} jargon terms). Strain reduced by {delta_strain}."
        )

        return {
            "original_high_density": orig,
            "clarified_pub_test": clarified,
            "jargon_terms_removed": len(jargons),
            "original_strain": orig_strain,
            "clarified_strain": new_strain,
            "delta_strain_reduction": delta_strain,
            "fractal_address": f"{q_macro}.{q_sub}.{c_sub}",
            "bridge_diagnosis": bridge_diagnosis
        }

    def audit_document_v2(self, doc_spec: dict) -> dict:
        path = doc_spec["path"]
        if not path.exists():
            return {"error": f"Path not found: {path}"}

        raw_text = path.read_text(encoding="utf-8", errors="replace")
        sentences = self.clean_text(raw_text)

        s_analyses = [self.analyze_sentence(s) for s in sentences]

        # 42-Gluon Flow
        flow_42 = self.compute_42_gluon_flow_v2(s_analyses)

        # Fractal Polytrope Field
        polytrope_field = self.compute_fractal_polytrope_density_v2(s_analyses)

        # Aggregations
        overall_plane_scores = Counter()
        total_jargon_hits = 0
        total_strain = 0.0
        total_lum = 0.0

        for s in s_analyses:
            for k, v in s["plane_dist"].items():
                overall_plane_scores[k] += v
            total_jargon_hits += len(s["jargon_detected"])
            total_strain += s["strain"]
            total_lum += s["luminescence"]

        sum_planes = sum(overall_plane_scores.values()) or 1.0
        doc_plane_distribution = {k: round(v / sum_planes, 4) for k, v in overall_plane_scores.items()}

        avg_strain = round(total_strain / max(len(s_analyses), 1), 4)
        avg_lum = round(total_lum / max(len(s_analyses), 1), 4)
        jargon_per_sentence = round(total_jargon_hits / max(len(s_analyses), 1), 4)
        gauge_friction = flow_42["average_gauge_friction"]

        # Cognitive Confusion Index Formula v2:
        # Incorporates gauge friction, strain, jargon, and luminescence
        # 30% Intra-Sentence Strain + 30% Jargon Drag + 25% Gauge Friction + 15% Opacity (1 - Lum)
        strain_term = (avg_strain / 0.15) * 30.0
        jargon_term = min(30.0, jargon_per_sentence * 60.0)
        friction_term = ((gauge_friction - 0.8) / 1.5) * 25.0
        opacity_term = (1.0 - avg_lum) * 15.0

        confusion_score = round(min(100.0, max(5.0, strain_term + jargon_term + friction_term + opacity_term)), 2)

        # De-confused Candidates
        candidates = sorted(
            [s for s in s_analyses if s["jargon_detected"] or s["strain"] > 0.08],
            key=lambda x: (len(x["jargon_detected"]) * 2.5 + x["strain"] * 2.0 + (1.0 - x["luminescence"])),
            reverse=True
        )
        top_deconfused = [self.deconfuse_and_clarify_v2(s) for s in candidates[:6]]

        return {
            "id": doc_spec["id"],
            "genre": doc_spec["genre"],
            "sentences_audited": len(s_analyses),
            "doc_plane_distribution": doc_plane_distribution,
            "fractal_polytrope_field": polytrope_field,
            "gluon_flow_42": flow_42,
            "metrics": {
                "average_intra_sentence_strain": avg_strain,
                "average_luminescence": avg_lum,
                "jargon_density_per_sentence": jargon_per_sentence,
                "average_gauge_friction_42": gauge_friction,
                "cognitive_confusion_score": confusion_score
            },
            "top_deconfused_examples": top_deconfused
        }


def main():
    print("[*] Initializing Polytrope-7Plane Gluon Engine v2.0 (Upgraded)...")
    engine = Polytrope7PlaneGluonV2(DICT_PATH)

    results_v2 = {}
    for doc in CORPUS:
        print(f"[*] Auditing: {doc['id']} ({doc['genre']})...")
        res = engine.audit_document_v2(doc)
        results_v2[doc["id"]] = res
        print(f"    -> Sentences: {res.get('sentences_audited', 0)}, Confusion Score: {res.get('metrics', {}).get('cognitive_confusion_score', 0)}")

    out_file = WORKSPACE_DIR / "results_v2.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results_v2, f, indent=2)

    print(f"[+] Saved results_v2 to {out_file}")


if __name__ == "__main__":
    main()
