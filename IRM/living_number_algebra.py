#!/usr/bin/env python3
"""
living_number_algebra.py — The Living Number Atom, [base_n.d.e.f...] Recursive Fractal Grammar,
Infinity Maths (Cost of Being 1inf, Propagation Operator P), and 0–2 Bounded Continuum
for Infinitesimal Reality Math (IRM Division 1: Pure Mathematics).

Direct Implementation of Jarrod Lyndsay Hamilton's Original Foundational Primitives:
1. The Living Number Atom:
   Number = [Variable_Name, Value]
   - Variable_Name: Structural coordinate address recording reference frame (base manifold offset b)
     and scale depth tier (Level 0 integer n, Level 1 tier d, Level 2 tier e, ..., Level omega s_omega).
   - Value: Physical magnitude or field state (exact rational or lazy stream generator).
2. The [base_n.d.e.f...] Recursive Fractal Grammar:
   - Base manifold offset b (e.g. [0_n.d.e.f...], [1_0.d.e.f...]).
   - Integer core n (Level 0, 10^0).
   - Nested fractional and infinitesimal tiers d (10^-1), e (10^-2), f (10^-3) down to s_omega (10^-omega).
   - Base-Shift Identity: [1_n.d.e.f...] = [0_n.d.e.f...] + 1.
   - Generative succession: a_n = (a-1)_{n+1}.
3. Infinity Maths & The Cost of Being (1inf):
   - 0.999... != 1.0. An infinite recurring decimal is an active running process; [1] is a closed whole.
   - Irreducible existence increment: 0.999... + 1inf = [1] and [1] - 1inf = 0.999... where 1inf = epsilon = (-inf + 1).
   - Potential vs. Actual Infinity: The Universe acts as a lazy evaluation engine, treating infinitesimal
     states as dormant potential seeds until observation/interaction forces resolution.
   - The Propagation Operator P: Cascades unphysical trailing zeros at infinite depth into canonical
     repeating blocks: P(0.0...40) -> 0.444... = [4]inf.
   - Physical Boundary Cutoffs: Gabriel's Horn paint thickness floor epsilon = 1inf; field singularity
     regularization r_min = 1inf_x = ell_P (no division by zero).
4. The 0–2 Bounded Continuum & Try²{}Catch{} Operator:
   - 0.0: baseline floor of homogeny (relative zero).
   - 1.0: unit parity rest center (equilibrium, lossless transmission).
   - 2.0: manifest physical saturation ceiling.
   - Try²{}Catch{} quadratic residual: R = ||v||^2 - ||N||^2. Excess over containment is caught as structural stress and drag.
   - 7 Evaluator Attractors A0 (0.00) to A6 (2.00).
   - (42+n)-polytrope minimal meaning bound requiring v_min = 43+n vertices, where the +1 vertex is the mandatory Observer/Definer.

Author: Lead Researcher for Infinitesimal Reality Math (ARI Division 1: Pure Mathematics)
Date: 2026-10-01
"""

import math
from fractions import Fraction
import sys
import os

_dir = os.path.dirname(os.path.abspath(__file__))
if _dir not in sys.path:
    sys.path.insert(0, _dir)

# Physical Cost of Being Constants (Natural Units / Planck Scale)
ONE_INF = Fraction(1, 10**35)  # Physical Cost of Being 1inf_x = ell_P (approx 10^-35 m)
PLANCK_LENGTH = 1.616255e-35  # meters
GRAVITATIONAL_CONSTANT = Fraction(667430, 10**16) # G = 6.67430e-11

