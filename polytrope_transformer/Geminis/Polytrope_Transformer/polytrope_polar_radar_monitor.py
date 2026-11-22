"""
Fractal Polytrope Sovereign LLM: Polar Radar Monitor & Institutional Health Index Engine.
Cycle 21 R&D Milestone. Evaluates real-time 14-Plane Polar Matrix states, computing the
Institutional Health Index (H_inst), plane-by-plane Order-to-Chaos ratios, and training the unified 300-tuple corpus.
"""

import json
import re
import time
import numpy as np

POLAR_14_LABELS = [
    "Q1_ORDER", "Q1_CHAOS",
    "Q2_ORDER", "Q2_CHAOS",
    "Q3_ORDER", "Q3_CHAOS",
    "Q4_ORDER", "Q4_CHAOS",
    "Q5_ORDER", "Q5_CHAOS",
    "Q6_ORDER", "Q6_CHAOS",
    "Q7_ORDER", "Q7_CHAOS"
]

class PolarRadarMonitor:
    """
    Evaluates institutional and discursive health across all 7 Planes:
    H_inst = sum(p_k_order) in [0, 1]
    Plane Ratios: R_k = p_k_order / (p_k_order + p_k_chaos)
    """
    @classmethod
    def evaluate_turn_health(cls, polar_dist_14):
        p = np.array(polar_dist_14, dtype=np.float64) / np.sum(polar_dist_14)
        order_probs = p[0::2]   # Q1_order, Q2_order, ..., Q7_order
        chaos_probs = p[1::2]   # Q1_chaos, Q2_chaos, ..., Q7_chaos
        
        h_inst = float(np.sum(order_probs))
        
        plane_ratios = {}
        plane_names = ["Q1_Identity", "Q2_Possible", "Q3_Physical", "Q4_Lyrical", "Q5_Logical", "Q6_Historical", "Q7_Emotive"]
        for k in range(7):
            total_k = order_probs[k] + chaos_probs[k]
            ratio = float(order_probs[k] / total_k) if total_k > 1e-6 else 0.5
            plane_ratios[plane_names[k]] = {
                "order_prob": round(float(order_probs[k]), 4),
                "chaos_prob": round(float(chaos_probs[k]), 4),
                "health_ratio": round(ratio, 4),
                "status": "HEALTHY (Order Dominant)" if ratio >= 0.55 else "RUPTURED (Chaos Dominant)" if ratio <= 0.45 else "BALANCED"
            }
            
        overall_status = "GENERATIVE_STATECRAFT (Order Coherent)" if h_inst >= 0.65 else \
                         "DEGENERATIVE_POLARIZATION (Chaos Entropic)" if h_inst <= 0.40 else "CONTESTED_EQUILIBRIUM"
                         
        return {
            "institutional_health_index": round(h_inst, 4),
            "entropic_chaos_index": round(1.0 - h_inst, 4),
            "regime_classification": overall_status,
            "plane_by_plane_radar": plane_ratios
        }

if __name__ == "__main__":
    from run_cycle21 import main
    main()
