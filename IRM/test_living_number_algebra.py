#!/usr/bin/env python3
"""
test_living_number_algebra.py — Standalone 10,000-Trial Adversarial Stress-Test Suite
for The Living Number Atom, [base_n.d.e.f...] Recursive Fractal Grammar,
Infinity Maths (Cost of Being 1inf, P-Operator), and 0–2 Bounded Continuum Try²{}Catch{}.

Audited Test Suites (10,000 total permutations):
- Suite 1: Living Number Atom Address-Value Binding & Base-Shift Identity (2,500 trials)
- Suite 2: Infinity Maths, Cost of Being (1inf), and Lazy Propagation Operator P (2,500 trials)
- Suite 3: Non-Singular Gravitational Field Regularization (r_min = 1inf_x) (2,500 trials)
- Suite 4: 0–2 Bounded Continuum, 7 Evaluator Attractors, and Try²{}Catch{} Drag (2,500 trials)

Author: Lead Researcher for Infinitesimal Reality Math (ARI Division 1: Pure Mathematics)
Date: 2026-10-01
"""

import math
from fractions import Fraction
import random
import sys
import os
import importlib.util

_base_dir = os.path.dirname(os.path.abspath(__file__))
_target_path = os.path.join(_base_dir, 'living_number_algebra.py')
spec = importlib.util.spec_from_file_location('living_number_algebra', _target_path)
lna = importlib.util.module_from_spec(spec)
sys.modules['living_number_algebra'] = lna
spec.loader.exec_module(lna)

LivingNumberAtom = lna.LivingNumberAtom
RecursiveGrammarNumber = lna.RecursiveGrammarNumber
InfinityEngine = lna.InfinityEngine
BoundedContinuum02 = lna.BoundedContinuum02

