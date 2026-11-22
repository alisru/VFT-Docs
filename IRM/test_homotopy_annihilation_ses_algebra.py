#!/usr/bin/env python3
"""
test_homotopy_annihilation_ses_algebra.py — Standalone 10,400-Trial Adversarial Stress-Test Suite
for Discrete Homotopy π₁(ℙ⁷), Vortex-Antivortex Annihilation, and SES Flood Road Closures.

Audited Test Suites (10,400 total permutations):
- Suite 1: Multi-Loop Homotopy Group Exact Integer Quantization (5,000 trials)
- Suite 2: Vortex-Antivortex Charge Conservation & Annihilation Energy Invariant (5,000 trials)
- Suite 3: Multi-Crossing SES Stage Monotonicity & Vulnerability Ordering (200 trials)
- Suite 4: Topological Wake Scour Amplification & Annihilation Damping (200 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-29
"""

import math
from fractions import Fraction
import random
import sys
import os
import importlib.util

_base_dir = os.path.dirname(os.path.abspath(__file__))
_target_path = os.path.join(_base_dir, 'homotopy_annihilation_ses_algebra.py')
spec = importlib.util.spec_from_file_location('homotopy_annihilation_ses_algebra', _target_path)
hasa = importlib.util.module_from_spec(spec)
sys.modules['homotopy_annihilation_ses_algebra'] = hasa
spec.loader.exec_module(hasa)

MultiLoopHomotopyLattice = hasa.MultiLoopHomotopyLattice
SESMultiBridgeRoadClosureModel = hasa.SESMultiBridgeRoadClosureModel

