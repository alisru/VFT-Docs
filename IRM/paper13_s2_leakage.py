#!/usr/bin/env python3
"""
paper13_s2_leakage.py - Engineer verification of Formal Paper 13, Theorem 2.1,
plus two arithmetic reproductions from Papers 8 and 12.

WHY THIS EXISTS
---------------
Formal Paper 13 section 2.3 states, as a THEOREM, three numbers:

    Lambda_true    <= 0.05     for "aligned representations"
    Lambda_generic >= 0.78     for "random dense rotations"
    SNR            >  15.6     "statistically decisive discriminant"

No derivation is given and no artifact computes them. The Checker pass recorded
in the PM document quotes all three as established, and the Orthodox Linker
lists Paper 13 under "Verification Pass". This is the same shape as the Formal
Paper 8 / irm_engine.py situation that created the Engineer role: published
numbers with nothing behind them.

Lambda_generic is a statement about random elements of SO(d) and the block
subgroup SO(7) x Aut(chi). That is a pure geometry question with no model in it,
so it is decidable here, by measurement.

Lambda_true is a claim about real learned representations. It is NOT decidable
here and this file does not pretend otherwise; test L-3 instead inverts the
geometry to report what perturbation size the 0.05 bound actually corresponds
to, which turns an untestable assertion into a stated precondition.

Definitions follow the paper:

    Lambda(P) = || P - Pi_G(P) ||_F / || P - I ||_F
    G         = SO(7) x Aut(chi),  Aut(chi) = SO(3) x R^+   (Paper 11 s2.1)

Pi_G is the nearest element of G in Frobenius norm. Because G is block-diagonal
in the (R^7 + R^3 + R^1) splitting, that projection separates: nearest SO(7) to
the 7x7 block, nearest SO(3) to the 3x3 block, nearest positive scalar to the
(mu, mu) entry, and zero on every off-diagonal block.

QUARANTINE NOTE (Director's instruction, 2026-08-31)
---------------------------------------------------
Tests L-1 through L-4 touch the quarantined representation-geometry strand.
They are retained because they FALSIFY a claim rather than extend one - L-2
shows Paper 13's bound fails in SO(11) - but nothing here licenses further
embedding work in the foundational papers.

My own contamination, named: the d = 768 row is a transformer hidden width. I
chose it because it is a real model's embedding dimension, which imported an
assumption about language models into an instrument that is supposed to test
the corpus's own claims. The d = 11 row is the corpus's own defining
representation and is the one that matters; 48 is semantic_connection.py's
synthetic width. Read 768 as "large d", not as an endorsement of the protocol.

Run:  python paper13_s2_leakage.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional, Tuple

import numpy as np

RNG_SEED = 13
DIM_7, DIM_3, DIM_1 = 7, 3, 1
DIM_V = DIM_7 + DIM_3 + DIM_1          # 11, the defining rep of Paper 10 s3.1


# ==========================================================================
# The subgroup and its nearest-point projection
# ==========================================================================
def nearest_special_orthogonal(M: np.ndarray) -> np.ndarray:
    """argmin over SO(n) of ||M - Q||_F, by SVD (Procrustes)."""
    U, _, Vt = np.linalg.svd(M)
    D = np.eye(M.shape[0])
    D[-1, -1] = np.linalg.det(U @ Vt)
    return U @ D @ Vt


def project_to_G(P: np.ndarray) -> np.ndarray:
    """
    Nearest element of G = SO(7) x SO(3) x R^+ embedded block-diagonally.

    Separates because the Frobenius norm is a sum over blocks and the blocks
    are independently constrained: off-diagonal blocks contribute ||P_ij||^2
    and are minimised by 0, and each diagonal block is minimised on its own
    factor.
    """
    d = P.shape[0]
    if d < DIM_V:
        raise ValueError("projection defined for d >= 11")
    Q = np.zeros_like(P)
    a, b, c = DIM_7, DIM_7 + DIM_3, DIM_7 + DIM_3 + DIM_1
    Q[:a, :a] = nearest_special_orthogonal(P[:a, :a])
    Q[a:b, a:b] = nearest_special_orthogonal(P[a:b, a:b])
    # R^+ acts by dilatation on the mu component; nearest positive scalar to
    # a real p is p when p > 0, and inf-not-attained (-> 0+) otherwise.
    Q[b:c, b:c] = max(float(P[b, b]), 0.0)
    # Anything beyond the 11 distinguished directions is outside the structure
    # group entirely and is projected to the identity on that complement.
    if d > c:
        Q[c:, c:] = np.eye(d - c)
    return Q


def leakage(P: np.ndarray) -> float:
    """Lambda(P) exactly as Paper 13 Theorem 2.1 writes it."""
    num = np.linalg.norm(P - project_to_G(P), "fro")
    den = np.linalg.norm(P - np.eye(P.shape[0]), "fro")
    if den == 0.0:
        return 0.0
    return float(num / den)


def haar_so(d: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-random element of SO(d) (QR of a Gaussian, sign-corrected)."""
    A = rng.standard_normal((d, d))
    Q, R = np.linalg.qr(A)
    Q = Q * np.sign(np.diag(R))
    if np.linalg.det(Q) < 0:
        Q[:, 0] = -Q[:, 0]
    return Q


