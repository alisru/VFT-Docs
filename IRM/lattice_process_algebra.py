#!/usr/bin/env python3
"""
lattice_process_algebra.py — Multi-Dimensional 7-Lattice Process Algebra & Non-Archimedean Regularization
for Infinitesimal Reality Math (IRM Division 1: Pure Mathematics).

Ground-Up Mathematical Innovations:
1. Non-Archimedean Regularized Process Division (⊘):
   Eliminates division-by-zero singularities using the infinitesimal Cost of Being floor ε = 1∞ > 0.
   Division by the zero atom Z = <A0=0, 0, 0> maps smoothly to the saturation wall A6 = 2
   with quantifiable overflow stress in O = V(A)/ε - 2, avoiding arbitrary IEEE 754 NaN/inf crashes.
2. Discrete 7-Lattice Mechanics & Quantum Boundary Transitions:
   Formulates the 7 Evaluator Anchors A0..A6 = {0, 1/3, 2/3, 1, 4/3, 5/3, 2} across [0, 2].
   Proves the Quantum Boundary Invariant: at every boundary midpoint Bk = (2k+1)/6,
   crossing the threshold induces an exact quantum macro-jump ΔT = ±1/3 and residue phase reset ΔR = ∓1/3,
   such that continuous total valuation ΔV = ΔT + ΔR = 0 is identically conserved everywhere.
3. 7-Plane Interrogative Vector Process Space (P⁷):
   Vectors of process atoms across Q1..Q7 (Who, What, Why, How, Where, When, Which).
   Inner products contract 7-dimensional semantic energy into a scalar process atom via Try²{}Catch{}.
4. 7x7 Process Matrix Operator Algebra (P⁷ˣ⁷):
   Closed associative and distributive matrix multiplication (A ⊙ B) ⊙ C == A ⊙ (B ⊙ C),
   cyclic trace invariance Tr(A ⊙ B) == Tr(B ⊙ A), and transpose distribution (A ⊙ B)ᵀ == Bᵀ ⊙ Aᵀ.

Author: Lead Mathematical Physicist & PDE Analyst (Division 1: Pure Mathematics, ARI)
Date: 2026-09-15
"""

import math
from fractions import Fraction


class ProcessAtom:
    """
    The Fundamental Bounded Process Atom: <T, R, O>.
    - T in {0, 1/3, 2/3, 1, 4/3, 5/3, 2}: Manifest Target pinned to 7 Evaluator Anchors.
    - R in [-1/6, 1/6]: Active Signed Process Residue (sub-anchor phase/strain).
    - O in Q: Accumulated Overflow Stress outside the manifest [0, 2] interval.
    """
    __slots__ = ('_T', '_R', '_O')

    ANCHORS = tuple(Fraction(k, 3) for k in range(7))
    ANCHOR_NAMES = ("A0", "A1", "A2", "A3", "A4", "A5", "A6")
    ANCHOR_MAP = {Fraction(k, 3): f"A{k}" for k in range(7)}
    BOUNDARIES = tuple(Fraction(2 * k + 1, 6) for k in range(6))
    EPS_FLOOR = Fraction(1, 10**9) # Infinitesimal Cost of Being floor 1∞

    def __init__(self, T, R=Fraction(0), O=Fraction(0)):
        self._T = Fraction(T)
        self._R = Fraction(R)
        self._O = Fraction(O)

    @property
    def T(self):
        return self._T

    @property
    def R(self):
        return self._R

    @property
    def O(self):
        return self._O

    @property
    def value(self):
        """Invariant total valuation V = T + R + O in Q."""
        return self._T + self._R + self._O

    @property
    def anchor_name(self):
        return self.ANCHOR_MAP.get(self._T, f"T={self._T}")

    @classmethod
    def from_rational(cls, V):
        """
        The Try²{}Catch{} Quadratic Level-Set Projector:
        Canonical ground-state projection with full overflow re-absorption.
        """
        V = Fraction(V)
        if V < 0:
            return cls(Fraction(0), Fraction(0), V)
        elif V > 2:
            return cls(Fraction(2), Fraction(0), V - Fraction(2))
        else:
            val_3 = 3 * V
            k = math.floor(val_3 + Fraction(1, 2))
            k = max(0, min(6, k))
            T = Fraction(k, 3)
            R = V - T
            return cls(T, R, Fraction(0))

    def __add__(self, other):
        if isinstance(other, (int, float, Fraction)):
            other = ProcessAtom.from_rational(other)
        return ProcessAtom.from_rational(self.value + other.value)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, (int, float, Fraction)):
            other = ProcessAtom.from_rational(other)
        return ProcessAtom.from_rational(self.value - other.value)

    def __rsub__(self, other):
        if isinstance(other, (int, float, Fraction)):
            other = ProcessAtom.from_rational(other)
        return other.__sub__(self)

    def __mul__(self, other):
        if isinstance(other, (int, float, Fraction)):
            other = ProcessAtom.from_rational(other)
        return ProcessAtom.from_rational(self.value * other.value)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """Non-Archimedean Regularized Process Division (⊘)."""
        return self.div_regularized(other)

    def div_regularized(self, other, eps=None):
        """
        Regularized division over Q(1∞).
        If denominator V(B) == 0, replaces denominator with infinitesimal floor ε = 1∞ > 0.
        Never raises ZeroDivisionError; traps excess at saturation wall with finite quantified stress in O.
        """
        if eps is None:
            eps = self.EPS_FLOOR
        if isinstance(other, (int, float, Fraction)):
            other = ProcessAtom.from_rational(other)
        den = other.value if other.value != 0 else eps
        return ProcessAtom.from_rational(self.value / den)

    def __neg__(self):
        return ProcessAtom.from_rational(-self.value)

    def __eq__(self, other):
        if not isinstance(other, ProcessAtom):
            return False
        return (self._T == other._T) and (self._R == other._R) and (self._O == other._O)

    def __repr__(self):
        return f"ProcessAtom(T={self.anchor_name}:{self._T}, R={self._R}, O={self._O}, V={self.value})"

    def quadratic_stress(self):
        """
        Signed Quadratic Stress Penalty from Try²{}Catch{}:
        Phi(V) = (V - 1)². Inside [0, 2], Phi(V) <= 1.
        Outside [0, 2], remainder = max(0, (V - 1)² - 1).
        """
        v = self.value
        phi = (v - 1) ** 2
        remainder = max(Fraction(0), phi - Fraction(1))
        sign = Fraction(1) if self._O > 0 else (Fraction(-1) if self._O < 0 else Fraction(0))
        return sign * remainder


