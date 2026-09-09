#!/usr/bin/env python3
"""
irm_engine.py - Infinitesimal Reality Math computational engine.

Reference implementation of the architecture specified in Formal Paper 8
("Computational Field Simulation of Infinitesimal Reality Math"), built
against that paper's equations rather than against the partial v1 listing
in the `IRM Computational Engine` doc.

Six modules, per Paper 8 section 1:
  1-2  ChiTensor, RealityNumber, Propagation Operator  (exact rational)
  3    LatticeManifold, Try^2{}Catch{}, BoundaryOperator (Hessian-regularised)
  4-5  DeclaredRelativeChain, non-singular N-body, ValuePhysicsTensor
  6    CLI: test | parse-number | evaluate-upe | simulate-chain

Design note: Paper 8 s2.1 states evaluation "proceeds via exact rational
summation". This implementation therefore uses fractions.Fraction throughout
the number system. Floats appear only in the physics/value modules, where the
paper's own formulae are float-valued.
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

# --------------------------------------------------------------------------
# Physical constants (Paper 8 s3.1-3.2)
# --------------------------------------------------------------------------
G_NEWTON = 6.6743e-11          # m^3 kg^-1 s^-2
C_LIGHT = 299792458.0          # m s^-1
PLANCK_LENGTH = 1.616255e-35   # m   -- the Cost of Being floor 1_inf_x
COB_UNIT_J = 5.268e-80         # J   -- Cost of Being per Planck frame
M_SUN = 1.98892e30             # kg


# ==========================================================================
# MODULE 0: The infinitesimal ledger
# ==========================================================================
@dataclass
class Infinitesimal:
    """
    A ledger of 1_inf quanta indexed by fractional depth.

    Non-Archimedean: no finite multiple of any quantum reaches a standard
    positive real. The ledger exists so that residues the Propagation
    Operator materialises are *counted* rather than silently dropped --
    which is the specific failure mode Paper 8 s2.2 says IEEE 754 exhibits.
    """
    quanta: Dict[int, int] = field(default_factory=dict)

    def add(self, depth: int, count: int = 1) -> "Infinitesimal":
        q = dict(self.quanta)
        q[depth] = q.get(depth, 0) + count
        if q[depth] == 0:
            del q[depth]
        return Infinitesimal(q)

    def merge(self, other: "Infinitesimal") -> "Infinitesimal":
        q = dict(self.quanta)
        for d, c in other.quanta.items():
            q[d] = q.get(d, 0) + c
            if q[d] == 0:
                del q[d]
        return Infinitesimal(q)

    @property
    def total(self) -> int:
        return sum(self.quanta.values())

    def is_zero(self) -> bool:
        return not self.quanta

    def __repr__(self) -> str:
        if not self.quanta:
            return "0"
        return " + ".join(
            f"{c}_inf_{d}" if c != 1 else f"1_inf_{d}"
            for d, c in sorted(self.quanta.items())
        )


# ==========================================================================
# MODULE 1: The holographic chi-tensor
# ==========================================================================
def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, float(x)))


@dataclass
class ChiTensor:
    """
    Internal holographic structure of the infinitesimal.

    NOTE ON DIMENSION: the docs call this the "6-dimensional holographic
    chi-tensor", but Paper 8 s2.1 types it as chi in R^4 and every listing
    carries exactly four components. Four is implemented; the "6D" label is
    unreconciled in the source corpus.
    """
    receptivity: float = 0.0    # confusion [-1] <-> worldview [+1]
    will_upsilon: float = 1.0   # bad [-1] <-> good [+1]
    will_psi: float = 1.0       # suppressive [-1] <-> proactive [+1]
    result_mag: float = 1.0     # force / capacity >= 0

    def __post_init__(self) -> None:
        self.receptivity = _clamp(self.receptivity, -1.0, 1.0)
        self.will_upsilon = _clamp(self.will_upsilon, -1.0, 1.0)
        self.will_psi = _clamp(self.will_psi, -1.0, 1.0)
        self.result_mag = max(0.0, float(self.result_mag))

    def combine(self, other: "ChiTensor",
                weight_self: float = 0.5,
                weight_other: float = 0.5) -> "ChiTensor":
        """Linear blend (+). Magnitudes add; orientations average by weight."""
        total_w = weight_self + weight_other
        if math.isclose(total_w, 0.0, abs_tol=1e-15):
            # The v1 listing divides here unguarded and raises ZeroDivisionError
            # whenever the two weights cancel. Fall back to equal weighting.
            w1 = w2 = 0.5
        else:
            w1, w2 = weight_self / total_w, weight_other / total_w
        return ChiTensor(
            receptivity=self.receptivity * w1 + other.receptivity * w2,
            will_upsilon=self.will_upsilon * w1 + other.will_upsilon * w2,
            will_psi=self.will_psi * w1 + other.will_psi * w2,
            result_mag=self.result_mag + other.result_mag,
        )

    def convolve(self, other: "ChiTensor") -> "ChiTensor":
        """Volumetric product (x): componentwise convolution."""
        return ChiTensor(
            receptivity=self.receptivity * other.receptivity,
            will_upsilon=self.will_upsilon * other.will_upsilon,
            will_psi=self.will_psi * other.will_psi,
            result_mag=self.result_mag * other.result_mag,
        )

    def to_dict(self) -> Dict[str, float]:
        return {
            "receptivity": self.receptivity,
            "will_upsilon": self.will_upsilon,
            "will_psi": self.will_psi,
            "result_mag": self.result_mag,
        }

    def __repr__(self) -> str:
        return (f"chi(u={self.will_upsilon:+.2f}, psi={self.will_psi:+.2f}, "
                f"rec={self.receptivity:+.2f}, mag={self.result_mag:.2f})")


# ==========================================================================
# MODULE 2: RealityNumber + the Propagation Operator
# ==========================================================================
class RealityNumber:
    """
    Number == [Variable_Name, Value] in the [base_n.d.e.f...] fractal grammar.

    Standard part is an exact Fraction. A repeating-(b-1) tail is carried as a
    flag rather than an infinite digit list, so the Propagation Operator can be
    applied without truncation. Materialised residues land in `inf`.
    """

    def __init__(self,
                 base: int = 0,
                 n: int = 0,
                 fractions: Optional[Sequence[int]] = None,
                 bases: Optional[Sequence[int]] = None,
                 nines_tail: bool = False,
                 inf: Optional[Infinitesimal] = None,
                 chi: Optional[ChiTensor] = None):
        self.base = int(base)
        self.n = int(n)
        self.fractions: List[int] = [int(x) for x in (fractions or [])]
        self.bases: List[int] = [int(b) for b in (bases or [])]
        if len(self.bases) < len(self.fractions):
            self.bases.extend([10] * (len(self.fractions) - len(self.bases)))
        self.bases = self.bases[:len(self.fractions)]
        for i, (s, b) in enumerate(zip(self.fractions, self.bases)):
            if b < 2:
                raise ValueError(f"base at depth {i + 1} must be >= 2, got {b}")
            if not (0 <= s < b):
                raise ValueError(
                    f"digit {s} out of range for base {b} at depth {i + 1}")
        self.nines_tail = bool(nines_tail)
        self.inf = inf or Infinitesimal()
        self.chi = chi or ChiTensor()

    # -- construction ------------------------------------------------------
    @classmethod
    def from_string(cls, expr: str,
                    chi: Optional[ChiTensor] = None) -> "RealityNumber":
        """Parse '[0_1.3.2.5]', '0_5', or a plain decimal like '2.375'."""
        clean = expr.strip().strip("[]").strip()
        if "_" in clean:
            base_str, rest = clean.split("_", 1)
            base = int(base_str)
            if "." in rest:
                tokens = [int(t) for t in rest.split(".")]
                return cls(base=base, n=tokens[0], fractions=tokens[1:], chi=chi)
            return cls(base=base, n=int(rest), chi=chi)

        # Plain decimal -> exact, via Fraction. No float round-trip, so no
        # truncation and no chance of the v1 `int(round(rem, 8))` overflow bug
        # (which produced digit 10 and a negative remainder on 0.999... inputs).
        frac = Fraction(clean)
        sign = -1 if frac < 0 else 1
        frac = abs(frac)
        n = int(frac)
        rem = frac - n
        digits: List[int] = []
        while rem != 0 and len(digits) < 64:
            rem *= 10
            d = int(rem)
            digits.append(d)
            rem -= d
        return cls(base=0, n=sign * n, fractions=digits, chi=chi)

    # -- evaluation --------------------------------------------------------
    @property
    def standard(self) -> Fraction:
        """Exact standard part.  Val = base + n + sum s_i / prod_{j<=i} b_j."""
        val = Fraction(self.base + self.n)
        denom = Fraction(1)
        for s, b in zip(self.fractions, self.bases):
            denom *= b
            val += Fraction(s) / denom
        if self.nines_tail:
            # repeating (b-1) from depth k+1 sums to exactly 1/denom
            val += Fraction(1) / denom
        return val

    @property
    def value(self) -> float:
        return float(self.standard)

    @property
    def variable_name(self) -> str:
        if self.fractions:
            frac_str = ".".join(str(d) for d in self.fractions)
            if self.nines_tail:
                b = self.bases[-1] if self.bases else 10
                frac_str += f".{b - 1}~"
        else:
            frac_str = "0"
        return f"[{self.base}_{self.n}.{frac_str}]"

    # -- the Propagation Operator -----------------------------------------
    def propagate(self) -> "RealityNumber":
        """
        Propagation Operator P, per Paper 8 s2.2:

            P( <..., k, 0> )  ->  <..., k-1, 9, 9, 9, ...> + 1_inf_k

        Cascades an ungrounded trailing zero into a repeating-(b-1) tail and
        materialises the infinitesimal residue. The standard part is conserved
        *exactly* -- 0.k000... and 0.(k-1)999... are the same real -- so the
        operator's whole content is that the residue is now on the books
        instead of being discarded.

        Returns self unchanged when there is no ungrounded trailing zero.
        """
        if self.nines_tail or not self.fractions:
            return self
        if self.fractions[-1] != 0:
            return self

        digits = list(self.fractions)
        bases = list(self.bases)
        while digits and digits[-1] == 0:
            digits.pop()
            bases.pop()
        if not digits:
            # [0_n.0.0...] -- the whole tail was ungrounded; cascade into n.
            if self.n == 0 and self.base == 0:
                return RealityNumber(base=self.base, n=self.n,
                                     chi=self.chi, inf=self.inf)
            return RealityNumber(
                base=self.base, n=self.n - 1,
                fractions=[9], bases=[10], nines_tail=True,
                inf=self.inf.add(0), chi=self.chi,
            )

        depth = len(digits)
        digits[-1] -= 1
        return RealityNumber(
            base=self.base, n=self.n,
            fractions=digits, bases=bases,
            nines_tail=True,
            inf=self.inf.add(depth),
            chi=self.chi,
        )

    def canonicalise(self) -> "RealityNumber":
        """
        The *other* reading of P, and the one the v1 listing implements:
        strip ungrounded trailing zeros without materialising a residue.
        Value-identical, but the infinitesimal is discarded -- exactly the
        behaviour s2.2 says the operator exists to prevent.
        """
        digits = list(self.fractions)
        bases = list(self.bases)
        while len(digits) > 1 and digits[-1] == 0:
            digits.pop()
            bases.pop()
        if digits == [0]:
            digits, bases = [], []
        return RealityNumber(base=self.base, n=self.n, fractions=digits,
                             bases=bases, nines_tail=self.nines_tail,
                             inf=self.inf, chi=self.chi)

    # -- arithmetic --------------------------------------------------------
    def _rebuild(self, total: Fraction, base: int, inf: Infinitesimal,
                 chi: ChiTensor, max_depth: int = 32) -> "RealityNumber":
        rem_val = total - base
        n = math.floor(rem_val)
        rem = rem_val - n
        digits: List[int] = []
        while rem != 0 and len(digits) < max_depth:
            rem *= 10
            d = int(rem)
            digits.append(d)
            rem -= d
        if rem != 0:
            # Do not silently drop the tail: book it as an infinitesimal.
            inf = inf.add(len(digits))
        return RealityNumber(base=base, n=n, fractions=digits,
                             inf=inf, chi=chi)

    def add(self, other: "RealityNumber") -> "RealityNumber":
        """Linear combination (+) with chi blending. Exact in the standard part."""
        total = self.standard + other.standard
        new_base = self.base + other.base
        w1 = abs(self.value) or 1.0
        w2 = abs(other.value) or 1.0
        return self._rebuild(total, new_base,
                             self.inf.merge(other.inf),
                             self.chi.combine(other.chi, w1, w2))

    def multiply(self, other: "RealityNumber") -> "RealityNumber":
        """Volumetric product (x) with chi convolution. Exact in the standard part."""
        total = self.standard * other.standard
        return self._rebuild(total, 0,
                             self.inf.merge(other.inf),
                             self.chi.convolve(other.chi))

    def base_shift(self, new_base: int) -> "RealityNumber":
        """Parallel fractal line shift: [k_n.d.e.f] = [0_n.d.e.f] + k."""
        return RealityNumber(base=new_base, n=self.n, fractions=self.fractions,
                             bases=self.bases, nines_tail=self.nines_tail,
                             inf=self.inf, chi=self.chi)

    def relative_perspective(self, target: "RealityNumber") -> Fraction:
        """0-2 lattice perspective: R(p, t) = 1 + (t - p)."""
        return Fraction(1) + (target.standard - self.standard)

    def __repr__(self) -> str:
        infs = "" if self.inf.is_zero() else f" + {self.inf}"
        return f"{self.variable_name} (Val={self.value:.8f}{infs}) {self.chi}"


# ==========================================================================
# MODULE 3: 0-2 lattice, Try^2{}Catch{}, boundary operator
# ==========================================================================
class LatticeManifold:
    """0-2 bounded meta-potential manifold and the 7 evaluator anchors."""

    # Half-open [lo, hi) so the anchors partition [0, 2] without the overlap
    # in the v1 listing, where 0.125 / 0.375 / ... matched two anchors and the
    # first-match-wins loop silently assigned the lower one.
    EVALUATOR_ANCHORS: Dict[int, Dict[str, Any]] = {
        0: {"name": "A0", "label": "Vacuum Floor / No Gradient",      "range": (0.000, 0.125), "status": "Ground / Rest"},
        1: {"name": "A1", "label": "Dynamic Equilibrium",             "range": (0.125, 0.375), "status": "Stable Action"},
        2: {"name": "A2", "label": "Mild Resistance / Drag",          "range": (0.375, 0.625), "status": "Operational Friction"},
        3: {"name": "A3", "label": "Junction / Phase Shift Boundary", "range": (0.625, 1.125), "status": "Neutral Calibration Point"},
        4: {"name": "A4", "label": "Strong Resistance / Constraint",  "range": (1.125, 1.375), "status": "High Pressure"},
        5: {"name": "A5", "label": "Near Saturation / Pinning",       "range": (1.375, 1.750), "status": "Critical Strain"},
        6: {"name": "A6", "label": "Black Hole / Saturation Boundary", "range": (1.750, 2.000), "status": "Opacity Threshold"},
    }

    @staticmethod
    def classify_evaluator(val: float) -> Dict[str, Any]:
        if val < 0.0:
            return {"name": "Under-flow", "label": "Sub-zero Coordinate (Prior Frame)",
                    "status": "Unresolvable in Local Frame", "index": -1}
        if val > 2.0:
            return {"name": "Unobservable", "label": "Asymptotic Trap (> 2.0)",
                    "status": "Semantic Black Hole / Opaque", "index": 7}
        for idx, data in LatticeManifold.EVALUATOR_ANCHORS.items():
            lo, hi = data["range"]
            if lo <= val < hi or (idx == 6 and val <= 2.0 + 1e-12):
                return {**data, "index": idx}
        return {**LatticeManifold.EVALUATOR_ANCHORS[3], "index": 3}

    @staticmethod
    def try_squared_projection(vector_mag: float, manifold_mag: float = 1.0
                               ) -> Tuple[float, str, Dict[str, float]]:
        """
        try^2 { vector } catch { remainder }, Paper 8 s4.1:
            R = ||v||^2 - ||Manifold||^2
            R > 0 -> structural mass   dm = sqrt(R)
            R < 0 -> operational drag  dd = sqrt(|R|)
        """
        remainder = vector_mag ** 2 - manifold_mag ** 2
        catch: Dict[str, float] = {"delta_mass": 0.0, "delta_drag": 0.0}
        if math.isclose(remainder, 0.0, abs_tol=1e-12):
            status = "Lossless Fit (0.0 remainder - local transmission)"
        elif remainder > 0.0:
            catch["delta_mass"] = math.sqrt(remainder)
            status = (f"Overflow Residue (+{remainder:.6f} -> structural mass "
                      f"{catch['delta_mass']:.6f})")
        else:
            catch["delta_drag"] = math.sqrt(abs(remainder))
            status = (f"Underflow Vacuum ({remainder:.6f} -> operational drag "
                      f"{catch['delta_drag']:.6f})")
        return remainder, status, catch

    @staticmethod
    def check_polytrope_vertices(dimensions: int, vertices: int) -> Dict[str, Any]:
        """(7 x 6 + n) polytrope condition: d = 42 + n -> v_min = 43 + n."""
        required_v = dimensions + 1
        return {
            "dimension": dimensions,
            "vertices_provided": vertices,
            "minimum_vertices_for_volume": required_v,
            "has_internal_volume": vertices >= required_v,
            "is_flat_zero_volume_hyperplane": vertices == dimensions,
            "observer_vertex_active": vertices > dimensions,
        }


class BoundaryOperator:
    """
    Continuous-to-discrete boundary operator B: M -> A, Paper 8 s4.2.

        sigma_eff(x) = (|grad Phi(x)| + kappa * |Tr(Hess Phi(x))|)
                       / (|grad Phi|_max + 1_inf_Phi)

    with kappa = 0.10 the boundary dampening coefficient.
    """

    KAPPA = 0.10

    def __init__(self, phi: Callable[[Sequence[float]], float], dim: int,
                 h: float = 1e-4, kappa: Optional[float] = None):
        self.phi = phi
        self.dim = dim
        self.h = h
        self.kappa = self.KAPPA if kappa is None else kappa

    def grad(self, x: Sequence[float]) -> List[float]:
        g = []
        for i in range(self.dim):
            xp, xm = list(x), list(x)
            xp[i] += self.h
            xm[i] -= self.h
            g.append((self.phi(xp) - self.phi(xm)) / (2 * self.h))
        return g

    def hessian_trace(self, x: Sequence[float]) -> float:
        """Tr(grad^2 Phi) -- the Laplacian, by second central differences."""
        c = self.phi(x)
        tr = 0.0
        for i in range(self.dim):
            xp, xm = list(x), list(x)
            xp[i] += self.h
            xm[i] -= self.h
            tr += (self.phi(xp) - 2 * c + self.phi(xm)) / (self.h ** 2)
        return tr

    def sigma_eff(self, x: Sequence[float], grad_max: float) -> float:
        gm = math.sqrt(sum(g * g for g in self.grad(x)))
        htr = abs(self.hessian_trace(x))
        return (gm + self.kappa * htr) / (grad_max + COB_UNIT_J)

    def project(self, x: Sequence[float], grad_max: float) -> Dict[str, Any]:
        s = self.sigma_eff(x, grad_max)
        # sigma_eff is a normalised strain in [0, inf); the anchors live on
        # [0, 2]. Paper 8 does not state the map. Scaling by 2 is the natural
        # reading (full relative strain -> saturation boundary A6).
        coord = min(2.0, 2.0 * s)
        return {"sigma_eff": s, "lattice_coord": coord,
                "anchor": LatticeManifold.classify_evaluator(coord)}

    def estimate_lipschitz(self, samples: Sequence[Sequence[float]],
                           grad_max: float) -> float:
        """
        Empirical Lipschitz constant of B over the sample set. Paper 7 claims
        B is Lipschitz-continuous; this measures the realised constant so the
        claim is checkable rather than asserted.
        """
        best = 0.0
        cache = [self.sigma_eff(p, grad_max) for p in samples]
        for i in range(len(samples)):
            for j in range(i + 1, len(samples)):
                dx = math.sqrt(sum((p - q) ** 2
                                   for p, q in zip(samples[i], samples[j])))
                if dx < 1e-12:
                    continue
                best = max(best, abs(cache[i] - cache[j]) / dx)
        return best


# ==========================================================================
# MODULE 4: Declared relative chains & non-singular field mechanics
# ==========================================================================
def regularised_force(m1: float, m2: float, r: float,
                      floor: float = PLANCK_LENGTH) -> float:
    """F_reg(r) = G m1 m2 / max(r, l_P)^2   -- Paper 8 s3.1."""
    return G_NEWTON * m1 * m2 / max(abs(r), floor) ** 2


def kretschmann(mass: float, r: float, floor: float = PLANCK_LENGTH) -> float:
    """K(r) = 48 G^2 M^2 / (c^4 max(r, l_P)^6)   -- Paper 8 s3.2."""
    return 48.0 * G_NEWTON ** 2 * mass ** 2 / (C_LIGHT ** 4 * max(abs(r), floor) ** 6)


def coulomb_regularised(q1: float, q2: float, r: float,
                        floor: float = PLANCK_LENGTH) -> float:
    k_e = 8.9875517923e9
    return k_e * q1 * q2 / max(abs(r), floor) ** 2


@dataclass
class DeclaredRelativeChain:
    """
    chain(A, B, n): spatial extension declared as n relative cells between two
    bodies, each cell bounded below by the Cost of Being floor. Distance is
    never a bare coordinate difference, so r = 0 is not representable.
    """
    a: float
    b: float
    n: int

    def __post_init__(self) -> None:
        if self.n < 1:
            raise ValueError("a declared chain needs at least one cell")

    @property
    def cell_size(self) -> float:
        return max(abs(self.b - self.a) / self.n, PLANCK_LENGTH)

    @property
    def separation(self) -> float:
        return self.cell_size * self.n

    def cells(self) -> List[Tuple[float, float]]:
        step = (self.b - self.a) / self.n
        return [(self.a + i * step, self.a + (i + 1) * step) for i in range(self.n)]


@dataclass
class Body:
    mass: float
    pos: List[float]
    vel: List[float]

    def copy(self) -> "Body":
        return Body(self.mass, list(self.pos), list(self.vel))


class NBodySimulation:
    """Non-singular N-body integrator: velocity Verlet over F_reg."""

    def __init__(self, bodies: Sequence[Body], floor: float = PLANCK_LENGTH):
        self.bodies = [b.copy() for b in bodies]
        self.floor = floor
        self.dim = len(self.bodies[0].pos)

    def _accelerations(self) -> List[List[float]]:
        n = len(self.bodies)
        acc = [[0.0] * self.dim for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                bi, bj = self.bodies[i], self.bodies[j]
                d = [bj.pos[k] - bi.pos[k] for k in range(self.dim)]
                r = math.sqrt(sum(x * x for x in d))
                r_eff = max(r, self.floor)
                f = G_NEWTON * bi.mass * bj.mass / r_eff ** 2
                unit = [x / r_eff for x in d] if r > 0 else [0.0] * self.dim
                for k in range(self.dim):
                    acc[i][k] += f * unit[k] / bi.mass
                    acc[j][k] -= f * unit[k] / bj.mass
        return acc

    def energy(self) -> float:
        ke = sum(0.5 * b.mass * sum(v * v for v in b.vel) for b in self.bodies)
        pe = 0.0
        n = len(self.bodies)
        for i in range(n):
            for j in range(i + 1, n):
                bi, bj = self.bodies[i], self.bodies[j]
                r = math.sqrt(sum((bj.pos[k] - bi.pos[k]) ** 2
                                  for k in range(self.dim)))
                pe -= G_NEWTON * bi.mass * bj.mass / max(r, self.floor)
        return ke + pe

    def step(self, dt: float) -> None:
        acc = self._accelerations()
        for i, b in enumerate(self.bodies):
            for k in range(self.dim):
                b.pos[k] += b.vel[k] * dt + 0.5 * acc[i][k] * dt * dt
        new_acc = self._accelerations()
        for i, b in enumerate(self.bodies):
            for k in range(self.dim):
                b.vel[k] += 0.5 * (acc[i][k] + new_acc[i][k]) * dt

    def run(self, steps: int, dt: float) -> Dict[str, Any]:
        e0 = self.energy()
        worst = 0.0
        for _ in range(steps):
            self.step(dt)
            e = self.energy()
            if e0 != 0:
                worst = max(worst, abs((e - e0) / e0))
        e1 = self.energy()
        return {
            "steps": steps, "dt": dt,
            "energy_initial": e0, "energy_final": e1,
            "relative_drift_final": abs((e1 - e0) / e0) if e0 else 0.0,
            "relative_drift_max": worst,
            "raised_exception": False,
        }


# ==========================================================================
# MODULE 5: Value physics & the Universal Price Tensor
# ==========================================================================
class ValuePhysicsTensor:
    """Universal Price Equation, coercion factor, WEST tokens, DQ."""

    @staticmethod
    def v_rel(u_a: float, u_b: float, cob: float = COB_UNIT_J) -> float:
        """v_rel = |U_A - U_B| / (max(U_A, U_B) + 1_inf_U)  -- Paper 8 s5.1."""
        return abs(u_a - u_b) / (max(u_a, u_b) + cob)

    @staticmethod
    def gamma(v_rel: float) -> float:
        """Lorentz coercion factor. v_rel >= 1 is unreachable by construction."""
        if v_rel >= 1.0:
            raise ValueError(f"v_rel={v_rel} >= 1: coercion factor undefined")
        return 1.0 / math.sqrt(1.0 - v_rel ** 2)

    @staticmethod
    def universal_price(m1: float, m2: float, s: float, u: float,
                        r_n: float, r_a: float,
                        u_a: float, u_b: float,
                        p_e: float = 0.0, p_b: float = 0.0) -> Dict[str, float]:
        """P = m1 m2 gamma(v_rel) [ S U / (R_n (1 - R_a)) ] + P_e + P_b"""
        if r_n == 0:
            raise ValueError("R_n = 0: reality tensor denominator ungrounded")
        if math.isclose(r_a, 1.0):
            raise ValueError("R_a = 1: total abstraction, denominator collapses")
        v = ValuePhysicsTensor.v_rel(u_a, u_b)
        g = ValuePhysicsTensor.gamma(v)
        reality_tensor = (s * u) / (r_n * (1.0 - r_a))
        p_m = m1 * m2 * g * reality_tensor
        return {
            "v_rel": v, "gamma": g, "reality_tensor": reality_tensor,
            "P_m": p_m, "P_e": p_e, "P_b": p_b, "P_total": p_m + p_e + p_b,
        }

    @staticmethod
    def west_tokens(samples: Sequence[Tuple[float, float, float, float]],
                    dt: float) -> float:
        """
        WEST = int_0^T s(t) e(t) [1 + d(t)] [1 + c(t)] dt, by trapezoid.
        samples: (skill, exertion, danger, consequence) per timestep.
        """
        if not samples:
            return 0.0
        vals = [s * e * (1 + d) * (1 + c) for s, e, d, c in samples]
        total = 0.0
        for i in range(len(vals) - 1):
            total += 0.5 * (vals[i] + vals[i + 1]) * dt
        return total

    @staticmethod
    def distortion_quotient(price_shares: Sequence[float],
                            west_shares: Sequence[float]) -> List[float]:
        """DQ = %share of nominal price / %share of WEST difficulty tokens."""
        pt, wt = sum(price_shares), sum(west_shares)
        if pt == 0 or wt == 0:
            raise ValueError("price or WEST totals are zero; DQ undefined")
        out = []
        for p, w in zip(price_shares, west_shares):
            ws = w / wt
            out.append(float("inf") if ws == 0 else (p / pt) / ws)
        return out


# ==========================================================================
# MODULE 6: Benchmark suite (Paper 8 s6) & CLI
# ==========================================================================
def _res(name: str, expected: str, got: str,
         ok: Optional[bool], note: str = "") -> Dict[str, Any]:
    return {"name": name, "expected": expected, "got": got, "ok": ok, "note": note}


def run_benchmarks() -> List[Dict[str, Any]]:
    """Reproduce the five rows of Paper 8's Table s6, honestly scored."""
    out: List[Dict[str, Any]] = []

    # 1. Holographic superposition
    c1 = ChiTensor(receptivity=0.5, result_mag=1.0)
    c2 = ChiTensor(receptivity=-0.5, result_mag=2.0)
    comb = c1.combine(c2)
    ok = (math.isclose(comb.receptivity, 0.0, abs_tol=1e-12)
          and math.isclose(comb.result_mag, 3.0))
    out.append(_res(
        "1. Holographic superposition", "rec=0.00, mag=3.00",
        f"rec={comb.receptivity:.2f}, mag={comb.result_mag:.2f}", ok,
        "Paper states only the two receptivities; magnitudes 1.0/2.0 inferred as "
        "the only simple pair summing to the quoted 3.00."))

    # 2. Propagation operator
    raw = RealityNumber(base=0, n=1, fractions=[3, 0, 0])
    canon = raw.canonicalise()
    prop = raw.propagate()
    ok2 = (math.isclose(float(canon.standard), 1.3)
           and canon.variable_name == "[0_1.3]")
    out.append(_res(
        "2. Propagation operator (as tabulated)", "[0_1.3] = 1.30000000",
        f"{canon.variable_name} = {float(canon.standard):.8f}", ok2))

    ok2b = prop.standard == raw.standard and prop.inf.total == 1
    out.append(_res(
        "2b. Propagation operator (as DEFINED in s2.2)",
        "standard part conserved exactly; one 1_inf materialised",
        f"{prop.variable_name} = {float(prop.standard):.8f} + {prop.inf} "
        f"(exact conservation: {prop.standard == raw.standard})", ok2b,
        "s2.2 defines P as cascade-into-nines-plus-1_inf. The tabulated row shows "
        "plain zero-stripping, which discards the residue rather than booking it. "
        "Both conserve the standard part; only one does what s2.2 says P is for."))

    # 3. Central collision singularity
    f = regularised_force(1.0, 1.0, 0.0)
    ok3 = math.isclose(f, 2.555e59, rel_tol=1e-3)
    out.append(_res("3. Central collision singularity", "F_max = 2.555e59 N",
                    f"F_max = {f:.4e} N", ok3))

    # 4. Black hole core curvature
    k = kretschmann(1.989e31, 0.0)
    ok4 = math.isclose(k, 5.875e218, rel_tol=1e-3)
    out.append(_res("4. Black hole core curvature", "K_max = 5.875e218 m^-4",
                    f"K_max = {k:.4e} m^-4", ok4))

    # 5. Coercive elasticity collapse
    v = ValuePhysicsTensor.v_rel(0.95, 0.10)
    g = ValuePhysicsTensor.gamma(v)
    ok5 = math.isclose(g, 2.24, abs_tol=5e-3)
    out.append(_res("5a. Coercive elasticity collapse (gamma)", "gamma = 2.24",
                    f"gamma = {g:.4f} (v_rel = {v:.6f})", ok5))
    out.append(_res(
        "5b. Coercive elasticity collapse (price)", "P = $7.46", "not computable",
        None,
        "UNDERSPECIFIED: P = m1 m2 gamma [S U / (R_n(1-R_a))] + P_e + P_b needs "
        "eight inputs. The table supplies only U_A and U_B, so $7.46 can be "
        "neither reproduced nor falsified from the paper as written. It is "
        "however plausible: m1=m2=1, S=2.5, U=1, R_n=1, R_a=0, P_e=1.00, "
        "P_b=0.85 yields $7.45. The figure looks derived, not invented -- the "
        "paper just never records the inputs."))

    # 6-9: claims made in the abstract that the table never tests.

    # 6a. Integrator sanity: two-body circular orbit, ~2 periods.
    m_orb, d_orb = 1.0e10, 1.0
    v_orb = math.sqrt(G_NEWTON * m_orb / (2 * d_orb))
    period = 2 * math.pi * (d_orb / 2) / v_orb
    sim = NBodySimulation([Body(m_orb, [-d_orb / 2, 0.0], [0.0, -v_orb]),
                           Body(m_orb, [d_orb / 2, 0.0], [0.0, v_orb])])
    r_orb = sim.run(steps=int(2 * period / 1e-3), dt=1e-3)
    ok6a = r_orb["relative_drift_max"] < 1e-9
    out.append(_res(
        "6a. Energy conservation - bound orbit", "conserved",
        f"max relative drift = {r_orb['relative_drift_max']:.3e} over "
        f"~2 orbits", ok6a,
        "The integrator itself is sound. Establishes the baseline for 6b."))

    # 6b. The case the corpus claims as its win: head-on collapse.
    drifts = []
    for dt in (1e-3, 1e-4, 1e-5):
        s = NBodySimulation([Body(1.0e10, [0.0, 0.0], [0.0, 0.0]),
                             Body(1.0e10, [1.0, 0.0], [0.0, 0.0])])
        drifts.append(s.run(int(1.0 / dt), dt)["relative_drift_max"])
    diverges = drifts[-1] > drifts[0]
    out.append(_res(
        "6b. 'exact energy conservation' - head-on collapse",
        "exact => drift 0",
        "max relative drift = " + ", ".join(
            f"{d:.2e} (dt={dt:g})" for d, dt in zip(drifts, (1e-3, 1e-4, 1e-5)))
        + (" - GROWS as dt shrinks" if diverges else ""),
        not diverges,
        "No exception is raised, so the singularity is removed as claimed. But "
        "the error grows as dt shrinks, which is divergence, not discretisation "
        "error. 'Exact energy conservation' does not hold for the collision case."))

    # 7. Where does the failure begin, relative to where the floor sits?
    s = NBodySimulation([Body(1.0e10, [0.0, 0.0], [0.0, 0.0]),
                         Body(1.0e10, [1.0, 0.0], [0.0, 0.0])])
    e0 = s.energy()
    r_fail = None
    for _ in range(10000):
        s.step(1e-4)
        sep = abs(s.bodies[1].pos[0] - s.bodies[0].pos[0])
        if abs((s.energy() - e0) / e0) > 1e-6:
            r_fail = sep
            break
    if r_fail:
        decades = math.log10(r_fail / PLANCK_LENGTH)
        out.append(_res(
            "7. Does the Planck floor reach the failure?",
            "floor at l_P regularises the collision",
            f"drift exceeds 1e-6 at r = {r_fail:.3e} m, which is {decades:.1f} "
            f"decades ABOVE the floor ({PLANCK_LENGTH:.3e} m)",
            False,
            "The floor never activates: numerical breakdown begins ~34 decades "
            "before any trajectory reaches l_P. A distance floor cannot be what "
            "rescues this case. KS and Sundman regularise by reparametrising "
            "TIME (ds = dt/r), a different mechanism, so the 'IRM vs Sundman "
            "and KS' superiority claim is not supported by this scheme."))

    # 8. Is F_reg conservative?
    m = 1.0
    def f_reg(rr: float) -> float:
        return G_NEWTON * m * m / max(rr, PLANCK_LENGTH) ** 2

    def v_reg(rr: float) -> float:
        return -G_NEWTON * m * m / max(rr, PLANCK_LENGTH)

    mismatch = []
    for rr in (1.0, PLANCK_LENGTH * 10, PLANCK_LENGTH * 0.5):
        h = rr * 1e-6
        num = abs((v_reg(rr + h) - v_reg(rr - h)) / (2 * h))
        mismatch.append((rr, f_reg(rr), num))
    inside = mismatch[-1]
    ok8 = math.isclose(inside[1], inside[2], rel_tol=1e-3)
    out.append(_res(
        "8. Is F_reg the gradient of V_reg?", "yes (required for conservation)",
        f"at r = {inside[0]:.3e} m (inside floor): F_reg = {inside[1]:.3e} N "
        f"but |dV_reg/dr| = {inside[2]:.3e} N", ok8,
        "Outside the floor they agree exactly. Inside, F_reg is pinned at F_max "
        "while V_reg is flat, so the field is non-conservative there by "
        "construction. Energy conservation below l_P is not merely inexact, it "
        "is impossible under this scheme."))

    def phi(x: Sequence[float]) -> float:
        return math.sin(3 * x[0]) * math.cos(2 * x[1]) + 0.3 * x[0] ** 2

    bop = BoundaryOperator(phi, dim=2)
    grid = [[i * 0.1, j * 0.1] for i in range(-8, 9) for j in range(-8, 9)]
    gmax = max(math.sqrt(sum(g * g for g in bop.grad(p))) for p in grid)
    sample = grid[::13]
    lip = bop.estimate_lipschitz(sample, gmax)
    out.append(_res(
        "9. Boundary operator Lipschitz continuity",
        "Lipschitz-continuous (Paper 7)",
        f"empirical constant L ~ {lip:.4f} over {len(sample)} samples",
        math.isfinite(lip),
        "Finite L is consistent with the claim on this test field. Evidence, "
        "not proof."))

    return out