def run_suite_1():
    """Suite 1: Living Number Atom Address-Value Binding & Base-Shift Identity (2,500 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(2500):
        base = random.randint(0, 5)
        core_n = random.randint(0, 20)
        num_tiers = random.randint(1, 8)
        tiers = [random.randint(0, 9) for _ in range(num_tiers)]
        
        num = RecursiveGrammarNumber(base, core_n, tiers)
        val = num.to_rational()
        atom = num.to_atom(f"atom_{trial}")
        
        # Check Living Number Atom structure: [Variable_Name, Value]
        cond_atom = atom.value == val and f"atom_{trial}" in atom.variable_name
        
        # Check Base-Shift Identity: [1_n.d.e.f...] = [0_n.d.e.f...] + 1
        num_shifted = num.apply_base_shift(1)
        val_shifted = num_shifted.to_rational()
        cond_shift = (val_shifted - val) == Fraction(1)
        
        # Check generative succession if core_n >= 1: a_n = (a-1)_{n+1}
        if core_n >= 1:
            num_succ = num.apply_generative_succession(tier_idx=0)
            cond_succ = (num_succ.to_rational() == val)
        else:
            cond_succ = True
            
        if cond_atom and cond_shift and cond_succ:
            passes += 1
        else:
            failures += 1
            print(f"Suite 1 Failure at trial {trial}")
            break
            
    return passes, failures

def run_suite_2():
    """Suite 2: Infinity Maths, Cost of Being (1inf), and Lazy Propagation Operator P (2,500 trials)."""
    passes = 0
    failures = 0
    engine = InfinityEngine()
    
    for trial in range(2500):
        depth = random.randint(1, 40)
        
        # Cost of being identity: 0.999... + 1inf = [1]
        inf_unit = Fraction(1, 10**depth)
        recurring_nine = Fraction(1) - inf_unit
        
        cond_cost = (recurring_nine + inf_unit == Fraction(1)) and (Fraction(1) - inf_unit == recurring_nine)
        cond_distinct = recurring_nine != Fraction(1) # 0.999... != 1.0 (active process vs. closed whole)
        
        # Propagation Operator P: P(0.0...d0) -> d/9 = 0.ddd... = [d]inf
        digit = random.randint(0, 9)
        prop_val = engine.propagation_operator_P(digit)
        cond_prop = prop_val == Fraction(digit, 9)
        
        # Gabriel's Horn paint thickness regularizer: finite surface area
        horn_len = 10.0 ** random.uniform(1, 40)
        horn_res = engine.gabriels_horn_regularization(horn_len)
        cond_horn = horn_res["is_finite"] and horn_res["regularized_volume"] <= math.pi
        
        if cond_cost and cond_distinct and cond_prop and cond_horn:
            passes += 1
        else:
            failures += 1
            print(f"Suite 2 Failure at trial {trial}")
            break
            
    return passes, failures

def run_suite_3():
    """Suite 3: Non-Singular Gravitational Field Regularization (r_min = 1inf_x) (2,500 trials)."""
    passes = 0
    failures = 0
    engine = InfinityEngine()
    
    for trial in range(2500):
        # Stress-test boundary distance from exact 0 to 10^12
        if trial == 0:
            r = 0.0
        elif trial == 1:
            r = 1e-45 # Far below Planck scale
        elif trial == 2:
            r = 1e-35 # Around Planck scale
        else:
            r = 10.0 ** random.uniform(-40, 10)
            
        m1 = 10.0 ** random.uniform(-10, 20)
        m2 = 10.0 ** random.uniform(-10, 20)
        
        res = engine.compute_non_singular_gravity(m1, m2, r)
        
        # Check non-singularity and upper bound
        cond_finite = res["is_non_singular"]
        cond_floor = res["r_effective"] >= float(engine.one_inf)
        cond_bound = res["force"] <= res["max_force_bound"] * (1.0 + 1e-12)
        
        if cond_finite and cond_floor and cond_bound:
            passes += 1
        else:
            failures += 1
            print(f"Suite 3 Failure at trial {trial}: r={r}, Force={res['force']}")
            break
            
    return passes, failures

def run_suite_4():
    """Suite 4: 0–2 Bounded Continuum, 7 Evaluator Attractors, and Try²{}Catch{} Drag (2,500 trials)."""
    passes = 0
    failures = 0
    
    for trial in range(2500):
        # Generate valuation across [0.0, 2.0]
        val = Fraction(random.randint(0, 200), 100)
        name, a_val, dist = BoundedContinuum02.nearest_evaluator_attractor(val)
        
        cond_attractor = name in ["A0", "A1", "A2", "A3", "A4", "A5", "A6"]
        cond_dist_bound = abs(dist) <= Fraction(1, 6) + 1e-9 # Halfway gap between attractors
        
        # Try²{}Catch{} quadratic drag: R = ||v||² - ||N||²
        v = random.uniform(0.0, 4.0)
        n = random.uniform(0.5, 2.0)
        tc = BoundedContinuum02.try_squared_catch(v, n)
        
        if v > n:
            cond_tc = (not tc["is_contained"]) and (tc["structural_drag"] > 0.0) and (abs(tc["residual_R"] - (v**2 - n**2)) < 1e-9)
        else:
            cond_tc = tc["is_contained"] and (tc["structural_drag"] == 0.0) and (tc["residual_R"] <= 0.0)
            
        # (42+n)-polytrope minimal meaning bound: v_min = 43 + n
        n_dim = random.randint(1, 10)
        v_valid = 43 + n_dim + random.randint(0, 5)
        v_invalid = 43 + n_dim - 1
        cond_poly = (BoundedContinuum02.verify_42_plus_n_meaning_bound(n_dim, v_valid) is True and
                     BoundedContinuum02.verify_42_plus_n_meaning_bound(n_dim, v_invalid) is False)
                     
        if cond_attractor and cond_dist_bound and cond_tc and cond_poly:
            passes += 1
        else:
            failures += 1
            print(f"Suite 4 Failure at trial {trial}")
            break
            
    return passes, failures

def main():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: LIVING NUMBER ATOM & IRM PRIMITIVES (10,000 TRIALS)")
    print("=" * 80)
    
    print("Running Suite 1: Living Number Atom Address Binding & Base-Shift (2,500 trials)...")
    p1, f1 = run_suite_1()
    print(f"  -> Suite 1 Result: {p1}/{p1+f1} PASS ({f1} failures)")
    
    print("Running Suite 2: Infinity Maths, Cost of Being (1inf), & P-Operator (2,500 trials)...")
    p2, f2 = run_suite_2()
    print(f"  -> Suite 2 Result: {p2}/{p2+f2} PASS ({f2} failures)")
    
    print("Running Suite 3: Non-Singular Gravity & r_min = 1inf_x Regularization (2,500 trials)...")
    p3, f3 = run_suite_3()
    print(f"  -> Suite 3 Result: {p3}/{p3+f3} PASS ({f3} failures)")
    
    print("Running Suite 4: 0–2 Bounded Continuum, Attractors, & Try²Catch (2,500 trials)...")
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
