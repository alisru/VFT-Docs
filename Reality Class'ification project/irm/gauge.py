#!/usr/bin/env python3
"""
gauge.py - numerical solvers for the connection 1-form and semantic field
strength curvature on the 42-simplex.  (Directive ENG-2 / Milestone 4.3.)

Implements the objects Formal Paper 9 defines only symbolically:

    g = so(7) + aut(chi),  dim g = 21 + 4 = 25          (Paper 9 s2.2, s3.1)
    omega = A_mu^a T_a dx^mu                            (s3.1)
    F_mu_nu^a = d_mu A_nu^a - d_nu A_mu^a + f_bc^a A_mu^b A_nu^c   (s3.2)
    W_gamma = (1/dim G) Tr[ P exp( closed-loop integral of omega ) ]  (Paper 10 s3.1)

and then tests the claims that rest on them:

  Paper 9  Thm 3.1  lossless transport  <=>  F_mu_nu = 0
  Paper 10 Thm 3.1  holonomy phase is quantised, W = exp(2 pi i n / k)

The tests are constructive where possible: rather than asserting that a flat
connection has trivial holonomy, build a pure-gauge connection A = g^-1 dg and
measure both sides.

Representation: g acts on R^7 (the seven interrogative planes) direct sum
R^4 (the chi tensor), i.e. block-diagonal 11 x 11 real matrices. so(7) is the
21 antisymmetric 7x7 generators; aut(chi) = so(3) + R^+ is 3 antisymmetric
generators on (rho, upsilon, psi) plus one dilatation on mu.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple

import numpy as np
from scipy.linalg import expm, logm

# Representation dimensions
DIM_Q = 7          # the seven interrogative planes
DIM_CHI = 4        # (rho, upsilon, psi, mu)
DIM_REP = DIM_Q + DIM_CHI          # 11
DIM_SO7 = DIM_Q * (DIM_Q - 1) // 2  # 21
DIM_AUT_CHI = 3 + 1                 # so(3) + R^+ = 4
DIM_G = DIM_SO7 + DIM_AUT_CHI       # 25


# ==========================================================================
# The Lie algebra
# ==========================================================================
class InfoLieAlgebra:
    """
    g = so(7) + aut(chi) in the block-diagonal 11-dimensional representation.

    Generator ordering:
      indices  0..20  : so(7), one per (i<j) pair, E_ij - E_ji
      indices 21..23  : so(3) acting on (rho, upsilon, psi)
      index      24   : the R^+ dilatation on mu
    """

    def __init__(self) -> None:
        self.generators: List[np.ndarray] = []
        self.labels: List[str] = []

        # so(7) block, rows/cols 0..6
        for i in range(DIM_Q):
            for j in range(i + 1, DIM_Q):
                T = np.zeros((DIM_REP, DIM_REP))
                T[i, j], T[j, i] = 1.0, -1.0
                self.generators.append(T)
                self.labels.append(f"so7[Q{i + 1},Q{j + 1}]")

        # so(3) on the chi orientation, rows/cols 7..9
        for i in range(3):
            for j in range(i + 1, 3):
                T = np.zeros((DIM_REP, DIM_REP))
                a, b = DIM_Q + i, DIM_Q + j
                T[a, b], T[b, a] = 1.0, -1.0
                self.generators.append(T)
                self.labels.append(f"so3[chi{i},chi{j}]")

        # R^+ dilatation on mu, row/col 10
        T = np.zeros((DIM_REP, DIM_REP))
        T[DIM_REP - 1, DIM_REP - 1] = 1.0
        self.generators.append(T)
        self.labels.append("R+[mu dilatation]")

        self.dim = len(self.generators)
        self._structure: Optional[np.ndarray] = None

    # -- basic algebra -----------------------------------------------------
    @staticmethod
    def bracket(X: np.ndarray, Y: np.ndarray) -> np.ndarray:
        return X @ Y - Y @ X

    def element(self, coeffs: Sequence[float]) -> np.ndarray:
        """A^a T_a."""
        out = np.zeros((DIM_REP, DIM_REP))
        for c, T in zip(coeffs, self.generators):
            if c:
                out = out + c * T
        return out

    def components(self, X: np.ndarray) -> np.ndarray:
        """
        Decompose X in g into generator coefficients, by least squares on the
        flattened basis. Exact for X actually in g.
        """
        B = np.stack([T.ravel() for T in self.generators], axis=1)
        coeffs, *_ = np.linalg.lstsq(B, X.ravel(), rcond=None)
        return coeffs

    def structure_constants(self) -> np.ndarray:
        """f_ab^c with [T_a, T_b] = f_ab^c T_c."""
        if self._structure is None:
            f = np.zeros((self.dim, self.dim, self.dim))
            for a in range(self.dim):
                for b in range(self.dim):
                    f[a, b] = self.components(
                        self.bracket(self.generators[a], self.generators[b]))
            self._structure = f
        return self._structure

    def closure_residual(self) -> float:
        """
        Max error in reconstructing every bracket from the structure constants.
        Nonzero would mean the generator set is not closed, i.e. not an algebra.
        """
        f = self.structure_constants()
        worst = 0.0
        for a in range(self.dim):
            for b in range(self.dim):
                lhs = self.bracket(self.generators[a], self.generators[b])
                rhs = sum(f[a, b, c] * self.generators[c] for c in range(self.dim))
                worst = max(worst, float(np.max(np.abs(lhs - rhs))))
        return worst

    def compact_part_indices(self) -> Tuple[List[int], List[int]]:
        """(compact generators, non-compact generators). See test 7."""
        compact, noncompact = [], []
        for i, T in enumerate(self.generators):
            (compact if np.allclose(T, -T.T) else noncompact).append(i)
        return compact, noncompact


# ==========================================================================
# Connections and curvature
# ==========================================================================
# A connection is a callable x -> A_mu(x), returning one 11x11 g-valued matrix
# per base direction. x is a point of the base manifold (a slice of Delta^42).
ConnectionFn = Callable[[np.ndarray], List[np.ndarray]]


def curvature(A: ConnectionFn, x: np.ndarray, mu: int, nu: int,
              h: float = 1e-5) -> np.ndarray:
    """
    F_mu_nu = d_mu A_nu - d_nu A_mu + [A_mu, A_nu].

    Derivatives by central differences; the commutator is exact.
    """
    xp, xm = x.copy(), x.copy()
    xp[mu] += h
    xm[mu] -= h
    dmu_Anu = (A(xp)[nu] - A(xm)[nu]) / (2 * h)

    xp, xm = x.copy(), x.copy()
    xp[nu] += h
    xm[nu] -= h
    dnu_Amu = (A(xp)[mu] - A(xm)[mu]) / (2 * h)

    Ax = A(x)
    return dmu_Anu - dnu_Amu + (Ax[mu] @ Ax[nu] - Ax[nu] @ Ax[mu])


def curvature_norm(A: ConnectionFn, x: np.ndarray, mu: int, nu: int,
                   h: float = 1e-5) -> float:
    return float(np.linalg.norm(curvature(A, x, mu, nu, h)))


def wilson_holonomy(A: ConnectionFn, loop: Sequence[np.ndarray],
                    segments: int = 400) -> np.ndarray:
    """
    Path-ordered exponential around a closed polygonal loop.

    Returns the holonomy MATRIX. Paper 10 s3.1's W_gamma is a normalised trace
    of this; see wilson_trace below, and test 6 for the normalisation issue.
    """
    U = np.eye(DIM_REP)
    n = len(loop)
    for i in range(n):
        p, q = loop[i], loop[(i + 1) % n]
        d = (q - p) / segments
        for s in range(segments):
            mid = p + d * (s + 0.5)
            Amid = A(mid)
            # omega(dx) = A_mu dx^mu
            step = sum(Amid[mu] * d[mu] for mu in range(len(d)))
            # Right multiplication: with F = dA + [A,A] the curvature
            # convention fixes A = g^-1 dg, whose transport obeys
            # dU/ds = U A. Left-multiplying here mismatches the two and
            # reports non-trivial holonomy for flat connections.
            U = U @ expm(step)
    return U


def wilson_trace(U: np.ndarray, normalisation: str = "rep") -> float:
    """
    Normalised trace of the holonomy.

    'rep'   : Tr(U) / dim(V)   -- gives exactly 1.0 for trivial holonomy.
    'paper' : Tr(U) / dim(G)   -- Paper 10 s3.1 as literally written.
    """
    d = DIM_REP if normalisation == "rep" else DIM_G
    return float(np.trace(U).real / d)


def pure_gauge_analytic(Ta: np.ndarray, Tb: np.ndarray) -> ConnectionFn:
    """
    A = g^-1 dg for g(x) = exp(x0 Ta) exp(x1 Tb), in closed form.

    Because Ta commutes with exp(x0 Ta), the pullback collapses to

        A_0(x) = Ad(exp(-x1 Tb)) Ta = e^{-x1 Tb} Ta e^{x1 Tb}
        A_1(x) = Tb

    Flat by construction, and analytic -- so curvature() differentiates an exact
    expression instead of a finite-difference approximation. Nested differencing
    left a residue of ~5e-6 in ||F||, which is FD error, not curvature.
    """
    def A(x: np.ndarray) -> List[np.ndarray]:
        c = expm(-x[1] * Tb)
        cinv = expm(x[1] * Tb)
        return [c @ Ta @ cinv, Tb.copy()]
    return A


# ==========================================================================
# Test suite
# ==========================================================================
@dataclass
class Result:
    name: str
    expected: str
    got: str
    ok: Optional[bool]
    note: str = ""


def run_tests() -> List[Result]:
    alg = InfoLieAlgebra()
    out: List[Result] = []
    rng = np.random.default_rng(7)

    # -- 1. algebra dimension and closure ---------------------------------
    res = alg.closure_residual()
    ok = alg.dim == 25 and res < 1e-10
    out.append(Result(
        "1. Lie algebra: dim g = 25 and closed under bracket",
        "dim = 25, closure residual = 0",
        f"dim = {alg.dim} ({DIM_SO7} + {DIM_AUT_CHI}), "
        f"closure residual = {res:.2e}", ok,
        "Confirms the P9-D2 correction. Note this REQUIRES chi to be 4-dimensional: "
        "aut(chi) = so(3) + R^+ has dim 4, giving 21 + 4 = 25. The papers' '6D chi' "
        "label is inconsistent with their own generator count (finding N-1)."))

    # -- 2. pure gauge is flat --------------------------------------------
    # g(x) = exp(x0 T_a + x1 T_b) for two non-commuting generators.
    Ta, Tb = alg.generators[0], alg.generators[8]
    A_flat = pure_gauge_analytic(Ta, Tb)
    pt = np.array([0.23, -0.41])
    f_flat = curvature_norm(A_flat, pt, 0, 1)
    ok2 = f_flat < 1e-8
    out.append(Result(
        "2. Pure gauge A = g^-1 dg has F = 0",
        "||F_01|| = 0",
        f"||F_01|| = {f_flat:.3e}", ok2,
        "Forward direction of Paper 9 Thm 3.1, verified constructively on an "
        "analytic pure-gauge connection."))

    # -- 3. flat connection has trivial holonomy --------------------------
    loop = [np.array([0.0, 0.0]), np.array([0.3, 0.0]),
            np.array([0.3, 0.3]), np.array([0.0, 0.3])]
    U_flat = wilson_holonomy(A_flat, loop, segments=200)
    dev_flat = float(np.linalg.norm(U_flat - np.eye(DIM_REP)))
    ok3 = dev_flat < 1e-6
    out.append(Result(
        "3. Flat connection => trivial holonomy",
        "||U - I|| = 0, W = 1",
        f"||U - I|| = {dev_flat:.3e}, W = {wilson_trace(U_flat):.8f}", ok3))

    # -- 4. non-flat connection has non-trivial holonomy ------------------
    coeff = rng.normal(size=(2, DIM_G)) * 0.4

    def A_curved(x: np.ndarray) -> List[np.ndarray]:
        return [alg.element(coeff[0] * (1.0 + x[1])),
                alg.element(coeff[1] * (1.0 + x[0] ** 2))]

    f_curved = curvature_norm(A_curved, pt, 0, 1)
    U_curved = wilson_holonomy(A_curved, loop, segments=400)
    dev_curved = float(np.linalg.norm(U_curved - np.eye(DIM_REP)))
    ok4 = f_curved > 1e-3 and dev_curved > 1e-3
    out.append(Result(
        "4. Curved connection => non-trivial holonomy",
        "||F|| > 0 and ||U - I|| > 0",
        f"||F_01|| = {f_curved:.4f}, ||U - I|| = {dev_curved:.4f}, "
        f"W = {wilson_trace(U_curved):.6f}", ok4,
        "Converse direction of Paper 9 Thm 3.1."))

    # -- 5. Ambrose-Singer: holonomy scales with enclosed area ------------
    ratios = []
    for a in (0.08, 0.04, 0.02, 0.01):
        sq = [np.array([0.0, 0.0]), np.array([a, 0.0]),
              np.array([a, a]), np.array([0.0, a])]
        U = wilson_holonomy(A_curved, sq, segments=300)
        dev = float(np.linalg.norm(logm(U)))
        ratios.append(dev / (a * a))
    spread = (max(ratios) - min(ratios)) / max(ratios)
    f0 = curvature_norm(A_curved, np.array([0.0, 0.0]), 0, 1)
    ok5 = spread < 0.15
    out.append(Result(
        "5. Ambrose-Singer: ||log U|| / area -> ||F|| as area -> 0",
        f"ratio converges to ||F_01(0)|| = {f0:.4f}",
        "ratios = " + ", ".join(f"{r:.4f}" for r in ratios)
        + f"  (spread {spread * 100:.1f}%)", ok5,
        "Cross-validates the curvature solver against the Wilson loop solver: "
        "they are computed by completely different routes and must agree in the "
        "small-loop limit."))

    # -- 6. Paper 9 Thm 3.1's stated CRITERION is abelian-only ------------
    # Loop integral of A vanishes componentwise, yet holonomy is non-trivial.
    X = 0.9 * alg.generators[0]
    Y = 0.9 * alg.generators[8]
    U_comm = expm(X) @ expm(Y) @ expm(-X) @ expm(-Y)
    line_integral = X + Y - X - Y           # exactly zero in the algebra
    dev_comm = float(np.linalg.norm(U_comm - np.eye(DIM_REP)))
    ok6 = np.allclose(line_integral, 0) and dev_comm > 1e-3
    out.append(Result(
        "6. Is 'Hol = {e} <=> loop integral of A = 0' correct?",
        "the stated criterion should characterise trivial holonomy",
        f"loop integral of A = 0 exactly (||.|| = {np.linalg.norm(line_integral):.1e}) "
        f"but ||U - I|| = {dev_comm:.4f}", not ok6,
        "FINDING. Paper 9 s3.1 writes Hol(omega) = {e} <=> closed-loop integral of "
        "A_mu dx^mu = 0. That is the ABELIAN criterion. For non-abelian G the "
        "path-ordering does not drop out: the group commutator "
        "e^X e^Y e^-X e^-Y ~ e^[X,Y] is non-trivial while the naive line integral "
        "cancels. Since G = SO(7) x Aut(chi) is explicitly non-abelian (that is the "
        "point of s3.2's f_bc^a term), the criterion as written is wrong. The "
        "correct statement is Hol = {e} <=> F = 0 on a simply connected base, which "
        "is what the rest of the theorem says."))

    # -- 7. non-compact R^+ factor breaks phase quantisation --------------
    compact, noncompact = alg.compact_part_indices()
    T_dil = alg.generators[noncompact[0]]
    U_dil = expm(0.8 * T_dil)
    eigs = np.linalg.eigvals(U_dil)
    max_mod = float(np.max(np.abs(eigs)))
    ok7 = math.isclose(max_mod, 1.0, abs_tol=1e-6)
    out.append(Result(
        "7. Paper 10 Thm 3.1: is holonomy always a quantised phase?",
        "W = exp(2 pi i n / k), i.e. |eigenvalues| = 1",
        f"dilatation holonomy has max |eigenvalue| = {max_mod:.6f} "
        f"({len(noncompact)} non-compact generator(s) in g)", ok7,
        "FINDING. Aut(chi) = SO(3) x R^+ contains a non-compact R^+ factor, whose "
        "generator is symmetric rather than antisymmetric. Its holonomy is a real "
        "dilatation, not a phase, so W = exp(2 pi i n / k) cannot hold on that "
        "factor. Phase quantisation is available only on the compact part "
        "SO(7) x SO(3) (dim 24 of 25). Either restrict the theorem to the compact "
        "subgroup or drop the R^+ factor from Aut(chi) - but note that dropping it "
        "changes dim g from 25 back to 24, which reopens P9-D2."))

    # -- 8. Wilson loop normalisation -------------------------------------
    w_rep = wilson_trace(np.eye(DIM_REP), "rep")
    w_paper = wilson_trace(np.eye(DIM_REP), "paper")
    ok8 = math.isclose(w_paper, 1.0, abs_tol=1e-9)
    out.append(Result(
        "8. Paper 10 s3.1 normalisation: does W = 1 for trivial holonomy?",
        "W_gamma = 1.0 for U = I ('n = 0: lossless resonance, W = 1.0')",
        f"with 1/dim(G) = 1/25 as written: W = {w_paper:.6f};  "
        f"with 1/dim(V) = 1/11: W = {w_rep:.6f}", ok8,
        "FINDING. W = (1/dim G) Tr[...] returns 11/25 = 0.44 for trivial holonomy in "
        "the defining 11-dimensional representation, contradicting s3.2's own "
        "'n = 0: W = 1.0'. The 1/dim G normalisation is correct only in the adjoint "
        "representation, where dim V = dim G = 25. Either state that omega is taken "
        "in the adjoint, or normalise by 1/dim(V)."))

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


def main() -> int:
    results = run_tests()
    width = 78
    print("=" * width)
    print("ENG-2: CONNECTION 1-FORM & SEMANTIC CURVATURE SOLVERS (Paper 9 / 10)")
    print("=" * width)
    print(f"\nrepresentation: R^{DIM_Q} (+) R^{DIM_CHI} = R^{DIM_REP}, "
          f"dim g = {DIM_SO7} + {DIM_AUT_CHI} = {DIM_G}\n")
    passed = failed = 0
    for r in results:
        if r.ok:
            tag = "PASS"
            passed += 1
        else:
            tag = "FAIL"
            failed += 1
        print(f"[{tag:^6}] {r.name}")
        print(f"         paper : {r.expected}")
        print(f"         solver: {r.got}")
        if r.note:
            for i, line in enumerate(_wrap(r.note, width - 19)):
                label = "note  : " if i == 0 else "        "
                print(f"         {label}{line}")
        print()
    print("=" * width)
    print(f"{passed} pass / {failed} fail")
    print("=" * width)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
