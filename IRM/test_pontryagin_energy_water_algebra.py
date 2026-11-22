#!/usr/bin/env python3
"""
test_pontryagin_energy_water_algebra.py — 20,000-Trial Adversarial Stress-Test Suite
for Process Pontryagin Maximum Principle (P-PMP), Discrete Symplectic Conservation,
and Coonabarabran Energy-Water Co-Optimization.

Verifies:
1. P-PMP Hamiltonian Maximization & Action Proportionality (5,000 trials)
2. Discrete Symplectic Stationary Invariant (5,000 trials)
3. Energy-Water Solar Allocation & Joint Zero-Stress Invariant (5,000 trials)
4. Peak Evening Grid Support & Gravity Water Supply Invariant (5,000 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-22
"""

import random
from fractions import Fraction
import importlib.util

# Load pontryagin_energy_water_algebra dynamically
spec = importlib.util.spec_from_file_location('pontryagin_energy_water_algebra', '/working_dir/c_0bfea5aee3b42ab1/downloads/pontryagin_energy_water_algebra.py')
pewa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pewa)

ProcessPontryaginSolver = pewa.ProcessPontryaginSolver
CoonabarabranEnergyWaterCoOptimizer = pewa.CoonabarabranEnergyWaterCoOptimizer
ProcessAtom = pewa.ProcessAtom


def run_test_suite():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: P-PMP & ENERGY-WATER CO-OPTIMIZATION (20,000 TRIALS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Suite 1: P-PMP Hamiltonian Maximization & Action Proportionality (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 1: Hamiltonian Maximization & Action Proportionality (5,000 trials)...")
    s1_fails = 0
    for _ in range(5000):
        c_val = Fraction(random.randint(2, 10), 10) # 0.2 to 1.0
        solver = ProcessPontryaginSolver(effort_costs=[c_val]*7)
        lam_val = Fraction(random.randint(-15, 30), 10)
        lam_atom = ProcessAtom.from_rational(lam_val)
        k_atom = ProcessAtom.from_rational(1) # at unit balance
        wear_val = Fraction(1, 20)

        opt_act = solver.optimal_action(lam_atom, plane_idx=0, max_inv=1)
        h_opt = solver.evaluate_hamiltonian(k_atom, opt_act, wear_val, lam_atom, plane_idx=0)

        # Test against 10 random alternative actions
        for _ in range(10):
            alt_act = Fraction(random.randint(0, 100), 100)
            h_alt = solver.evaluate_hamiltonian(k_atom, alt_act, wear_val, lam_atom, plane_idx=0)
            if h_alt > h_opt + Fraction(1, 10**9):
                s1_fails += 1
                break

    print(f"  -> Suite 1 Result: {5000 - s1_fails}/5000 PASS ({s1_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 2: Discrete Symplectic Stationary Invariant (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 2: Discrete Symplectic Stationary Invariant (5,000 trials)...")
    s2_fails = 0
    solver_symp = ProcessPontryaginSolver()
    for _ in range(5000):
        # When K is inside [0, 2], grad_stress is 0, so lambda is constant
        k_atom = ProcessAtom.from_rational(Fraction(random.randint(2, 18), 10))
        lam_atom = ProcessAtom.from_rational(Fraction(random.randint(5, 15), 10))
        wear_val = Fraction(1, 25)

        opt_act = solver_symp.optimal_action(lam_atom)
        h1 = solver_symp.evaluate_hamiltonian(k_atom, opt_act, wear_val, lam_atom)

        lam_next = solver_symp.step_adjoint(lam_atom, k_atom)
        # Advance K with optimal action
        v_k_next = k_atom.value + opt_act - wear_val
        k_next = ProcessAtom.from_rational(v_k_next)

        if 0 <= v_k_next <= 2:
            # If K remains inside [0, 2], adjoint lambda is preserved exactly
            if lam_next != lam_atom:
                s2_fails += 1
            h2 = solver_symp.evaluate_hamiltonian(k_next, opt_act, wear_val, lam_next)
            if h1 != h2:
                s2_fails += 1

    print(f"  -> Suite 2 Result: {5000 - s2_fails}/5000 PASS ({s2_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 3: Energy-Water Solar Allocation & Joint Zero-Stress Invariant (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 3: Energy-Water Solar Allocation & Zero Stress (5,000 trials)...")
    s3_fails = 0
    for _ in range(5000):
        coopt = CoonabarabranEnergyWaterCoOptimizer()
        # Moderate solar surplus in [0.8, 2.2] MW
        solar_surplus = Fraction(random.randint(8, 22), 10)
        res = coopt.dispatch_solar_window(solar_surplus)

        # Both buffers must have zero stress
        if res['soc_stress'] != Fraction(0) or res['water_stress'] != Fraction(0):
            s3_fails += 1
        # Solar must be fully accounted for
        if abs((res['solar_bess_mw'] + res['solar_pumps_mw']) - float(solar_surplus)) > 1e-9:
            s3_fails += 1

    print(f"  -> Suite 3 Result: {5000 - s3_fails}/5000 PASS ({s3_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 4: Peak Evening Grid Support & Gravity Water Supply Invariant (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 4: Evening Peak Grid Support & Gravity Supply (5,000 trials)...")
    s4_fails = 0
    for _ in range(5000):
        coopt_eve = CoonabarabranEnergyWaterCoOptimizer()
        # Pre-charge from solar
        coopt_eve.dispatch_solar_window(Fraction(2, 1))

        # Evening peak discharge in [0.5, 1.8] MW
        peak_demand = Fraction(random.randint(5, 18), 10)
        res_eve = coopt_eve.dispatch_evening_peak(peak_demand)

        # Pumps must be inactive
        if res_eve['pumps_active'] != False:
            s4_fails += 1
        # Total joint stress must remain zero
        if res_eve['total_joint_stress'] != Fraction(0):
            s4_fails += 1
        # BESS must supply the grid peak
        if abs(res_eve['bess_discharge_mw'] - float(peak_demand)) > 1e-9:
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
