#!/usr/bin/env python3
"""
test_renormalization_catchment_algebra.py — 10,400-Trial Adversarial Stress-Test Suite
for Process Renormalization Group (P-RG) Flow, Residue Central Limit Damping,
and Warrumbungle Radar Catchment Inflow Mechanics.

Verifies:
1. P-RG Scale Coarse-Graining Valuation Conservation (5,000 trials)
2. Residue Central Limit Damping & Anchor Pinning (5,000 trials)
3. Multi-Station Radar Pixel Aggregation & Conservation (200 trials)
4. Farm Dam Spillway Saturation & Flood Overflow Containment (200 trials)

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-27
"""

import random
from fractions import Fraction
import importlib.util

# Load renormalization_catchment_algebra dynamically
spec = importlib.util.spec_from_file_location('renormalization_catchment_algebra', '/working_dir/c_0bfea5aee3b42ab1/downloads/renormalization_catchment_algebra.py')
rca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rca)

ProcessRenormalizationGroupEngine = rca.ProcessRenormalizationGroupEngine
WarrumbungleRadarCatchmentModel = rca.WarrumbungleRadarCatchmentModel
ProcessAtom = rca.ProcessAtom


def run_test_suite():
    print("=" * 80)
    print("ADVERSARIAL STRESS-TESTING: P-RG & RADAR CATCHMENT HYDROLOGY (10,400 TRIALS)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # Suite 1: P-RG Scale Coarse-Graining Valuation Conservation (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 1: P-RG Scale Valuation Conservation (5,000 trials)...")
    s1_fails = 0
    rg = ProcessRenormalizationGroupEngine(num_sectors=7, agents_per_sector=7)
    for _ in range(5000):
        micro_vals = [Fraction(random.randint(-10, 30), 10) for _ in range(49)]
        res_c = rg.compute_scaling_conservation(micro_vals)
        if not res_c['is_conserved'] or res_c['total_micro'] != res_c['total_macro']:
            s1_fails += 1

    print(f"  -> Suite 1 Result: {5000 - s1_fails}/5000 PASS ({s1_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 2: Residue Central Limit Damping & Anchor Pinning (5,000 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 2: Residue Central Limit Damping (5,000 trials)...")
    s2_fails = 0
    for _ in range(5000):
        # Micro agents centered around A3=1 with small random residue
        micro_vals = [Fraction(1, 1) + Fraction(random.randint(-15, 15), 100) for _ in range(49)]
        macro_atoms = rg.coarse_grain_state(micro_vals)

        for atom in macro_atoms:
            # Macro residue variance must be damped: |R| <= 1/6
            if abs(atom.R) > Fraction(1, 6) + Fraction(1, 10**9):
                s2_fails += 1
            # Macro anchor must be a valid Evaluator Anchor
            if atom.T not in ProcessAtom.ANCHORS:
                s2_fails += 1

    print(f"  -> Suite 2 Result: {5000 - s2_fails}/5000 PASS ({s2_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 3: Multi-Station Radar Pixel Aggregation & Conservation (200 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 3: Radar Pixel Aggregation Conservation (200 trials)...")
    s3_fails = 0
    for _ in range(200):
        dam_model = WarrumbungleRadarCatchmentModel()
        pixels = [Fraction(random.randint(0, 60), 1) for _ in range(36)]
        res = dam_model.step_storm_event(pixels)

        expected_avg = sum(pixels) / Fraction(36)
        expected_inflow = expected_avg * Fraction(126, 1000)

        if abs(res['avg_rain_mm'] - float(expected_avg)) > 1e-9:
            s3_fails += 1
        if abs(res['inflow_val'] - float(expected_inflow)) > 1e-9:
            s3_fails += 1

    print(f"  -> Suite 3 Result: {200 - s3_fails}/200 PASS ({s3_fails} failures)")

    # -------------------------------------------------------------------------
    # Suite 4: Farm Dam Spillway Saturation & Flood Overflow Containment (200 trials)
    # -------------------------------------------------------------------------
    print("Running Suite 4: Spillway Saturation & Flood Containment (200 trials)...")
    s4_fails = 0
    for _ in range(200):
        dam_flood = WarrumbungleRadarCatchmentModel(dam_init=1)
        # Intense flood rain: 50 to 90 mm across catchment
        storm_rain = [Fraction(random.randint(50, 90), 1) for _ in range(36)]
        res_f = dam_flood.step_storm_event(storm_rain)

        # Dam must saturate at A6=2 limit wall
        if not res_f['dam_full'] or res_f['dam_atom'].T != Fraction(2):
            s4_fails += 1
        # Spillway overflow ML must be strictly positive
        if res_f['spillway_overflow_ml'] <= 0:
            s4_fails += 1
        # Flood stress must be strictly positive
        if res_f['flood_stress'] <= 0:
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
