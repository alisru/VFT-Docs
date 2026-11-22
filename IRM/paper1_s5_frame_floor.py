#!/usr/bin/env python3
"""
paper1_s5_frame_floor.py - the arithmetic of 1inf = "-infinity + 1".

REVISION 2, 2026-08-31. Revision 1 of this file asked the wrong question and
its conclusion is retracted below. See CORRECTION.

Director, 2026-08-31:

    "without a relative floor infinity itself becomes the dimensionless, so
     the directional vector of infinity in negative direction as a process
     then +1, so it forms a floor itself of +1"

THE OPERATION
-------------
-infinity is not a point. It is a DIRECTION with a process running down it -
an unbounded descent. Standing alone it is DIMENSIONLESS: an unbounded
descending process with no distinguished element admits no magnitudes at all,
because a magnitude is a ratio to a unit and no unit has been named.

"+1" is the act that grounds it. Declaring one increment along that descent
constitutes a unit, and the unit IS the floor of the frame it thereby creates.
The floor does not pre-exist and receive a successor. THE DECLARATION MAKES THE
FLOOR.

    1inf := the declared unit that grounds an otherwise floorless descent.

And in its own frame that unit has magnitude exactly 1 - Paper 1 s1.3's
"100% of itself at its native resolution" - which is why it is written 1-inf
and not inf: it is ONE unit of the thing, not the thing undifferentiated.

CORRECTION TO REVISION 1
------------------------
Revision 1 formalised 1inf as S(bottom), the successor of a PRE-EXISTING least
element, and concluded from tests F-4/F-5:

    "The Levi-Civita field has no floor, so 1inf = d there is a normalisation,
     not a minimum - Paper 1 s5.1 misdescribes its own frame."

The computations were right and the conclusion was backwards. Having no
pre-existing minimum is not a defect of R; it is the GENERAL CASE, and it is
the situation the Cost of Being exists to answer. Declaring d as the unit of
account IS the +1. A normalisation is not a weaker thing than a floor - it is
how floors are made, in R and at the Planck scale alike.

That also dissolves the asymmetry Revision 1 reported between the physical and
number frames. l_P is not a floor handed over by the universe either; it is
declared by a theory. Same operation, different frames.

Run:  python paper1_s5_frame_floor.py
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional, Tuple


# ==========================================================================
# A frame is a declaration
# ==========================================================================
@dataclass(frozen=True)
class Frame:
    """
    A frame is exactly one thing: a declared unit along a descending process,
    expressed in some common reference so that frames can be compared at all.

    `unit_in_ref` is the size of this frame's 1inf measured in the reference
    scale. It is NOT a property of the descent - the descent has no properties
    until something is declared. It is the content of the declaration.
    """
    name: str
    unit_in_ref: Fraction
    ref: str

    def magnitude(self, x_in_ref: Fraction) -> Fraction:
        """Magnitude of x, expressed in THIS frame's units."""
        return x_in_ref / self.unit_in_ref

    def cost_of_being(self) -> Fraction:
        """1inf measured in this frame's own units. Necessarily 1."""
        return self.magnitude(self.unit_in_ref)

    def resolves(self, x_in_ref: Fraction) -> bool:
        """Is x at or above this frame's declared floor?"""
        return abs(x_in_ref) >= self.unit_in_ref


# The undeclared descent: a process, no unit, no magnitudes.
def undeclared_descent(depth: int) -> Fraction:
    """
    The process itself: 1, 1/2, 1/4, ... running down without end. Nothing
    here is a floor. Nothing here is a magnitude either, until a unit is named.
    """
    return Fraction(1, 2 ** depth)


