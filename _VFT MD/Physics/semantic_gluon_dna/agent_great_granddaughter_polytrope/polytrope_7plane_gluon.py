#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Great-Granddaughter: Polytrope-Gauge (Gen 4 Progeny: 25% Male / 75% Female)
================================================================================
7-Plane Reality Gluon & Fractal Polytrope Transformer Engine (v1.0)
Lineage: The Granddaughter (Omni-Horizon) x The Grandson (Lexicon-Veritas)
Mandate:
  1. The 7 Planes of Reality (The 7 "-ics") & 42-Structure Gauge Flow.
  2. Fractal Polytrope Density Field (7 -> 49 -> 343 recursive scaling).
  3. Cognitive Confusion Reduction Engine (Strain calculation, Missing Bridge Gluons,
     and Grounded Plain English Translation).
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

# Benchmark Corpus
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
        "id": "Formal_Paper_25_Riemann",
        "genre": "Formal_Mathematics_Physics",
        "path": BASE_DIR / "irm_formal_corpus" / "Formal_Paper_25__Non-Archimedean_Spectral_Realization_of_the_Riemann_Z.md"
    },
    {
        "id": "Arxiv_Attention_Transformer",
        "genre": "Computer_Science_AI",
        "path": BASE_DIR / "arxiv_samples" / "arxiv_1706.10173v1.md"
    }
]

# 7 Planes of Reality Specification
PLANES = {
    "Q1": {
        "index": 1,
        "name": "Who – Metaphysical",
        "discipline": "Epistemics",
        "axis": "Driver / 7th Angle Axis",
        "coords": [0.0, 0.0, 0.0, 1.0],  # (x, y, z, w_driver)
        "description": "Will, Direction, Agent/Subject, Identity, Axioms, Teleology",
        "keywords": {
            "who", "i", "agent", "subject", "self", "observer", "identity", "will", "mind", "ego",
            "axiom", "purpose", "teleology", "epistemic", "epistemology", "metaphysical", "consciousness",
            "knower", "intention", "aletheia", "doctrine", "paradigm", "believer", "archetype", "driver"
        }
    },
    "Q2": {
        "index": 2,
        "name": "What – Possible",
        "discipline": "Energetics / Probabilistics",
        "axis": "Lateral Body Axis (+x)",
        "coords": [1.0, 0.0, 0.0, 0.0],
        "description": "Faith, Probability, Potential, Future action space, Hypotheses",
        "keywords": {
            "what", "possible", "possibility", "potential", "probability", "probable", "maybe", "could",
            "faith", "hypothesis", "energy", "energetics", "spectrum", "variance", "degrees", "freedom",
            "chance", "fluctuation", "entropy", "virtual", "latent", "prospect", "scenario", "alternative"
        }
    },
    "Q3": {
        "index": 3,
        "name": "Where – Physical",
        "discipline": "Physics / Mechanics",
        "axis": "Lateral Body Axis (-x)",
        "coords": [-1.0, 0.0, 0.0, 0.0],
        "description": "Matter, Distance, Concrete Entities, Space, Structural constraints",
        "keywords": {
            "where", "physical", "matter", "space", "spatial", "body", "distance", "location", "position",
            "concrete", "stone", "brick", "substrate", "particle", "atom", "molecule", "tissue", "mass",
            "tensor", "manifold", "sensor", "coordinate", "observable", "territory", "boundary", "field"
        }
    },
    "Q4": {
        "index": 4,
        "name": "Why – Lyrical",
        "discipline": "Semantics / Poetics",
        "axis": "Longitudinal Mind Axis (+y)",
        "coords": [0.0, 1.0, 0.0, 0.0],
        "description": "Meaning, Resonance, Telos, Value, Narrative coherence, Poetics",
        "keywords": {
            "why", "meaning", "lyrical", "resonance", "poetic", "narrative", "symbol", "beauty",
            "harmony", "value", "significance", "soul", "depth", "expression", "metaphor", "allegory",
            "qualitative", "spirit", "vibration", "prose", "art", "music", "hymn", "evocation"
        }
    },
    "Q5": {
        "index": 5,
        "name": "How – Logical",
        "discipline": "Analytics / Cybernetics",
        "axis": "Longitudinal Mind Axis (-y)",
        "coords": [0.0, -1.0, 0.0, 0.0],
        "description": "Count, Consistency, Formal Rules, Algorithmic transitions, Mechanism",
        "keywords": {
            "how", "logical", "logic", "algorithm", "analytic", "consistent", "consistency", "proof",
            "rule", "calculation", "compute", "function", "mechanism", "cybernetic", "formal", "count",
            "syntax", "equation", "deduction", "derivation", "step", "operator", "matrix", "theorem"
        }
    },
    "Q6": {
        "index": 6,
        "name": "Cause – Historical",
        "discipline": "Historics / Lineage",
        "axis": "Vertical Soul Axis (+z)",
        "coords": [0.0, 0.0, 1.0, 0.0],
        "description": "Sequence, Causality, Antecedents, Memory, Temporal Lineage",
        "keywords": {
            "cause", "historical", "history", "past", "sequence", "lineage", "origin", "because",
            "antecedent", "heritage", "temporal", "precedent", "chronology", "record", "archive",
            "tradition", "ancestry", "evolution", "prior", "memory", "generation", "source"
        }
    },
    "Q7": {
        "index": 7,
        "name": "Effect – Emotive",
        "discipline": "Emotics / Ethics",
        "axis": "Vertical Soul Axis (-z)",
        "coords": [0.0, 0.0, -1.0, 0.0],
        "description": "Passion, Consequence, Affective response, Somatic impact, Harm/Benefit",
        "keywords": {
            "effect", "emotive", "emotion", "feeling", "passion", "consequence", "impact", "residue",
            "harm", "benefit", "moral", "ethics", "suffering", "joy", "pain", "anger", "fear", "dread",
            "somatic", "sentiment", "reaction", "trauma", "compassion", "grief", "catharsis"
        }
    }
}

