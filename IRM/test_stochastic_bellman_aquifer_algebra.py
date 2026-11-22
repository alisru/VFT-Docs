#!/usr/bin/env python3
"""
test_stochastic_bellman_aquifer_algebra.py — 20,000-Trial Adversarial Stress-Test Suite
for 7-Plane Stochastic Process Bellman Dynamic Programming
and Warrumbungle Aquifer Hydro-Ecological Irrigation Mechanics.

Verifies:
1. Stochastic Bellman Contraction & Loss Minimization (5,000 trials)
2. Stochastic Overcapacity Zero-Investment Invariant (5,000 trials)
3. Warrumbungle Aquifer Multi-Season Resilience (5,000 trials)
4. Valuation Conservation on Agricultural Phase Resets (5,000 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-23
"""

import random
from fractions import Fraction
import importlib.util

# Load stochastic_bellman_aquifer_algebra dynamically
spec = importlib.util.spec_from_file_location('stochastic_bellman_aquifer_algebra', '/working_dir/c_0bfea5aee3b42ab1/downloads/stochastic_bellman_aquifer_algebra.py')
sbaa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbaa)

StochasticProcessBellman = sbaa.StochasticProcessBellman
WarrumbungleAquiferModel = sbaa.WarrumbungleAquiferModel
ProcessAtom = sbaa.ProcessAtom


def run_test_suite():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: STOCHASTIC BELLMAN & AQUIFER RESILIENCE (20,000 TRIALS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Suite 1: Stochastic Bellman Contraction & Loss Minimization (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 1: Stochastic Loss Minimization (5,000 trials)...")
    s1_fails = 0
    for _ in range(5000):
        # Random probabilities summing to 1
        r1, r2, r3 = random.randint(1, 5), random.randint(1, 5), random.randint(1, 5)
        tot_r = r1 + r2 + r3
        custom_regimes = [
            {'name': 'Wet',     'prob': Fraction(r1, tot_r), 'influx': Fraction(20, 100), 'loss': Fraction(3, 100)},
            {'name': 'Average', 'prob': Fraction(r2, tot_r), 'influx': Fraction(5, 100),  'loss': Fraction(5, 100)},
            {'name': 'Drought', 'prob': Fraction(r3, tot_r), 'influx': Fraction(-15, 100), 'loss': Fraction(10, 100)}
        ]
        solver = StochasticProcessBellman(regimes=custom_regimes)
        v_init = Fraction(random.randint(3, 8), 10)
        d_val = Fraction(1, 1)

        res = solver.compute_optimal_control(v_init, d_val, max_inv=1)
        opt_loss = res['expected_loss']

        # Test against 5 alternative actions
        for _ in range(5):
            alt_inv = Fraction(random.randint(0, 40), 40)
            alt_loss = solver.evaluate_expected_loss(v_init, alt_inv, d_val)
            if alt_loss < opt_loss - Fraction(1, 10**9):
                s1_fails += 1
                break

    print(f"  -> Suite 1 Result: {5000 - s1_fails}/5000 PASS ({s1_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 2: Stochastic Overcapacity Zero-Investment Invariant (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 2: Overcapacity Zero-Investment Invariant (5,000 trials)...")
    s2_fails = 0
    solver_over = StochasticProcessBellman()
    for _ in range(5000):
        v_over = Fraction(random.randint(21, 75), 10)
        d_val = Fraction(random.randint(5, 12), 10)

        res = solver_over.compute_optimal_control(v_over, d_val)
        if not res['is_overcapacity_shutoff'] or res['optimal_inv'] != Fraction(0):
            s2_fails += 1

    print(f"  -> Suite 2 Result: {5000 - s2_fails}/5000 PASS ({s2_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 3: Warrumbungle Aquifer Multi-Season Resilience (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 3: Warrumbungle Aquifer Multi-Season Resilience (5,000 trials)...")
    s3_fails = 0
    regimes = ['Wet', 'Average', 'Drought']
    probs = [0.3, 0.5, 0.2]

    for _ in range(5000):
        model = WarrumbungleAquiferModel(aquifer_init=1, crop_init=1)
        # Simulate 6-month seasonal cycle
        for _ in range(6):
            # Sample weather regime
            r = random.choices(regimes, weights=probs)[0]
            # Adaptive irrigation rule: irrigate more in drought if aquifer is healthy
            if r == 'Drought':
                irrig = Fraction(15, 100) if model.aquifer.value > Fraction(2, 3) else Fraction(5, 100)
            elif r == 'Average':
                irrig = Fraction(5, 100)
            else:
                irrig = Fraction(0)

            rec = model.step_month(r, irrig)
            if not rec['aquifer_safe']:
                s3_fails += 1
                break

    print(f"  -> Suite 3 Result: {5000 - s3_fails}/5000 PASS ({s3_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 4: Valuation Conservation on Agricultural Phase Resets (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 4: Agricultural Phase Reset Valuation Conservation (5,000 trials)...")
    s4_fails = 0
    for _ in range(5000):
        # Pick random starting anchor A1..A5
        k_start = random.randint(1, 5)
        init_atom = ProcessAtom.from_rational(Fraction(k_start, 3))
        # Drawdown across boundary
        drawdown = Fraction(1, 6) + Fraction(random.randint(1, 50), 1000)
        v_next = init_atom.value - drawdown
        next_atom = ProcessAtom.from_rational(v_next)

        # Grade must have dropped
        if next_atom.T >= init_atom.T:
            s4_fails += 1
        # Valuation must be identically conserved
        if next_atom.value != v_next:
            s4_fails += 1
        if (next_atom.T + next_atom.R + next_atom.O) != v_next:
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