def random_in_G(d: int, rng: np.random.Generator,
                dilatation: float = 1.0) -> np.ndarray:
    """A genuine element of G, block-embedded in d dimensions."""
    Q = np.eye(d)
    Q[:DIM_7, :DIM_7] = haar_so(DIM_7, rng)
    Q[DIM_7:DIM_7 + DIM_3, DIM_7:DIM_7 + DIM_3] = haar_so(DIM_3, rng)
    Q[DIM_7 + DIM_3, DIM_7 + DIM_3] = dilatation
    return Q


def geodesic_perturb(Q: np.ndarray, eps: float,
                     rng: np.random.Generator) -> np.ndarray:
    """Push Q off G by a rotation of Frobenius size ~eps in a generic direction."""
    d = Q.shape[0]
    X = rng.standard_normal((d, d))
    X = X - X.T
    X = X / np.linalg.norm(X, "fro")
    # expm of a small skew matrix, series is plenty at this magnitude
    E = np.eye(d)
    term = np.eye(d)
    for k in range(1, 18):
        term = term @ (eps * X) / k
        E = E + term
    return E @ Q


# ==========================================================================
# Result plumbing (same shape as gauge.py / semantic_connection.py)
# ==========================================================================
@dataclass
class Result:
    ok: Optional[bool]
    name: str
    expect: str
    got: str
    note: str


def _wrap(text: str, width: int) -> List[str]:
    out, line = [], ""
    for word in text.split():
        if len(line) + len(word) + 1 > width:
            out.append(line)
            line = word
        else:
            line = word if not line else line + " " + word
    if line:
        out.append(line)
    return out


