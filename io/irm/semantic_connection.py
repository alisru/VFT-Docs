#!/usr/bin/env python3
"""
semantic_connection.py - the missing map from an embedding space to a gauge
connection.

Formal Paper 9 asserts that Information Space is a principal G-bundle and that
"understanding is holonomy-free parallel transport (F_mu_nu = 0)". It never
says what A_mu IS for an actual learned representation, so the claim has no
empirical content. gauge.py (ENG-2) made F computable ONCE YOU HAVE A
CONNECTION. This module constructs the connection from representations.

THE CONSTRUCTION
----------------
Base manifold : the context space C. A point c is whatever conditions the
                model's encoding - a framing, persona, prompt prefix, position.
                Paper 9's Delta^42 is the claim that C is charted by 7
                interrogative planes x 6 inquiry axes.
Fibre         : the representation space R^d. What is physically meaningful is
                not a vector but a FRAME, since no direction in R^d is
                intrinsically labelled. The bundle is the frame bundle.
Probe set     : N fixed concepts. E(c) in R^{N x d} stacks their embeddings in
                context c, row-centred and unit-normalised.
Transport     : P(c -> c') = argmin over R in SO(d) of || E(c) R - E(c') ||_F,
                the orthogonal Procrustes map. Solved by SVD.
Connection    : A_mu(c) = lim_{h->0} log P(c -> c + h e_mu) / h  in so(d).
Curvature     : F_mu_nu = d_mu A_nu - d_nu A_mu + [A_mu, A_nu], or equivalently
                and more stably the lattice plaquette log(W_square)/h^2.

WHAT CURVATURE MEANS HERE
-------------------------
A representation is a function of context alone: E : C -> R^{N x d}. So if
context acted on representations by an EXACT rotation, we would have
E(c') = E(c) R(c, c') with zero residual, forcing R(c, c') = R(c)^-1 R(c') and
hence A = R^-1 dR, which is pure gauge and therefore FLAT.

Curvature can only arise when the Procrustes fit is INEXACT. So:

    F = 0   <=>  reframing moves the frame but leaves the relational geometry
                 of the probe set rigid.
    F != 0  <=>  reframing DEFORMS the relative geometry, no rotation can
                 identify the two configurations, and the best-fit rotations
                 fail to compose around a loop.

That is a sharper reading of Paper 9's thesis than the paper states, and it is
testable. "Understanding a concept invariantly" becomes "its relations to other
concepts are rigid under reframing"; ideological curvature becomes "reframing
warps those relations."

Observable consequences, all known LLM phenomena, all predicted to be the same
quantity: prompt order effects, framing effects, context hysteresis in long
conversations, and getting a different answer by a roundabout route.

VALIDATION STATUS
-----------------
Validated here against SYNTHETIC ground truth, where the rigidity of the
context action is a tunable knob. Not yet run against a real language model -
no cached model is available locally and downloading one needs the user's go
ahead. The estimator is model-agnostic: supply any callable c -> E(c).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple

import numpy as np
from scipy.linalg import logm

# A context is a real coordinate vector; an embedding map takes one to an
# N x d array of probe representations.
EmbedFn = Callable[[np.ndarray], np.ndarray]


# ==========================================================================
# Transport
# ==========================================================================
@dataclass
class Transport:
    R: np.ndarray          # the SO(d) rotation
    scale: float           # the R^+ dilatation factor
    residual: float        # relative Procrustes residual; 0 => rigid action


def procrustes_transport(E1: np.ndarray, E2: np.ndarray,
                         allow_scale: bool = False) -> Transport:
    """
    Best rotation carrying the probe configuration in context 1 to context 2.

        R = argmin_{R in SO(d)} || E1 R - E2 ||_F

    The residual is the part of the context change that is NOT a rigid motion.
    It is the source of all curvature (see module docstring), so it is returned
    rather than discarded.

    With allow_scale=True the fit also returns the best uniform dilatation,
    which is the R^+ factor of Aut(chi) - see gauge.py finding G-2.
    """
    M = E1.T @ E2
    U, S, Vt = np.linalg.svd(M)
    D = np.eye(U.shape[0])
    # Keep the map in SO(d) rather than O(d): a reflection is not connected to
    # the identity and cannot be a parallel transport.
    D[-1, -1] = np.sign(np.linalg.det(U @ Vt))
    R = U @ D @ Vt

    scale = 1.0
    if allow_scale:
        denom = float(np.sum(E1 * E1))
        scale = float(np.sum(S * np.diag(D))) / denom if denom > 0 else 1.0

    approx = scale * (E1 @ R)
    num = float(np.linalg.norm(approx - E2))
    den = float(np.linalg.norm(E2))
    return Transport(R, scale, num / den if den > 0 else 0.0)


def normalise(E: np.ndarray) -> np.ndarray:
    """Row-centre and unit-normalise, so only relational geometry survives."""
    E = E - E.mean(axis=0, keepdims=True)
    n = np.linalg.norm(E, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return E / n


# ==========================================================================
# Connection and curvature
# ==========================================================================
class SemanticConnection:
    """Gauge connection induced on the frame bundle by an embedding map."""

    def __init__(self, embed: EmbedFn, h: float = 1e-3,
                 allow_scale: bool = False):
        self.embed = embed
        self.h = h
        self.allow_scale = allow_scale

    def _E(self, c: np.ndarray) -> np.ndarray:
        return normalise(self.embed(c))

    def transport(self, c1: np.ndarray, c2: np.ndarray) -> Transport:
        return procrustes_transport(self._E(c1), self._E(c2), self.allow_scale)

    def A(self, c: np.ndarray, mu: int) -> np.ndarray:
        """A_mu(c) in so(d), by symmetric difference of the transport."""
        cp, cm = c.copy(), c.copy()
        cp[mu] += self.h
        cm[mu] -= self.h
        R = procrustes_transport(self._E(cm), self._E(cp), False).R
        L = np.real(logm(R))
        return L / (2 * self.h)

    def curvature_from_A(self, c: np.ndarray, mu: int, nu: int) -> np.ndarray:
        """F = d_mu A_nu - d_nu A_mu + [A_mu, A_nu]. Same form as gauge.py."""
        cp, cm = c.copy(), c.copy()
        cp[mu] += self.h
        cm[mu] -= self.h
        dmu_Anu = (self.A(cp, nu) - self.A(cm, nu)) / (2 * self.h)

        cp, cm = c.copy(), c.copy()
        cp[nu] += self.h
        cm[nu] -= self.h
        dnu_Amu = (self.A(cp, mu) - self.A(cm, mu)) / (2 * self.h)

        Amu, Anu = self.A(c, mu), self.A(c, nu)
        return dmu_Anu - dnu_Amu + (Amu @ Anu - Anu @ Amu)

    def plaquette(self, c: np.ndarray, mu: int, nu: int,
                  h: Optional[float] = None) -> Tuple[np.ndarray, float]:
        """
        Lattice-gauge plaquette: transport around a small square in the
        (mu, nu) plane and return (holonomy, ||F|| estimate = ||log W|| / h^2).

        More stable than differencing A, because it never takes a matrix log of
        a near-identity twice.
        """
        h = self.h if h is None else h
        c00 = c.copy()
        c10 = c.copy(); c10[mu] += h
        c11 = c.copy(); c11[mu] += h; c11[nu] += h
        c01 = c.copy(); c01[nu] += h

        W = np.eye(self._E(c).shape[1])
        for a, b in ((c00, c10), (c10, c11), (c11, c01), (c01, c00)):
            W = W @ procrustes_transport(self._E(a), self._E(b), False).R
        return W, float(np.linalg.norm(np.real(logm(W)))) / (h * h)

    def holonomy(self, loop: Sequence[np.ndarray]) -> Tuple[np.ndarray, float]:
        """Compose transport around a closed context loop; return (U, ||U-I||)."""
        d = self._E(loop[0]).shape[1]
        U = np.eye(d)
        for i in range(len(loop)):
            a, b = loop[i], loop[(i + 1) % len(loop)]
            U = U @ procrustes_transport(self._E(a), self._E(b), False).R
        return U, float(np.linalg.norm(U - np.eye(d)))

    def subbundle_leakage(self, c: np.ndarray, mu: int, k: int,
                          step: float = 0.5) -> float:
        """
        Fraction of a k-dimensional distinguished subspace that leaves that
        subspace when transported over a FINITE context change.

        This is the test of Paper 9's structure-group reduction. The paper takes
        G = SO(7), i.e. it assumes a 7-dimensional plane subbundle that is
        PARALLEL - preserved by transport. If leakage is large, SO(7) is a lossy
        approximation to the true SO(d) connection and the paper should say so.
        Returns 0 for an exactly parallel subbundle, up to 1 for total leakage.

        NOTE: the step must be finite. Over an infinitesimal step R -> I and
        leakage -> 0 for ANY subspace, so an infinitesimal version of this
        measurement cannot discriminate and is meaningless.
        """
        cp = c.copy()
        cp[mu] += step
        R = procrustes_transport(self._E(c), self._E(cp), False).R
        d = R.shape[0]
        P = np.zeros((d, d))
        P[:k, :k] = np.eye(k)                  # projector onto the subbundle
        moved = R.T @ P @ R                    # the transported subspace
        inside = float(np.trace(P @ moved @ P))
        return max(0.0, 1.0 - inside / k)


# ==========================================================================
# Synthetic ground truth
# ==========================================================================
def synthetic_model(d: int = 48, n_probes: int = 300, dim_context: int = 4,
                    deformation: float = 0.0, seed: int = 11,
                    block: Optional[int] = None) -> EmbedFn:
    """
    A controlled stand-in for a language model.

    E(c) = E0 @ R(c) + deformation * D(c)

      R(c) in SO(d)  : context acts by rotating the frame. Rigid.
      D(c)           : a context-dependent NON-rigid warp of the relational
                       geometry, i.e. the part no rotation can undo.

    deformation = 0 gives an exactly rigid context action, for which the induced
    connection must be pure gauge and the curvature must vanish. Raising it
    should raise ||F|| smoothly. That is the ground truth this module is
    validated against.
    """
    rng = np.random.default_rng(seed)
    E0 = rng.normal(size=(n_probes, d))
    gens = [rng.normal(size=(d, d)) for _ in range(dim_context)]
    if block is not None:
        # Block-diagonal generators preserve the first `block` coordinates
        # exactly, giving a genuinely parallel subbundle to calibrate the
        # leakage measurement against.
        for G in gens:
            G[:block, block:] = 0.0
            G[block:, :block] = 0.0
    gens = [0.7 * (G - G.T) / np.linalg.norm(G - G.T) * math.sqrt(d)
            for G in gens]
    warps = [rng.normal(size=(n_probes, d)) * 0.1 for _ in range(dim_context)]

    def embed(c: np.ndarray) -> np.ndarray:
        from scipy.linalg import expm
        X = sum(c[i] * gens[i] for i in range(len(gens)))
        R = expm(X)
        out = E0 @ R
        if deformation:
            # Non-rigid: a warp whose PATTERN depends on context, so it cannot
            # be absorbed into any single global rotation.
            w = sum(math.sin(2.3 * c[i]) * warps[i] for i in range(len(warps)))
            out = out + deformation * w
        return out
    return embed


# ==========================================================================
# Tests
# ==========================================================================
@dataclass
class Result:
    name: str
    expected: str
    got: str
    ok: Optional[bool]
    note: str = ""


def run_tests() -> List[Result]:
    out: List[Result] = []
    c0 = np.array([0.21, -0.13, 0.07, 0.34])

    # S1. Rigid context action must give flat connection.
    conn_rigid = SemanticConnection(synthetic_model(deformation=0.0), h=2e-3)
    t = conn_rigid.transport(c0, c0 + np.array([0.05, 0.0, 0.0, 0.0]))
    _, f_rigid = conn_rigid.plaquette(c0, 0, 1)
    ok1 = t.residual < 1e-8 and f_rigid < 1e-3
    out.append(Result(
        "S1. Rigid context action => F = 0",
        "Procrustes residual 0, ||F|| 0",
        f"residual = {t.residual:.2e}, ||F_01|| = {f_rigid:.3e}", ok1,
        "Confirms the module's central claim: if reframing acts by exact "
        "rotation, the connection is pure gauge and must be flat. Curvature "
        "requires the fit to be inexact."))

    # S2. Curvature should grow with non-rigidity.
    rows = []
    for eps in (0.0, 0.05, 0.2, 0.8, 3.2):
        conn = SemanticConnection(synthetic_model(deformation=eps), h=2e-3)
        res = conn.transport(c0, c0 + np.array([0.05, 0.0, 0.0, 0.0])).residual
        _, f = conn.plaquette(c0, 0, 1)
        rows.append((eps, res, f))
    monotone = all(rows[i][2] <= rows[i + 1][2] * 1.15
                   for i in range(len(rows) - 1))
    ok2 = monotone and rows[-1][2] > 100 * max(rows[0][2], 1e-12)
    out.append(Result(
        "S2. ||F|| increases with non-rigidity of the context action",
        "monotone increase in ||F|| with deformation",
        "  ".join(f"eps={e:.2f}: resid={r:.3f}, ||F||={f:.3f}"
                 for e, r, f in rows), ok2,
        "Curvature is a graded measure of how far reframing is from a rigid "
        "motion, not a binary."))

    # S3. Holonomy around a closed context loop.
    loop = [c0,
            c0 + np.array([0.25, 0.0, 0.0, 0.0]),
            c0 + np.array([0.25, 0.25, 0.0, 0.0]),
            c0 + np.array([0.0, 0.25, 0.0, 0.0])]
    _, dev_rigid = conn_rigid.holonomy(loop)
    conn_def = SemanticConnection(synthetic_model(deformation=0.15), h=2e-3)
    _, dev_def = conn_def.holonomy(loop)
    ok3 = dev_rigid < 1e-6 < dev_def
    out.append(Result(
        "S3. Closed context loop: hysteresis only when non-rigid",
        "||U - I|| = 0 rigid, > 0 deformed",
        f"rigid: {dev_rigid:.3e}   deformed: {dev_def:.4f}", ok3,
        "This is the operational form of Paper 9 Thm 3.1. Return to the "
        "starting context by a loop; a residual rotation is context hysteresis "
        "- the same thing as prompt order effects and framing carryover."))

    # S4. Cross-validate the two curvature routes.
    conn = SemanticConnection(synthetic_model(deformation=0.10), h=4e-3)
    f_plaq = conn.plaquette(c0, 0, 1)[1]
    f_diff = float(np.linalg.norm(conn.curvature_from_A(c0, 0, 1)))
    rel = abs(f_plaq - f_diff) / max(f_plaq, f_diff)
    ok4 = rel < 0.35
    out.append(Result(
        "S4. Plaquette curvature agrees with the differenced-A curvature",
        "two independent routes agree",
        f"plaquette ||F|| = {f_plaq:.4f}, differenced ||F|| = {f_diff:.4f} "
        f"(rel. gap {rel * 100:.1f}%)", ok4,
        "Same cross-check as ENG-2's Ambrose-Singer test, now on an "
        "embedding-derived connection. Agreement is loose because differencing "
        "A takes two nested matrix logs; the plaquette is the estimator to use."))

    # S5. Is Paper 9's SO(7) reduction justified? Calibrate the instrument
    # against a model that HAS a parallel 7-subbundle and one that does not.
    conn_par = SemanticConnection(
        synthetic_model(deformation=0.0, block=7), h=2e-3)
    sweep = []
    for step in (0.25, 0.5, 1.0, 2.0):
        sweep.append((step,
                      conn_par.subbundle_leakage(c0, 0, k=7, step=step),
                      conn_rigid.subbundle_leakage(c0, 0, k=7, step=step)))
    leak_parallel = max(p for _, p, _ in sweep)
    leak_generic = max(g for _, _, g in sweep)
    # The criterion is DISCRIMINATION, not an absolute magnitude: leakage for a
    # generic subspace depends on how far the transport rotates, so a fixed
    # threshold would be arbitrary. What must hold is that a genuinely parallel
    # subbundle reads ~0 while a generic one does not.
    ok5 = leak_parallel < 1e-3 and leak_generic > 100 * max(leak_parallel, 1e-12)
    out.append(Result(
        "S5. Does the leakage measure detect a non-parallel subbundle?",
        "~0% for a parallel subbundle, clearly non-zero for a generic one",
        "  ".join(f"step={s:.2f}: parallel={p * 100:.3f}% generic={g * 100:.1f}%"
                 for s, p, g in sweep), ok5,
        "Instrument calibration, not yet a finding about Paper 9. It shows the "
        "measure discriminates: near-zero when a parallel subbundle genuinely "
        "exists, large otherwise. Paper 9 reduces the structure group to SO(7), "
        "which PRESUMES the 7-plane subbundle is parallel - an empirical claim "
        "the paper never tests. Pointing this at a real model settles it. High "
        "leakage would mean SO(7) is a lossy chart of an SO(d) connection and "
        "the reduction must be restated as an approximation."))

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
    print("SEMANTIC CONNECTION - embedding space -> gauge connection")
    print("=" * width)
    print("\nvalidated against synthetic ground truth; no language model used\n")
    passed = failed = 0
    for r in results:
        tag = "PASS" if r.ok else "FAIL"
        passed, failed = (passed + 1, failed) if r.ok else (passed, failed + 1)
        print(f"[{tag:^6}] {r.name}")
        print(f"         expect: {r.expected}")
        print(f"         got   : {r.got}")
        if r.note:
            for i, line in enumerate(_wrap(r.note, width - 19)):
                print(f"         {'note  : ' if i == 0 else '        '}{line}")
        print()
    print("=" * width)
    print(f"{passed} pass / {failed} fail")
    print("=" * width)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
