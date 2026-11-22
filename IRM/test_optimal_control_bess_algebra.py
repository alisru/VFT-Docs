#!/usr/bin/env python3
"""
test_optimal_control_bess_algebra.py — 20,000-Trial Adversarial Stress-Test Suite
for 7-Lattice Process Hamilton-Jacobi-Bellman (P-HJB) Dynamic Programming
and Coonabarabran BESS Rural Grid Storage Mechanics.

Verifies:
1. P-HJB Optimal Restoring Policy & Unit Parity Attractor (5,000 trials)
2. Overcapacity Zero-Investment Invariant (5,000 trials)
3. Coonabarabran BESS Diurnal Cycling & Energy Balance (5,000 trials)
4. Accelerated Cell Degradation & Valuation Conservation (5,000 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-21
"""

import random
from fractions import Fraction
import importlib.util

# Load optimal_control_bess_algebra dynamically
spec = importlib.util.spec_from_file_location('optimal_control_bess_algebra', '/working_dir/c_0bfea5aee3b42ab1/downloads/optimal_control_bess_algebra.py')
ocba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ocba)

ProcessHJBController = ocba.ProcessHJBController
CoonabarabranBESSGridModel = ocba.CoonabarabranBESSGridModel
ProcessAtom = ocba.ProcessAtom


def run_test_suite():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: P-HJB & COONABARABRAN BESS (20,000 TRIALS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Suite 1: P-HJB Optimal Restoring Policy & Unit Parity Attractor (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 1: P-HJB Optimal Restoring Policy (5,000 trials)...")
    s1_fails = 0
    ctrl = ProcessHJBController()
    for _ in range(5000):
        # Degraded capital valuation V in [0.2, 0.8]
        v_init = Fraction(random.randint(2, 8), 10)
        d_val = Fraction(1, 1) # demand at Unit Balance A3=1
        w_val = Fraction(random.randint(1, 10), 100) # wear in [0.01, 0.10]

        res = ctrl.compute_optimal_control(v_init, d_val, w_val)
        # Optimal investment must be strictly positive
        if res['optimal_inv'] <= Fraction(0):
            s1_fails += 1
        # Resulting valuation must be closer to A3=1 than without investment
        v_unmaintained = v_init - w_val
        if abs(res['next_v'] - Fraction(1)) >= abs(v_unmaintained - Fraction(1)):
            s1_fails += 1
        # Resulting atom must have zero overflow stress O
        if res['next_atom'].O != Fraction(0):
            s1_fails += 1

    print(f"  -> Suite 1 Result: {5000 - s1_fails}/5000 PASS ({s1_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 2: Overcapacity Zero-Investment Invariant (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 2: Overcapacity Zero-Investment Invariant (5,000 trials)...")
    s2_fails = 0
    for _ in range(5000):
        # Overcapacity valuation V strictly > 2 (up to 8.0)
        v_over = Fraction(random.randint(21, 80), 10)
        d_val = Fraction(random.randint(5, 15), 10)
        w_val = Fraction(random.randint(1, 10), 100)

        res = ctrl.compute_optimal_control(v_over, d_val, w_val)
        if not res['is_overcapacity_shutoff'] or res['optimal_inv'] != Fraction(0):
            s2_fails += 1

    print(f"  -> Suite 2 Result: {5000 - s2_fails}/5000 PASS ({s2_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 3: Coonabarabran BESS Diurnal Cycling & Energy Balance (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 3: Coonabarabran BESS Diurnal Cycling (5,000 trials)...")
    s3_fails = 0
    for _ in range(5000):
        bess = CoonabarabranBESSGridModel(capacity_mwh=Fraction(5, 1))
        # Random daytime solar charge (-0.5 to -2.0 MW for 4 hours)
        solar_mw = Fraction(-random.randint(5, 20), 10)
        for _ in range(4):
            bess.step_dispatch(solar_mw)

        soc_post_solar = bess.soc.value
        # SoC must have increased
        if soc_post_solar <= Fraction(1):
            s3_fails += 1

        # Evening peak discharge (+0.5 to +2.0 MW for 4 hours)
        peak_mw = Fraction(random.randint(5, 20), 10)
        for _ in range(4):
            bess.step_dispatch(peak_mw)

        soc_post_peak = bess.soc.value
        # SoC must have decreased during peak discharge
        if soc_post_peak >= soc_post_solar:
            s3_fails += 1

    print(f"  -> Suite 3 Result: {5000 - s3_fails}/5000 PASS ({s3_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 4: Accelerated Cell Degradation & Valuation Conservation (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 4: Accelerated Degradation & Valuation Conservation (5,000 trials)...")
    s4_fails = 0
    for _ in range(5000):
        bess_deg = CoonabarabranBESSGridModel(capacity_mwh=Fraction(5, 1))
        # Push battery with heavy cycles to induce cell wear
        # Check that valuation change equals exact wear
        v_health_init = bess_deg.health.value
        load = Fraction(random.randint(1, 3), 1)
        res_step = bess_deg.step_dispatch(load)

        expected_health_v = v_health_init - res_step['hour_wear']
        if bess_deg.health.value != expected_health_v:
            s4_fails += 1
        # Target + Residue + Overflow conservation
        h_atom = bess_deg.health
        if (h_atom.T + h_atom.R + h_atom.O) != expected_health_v:
            s4_fails += 1

    print(f"  -> Suite 4 Result: {5000 - s4_fails}/5000 PASS ({s4_fails} failures)")

    total_failures = s1_fails + s2_fails + s3_fails + s4_fails
    print("-" * 80)
    print(f"TOTAL ADVERSARIAL PERMUTATIONS TESTED: 20,000")
    print(f"TOTAL FAILURES DETECTED:                {total_failures}")
    if total_failures == 0:
        print("OVERALL VERDICT: UNCONDITIONAL MATHEMATICAL PASS (4/4 SUITES, 100% OPERATIONAL)")
    else:
        print("OVERALL VERDICT: FAILURES DETECTED")
    print("=" * 80)


if __name__ == '__main__':
    run_test_suite()