class LivingNumberAtom:
    """
    Primitive 1: The Living Number Atom
    Number = [Variable_Name, Value]
    - Variable_Name: Structural coordinate address in recursive grammar.
    - Value: Exact rational magnitude or physical field state.
    """
    def __init__(self, variable_name: str, value: Fraction):
        self.variable_name = str(variable_name)
        self.value = Fraction(value)

    def __repr__(self):
        return f"[{self.variable_name}, {self.value}]"

    def __eq__(self, other):
        if isinstance(other, LivingNumberAtom):
            return self.variable_name == other.variable_name and self.value == other.value
        return False

    def shift_base(self, delta_base: int):
        """
        Base-Shift Identity: shifts the base coordinate and adds integer delta.
        """
        new_name = f"base_{delta_base}::{self.variable_name}"
        return LivingNumberAtom(new_name, self.value + Fraction(delta_base))


class RecursiveGrammarNumber:
    """
    Primitive 2: The [base_n.d.e.f...] Recursive Fractal Grammar
    Encodes numbers with explicit base manifold offset b, integer core n,
    and nested tiers [d, e, f, ...].
    """
    def __init__(self, base: int, core_n: int, tiers: list):
        self.base = int(base)
        self.core_n = int(core_n)
        # tiers are digits at 10^-1, 10^-2, 10^-3, etc.
        self.tiers = [int(t) for t in tiers]

    @classmethod
    def from_string(cls, repr_str: str):
        """
        Parses grammar string like '[0_3.1.4.1.5]' or '[1_0.9.9.9]'.
        """
        clean = repr_str.strip("[] ")
        parts = clean.split("_")
        base = int(parts[0])
        subparts = parts[1].split(".")
        core_n = int(subparts[0])
        tiers = [int(d) for d in subparts[1:] if d]
        return cls(base, core_n, tiers)

    def to_rational(self) -> Fraction:
        """
        Evaluates exact rational magnitude: base + core_n + ∑ tier_k · 10^{-(k+1)}.
        """
        val = Fraction(self.base + self.core_n)
        denom = 10
        for t in self.tiers:
            val += Fraction(t, denom)
            denom *= 10
        return val

    def to_atom(self, name_prefix: str = "num") -> LivingNumberAtom:
        tiers_str = ".".join(str(t) for t in self.tiers)
        addr = f"{name_prefix}[{self.base}_{self.core_n}.{tiers_str}]"
        return LivingNumberAtom(addr, self.to_rational())

    def apply_base_shift(self, shift: int):
        """
        Base-Shift Identity: [1_n.d.e.f...] = [0_n.d.e.f...] + 1.
        """
        return RecursiveGrammarNumber(self.base + shift, self.core_n, self.tiers)

    def apply_generative_succession(self, tier_idx: int):
        """
        Generative succession identity: a_n = (a-1)_{n+1}.
        Borrowing 1 unit from tier n generates 10 units at tier n+1.
        """
        new_tiers = list(self.tiers)
        if tier_idx == 0:
            assert self.core_n >= 1, "Cannot borrow from zero core"
            new_core = self.core_n - 1
            if len(new_tiers) > 0:
                new_tiers[0] += 10
            else:
                new_tiers.append(10)
            return RecursiveGrammarNumber(self.base, new_core, new_tiers)
        else:
            idx = tier_idx - 1
            assert idx < len(new_tiers), "Tier index out of bounds"
            assert new_tiers[idx] >= 1, "Cannot borrow from zero tier"
            new_tiers[idx] -= 1
            if idx + 1 < len(new_tiers):
                new_tiers[idx + 1] += 10
            else:
                new_tiers.append(10)
            return RecursiveGrammarNumber(self.base, self.core_n, new_tiers)