# ==========================================================================
# Tests
# ==========================================================================
def run_tests() -> List[Result]:
    rng = np.random.default_rng(RNG_SEED)
    res: List[Result] = []

    # ---------------------------------------------------------------- L-1
    # Lambda on genuine elements of G must be 0. Calibrates the instrument:
    # if this is not 0 the projection is wrong and nothing below means anything.
    vals = [leakage(random_in_G(DIM_V, rng, dilatation=s))
            for s in (1.0, 1.0, 0.85, 1.3)]
    worst = max(vals)
    res.append(Result(
        worst < 1e-9,
        "L-1. Lambda = 0 on genuine elements of SO(7) x Aut(chi)?",
        "exactly 0 for any P in G",
        f"max over 4 draws = {worst:.3e}",
        "Instrument calibration, not a finding about Paper 13. The projection "
        "must be exact on the subgroup before its value off the subgroup can "
        "be quoted."))

    # ---------------------------------------------------------------- L-2
    # THE claim: Lambda_generic >= 0.78 for random dense rotations.
    for d in (DIM_V, 48, 768):
        samples = np.array([leakage(haar_so(d, rng)) for _ in range(400)])
        lo, med, hi = samples.min(), np.median(samples), samples.max()
        ok = bool(lo >= 0.78)
        res.append(Result(
            ok,
            f"L-2({d}). Paper 13 Thm 2.1: Lambda_generic >= 0.78 in SO({d})?",
            "every random dense rotation gives Lambda >= 0.78",
            f"min={lo:.4f} median={med:.4f} max={hi:.4f} over 400 Haar draws",
            "The bound is stated in Paper 13 without a dimension. Lambda "
            "depends on d: the subgroup occupies 25 of the d(d-1)/2 rotation "
            "directions, so a random rotation sits further from G as d grows. "
            "A bound quoted with no d attached is not checkable as written, "
            "and holds or fails depending on which d the reader assumes."))

    # ---------------------------------------------------------------- L-3
    # Lambda_true <= 0.05 is a claim about real models and cannot be settled
    # here. What CAN be settled is the geometry it implies: how far off G a
    # transport may sit and still pass. Reported, not judged.
    rows = []
    for eps in (0.01, 0.05, 0.10, 0.25, 0.50, 1.00):
        Q = random_in_G(DIM_V, rng)
        lam = np.median([leakage(geodesic_perturb(random_in_G(DIM_V, rng),
                                                  eps, rng))
                         for _ in range(60)])
        rows.append((eps, lam))
    crossing = None
    for (e0, l0), (e1, l1) in zip(rows, rows[1:]):
        if l0 <= 0.05 <= l1:
            crossing = e0 + (0.05 - l0) * (e1 - e0) / (l1 - l0)
            break
    res.append(Result(
        None,
        "L-3. What does Lambda_true <= 0.05 actually require of a model?",
        "Paper 13 asserts <= 0.05 for 'aligned representations'",
        "  ".join(f"eps={e:.2f}->{l:.3f}" for e, l in rows)
        + (f"   (0.05 crossed near eps={crossing:.3f})" if crossing else ""),
        "UNDERSPECIFIED, not FAIL. The 0.05 figure is a claim about learned "
        "representations and needs a model to test; ENG-4.4 is where that "
        "belongs. This row records what the number means geometrically so the "
        "eventual measurement has a pass criterion instead of a target."))

    # ---------------------------------------------------------------- L-4
    # The 'SNR > 15.6' claim.
    ratio = 0.78 / 0.05
    res.append(Result(
        False,
        "L-4. Is 'SNR > 15.6' a signal-to-noise ratio?",
        "a statistically decisive discriminant, SNR > 15.6",
        f"0.78 / 0.05 = {ratio:.1f}; no variance, sample size, or noise model "
        f"appears anywhere in Theorem 2.1",
        "FINDING. 15.6 is the quotient of the two asserted bounds. A "
        "signal-to-noise ratio divides a separation by a spread; this divides "
        "one bound by the other, so it restates the two numbers rather than "
        "measuring anything. L-2 above gives the spread the claim needs. "
        "Either call it a separation ratio, or compute SNR from the measured "
        "distributions."))

    # ---------------------------------------------------------------- V-1
    # Paper 12 s4.2: twin dragon boundary dimension. My own error in an
    # earlier pass (AUD-ENG-14), so it gets recomputed every run.
    lam_root = np.roots([1.0, -1.0, 0.0, -2.0])
    lam_real = float(max(r.real for r in lam_root if abs(r.imag) < 1e-12))
    d_h = 2.0 * math.log(lam_real, 2)
    ok = abs(lam_real - 1.695620770) < 5e-9 and abs(d_h - 1.523627086) < 5e-9
    res.append(Result(
        ok,
        "V-1. Paper 12 s4.2 twin dragon: lambda root and d_H(dT).",
        "lambda ~ 1.695620770 root of x^3 - x^2 - 2, d_H = 2 log_2 lambda ~ 1.523627086",
        f"lambda = {lam_real:.9f}, d_H = {d_h:.9f}",
        "Recomputed rather than cited. This is the claim I got wrong from "
        "memory in an earlier pass, which is why it is now computed in the "
        "artifact that states it."))

    # ---------------------------------------------------------------- V-2
    # Paper 8 s3.2 Kretschmann bound.
    G_N, c_l, M_bh, l_P = 6.6743e-11, 299792458.0, 1.989e31, 1.616255e-35
    K = 48.0 * G_N ** 2 * M_bh ** 2 / (c_l ** 4 * l_P ** 6)
    ok = abs(K - 5.875e218) / 5.875e218 < 5e-3
    res.append(Result(
        ok,
        "V-2. Paper 8 s3.2: K_max for a 10 M_sun black hole at the Planck floor.",
        "K_max ~ 5.875e218 m^-4",
        f"K_max = {K:.4e} m^-4",
        "Reproduces from the constants the paper itself publishes."))

    # ---------------------------------------------------------------- V-3
    # Paper 8 s6 Benchmark 5, against the engine's own UPE evaluator.
    m1 = m2 = 1.0
    S, U, Rn, Ra, Pe, Pb = 2.5, 1.0, 1.0, 0.0, 1.00, 0.85
    UA, UB = 0.95, 0.10
    v_rel = abs(UA - UB) / max(UA, UB)
    gamma = 1.0 / math.sqrt(1.0 - v_rel ** 2)
    P_total = m1 * m2 * gamma * (S * U / (Rn * (1.0 - Ra))) + Pe + Pb
    ok = abs(P_total - 7.46) < 0.005
    res.append(Result(
        ok,
        "V-3. Paper 8 s6 Benchmark 5: does the published price reproduce?",
        "gamma = 2.24, P = $7.46, row marked PASS",
        f"v_rel = {v_rel:.6f}, gamma = {gamma:.6f}, P = ${P_total:.6f} "
        f"(irm_engine.py evaluate-upe prints P_total = 7.447929)",
        "FINDING. v_rel and gamma reproduce exactly. The total does not: the "
        "paper's own engine returns $7.4479, which rounds to $7.45, and the "
        "benchmark table publishes $7.46 with a PASS. One cent, but the row "
        "asserts agreement between paper and engine and they disagree. F-4 "
        "asked for this parameter vector precisely so the row could be "
        "re-run; re-running it is what turns the number up."))

    return res


def main() -> int:
    print("=" * 78)
    print("PAPER 13 SECTION 2 SUBBUNDLE DISCRIMINANT - ENGINEER VERIFICATION")
    print("=" * 78)
    print(__doc__.strip().split("Run:")[0].strip())
    print()
    print("=" * 78)

    results = run_tests()
    for r in results:
        tag = "UNDERSPEC" if r.ok is None else ("PASS" if r.ok else "FAIL")
        print(f"\n[{tag:^9}] {r.name}")
        print(f"            paper : {r.expect}")
        print(f"            solver: {r.got}")
        for line in _wrap(r.note, 62):
            print(f"            note  : {line}" if line is _wrap(r.note, 62)[0]
                  else f"                    {line}")

    graded = [r for r in results if r.ok is not None]
    npass = sum(1 for r in graded if r.ok)
    nfail = len(graded) - npass
    nunder = len(results) - len(graded)
    print()
    print("=" * 78)
    print(f"{npass} pass / {nfail} fail / {nunder} underspecified")
    print("=" * 78)
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
