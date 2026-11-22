#!/usr/bin/env python3
"""
test_metabolic_attractor_algebra.py — 35,000-Trial Adversarial Stress-Test Suite
for Multi-Commodity Metabolic Exchange & Bounded Resonance Attractor Dynamics.

Verifies:
1. Multi-Commodity Matrix Divergence Conservation (10,000 trials)
2. Bounded Resonance Attractor Invariant (10,000 trials)
3. Anti-Chattering during Limit-Cycle Oscillations (10,000 trials)
4. Multi-Commodity Input Collapse & Quadratic Stress Bounds (5,000 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-18
"""

import random
import math
from fractions import Fraction
import importlib.util

# Load metabolic_attractor_algebra dynamically
spec = importlib.util.spec_from_file_location('metabolic_attractor_algebra', '/working_dir/c_0bfea5aee3b42ab1/downloads/metabolic_attractor_algebra.py')
maa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(maa)

MultiCommodityExchangeEngine = maa.MultiCommodityExchangeEngine
ResonantAttractorSolver = maa.ResonantAttractorSolver
ProcessAtom = maa.ProcessAtom


def run_test_suite():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: METABOLIC EXCHANGE & RESONANT ATTRACTORS (35,000 TRIALS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Suite 1: Multi-Commodity Matrix Divergence Conservation (10,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 1: Multi-Commodity Divergence Conservation (10,000 trials)...")
    s1_fails = 0
    engine = MultiCommodityExchangeEngine(initial_endowments=[Fraction(500, 1)] * 7)
    initial_wealth = engine.initial_total_wealth

    for _ in range(10000):
        # Generate random 7x7 matrix of process flow atoms
        flow_matrix = [
            [
                ProcessAtom.from_rational(Fraction(random.randint(0, 20), 10))
                if i != j else ProcessAtom.from_rational(0)
                for j in range(7)
            ]
            for i in range(7)
        ]
        res = engine.execute_metabolic_cycle(flow_matrix)
        if not res['is_conserved'] or sum(res['divergences']) != Fraction(0) or engine.total_wealth != initial_wealth:
            s1_fails += 1

    print(f"  -> Suite 1 Result: {10000 - s1_fails}/10000 PASS ({s1_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 2: Bounded Resonance Attractor Invariant (10,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 2: Bounded Resonance Attractor Invariant (10,000 trials)...")
    s2_fails = 0
    for _ in range(10000):
        base_val = Fraction(random.randint(1, 3), 1)
        amp = Fraction(random.randint(1, 20), 2) # amplitude up to 10.0
        freq = Fraction(random.randint(1, 10), 2) # 0.5 to 5.0 Hz
        solver = ResonantAttractorSolver(tau=Fraction(1, 1), dt=Fraction(1, 20))
        res = solver.simulate_periodic_drive(base_val, amp, freq, num_steps=20)
        if not res['is_bounded'] or res['max_v'] > (base_val + amp + Fraction(1, 1)):
            s2_fails += 1

    print(f"  -> Suite 2 Result: {10000 - s2_fails}/10000 PASS ({s2_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 3: Anti-Chattering during Limit-Cycle Oscillations (10,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 3: Anti-Chattering during Limit-Cycle Oscillations (10,000 trials)...")
    s3_fails = 0
    boundaries = [Fraction(2 * k + 1, 6) for k in range(6)]
    eps_hys = Fraction(1, 10**6)

    for _ in range(10000):
        bk = random.choice(boundaries)
        solver = ResonantAttractorSolver(tau=Fraction(1, 1), dt=Fraction(1, 20), eps_hys=eps_hys)
        flow = solver.flow
        flow.v_current = bk
        flow.projector.project_step(bk)
        initial_transitions = len(flow.projector.transition_history)

        # Oscillate near boundary with sub-threshold noise
        for step in range(20):
            noise = (eps_hys / 4) if step % 2 == 0 else (-eps_hys / 4)
            flow.step(bk + noise)

        spurious_transitions = len(flow.projector.transition_history) - initial_transitions
        if spurious_transitions != 0:
            s3_fails += 1

    print(f"  -> Suite 3 Result: {10000 - s3_fails}/10000 PASS ({s3_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 4: Multi-Commodity Input Collapse & Quadratic Stress Bounds (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 4: Input Collapse & Quadratic Stress Bounds (5,000 trials)...")
    s4_fails = 0
    for _ in range(5000):
        # Disrupted flows where 1 to 3 rows are acute shortages (overflow stress atoms)
        disrupted_rows = random.sample(range(7), k=random.randint(1, 3))
        flow_matrix = []
        for i in range(7):
            row = []
            for j in range(7):
                if i in disrupted_rows and i != j:
                    # Acute shortage flow: massive valuation mapped to A6 with positive overflow
                    row.append(ProcessAtom.from_rational(Fraction(random.randint(100, 500), 10)))
                elif i != j:
                    row.append(ProcessAtom.from_rational(Fraction(random.randint(1, 10), 10)))
                else:
                    row.append(ProcessAtom.from_rational(0))
            flow_matrix.append(row)

        engine_disrupted = MultiCommodityExchangeEngine(initial_endowments=[Fraction(10000, 1)] * 7)
        initial_wealth = engine_disrupted.initial_total_wealth
        res = engine_disrupted.execute_metabolic_cycle(flow_matrix)

        if not res['is_conserved'] or engine_disrupted.total_wealth != initial_wealth:
            s4_fails += 1

        # Verify that shortage flows exhibit saturation and positive quadratic stress
        for i in disrupted_rows:
            for j in range(7):
                if i != j:
                    atom = flow_matrix[i][j]
                    if atom.T != Fraction(2) or atom.O <= 0 or atom.quadratic_stress() <= 0:
                        s4_fails += 1

    print(f"  -> Suite 4 Result: {5000 - s4_fails}/5000 PASS ({s4_fails} failures)")

    total_failures = s1_fails + s2_fails + s3_fails + s4_fails
    print("-" * 80)
    print(f"TOTAL ADVERSARIAL PERMUTATIONS TESTED: 35,000")
    print(f"TOTAL FAILURES DETECTED:                {total_failures}")
    if total_failures == 0:
        print("OVERALL VERDICT: UNCONDITIONAL MATHEMATICAL PASS (4/4 SUITES, 100% OPERATIONAL)")
    else:
        print("OVERALL VERDICT: FAILURES DETECTED")
    print("=" * 80)


if __name__ == '__main__':
    run_test_suite()
