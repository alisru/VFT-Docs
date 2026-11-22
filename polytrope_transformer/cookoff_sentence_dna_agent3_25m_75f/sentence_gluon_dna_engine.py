"""
Sentence-Level Semantic Gluon DNA Engine - Competitor 3 (Topological Explorer: 25% Male / 75% Female)
====================================================================================================
Focus: State-Space Expansion, Non-Local Multi-Sentence Resonant Entanglement,
       and Unsaid Horizon Projection (Q2 -> Q3).
Evaluates sentences as DNA codons along a 5' -> 3' reading strand.
In addition to adjacent gluon bonds (S_i -> S_{i+1}), Agent 3 computes long-range non-local
gluon entanglement (S_i <-> S_j) across the document and calculates the "Unsaid Horizon" vector:
the foundational concept topologically implied by the document's geometry that was never explicitly stated.
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

ALPHA_S = 0.35
SIGMA = 0.85
M_QUARK = 0.65
R_CRITICAL = (2.0 * M_QUARK + ALPHA_S) / SIGMA  # ~1.529

PLANES = [
    "Q1_Metaphysical",  # Who - Will, Agency, Epistemics
    "Q2_Possible",      # What - Potential, Superposition, Horizon
    "Q3_Physical",      # Where - Matter, Space, Coordinates
    "Q4_Lyrical",       # Why - Meaning, Resonance, Poetics
    "Q5_Logical",       # How - Analytics, Consistency, Equation
    "Q6_Historical",    # Cause - Precedent, Sequence, Lineage
    "Q7_Emotive"        # Effect - Passion, Somatic Strain
]

GAUGE_FRICTION = {
    ("Q3_Physical", "Q5_Logical"): 0.80,
    ("Q5_Logical", "Q4_Lyrical"): 0.85,
    ("Q4_Lyrical", "Q1_Metaphysical"): 0.90,
    ("Q1_Metaphysical", "Q2_Possible"): 0.95,
    ("Q2_Possible", "Q3_Physical"): 1.00,
    ("Q4_Lyrical", "Q3_Physical"): 2.30,
    ("Q7_Emotive", "Q5_Logical"): 2.20,
    ("Q1_Metaphysical", "Q5_Logical"): 1.60,
}

def get_gauge_friction(p1: str, p2: str) -> float:
    if p1 == p2:
        return 0.50
    if (p1, p2) in GAUGE_FRICTION:
        return GAUGE_FRICTION[(p1, p2)]
    idx1, idx2 = int(p1[1]), int(p2[1])
    return 1.0 + abs(idx1 - idx2) * 0.16

class TopologicalExplorerSentenceDNA:
    def __init__(self):
        print("[Agent 3 - Topological Explorer (25M/75F)] Initializing Local Neural Embedder...")
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

    def evaluate_splicing_generative(self, sentence: str, plane: str, confidence: float, is_singlet: bool) -> Tuple[str, str]:
        """
        Agent 3 Generative Splicing Gate:
        Preserves exploratory hypotheses (Q2), metaphorical bridges (Q4), and formal axioms.
        Culls purely boilerplate navigational intros.
        """
        s_low = sentence.lower()
        words = sentence.split()
        
        if len(words) < 5:
            return "INTRON", "Short non-substantive fragment."
        if bool(re.search(r'\b(skip to|click here|table of contents)\b', s_low)):
            return "INTRON", "Navigation boilerplate."
            
        return "EXON", "Active conceptual codon contributing to semantic manifold."

    def compute_consecutive_bonds(self, sentences: List[str], sentence_embs: np.ndarray, planes: List[str]) -> List[Dict[str, Any]]:
        bonds = []
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
            
            bonds.append({
                "from_index": i,
                "to_index": i + 1,
                "p1": p1,
                "p2": p2,
                "euclidean_dist": round(euclid_d, 4),
                "gauge_friction": round(friction, 3),
                "r_effective": round(r_eff, 4),
                "v_cornell": round(v_cornell, 4),
                "string_snapped": is_snapped
            })
        return bonds

    def discover_nonlocal_resonances(self, sentences: List[str], sentence_embs: np.ndarray, planes: List[str], min_separation: int = 5, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Discovers Long-Range Non-Local Gluon Entanglement:
        Pairs of sentences separated by > min_separation that exhibit high cosine similarity
        and cross-plane harmonic resonance (e.g. Q3 Physical grounding echoing Q4 Lyrical purpose).
        """
        n = len(sentences)
        norm_embs = sentence_embs / np.linalg.norm(sentence_embs, axis=1, keepdims=True)
        
        sim_matrix = np.dot(norm_embs, norm_embs.T) # [N, N]
        resonances = []
        
        for i in range(n):
            for j in range(i + min_separation, n):
                sim = float(sim_matrix[i, j])
                p1, p2 = planes[i], planes[j]
                
                # Check for high similarity across distinct planes or distant sections
                if sim > 0.72 and p1 != p2:
                    resonances.append({
                        "sentence_i_index": i,
                        "sentence_j_index": j,
                        "sentence_i_text": sentences[i],
                        "sentence_j_text": sentences[j],
                        "plane_i": p1,
                        "plane_j": p2,
                        "resonance_strength": round(sim, 4),
                        "topological_bridge_type": f"Resonance between {p1} and {p2}"
                    })
                    
        resonances.sort(key=lambda x: x["resonance_strength"], reverse=True)
        return resonances[:top_k]

    def project_unsaid_horizon(self, sentences: List[str], sentence_embs: np.ndarray) -> Dict[str, Any]:
        """
        Mines the "Unsaid Horizon" along the Possibility Spectrum (Q2):
        Calculates the document's global semantic centroid, identifies the plane with highest
        unrealized latent potential, and extracts the primary unstated foundational conclusion.
        """
        norm_embs = sentence_embs / np.linalg.norm(sentence_embs, axis=1, keepdims=True)
        centroid = np.mean(norm_embs, axis=0)
        centroid = centroid / np.linalg.norm(centroid)
        
        # Project centroid onto the 7 planes
        plane_projections = np.dot(self.plane_anchors, centroid) # [7]
        plane_dist = {PLANES[i]: round(float(plane_projections[i]), 4) for i in range(7)}
        
        # Find dominant and latent planes
        dominant_plane = PLANES[int(np.argmax(plane_projections))]
        
        # Latent unsaid plane is the plane with high positive projection but lowest explicit sentence count
        sorted_planes = sorted(plane_dist.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "global_centroid_plane_distribution": plane_dist,
            "dominant_gravitational_anchor": dominant_plane,
            "unsaid_horizon_mining": {
                "highest_latent_potential_plane": sorted_planes[1][0],
                "unsaid_horizon_insight": (
                    f"The document's underlying event physics concentrates most strongly on {dominant_plane}, "
                    f"yet establishes an unsaid bridge directly into {sorted_planes[1][0]}. "
                    f"The implicit topological conclusion is that {dominant_plane.split('_')[1]} operations "
                    f"inevitably constrain the {sorted_planes[1][0].split('_')[1]} state space."
                )
            }
        }

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
            splicing_type, reason = self.evaluate_splicing_generative(s, planes[i], confidences[i], is_singlet)
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
            
        bonds = self.compute_consecutive_bonds(sentences, sentence_embs, planes)
        resonances = self.discover_nonlocal_resonances(sentences, sentence_embs, planes)
        horizon = self.project_unsaid_horizon(sentences, sentence_embs)
        
        exons = [c["text"] for c in codons if c["splicing"] == "EXON"]
        introns = [c["text"] for c in codons if c["splicing"] == "INTRON"]
        total_snaps = sum(1 for b in bonds if b["string_snapped"])
        
        runtime_ms = (time.time() - start_time) * 1000.0
        
        return {
            "agent": "Competitor 3: Topological Explorer (25M / 75F)",
            "metrics": {
                "total_sentences": len(sentences),
                "retained_exons": len(exons),
                "culled_introns": len(introns),
                "culling_rate_pct": round(100.0 * len(introns) / len(sentences), 2),
                "string_snapping_events": total_snaps,
                "nonlocal_resonances_found": len(resonances),
                "hadron_singlet_count": sum(1 for c in codons if c["is_hadron_singlet"]),
                "runtime_ms": round(runtime_ms, 2)
            },
            "codons": codons,
            "gluon_bonds": bonds,
            "nonlocal_resonances": resonances,
            "unsaid_horizon": horizon,
            "distilled_exon_backbone": exons
        }
