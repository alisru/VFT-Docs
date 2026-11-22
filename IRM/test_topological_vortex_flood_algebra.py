#!/usr/bin/env python3
"""
test_topological_vortex_flood_algebra.py — Standalone 10,400-Trial Adversarial Stress-Test Suite
for Discrete Topological Solitons, Quantized Vortices, and Castlereagh River Bridge Flood Inundation.

Audited Test Suites (10,400 total permutations):
- Suite 1: Discrete Phase Winding Exact Integer Quantization (5,000 trials)
- Suite 2: Topological Soliton Stability under Bounded Perturbations (5,000 trials)
- Suite 3: Castlereagh Stage-Discharge Monotonicity & Rating Continuity (200 trials)
- Suite 4: Causeway Inundation Threshold & Vortex Scour Amplification (200 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-28
"""

import math
from fractions import Fraction
import random
import sys
import os
import importlib.util

_base_dir = os.path.dirname(os.path.abspath(__file__))
_target_path = os.path.join(_base_dir, 'topological_vortex_flood_algebra.py')
spec = importlib.util.spec_from_file_location('topological_vortex_flood_algebra', _target_path)
tvfa = importlib.util.module_from_spec(spec)
sys.modules['topological_vortex_flood_algebra'] = tvfa
spec.loader.exec_module(tvfa)

TopologicalVortexLattice = tvfa.TopologicalVortexLattice
CastlereaghBridgeFloodModel = tvfa.CastlereaghBridgeFloodModel

def run_suite_1():
    """Suite 1: Discrete Phase Winding Exact Integer Quantization (5,000 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(5000):
        # Generate random or structured valuations across the 7-node ring
        mode = trial % 5
        if mode == 0:
            # W = 0 uniform or near-uniform
            base = random.uniform(0.1, 1.8)
            vals = [Fraction(round((base + random.uniform(-0.05, 0.05)) * 1000), 1000) for _ in range(7)]
        elif mode == 1:
            # W = +1 vortex winding
            vals = [Fraction(round((k * 2.0 / 7.0 + random.uniform(-0.02, 0.02)) * 1000), 1000) for k in range(7)]
        elif mode == 2:
            # W = -1 vortex winding
            vals = [Fraction(round(((6 - k) * 2.0 / 7.0 + random.uniform(-0.02, 0.02)) * 1000), 1000) for k in range(7)]
        elif mode == 3:
            # Random valuations across [0, 2]
            vals = [Fraction(random.randint(0, 200), 100) for _ in range(7)]
        else:
            # Edge-case boundary anchors
            anchors = [0, Fraction(1, 3), Fraction(2, 3), 1, Fraction(4, 3), Fraction(5, 3), 2]
            vals = random.sample(anchors, 7)
            
        tvl = TopologicalVortexLattice(vals)
        if tvl.verify_winding_quantization(tolerance=1e-5):
            passes += 1
        else:
            failures += 1
            print(f"Suite 1 Failure at trial {trial}: Winding quantization failed.")
            break
            
    return passes, failures

def run_suite_2():
    """Suite 2: Topological Soliton Stability under Bounded Perturbations (5,000 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(5000):
        # Choose baseline winding configuration
        w_target = (trial % 3) - 1 # -1, 0, or +1
        if w_target == 0:
            base_vals = [Fraction(1, 1) for _ in range(7)]
        elif w_target == 1:
            base_vals = [Fraction(round(k * 2.0 / 7.0 * 1000), 1000) for k in range(7)]
        else:
            base_vals = [Fraction(round((6 - k) * 2.0 / 7.0 * 1000), 1000) for k in range(7)]
            
        tvl_base = TopologicalVortexLattice(base_vals)
        w_base = tvl_base.compute_topological_winding()
        
        # Apply random bounded perturbations |δV| < 1/14
        deltas = [Fraction(random.randint(-50, 50), 1000) for _ in range(7)] # max delta 0.05 < 1/14 ≈ 0.0714
        tvl_perturbed = tvl_base.apply_bounded_perturbation(deltas)
        w_perturbed = tvl_perturbed.compute_topological_winding()
        
        if w_base == w_perturbed:
            passes += 1
        else:
            failures += 1
            print(f"Suite 2 Failure at trial {trial}: Winding number changed from {w_base} to {w_perturbed}")
            break
            
    return passes, failures

def run_suite_3():
    """Suite 3: Castlereagh Stage-Discharge Monotonicity & Rating Continuity (200 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(200):
        inflow_1 = float(trial * 1.5)
        inflow_2 = inflow_1 + random.uniform(0.5, 5.0)
        
        model_1 = CastlereaghBridgeFloodModel(inflow_ml=inflow_1)
        model_2 = CastlereaghBridgeFloodModel(inflow_ml=inflow_2)
        
        stage_1 = model_1.compute_river_stage()
        stage_2 = model_2.compute_river_stage()
        
        v_1 = float(model_1.compute_normalized_stage_valuation())
        v_2 = float(model_2.compute_normalized_stage_valuation())
        
        if stage_1 < stage_2 and v_1 <= v_2 and v_1 >= 0.0:
            passes += 1
        else:
            failures += 1
            print(f"Suite 3 Failure at trial {trial}: Monotonicity violated.")
            break
            
    return passes, failures

def run_suite_4():
    """Suite 4: Causeway Inundation Threshold & Vortex Scour Amplification (200 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(200):
        # Vary inflow from 0 ML to 250 ML
        inflow = float(trial * 1.25)
        flood = CastlereaghBridgeFloodModel(inflow_ml=inflow)
        
        res_0 = flood.evaluate_john_street_causeway(winding_number=0)
        res_1 = flood.evaluate_john_street_causeway(winding_number=1)
        
        # Check inundation threshold consistency
        if res_0["is_inundated"]:
            cond_overflow = res_0["overflow_stress"] > 0.0
            cond_scour_pos = res_0["scour_stress"] > 0.0
            # Vortex shedding |W| = 1 must strictly amplify scour stress
            cond_vortex_amp = res_1["scour_stress"] > res_0["scour_stress"]
            if cond_overflow and cond_scour_pos and cond_vortex_amp:
                passes += 1
            else:
                failures += 1
                print(f"Suite 4 Failure at trial {trial}: Scour conditions failed during inundation.")
                break
        else:
            # Below deck level
            cond_no_overflow = res_0["overflow_stress"] == 0.0
            cond_no_scour = res_0["scour_stress"] == 0.0
            if cond_no_overflow and cond_no_scour:
                passes += 1
            else:
                failures += 1
                print(f"Suite 4 Failure at trial {trial}: Pre-inundation stress non-zero.")
                break
                
    return passes, failures

def main():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: TOPOLOGICAL VORTICES & FLOOD SCOUR (10,400 TRIALS)")
    print("=" * 80)
    
    print("Running Suite 1: Discrete Phase Winding Quantization (5,000 trials)...")
    p1, f1 = run_suite_1()
    print(f"  -> Suite 1 Result: {p1}/{p1+f1} PASS ({f1} failures)")
    
    print("Running Suite 2: Topological Soliton Stability under Perturbations (5,000 trials)...")
    p2, f2 = run_suite_2()
    print(f"  -> Suite 2 Result: {p2}/{p2+f2} PASS ({f2} failures)")
    
    print("Running Suite 3: Castlereagh Stage-Discharge Monotonicity (200 trials)...")
    p3, f3 = run_suite_3()
    print(f"  -> Suite 3 Result: {p3}/{p3+f3} PASS ({f3} failures)")
    
    print("Running Suite 4: Causeway Inundation & Scour Amplification (200 trials)...")
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