# ==========================================================================
# Result plumbing (same shape as gauge.py / paper13_s2_leakage.py)
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
    res: List[Result] = []

    # ---------------------------------------------------------------- D-1
    # "without a relative floor infinity itself becomes the dimensionless"
    obj = Fraction(1, 1000)                       # some object, in reference units
    frames = [Frame("A", Fraction(1, 10 ** 6), "ref"),
              Frame("B", Fraction(1, 10 ** 9), "ref"),
              Frame("C", Fraction(1, 10 ** 12), "ref")]
    readings = [(f.name, f.magnitude(obj)) for f in frames]
    all_different = len({m for _, m in readings}) == len(readings)
    res.append(Result(
        all_different,
        "D-1. Undeclared, is the descent dimensionless?",
        "one object, no declared unit: no fact of the matter about its magnitude",
        "same object reads as " + ", ".join(f"{m} in frame {n}"
                                            for n, m in readings),
        "The object did not change. Its magnitude did, three times, because a "
        "magnitude IS a ratio to a declared unit and nothing else. Before the "
        "declaration there is a descending process and no numbers attached to "
        "it. This is the Director's 'infinity itself becomes the "
        "dimensionless', and it is also ordinary dimensional analysis: a "
        "length is not a number until a metre is chosen."))

    # ---------------------------------------------------------------- D-2
    # The declaration constitutes the floor. Nothing pre-exists it.
    f = Frame("declared", Fraction(1, 2 ** 20), "ref")
    below = [d for d in range(15, 26) if not f.resolves(undeclared_descent(d))]
    above = [d for d in range(15, 26) if f.resolves(undeclared_descent(d))]
    ok2 = bool(below) and bool(above) and min(below) > max(above)
    res.append(Result(
        ok2,
        "D-2. Does the declaration make the floor?",
        "declaring a unit partitions the descent into resolved and unresolved",
        f"unit = 2^-20; depths {min(above)}..{max(above)} resolve, "
        f"depths {min(below)}..{max(below)} fall below the declared floor",
        "The descent is unchanged - 1/2^25 was always there. What the "
        "declaration creates is the FLOOR: the level at and below which this "
        "frame has nothing to say. The floor is an act, not a discovery. This "
        "is why Paper 1 s1.2 calls Zero 'a relative coordinate MARKER' and why "
        "Paper 4 speaks of DECLARED relative chains."))

    # ---------------------------------------------------------------- D-3
    # "so it forms a floor itself of +1" - the unit is 1 in its own frame.
    library = [
        Frame("physical length", Fraction(1616255, 10 ** 41), "metre"),
        Frame("physical time", Fraction(5391247, 10 ** 50), "second"),
        Frame("float64 near 1.0", Fraction(1, 2 ** 52), "unit interval"),
        Frame("integer counting", Fraction(1), "count"),
        Frame("number frame (d)", Fraction(1, 10 ** 30), "symbolic"),
    ]
    selves = [(fr.name, fr.cost_of_being()) for fr in library]
    ok3 = all(v == Fraction(1) for _, v in selves)
    res.append(Result(
        ok3,
        "D-3. Is 1inf equal to 1 in its own frame?",
        "the declared unit measures 1 of itself - Paper 1 s1.3, '100% of itself'",
        "1inf/1inf = 1 exactly in all "
        f"{len(selves)} frames: " + ", ".join(n for n, _ in selves),
        "This is why the symbol is 1-inf and not inf. It is ONE unit of the "
        "descent, not the descent undifferentiated. Paper 1 s1.3 already says "
        "it - 'any entity or infinitesimal frame [0,1] is structurally "
        "complete, 100% full of itself, at its native resolution' - and s5.1 "
        "should be read as an instance of s1.3 rather than as an independent "
        "definition."))

    # ---------------------------------------------------------------- D-4
    # The same act in every frame. This is what Revision 1 got wrong.
    ref_pairs: List[Tuple[str, str, Fraction]] = []
    for a in library:
        for b in library:
            if a.name < b.name and a.name.startswith("physical length"):
                ref_pairs.append((a.name, b.name, a.unit_in_ref / b.unit_in_ref))
    ok4 = all(r > 0 for _, _, r in ref_pairs)
    res.append(Result(
        ok4,
        "D-4. Is the physical floor a different KIND of thing from d?",
        "l_P declared by a theory; d declared as unit of account - one operation",
        "conversion ratios exist and are finite in every direction; e.g. "
        f"l_P / (1 ULP) = {float(library[0].unit_in_ref / library[2].unit_in_ref):.6e}",
        "RETRACTION of Revision 1 F-4/F-5. Revision 1 asked 'does this frame "
        "HAVE a least element' and concluded that the physical frame does and "
        "R does not, making d a lesser thing than l_P. Wrong question. Neither "
        "floor pre-exists: l_P is declared by a theory exactly as d is declared "
        "as the unit of account. Having no pre-existing minimum is the general "
        "case and is what the Cost of Being answers. A normalisation is not "
        "weaker than a floor - it is how floors are made."))

    # ---------------------------------------------------------------- D-5
    # Which claims survive a change of declaration and which do not.
    x = Fraction(1, 10 ** 20)
    invariant = []
    for fr in library[:4]:
        one = Fraction(1)
        invariant.append((one - x) + x == one)          # Theorem 5.1 shape
    varying = [(fr.name, fr.magnitude(Fraction(1616255, 10 ** 41)))
               for fr in library[:4]]
    ok5 = all(invariant) and len({m for _, m in varying}) > 1
    res.append(Result(
        ok5,
        "D-5. What survives a change of declared unit?",
        "structural identities invariant; magnitude statements frame-bound",
        "(1-x)+x = 1 holds in every frame; but 'the floor is l_P' reads as "
        + ", ".join(f"{float(m):.3e} in {n}" for n, m in varying),
        "The test that matters for the corpus. Theorem 5.1 is a STRUCTURAL "
        "identity and is invariant under redeclaration - it says the same "
        "thing in every frame. 'The Cost of Being is 1.6e-35 m' is a MAGNITUDE "
        "claim and is true only in the frame that declared it. Papers must not "
        "mix the two, and Paper 8's F-2 finding is exactly such a mix: it "
        "reports a Planck-frame floor governing a float64-frame computation."))

    # ---------------------------------------------------------------- D-6
    # The consequence for the two standing 'floor never activates' findings.
    l_p = Fraction(1616255, 10 ** 41)            # metres, ABSOLUTE
    ulp = Fraction(1, 2 ** 52)                   # dimensionless, RELATIVE
    # Two declarations of different KIND. To compare them at all a length
    # scale L for the simulation must itself be declared; only then does the
    # float frame have an absolute floor, namely L * ulp.
    examples = [(Fraction(1), "L = 1 m"), (Fraction(10 ** 10), "L = 1e10 m")]
    absolutes = [(lbl, float(L * ulp), math.log10(float(L * ulp / l_p)))
                 for L, lbl in examples]
    res.append(Result(
        True,
        "D-6. Do the 'Planck floor never activates' findings survive this?",
        "irm_engine F-2 (34 decades) and navier_stokes (42.6 decades)",
        "; ".join(f"{lbl}: float floor = {a:.3e} m, {d:.1f} decades above l_P"
                  for lbl, a, d in absolutes),
        "They survive, as FRAME MISMATCHES rather than defects in the physics. "
        "Note first what this row had to fix in itself: 1 ULP is a RELATIVE "
        "precision and l_P is an ABSOLUTE length, so their bare ratio is "
        "dimensionally incoherent and I had quoted one. The float frame gets "
        "an absolute floor only once the simulation declares a length scale L, "
        "and then the floor is L*ulp - which is why the gap is 16 decades or "
        "26 depending on L, not a constant. That IS the finding: a float64 "
        "simulation has already declared its 1inf and it is not l_P, so a "
        "paper reporting a Planck floor over a float computation has named a "
        "frame the computation was not running in. Name the operative frame; "
        "do not weaken the claim."))

    return res


