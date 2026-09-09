#!/usr/bin/env python3
"""
eng3_decay.py - exact rational arithmetic vs IEEE 754 in asymptotic decay.
(Directive ENG-3.)

Formal Paper 8 s2.2 claims floating-point registers "discard infinitesimal
residuals", causing "energy annihilation" during continuous asymptotic decay,
and that the Propagation Operator prevents it. This measures the claim.

Two ledgers, because they have very different answers and the difference is
the whole result:

  A. CLOSED DECAY. Energy moves from `remaining` into `accumulated`, nothing
     enters or leaves. Invariant: accumulated + remaining == 1, always.

  B. DRIVEN ACCUMULATION. A small quantity is added repeatedly to a large
     accumulator from outside. Invariant: total == base + n * quantum.

METHODOLOGICAL NOTE. The first version of this file hardcoded a verdict string
asserting that float destroys energy, and printed it regardless of the measured
defect - which was zero. That is precisely the failure mode logged against the
PM document in CLAUDE_LOG Entry 002 s4: a conclusion written before the
evidence and not revised by it. The verdict below is now COMPUTED from the
measured defects. Kept in the record deliberately; see Entry 004 s4.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional, Tuple


# ==========================================================================
# Ledger A: closed decay
# ==========================================================================
@dataclass
class DecayResult:
    label: str
    rate: str
    steps: int
    total: float
    defect: float
    relative_defect: float
    first_drop_step: Optional[int]
    first_drop_remaining: Optional[float]
    seconds: float


def decay_float(q: float, steps: int) -> DecayResult:
    t0 = time.perf_counter()
    remaining, accumulated = 1.0, 0.0
    first_step: Optional[int] = None
    first_rem: Optional[float] = None
    for i in range(steps):
        delta = remaining * q
        before = accumulated
        accumulated = accumulated + delta
        remaining = remaining - delta
        if first_step is None and delta != 0.0 and accumulated == before:
            first_step, first_rem = i, remaining
    total = accumulated + remaining
    d = abs(total - 1.0)
    return DecayResult("IEEE 754 float", f"q={q}", steps, total, d, d,
                       first_step, first_rem, time.perf_counter() - t0)


def decay_fraction(q: Fraction, steps: int) -> DecayResult:
    t0 = time.perf_counter()
    remaining, accumulated = Fraction(1), Fraction(0)
    for _ in range(steps):
        delta = remaining * q
        accumulated += delta
        remaining -= delta
    total = accumulated + remaining
    d = float(abs(total - 1))
    return DecayResult("fractions.Fraction", f"q={q}", steps, float(total), d,
                       d, None, None, time.perf_counter() - t0)


# ==========================================================================
# Ledger B: driven accumulation
# ==========================================================================
@dataclass
class DrivenResult:
    label: str
    base: float
    quantum: float
    n: int
    expected_gain: float
    measured_gain: float
    fraction_lost: float
    seconds: float


def driven_float(base: float, quantum: float, n: int) -> DrivenResult:
    t0 = time.perf_counter()
    acc = base
    for _ in range(n):
        acc = acc + quantum
    gain = acc - base
    expected = quantum * n
    lost = 1.0 - (gain / expected) if expected else 0.0
    return DrivenResult("IEEE 754 float", base, quantum, n, expected, gain,
                        lost, time.perf_counter() - t0)


def driven_fraction(base: Fraction, quantum: Fraction, n: int) -> DrivenResult:
    t0 = time.perf_counter()
    acc = base
    for _ in range(n):
        acc = acc + quantum
    gain = acc - base
    expected = quantum * n
    lost = float(1 - (gain / expected)) if expected else 0.0
    return DrivenResult("fractions.Fraction", float(base), float(quantum), n,
                        float(expected), float(gain), lost,
                        time.perf_counter() - t0)


def underflow_scales() -> Tuple[float, float]:
    acc, tiny = 1.0, 1.0
    while acc + tiny != acc:
        tiny /= 2.0
    v = 1.0
    while v / 2.0 != 0.0:
        v /= 2.0
    return tiny, v


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
    width = 78
    print("=" * width)
    print("ENG-3: EXACT RATIONAL vs IEEE 754 IN ASYMPTOTIC DECAY")
    print("=" * width)

    rel, absolute = underflow_scales()
    gap = abs(math.log10(rel) - math.log10(absolute))
    print(f"\nrelative underflow  (1 + x == 1)  : {rel:.3e}")
    print(f"absolute underflow  (x/2 == 0)    : {absolute:.3e}")
    print(f"gap                               : {gap:.0f} decades\n")

    # ---- Ledger A -------------------------------------------------------
    print("-" * width)
    print("A. CLOSED DECAY - accumulated + remaining must equal 1")
    print("-" * width)
    print(f"{'arithmetic':<20} {'rate':>8} {'steps':>7} {'defect':>12} {'sec':>7}")
    decay_rows: List[DecayResult] = []
    for q_f, q_r in ((0.5, Fraction(1, 2)), (0.1, Fraction(1, 10))):
        for steps in (2000,):
            rf = decay_float(q_f, steps)
            rq = decay_fraction(q_r, steps)
            decay_rows.append(rf)
            for r in (rf, rq):
                print(f"{r.label:<20} {r.rate:>8} {r.steps:>7} "
                      f"{r.defect:>12.3e} {r.seconds:>7.3f}")
    print()
    for r in decay_rows:
        if r.first_drop_step is not None:
            print(f"  {r.rate}: first silently dropped residual at step "
                  f"{r.first_drop_step}, remaining = {r.first_drop_remaining:.3e}")

    # ---- Ledger B -------------------------------------------------------
    print("\n" + "-" * width)
    print("B. DRIVEN ACCUMULATION - add a quantum to a large accumulator n times")
    print("-" * width)
    print(f"{'arithmetic':<20} {'quantum':>10} {'n':>9} {'expected':>12} "
          f"{'measured':>12} {'lost':>8}")
    driven_rows: List[DrivenResult] = []
    for quantum, n in ((1e-18, 200000), (1e-12, 200000)):
        df = driven_float(1.0, quantum, n)
        dq = driven_fraction(Fraction(1), Fraction(quantum), n)
        driven_rows.append(df)
        for r in (df, dq):
            print(f"{r.label:<20} {r.quantum:>10.0e} {r.n:>9} "
                  f"{r.expected_gain:>12.4e} {r.measured_gain:>12.4e} "
                  f"{r.fraction_lost * 100:>7.1f}%")
        print()

    # ---- Verdict, computed from the measurements ------------------------
    print("=" * width)
    print("VERDICT (computed from the rows above, not asserted)")
    print("=" * width)

    worst_decay = max(r.relative_defect for r in decay_rows)
    worst_driven = max(r.fraction_lost for r in driven_rows)
    dropped_anywhere = any(r.first_drop_step is not None for r in decay_rows)

    lines: List[str] = []
    if worst_decay > 1e-12:
        lines.append(
            f"CLOSED DECAY: float loses {worst_decay:.2e} relative. The claim "
            f"holds here.")
    elif dropped_anywhere:
        lines.append(
            f"CLOSED DECAY: float DOES silently drop residuals, but the ledger "
            f"defect is only {worst_decay:.2e}. The dropped residual is taken "
            f"from energy that is itself already ~1e-16 of the total, so the "
            f"loss is bounded by machine epsilon. Paper 8's 'energy "
            f"annihilation' is real in mechanism but negligible in magnitude "
            f"for a closed decay - it is not the catastrophe the abstract "
            f"implies.")
    else:
        lines.append(
            "CLOSED DECAY: no measurable loss. For dyadic rates the halving is "
            "exact in binary and nothing is destroyed at all.")

    if worst_driven > 0.5:
        lines.append(
            f"DRIVEN ACCUMULATION: float loses {worst_driven * 100:.1f}% of the "
            f"injected quantity - total annihilation of the input. THIS is "
            f"where Paper 8's claim bites, and it is a real and serious effect: "
            f"a decay model with an external source term will silently discard "
            f"the entire source once the quantum falls below eps times the "
            f"accumulator. Exact rationals lose nothing.")
    else:
        lines.append(
            f"DRIVEN ACCUMULATION: float loses {worst_driven * 100:.1f}%.")

    lines.append(
        "SCALE. Loss begins at RELATIVE underflow, ~1e-16 of the accumulator, "
        f"not at the {absolute:.0e} denormal floor - {gap:.0f} decades apart. "
        "Same structural point as finding F-2: the Cost of Being floor is "
        "calibrated to where representation ends, while arithmetic fails where "
        "PRECISION ends. A floor at the Planck scale does not protect against "
        "a failure at machine epsilon.")

    slow = [r for r in (decay_fraction(Fraction(1, 10), 2000),)]
    lines.append(
        f"COST. Exactness is not free: Fraction denominators grow without "
        f"bound, so per-step cost rises through the run ({slow[0].seconds:.2f} s "
        f"for 2000 steps against ~0.00 s for float). That is the honest price, "
        f"and it is why the engine uses exact rationals in the number system "
        f"and floats in the physics.")

    for i, block in enumerate(lines):
        for line in _wrap(block, width):
            print(line)
        if i < len(lines) - 1:
            print()
    print("=" * width)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