def _wrap(text: str, width: int) -> List[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    if cur:
        lines.append(cur)
    return lines


def _print_benchmarks(results: Sequence[Dict[str, Any]]) -> int:
    width = 78
    print("=" * width)
    print("IRM ENGINE - BENCHMARKS (Formal Paper 8, Table s6 + abstract claims)")
    print("=" * width)
    passed = failed = unresolved = 0
    for r in results:
        if r["ok"] is None:
            tag = "UNDERSPEC"
            unresolved += 1
        elif r["ok"]:
            tag = "PASS"
            passed += 1
        else:
            tag = "FAIL"
            failed += 1
        print(f"\n[{tag:^9}] {r['name']}")
        print(f"            paper : {r['expected']}")
        print(f"            engine: {r['got']}")
        if r["note"]:
            for i, line in enumerate(_wrap(r["note"], width - 22)):
                label = "note  : " if i == 0 else "        "
                print(f"            {label}{line}")
    print("\n" + "=" * width)
    print(f"{passed} pass / {failed} fail / {unresolved} underspecified")
    print("=" * width)
    return 1 if failed else 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="irm_engine",
        description="Infinitesimal Reality Math computational engine")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("test", help="run the Paper 8 benchmark suite")

    pn = sub.add_parser("parse-number",
                        help="parse and evaluate a [base_n.d.e.f...] expression")
    pn.add_argument("expr")
    pn.add_argument("--propagate", action="store_true",
                    help="apply the s2.2 Propagation Operator instead of "
                         "plain canonicalisation")

    up = sub.add_parser("evaluate-upe", help="evaluate the Universal Price Equation")
    for name, default in (("--m1", 1.0), ("--m2", 1.0), ("--S", 1.0), ("--U", 1.0),
                          ("--Rn", 1.0), ("--Ra", 0.0), ("--Pe", 0.0), ("--Pb", 0.0)):
        up.add_argument(name, type=float, default=default)
    up.add_argument("--UA", type=float, required=True)
    up.add_argument("--UB", type=float, required=True)

    sc = sub.add_parser("simulate-chain",
                        help="simulate a declared relative chain / N-body collapse")
    sc.add_argument("--m1", type=float, default=1.0)
    sc.add_argument("--m2", type=float, default=1.0)
    sc.add_argument("--separation", type=float, default=1.0)
    sc.add_argument("--cells", type=int, default=8)
    sc.add_argument("--steps", type=int, default=1000)
    sc.add_argument("--dt", type=float, default=1e-3)

    a = p.parse_args(argv)

    if a.cmd == "test":
        return _print_benchmarks(run_benchmarks())

    if a.cmd == "parse-number":
        rn = RealityNumber.from_string(a.expr)
        out = rn.propagate() if a.propagate else rn.canonicalise()
        print(f"input         : {a.expr}")
        print(f"parsed        : {rn.variable_name}")
        print(f"operator      : "
              f"{'P (s2.2 cascade)' if a.propagate else 'canonicalise (strip)'}")
        print(f"result        : {out.variable_name}")
        print(f"exact value   : {out.standard} = {float(out.standard):.12f}")
        print(f"infinitesimals: {out.inf}")
        print(f"conserved     : {out.standard == rn.standard}")
        anchor = LatticeManifold.classify_evaluator(float(out.standard))
        print(f"lattice       : {anchor['name']} - {anchor['label']}")
        return 0

    if a.cmd == "evaluate-upe":
        r = ValuePhysicsTensor.universal_price(a.m1, a.m2, a.S, a.U, a.Rn, a.Ra,
                                               a.UA, a.UB, a.Pe, a.Pb)
        for k, v in r.items():
            print(f"{k:>16}: {v:.6f}")
        return 0

    if a.cmd == "simulate-chain":
        chain = DeclaredRelativeChain(0.0, a.separation, a.cells)
        print(f"declared chain: {a.cells} cells, cell size "
              f"{chain.cell_size:.6e} m, separation {chain.separation:.6e} m")
        print(f"F_reg at contact (r=0): "
              f"{regularised_force(a.m1, a.m2, 0.0):.6e} N")
        sim = NBodySimulation([Body(a.m1, [0.0, 0.0], [0.0, 0.0]),
                               Body(a.m2, [a.separation, 0.0], [0.0, 0.0])])
        r = sim.run(a.steps, a.dt)
        for k, v in r.items():
            print(f"{k:>22}: {v}")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
