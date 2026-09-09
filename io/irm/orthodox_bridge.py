#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
orthodox_bridge.py - The Engineer's independent orthodox-literature bridge,
with the checkable parts actually checked.

WHY THIS EXISTS, AND HOW IT DIFFERS FROM THE ORTHODOX LINKER TREATISE
---------------------------------------------------------------------
The corpus already has an Orthodox Linker Treatise. It is a prose mapping: IRM
concept X "maps to" orthodox result Y. Nothing in it is executed, and at least
one of its pairings is provably incoherent (see B-6 below).

This file is the Engineer's version of the same job. The rule is the role's
usual one: a bridge is PASS only if it was run. Bridges that are genuine
literature claims and cannot be settled by computation are marked
LITERATURE-ONLY and carry no PASS, because an unexecuted citation is not
evidence of anything.

The organising question is the Director's: what is the pathway to ZFC?

Run:  python orthodox_bridge.py
"""
from __future__ import annotations

from fractions import Fraction
from typing import Dict, List, Optional, Tuple

import itertools
import random

RESULTS: List[Tuple[str, str, str]] = []     # (id, status, headline)


def record(bid: str, status: str, headline: str) -> None:
    RESULTS.append((bid, status, headline))


def head(bid: str, title: str) -> None:
    print()
    print("-" * 78)
    print("%s  %s" % (bid, title))
    print("-" * 78)


# ==========================================================================
# B-1. The LCP ultrametric is a genuine ultrametric - and is NOT the n-adic one
# ==========================================================================
def lcp(a: str, b: str) -> int:
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def d_lcp(a: str, b: str) -> float:
    return 0.0 if a == b else 10.0 ** (-lcp(a, b))


def bridge_1() -> None:
    head("B-1", "LCP metric on digit streams -> ultrametric / Baire space")
    print("IRM's d(x,y) = 10^-LCP(x,y) is asserted 'non-Archimedean'. The")
    print("orthodox object is the standard product-topology metric on the")
    print("sequence space D^N (Baire/Cantor space), whose defining property is")
    print("the STRONG triangle inequality d(x,z) <= max(d(x,y), d(y,z)).")
    print()
    rng = random.Random(11)
    worst = 0.0
    trials = 200000
    for _ in range(trials):
        a, b, c = ("".join(rng.choice("0123456789") for _ in range(12))
                   for _ in range(3))
        lhs = d_lcp(a, c)
        rhs = max(d_lcp(a, b), d_lcp(b, c))
        worst = max(worst, lhs - rhs)
    ok = worst <= 0.0
    print("   %d random triples, max violation of d(x,z) - max(...) = %.1e"
          % (trials, worst))
    print()
    print("   IMPORTANT DISTINCTION, and the Orthodox Linker does not draw it:")
    print("   this is NOT the n-adic metric. The LCP metric reads digits from")
    print("   the MOST significant end (agreement of prefixes); the n-adic")
    print("   absolute value reads from the LEAST significant end (divisibility")
    print("   by n^k). They induce different topologies on different objects.")
    print("   Citing Ostrowski or p-adic analysis for the LCP metric is a")
    print("   category error; the correct citation is descriptive set theory")
    print("   (Kechris, Classical Descriptive Set Theory, ch. 2) - and Baire")
    print("   space is a plain ZFC object, constructed with no choice at all.")
    record("B-1", "PASS" if ok else "FAIL",
           "LCP metric verified ultrametric on %d triples; it is Baire space, "
           "not a p-adic completion" % trials)


# ==========================================================================
# B-2. Base 10 is not prime, so Z_10 is not a domain
# ==========================================================================
def bridge_2() -> None:
    head("B-2", "[base_n] with n composite -> Z_n has zero divisors")
    print("If the [base_n.d.e.f...] stream ring is intended as an n-adic ring,")
    print("the choice of n is load-bearing: Z_n is an integral domain iff n is")
    print("prime. Base 10 is the corpus default. Searching for a non-trivial")
    print("idempotent mod 10^k (an element with x^2 = x, x != 0, 1) - which")
    print("exists iff the ring splits, i.e. iff it is NOT a domain.")
    print()
    found = []
    for k in (4, 8, 12, 16):
        m = 10 ** k
        # CRT idempotent: x = 0 mod 2^k, x = 1 mod 5^k
        p, q = 2 ** k, 5 ** k
        x = q * pow(q, -1, p) % m
        assert (x * x - x) % m == 0
        if x not in (0, 1):
            found.append((k, x))
            print("   k=%-3d x = ...%s   x^2 = x (mod 10^%d): %s"
                  % (k, str(x)[-12:], k, (x * x - x) % m == 0))
    y = 10 ** 16 - found[-1][1] + 1 - 1
    a, b = found[-1][1], (10 ** 16 - found[-1][1])
    print()
    print("   Zero divisors follow directly: with a = ...%s and" % str(a)[-8:])
    print("   b = 1 - a = ...%s, a*b = 0 mod 10^16 while a,b != 0."
          % str(b % 10 ** 16)[-8:])
    print("   check a*b mod 10^16 =", (a * (1 - a)) % 10 ** 16)
    print()
    print("   CONSEQUENCE FOR THE CORPUS. Z_10 = Z_2 x Z_5 by CRT. It is a")
    print("   ring, never a field, and it has zero divisors, so no valuation on")
    print("   it is multiplicative and 'non-Archimedean FIELD' language does")
    print("   not apply to base 10. Either fix n prime, or - better, and this")
    print("   is B-3 - stop treating the object as n-adic at all.")
    ok = len(found) == 4 and (a * (1 - a)) % 10 ** 16 == 0
    record("B-2", "PASS" if ok else "FAIL",
           "Z_10 shown to have non-trivial idempotents and zero divisors at "
           "k=4,8,12,16; 'non-Archimedean field' is wrong for base 10")


# ==========================================================================
# B-3. The Levi-Civita field: the correct orthodox home, and ZFC-constructible
# ==========================================================================
class LC:
    """
    Minimal Levi-Civita field element: finite truncation of a formal series
    sum_q a_q * d^q with rational exponents and left-finite support.

    d is the canonical positive infinitesimal. This is a real closed
    non-Archimedean field extension of R (Levi-Civita 1892; Berz 1994 for the
    computational treatment), and - the point for the Director's question - it
    is built inside ZFC by pure construction: no ultrafilter, no choice.
    """

    def __init__(self, terms: Dict[Fraction, Fraction]):
        self.t = {q: c for q, c in terms.items() if c != 0}

    def __add__(self, o: "LC") -> "LC":
        r = dict(self.t)
        for q, c in o.t.items():
            r[q] = r.get(q, Fraction(0)) + c
        return LC(r)

    def __neg__(self) -> "LC":
        return LC({q: -c for q, c in self.t.items()})

    def __sub__(self, o: "LC") -> "LC":
        return self + (-o)

    def __mul__(self, o: "LC") -> "LC":
        r: Dict[Fraction, Fraction] = {}
        for q1, c1 in self.t.items():
            for q2, c2 in o.t.items():
                r[q1 + q2] = r.get(q1 + q2, Fraction(0)) + c1 * c2
        return LC(r)

    def valuation(self) -> Optional[Fraction]:
        return min(self.t) if self.t else None

    def inverse(self, order: int = 6) -> "LC":
        """1/x by geometric series on the leading term. Requires x != 0."""
        v = self.valuation()
        assert v is not None, "no inverse of zero"
        a0 = self.t[v]
        # x = a0 d^v (1 + u), so 1/x = a0^-1 d^-v (1 - u + u^2 - ...)
        u = LC({q - v: c / a0 for q, c in self.t.items() if q != v})
        acc = LC({Fraction(0): Fraction(1)})
        term = LC({Fraction(0): Fraction(1)})
        for _ in range(order):
            term = term * (-u)
            acc = acc + term
        return LC({Fraction(0): 1 / a0}) * LC({-v: Fraction(1)}) * acc

    def __repr__(self) -> str:
        if not self.t:
            return "0"
        parts = []
        for q in sorted(self.t):
            c = self.t[q]
            parts.append("%s*d^%s" % (c, q) if q != 0 else "%s" % c)
        return " + ".join(parts)

    def __eq__(self, o) -> bool:
        return self.t == o.t


def R(x) -> LC:
    return LC({Fraction(0): Fraction(x)})


D = LC({Fraction(1): Fraction(1)})          # the canonical infinitesimal


def bridge_3() -> None:
    head("B-3", "[base_n.d.e.f...] with 1_inf -> the Levi-Civita field")
    print("Claim under test: IRM's number atom, a standard part plus a booked")
    print("infinitesimal residue, is an element of the Levi-Civita field with")
    print("1_inf = d. If so, IRM's arithmetic is not new mathematics - it is a")
    print("computable non-Archimedean field that has existed since 1892.")
    print()
    checks = []

    # (i) The corpus identity 0.999... + 1_inf = [1].
    lhs = (R(1) - D) + D
    checks.append(("0.999... + 1_inf = [1]", lhs == R(1), repr(lhs)))

    # (ii) d is NOT nilpotent - this is what forces the NSA side, not SIA.
    d2 = D * D
    checks.append(("d^2 != 0 (not nilpotent)", d2 != LC({}), repr(d2)))

    # (iii) d is invertible, and 1/d is infinite (valuation -1).
    dinv = D.inverse()
    checks.append(("1/d exists, valuation -1",
                   dinv.valuation() == Fraction(-1), repr(dinv)))
    checks.append(("d * (1/d) = 1", (D * dinv) == R(1), repr(D * dinv)))

    # (iv) Field arithmetic on a mixed element, exactly.
    x = R(3) + R(2) * D - R(5) * (D * D)
    xi = x.inverse(order=8)
    prod = x * xi
    lead_ok = prod.t.get(Fraction(0)) == Fraction(1)
    tail = {q: c for q, c in prod.t.items() if q != 0 and q <= 4}
    checks.append(("x * x^-1 = 1 to order d^4", lead_ok and not tail,
                   repr(LC({q: c for q, c in prod.t.items() if q <= 4}))))

    # (v) Ultrametric valuation is non-Archimedean: v(a+b) >= min(v(a),v(b))
    rng = random.Random(5)
    worst = None
    for _ in range(2000):
        a = LC({Fraction(rng.randint(0, 3)): Fraction(rng.randint(1, 9))})
        b = LC({Fraction(rng.randint(0, 3)): Fraction(rng.randint(-9, -1))})
        s = a + b
        if s.t:
            gap = s.valuation() - min(a.valuation(), b.valuation())
            worst = gap if worst is None else min(worst, gap)
    checks.append(("v(a+b) >= min(v a, v b) over 2000 pairs",
                   worst is not None and worst >= 0, "min gap = %s" % worst))

    allok = True
    for name, ok, detail in checks:
        print("   [%s] %-38s %s" % ("PASS" if ok else "FAIL", name, detail))
        allok = allok and ok
    print()
    print("   THE ZFC PATHWAY, and it is short. The Levi-Civita field is the")
    print("   set of functions Q -> R with left-finite support. That is a")
    print("   subset of R^Q, which is a set by Power Set and Replacement. No")
    print("   ultrafilter, no ultraproduct, no choice. So IRM's number system,")
    print("   under this identification, is an ordinary ZFC-definable object.")
    record("B-3", "PASS" if allok else "FAIL",
           "IRM number atom embeds in the Levi-Civita field; d invertible and "
           "non-nilpotent; ZFC-constructible with no choice")


# ==========================================================================
# B-4. The pre-quotient bridge: why 0.999... = 1 and 0.999... + 1_inf = [1]
#      are both true, of different objects
# ==========================================================================
def bridge_4() -> None:
    head("B-4", "0.999... = 1 in R vs 0.999... + 1_inf = [1] in IRM")
    print("The archived 'Superiority over ZFC' document treats these as rival")
    print("claims. They are not. They are claims about two different objects,")
    print("and BOTH objects live in ZFC.")
    print()
    print("   In ZFC, R is built from Cauchy sequences of rationals MODULO the")
    print("   equivalence 'difference tends to 0'. The digit-stream space D^N")
    print("   is the pre-quotient object; R is the quotient. The quotient map")
    print("   pi : D^N -> R is surjective and NOT injective.")
    print()
    a = "0" + "9" * 40          # 0.999...
    b = "1" + "0" * 40          # 1.000...
    va = sum(Fraction(int(ch), 10 ** (i + 1)) for i, ch in enumerate(a))
    vb = sum(Fraction(int(ch), 10 ** (i + 1)) for i, ch in enumerate(b))
    gap = vb - va
    print("   truncating both streams at 40 digits:")
    print("     pi(0.999...) = %s" % va)
    print("     pi(1.000...) = %s" % vb)
    print("     difference   = %s  ~ %.3e" % (gap, float(gap)))
    print("   The difference is non-zero at EVERY finite truncation and its")
    print("   limit is 0, which is exactly the statement that the two streams")
    print("   are distinct points of D^N identified by pi.")
    print()
    print("   So: IRM refuses to apply pi and keeps the residue as a booked")
    print("   quantity. That is a legitimate and orthodox move - it is the")
    print("   same move Levi-Civita series make - but it is NOT a defeat of")
    print("   the real numbers, and it is not independent of ZFC. It is a")
    print("   finer object DEFINED INSIDE ZFC, mapping onto R by a quotient")
    print("   that IRM declines to take.")
    print()
    print("   RECOMMENDATION. 'Computational and Ontological Superiority of IRM")
    print("   over ZFC' cannot be defended as written: a structure definable")
    print("   inside ZFC cannot exceed ZFC's consistency strength, and every")
    print("   theorem IRM proves about its atoms is a ZFC theorem about the")
    print("   corresponding element of R^Q. Reframe as 'IRM as a pre-quotient")
    print("   refinement of the real line' and the content survives intact.")
    ok = gap > 0 and float(gap) < 1e-30
    record("B-4", "PASS" if ok else "FAIL",
           "streams shown distinct pre-quotient with vanishing image gap; "
           "'superiority over ZFC' is not defensible, 'pre-quotient' is")


# ==========================================================================
# B-5. Confluence: Newman's Lemma, mechanically checked on a small system
# ==========================================================================
def bridge_5() -> None:
    head("B-5", "Propagation Operator confluence -> Newman's Lemma")
    print("The corpus claims Church-Rosser for the Propagation Operator. The")
    print("orthodox route is Newman's Lemma: terminating + locally confluent")
    print("=> confluent. Both hypotheses are decidable on a finite system, so")
    print("this is checkable rather than assertable.")
    print()

    def step(s: Tuple[int, ...]) -> List[Tuple[int, ...]]:
        """Cascade: any digit >= 10 carries one unit leftward."""
        out = []
        for i, v in enumerate(s):
            if v >= 10:
                t = list(s)
                t[i] -= 10
                if i == 0:
                    t = [1] + t
                else:
                    t[i - 1] += 1
                out.append(tuple(t))
        return out

    def normal_forms(s: Tuple[int, ...]) -> set:
        seen, stack, nf = set(), [s], set()
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            nxt = step(cur)
            if not nxt:
                nf.add(cur)
            stack.extend(nxt)
        return nf

    rng = random.Random(2)
    cases = []
    for _ in range(4000):
        s = tuple(rng.randint(0, 19) for _ in range(rng.randint(2, 5)))
        cases.append(s)

    unique = 0
    terminating = True
    for s in cases:
        nf = normal_forms(s)
        if len(nf) == 1:
            unique += 1
        # value preservation: cascade conserves the represented integer
        def val(t):
            return sum(v * 10 ** (len(t) - 1 - i) for i, v in enumerate(t))
        for f in nf:
            if val(f) != val(s):
                terminating = False
    ok = unique == len(cases) and terminating
    print("   %d random digit vectors, each reduced by every available route:"
          % len(cases))
    print("     unique normal form in %d / %d cases" % (unique, len(cases)))
    print("     represented value conserved on every route: %s" % terminating)
    print()
    print("   This is a genuine confluence check, not a citation: the search")
    print("   explores ALL reduction orders, so a divergent pair would show up")
    print("   as a second normal form. Orthodox home: Newman (1942); Baader &")
    print("   Nipkow, Term Rewriting and All That, ch. 2. Plain ZFC.")
    record("B-5", "PASS" if ok else "FAIL",
           "cascade confluent and value-preserving on %d cases by exhaustive "
           "route search (Newman's Lemma hypotheses)" % len(cases))


# ==========================================================================
# B-6. The incompatibility the Orthodox Linker Treatise missed
# ==========================================================================
def bridge_6() -> None:
    head("B-6", "Robinson NSA and Lawvere-Kock SIA cannot both be the home")
    print("The Orthodox Linker Treatise cites BOTH Robinson's Non-Standard")
    print("Analysis AND Lawvere-Kock Smooth Infinitesimal Analysis as the")
    print("grounding for IRM's infinitesimal. Those two are incompatible, and")
    print("the incompatibility is a two-line argument.")
    print()
    print("   In SIA every infinitesimal is NILSQUARE: d^2 = 0.")
    print("   In NSA every non-zero infinitesimal is INVERTIBLE.")
    print("   Suppose both of an infinitesimal d != 0:")
    print("       d = d * 1 = d * (d * d^-1) = (d * d) * d^-1 = 0 * d^-1 = 0")
    print("   contradicting d != 0. So no non-zero element is both.")
    print()
    # Mechanical check of the same argument in the LC field.
    d2 = D * D
    nilsquare = (d2 == LC({}))
    invertible = (D * D.inverse()) == R(1)
    print("   Mechanically, in the Levi-Civita model used at B-3:")
    print("     d^2 == 0 ?      %s   (d^2 = %s)" % (nilsquare, d2))
    print("     d invertible ?  %s   (d * 1/d = %s)" % (invertible, D * D.inverse()))
    print()
    print("   IRM's 1_inf appears in DENOMINATORS throughout the corpus - the")
    print("   Cost of Being floor divides by it, and Paper 10's inner product")
    print("   has exp(-d_R/1_inf). That requires invertibility. Therefore IRM")
    print("   is on the NSA / Levi-Civita side, and the SIA citation is wrong")
    print("   and must be removed. SIA also requires INTUITIONISTIC logic,")
    print("   where excluded middle fails - while the corpus uses proof by")
    print("   contradiction freely, including in Paper 9 Theorem 1.1.")
    ok = (not nilsquare) and invertible
    record("B-6", "PASS" if ok else "FAIL",
           "NSA and SIA shown mutually exclusive; IRM's use of 1_inf in "
           "denominators forces the NSA side, so the SIA citation is an error")


# ==========================================================================
# B-7 .. B-9  Literature-only: stated, not executed
# ==========================================================================
def bridge_literature() -> None:
    head("B-7..B-9", "Literature-only bridges (NOT executed, NOT evidence)")
    items = [
        ("B-7", "Hyperreals *R require a non-principal ultrafilter on N, whose "
                "existence is not provable in ZF - it needs the Boolean Prime "
                "Ideal theorem, a strict fragment of AC. So IF IRM's "
                "infinitesimals are hyperreal, IRM inherits a choice "
                "dependence. The Levi-Civita reading at B-3 does NOT. That is "
                "a reason to prefer it. (Robinson 1966; Jech, The Axiom of "
                "Choice, ch. 2.)"),
        ("B-8", "Final coalgebras for bounded endofunctors exist in ZFC "
                "(Aczel-Mendler 1989); stream calculus and bisimulation as "
                "proof principle are Rutten (2000). The corpus's coalgebraic "
                "layer is therefore orthodox and ZFC-internal. Anti-Foundation "
                "(Aczel 1988) is NOT required for streams - it is required "
                "only for genuinely non-well-founded SETS, which the corpus "
                "does not appear to use. If it does not, AFA should not be "
                "cited."),
        ("B-9", "Conway's surreals No form a PROPER CLASS, not a set. Any "
                "claim that IRM numbers are 'surreal-like in generality' "
                "leaves ZFC set-hood and needs NBG with global choice to state "
                "properly. The Levi-Civita field is a set and suffices for "
                "everything the corpus actually computes, so this is a "
                "citation to drop rather than to formalise. (Conway 1976; "
                "Ehrlich 2012 on the class-sized picture.)"),
    ]
    for bid, text in items:
        print()
        print("   %s. %s" % (bid, text.replace("\n", " ")))
        record(bid, "LIT", text.split(".")[0][:96])


# ==========================================================================
def main() -> int:
    print("=" * 78)
    print("ORTHODOX BRIDGE - The Engineer's independent linkage, with the")
    print("checkable parts checked. Director's question: pathway to ZFC.")
    print("=" * 78)

    bridge_1()
    bridge_2()
    bridge_3()
    bridge_4()
    bridge_5()
    bridge_6()
    bridge_literature()

    print()
    print("=" * 78)
    print("SUMMARY")
    print("=" * 78)
    npass = sum(1 for _, s, _ in RESULTS if s == "PASS")
    nfail = sum(1 for _, s, _ in RESULTS if s == "FAIL")
    nlit = sum(1 for _, s, _ in RESULTS if s == "LIT")
    for bid, status, headline in RESULTS:
        print("[%-4s] %-6s %s" % (status, bid, headline))
    print()
    print("%d executed and passing / %d failing / %d literature-only"
          % (npass, nfail, nlit))
    print()
    print("THE PATHWAY TO ZFC, IN ONE LINE:")
    print("  IRM number atom  ->  Levi-Civita field  ->  functions Q -> R with")
    print("  left-finite support  ->  a subset of R^Q  ->  a ZFC set by Power")
    print("  Set + Replacement, with NO use of choice.")
    print()
    print("  Everything else follows: the ultrametric is Baire space (B-1),")
    print("  confluence is Newman (B-5), the coalgebra is Aczel-Mendler (B-8).")
    print("  The corpus is not an alternative foundation. It is a family of")
    print("  ordinary ZFC objects with an unusual and defensible refusal to")
    print("  take one quotient (B-4).")
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
