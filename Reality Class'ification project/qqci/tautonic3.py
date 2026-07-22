"""
Tautonic decomposition v3: ordered TRIGRAMS into Q.q.c cells.

WHY v3 EXISTS
-------------
v1 (tautonic.py) summed per-character contributions into 7 plane scores. It was
measured on 14,258 corpus word types and failed:

    information retention  0.0163   (233 distinct vectors for 14,258 words)
    anagram collapse       100%     (vector == covert, who == how, time == emit)
    dead planes            CAUSE flat at 1.00 for every single word

A bag of characters cannot be an identity, and the string IS the Who, so
throwing away order threw away the thing the design says is primary.

WHAT CHANGED
------------
An ordered n-gram of characters maps to a Qqci CELL: the first character names
the plane, the second the sub-plane, the third the sub-sub-plane. So a trigram
IS a Q.q.c address, and a word is the multiset of addresses its trigrams visit.
The bigram is the Qq drill; the trigram is the full 7x7x7.

MEASURED, same corpus, retention and morphological-family separation:

    n   cells  retention  within-family  across-family   gap
    1       7     0.0841          0.869          0.540  +0.329
    2      49     0.8071          0.747          0.179  +0.567
    3     343     0.8712          0.670          0.042  +0.628   <- peak
    4    2401     0.8602          0.613          0.009  +0.604

Both metrics peak at 3 and DECLINE at 4, so there is a genuine optimum and it
sits at 7x7x7. Retention alone would be a trap (a hash scores 1.0 and means
nothing); the gap metric is what makes the peak meaningful.

HONEST LIMITS
-------------
One corpus, and it is the user's own. The character-to-plane map is a
26-entry authored table, so the result is not independent of that choice.
Shared-prefix is a crude proxy for semantic relatedness. The 3-vs-2 margin is
modest; the strong evidence is the decline at 4.

THE DECISIVE NEGATIVE RESULT
----------------------------
v3 fixes what v1 broke (anagram collapse 100% -> 0%, retention 0.016 -> 0.871)
and is still NOT USABLE AS A SEMANTIC ANCHOR SET. Measured on the retelling:

    derived vectors, sea -> startup   0/9
    derived vectors, sea -> orbit     2/9
    (hand-authored VFT scores scored 9/9 and 9/9)

    mean cosine, same functional type   0.106
    mean cosine, different type         0.064
    separation gap                     +0.042

A gap of 0.04 is noise. Spelling does not track meaning, and it was never
going to: 'storm' and 'recession' are the same functional object and share no
letters, while 'storm' and 'stormy' share nearly all of them but so do
'storm' and 'store'.

WHAT THIS ACTUALLY MEASURES
---------------------------
The 0.871 retention and the +0.628 family gap are real, but they measure
ORTHOGRAPHIC structure, not semantics. The morphological-family test rewarded
exactly that, because shared 5-character prefixes ARE spelling. The test was
circular and the earlier report of it overstated what it showed.

So the trigram layer is a good WORD-FORM signature -- order-sensitive,
sparse, collision-resistant, cheap -- and belongs at L2 as identity structure.
It is not a source of plane scores. Those need either the corpus distribution
(what a word co-occurs with) or the NSM base-plus-modifier layer that
core_dictionary.md already specifies. The character tensor alone cannot carry
it, and any anchor term built on v3 would pin the axes to spelling.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from qqci_engine import Plane, QqciAddress, TensorRank
from tautonic import (
    ANCHOR_PLANE, CHAR_TENSOR, Encapsulation, POLARITY_PUSH, SPECTRUM,
)
from vft import FieldMath, MoralVectors

Cell = Tuple[int, ...]          # (plane, sub, subsub) as 1-based plane numbers

PLANE_BY_NUM = {int(p): p for p in Plane}
VECTOR_BY_PLANE = {
    Plane.WHO: MoralVectors.WHO, Plane.WHAT: MoralVectors.WHAT,
    Plane.WHERE: MoralVectors.WHERE, Plane.WHY: MoralVectors.WHY,
    Plane.HOW: MoralVectors.HOW, Plane.CAUSE: MoralVectors.CAUSE,
    Plane.EFFECT: MoralVectors.EFFECT,
}


def cell_address(cell: Cell) -> str:
    head = f"Q{cell[0]}"
    return head + "".join(f".q{c}" for c in cell[1:])


def cell_name(cell: Cell) -> str:
    names = [VECTOR_BY_PLANE[PLANE_BY_NUM[c]].interrogative for c in cell]
    return " of ".join(reversed(names))


@dataclass
class Tautonic3:
    """
    A word is its string (Q1 identity) plus the Q.q.c cells its trigrams visit.
    Sparse by construction: a word of length L populates at most L-2 of 343.
    """
    string: str
    cells: Dict[Cell, int] = field(default_factory=dict)
    encapsulation: Dict[str, int] = field(default_factory=dict)
    unknown_chars: int = 0

    # --- the sparse 343 reading ---
    @property
    def occupancy(self) -> int:
        return len(self.cells)

    def top_cells(self, k: int = 5) -> List[Tuple[Cell, int]]:
        return sorted(self.cells.items(), key=lambda kv: (-abs(kv[1]), kv[0]))[:k]

    # --- collapse to 7 planes when a dense vector is needed ---
    @property
    def scores(self) -> Dict[Plane, float]:
        """
        Marginalise the 343 cells onto the six paired planes by their ROOT
        (the cell's first coordinate). Q1 is excluded: the string is the Who.
        """
        steps: Dict[Plane, int] = {}
        for cell, v in self.cells.items():
            p = PLANE_BY_NUM[cell[0]]
            if p == Plane.WHO:
                continue
            steps[p] = steps.get(p, 0) + v
        out = {}
        for p in Plane:
            if p == Plane.WHO:
                continue
            n = max(-3, min(3, steps.get(p, 0)))
            out[p] = SPECTRUM[n]
        return out

    @property
    def scope(self) -> str:
        if not self.encapsulation:
            return Encapsulation.SINGULAR
        return max(self.encapsulation.items(), key=lambda kv: kv[1])[0]

    @property
    def address(self) -> QqciAddress:
        """Q1-rooted; the leaf is the root plane of the strongest cell."""
        if not self.cells:
            return QqciAddress.of(Plane.WHO)
        top = self.top_cells(1)[0][0]
        return QqciAddress.of(Plane.WHO, PLANE_BY_NUM[top[0]])

    def r_net(self) -> float:
        return FieldMath.fractal_ratio(list(self.scores.values()))

    # --- comparison over the sparse cells ---
    def cosine(self, other: "Tautonic3") -> float:
        shared = set(self.cells) & set(other.cells)
        if not self.cells or not other.cells:
            return 0.0
        dot = sum(self.cells[c] * other.cells[c] for c in shared)
        na = math.sqrt(sum(v * v for v in self.cells.values()))
        nb = math.sqrt(sum(v * v for v in other.cells.values()))
        if na == 0 or nb == 0:
            return 1.0 if set(self.cells) == set(other.cells) else 0.0
        return dot / (na * nb)

    def report(self) -> str:
        lines = [f"  '{self.string}'   Q1 identity = the string",
                 f"  scope {self.scope}   occupancy {self.occupancy}/343 cells"
                 f"   address {self.address}   R_net {self.r_net():.4f}"]
        lines.append("  strongest Q.q.c cells:")
        for cell, v in self.top_cells(5):
            lines.append(f"    {cell_address(cell):<12}{v:+3d}  {cell_name(cell)}")
        lines.append("  marginalised paired-plane scores:")
        for p, sc in sorted(self.scores.items()):
            v = VECTOR_BY_PLANE[p]
            tag = (v.virtue if abs(sc - 1.0) < 1e-9
                   else f"{'Excess' if sc > 1 else 'Deficit'}: {v.sin}")
            lines.append(f"    {v.interrogative:<7}{sc:5.2f}  {tag}")
        return "\n".join(lines)


def decompose3(string: str, n: int = 3) -> Tautonic3:
    """
    Ordered n-grams to Qqci cells. n=3 gives the full 7x7x7; n is exposed only
    so the depth sweep can be reproduced, not because other values are correct.
    """
    w = Tautonic3(string=string)
    s = string.lower()
    for ch in s:
        ct = CHAR_TENSOR.get(ch)
        if ct is None:
            w.unknown_chars += 1
        else:
            w.encapsulation[ct.encapsulation] = (
                w.encapsulation.get(ct.encapsulation, 0) + 1)
    for i in range(len(s) - n + 1):
        gram = s[i:i + n]
        if not all(c in CHAR_TENSOR for c in gram):
            continue
        cell: Cell = tuple(int(ANCHOR_PLANE[c][0]) for c in gram)
        push = sum(POLARITY_PUSH[CHAR_TENSOR[c].polarity] for c in gram)
        w.cells[cell] = w.cells.get(cell, 0) + push
    return w


def nearest(word: str, vocabulary: List[str], k: int = 5
            ) -> List[Tuple[str, float]]:
    a = decompose3(word)
    scored = [(v, a.cosine(decompose3(v))) for v in vocabulary if v != word]
    scored.sort(key=lambda kv: -kv[1])
    return scored[:k]


if __name__ == "__main__":
    print("=" * 72)
    print("TAUTONIC v3: ordered trigrams into the 7x7x7")
    print("=" * 72)
    for word in ("house", "home", "storm", "boat", "fisherman"):
        print()
        print(decompose3(word).report())

    print()
    print("=" * 72)
    print("ANAGRAM CHECK (v1 collapsed 100% of these)")
    for a, b in [("vector", "covert"), ("state", "taste"), ("who", "how"),
                 ("time", "emit"), ("listen", "silent")]:
        x, y = decompose3(a), decompose3(b)
        same = (x.cells == y.cells)
        print(f"  {a:<8} vs {b:<8} identical={same!s:<5} "
              f"cosine={x.cosine(y):.3f}")
