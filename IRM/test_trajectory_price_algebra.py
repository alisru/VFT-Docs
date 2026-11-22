#!/usr/bin/env python3
"""
test_trajectory_price_algebra.py — 35,000-Trial Adversarial Stress-Test Suite
for Continuous-to-Discrete Trajectory Discretization & Process Universal Price Equation (P-UPE).

Verifies:
1. Anti-Chattering Theorem & Boundary Noise Absorption (10,000 trials)
2. Trajectory Discretization Valuation Conservation (10,000 trials)
3. P-UPE Balanced Equilibrium Invariants (5,000 trials)
4. Acute Scarcity & Capacity Collapse Bounds (5,000 trials)
5. 7-Plane Strict Monotonicity & Sensitivity (5,000 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-16
"""

import random
from fractions import Fraction
import importlib.util

spec = importlib.util.spec_from_file_location('trajectory_price_algebra', '/working_dir/c_0bfea5aee3b42ab1/trajectory_price_algebra.py')
tpa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tpa)

ContinuousToDiscreteProjector = tpa.ContinuousToDiscreteProjector
ProcessUniversalPriceEquation = tpa.ProcessUniversalPriceEquation
ProcessAtom = tpa.ProcessAtom
ProcessVector7 = tpa.ProcessVector7


def run_test_suite():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: TRAJECTORY DISCRETIZATION & P-UPE (35,000 TRIALS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Suite 1: Anti-Chattering Theorem & Boundary Noise Absorption (10,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 1: Anti-Chattering Invariant (10,000 trials)...")
    s1_fails = 0
    boundaries = [Fraction(2 * k + 1, 6) for k in range(6)]
    eps_hys = Fraction(1, 10**6)

    for _ in range(10000):
        bk = random.choice(boundaries)
        projector = ContinuousToDiscreteProjector(eps_hys=eps_hys)
        # Initialize projector just below boundary
        projector.project_step(bk - 2 * eps_hys)
        initial_transitions = len(projector.transition_history)

        # Oscillate 50 times with sub-threshold noise |delta| < eps_hys
        noise_amp = eps_hys / 4
        for step in range(50):
            noisy_val = bk + (noise_amp if step % 2 == 0 else -noise_amp)
            atom = projector.project_step(noisy_val)

        # There must be ZERO spurious state transitions triggered by sub-threshold noise
        transitions_during_noise = len(projector.transition_history) - initial_transitions
        if transitions_during_noise != 0:
            s1_fails += 1

    print(f"  -> Suite 1 Result: {10000 - s1_fails}/10000 PASS ({s1_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 2: Trajectory Discretization Valuation Conservation (10,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 2: Trajectory Valuation Conservation (10,000 trials)...")
    s2_fails = 0
    for _ in range(10000):
        projector = ContinuousToDiscreteProjector()
        v_prev = Fraction(random.randint(-10, 30), 10)
        atom_prev = projector.project_step(v_prev)

        v_curr = v_prev + Fraction(random.randint(-15, 15), 10)
        atom_curr = projector.project_step(v_curr)

        dT = atom_curr.T - atom_prev.T
        dR = atom_curr.R - atom_prev.R
        dO = atom_curr.O - atom_prev.O
        dV = v_curr - v_prev

        if (dT + dR + dO) != dV:
            s2_fails += 1

    print(f"  -> Suite 2 Result: {10000 - s2_fails}/10000 PASS ({s2_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 3: P-UPE Balanced Equilibrium Invariants (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 3: P-UPE Balanced Equilibrium Invariants (5,000 trials)...")
    s3_fails = 0
    upe = ProcessUniversalPriceEquation()
    C_being = ProcessAtom.from_rational(Fraction(1, 2))
    S_weights = ProcessVector7([Fraction(1, 7)] * 7)

    for _ in range(5000):
        # Generate random balanced supply and demand (D_i == K_i)
        scale = Fraction(random.randint(1, 100), random.randint(1, 10))
        D = ProcessVector7([scale] * 7)
        K = ProcessVector7([scale] * 7)

        res = upe.evaluate_price(C_being, S_weights, D, K)
        # In balanced case: price must be exactly A3=1.000 with 0 stress
        if res['manifest_anchor'] != 'A3' or res['overflow_stress'] != 0 or res['quadratic_penalty'] != 0:
            s3_fails += 1
        if res['price_atom'].value != Fraction(1):
            s3_fails += 1

    print(f"  -> Suite 3 Result: {5000 - s3_fails}/5000 PASS ({s3_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 4: Acute Scarcity & Capacity Collapse Bounds (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 4: Acute Scarcity & Capacity Collapse Bounds (5,000 trials)...")
    s4_fails = 0
    for _ in range(5000):
        D_coords = [Fraction(random.randint(1, 5), 1) for _ in range(7)]
        K_coords = [Fraction(random.randint(1, 5), 1) for _ in range(7)]

        # Zero out 1 to 3 random capacity channels
        zero_channels = random.sample(range(7), k=random.randint(1, 3))
        for ch in zero_channels:
            K_coords[ch] = Fraction(0)

        D = ProcessVector7(D_coords)
        K = ProcessVector7(K_coords)

        res = upe.evaluate_price(C_being, S_weights, D, K)

        # Must saturate at A6=2 limit wall with positive overflow stress
        if res['price_atom'].T != Fraction(2):
            s4_fails += 1
        if res['overflow_stress'] <= 0:
            s4_fails += 1
        if res['quadratic_penalty'] <= 0:
            s4_fails += 1
        if not res['is_saturated']:
            s4_fails += 1

    print(f"  -> Suite 4 Result: {5000 - s4_fails}/5000 PASS ({s4_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 5: 7-Plane Strict Monotonicity & Sensitivity (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 5: 7-Plane Strict Monotonicity (5,000 trials)...")
    s5_fails = 0
    for _ in range(5000):
        target_ch = random.randint(0, 6)
        D_base = [Fraction(random.randint(1, 10), 2) for _ in range(7)]
        K_base = [Fraction(random.randint(1, 10), 2) for _ in range(7)]

        # 1. Test demand monotonicity: D_higher => higher price
        D_higher = list(D_base)
        D_higher[target_ch] += Fraction(1, 2)

        p_base = upe.evaluate_price(C_being, S_weights, ProcessVector7(D_base), ProcessVector7(K_base))
        p_higher_d = upe.evaluate_price(C_being, S_weights, ProcessVector7(D_higher), ProcessVector7(K_base))

        if p_higher_d['v_price'] <= p_base['v_price']:
            s5_fails += 1

        # 2. Test capacity monotonicity: K_higher => lower price
        K_higher = list(K_base)
        K_higher[target_ch] += Fraction(1, 2)

        p_higher_k = upe.evaluate_price(C_being, S_weights, ProcessVector7(D_base), ProcessVector7(K_higher))

        if p_higher_k['v_price'] >= p_base['v_price']:
            s5_fails += 1

    print(f"  -> Suite 5 Result: {5000 - s5_fails}/5000 PASS ({s5_fails} failures)")

    total_failures = s1_fails + s2_fails + s3_fails + s4_fails + s5_fails
    print("-" * 80)
    print(f"TOTAL ADVERSARIAL PERMUTATIONS TESTED: 35,000")
    print(f"TOTAL FAILURES DETECTED:                {total_failures}")
    if total_failures == 0:
        print("OVERALL VERDICT: UNCONDITIONAL MATHEMATICAL PASS (5/5 SUITES, 100% OPERATIONAL)")
    else:
        print("OVERALL VERDICT: FAILURES DETECTED")
    print("=" * 80)


if __name__ == '__main__':
    run_test_suite()
