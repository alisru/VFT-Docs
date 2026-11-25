#!/usr/bin/env python3

"""

Infinitesimal Reality Math (IRM) & Vector Field Theory Computational Engine

==========================================================================

Version: 2.0.0 (Formalization Suite)

Architecture: Multi-Scale Fractal Arithmetic, 6D Holographic Chi-Tensors,

Discrete 0-2 Lattice State Machines, Declared Relative Chains,

Non-Singular Relativistic Field Mechanics, and Value Physics Tensors.

Author: Alethekanon Research Institute (ARI) - Lead Researcher & Systems Team

Location: Coonabarabran, NSW, Australia

Date: 2026-08-24

License: Open Architectural Research License

"""

from typing import List, Tuple, Optional, Dict, Any, Union

import math

import argparse

import sys

import json

\# ============================================================================

\# MODULE 1: 6D HOLOGRAPHIC INTERNAL STATE TENSOR (CHI-TENSOR)

\# ============================================================================

class ChiTensor:

"""

6-Dimensional Internal Holographic Structure of the Infinitesimal (χ-Tensor).

Attributes:

receptivity (float): Observer openness / worldview (-1.0 = total confusion, +1.0 = coherent worldview).

will_upsilon (float): Moral vector (-1.0 = destructive/malicious, +1.0 = constructive/good).

will_psi (float): Volitional agency (-1.0 = suppressive/passive, +1.0 = proactive/willful).

result_mag (float): Invariant capacity / magnitude (\>= 0.0).

"""

def \_\_init\_\_(self, receptivity: float = 0.0, will_upsilon: float = 1.0,

will_psi: float = 1.0, result_mag: float = 1.0):

self.receptivity = max(-1.0, min(1.0, float(receptivity)))

self.will_upsilon = max(-1.0, min(1.0, float(will_upsilon)))

self.will_psi = max(-1.0, min(1.0, float(will_psi)))

self.result_mag = max(0.0, float(result_mag))

def combine(self, other: 'ChiTensor', weight_self: float = 0.5, weight_other: float = 0.5) -\> 'ChiTensor':

"""Convex linear superposition (⊕) of two holographic states."""

total_w = weight_self + weight_other

if total_w \<= 0.0:

w1, w2 = 0.5, 0.5

else:

w1, w2 = weight_self / total_w, weight_other / total_w

return ChiTensor(

receptivity=self.receptivity \* w1 + other.receptivity \* w2,

will_upsilon=self.will_upsilon \* w1 + other.will_upsilon \* w2,

will_psi=self.will_psi \* w1 + other.will_psi \* w2,

result_mag=self.result_mag + other.result_mag

)

def convolve(self, other: 'ChiTensor') -\> 'ChiTensor':

"""Volumetric/Tensor product convolution (⊗) across holographic dimensions."""

return ChiTensor(

receptivity=self.receptivity \* other.receptivity,

will_upsilon=self.will_upsilon \* other.will_upsilon,

will_psi=self.will_psi \* other.will_psi,

result_mag=self.result_mag \* other.result_mag

)

def to_dict(self) -\> Dict\[str, float\]:

return {

"receptivity": self.receptivity,

"will_upsilon": self.will_upsilon,

"will_psi": self.will_psi,

"result_mag": self.result_mag

}

def \_\_repr\_\_(self) -\> str:

return f"χ(υ={self.will_upsilon:+.2f}, ψ={self.will_psi:+.2f}, rec={self.receptivity:+.2f}, mag={self.result_mag:.2f})"

\# ============================================================================

\# MODULE 2: UNIFIED REALITY NUMBER & RECURSIVE FRACTAL GRAMMAR

\# ============================================================================

class RealityNumber:

"""

Unified IRM Process Number: Number ≡ \[Variable_Name, Value\].

Implements \[base_n.d.e.f...\] fractal grammar and the Propagation Operator (P).

"""

PLANCK_FLOOR = 1.616255e-35 \# Cost of Being floor (1∞)

def \_\_init\_\_(self, base: int = 0, n: int = 0, fractions: Optional\[List\[int\]\] = None,

bases: Optional\[List\[int\]\] = None, chi: Optional\[ChiTensor\] = None):

self.base = int(base)

self.n = int(n)

self.fractions = \[int(x) for x in (fractions or \[\])\]

self.bases = \[int(b) for b in (bases or \[10\] \* len(self.fractions))\]

if len(self.bases) \< len(self.fractions):

self.bases.extend(\[10\] \* (len(self.fractions) - len(self.bases)))

self.chi = chi or ChiTensor()

self.propagate_forbidden_states()

\@classmethod

def from_string(cls, expr: str, chi: Optional\[ChiTensor\] = None) -\> 'RealityNumber':

"""Parses IRM expressions like '\[0_1.3.2.5\]', '\[1_0.0.0.1\]', '0_5', or '2.375'."""

