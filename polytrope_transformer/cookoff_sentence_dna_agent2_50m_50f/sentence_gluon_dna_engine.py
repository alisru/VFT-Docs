"""
Sentence-Level Semantic Gluon DNA Engine - Competitor 2 (Equilibrium Arbiter: 50% Male / 50% Female)
==================================================================================================
Focus: Rigor + Synthesis Balance, Self-Healing Bridging Gluons (lambda_3 (x) lambda_8),
       and Dynamic Exon-Intron Co-occurrence Splicing.
Evaluates sentences as DNA codons along a 5' -> 3' reading strand.
When consecutive sentences snap (r >= 1.529), Agent 2 dynamically calculates the intermediate
bridging tensor to heal the causal rupture and identify the missing derivation step.
"""

import os
import sys
import re
import math
import time
import json
import numpy as np
from typing import List, Dict, Tuple, Any

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from local_sentence_embedder import LocalSentenceEmbedder

# Physics Constants
ALPHA_S = 0.35        # Strong coupling constant
SIGMA = 0.85          # String tension parameter
M_QUARK = 0.65        # Constituent quark mass
R_CRITICAL = (2.0 * M_QUARK + ALPHA_S) / SIGMA  # ~1.529

PLANES = [
    "Q1_Metaphysical",  # Who - Will, Agency, Epistemics
    "Q2_Possible",      # What - Potential, Superposition, Optionality
    "Q3_Physical",      # Where - Matter, Space, Coordinates, Sensors
    "Q4_Lyrical",       # Why - Meaning, Resonance, Poetics, Symbol
    "Q5_Logical",       # How - Analytics, Consistency, Formal Logic
    "Q6_Historical",    # Cause - Precedent, Sequence, Lineage
    "Q7_Emotive"        # Effect - Passion, Somatic Strain, Impact
]

GAUGE_FRICTION = {
    ("Q3_Physical", "Q5_Logical"): 0.80,
    ("Q5_Logical", "Q4_Lyrical"): 0.85,
    ("Q4_Lyrical", "Q1_Metaphysical"): 0.90,
    ("Q1_Metaphysical", "Q2_Possible"): 0.95,
    ("Q2_Possible", "Q3_Physical"): 1.00,
    ("Q4_Lyrical", "Q3_Physical"): 2.40,
    ("Q7_Emotive", "Q5_Logical"): 2.30,
    ("Q1_Metaphysical", "Q5_Logical"): 1.70,
}

def get_gauge_friction(p1: str, p2: str) -> float:
    if p1 == p2:
        return 0.50
    if (p1, p2) in GAUGE_FRICTION:
        return GAUGE_FRICTION[(p1, p2)]
    idx1, idx2 = int(p1[1]), int(p2[1])
    return 1.0 + abs(idx1 - idx2) * 0.18

