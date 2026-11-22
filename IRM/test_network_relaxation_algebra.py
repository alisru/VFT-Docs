#!/usr/bin/env python3
"""
test_network_relaxation_algebra.py — 35,000-Trial Adversarial Stress-Test Suite
for Inertial Price Flow & Closed Circular Network Value Conservation.

Verifies:
1. Inertial Price Relaxation Damping & Bounded Derivatives (10,000 trials)
2. Anti-Chattering during Trajectory Relaxation (10,000 trials)
3. Closed-Network Value Conservation Theorem (10,000 transaction rounds)
4. Acute Capacity Collapse & Overflow Stress Containment (5,000 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-17
"""

import random
from fractions import Fraction
import importlib.util

# Load network_relaxation_algebra dynamically
spec = importlib.util.spec_from_file_location('network_relaxation_algebra', '/working_dir/c_0bfea5aee3b42ab1/downloads/network_relaxation_algebra.py')
nra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nra)

InertialPriceFlow = nra.InertialPriceFlow
CircularProcessNetwork = nra.CircularProcessNetwork
ProcessAtom = nra.ProcessAtom


def run_test_suite():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: NETWORK RELAXATION & VALUE CONSERVATION (35,000 TRIALS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Suite 1: Inertial Price Relaxation Damping & Bounded Derivatives (10,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 1: Inertial Damping & Derivative Bounds (10,000 trials)...")
    s1_fails = 0
    for _ in range(10000):
        tau = Fraction(random.randint(5, 50), 10) # 0.5 to 5.0 s
        dt = Fraction(random.randint(1, 10), 100) # 0.01 to 0.1 s
        flow = InertialPriceFlow(tau=tau, dt=dt)
        flow.v_current = Fraction(random.randint(0, 20), 10)

        # Apply sudden target shock
        v_target = flow.v_current + Fraction(random.randint(-30, 30), 10)
        res = flow.step(v_target)

        # Theoretical bound: |velocity| <= |v_target - v_initial| / tau
        # In discrete Euler: velocity = (factor * (v_target - v_init)) / dt = (v_target - v_init) / (tau + dt)
        expected_vel = (v_target - (flow.v_current - res['velocity'] * dt)) / (tau + dt)
        if abs(res['velocity'] - expected_vel) > Fraction(1, 10**9):
            s1_fails += 1
        # Check strict boundedness: |velocity| <= |v_target - v_init| / tau
        shock_mag = abs(v_target - (flow.v_current - res['velocity'] * dt))
        if abs(res['velocity']) > (shock_mag / tau) + Fraction(1, 10**9):
            s1_fails += 1

    print(f"  -> Suite 1 Result: {10000 - s1_fails}/10000 PASS ({s1_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 2: Anti-Chattering during Trajectory Relaxation (10,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 2: Anti-Chattering during Trajectory Relaxation (10,000 trials)...")
    s2_fails = 0
    boundaries = [Fraction(2 * k + 1, 6) for k in range(6)]
    eps_hys = Fraction(1, 10**6)

    for _ in range(10000):
        bk = random.choice(boundaries)
        flow = InertialPriceFlow(tau=Fraction(1, 1), dt=Fraction(1, 20), eps_hys=eps_hys)
        flow.v_current = bk

        # First establish state right at boundary
        flow.projector.project_step(bk)
        initial_transitions = len(flow.projector.transition_history)

        # Add 20 steps of sub-threshold relaxation noise around bk
        for step in range(20):
            noise = (eps_hys / 3) if step % 2 == 0 else (-eps_hys / 3)
            # target hovers near bk with sub-threshold amplitude
            res = flow.step(bk + noise)

        # Must have zero spurious transitions from sub-threshold perturbation
        spurious_transitions = len(flow.projector.transition_history) - initial_transitions
        if spurious_transitions != 0:
            s2_fails += 1

    print(f"  -> Suite 2 Result: {10000 - s2_fails}/10000 PASS ({s2_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 3: Closed-Network Value Conservation Theorem (10,000 transaction rounds)
    # -------------------------------------------------------------------------
    print("Running Suite 3: Closed-Network Value Conservation (10,000 rounds)...")
    s3_fails = 0
    net = CircularProcessNetwork(initial_endowment_per_node=Fraction(100, 1))
    initial_total = net.total_endowment

    for round_idx in range(10000):
        buyer = random.randint(0, 6)
        seller = random.randint(0, 6)
        while seller == buyer:
            seller = random.randint(0, 6)

        # Vary demand and capacity dynamically
        net.nodes[buyer].demand = Fraction(random.randint(5, 25), 10)
        net.nodes[seller].capacity = Fraction(random.randint(5, 25), 10)

        res = net.execute_transaction(buyer, seller)
        if not res['is_conserved'] or net.total_endowment != initial_total:
            s3_fails += 1

    print(f"  -> Suite 3 Result: {10000 - s3_fails}/10000 PASS ({s3_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 4: Acute Capacity Collapse & Overflow Stress Containment (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 4: Acute Capacity Shock & Overflow Containment (5,000 trials)...")
    s4_fails = 0
    net_shock = CircularProcessNetwork(initial_endowment_per_node=Fraction(200, 1))
    initial_shock_total = net_shock.total_endowment

    for _ in range(5000):
        buyer = random.randint(0, 6)
        shocked_seller = random.randint(0, 6)
        while shocked_seller == buyer:
            shocked_seller = random.randint(0, 6)

        # Collapse seller capacity to exact zero
        net_shock.nodes[shocked_seller].capacity = Fraction(0)
        net_shock.nodes[buyer].demand = Fraction(random.randint(1, 5), 1)

        # Execute multiple steps to let price relax towards acute shortage
        for _ in range(5):
            res = net_shock.execute_transaction(buyer, shocked_seller)

        # In acute shortage: price atom must saturate at A6=2, with positive overflow & quadratic stress
        if res['price_atom'].T != Fraction(2):
            s4_fails += 1
        if res['overflow_stress'] <= 0:
            s4_fails += 1
        if res['quadratic_penalty'] <= 0:
            s4_fails += 1
        # Conservation must still hold unconditionally!
        if net_shock.total_endowment != initial_shock_total:
            s4_fails += 1

        # Restore capacity
        net_shock.nodes[shocked_seller].capacity = Fraction(1, 1)

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