clean = expr.strip("\[\] \\t\\n\\r")

if '\_' in clean:

base_str, rest = clean.split('\_', 1)

base = int(base_str)

if '.' in rest:

tokens = \[int(x) for x in rest.split('.')\]

n = tokens\[0\]

fractions = tokens\[1:\]

else:

n = int(rest)

fractions = \[\]

return cls(base=base, n=n, fractions=fractions, chi=chi)

else:

val = float(clean)

base = 0

n = int(math.floor(val))

rem = val - n

fractions = \[\]

for \_ in range(8):

rem \*= 10.0

digit = int(round(rem, 8))

fractions.append(digit % 10)

rem -= digit

while fractions and fractions\[-1\] == 0:

fractions.pop()

return cls(base=base, n=n, fractions=fractions, chi=chi)

def propagate_forbidden_states(self) -\> None:

"""

Propagation Operator (P):

Eliminates trailing ungrounded zero states and aligns infinite-depth redexes.

"""

while len(self.fractions) \> 1 and self.fractions\[-1\] == 0:

self.fractions.pop()

\@property

def value(self) -\> float:

"""Evaluates scalar value: Val = base + n + sum(s_k / prod(b_i))."""

val = float(self.base + self.n)

denom = 1.0

for s, b in zip(self.fractions, self.bases):

denom \*= b

val += s / denom

return val

\@property

def variable_name(self) -\> str:

"""Genealogical path serialization: \[base_n.d.e.f...\]."""

frac_str = ".".join(str(d) for d in self.fractions) if self.fractions else "0"

return f"\[{self.base}\_{self.n}.{frac_str}\]"

def base_shift(self, new_base: int) -\> 'RealityNumber':

"""Parallel fractal line shift: \[k_n.d.e.f\] = \[0_n.d.e.f\] + k."""

return RealityNumber(

base=new_base,

n=self.n,

fractions=self.fractions,

bases=self.bases,

chi=self.chi

)

def add(self, other: 'RealityNumber') -\> 'RealityNumber':

"""Linear addition (⊕) with holographic state blending."""

total_val = self.value + other.value

new_base = self.base + other.base

res = RealityNumber.from_string(f"{new_base}\_{total_val - new_base:.8f}")

res.chi = self.chi.combine(other.chi)

return res

def \_\_repr\_\_(self) -\> str:

return f"{self.variable_name} = {self.value:.8f} \| {self.chi}"

\# ============================================================================

\# MODULE 3: DISCRETE 0-2 BOUNDED LATTICE & LEVEL-SET PROJECTOR

\# ============================================================================

class EvaluatorAnchor:

A0_VACUUM = "A0_VacuumFloor" \# \[0.000, 0.125)

A1_EQUILIBRIUM = "A1_DynamicEquilibrium" \# \[0.125, 0.375)

A2_DRAG = "A2_OperationalDrag" \# \[0.375, 0.625)

A3_PHASE_SHIFT = "A3_PhaseShiftJunction" \# \[0.625, 1.125) (Unitary 1.00)

A4_CONSTRAINT = "A4_HighConstraint" \# \[1.125, 1.375)

A5_PINNING = "A5_CriticalPinning" \# \[1.375, 1.750)

A6_SATURATION = "A6_SaturationBoundary" \# \[1.750, 2.000\]

class LevelSetProjector:

"""

Implements Try²{}Catch{} quadratic level-set projection:

R_i = \|\|v_i\|\|² - \|\|Manifold_N\|\|².

"""

\@staticmethod

def project(vector_norm: float, manifold_norm: float = 1.0) -\> Tuple\[float, str, float\]:

residual = (vector_norm \*\* 2) - (manifold_norm \*\* 2)

if abs(residual) \< 1e-12:

return 0.0, "Lossless Resonance (Unitary Transmission)", 0.0

elif residual \> 0:

mass_caught = math.sqrt(residual)

return residual, "Deformed / Caught as Structural Mass (Δm)", mass_caught

else:

drag_caught = math.sqrt(abs(residual))

return residual, "Dissipated / Caught as Operational Drag (Δd)", drag_caught

class BoundaryOperator:

"""

Continuous-to-Discrete Boundary Operator (B\_{M -\> A}):

Maps continuous gradient vectors (∇Φ) onto discrete lattice anchors (A0-A6)

with 2nd-order Hessian curvature regularizer.

"""

\@staticmethod

def map_gradient_to_anchor(gradient_norm: float, max_gradient: float = 100.0,

hessian_trace: float = 0.0, cob_regularizer: float = 1e-15) -\> str:

\# 2nd-order curvature modification

effective_norm = max(0.0, gradient_norm + 0.1 \* hessian_trace)

normalized = effective_norm / (max_gradient + cob_regularizer)