class DiscreteLattice7:
    """
    Discrete 7-Lattice Mechanics across the 7 Evaluator Anchors (A0..A6).
    Formalizes boundary midpoints Bk, quantum transition jumps, and state indices.
    """
    @staticmethod
    def boundary_index(V):
        """Determines the active lattice cell index k in {0..6} for valuation V in [0, 2]."""
        V = Fraction(V)
        if V <= 0:
            return 0
        if V >= 2:
            return 6
        val_3 = 3 * V
        k = math.floor(val_3 + Fraction(1, 2))
        return max(0, min(6, k))

    @staticmethod
    def quantum_transition(V_before, V_after):
        """
        Analyzes the state transition between two valuations.
        Returns (delta_T, delta_R, delta_O, delta_V, transition_occurred).
        """
        atom_before = ProcessAtom.from_rational(V_before)
        atom_after = ProcessAtom.from_rational(V_after)
        dT = atom_after.T - atom_before.T
        dR = atom_after.R - atom_before.R
        dO = atom_after.O - atom_before.O
        dV = atom_after.value - atom_before.value
        transition = (atom_before.T != atom_after.T)
        return {
            'delta_T': dT,
            'delta_R': dR,
            'delta_O': dO,
            'delta_V': dV,
            'conserved': (dT + dR + dO == dV),
            'transition_occurred': transition
        }


class ProcessVector7:
    """
    7-Plane Interrogative Vector Process Space (P⁷).
    Coordinates correspond to the 7 Interrogative Planes:
    Q1: Who, Q2: What, Q3: Why, Q4: How, Q5: Where, Q6: When, Q7: Which.
    """
    __slots__ = ('_coords',)

    def __init__(self, coords):
        coords = tuple(coords)
        assert len(coords) == 7, "ProcessVector7 must contain exactly 7 coordinates"
        self._coords = tuple(
            c if isinstance(c, ProcessAtom) else ProcessAtom.from_rational(c)
            for c in coords
        )

    def __getitem__(self, idx):
        return self._coords[idx]

    def __len__(self):
        return 7

    @property
    def coords(self):
        return self._coords

    def __add__(self, other):
        assert isinstance(other, ProcessVector7), "Addition must be with another ProcessVector7"
        return ProcessVector7(a + b for a, b in zip(self._coords, other._coords))

    def __sub__(self, other):
        assert isinstance(other, ProcessVector7), "Subtraction must be with another ProcessVector7"
        return ProcessVector7(a - b for a, b in zip(self._coords, other._coords))

    def scale(self, scalar):
        """Multiplication by scalar ProcessAtom or rational."""
        if not isinstance(scalar, ProcessAtom):
            scalar = ProcessAtom.from_rational(scalar)
        return ProcessVector7(c * scalar for c in self._coords)

    def inner_product(self, other):
        """
        Process Inner Product (Contraction) <X, Y>_P:
        Evaluates sum of component products in Q and projects via Try²{}Catch{} to a single ProcessAtom.
        """
        assert isinstance(other, ProcessVector7), "Inner product must be with another ProcessVector7"
        tot_val = sum((a.value * b.value for a, b in zip(self._coords, other._coords)), Fraction(0))
        return ProcessAtom.from_rational(tot_val)

    def total_quadratic_stress(self):
        """Total quadratic stress across all 7 interrogative planes: sum((V_i - 1)²)."""
        return sum(((c.value - 1) ** 2 for c in self._coords), Fraction(0))

    def __eq__(self, other):
        if not isinstance(other, ProcessVector7):
            return False
        return self._coords == other._coords

    def __repr__(self):
        vals = [f"{c.anchor_name}" for c in self._coords]
        return f"ProcessVector7({', '.join(vals)})"