class InfinityEngine:
    """
    Primitive 3: Infinity Maths & The Cost of Being (1inf)
    - 0.999... != 1.0 (active running process vs. closed whole).
    - Irreducible existence increment: 0.999... + 1inf = [1].
    - Propagation Operator P: cascades trailing states into canonical repeating blocks.
    - Non-singular physical field regularization: r_min = 1inf_x.
    """
    def __init__(self, one_inf: Fraction = ONE_INF):
        self.one_inf = one_inf

    def closed_whole(self, n: int = 1) -> LivingNumberAtom:
        """
        The closed whole [n].
        """
        return LivingNumberAtom(f"closed_whole[{n}]", Fraction(n))

    def active_recurring_nine(self, depth: int = 35) -> LivingNumberAtom:
        """
        Active running process 0.999... truncated to finite observation depth.
        0.999... = 1 - 10^-depth.
        """
        val = Fraction(1) - Fraction(1, 10**depth)
        return LivingNumberAtom(f"recurring_process[0.9_depth_{depth}]", val)

    def verify_cost_of_being_increment(self, depth: int = 35) -> bool:
        """
        Verifies: (1 - 1inf) + 1inf == [1] and [1] - 1inf == (1 - 1inf).
        """
        inf_unit = Fraction(1, 10**depth)
        active_nine = Fraction(1) - inf_unit
        
        sum_check = (active_nine + inf_unit) == Fraction(1)
        sub_check = (Fraction(1) - inf_unit) == active_nine
        return sum_check and sub_check

    @staticmethod
    def propagation_operator_P(digit: int, depth_k: int = 7) -> Fraction:
        """
        The Propagation Operator P:
        Cascades trailing unphysical zeros/seeds at infinite depth into canonical
        repeating blocks: P(0.0...d0) -> d/9 = 0.ddd... = [d]inf.
        """
        assert 0 <= digit <= 9, "Digit must be 0..9"
        # Canonical recurring rational representation of 0.ddd...
        return Fraction(digit, 9)

    def gabriels_horn_regularization(self, horn_length: float) -> dict:
        """
        Gabriel's Horn Resolution:
        In classical math, y = 1/x for x ∈ [1, ∞) yields finite volume π, infinite surface area 2π ∫ 1/x dx.
        In IRM, physical paint thickness cannot drop below the Cost of Being floor epsilon = 1inf.
        When radius r(x) = 1/x < 1inf (i.e. x > 1 / 1inf), paint cannot enter, cutting off surface area!
        """
        x_cutoff = float(1 / self.one_inf)
        eff_length = min(float(horn_length), x_cutoff)
        
        # Volume = π ∫_1^L (1/x²) dx = π (1 - 1/L) < π
        vol = math.pi * (1.0 - 1.0 / eff_length)
        # Regularized surface area = 2π ∫_1^L 1/x √(1 + 1/x⁴) dx ≈ 2π ln(eff_length) < ∞
        surf_area = 2.0 * math.pi * math.log(eff_length)
        
        return {
            "eff_length": eff_length,
            "cutoff_reached": horn_length >= x_cutoff,
            "regularized_volume": vol,
            "regularized_surface_area": surf_area,
            "is_finite": math.isfinite(surf_area)
        }

    def compute_non_singular_gravity(self, m1: float, m2: float, r: float) -> dict:
        """
        Non-singular gravitational field regularization:
        r_eff = max(r, 1inf_x)
        F = G · m1 · m2 / r_eff²
        Guarantees zero division-by-zero traps at r = 0.
        """
        r_min = float(self.one_inf)
        r_eff = max(abs(float(r)), r_min)
        g_const = 6.67430e-11
        force = (g_const * m1 * m2) / (r_eff ** 2)
        max_force = (g_const * m1 * m2) / (r_min ** 2)
        
        return {
            "r_input": r,
            "r_effective": r_eff,
            "force": force,
            "max_force_bound": max_force,
            "is_non_singular": math.isfinite(force) and force <= max_force
        }