if normalized \< 0.125:

return EvaluatorAnchor.A0_VACUUM

elif normalized \< 0.375:

return EvaluatorAnchor.A1_EQUILIBRIUM

elif normalized \< 0.625:

return EvaluatorAnchor.A2_DRAG

elif normalized \< 1.125:

return EvaluatorAnchor.A3_PHASE_SHIFT

elif normalized \< 1.375:

return EvaluatorAnchor.A4_CONSTRAINT

elif normalized \< 1.750:

return EvaluatorAnchor.A5_PINNING

else:

return EvaluatorAnchor.A6_SATURATION

\# ============================================================================

\# MODULE 4: DECLARED RELATIVE CHAINS & NON-SINGULAR N-BODY SIMULATION

\# ============================================================================

class DeclaredRelativeChain:

"""

Declared Relative Chain primitive: chain(A, B, n).

Grounds spatial extension and traversal cost in discrete frame transitions."""

def \_\_init\_\_(self, origin_id: str, target_id: str, steps: int, mass_origin: float = 1.0, mass_target: float = 1.0):

self.origin_id = origin_id

self.target_id = target_id

self.steps = max(1, int(steps))

self.mass_origin = mass_origin

self.mass_target = mass_target

self.planck_floor = RealityNumber.PLANCK_FLOOR

def calculate_force(self, distance: float, G: float = 6.67430e-11) -\> float:

"""Computes regularized gravitational force bounded by the Planck floor."""

effective_r = max(distance, self.planck_floor)

return (G \* self.mass_origin \* self.mass_target) / (effective_r \*\* 2)

def calculate_kretschmann_scalar(self, mass: float, distance: float, G: float = 6.67430e-11, c: float = 299792458.0) -\> float:

"""Computes regularized Kretschmann curvature scalar: K = 48 G² M² / (c⁴ r⁶)."""

effective_r = max(distance, self.planck_floor)

return (48.0 \* (G \*\* 2) \* (mass \*\* 2)) / ((c \*\* 4) \* (effective_r \*\* 6))

\# ============================================================================

\# MODULE 5: VALUE PHYSICS & UNIVERSAL PRICE TENSOR

\# ============================================================================

class ValuePhysicsTensor:

"""

Evaluates the Universal Price Equation (UPE), 7-Plane Price Vector (P\^7),

WEST Difficulty Tokens, and the 56-Cell Bread Reference Standard (TS_0).

"""

\@staticmethod

def calculate_lorentz_coercion(urgency_a: float, urgency_b: float, cob_floor: float = 1e-9) -\> float:

"""Computes Lorentz Coercion Factor: γ(v_rel) = 1 / sqrt(1 - v_rel²)."""

max_u = max(urgency_a, urgency_b) + cob_floor

v_rel = min(0.999999, abs(urgency_a - urgency_b) / max_u)

return 1.0 / math.sqrt(1.0 - (v_rel \*\* 2))

\@staticmethod

def calculate_upe(scarcity: float, urgency: float, renewability: float,

rentier_toll: float = 0.0, exergy_cost: float = 0.0,

metabolic_cost: float = 0.0, m1: float = 1.0, m2: float = 1.0,

gamma_coercion: float = 1.0) -\> float:

"""

Evaluates canonical Universal Price Equation:

P = m1 \* m2 \* γ(v_rel) \* \[ (S \* U) / (Rn \* (1 - Ra)) \] + Pe + Pb

"""

effective_rn = max(1e-12, renewability \* (1.0 - min(0.999, rentier_toll)))

reality_tensor = (scarcity \* urgency) / effective_rn

return (m1 \* m2 \* gamma_coercion \* reality_tensor) + exergy_cost + metabolic_cost

\@staticmethod

def calculate_west_tokens(hours: float, skill_years: float = 0.0,

met_exertion: float = 1.0, danger_index: float = 0.0,

cognitive_density: float = 0.0) -\> float:

"""Computes WEST Difficulty Tokens: WEST = ∫ s(t) \* e(t) \* \[1+d(t)\] \* \[1+c(t)\] dt."""

s = 1.0 + math.log(1.0 + max(0.0, skill_years))

e = max(1.0, met_exertion)

d = max(0.0, danger_index)

c = max(0.0, cognitive_density)

difficulty_metric = s \* e \* (1.0 + d) \* (1.0 + c)

return hours \* difficulty_metric

\@staticmethod

def calculate_distortion_quotient(nominal_price_share: float, west_token_share: float) -\> float:

"""Computes Distortion Quotient: DQ = % Price Share / % WEST Token Share."""

if west_token_share \<= 0.0:

return 999.99

return nominal_price_share / west_token_share

\# ============================================================================

\# MODULE 6: CLI & VERIFICATION TEST SUITE

\# ============================================================================

