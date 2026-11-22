"""
Fractal Polytrope Sovereign LLM: Coalition Sensitivity & Perturbation Analyzer.
Cycle 12 R&D Milestone. Self-contained module with zero external dependencies.
Simulates exogenous shocks (mandate erosion, economic stagflation, infrastructure crisis)
to discover the critical tipping point delta_c where parliamentary accords bifurcate into deadlock.
"""

import json
import os
import re
import time
import numpy as np
import pathlib

# ============================================================================
# 1. POLYTROPE COMPLEX DEFINITION
# ============================================================================

class ComplexState:
    def __init__(self, name, centroid, cov, q_planes):
        self.name = name
        self.centroid = np.array(centroid, dtype=np.float64) # (upsilon, psi, z)
        self.cov = np.array(cov, dtype=np.float64)
        self.q_planes = np.array(q_planes, dtype=np.float64) / np.sum(q_planes)

    def copy(self):
        return ComplexState(self.name, self.centroid.copy(), self.cov.copy(), self.q_planes.copy())

# ============================================================================
# 2. THREE-BODY SOLVER FOR SENSITIVITY SWEEPS
# ============================================================================

def solve_tripartite_fast(c_gov, c_opp, c_cross, steps=80, lr=0.05, damping=0.85):
    s = (c_gov.centroid + c_opp.centroid + c_cross.centroid) / 3.0
    v = np.zeros(3, dtype=np.float64)
    inv_g = np.linalg.inv(c_gov.cov)
    inv_o = np.linalg.inv(c_opp.cov)
    inv_c = np.linalg.inv(c_cross.cov)
    
    for _ in range(steps):
        f_net = inv_g @ (c_gov.centroid - s) + inv_o @ (c_opp.centroid - s) + inv_c @ (c_cross.centroid - s)
        v = damping * v + lr * f_net
        s = np.clip(s + v, -2.0, 2.0)
        
    u_star, p_star, z_star = s
    if u_star >= 0 and p_star >= 0:
        modal = "PRODUCTIVE ACCORD [can be]"
    elif u_star < 0 and p_star >= 0:
        modal = "REDUCTIVE COMPROMISE [is not]"
    elif u_star < 0 and p_star < 0:
        modal = "REGRESSIVE DEADLOCK [was like]"
    else:
        modal = "CONSTRUCTIVE TREATY [is like]"
        
    return s, modal, float(np.linalg.norm(f_net))

# ============================================================================
# 3. COALITION SENSITIVITY ANALYZER
# ============================================================================

class CoalitionSensitivityAnalyzer:
    @staticmethod
    def run_shock_sweep(c_gov_base, c_opp_base, c_cross_base, shock_type="economic_stagflation", delta_range=np.linspace(0.0, 1.2, 13)):
        sweep_records = []
        bifurcation_point = None
        previous_modal = None
        
        for delta in delta_range:
            g = c_gov_base.copy()
            o = c_opp_base.copy()
            c = c_cross_base.copy()
            
            # Apply shock perturbations
            if shock_type == "mandate_integrity_erosion":
                # Executive mandate shrinks in boundary (-u) and kinetic will (-p)
                g.centroid[0] -= 1.0 * delta
                g.centroid[1] -= 0.8 * delta
                o.centroid[1] += 0.5 * delta # opposition attack increases
            elif shock_type == "economic_stagflation":
                # Government causal yield (+z) collapses into deficit (-z), boundary tightens
                g.centroid[0] -= 0.8 * delta
                g.centroid[2] -= 1.2 * delta
                o.centroid[0] -= 0.5 * delta
            elif shock_type == "infrastructure_disaster":
                # Crossbench demands mass transport repair (Q3), pulling kinetic drive into drag (-p)
                c.centroid[1] -= 1.0 * delta
                c.centroid[0] += 0.5 * delta
                g.centroid[2] -= 0.6 * delta
                
            s_star, modal, res_force = solve_tripartite_fast(g, o, c)
            
            is_phase_shift = (previous_modal is not None and modal != previous_modal)
            if is_phase_shift and bifurcation_point is None:
                bifurcation_point = round(float(delta), 3)
                
            sweep_records.append({
                "perturbation_magnitude_delta": round(float(delta), 3),
                "s_star": [round(float(x), 4) for x in s_star],
                "modal_state": modal,
                "residual_force": round(res_force, 6),
                "phase_transition": is_phase_shift
            })
            previous_modal = modal
            
        return {
            "shock_type": shock_type,
            "bifurcation_threshold_delta_c": bifurcation_point,
            "sweep_trajectory": sweep_records
        }

# ============================================================================
# 4. EXECUTION OF EXPERIMENT
# ============================================================================

def run_sensitivity_experiment():
    print("=" * 70)
    print("HOURLY R&D EXECUTION: CYCLE 12 (COALITION SENSITIVITY & PHASE TRANSITIONS)")
    print("=" * 70)
    
    # Base Tripartite Complexes from Cycle 11
    c_gov = ComplexState("Government Executive", [1.10, 0.80, 0.55], np.diag([0.30, 0.25, 0.35]), [0.4, 0.1, 0.15, 0.05, 0.25, 0.02, 0.03])
    c_opp = ComplexState("Opposition Scrutiny", [-1.15, 0.45, -0.40], np.diag([0.25, 0.20, 0.30]), [0.45, 0.05, 0.1, 0.05, 0.15, 0.05, 0.15])
    c_cross = ComplexState("Regional Crossbench", [0.45, -0.15, 0.10], np.diag([0.20, 0.20, 0.20]), [0.15, 0.1, 0.35, 0.25, 0.1, 0.02, 0.03])
    
    shocks = ["economic_stagflation", "mandate_integrity_erosion", "infrastructure_disaster"]
    all_sweeps = {}
    
    for shock in shocks:
        print(f"\nSimulating Exogenous Shock: {shock.upper()}")
        print("-" * 70)
        res = CoalitionSensitivityAnalyzer.run_shock_sweep(c_gov, c_opp, c_cross, shock_type=shock)
        all_sweeps[shock] = res
        print(f"Critical Bifurcation Threshold (δ_c): {res['bifurcation_threshold_delta_c']}")
        
        # Display key step transitions
        for step in res["sweep_trajectory"][::3]:
            trans = " [PHASE SHIFT!]" if step["phase_transition"] else ""
            print(f"  δ = {step['perturbation_magnitude_delta']:4.2f} -> s* = {step['s_star']} | State: {step['modal_state']}{trans}")
            
    out_file = "/working_dir/c_424c86baff31945d/artifacts/file_generation/ttl=63d/output/coalition_sensitivity_results.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({
            "cycle": 12,
            "experiment": "Coalition Sensitivity Perturbation Analysis & Phase Transitions",
            "shocks_evaluated": all_sweeps
        }, f, indent=2)
    print(f"\nSaved Cycle 12 sensitivity metrics to: {out_file}")

if __name__ == "__main__":
    run_sensitivity_experiment()