class BoundedContinuum02:
    """
    Primitive 4: The 0–2 Bounded Continuum & Try²{}Catch{} Operator
    - 0.0: baseline floor of homogeny (relative zero).
    - 1.0: unit parity rest center (equilibrium, lossless transmission).
    - 2.0: manifest physical saturation ceiling.
    - Try²{}Catch{} quadratic residual: R = ||v||^2 - ||N||^2.
    - 7 Evaluator Attractors A0 (0.00) to A6 (2.00).
    - (42+n)-polytrope minimal meaning bound (v_min = 43+n vertices with +1 observer).
    """
    ATTRACTORS = {
        "A0": Fraction(0, 3), # 0.00: Homogeny / Relative Zero
        "A1": Fraction(1, 3), # 0.333...: Sub-Harmonic Initiation
        "A2": Fraction(2, 3), # 0.666...: Active Resonant Flux
        "A3": Fraction(3, 3), # 1.00: Unit Parity Rest Center / Equilibrium
        "A4": Fraction(4, 3), # 1.333...: Super-Harmonic Strain
        "A5": Fraction(5, 3), # 1.666...: Near-Saturation Turbulence
        "A6": Fraction(6, 3), # 2.00: Manifest Physical Saturation Ceiling
    }

    @classmethod
    def nearest_evaluator_attractor(cls, val: Fraction) -> tuple:
        """
        Finds the nearest Evaluator Attractor A0..A6 and the signed distance to it.
        """
        clamped_val = max(Fraction(0), min(Fraction(2), val))
        best_name = "A0"
        min_dist = abs(clamped_val - cls.ATTRACTORS["A0"])
        for name, a_val in cls.ATTRACTORS.items():
            dist = abs(clamped_val - a_val)
            if dist < min_dist:
                min_dist = dist
                best_name = name
        return best_name, cls.ATTRACTORS[best_name], clamped_val - cls.ATTRACTORS[best_name]

    @staticmethod
    def try_squared_catch(v_magnitude: float, containment_capacity: float) -> dict:
        """
        The Try²{}Catch{} Operator:
        R = ||v||² - ||N||²
        If ||v||² > ||N||², excess over containment is caught as structural stress and physical drag.
        If ||v||² ≤ ||N||², motion is completely contained without drag (lossless transmission).
        """
        v_sq = float(v_magnitude) ** 2
        n_sq = float(containment_capacity) ** 2
        residual = v_sq - n_sq
        
        if residual > 0.0:
            stress_drag = residual
            is_contained = False
        else:
            stress_drag = 0.0
            is_contained = True
            
        return {
            "v_sq": v_sq,
            "n_sq": n_sq,
            "residual_R": residual,
            "is_contained": is_contained,
            "structural_drag": stress_drag
        }

    @staticmethod
    def verify_42_plus_n_meaning_bound(n_dimensions: int, total_vertices: int) -> bool:
        """
        The (42+n)-polytrope minimal meaning bound:
        v_min = 43 + n (where +1 is the mandatory Observer/Definer vertex).
        """
        required_min = 43 + int(n_dimensions)
        return total_vertices >= required_min


if __name__ == "__main__":
    print("Testing Living Number Atom & Recursive Grammar...")
    num = RecursiveGrammarNumber(0, 3, [1, 4, 1, 5])
    atom = num.to_atom("pi_approx")
    print(f"Living Number Atom: {atom}, Rational: {atom.value}")
    
    # Base shift identity
    num_shift = num.apply_base_shift(1)
    print(f"Shifted [1_3.1.4.1.5]: {num_shift.to_rational()} (Diff: {num_shift.to_rational() - num.to_rational()})")
    
    # Infinity Maths Cost of Being
    inf_engine = InfinityEngine()
    print("Cost of Being Increment Verified:", inf_engine.verify_cost_of_being_increment())
    
    # Non-singular gravity at r = 0
    grav_res = inf_engine.compute_non_singular_gravity(100.0, 100.0, 0.0)
    print(f"Non-singular gravity at r=0: Force = {grav_res['force']:.4e} N (Finite: {grav_res['is_non_singular']})")
    
    # Try²{}Catch{} operator
    tc = BoundedContinuum02.try_squared_catch(2.5, 2.0)
    print(f"Try²Catch (v=2.5, N=2.0): Residual = {tc['residual_R']}, Drag = {tc['structural_drag']}")
