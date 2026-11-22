#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
base_systems.py - Variable, infinite and fractal-recursive bases: what the
corpus already has, what it has named, and what the orthodox names are.

THE DIRECTOR'S QUESTION
-----------------------
"Have we explored base infinite? base fn()? fractal recursive bases?"

Short answer, established below by execution rather than assertion:

  * base fn()          ALREADY IN THE FORMALISM, unnamed. Paper 1 section 3.2's
                       evaluation map IS the Cantor series expansion (1869).
                       The engine computes it correctly. The NOTATION cannot
                       express it.
  * base infinite      PRESENT BUT ONLY QUALITATIVELY (Paper 1 section 7,
                       "amplifying mirror"). The orthodox object is the
                       factorial-base / profinite completion, and it does NOT
                       rescue the base-10 defect of orthodox_bridge.py B-2.
  * fractal recursive  NOT EXPLORED, and this is the real gap. The orthodox
                       name is Bratteli-Vershik / adic numeration. A concrete
                       instance is verified below.

Run:  python base_systems.py
"""
from __future__ import annotations

import itertools
import math
from fractions import Fraction
from typing import Dict, List, Optional, Set, Tuple

RESULTS: List[Tuple[str, str, str]] = []


def record(bid: str, status: str, headline: str) -> None:
    RESULTS.append((bid, status, headline))


def head(bid: str, title: str) -> None:
    print()
    print("-" * 78)
    print("%s  %s" % (bid, title))
    print("-" * 78)


# ==========================================================================
# B-10. base fn() is already the formalism - it is the Cantor series
# ==========================================================================
def cantor_expand(x: Fraction, bases: List[int]) -> List[int]:
    """Greedy digits of x in [0,1) for the mixed radix (b_1, b_2, ...)."""
    digits = []
    r = x
    for b in bases:
        r *= b
        d = int(r)
        digits.append(d)
        r -= d
    return digits


def cantor_value(digits: List[int], bases: List[int]) -> Fraction:
    """Paper 1 section 3.2:  sum_k s_k / prod_{i<=k} b_i."""
    val, denom = Fraction(0), Fraction(1)
    for s, b in zip(digits, bases):
        denom *= b
        val += Fraction(s) / denom
    return val


def bridge_10() -> None:
    head("B-10", "Paper 1 section 3.2 IS the Cantor series expansion (1869)")
    print("Paper 1 section 3.1 types the number as carrying a base SEQUENCE")
    print("(b_k), and section 3.2 evaluates it as")
    print()
    print("      Val = b + n + sum_k [ s_k / prod_{i<=k} b_i ]")
    print()
    print("That is not a new construction. It is the Cantor series expansion,")
    print("Georg Cantor 1869, the standard mixed-radix numeration system. The")
    print("corpus writes it down and then immediately sets every b_k = 10.")
    print()

    # Factorial base: b_k = k+1. Classical, and the canonical 'growing base'.
    fact_bases = [k + 1 for k in range(1, 12)]
    tests = [Fraction(23, 24), Fraction(1, 3), Fraction(5, 7), Fraction(1, 2)]
    ok = True
    print("   factorial base b_k = k+1 (place values 1/2!, 1/3!, ...):")
    for x in tests:
        d = cantor_expand(x, fact_bases)
        back = cantor_value(d, fact_bases)
        exact = (back == x)
        ok = ok and (exact or abs(float(back - x)) < 1e-12)
        print("     %-8s -> digits %-26s -> %-10s %s"
              % (x, d[:7], back if exact else "%.10f" % float(back),
                 "EXACT" if exact else "converging"))
    print()
    print("   Digit ranges are correct by construction: s_k < b_k always.")
    rng_ok = all(0 <= s < b for x in tests
                 for s, b in zip(cantor_expand(x, fact_bases), fact_bases))
    print("   digit s_k in [0, b_k) for every test: %s" % rng_ok)
    print()
    print("   ORTHODOX ANCHOR. Cantor (1869), 'Ueber die einfachen")
    print("   Zahlensysteme'. Every real in [0,1) has a Cantor series")
    print("   expansion w.r.t. any base sequence with b_k >= 2, and it is")
    print("   unique up to the usual tail convention. Plain ZFC, no choice.")
    record("B-10", "PASS" if (ok and rng_ok) else "FAIL",
           "Paper 1 s3.2 evaluation map identified as the Cantor series (1869); "
           "verified exact on factorial base over 4 rationals")


# ==========================================================================
# B-11. The engine computes variable bases; the NOTATION cannot express them
# ==========================================================================
def bridge_11() -> None:
    head("B-11", "Engine supports base fn(); [base_n.d.e.f...] notation does not")
    print("Verification by execution against the live engine.")
    print()
    try:
        from irm_engine import RealityNumber
    except Exception as exc:                                # pragma: no cover
        print("   engine import failed: %s" % exc)
        record("B-11", "FAIL", "irm_engine import failed")
        return

    x = RealityNumber(base=0, n=0, fractions=[1, 2, 3], bases=[2, 3, 4])
    expect = Fraction(1, 2) + Fraction(2, 6) + Fraction(3, 24)
    val_ok = (x.standard == expect)
    print("   constructor with bases=(2,3,4), digits (1,2,3):")
    print("     engine   = %s" % x.standard)
    print("     expected = %s   -> %s" % (expect, "MATCH" if val_ok else "MISMATCH"))

    range_ok = False
    try:
        RealityNumber(base=0, n=0, fractions=[3], bases=[2])
    except ValueError:
        range_ok = True
    print("   per-depth digit range enforced: %s" % range_ok)

    y = RealityNumber.from_string("[0_0.1.2.3]")
    notation_ok = (y.bases == [10, 10, 10])
    print()
    print("   BUT the canonical notation cannot carry the base sequence:")
    print("     from_string('[0_0.1.2.3]').bases = %s" % y.bases)
    print()
    print("   FINDING. Paper 1 section 3.1 makes (b_k) part of the TYPE, but")
    print("   the canonical string form '[ b _ n . d . e . f ... ]' it defines")
    print("   in the same section has no slot for it. So the notation is")
    print("   strictly less expressive than the type it is supposed to denote,")
    print("   and every parsed number silently becomes base 10 at every depth.")
    print("   A variable-base number can be CONSTRUCTED but never WRITTEN.")
    print()
    print("   A second inconsistency, same area: section 4.1 fixes the")
    print("   coalgebra functor as F(X) = Z x N_0 x (d -> X) x chi with")
    print("   'd = {0,...,9} the decimal digit alphabet'. If the base varies")
    print("   with depth then the alphabet varies with depth, so the functor")
    print("   is not this one - it is a dependent/indexed polynomial functor")
    print("   with alphabet d_k at level k, and FINALITY MUST BE RE-DERIVED.")
    print("   The finality claim as stated covers only the fixed-base case.")
    ok = val_ok and range_ok and notation_ok
    record("B-11", "PASS" if ok else "FAIL",
           "engine computes mixed radix correctly, but from_string collapses "
           "all depths to base 10; notation less expressive than the type")


# ==========================================================================
# B-12. Base infinity: the orthodox object, and what it does NOT fix
# ==========================================================================
def bridge_12() -> None:
    head("B-12", "Base infinity -> factorial base -> profinite integers")
    print("Paper 1 section 7 has 'Base Infinity (B_inf) as an Amplifying")
    print("Mirror', but it is qualitative: 'Number = Seed x B_inf', 'the")
    print("Infiniteness of Five', and the rule N + inf := N + 1. There is no")
    print("construction and nothing computable.")
    print()
    print("   The orthodox object that IS 'base infinity' is the inverse limit")
    print("   of the factorial-base truncations:")
    print()
    print("       Z-hat = lim_<- Z / n! Z   ~=   prod_p Z_p")
    print()
    print("   i.e. the profinite integers. Every b_k grows without bound, and")
    print("   the completion contains every p-adic integer at once.")
    print()
    # Demonstrate the CRT decomposition concretely.
    n = math.factorial(12)
    print("   12! = %d" % n)
    fac: Dict[int, int] = {}
    m = n
    for p in (2, 3, 5, 7, 11):
        while m % p == 0:
            fac[p] = fac.get(p, 0) + 1
            m //= p
    print("       = " + " * ".join("%d^%d" % (p, e) for p, e in sorted(fac.items())))
    print("   so Z/12!Z ~= " + " x ".join("Z/%d^%dZ" % (p, e)
                                          for p, e in sorted(fac.items())))
    print()
    # The key negative result: this does NOT remove zero divisors.
    p, q = 2 ** fac[2], n // (2 ** fac[2])
    a = q * pow(q, -1, p) % n
    b = (1 - a) % n
    zd = (a * b) % n == 0 and a % n != 0 and b % n != 0
    print("   CRITICAL: this does NOT rescue orthodox_bridge.py B-2.")
    print("   A product of rings has zero divisors. Idempotent a = %d" % a)
    print("   with b = 1 - a = %d gives a*b mod 12! = %d"
          % (b, (a * b) % n))
    print("   with both factors non-zero: %s" % zd)
    print()
    print("   CONSEQUENCE. Moving to base infinity does NOT buy a field. Only")
    print("   a SINGLE PRIME does: Z_p is a domain and Q_p is a field, for p")
    print("   prime and only then. So if the corpus wants non-Archimedean")
    print("   FIELD language it must pick one prime, or drop the p-adic")
    print("   framing entirely and take the Levi-Civita reading of LINK-02,")
    print("   where the exponent set is Q and no base is privileged at all.")
    record("B-12", "PASS" if zd else "FAIL",
           "base infinity identified as factorial/profinite completion "
           "Z-hat = prod_p Z_p; shown NOT to remove zero divisors")


# ==========================================================================
# B-13. Fractal recursive bases: a real one, verified
# ==========================================================================
def bridge_13() -> None:
    head("B-13", "Fractal recursive bases -> canonical number systems")
    print("This is the genuine gap. The corpus calls [base_n.d.e.f...] a")
    print("'recursive fractal number system' but never connects it to the")
    print("field where recursive, self-similar numeration is the subject.")
    print()
    print("   Verifying one concrete instance: base beta = -1 + i over the")
    print("   Gaussian integers Z[i], with digit set {0, 1}. Katai-Szabo")
    print("   (1975) proves every Gaussian integer has a UNIQUE finite")
    print("   representation sum_k d_k (-1+i)^k. Its fundamental domain is")
    print("   the 'twin dragon'. The TILE has Hausdorff dimension 2 (it has")
    print("   positive planar area); its BOUNDARY has dimension 2*log2(lam) =")
    print("   1.5236, lam the real root of x^3 - x^2 - 2 (Gilbert 1982).")
    print("   CORRECTION 2026-08-28: an earlier version of this file said the")
    print("   BOUNDARY had dimension 2. That was wrong and it propagated into")
    print("   Formal Paper 12 section 4.2 - see CLAUDE_LOG.md Entry 009.")
    print()

    def expand(z: complex) -> Optional[List[int]]:
        """Greedy expansion of a Gaussian integer in base -1+i, digits {0,1}."""
        a, b = int(round(z.real)), int(round(z.imag))
        digits = []
        for _ in range(200):
            if a == 0 and b == 0:
                return digits
            # a+bi is divisible by (-1+i) iff a+b is even, so the digit
            # is forced by the parity of a+b, NOT by the parity of a alone.
            d = (a + b) % 2
            a -= d
            # divide (a + bi) by (-1 + i):  (a+bi)(-1-i)/2 = ((-a+b) + (-a-b)i)/2
            a, b = (-a + b) // 2, (-a - b) // 2
            digits.append(d)
        return None

    def value(digits: List[int]) -> complex:
        beta = complex(-1, 1)
        return sum(d * beta ** k for k, d in enumerate(digits))

    tested = 0
    ok = True
    seen: Set[Tuple[int, ...]] = set()
    collisions = 0
    for re_ in range(-6, 7):
        for im in range(-6, 7):
            z = complex(re_, im)
            d = expand(z)
            if d is None:
                ok = False
                continue
            back = value(d)
            if abs(back - z) > 1e-6:
                ok = False
            key = tuple(d)
            if key in seen:
                collisions += 1
            seen.add(key)
            tested += 1
    print("   %d Gaussian integers in [-6,6]^2:" % tested)
    print("     every one has a terminating expansion : %s" % ok)
    print("     all round-trip to the original value  : %s" % ok)
    print("     distinct integers, distinct digit strings (collisions=%d): %s"
          % (collisions, collisions == 0))
    print()
    print("   Sample: 5 + 3i -> %s" % expand(complex(5, 3)))
    print("           value  -> %s" % value(expand(complex(5, 3))))
    print()
    print("   THE GENERAL FRAMEWORK the corpus should be citing:")
    print("     * Bratteli-Vershik / adic transformations (Vershik 1981) -")
    print("       THE general theory of numeration with a level-dependent,")
    print("       recursively generated digit structure. Every minimal Cantor")
    print("       system is one. This is 'fractal recursive base' done")
    print("       properly, and it subsumes odometers and substitutions.")
    print("     * Canonical number systems in algebraic number fields")
    print("       (Katai-Szabo 1975; Akiyama) - bases with fractal tiles.")
    print("     * beta-expansions for non-integer beta (Renyi 1957, Parry")
    print("       1960) - see B-14.")
    record("B-13", "PASS" if (ok and collisions == 0) else "FAIL",
           "base (-1+i) with digits {0,1} verified: unique terminating "
           "expansion for %d Gaussian integers; twin-dragon tile dim 2, boundary dim 1.5236"
           % tested)


# ==========================================================================
# B-14. Non-integer bases, and why they matter to Theorem 5.1
# ==========================================================================
def bridge_14() -> None:
    head("B-14", "beta-expansions: Theorem 5.1 is base-dependent")
    print("Paper 1 Theorem 5.1 treats 0.999... + 1_inf = [1] as a deep fact")
    print("about the continuum. It is a fact about BASE 10. In a non-integer")
    print("base the same phenomenon appears with different structure, which")
    print("is worth knowing before the identity is made load-bearing.")
    print()
    phi = (1 + math.sqrt(5)) / 2
    print("   Golden ratio base beta = phi = %.10f" % phi)
    lhs = phi ** -1 + phi ** -2
    print("     phi^-1 + phi^-2 = %.15f    so  1 = 0.11 in base phi" % lhs)
    print("     (exactly, since phi^2 = phi + 1)")
    print()
    # The base-phi analogue of the 0.999... ambiguity.
    tail = sum(phi ** -(2 * k) for k in range(1, 40))     # 0.0101010101...
    print("     0.0101010101... (base phi) = %.15f" % tail)
    print("     phi^-1 = %.15f" % (phi ** -1))
    print("     so 0.11 = 1 AND 0.1011111... = 1 : representations are")
    print("     NON-UNIQUE in base phi, and not by a single tail convention.")
    print()
    print("   Erdos-Joo-Komornik: for 1 < beta < golden ratio, EVERY x in the")
    print("   expansion interval has a CONTINUUM of distinct beta-expansions.")
    print("   Uniqueness of representation is not a property of numeration in")
    print("   general - it is a property of integer bases with a convention.")
    print()
    print("   BEARING ON THE CORPUS. The Active Process identity is offered as")
    print("   an ontological correction to the real continuum. It is better")
    print("   understood as the statement that the digit-stream space is finer")
    print("   than its quotient (orthodox_bridge.py B-4), and the amount of")
    print("   that fineness DEPENDS ON THE BASE - vanishing for base 1, one")
    print("   ambiguous pair per rational for integer bases, and a continuum")
    print("   of representations for beta below the golden ratio. A theory")
    print("   built on booking 'the' residue should say which base it is in.")
    ok = abs(lhs - 1.0) < 1e-12 and abs(tail - phi ** -1) < 1e-9
    record("B-14", "PASS" if ok else "FAIL",
           "base-phi verified 1 = 0.11 with non-unique expansions; Theorem 5.1 "
           "shown base-dependent, not a fact about the continuum")


# ==========================================================================
def main() -> int:
    print("=" * 78)
    print("BASE SYSTEMS - variable, infinite and fractal-recursive bases")
    print("Director's question, answered by execution.")
    print("=" * 78)

    bridge_10()
    bridge_11()
    bridge_12()
    bridge_13()
    bridge_14()

    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    for bid, status, headline in RESULTS:
        print("[%-4s] %-6s %s" % (status, bid, headline))
    npass = sum(1 for _, s, _ in RESULTS if s == "PASS")
    nfail = sum(1 for _, s, _ in RESULTS if s == "FAIL")
    print()
    print("%d passing / %d failing" % (npass, nfail))
    print()
    print("ANSWER TO THE QUESTION:")
    print("  base fn()         -> ALREADY THERE, unnamed. It is Cantor 1869.")
    print("                       Engine computes it; notation cannot write it.")
    print("  base infinite     -> Present only as metaphor. The real object is")
    print("                       Z-hat = prod_p Z_p, and it does NOT fix B-2.")
    print("  fractal recursive -> NOT explored, and it is the best-matched")
    print("                       orthodox field the corpus has not yet used:")
    print("                       Bratteli-Vershik adic numeration.")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