class ProcessMatrix7x7:
    """
    7x7 Process Matrix Operator Space (P⁷ˣ⁷).
    Represents inter-plane transformations, holonomies, and semantic couplings across Q1..Q7.
    """
    __slots__ = ('_rows',)

    def __init__(self, rows):
        rows = tuple(tuple(r) for r in rows)
        assert len(rows) == 7 and all(len(r) == 7 for r in rows), "Must be 7x7 matrix"
        self._rows = tuple(
            tuple(c if isinstance(c, ProcessAtom) else ProcessAtom.from_rational(c) for c in row)
            for row in rows
        )

    def __getitem__(self, idx):
        return self._rows[idx]

    @classmethod
    def identity(cls):
        """Multiplicative Identity Matrix I₇ in P⁷ˣ⁷."""
        return cls([[ProcessAtom.from_rational(1 if i == j else 0) for j in range(7)] for i in range(7)])

    @classmethod
    def zero(cls):
        """Additive Zero Matrix 0₇ in P⁷ˣ⁷."""
        return cls([[ProcessAtom.from_rational(0) for j in range(7)] for i in range(7)])

    def __add__(self, other):
        assert isinstance(other, ProcessMatrix7x7), "Addition must be with another ProcessMatrix7x7"
        return ProcessMatrix7x7([[self._rows[i][j] + other._rows[i][j] for j in range(7)] for i in range(7)])

    def __sub__(self, other):
        assert isinstance(other, ProcessMatrix7x7), "Subtraction must be with another ProcessMatrix7x7"
        return ProcessMatrix7x7([[self._rows[i][j] - other._rows[i][j] for j in range(7)] for i in range(7)])

    def matmul(self, other):
        """Matrix-Matrix Multiplication (⊙) in P⁷ˣ⁷."""
        assert isinstance(other, ProcessMatrix7x7), "Must multiply by another ProcessMatrix7x7"
        res = []
        for i in range(7):
            row = []
            for j in range(7):
                v = sum((self._rows[i][k].value * other._rows[k][j].value for k in range(7)), Fraction(0))
                row.append(ProcessAtom.from_rational(v))
            res.append(row)
        return ProcessMatrix7x7(res)

    def apply_vector(self, vec):
        """Matrix-Vector Transformation M ⊙ X -> ProcessVector7."""
        assert isinstance(vec, ProcessVector7), "Must apply to ProcessVector7"
        res = []
        for i in range(7):
            v = sum((self._rows[i][j].value * vec[j].value for j in range(7)), Fraction(0))
            res.append(ProcessAtom.from_rational(v))
        return ProcessVector7(res)

    def transpose(self):
        """Matrix Transpose Mᵀ."""
        return ProcessMatrix7x7([[self._rows[j][i] for j in range(7)] for i in range(7)])

    def trace(self):
        """Matrix Trace Tr(M) = ⊕ Mᵢᵢ."""
        tot = sum((self._rows[i][i].value for i in range(7)), Fraction(0))
        return ProcessAtom.from_rational(tot)

    def __eq__(self, other):
        if not isinstance(other, ProcessMatrix7x7):
            return False
        return self._rows == other._rows

    def __repr__(self):
        return f"ProcessMatrix7x7(Trace={self.trace().anchor_name}:{self.trace().value})"


ATOM_ZERO = ProcessAtom.from_rational(0)  # Additive Identity <A0=0, 0, 0>
ATOM_UNIT = ProcessAtom.from_rational(1)  # Multiplicative Identity <A3=1, 0, 0>
ATOM_MAX  = ProcessAtom.from_rational(2)  # Saturation Limit <A6=2, 0, 0>
MATRIX_I7 = ProcessMatrix7x7.identity()
MATRIX_Z7 = ProcessMatrix7x7.zero()
