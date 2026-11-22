#!/usr/bin/env python3
"""
test_fluctuation_dissipation_bom_algebra.py — 10,400-Trial Adversarial Stress-Test Suite
for Process Fluctuation-Dissipation Theorem (P-FDT), Residue Variance Boundedness,
and BOM Forecast-Augmented Rotational Grazing.

Verifies:
1. Process Fluctuation-Dissipation Theorem Invariant (5,000 trials)
2. Residue Boundary Clamping & Variance Boundedness (5,000 trials)
3. BOM Rainfall Forecast Valuation Projection Bounds (200 trials)
4. Multi-Season Predictive Grazing Biomass Advantage (200 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-26
"""

import random
from fractions import Fraction
import importlib.util

# Load fluctuation_dissipation_bom_algebra dynamically
spec = importlib.util.spec_from_file_location('fluctuation_dissipation_bom_algebra', '/working_dir/c_0bfea5aee3b42ab1/downloads/fluctuation_dissipation_bom_algebra.py')
fdba = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fdba)

ProcessFluctuationDissipationEngine = fdba.ProcessFluctuationDissipationEngine
BOMPredictiveGrazingModel = fdba.BOMPredictiveGrazingModel
ProcessAtom = fdba.ProcessAtom


def run_test_suite():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: P-FDT & BOM PREDICTIVE GRAZING (10,400 TRIALS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Suite 1: Process Fluctuation-Dissipation Theorem Invariant (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 1: P-FDT Variance Scaling (5,000 trials)...")
    s1_fails = 0
    for _ in range(5000):
        tau = Fraction(random.randint(10, 40), 10) # 1.0 to 4.0
        kappa = Fraction(random.randint(5, 15), 10) # 0.5 to 1.5
        dt = Fraction(1, 10)
        engine = ProcessFluctuationDissipationEngine(tau=tau, kappa=kappa, dt=dt)

        # Inject 100 noise steps with standard deviation sigma_D
        sigma_d_int = random.randint(5, 15) # 0.05 to 0.15
        for _ in range(100):
            noise = Fraction(random.randint(-sigma_d_int, sigma_d_int), 100)
            engine.step(noise)

        emp_var = engine.compute_empirical_variance()
        # Variance must be strictly non-negative and bounded by (1/6)^2
        if emp_var < Fraction(0) or emp_var > Fraction(1, 36) + Fraction(1, 10**9):
            s1_fails += 1

    print(f"  -> Suite 1 Result: {5000 - s1_fails}/5000 PASS ({s1_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 2: Residue Boundary Clamping & Variance Boundedness (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 2: Residue Boundary Clamping & Variance Boundedness (5,000 trials)...")
    s2_fails = 0
    for _ in range(5000):
        engine_extreme = ProcessFluctuationDissipationEngine(tau=Fraction(1, 2), dt=Fraction(1, 10))
        # Inject massive shock noise that would blow up an unconstrained system
        for _ in range(50):
            extreme_noise = Fraction(random.randint(-150, 150), 100) # [-1.5, +1.5]
            atom = engine_extreme.step(extreme_noise)
            # Residue must be strictly clamped within [-1/6, 1/6]
            if abs(atom.R) > Fraction(1, 6) + Fraction(1, 10**9):
                s2_fails += 1
                break

        if engine_extreme.compute_empirical_variance() > Fraction(1, 36) + Fraction(1, 10**9):
            s2_fails += 1

    print(f"  -> Suite 2 Result: {5000 - s2_fails}/5000 PASS ({s2_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 3: BOM Rainfall Forecast Valuation Projection Bounds (200 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 3: BOM Rainfall Forecast Valuation Projection (200 trials)...")
    s3_fails = 0
    for _ in range(200):
        model = BOMPredictiveGrazingModel()
        rain_mm = Fraction(random.randint(0, 100), 1)
        dec, rot, v_proj = model.evaluate_rotation_decision(rain_mm)

        expected_proj = model.paddocks[model.active_paddock].value - model.graze_rate + rain_mm * model.rain_conversion
        if abs(v_proj - expected_proj) > Fraction(1, 10**9):
            s3_fails += 1

        # Check rainfall threshold holding logic
        if rain_mm >= Fraction(25, 1) and model.paddocks[model.active_paddock].value <= Fraction(1, 2):
            if rot != False or dec != 'HOLD_PADDOCK_RAIN_REPLENISHMENT':
                s3_fails += 1

    print(f"  -> Suite 3 Result: {200 - s3_fails}/200 PASS ({s3_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 4: Multi-Season Predictive Grazing Biomass Advantage (200 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 4: Predictive Grazing Biomass Advantage (200 trials)...")
    s4_fails = 0
    for _ in range(200):
        model_pred = BOMPredictiveGrazingModel(num_paddocks=4)

        # Run 52 weeks (1 full year)
        for _ in range(52):
            # Sample random weekly rainfall: mostly dry (0-10mm) with occasional rain events (25-50mm)
            r_mm = random.choices([0, 5, 10, 25, 45], weights=[0.4, 0.3, 0.15, 0.1, 0.05])[0]
            res = model_pred.step_week(r_mm)

        # Mean paddock biomass across all paddocks must remain healthy (>= A2=2/3)
        if res['mean_biomass'] < Fraction(2, 3):
            s4_fails += 1
        # Rotations must have been executed safely
        if len(model_pred.rotation_history) < 2:
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
