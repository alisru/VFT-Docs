"""
Sentence-Level Semantic Gluon DNA Engine - Competitor 1 (Strict Verifier: 75% Male / 25% Female)
================================================================================================
Focus: Hard Boundary Defense, Causal Debt Invariant, Exon Preservation, Zero False-Positives.
Evaluates sentences as DNA codons along a 5' -> 3' reading strand.
Uses real neural sentence embeddings (FastEmbed), 7 Q-Planes, QCD Cornell Confinement,
and hard String Snapping to eliminate ungrounded leaps.
"""

import os
import sys
import re
import math
import time
import json
import numpy as np
from typing import List, Dict, Tuple, Any

# Ensure src is on path for local_sentence_embedder
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from local_sentence_embedder import LocalSentenceEmbedder

# Physics Constants
ALPHA_S = 0.35        # Strong coupling constant
SIGMA = 0.85          # String tension parameter
M_QUARK = 0.65        # Effective constituent quark mass
R_CRITICAL = (2.0 * M_QUARK + ALPHA_S) / SIGMA  # ~1.529 (String snapping threshold)

# The 7 Planes of Reality (42-Structure)
PLANES = [
    "Q1_Metaphysical",  # Who - Will, Intent, Epistemics
    "Q2_Possible",      # What - Potential, Superposition, Faith
    "Q3_Physical",      # Where - Matter, Space, Sensor, Distance
    "Q4_Lyrical",       # Why - Meaning, Resonance, Poetics
    "Q5_Logical",       # How - Analytics, Consistency, Equation
    "Q6_Historical",    # Cause - Precedent, Sequence, Lineage
    "Q7_Emotive"        # Effect - Passion, Strain, Somatic
]

# Non-Commutative Directional Gauge Friction Matrix (7x7)
GAUGE_FRICTION = {
    ("Q3_Physical", "Q5_Logical"): 0.80,       # Natural grounding: empirical observation to logic
    ("Q5_Logical", "Q4_Lyrical"): 0.85,       # Logic resolves into meaning
    ("Q4_Lyrical", "Q1_Metaphysical"): 0.90,  # Meaning informs conscious sovereignty
    ("Q1_Metaphysical", "Q2_Possible"): 0.95, # Will explores options
    ("Q2_Possible", "Q3_Physical"): 1.00,     # Potential collapses into matter
    ("Q4_Lyrical", "Q3_Physical"): 2.50,      # Inverted Leap: claiming physical reality from metaphor
    ("Q7_Emotive", "Q5_Logical"): 2.40,       # Inverted Leap: emotional outrage posing as formal proof
    ("Q1_Metaphysical", "Q5_Logical"): 1.80,  # Ideological fiat demanding logical validity
}

def get_gauge_friction(p1: str, p2: str) -> float:
    if p1 == p2:
        return 0.50
    if (p1, p2) in GAUGE_FRICTION:
        return GAUGE_FRICTION[(p1, p2)]
    # Default metric distance between plane indices
    idx1 = int(p1[1])
    idx2 = int(p2[1])
    return 1.0 + abs(idx1 - idx2) * 0.20

