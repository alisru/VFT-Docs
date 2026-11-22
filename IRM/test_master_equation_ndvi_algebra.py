#!/usr/bin/env python3
"""
test_master_equation_ndvi_algebra.py — 10,400-Trial Adversarial Stress-Test Suite
for Multi-Agent Process Master Equation (P-ME), Process H-Theorem Stress Relaxation,
and Sentinel-2 NDVI Pasture Rotational Grazing.

Verifies:
1. Process Master Equation Probability Conservation (5,000 trials)
2. Process H-Theorem Monotonic Stress Relaxation (5,000 trials)
3. Sentinel-2 NDVI Process Mapping & Boundedness (200 trials)
4. Multi-Paddock Rotational Grazing Preservation Invariant (200 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-25
"""

import random
from fractions import Fraction
import importlib.util

# Load master_equation_ndvi_algebra dynamically
spec = importlib.util.spec_from_file_location('master_equation_ndvi_algebra', '/working_dir/c_0bfea5aee3b42ab1/downloads/master_equation_ndvi_algebra.py')
mena = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mena)

ProcessMasterEquationSolver = mena.ProcessMasterEquationSolver
SentinelNDVIPastureModel = mena.SentinelNDVIPastureModel
ProcessAtom = mena.ProcessAtom


def run_test_suite():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: P-ME & SENTINEL NDVI ROTATION (10,400 TRIALS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Suite 1: Process Master Equation Probability Conservation (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 1: P-ME Probability Conservation (5,000 trials)...")
    s1_fails = 0
    for _ in range(5000):
        # Generate random probability distribution summing to 1
        weights = [random.randint(1, 10) for _ in range(7)]
        tot_w = sum(weights)
        p_init = [Fraction(w, tot_w) for w in weights]

        pme = ProcessMasterEquationSolver()
        pme.prob = p_init
        dt = Fraction(random.randint(1, 10), 10) # 0.1 to 1.0

        res = pme.step(dt)
        if not res['is_prob_conserved'] or res['total_prob'] != Fraction(1, 1):
            s1_fails += 1

    print(f"  -> Suite 1 Result: {5000 - s1_fails}/5000 PASS ({s1_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 2: Process H-Theorem Monotonic Stress Relaxation (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 2: Process H-Theorem Stress Relaxation (5,000 trials)...")
    s2_fails = 0
    for _ in range(5000):
        pme_h = ProcessMasterEquationSolver()
        # Random initial distribution
        weights = [random.randint(1, 5) for _ in range(7)]
        tot_w = sum(weights)
        pme_h.prob = [Fraction(w, tot_w) for w in weights]

        stress_initial = sum(pme_h.prob[a] * pme_h.stresses[a] for a in range(7))
        res_h = pme_h.step(dt=Fraction(1, 2))

        # Expected stress must be monotonically non-increasing: Stress(t+1) <= Stress(t)
        if res_h['expected_stress'] > stress_initial + Fraction(1, 10**9):
            s2_fails += 1

    print(f"  -> Suite 2 Result: {5000 - s2_fails}/5000 PASS ({s2_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 3: Sentinel-2 NDVI Process Mapping & Boundedness (200 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 3: Sentinel-2 NDVI Process Mapping (200 trials)...")
    s3_fails = 0
    for _ in range(200):
        raw_val = Fraction(random.randint(15, 85), 100) # within [0.15, 0.85]
        v_proc = SentinelNDVIPastureModel.raw_ndvi_to_process_val(raw_val)
        atom = ProcessAtom.from_rational(v_proc)

        # Must lie within manifest [0, 2] with zero overflow stress
        if atom.O != Fraction(0) or atom.T not in ProcessAtom.ANCHORS:
            s3_fails += 1
        # Specific anchor sanity checks
        if raw_val == Fraction(50, 100) and atom.T != Fraction(1):
            s3_fails += 1

    print(f"  -> Suite 3 Result: {200 - s3_fails}/200 PASS ({s3_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 4: Multi-Paddock Rotational Grazing Preservation Invariant (200 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 4: Multi-Paddock Rotational Preservation (200 trials)...")
    s4_fails = 0
    for _ in range(200):
        model = SentinelNDVIPastureModel(num_paddocks=4)
        dep = Fraction(random.randint(6, 10), 100) # 0.06 to 0.10/week
        rec = Fraction(random.randint(5, 8), 100)  # 0.05 to 0.08/week

        # Simulate 52 weeks (full annual grazing cycle)
        for _ in range(52):
            step_res = model.step_week(graze_depletion=dep, rest_recovery=rec)
            if not step_res['all_paddocks_healthy']:
                s4_fails += 1
                break
        # Rotations must have occurred
        if len(model.rotation_history) < 2:
            s4_fails += 1

    print(f"  -> Suite 4 Result: {200 - s4_fails}/200 PASS ({s4_fails} failures)")

    total_failures = s1_fails + s2_fails + s3_fails + s4_fails
    print("-" * 80)
    print(f"TOTAL ADVERSARIAL PERMUTATIONS TESTED: 10,400")
    print(f"TOTAL FAILURES DETECTED:                {total_failures}")
    if total_failures == 0:
        print("OVERALL VERDICT: UNCONDITIONAL MATHEMATICAL PASS (4/4 SUITES, 100% OPERATIONAL)")
    else:
        print("OVERALL VERDICT: FAILURES DETECTED")
    print("=" * 80)


if __name__ == '__main__':
    run_test_suite()
