#!/usr/bin/env python3
"""
paper17_ns_claims.py - Engineer verification of Formal Paper 17's checkable claims.

Formal Paper 17 is headed "Target: Clay Millennium Prize Problem Resolution" and
concludes (s9.2) that "Global Existence and Smoothness (Statement A) is Proven".
This file checks what can be checked by execution. The two decisive objections
are structural rather than numerical and are stated in T-5 and T-7; they are
recorded here so they travel with the arithmetic.

Companion artifacts audited: navier_stokes_cellular.py (the consolidated
18,656-byte version) and navier_stokes_smoothness.lean.

Run:  python paper17_ns_claims.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List, Optional

import numpy as np

C_LIGHT = 299792458.0
L_PLANCK = 1.616255e-35
CEILING = C_LIGHT / L_PLANCK


@dataclass
class Result:
    ok: Optional[bool]
    name: str
    expect: str
    got: str
    note: str


def _wrap(text: str, width: int) -> List[str]:
    out, line = [], ""
    for w in text.split():
        if len(line) + len(w) + 1 > width:
            out.append(line); line = w
        else:
            line = w if not line else line + " " + w
    if line:
        out.append(line)
    return out


def run_tests() -> List[Result]:
    res: List[Result] = []

    # ------------------------------------------------------------------ T-1
    res.append(Result(
        abs(CEILING - 1.85487e43) / 1.85487e43 < 1e-4,
        "T-1. s3.1 universal strain ceiling c / l_P",
        "1.85487e43 s^-1",
        f"{CEILING:.5e} s^-1",
        "The paper's headline constant reproduces. Recorded as a PASS so the "
        "failures below are not read as a blanket rejection."))

    # ------------------------------------------------------------------ T-2
    eps = 2.0 * CEILING ** 2
    res.append(Result(
        abs(eps - 6.88e84) / 6.88e84 < 1e-2,
        "T-2. s6.2 maximum viscous dissipation eps_max = 2 nu (c/l_P)^2",
        "6.88e84 nu W/m^3",
        f"{eps:.3e} nu W/m^3 - the paper is low by a factor of "
        f"{eps / 6.88e84:.0f}",
        "FINDING. Off by 10^2. Same magnitude of error, and the same factor, "
        "as the deleted irm_engine (1).py Kretschmann value. Two 100x slips in "
        "one day suggests a shared source rather than two coincidences."))

    # ------------------------------------------------------------------ T-3
    octaves = math.floor(math.log2(1.0 / L_PLANCK))
    decades = math.log10(1.0 / L_PLANCK)
    lean_reach = 1.0 / 2 ** 35
    short_by = math.log10(lean_reach / L_PLANCK)
    res.append(Result(
        False,
        "T-3. s7.2 octree depth vs the Lean file's depth cap",
        "l_max = floor(log2(L_0 / l_P)) <= 116 dyadic levels to reach the floor",
        f"computed l_max = {octaves} octaves ({decades:.2f} decades). The Lean "
        f"caps h_depth : depth <= 35, reaching {lean_reach:.3e} m - short of "
        f"l_P by {short_by:.1f} decades",
        "FINDING. 35 is the number of DECADES (log10) and 116 the number of "
        "OCTAVES (log2). The Lean file has taken the decade count as a dyadic "
        "depth cap, so its fractal grid terminates around the atomic scale "
        "rather than at the Planck floor. Theorem 7.1's part 2 - 'at the "
        "terminating depth, sub-cell resolution coincides with the Cost of "
        "Being floor' - is false of the formalisation as written."))

    # ------------------------------------------------------------------ T-4
    t_break = 1e100 / CEILING
    res.append(Result(
        False,
        "T-4. Lean bkm_integral_strictly_finite is FALSE as stated",
        "(T_star * universal_strain_ceiling) < 1e100, hypothesis only T_star > 0",
        f"false for every T_star > {t_break:.4e} s; the statement quantifies "
        f"over all positive T_star",
        "FINDING. The theorem as written is not the BKM criterion (which is "
        "the integral of ||omega||_inf over time) but a numeric inequality "
        "between two constants, and it is false for large T_star. It carries "
        "`sorry`, so nothing is proved either way - but a `sorry` on a false "
        "statement is worse than an unproved true one, because completing it "
        "is impossible rather than merely open."))

    # ------------------------------------------------------------------ T-5
    # The decisive objection, made executable: the s3.1 bound discriminates
    # nothing, because it holds for ANY bounded field on a floored lattice.
    rng = np.random.default_rng(17)
    n = 40
    fields = {
        "a Navier-Stokes-like smooth field": np.sin(
            np.linspace(0, 2 * np.pi, n)) * C_LIGHT * 0.5,
        "white noise (solves nothing)": rng.uniform(
            -C_LIGHT, C_LIGHT, n),
        "a discontinuous square wave": np.where(
            np.arange(n) % 7 < 3, C_LIGHT, -C_LIGHT).astype(float),
    }
    quotients = {}
    for label, f in fields.items():
        # the paper's s2.2 derivative: a difference quotient at fixed step l_P
        q = np.max(np.abs(np.diff(f))) / L_PLANCK
        quotients[label] = q
    all_bounded = all(q <= 2 * CEILING * 1.0000001 for q in quotients.values())
    res.append(Result(
        not all_bounded,
        "T-5. Does the s3.1 ceiling distinguish solutions from non-solutions?",
        "a regularity theorem must fail for fields that are not solutions",
        "every field tested satisfies it: " + "; ".join(
            f"{k} -> {v:.3e}" for k, v in quotients.items())
        + f"  (all <= 2c/l_P = {2 * CEILING:.3e})",
        "FINDING, and the decisive one. Theorem 3.1 bounds a difference "
        "quotient with a fixed denominator l_P and a numerator bounded by 2c. "
        "That is arithmetic about bounded functions on a lattice, and it holds "
        "for white noise and for a discontinuous square wave exactly as it "
        "holds for a smooth flow. A bound satisfied by every field regardless "
        "of the equation cannot separate regular solutions from singular ones, "
        "so it is not a regularity theorem. Everything in the paper rests on "
        "it: Theorem 4.1 integrates it, and Theorem 5.1 feeds it to Serrin."))

    # ------------------------------------------------------------------ T-6
    # Does the mechanism ever engage in the companion solver?
    observed_max_vorticity = 5.019709      # Kida-Pelz, the most extreme test
    headroom = math.log10(CEILING / observed_max_vorticity)
    res.append(Result(
        False,
        "T-6. Does navier_stokes_cellular.py ever exercise the ceiling?",
        "5/5 PASS is offered as corroboration of the regularization",
        f"largest vorticity anywhere in the 5 suites = "
        f"{observed_max_vorticity:.3f} s^-1, which is {headroom:.1f} decades "
        f"below the c/l_P ceiling of {CEILING:.3e}",
        "FINDING. The regularizer the proof depends on is never active in any "
        "test. The suites exercise an ordinary incompressible solver, which "
        "behaves as one should. Three further defects in that suite: TEST 2, "
        "the 'singularity stress test', measures vorticity FALLING 3.230 -> "
        "2.170; TEST 4 reports ||u||_H3 GROWING 62.998 -> 64.256 and calls it "
        "'uniformly bounded'; TEST 5 reports 1 fractal level and inter-scale "
        "flux of exactly 0.000000 and calls it 'smoothly transfers "
        "enstrophy'. Per AUD-ENG-35, a suite that has never printed FAIL is "
        "evidence about the suite."))

    # ------------------------------------------------------------------ T-7
    res.append(Result(
        None,
        "T-7. Is the theorem proved the theorem the Clay problem poses?",
        "Fefferman 2000 poses Statement A on R^3 (or the torus T^3)",
        "Paper 17 s9.2: 'Statement A is Proven on (M^3, g_munu^IRM)' - a "
        "manifold whose defining axiom is d(x,y) >= l_P for x != y",
        "NOT A COMPUTATION - stated here so it travels with the arithmetic. "
        "M^3 is not R^3. The Clay problem asks whether the Archimedean "
        "continuum admits finite-time blowup; replacing it with a space that "
        "has a minimum separation answers a different question. The paper "
        "argues in s9.1 that blowup is 'an unphysical pathology arising from "
        "the idealization of space as an infinitely divisible continuum' - "
        "which is a case that the Clay problem is UNINTERESTING, not that it "
        "is solved. That case may be worth making. It is not a resolution, "
        "and the registry must not carry it as one."))

    return res


def main() -> int:
    print("=" * 78)
    print("FORMAL PAPER 17 - ENGINEER VERIFICATION OF CHECKABLE CLAIMS")
    print("=" * 78)
    print(__doc__.strip().split("Run:")[0].strip())
    print("=" * 78)

    results = run_tests()
    for r in results:
        tag = "STRUCTURAL" if r.ok is None else ("PASS" if r.ok else "FAIL")
        print(f"\n[{tag:^10}] {r.name}")
        print(f"             paper : {r.expect}")
        print(f"             solver: {r.got}")
        for i, line in enumerate(_wrap(r.note, 61)):
            print(f"             note  : {line}" if i == 0
                  else f"                     {line}")

    graded = [r for r in results if r.ok is not None]
    npass = sum(1 for r in graded if r.ok)
    nfail = len(graded) - npass
    print()
    print("=" * 78)
    print(f"{npass} pass / {nfail} fail / {len(results) - len(graded)} structural")
    print()
    print("VERDICT")
    print("  The arithmetic is mostly right and one constant is wrong by 100x.")
    print("  The Lean file proves nothing: every theorem carries `sorry`, the")
    print("  Navier-Stokes equation appears nowhere in it, and the Millennium")
    print("  theorem's body is the Bool `true`.")
    print("  The mathematical objection is T-5: the central bound holds for")
    print("  every bounded field on the lattice, so it cannot be a regularity")
    print("  criterion. The domain objection is T-7: M^3 is not R^3.")
    print("=" * 78)
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