# The 42-Structure: 7 x 6 Directed Bridge Gluons between distinct planes
BRIDGE_GLUONS_42 = {}
plane_keys = list(PLANES.keys())
for i, src in enumerate(plane_keys):
    for j, tgt in enumerate(plane_keys):
        if src != tgt:
            key = f"{src}->{tgt}"
            # Geometric distance in (x,y,z,w)
            c1 = PLANES[src]["coords"]
            c2 = PLANES[tgt]["coords"]
            dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
            
            # Bridge function archetype
            if src == "Q3" and tgt == "Q5":
                role = "Empirical Formalization (Matter -> Logic)"
            elif src == "Q5" and tgt == "Q4":
                role = "Semantic Interpretation (Logic -> Meaning)"
            elif src == "Q1" and tgt == "Q2":
                role = "Teleological Projection (Will -> Possibility)"
            elif src == "Q2" and tgt == "Q3":
                role = "Physical Instantiation (Possibility -> Matter)"
            elif src == "Q6" and tgt == "Q7":
                role = "Moral Consequence (History -> Emotive Effect)"
            elif src == "Q7" and tgt == "Q1":
                role = "Affective Recalibration (Effect -> Will)"
            elif src == "Q5" and tgt == "Q3":
                role = "Engineering Implementation (Logic -> Physical)"
            elif dist >= 2.0:
                role = f"Axial Inversion Jump ({PLANES[src]['axis']} -> {PLANES[tgt]['axis']})"
            else:
                role = f"Cross-Plane Transition ({PLANES[src]['discipline']} -> {PLANES[tgt]['discipline']})"

            BRIDGE_GLUONS_42[key] = {
                "source": src,
                "target": tgt,
                "distance": round(dist, 4),
                "role": role,
                "requires_mediator": dist > 1.5
            }