class EquilibriumArbiterSentenceDNA:
    def __init__(self):
        print("[Agent 2 - Equilibrium Arbiter (50M/50F)] Initializing Local Neural Embedder...")
        self.embedder = LocalSentenceEmbedder()
        self._init_plane_anchors()

    def _init_plane_anchors(self):
        anchor_texts = [
            "Conscious sovereign intent, personal will, selfhood, and metaphysical agency.",
            "Future potential, uncommitted optionality, probability distribution, and superposition.",
            "Physical matter, spatial distance, sensory coordinates, atoms, and observable ground.",
            "Lyrical resonance, poetic depth, overarching purpose, and existential meaning.",
            "Logical consistency, mathematical equations, formal deduction, algorithmic proof, and causality.",
            "Historical origin, precedent, genealogical lineage, ancestral timeline, and antecedent cause.",
            "Somatic passion, emotional suffering, visceral reaction, grief, joy, and experiential effect."
        ]
        self.plane_anchors = self.embedder.embed(anchor_texts)

    def split_into_sentences(self, text: str) -> List[str]:
        clean_lines = []
        for line in text.splitlines():
            s = line.strip()
            if not s or s.startswith('#') or s.startswith('---'):
                continue
            clean_lines.append(s)
        joined = " ".join(clean_lines)
        
        raw_sents = re.split(r'(?<=[.!?])\s+(?=[A-Z0-9"\'\*\$])', joined)
        sentences = [s.strip() for s in raw_sents if len(s.strip().split()) >= 4]
        return sentences

    def classify_planes(self, sentence_embs: np.ndarray) -> List[Tuple[str, float]]:
        norm_embs = sentence_embs / np.linalg.norm(sentence_embs, axis=1, keepdims=True)
        sims = np.dot(norm_embs, self.plane_anchors.T)
        exp_sims = np.exp(sims * 4.0)
        probs = exp_sims / np.sum(exp_sims, axis=1, keepdims=True)
        
        results = []
        for i in range(len(probs)):
            top_idx = int(np.argmax(probs[i]))
            results.append((PLANES[top_idx], float(probs[i, top_idx])))
        return results

    def compute_qcd_color_charges(self, sentence: str) -> Tuple[float, float, float, bool]:
        s_low = sentence.lower()
        r_markers = len(re.findall(r'\b(will|shall|must|is|defines|demands|acts|asserts|thesis|purpose|sovereign)\b', s_low))
        g_markers = len(re.findall(r'\b(can|could|through|via|operates|transfers|mechanism|context|moves|process)\b', s_low))
        b_markers = len(re.findall(r'\b(not|cannot|impossible|boundary|constraint|proves|therefore|hence|yields|axiom|invariant)\b', s_low))
        
        tot = (r_markers * 1.5) + (g_markers * 1.2) + (b_markers * 1.8) + 1e-4
        cr = (r_markers * 1.5) / tot
        cg = (g_markers * 1.2) / tot
        cb = (b_markers * 1.8) / tot
        
        is_singlet = (cr >= 0.15 and cg >= 0.15 and cb >= 0.15 and (max(cr, cg, cb) - min(cr, cg, cb) < 0.45))
        return round(float(cr), 3), round(float(cg), 3), round(float(cb), 3), is_singlet

    def evaluate_splicing_balanced(self, sentence: str, plane: str, confidence: float, is_singlet: bool) -> Tuple[str, str]:
        """
        Agent 2 Balanced Splicing:
        Preserves core mathematical and philosophical exons, while keeping necessary semantic transitions.
        Only culls pure conversational metadata or extreme redundancy.
        """
        s_low = sentence.lower()
        words = sentence.split()
        
        if len(words) < 5:
            return "INTRON", "Short non-substantive fragment."
        if bool(re.search(r'\b(in this section|skip to|click here|note that)\b', s_low)) and len(words) < 12:
            return "INTRON", "Navigational/document metadata."
            
        if is_singlet or confidence >= 0.22:
            return "EXON", "Hadron-balanced proposition or high-confidence planar invariant."
        return "EXON", "Informational context exon."

    def synthesize_bridging_gluon(self, emb1: np.ndarray, emb2: np.ndarray, p1: str, p2: str) -> Dict[str, Any]:
        """
        Self-Healing Bridging Gluon Operator lambda_3 (x) lambda_8:
        Computes the intermediate vector in latent space to diagnose what missing plane
        or concept is required to restore continuous causal derivation.
        """
        midpoint = (emb1 + emb2) / 2.0
        norm_mid = midpoint / (np.linalg.norm(midpoint) + 1e-8)
        sims = np.dot(norm_mid, self.plane_anchors.T) # [7]
        best_p_idx = int(np.argmax(sims))
        bridge_plane = PLANES[best_p_idx]
        
        return {
            "bridge_plane": bridge_plane,
            "bridge_confidence": round(float(sims[best_p_idx]), 4),
            "repair_operator": f"lambda_3 (x) lambda_8 :: Traverse {bridge_plane} to close gap from {p1} to {p2}"
        }

    def compute_consecutive_bonds(self, sentences: List[str], sentence_embs: np.ndarray, planes: List[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        bonds = []
        bridges = []
        n = len(sentences)
        norm_embs = sentence_embs / np.linalg.norm(sentence_embs, axis=1, keepdims=True)
        
        for i in range(n - 1):
            p1, p2 = planes[i], planes[i+1]
            cos_sim = float(np.dot(norm_embs[i], norm_embs[i+1]))
            cos_sim = max(-1.0, min(1.0, cos_sim))
            euclid_d = math.sqrt(max(0.0, 2.0 * (1.0 - cos_sim)))
            friction = get_gauge_friction(p1, p2)
            r_eff = euclid_d * friction
            
            v_cornell = -ALPHA_S / (r_eff + 0.01) + SIGMA * r_eff
            is_snapped = (r_eff >= R_CRITICAL)
            
            bridge_info = None
            if is_snapped:
                # Apply Self-Healing Bridging Operator
                bridge_info = self.synthesize_bridging_gluon(norm_embs[i], norm_embs[i+1], p1, p2)
                bridges.append({
                    "rupture_index": i,
                    "from_sentence": sentences[i][:60] + "...",
                    "to_sentence": sentences[i+1][:60] + "...",
                    "bridge": bridge_info
                })
            
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
                "bridged": is_snapped,
                "bridge_plane": bridge_info["bridge_plane"] if bridge_info else None
            })
            
        return bonds, bridges

    def process_document(self, text: str) -> Dict[str, Any]:
        start_time = time.time()
        sentences = self.split_into_sentences(text)
        if not sentences:
            return {"error": "No valid sentences extracted."}
            
        sentence_embs = self.embedder.embed(sentences)
        
        plane_results = self.classify_planes(sentence_embs)
        planes = [p[0] for p in plane_results]
        confidences = [p[1] for p in plane_results]
        
        codons = []
        for i, s in enumerate(sentences):
            cr, cg, cb, is_singlet = self.compute_qcd_color_charges(s)
            splicing_type, reason = self.evaluate_splicing_balanced(s, planes[i], confidences[i], is_singlet)
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
            
        bonds, bridges = self.compute_consecutive_bonds(sentences, sentence_embs, planes)
        
        exons = [c["text"] for c in codons if c["splicing"] == "EXON"]
        introns = [c["text"] for c in codons if c["splicing"] == "INTRON"]
        total_snaps = sum(1 for b in bonds if b["string_snapped"])
        
        runtime_ms = (time.time() - start_time) * 1000.0
        
        return {
            "agent": "Competitor 2: Equilibrium Arbiter (50M / 50F)",
            "metrics": {
                "total_sentences": len(sentences),
                "retained_exons": len(exons),
                "culled_introns": len(introns),
                "culling_rate_pct": round(100.0 * len(introns) / len(sentences), 2),
                "string_snapping_events": total_snaps,
                "healed_bridging_gluons": len(bridges),
                "hadron_singlet_count": sum(1 for c in codons if c["is_hadron_singlet"]),
                "runtime_ms": round(runtime_ms, 2)
            },
            "codons": codons,
            "gluon_bonds": bonds,
            "synthesized_bridges": bridges,
            "distilled_exon_backbone": exons
        }