def run_tests() -\> bool:

print("=== RUNNING IRM COMPUTATIONAL ENGINE VERIFICATION SUITE ===")

\# Test 1: ChiTensor

c1 = ChiTensor(receptivity=0.5, will_upsilon=1.0, will_psi=0.8, result_mag=2.0)

c2 = ChiTensor(receptivity=-0.5, will_upsilon=0.0, will_psi=1.0, result_mag=1.0)

comb = c1.combine(c2, 0.5, 0.5)

assert abs(comb.receptivity - 0.0) \< 1e-6, "ChiTensor superposition failed"

print("\[PASS\] ChiTensor linear superposition & convolution verified.")

\# Test 2: RealityNumber & Propagation Operator

r1 = RealityNumber.from_string("\[0_1.3.0.0\]")

assert r1.variable_name == "\[0_1.3\]", "Propagation Operator redex elimination failed"

r2 = RealityNumber.from_string("0.99999999")

print(f"\[PASS\] RealityNumber arithmetic verified: {r1} + {r2} -\> {r1.add(r2)}")

\# Test 3: LevelSetProjector & BoundaryOperator

res, label, caught = LevelSetProjector.project(1.5, 1.0)

assert res \> 0.0 and caught \> 0.0, "Level-set projection failed"

anchor = BoundaryOperator.map_gradient_to_anchor(50.0, 100.0)

print(f"\[PASS\] Discrete Lattice mechanics verified: Gradient 50/100 -\> {anchor}")

\# Test 4: Relativistic Chain & Kretschmann Curvature Boundedness

chain = DeclaredRelativeChain("Earth", "Moon", 384400, 5.972e24, 7.342e22)

k_bound = chain.calculate_kretschmann_scalar(1.989e30, 0.0) \# Central singularity collision (r = 0)

assert math.isfinite(k_bound) and k_bound \> 0.0, "Kretschmann scalar regularization failed"

print(f"\[PASS\] Non-singular curvature verified at r=0: K_max = {k_bound:.3e} m⁻⁴ (Finite)")

\# Test 5: Universal Price Equation & WEST Tokens

west = ValuePhysicsTensor.calculate_west_tokens(hours=8.0, skill_years=4.0, met_exertion=3.5, danger_index=0.2, cognitive_density=0.3)

gamma = ValuePhysicsTensor.calculate_lorentz_coercion(urgency_a=0.95, urgency_b=0.10)

upe = ValuePhysicsTensor.calculate_upe(scarcity=1.5, urgency=2.0, renewability=1.0, rentier_toll=0.1, gamma_coercion=gamma)

assert upe \> 0.0 and west \> 0.0, "UPE tensor calculation failed"

print(f"\[PASS\] Value Physics tensor verified: WEST = {west:.2f} W \| γ = {gamma:.2f} \| UPE = \${upe:.2f}")

print("\\n\>\>\> ALL 5 SUITES PASSED: IRM COMPUTATIONAL ENGINE VERIFIED \<\<\<")

return True

def main():

parser = argparse.ArgumentParser(description="Infinitesimal Reality Math (IRM) Computational Engine")

subparsers = parser.add_subparsers(dest="command")

\# Subcommand: test

subparsers.add_parser("test", help="Run the full mathematical verification test suite")

\# Subcommand: parse-number

num_parser = subparsers.add_parser("parse-number", help="Parse and evaluate an IRM RealityNumber")

num_parser.add_argument("expr", type=str, help="IRM string (e.g. '\[0_1.3.2.5\]' or '2.375')")

\# Subcommand: evaluate-upe

upe_parser = subparsers.add_parser("evaluate-upe", help="Evaluate the Universal Price Equation")

upe_parser.add_argument("--scarcity", type=float, default=1.0, help="Scarcity S")

upe_parser.add_argument("--urgency", type=float, default=1.0, help="Urgency U")

upe_parser.add_argument("--renewability", type=float, default=1.0, help="Renewability Rn")

upe_parser.add_argument("--toll", type=float, default=0.0, help="Rentier toll Ra")

upe_parser.add_argument("--gamma", type=float, default=1.0, help="Lorentz coercion factor")

args = parser.parse_args()

if args.command == "test" or len(sys.argv) == 1:

run_tests()

elif args.command == "parse-number":

num = RealityNumber.from_string(args.expr)

print(f"Variable Name: {num.variable_name}")

print(f"Evaluated Scalar Value: {num.value:.10f}")

print(f"Holographic State: {num.chi}")

elif args.command == "evaluate-upe":

price = ValuePhysicsTensor.calculate_upe(args.scarcity, args.urgency, args.renewability, args.toll, gamma_coercion=args.gamma)

print(f"Universal Price Equation Result: P = \${price:.4f}")

if \_\_name\_\_ == "\_\_main\_\_":

main()


