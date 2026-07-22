"""
The Tautonic layer: a word's STRING is its Q1 identity, and decomposing that
string through the character tensor yields the other six planes.

SOURCE
------
_VFT MD/Actualism/Language/translating/Tautonic_Semantic_Dictionary_Full.md
    the character tensor: each char -> Greek anchor, Polarity, Encapsulation
_VFT MD/Actualism/Language/translating/nsm_reduction/core_dictionary.md
    the language rules: the ---word+++ spectrum, seven steps around the default

Neither was authored here. Both already existed in the corpus.

THE STRUCTURE
-------------
Q1 (Who) is the Driver, the unpaired 7th-angle axis, Will and Direction. A
word's identity is not a score on Q1 -- it IS the string. The string is the
address; the graph is what the string decomposes into.

The six paired planes (Q2..Q7) take their scores from the characters:

    Greek anchor  ->  WHICH plane the character speaks on
    Polarity      ->  WHICH DIRECTION it pushes that plane off Unity
                      Positive -> Excess, Negative -> Deficit,
                      Neutral -> no push, Mixed -> both (widens, no net)
    Encapsulation ->  the noun-structure axis: Singular, Plural, Class,
                      Totality. This is scope, not score, and it is why a
                      noun is not a claim.

The ---word+++ spectrum supplies the quantisation, so scores land on a
principled seven-step ladder instead of arbitrary decimals:

    ---    --     -    word     +     ++    +++
    0.40  0.60  0.80   1.00   1.20  1.40  1.60

HONEST NOTE
-----------
One table IS authored here: the map from the 26 Greek anchors to planes
(ANCHOR_PLANE below). That is 26 arguable decisions made once and visible,
rather than seven arguable decisions per word made invisibly. Every entry
carries its reasoning. If an entry is wrong, one edit fixes every word that
uses that letter.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from qqci_engine import Plane, QqciAddress, TensorRank
from vft import FieldMath, Idea, Judgement, MoralVectors

# --- the ---word+++ ladder, from core_dictionary.md Part I ---
SPECTRUM = {-3: 0.40, -2: 0.60, -1: 0.80, 0: 1.00, 1: 1.20, 2: 1.40, 3: 1.60}
STEP = 0.20


class Encapsulation:
    SINGULAR = "Singular"      # a
    PLURAL = "Plural"          # (
    CLASS = "Class"            # }
    TOTALITY = "Totality"      # omega
    TEMPORAL = "Temporal"      # ~
    ENERGY = "Energy"          # delta
    PROCESS = "Process"        # ->


@dataclass(frozen=True)
class CharTensor:
    char: str
    greek: str
    meaning: str
    polarity: str        # "+", "-", ".", "+-"
    encapsulation: str


# --- Tautonic_Semantic_Dictionary_Full.md, section 2, transcribed ---
CHAR_TENSOR: Dict[str, CharTensor] = {c.char: c for c in [
    CharTensor("a", "alpha",   "Beginning / Singular / Base",        ".",  Encapsulation.SINGULAR),
    CharTensor("b", "beta",    "Growth / Extension / Expansion",     "+",  Encapsulation.SINGULAR),
    CharTensor("c", "gamma",   "Flow / Exchange / Movement",         ".",  Encapsulation.SINGULAR),
    CharTensor("d", "delta",   "Change / Difference / Delta",        ".",  Encapsulation.SINGULAR),
    CharTensor("e", "epsilon", "Perception / Insight / Vision",      "+",  Encapsulation.SINGULAR),
    CharTensor("f", "zeta",    "Network / Connection / Web",         "+-", Encapsulation.PLURAL),
    CharTensor("g", "eta",     "Harmony / Balance / Symmetry",       "+",  Encapsulation.SINGULAR),
    CharTensor("h", "theta",   "Constraint / Limit / Boundary",      "-",  Encapsulation.SINGULAR),
    CharTensor("i", "iota",    "Movement / Progression / Path",      ".",  Encapsulation.SINGULAR),
    CharTensor("j", "kappa",   "Knowledge / Cognition / Logic",      "+",  Encapsulation.SINGULAR),
    CharTensor("k", "lambda",  "Structure / Order / Skeleton",       ".",  Encapsulation.SINGULAR),
    CharTensor("l", "mu",      "Mass / Substance / Weight",          ".",  Encapsulation.SINGULAR),
    CharTensor("m", "nu",      "Interaction / Relation / Link",      "+-", Encapsulation.PLURAL),
    CharTensor("n", "xi",      "Complexity / Interweaving",          ".",  Encapsulation.PLURAL),
    CharTensor("o", "omicron", "Cycle / Repeat / Loop",              ".",  Encapsulation.SINGULAR),
    CharTensor("p", "pi",      "Procedure / Completeness / Ratio",   ".",  Encapsulation.SINGULAR),
    CharTensor("q", "rho",     "Flow / Resistance / Fluidity",       "+-", Encapsulation.PLURAL),
    CharTensor("r", "sigma",   "Summary / Synthesis / Collective",   "+",  Encapsulation.CLASS),
    CharTensor("s", "tau",     "Time / Sequence / Serial",           ".",  Encapsulation.SINGULAR),
    CharTensor("t", "upsilon", "Potential / Capability / Vector",    "+",  Encapsulation.SINGULAR),
    CharTensor("u", "phi",     "Transformation / Change / Flux",     "+-", Encapsulation.PLURAL),
    CharTensor("v", "chi",     "Conflict / Contrast / Tensity",      "-",  Encapsulation.SINGULAR),
    CharTensor("w", "psi",     "Mind / Abstraction / Intent",        "+",  Encapsulation.CLASS),
    CharTensor("x", "omega",   "Completion / Totality / End",        "+",  Encapsulation.TOTALITY),
    CharTensor("y", "alpha-",  "Base Singular (Modified)",           ".",  Encapsulation.SINGULAR),
    CharTensor("z", "beta-",   "Extension Singular (Modified)",      "+",  Encapsulation.SINGULAR),
]}


# --- THE ONE AUTHORED TABLE: which plane does each anchor speak on? ---
# Q1 is absent by construction: Who is the string itself, not a letter.
ANCHOR_PLANE: Dict[str, Tuple[Plane, str]] = {
    "a": (Plane.CAUSE,  "beginning is a causal origin"),
    "b": (Plane.WHAT,   "growth expands the possible"),
    "c": (Plane.WHERE,  "movement and exchange happen in space"),
    "d": (Plane.WHAT,   "difference is a shift in what could be"),
    "e": (Plane.WHY,    "perception is meaning apprehended"),
    "f": (Plane.EFFECT, "a network is consequence between things"),
    "g": (Plane.HOW,    "harmony and symmetry are consistency"),
    "h": (Plane.WHERE,  "a boundary is matter and distance"),
    "i": (Plane.CAUSE,  "a path is a progression, a sequence"),
    "j": (Plane.HOW,    "logic is count and consistency"),
    "k": (Plane.HOW,    "structure and order are method"),
    "l": (Plane.WHERE,  "mass is matter"),
    "m": (Plane.EFFECT, "relation is what one thing does to another"),
    "n": (Plane.WHAT,   "interweaving multiplies possibility"),
    "o": (Plane.CAUSE,  "a cycle is recurrence in sequence"),
    "p": (Plane.HOW,    "procedure and ratio are method and count"),
    "q": (Plane.WHERE,  "flow and resistance are physical"),
    "r": (Plane.WHY,    "synthesis is meaning gathered; Class scope"),
    "s": (Plane.CAUSE,  "time and sequence are causality itself"),
    "t": (Plane.WHAT,   "potential is probability"),
    "u": (Plane.WHAT,   "flux is the possible in motion"),
    "v": (Plane.EFFECT, "conflict is passion and consequence"),
    "w": (Plane.WHY,    "intent is meaning directed"),
    "x": (Plane.EFFECT, "completion is the consequence realised"),
    "y": (Plane.CAUSE,  "modified base, still an origin"),
    "z": (Plane.WHAT,   "modified extension, still expansion"),
}

POLARITY_PUSH = {"+": +1, "-": -1, ".": 0, "+-": 0}   # Mixed widens, no net push


@dataclass
class TautonicWord:
    """
    A word IS its string (Q1), decomposed into a graph on the six paired planes.
    """
    string: str
    steps: Dict[Plane, int] = field(default_factory=dict)
    widened: Dict[Plane, int] = field(default_factory=dict)
    encapsulation: Dict[str, int] = field(default_factory=dict)
    trace: List[str] = field(default_factory=list)

    @property
    def scores(self) -> Dict[Plane, float]:
        """
        Six paired-plane scores on the ---word+++ ladder. Q1 has no score:
        the identity is the string, not a position.
        """
        out = {}
        for p in Plane:
            if p == Plane.WHO:
                continue
            n = max(-3, min(3, self.steps.get(p, 0)))
            out[p] = SPECTRUM[n]
        return out

    @property
    def scope(self) -> str:
        """The noun-structure reading: which encapsulation dominates."""
        if not self.encapsulation:
            return Encapsulation.SINGULAR
        return max(self.encapsulation.items(), key=lambda kv: kv[1])[0]

    @property
    def address(self) -> QqciAddress:
        """
        Q1-rooted by construction, drilled by the most-deviant paired plane.
        The Driver is always the root because the string is always the Who.
        """
        s = self.scores
        leaf = max(s.items(), key=lambda kv: (abs(kv[1] - 1.0), -kv[0]))[0]
        return QqciAddress.of(Plane.WHO, leaf)

    def r_net(self) -> float:
        return FieldMath.fractal_ratio(list(self.scores.values()))

    def report(self) -> str:
        names = {Plane.WHAT: MoralVectors.WHAT, Plane.WHERE: MoralVectors.WHERE,
                 Plane.WHY: MoralVectors.WHY, Plane.HOW: MoralVectors.HOW,
                 Plane.CAUSE: MoralVectors.CAUSE, Plane.EFFECT: MoralVectors.EFFECT}
        lines = [f"  '{self.string}'   Q1 identity = the string itself",
                 f"  scope (Encapsulation): {self.scope}",
                 "  character decomposition:"]
        lines.extend(f"    {t}" for t in self.trace)
        lines.append("  derived paired-plane scores:")
        for p, sc in sorted(self.scores.items()):
            v = names[p]
            if abs(sc - 1.0) < 1e-9:
                tag = v.virtue
            else:
                tag = f"{'Excess' if sc > 1 else 'Deficit'}: {v.sin}"
            w = f"  (widened x{self.widened[p]})" if self.widened.get(p) else ""
            lines.append(f"    {v.interrogative:<7}{sc:5.2f}  {tag}{w}")
        lines.append(f"  address {self.address}   R_net {self.r_net():.4f}")
        return "\n".join(lines)


def decompose(string: str) -> TautonicWord:
    """Q1 = the string. Q2..Q7 = what its characters do."""
    w = TautonicWord(string=string)
    for ch in string.lower():
        ct = CHAR_TENSOR.get(ch)
        if ct is None:
            continue
        plane, why = ANCHOR_PLANE[ch]
        push = POLARITY_PUSH[ct.polarity]
        w.steps[plane] = w.steps.get(plane, 0) + push
        if ct.polarity == "+-":
            w.widened[plane] = w.widened.get(plane, 0) + 1
        w.encapsulation[ct.encapsulation] = (
            w.encapsulation.get(ct.encapsulation, 0) + 1)
        sign = {"+": "+1", "-": "-1", ".": " 0", "+-": "+-"}[ct.polarity]
        w.trace.append(
            f"{ch} {ct.greek:<8} {ct.meaning:<34} -> "
            f"{plane.name:<6} {sign}  ({ct.encapsulation})")
    return w


def compare_to_authored(string: str, authored: Dict[str, float]) -> str:
    """
    Honest check: how far were the hand-authored scores from what the
    corpus's own dictionary derives?
    """
    d = decompose(string)
    key = {"what": Plane.WHAT, "where": Plane.WHERE, "why": Plane.WHY,
           "how": Plane.HOW, "cause": Plane.CAUSE, "effect": Plane.EFFECT}
    lines = [f"  DERIVED vs AUTHORED for '{string}'",
             f"    {'plane':<8}{'derived':>9}{'authored':>10}{'delta':>9}"]
    total = 0.0
    for k, p in key.items():
        dv, av = d.scores[p], authored[k]
        total += abs(dv - av)
        lines.append(f"    {p.name:<8}{dv:9.2f}{av:10.2f}{dv - av:+9.2f}")
    lines.append(f"    mean absolute error: {total / len(key):.3f}")
    return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 72)
    print("TAUTONIC DECOMPOSITION: the string is the Who")
    print("=" * 72)
    for word in ("house", "home", "storm", "boat"):
        print()
        print(decompose(word).report())
    print()
    print("=" * 72)
    print(compare_to_authored("house", {
        "what": 1.25, "where": 1.00, "why": 0.95,
        "how": 1.05, "cause": 1.00, "effect": 0.95}))