# Jargon Dictionary for Cognitive Confusion Filtering
JARGON_PATTERNS = [
    (r"\bphenomenological\s+reduction\b", "looking at what's really there without assumptions"),
    (r"\bepistemological\s+framework\b", "way of knowing"),
    (r"\bontological\s+structuralism\b", "structure of reality"),
    (r"\bdescriptive\s+teleology\b", "tracking where actions lead"),
    (r"\bsolipsistic\s+tyranny\b", "selfish domination"),
    (r"\bepistemic\s+anomalies\b", "facts that don't fit the theory"),
    (r"\bforensic\s+epistemology\b", "fact-checking reality"),
    (r"\bcoherentist\s+structures\b", "stories that only agree with themselves"),
    (r"\bnon-normative\s+geometry\b", "straight-up mapping without moralizing"),
    (r"\btranscendental\s+deduction\b", "working out the necessary bedrock"),
    (r"\bconatus\b", "will to persist"),
    (r"\bepoch[eé]\b", "setting aside bias"),
    (r"\baletheia\b", "unvarnished truth"),
    (r"\bdoxa\b", "untested popular opinion"),
    (r"\bhegemonic\b", "ruling / dominant"),
    (r"\binstantiation\b", "concrete example"),
    (r"\bparadigmatic\b", "standard model"),
    (r"\brecursive\s+drill\b", "deeper investigation")
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


class Polytrope7PlaneGluon:
    def __init__(self, dict_path: Path):
        self.dictionary = {}
        if dict_path.exists():
            with open(dict_path, "r", encoding="utf-8") as f:
                entries = json.load(f)
                for e in entries:
                    self.dictionary[e["word"].lower()] = e

    def classify_token_plane(self, token: str) -> dict:
        """Score token across the 7 Planes of Reality."""
        t = token.lower().strip()
        scores = {k: 0.05 for k in PLANES.keys()}  # Baseline non-zero Dirichlet prior

        # Check explicit keywords
        for p_key, p_info in PLANES.items():
            if t in p_info["keywords"]:
                scores[p_key] += 2.0
            for kw in p_info["keywords"]:
                if len(kw) > 4 and (kw in t or t in kw):
                    scores[p_key] += 0.8

        # Suffix and morphological heuristics
        if t.endswith("tion") or t.endswith("ment") or t.endswith("ance"):
            scores["Q5"] += 0.5  # Logical / process
        if t.endswith("ology") or t.endswith("ism") or t.endswith("ist"):
            scores["Q1"] += 0.7  # Metaphysical / Epistemic
        if t.endswith("ness") or t.endswith("ity"):
            scores["Q4"] += 0.5  # Lyrical / state of being
        if t.endswith("ic") or t.endswith("ical"):
            scores["Q5"] += 0.4  # Formal
        if t.endswith("ed"):
            scores["Q6"] += 0.5  # Historical / past
        if t.endswith("ing") or t.endswith("able") or t.endswith("ive"):
            scores["Q2"] += 0.5  # Potential / capability
        if any(aff in t for aff in ["feel", "suffer", "pain", "harm", "joy", "grief", "rage", "fear"]):
            scores["Q7"] += 1.5  # Emotive

        # Normalize
        tot = sum(scores.values())
        return {k: round(v / tot, 4) for k, v in scores.items()}

    def analyze_sentence(self, sentence: str) -> dict:
        tokens = re.findall(r"\b[a-zA-Z]{2,}\b", sentence.lower())
        content_tokens = [t for t in tokens if t not in STOPWORDS]
        
        if not content_tokens:
            return {
                "text": sentence,
                "plane_dist": {k: round(1.0 / 7.0, 4) for k in PLANES.keys()},
                "dominant_plane": "Q1",
                "content_tokens_count": 0,
                "jargon_detected": [],
                "strain": 0.0
            }

        # Aggregate plane scores
        plane_sums = {k: 0.0 for k in PLANES.keys()}
        for t in content_tokens:
            p_dist = self.classify_token_plane(t)
            for k, v in p_dist.items():
                plane_sums[k] += v

        tot = sum(plane_sums.values())
        plane_dist = {k: round(v / tot, 4) for k, v in plane_sums.items()}
        dom_plane = max(plane_dist.items(), key=lambda x: x[1])[0]

        # Detect academic jargon
        jargon_detected = []
        lower_s = sentence.lower()
        for pat, repl in JARGON_PATTERNS:
            if re.search(pat, lower_s):
                jargon_detected.append({"pattern": pat, "plain_replacement": repl})

        # Calculate Intra-Sentence Strain: variance across polar axes
        # Strain increases when contradictory polar planes are evoked simultaneously without logical grounding
        lateral_strain = abs(plane_dist["Q2"] - plane_dist["Q3"])
        longitudinal_strain = abs(plane_dist["Q4"] - plane_dist["Q5"])
        vertical_strain = abs(plane_dist["Q6"] - plane_dist["Q7"])
        internal_strain = round((lateral_strain + longitudinal_strain + vertical_strain) / 3.0, 4)

        return {
            "text": sentence,
            "plane_dist": plane_dist,
            "dominant_plane": dom_plane,
            "content_tokens_count": len(content_tokens),
            "jargon_detected": jargon_detected,
            "strain": internal_strain
        }

    def compute_42_gluon_flow(self, sentence_analyses: list) -> dict:
        """Trace the 7-color gluon flow across the 42-structure between sentences."""
        transitions = Counter()
        erratic_jumps = []
        total_transitions = 0
        total_jump_strain = 0.0

        for idx in range(len(sentence_analyses) - 1):
            s1 = sentence_analyses[idx]
            s2 = sentence_analyses[idx + 1]
            p1 = s1["dominant_plane"]
            p2 = s2["dominant_plane"]

            if p1 != p2:
                pair_key = f"{p1}->{p2}"
                transitions[pair_key] += 1
                total_transitions += 1
                
                gluon_info = BRIDGE_GLUONS_42.get(pair_key, {})
                jump_dist = gluon_info.get("distance", 1.414)
                total_jump_strain += jump_dist

                # Flag erratic jumps: distance >= 2.0 (axial inversions) without bridging
                if jump_dist >= 2.0:
                    erratic_jumps.append({
                        "from_sentence_idx": idx,
                        "to_sentence_idx": idx + 1,
                        "transition": pair_key,
                        "distance": jump_dist,
                        "issue": gluon_info.get("role", "Axial Inversion"),
                        "from_text": s1["text"][:80] + "...",
                        "to_text": s2["text"][:80] + "..."
                    })

        avg_jump_strain = round(total_jump_strain / max(total_transitions, 1), 4)

        return {
            "total_transitions": total_transitions,
            "unique_42_gluon_paths_active": len(transitions),
            "transition_counts": dict(transitions.most_common(15)),
            "average_jump_strain": avg_jump_strain,
            "erratic_jumps_detected": len(erratic_jumps),
            "sample_erratic_jumps": erratic_jumps[:5]
        }

    def compute_fractal_polytrope_density(self, content_words: list) -> dict:
        """
        Calculate the Fractal Polytrope Density Field across 3 recursive depths:
        Depth 1: Q-planes (7^1 = 7)
        Depth 2: Qq-subplanes (7^2 = 49)
        Depth 3: Qqc-subsubplanes (7^3 = 343)
        """
        N = len(content_words)
        if N == 0:
            return {"error": "No content words"}

        # Depth 1: 7 Q-planes
        d1_counts = Counter()
        # Depth 2: 49 Qq-subplanes
        d2_counts = Counter()
        # Depth 3: 343 Qqc-subsubplanes
        d3_counts = Counter()

        for w in content_words:
            p_dist = self.classify_token_plane(w)
            top_q = max(p_dist.items(), key=lambda x: x[1])[0]
            d1_counts[top_q] += 1

            # Sub-plane heuristic: second highest plane determines q-subplane
            sorted_planes = sorted(p_dist.items(), key=lambda x: x[1], reverse=True)
            top_sub_q = sorted_planes[1][0]
            qq_key = f"{top_q}.{top_sub_q.lower()}"
            d2_counts[qq_key] += 1

            # Sub-subplane heuristic: third highest plane determines c-subplane
            top_sub_sub_q = sorted_planes[2][0]
            qqc_key = f"{top_q}.{top_sub_q.lower()}.c{PLANES[top_sub_sub_q]['index']}"
            d3_counts[qqc_key] += 1

        # Calculate density fields
        rho_1 = round(len(d1_counts) / 7.0, 4)
        rho_2 = round(len(d2_counts) / 49.0, 4)
        rho_3 = round(len(d3_counts) / 343.0, 4)

        # Shannon Entropy for each depth
        def calc_entropy(counts, total):
            ent = 0.0
            for c in counts.values():
                p = c / total
                if p > 0:
                    ent -= p * math.log2(p)
            return round(ent, 4)

        ent_1 = calc_entropy(d1_counts, N)
        ent_2 = calc_entropy(d2_counts, N)
        ent_3 = calc_entropy(d3_counts, N)

        # Polytrope Index n_p estimation:
        # Scaling of information compression: ratio of entropy increase to dimensional capacity increase
        # Delta S / Delta log2(Capacity)
        delta_s_1_2 = ent_2 - ent_1
        delta_cap_1_2 = math.log2(49) - math.log2(7)  # log2(7) = 2.807
        compression_ratio = round(delta_s_1_2 / delta_cap_1_2, 4)

        # Polytrope Index n: P ~ rho^(1 + 1/n)
        # If density collapses rapidly under depth, n is small (high pressure star); if spread evenly, n is high
        if rho_3 > 0.01:
            polytrope_index = round(1.0 / max(0.01, (rho_1 / rho_3) ** 0.5 - 1.0), 2)
        else:
            polytrope_index = 0.5

        return {
            "total_content_tokens": N,
            "depth_1": {
                "active_cells": len(d1_counts),
                "total_capacity": 7,
                "density_rho": rho_1,
                "entropy_bits": ent_1
            },
            "depth_2": {
                "active_cells": len(d2_counts),
                "total_capacity": 49,
                "density_rho": rho_2,
                "entropy_bits": ent_2
            },
            "depth_3": {
                "active_cells": len(d3_counts),
                "total_capacity": 343,
                "density_rho": rho_3,
                "entropy_bits": ent_3
            },
            "polytrope_compression_ratio": compression_ratio,
            "polytrope_index_np": polytrope_index
        }

    def deconfuse_and_clarify(self, sentence_data: dict) -> dict:
        """
        Cognitive Confusion Reduction:
        Identify jargon, high cross-plane strain, and produce a grounded, plain-English rewrite.
        """
        text = sentence_data["text"]
        jargons = sentence_data["jargon_detected"]
        dom_plane = sentence_data["dominant_plane"]
        strain = sentence_data["strain"]

        # Plain English replacement
        clarified = text
        for j in jargons:
            pat = j["pattern"]
            repl = j["plain_replacement"]
            clarified = re.sub(pat, repl, clarified, flags=re.I)

        # Simplify convoluted punctuation and academic clutter
        clarified = re.sub(r"\s+", " ", clarified).strip()

        # Generate bridging explanation
        bridge_note = f"Grounded in {PLANES[dom_plane]['name']} ({PLANES[dom_plane]['discipline']})."
        if strain > 0.35:
            bridge_note += f" [High Tension Detected ({strain}) - re-anchored to direct observation]"

        return {
            "original": text,
            "clarified_pub_test": clarified,
            "jargon_count": len(jargons),
            "dominant_plane": dom_plane,
            "bridge_note": bridge_note
        }

    def audit_document(self, doc_spec: dict) -> dict:
        path = doc_spec["path"]
        if not path.exists():
            return {"error": f"Path not found: {path}"}

        raw_text = path.read_text(encoding="utf-8", errors="replace")
        
        # Split into sentences (filtering headers and code blocks)
        cleaned_text = re.sub(r"```.*?```", "", raw_text, flags=re.DOTALL)
        raw_sentences = re.split(r"(?<=[.!?])\s+", cleaned_text)
        sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 25 and not s.strip().startswith("#")]

        # Sentence-level analyses
        s_analyses = [self.analyze_sentence(s) for s in sentences]
        all_content_tokens = []
        for s in s_analyses:
            tokens = re.findall(r"\b[a-zA-Z]{2,}\b", s["text"].lower())
            all_content_tokens.extend([t for t in tokens if t not in STOPWORDS])

        # 42-Gluon Flow
        flow_42 = self.compute_42_gluon_flow(s_analyses)

        # Fractal Polytrope Field
        polytrope_field = self.compute_fractal_polytrope_density(all_content_tokens)

        # Aggregate Plane Distribution
        overall_plane_scores = Counter()
        total_jargon_hits = 0
        total_strain = 0.0

        for s in s_analyses:
            for k, v in s["plane_dist"].items():
                overall_plane_scores[k] += v
            total_jargon_hits += len(s["jargon_detected"])
            total_strain += s["strain"]

        sum_planes = sum(overall_plane_scores.values()) or 1.0
        doc_plane_distribution = {k: round(v / sum_planes, 4) for k, v in overall_plane_scores.items()}

        # Confusion Score (0-100)
        avg_strain = round(total_strain / max(len(s_analyses), 1), 4)
        jargon_per_sentence = round(total_jargon_hits / max(len(s_analyses), 1), 4)
        jump_strain = flow_42["average_jump_strain"]

        # Confusion Index Formula:
        # 35% Intra-Sentence Strain + 35% Academic Jargon Density + 30% 42-Gluon Jump Strain
        raw_conf = (avg_strain * 35.0) + (min(jargon_per_sentence * 50.0, 35.0)) + ((jump_strain / 2.0) * 30.0)
        confusion_score = round(min(100.0, max(5.0, raw_conf)), 2)

        # Top 5 Most Confusing Sentences & De-confused Rewrites
        confusing_candidates = sorted(
            [s for s in s_analyses if s["jargon_detected"] or s["strain"] > 0.30],
            key=lambda x: (len(x["jargon_detected"]) * 2.0 + x["strain"]),
            reverse=True
        )
        top_deconfused = [self.deconfuse_and_clarify(s) for s in confusing_candidates[:5]]

        return {
            "id": doc_spec["id"],
            "genre": doc_spec["genre"],
            "sentences_audited": len(s_analyses),
            "total_content_tokens": len(all_content_tokens),
            "doc_plane_distribution": doc_plane_distribution,
            "fractal_polytrope_field": polytrope_field,
            "gluon_flow_42": flow_42,
            "metrics": {
                "average_intra_sentence_strain": avg_strain,
                "jargon_density_per_sentence": jargon_per_sentence,
                "average_jump_strain_42": jump_strain,
                "cognitive_confusion_score": confusion_score
            },
            "top_deconfused_examples": top_deconfused
        }


def main():
    print("[*] Initializing Polytrope-7Plane Gluon Engine v1.0...")
    engine = Polytrope7PlaneGluon(DICT_PATH)

    results = {}
    for doc in CORPUS:
        print(f"[*] Auditing: {doc['id']} ({doc['genre']})...")
        res = engine.audit_document(doc)
        results[doc["id"]] = res
        print(f"    -> Sentences: {res.get('sentences_audited', 0)}, Confusion Score: {res.get('metrics', {}).get('cognitive_confusion_score', 0)}")

    out_file = WORKSPACE_DIR / "results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"[+] Saved results to {out_file}")


if __name__ == "__main__":
    main()