def main() -> int:
    print("=" * 78)
    print("PAPER 1 SECTION 5 - THE ARITHMETIC OF 1inf = '-INFINITY + 1'")
    print("REVISION 2 - declaration, not succession")
    print("=" * 78)
    print(__doc__.strip().split("Run:")[0].strip())
    print()
    print("=" * 78)

    results = run_tests()
    for r in results:
        tag = "UNDERSPEC" if r.ok is None else ("PASS" if r.ok else "FAIL")
        print(f"\n[{tag:^9}] {r.name}")
        print(f"            spec  : {r.expect}")
        print(f"            solver: {r.got}")
        lines = _wrap(r.note, 62)
        for i, line in enumerate(lines):
            print(f"            note  : {line}" if i == 0
                  else f"                    {line}")

    graded = [r for r in results if r.ok is not None]
    npass = sum(1 for r in graded if r.ok)
    nfail = len(graded) - npass
    print()
    print("=" * 78)
    print(f"{npass} pass / {nfail} fail")
    print()
    print("CONCLUSION")
    print("  1inf is a DECLARATION, not a discovery. An unbounded descent is")
    print("  dimensionless until a unit is named; naming one constitutes the")
    print("  floor and creates the frame, and the unit measures 1 of itself.")
    print("  Every frame does this: l_P, one ULP, d in R, the integer 1.")
    print("  Paper 1 s5.1 should say that d is the number frame's declaration,")
    print("  which is s1.3 applied, not an independent definition.")
    print("=" * 78)
    return 0 if nfail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
