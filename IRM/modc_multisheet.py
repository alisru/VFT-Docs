#!/usr/bin/env python3
"""
modc_multisheet.py — Standalone Multi-Sheeted Riemann-Finsler Modulo-c Spacetime Solver (IRM).

Implements:
1. Bijective State Decomposition: v <-> (v_eff, n, is_positive_branch)
   n = floor(v / 2c + 0.5), v_eff = |v - 2cn|, v = 2cn + sign * v_eff
2. Exact bijectivity / reconstruction test across subluminal, horizon, and superluminal velocities.
3. Multi-Sheet Finsler Energy evaluation with horizon-crossing action penalties.
4. Value Physics multi-sheet coercion tracking: distinguishes rest (n=0, v_rel=0) from 2c resonance (n=1, v_rel=2c).

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-02
"""

import math
import numpy as np

C_SPEED_OF_LIGHT = 299792458.0  # m/s
PLANCK_LENGTH = 1.616255e-35    # m
COST_OF_BEING_ALPHA = 1e-15     # Horizon crossing action penalty


class MultiSheetVelocity:
    """
    Implements the Bijective Decomposition of velocity into (v_eff, n, branch).
    """
    def __init__(self, c=C_SPEED_OF_LIGHT):
        self.c = c

    def decompose(self, v):
        """
        Decomposes real velocity v into (v_eff, n, is_positive_branch).
        n: Topological Winding Index (sheet number)
        v_eff: Effective velocity in fundamental Brillouin zone [0, c]
        is_positive_branch: True if v >= 2c*n, False if v < 2c*n
        """
        n = math.floor(v / (2.0 * self.c) + 0.5)
        center = 2.0 * self.c * n
        diff = v - center
        v_eff = abs(diff)
        is_positive_branch = (diff >= 0.0)
        return v_eff, n, is_positive_branch

    def reconstruct(self, v_eff, n, is_positive_branch):
        """
        Exact inverse map: (v_eff, n, branch) -> v.
        """
        center = 2.0 * self.c * n
        if is_positive_branch:
            return center + v_eff
        else:
            return center - v_eff

    def gamma_multisheet(self, v, eps=1e-15):
        """
        Computes the augmented state vector: (gamma_modc, n, v_eff).
        """
        v_eff, n, is_pos = self.decompose(v)
        ratio = min(v_eff / self.c, 1.0 - eps)
        gamma = 1.0 / math.sqrt(1.0 - ratio**2)
        return gamma, n, v_eff

    def finsler_energy(self, mass, v):
        """
        Computes Finsler Lagrangian energy incorporating topological winding penalty.
        E = m c² γ_modc(v) · exp(α |n|)
        """
        gamma, n, _ = self.gamma_multisheet(v)
        penalty = math.exp(COST_OF_BEING_ALPHA * abs(n))
        return mass * (self.c**2) * gamma * penalty


def run_unit_tests():
    print("================================================================================")
    print("MULTI-SHEETED RIEMANN-FINSLER MODULO-C SPACETIME BENCHMARK (IRM)")
    print("================================================================================")

    c = C_SPEED_OF_LIGHT
    msv = MultiSheetVelocity(c)

    # 1. Bijective Reconstruction Test across 1000 velocities in [-10c, 10c]
    test_velocities = np.linspace(-10.0 * c, 10.0 * c, 1000)
    max_error = 0.0

    for v in test_velocities:
        v_eff, n, branch = msv.decompose(v)
        v_rec = msv.reconstruct(v_eff, n, branch)
        err = abs(v - v_rec)
        if err > max_error:
            max_error = err

    print(f"[TEST 1: Bijective Reconstruction Across [-10c, 10c]]")
    print(f"  Maximum Reconstruction Error: {max_error:.6e} m/s")
    assert max_error < 1e-6, "Reconstruction must be exact and bijective"
    print("  --> PASS: 100% Bijective recovery verified across multi-sheet domain.\n")

    # 2. Non-Injectivity Resolution (Finding G-5)
    v_rest = 0.0
    v_2c = 2.0 * c
    v_4c = 4.0 * c

    g_rest, n_rest, _ = msv.gamma_multisheet(v_rest)
    g_2c, n_2c, _ = msv.gamma_multisheet(v_2c)
    g_4c, n_4c, _ = msv.gamma_multisheet(v_4c)

    print(f"[TEST 2: Disambiguation of Folded γ = 1.00 States]")
    print(f"  v = 0.0c: γ = {g_rest:.4f}, Winding Index n = {n_rest} (State: (1.0, 0))")
    print(f"  v = 2.0c: γ = {g_2c:.4f}, Winding Index n = {n_2c} (State: (1.0, 1))")
    print(f"  v = 4.0c: γ = {g_4c:.4f}, Winding Index n = {n_4c} (State: (1.0, 2))")
    assert (g_rest, n_rest) != (g_2c, n_2c), "Augmented state vector must be strictly injective"
    assert (g_2c, n_2c) != (g_4c, n_4c), "Higher sheet states must have unique winding indices"
    print("  --> PASS: Non-injectivity G-5 resolved: augmented states are uniquely distinguished.\n")

    # 3. Finsler Horizon Action Monotonicity
    m = 1.0  # kg
    E_rest = msv.finsler_energy(m, v_rest)
    E_2c = msv.finsler_energy(m, v_2c)
    E_4c = msv.finsler_energy(m, v_4c)

    print(f"[TEST 3: Finsler Energy Monotonicity Across Riemann Sheets]")
    print(f"  E(v = 0c) = {E_rest:.6e} J")
    print(f"  E(v = 2c) = {E_2c:.6e} J (Penalty ΔE = {E_2c - E_rest:.6e} J)")
    print(f"  E(v = 4c) = {E_4c:.6e} J (Penalty ΔE = {E_4c - E_rest:.6e} J)")
    assert E_4c > E_2c > E_rest, "Finsler energy must strictly increase across winding sheets"
    print("  --> PASS: Causal horizon crossings incur irreversible topological action cost.\n")

    # 4. Value Physics Coercion Winding Index (Dimensionless c = 1.0)
    print(f"[TEST 4: Value Physics Multi-Sheet Coercion Disambiguation]")
    msv_econ = MultiSheetVelocity(c=1.0)
    # Zero coercion market
    v_eff_0, n_0, _ = msv_econ.decompose(0.0)
    # Catastrophic multi-fold bankruptcy cycle (v_rel = 2.0)
    v_eff_2, n_2, _ = msv_econ.decompose(2.0)
    print(f"  Zero Coercion (v_rel = 0.0):      Folded v_eff = {v_eff_0:.2f}, Winding n = {n_0}")
    print(f"  Bankruptcy Cycle (v_rel = 2.0c):  Folded v_eff = {v_eff_2:.2f}, Winding n = {n_2}")
    assert n_2 == 1 and n_0 == 0, "Winding index must cleanly tag multi-sheet bankruptcy"
    print("  --> PASS: Value Physics multi-sheet state tracking verified.\n")

    print("================================================================================")
    print("ALL MULTI-SHEETED RIEMANN-FINSLER BENCHMARKS PASSED (4/4)")
    print("================================================================================")


if __name__ == "__main__":
    run_unit_tests()