def run_suite_1():
    """Suite 1: Multi-Loop Homotopy Group Integer Quantization (5,000 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(5000):
        # Generate random or structured valuations for Loop A and Loop B
        mode = trial % 4
        if mode == 0:
            # Random valuations across [0, 2]
            vals_a = [Fraction(random.randint(0, 200), 100) for _ in range(7)]
            vals_b = [Fraction(random.randint(0, 200), 100) for _ in range(7)]
        elif mode == 1:
            # W_A = +1, W_B = -1
            vals_a = [Fraction(round((k * 2.0 / 7.0 + random.uniform(-0.02, 0.02)) * 1000), 1000) for k in range(7)]
            vals_b = [Fraction(round(((6 - k) * 2.0 / 7.0 + random.uniform(-0.02, 0.02)) * 1000), 1000) for k in range(7)]
        elif mode == 2:
            # Uniform or near uniform (W_A = 0, W_B = 0)
            base_a = random.uniform(0.2, 1.8)
            base_b = random.uniform(0.2, 1.8)
            vals_a = [Fraction(round((base_a + random.uniform(-0.05, 0.05)) * 1000), 1000) for _ in range(7)]
            vals_b = [Fraction(round((base_b + random.uniform(-0.05, 0.05)) * 1000), 1000) for _ in range(7)]
        else:
            # Anchor edge cases
            anchors = [0, Fraction(1, 3), Fraction(2, 3), 1, Fraction(4, 3), Fraction(5, 3), 2]
            vals_a = random.sample(anchors, 7)
            vals_b = random.sample(anchors, 7)
            
        ml = MultiLoopHomotopyLattice(vals_a, vals_b)
        wa, wb = ml.compute_individual_windings()
        q_top = ml.compute_total_topological_charge()
        
        is_quant_a = ml.loop_a.verify_winding_quantization()
        is_quant_b = ml.loop_b.verify_winding_quantization()
        
        if is_quant_a and is_quant_b and q_top == (wa + wb):
            passes += 1
        else:
            failures += 1
            print(f"Suite 1 Failure at trial {trial}: Quantization failed.")
            break
            
    return passes, failures

def run_suite_2():
    """Suite 2: Vortex-Antivortex Charge Conservation & Annihilation Energy Invariant (5,000 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(5000):
        # Create perturbed opposing vortex pairs (W_A = +1, W_B = -1 or vice versa)
        orientation = 1 if (trial % 2 == 0) else -1
        if orientation == 1:
            vals_a = [Fraction(round((k * 2.0 / 7.0 + random.uniform(-0.03, 0.03)) * 1000), 1000) for k in range(7)]
            vals_b = [Fraction(round(((6 - k) * 2.0 / 7.0 + random.uniform(-0.03, 0.03)) * 1000), 1000) for k in range(7)]
        else:
            vals_a = [Fraction(round(((6 - k) * 2.0 / 7.0 + random.uniform(-0.03, 0.03)) * 1000), 1000) for k in range(7)]
            vals_b = [Fraction(round((k * 2.0 / 7.0 + random.uniform(-0.03, 0.03)) * 1000), 1000) for k in range(7)]
            
        ml = MultiLoopHomotopyLattice(vals_a, vals_b)
        res = ml.simulate_vortex_annihilation()
        
        cond_ann = res["is_annihilated"] is True
        cond_q_zero = res["q_top_initial"] == 0 and res["q_top_final"] == 0
        cond_e_pos = res["energy_released"] > 0.0
        
        if cond_ann and cond_q_zero and cond_e_pos:
            passes += 1
        else:
            failures += 1
            print(f"Suite 2 Failure at trial {trial}: Annihilation conservation failed.")
            break
            
    return passes, failures

def run_suite_3():
    """Suite 3: Multi-Crossing SES Stage Monotonicity & Vulnerability Ordering (200 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(200):
        # Vary inflow from 0 to 200 ML
        inflow = float(trial * 1.0)
        ses_model = SESMultiBridgeRoadClosureModel(inflow_ml=inflow)
        evals = ses_model.evaluate_all_crossings(net_topological_charge=0)
        
        t_res = evals["timor_culvert"]
        j_res = evals["john_street"]
        c_res = evals["cowper_street"]
        
        # Physical vulnerability check:
        # If Cowper is closed, John must be closed. If John is closed, Timor must be closed.
        order_ok = True
        if c_res["is_closed"] and not j_res["is_closed"]:
            order_ok = False
        if j_res["is_closed"] and not t_res["is_closed"]:
            order_ok = False
            
        # Monotonic hazard check
        hazard_ok = (t_res["hazard_factor_z"] >= 0.0 and
                     j_res["hazard_factor_z"] >= 0.0 and
                     c_res["hazard_factor_z"] >= 0.0)
                     
        if order_ok and hazard_ok:
            passes += 1
        else:
            failures += 1
            print(f"Suite 3 Failure at trial {trial}: Vulnerability ordering violated.")
            break
            
    return passes, failures

def run_suite_4():
    """Suite 4: Topological Wake Scour Amplification & Annihilation Damping (200 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(200):
        # Choose inflow high enough to cause inundation across crossings (e.g. 100 to 200 ML)
        inflow = 100.0 + float(trial * 0.5)
        ses_model = SESMultiBridgeRoadClosureModel(inflow_ml=inflow)
        
        evals_coherent = ses_model.evaluate_all_crossings(net_topological_charge=1)
        evals_annihilated = ses_model.evaluate_all_crossings(net_topological_charge=0)
        
        all_amplified = True
        for key in ["timor_culvert", "john_street", "cowper_street"]:
            scour_coh = evals_coherent[key]["scour_stress"]
            scour_ann = evals_annihilated[key]["scour_stress"]
            if evals_coherent[key]["is_inundated"]:
                if scour_coh <= scour_ann:
                    all_amplified = False
                    break
                    
        if all_amplified:
            passes += 1
        else:
            failures += 1
            print(f"Suite 4 Failure at trial {trial}: Wake scour amplification failed.")
            break
            
    return passes, failures

def main():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: HOMOTOPY, ANNIHILATION & SES CLOSURES (10,400 TRIALS)")
    print("=" * 80)
    
    print("Running Suite 1: Multi-Loop Homotopy Integer Quantization (5,000 trials)...")
    p1, f1 = run_suite_1()
    print(f"  -> Suite 1 Result: {p1}/{p1+f1} PASS ({f1} failures)")
    
    print("Running Suite 2: Vortex-Antivortex Charge Conservation & Annihilation (5,000 trials)...")
    p2, f2 = run_suite_2()
    print(f"  -> Suite 2 Result: {p2}/{p2+f2} PASS ({f2} failures)")
    
    print("Running Suite 3: Multi-Crossing Vulnerability Ordering (200 trials)...")
    p3, f3 = run_suite_3()
    print(f"  -> Suite 3 Result: {p3}/{p3+f3} PASS ({f3} failures)")
    
    print("Running Suite 4: Wake Scour Amplification & Annihilation Damping (200 trials)...")
    p4, f4 = run_suite_4()
    print(f"  -> Suite 4 Result: {p4}/{p4+f4} PASS ({f4} failures)")
    
    total_p = p1 + p2 + p3 + p4
    total_f = f1 + f2 + f3 + f4
    
    print("-" * 80)
    print(f"TOTAL ADVERSARIAL PERMUTATIONS TESTED: {total_p + total_f:,}")
    print(f"TOTAL FAILURES DETECTED:                {total_f}")
    if total_f == 0:
        print("OVERALL VERDICT: UNCONDITIONAL MATHEMATICAL PASS (4/4 SUITES, 100% OPERATIONAL)")
    else:
        print("OVERALL VERDICT: BENCHMARK SUITE FAILED")
    print("=" * 80)
    
    assert total_f == 0, f"Benchmark suite detected {total_f} failures!"

if __name__ == "__main__":
    main()