class StrictVerifierSentenceDNA:
    def __init__(self):
        print("[Agent 1 - Strict Verifier (75M/25F)] Initializing Local Neural Embedder...")
        self.embedder = LocalSentenceEmbedder()
        self._init_plane_anchors()

    def _init_plane_anchors(self):
        """Initializes canonical anchor propositions for the 7 Q-Planes to calibrate projections."""
        anchor_texts = [
            "Conscious sovereign intent, personal will, selfhood, and metaphysical agency.", # Q1
            "Future potential, uncommitted optionality, probability distribution, and superposition.", # Q2
            "Physical matter, spatial distance, sensory coordinates, atoms, and observable ground.", # Q3
            "Lyrical resonance, poetic depth, overarching purpose, and existential meaning.", # Q4
            "Logical consistency, mathematical equations, formal deduction, algorithmic proof, and causality.", # Q5
            "Historical origin, precedent, genealogical lineage, ancestral timeline, and antecedent cause.", # Q6
            "Somatic passion, emotional suffering, visceral reaction, grief, joy, and experiential effect." # Q7
        ]
        self.plane_anchors = self.embedder.embed(anchor_texts) # [7, D]

    def split_into_sentences(self, text: str) -> List[str]:
        """Splits markdown prose cleanly into semantic sentences, removing headers and raw formatting."""
        # Normalize whitespace
        clean_lines = []
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith('#') or s.startswith('---'):
                continue
            clean_lines.append(s)
        joined = " ".join(clean_lines)
        
        # Regex split on sentence boundaries
        raw_sents = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"\'\*\$])', joined)
        sentences = []
        for s in raw_sents:
            s_clean = s.strip()
            # Must be substantial enough to be a sentence
            if len(s_clean.split()) >= 4:
                sentences.append(s_clean)
        return sentences

    def classify_planes(self, sentence_embs: np.ndarray) -> List[Tuple[str, float]]:
        """Projects sentence embeddings onto the 7 Q-Planes via cosine similarity to invariant anchors."""
        norm_embs = sentence_embs / np.linalg.norm(sentence_embs, axis=1, keepdims=True)
        sims = np.dot(norm_embs, self.plane_anchors.T) # [N, 7]
        # Softmax with temperature
        exp_sims = np.exp(sims * 4.0)
        probs = exp_sims / np.sum(exp_sims, axis=1, keepdims=True)
        
        results = []
        for i in range(len(probs)):
            top_idx = int(np.argmax(probs[i]))
            results.append((PLANES[top_idx], float(probs[i, top_idx])))
        return results

    def compute_qcd_color_charges(self, sentence: str) -> Tuple[float, float, float, bool]:
        """
        SU(3) Color Gauge:
          Red   (r): Directional Premise / Assertive Will / Thesis
          Green (g): Operational Mechanism / Intermediate Action / Context
          Blue  (b): Invariant Constraint / Boundary / Deductive Proof
        """
        s_low = sentence.lower()
        
        r_markers = len(re.findall(r'\b(will|shall|must|is|defines|demands|acts|asserts|thesis|purpose|sovereign)\b', s_low))
        g_markers = len(re.findall(r'\b(can|could|through|via|operates|transfers|mechanism|context|moves|process)\b', s_low))
        b_markers = len(re.findall(r'\b(not|cannot|impossible|boundary|constraint|proves|therefore|hence|yields|axiom|invariant)\b', s_low))
        
        # Total
        tot = (r_markers * 1.5) + (g_markers * 1.2) + (b_markers * 1.8) + 1e-4
        cr = (r_markers * 1.5) / tot
        cg = (g_markers * 1.2) / tot
        cb = (b_markers * 1.8) / tot
        
        # White Singlet Hadron: Balanced representation of all three colors
        is_singlet = (cr >= 0.15 and cg >= 0.15 and cb >= 0.15 and (max(cr, cg, cb) - min(cr, cg, cb) < 0.45))
        return round(float(cr), 3), round(float(cg), 3), round(float(cb), 3), is_singlet

    def evaluate_ribosomal_splicing(self, sentence: str, plane: str, confidence: float) -> Tuple[str, str]:
        """
        Agent 1 Strict Verifier Splicing Gate:
        Exon = High semantic substance, formal definition, physical or logical axiom.
        Intron = Conversational filler, meta-announcements ('in this section we will discuss'), vague transitions.
        """
        s_low = sentence.lower()
        words = sentence.split()
        
        # Intron patterns
        is_meta_intron = bool(re.search(r'\b(in this section|let us now|we have seen|as mentioned earlier|skip to|click here|note that)\b', s_low))
        is_short_fragment = len(words) < 6
        is_pure_rhetoric = bool(re.search(r'\b(obviously|needless to say|simply put|in other words)\b', s_low)) and len(words) < 10
        
        if is_meta_intron or is_short_fragment or is_pure_rhetoric:
            return "INTRON", "Conversational filler or rhetorical padding without empirical invariant."
        
        # Exon criteria: strong plane alignment or formal assertion
        has_axiom = bool(re.search(r'\b(formula|action|effect|strain|physics|definition|invariant|equation|constant|law|always|never)\b', s_low))
        if has_axiom or confidence >= 0.25:
            return "EXON", "Causal invariant or operational mechanism."
        
        return "EXON", "Standard propositions with informational content."

    def compute_consecutive_bonds(self, sentences: List[str], sentence_embs: np.ndarray, planes: List[str]) -> List[Dict[str, Any]]:
        """
        Computes the Gluon Flux Tube tension between consecutive sentences S_i -> S_{i+1}:
          Effective distance: r_eff = ||h_{i+1} - h_i|| * Gamma(P_i, P_{i+1})
          Cornell Potential: V(r) = -alpha_s / r + sigma * r
          String Snapping: r_eff >= R_CRITICAL (1.529)
        """
        bonds = []
        n = len(sentences)
        
        norm_embs = sentence_embs / np.linalg.norm(sentence_embs, axis=1, keepdims=True)
        
        for i in range(n - 1):
            s1, s2 = sentences[i], sentences[i+1]
            p1, p2 = planes[i], planes[i+1]
            
            # Semantic Euclidean distance on hypersphere: d = sqrt(2 * (1 - cos_sim))
            cos_sim = float(np.dot(norm_embs[i], norm_embs[i+1]))
            cos_sim = max(-1.0, min(1.0, cos_sim))
            euclid_d = math.sqrt(max(0.0, 2.0 * (1.0 - cos_sim)))
            
            # Modulate by directional gauge friction
            friction = get_gauge_friction(p1, p2)
            r_eff = euclid_d * friction
            
            # Cornell Potential
            v_cornell = -ALPHA_S / (r_eff + 0.01) + SIGMA * r_eff
            is_snapped = (r_eff >= R_CRITICAL)
            
            # Causal Debt Check: Does S2 claim "therefore/proves" when S1 was an ungrounded leap?
            s2_low = s2.lower()
            claims_proof = bool(re.search(r'\b(therefore|thus|hence|proves|consequently|yields|so we see)\b', s2_low))
            causal_debt_penalty = 0.0
            if claims_proof and is_snapped:
                causal_debt_penalty = 2.50 # Severe penalty for unearned conclusion ('maths without working out')
                v_cornell += causal_debt_penalty
            
            bonds.append({
                "from_index": i,
                "to_index": i + 1,
                "p1": p1,
                "p2": p2,
                "euclidean_dist": round(euclid_d, 4),
                "gauge_friction": round(friction, 3),
                "r_effective": round(r_eff, 4),
                "v_cornell": round(v_cornell, 4),
                "string_snapped": is_snapped,
                "causal_debt_flag": claims_proof and is_snapped
            })
            
        return bonds

    def process_document(self, text: str) -> Dict[str, Any]:
        """Executes full sentence-level Semantic Gluon DNA analysis on input text."""
        start_time = time.time()
        sentences = self.split_into_sentences(text)
        if not sentences:
            return {"error": "No valid sentences extracted."}
            
        # 1. Embed sentences
        sentence_embs = self.embedder.embed(sentences)
        
        # 2. Classify Planes
        plane_results = self.classify_planes(sentence_embs)
        planes = [p[0] for p in plane_results]
        confidences = [p[1] for p in plane_results]
        
        # 3. Compute QCD Colors & Splicing
        codons = []
        for i, s in enumerate(sentences):
            cr, cg, cb, is_singlet = self.compute_qcd_color_charges(s)
            splicing_type, reason = self.evaluate_ribosomal_splicing(s, planes[i], confidences[i])
            codons.append({
                "index": i,
                "text": s,
                "plane": planes[i],
                "plane_confidence": round(confidences[i], 3),
                "color_charges": {"red": cr, "green": cg, "blue": cb},
                "is_hadron_singlet": is_singlet,
                "splicing": splicing_type,
                "splicing_reason": reason
            })
            
        # 4. Compute Consecutive Sentence Gluon Bonds
        bonds = self.compute_consecutive_bonds(sentences, sentence_embs, planes)
        
        # 5. Extract Distilled Exon Backbone
        exons = [c["text"] for c in codons if c["splicing"] == "EXON"]
        introns = [c["text"] for c in codons if c["splicing"] == "INTRON"]
        
        total_snaps = sum(1 for b in bonds if b["string_snapped"])
        total_causal_debts = sum(1 for b in bonds if b["causal_debt_flag"])
        
        runtime_ms = (time.time() - start_time) * 1000.0
        
        return {
            "agent": "Competitor 1: Strict Verifier (75M / 25F)",
            "metrics": {
                "total_sentences": len(sentences),
                "retained_exons": len(exons),
                "culled_introns": len(introns),
                "culling_rate_pct": round(100.0 * len(introns) / len(sentences), 2),
                "string_snapping_events": total_snaps,
                "causal_debt_violations": total_causal_debts,
                "hadron_singlet_count": sum(1 for c in codons if c["is_hadron_singlet"]),
                "runtime_ms": round(runtime_ms, 2)
            },
            "codons": codons,
            "gluon_bonds": bonds,
            "distilled_exon_backbone": exons
        }
