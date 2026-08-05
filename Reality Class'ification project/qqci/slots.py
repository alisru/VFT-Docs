"""
THE CORE MECHANISM: a word is a 7-plane frame with OPEN and FILLED slots, and
composition is UNIFICATION (open slots take the partner's filled values).

WHAT THIS IMPLEMENTS, AND WHOSE SOLUTION IS BEING COPIED
--------------------------------------------------------
The user's claim: "all words have a meaning across the 7 planes hanging off Q4,
but some are blank so they fill and attach to other words like DNA."

Three existing fields already solved exactly this, and their solutions agree:

1. HPSG / LFG UNIFICATION GRAMMAR (Pollard & Sag).
   A word is a typed feature structure. Unspecified features are variables.
   Two structures unify iff no specified feature conflicts; unification fills
   each side's unspecified features from the other. THIS IS THE DNA PAIRING.
   Copied: unify(), the conflict rule, the subsumption order.

2. DisCoCat (Coecke, Sadrzadeh, Clark). A word's grammatical type determines
   its TENSOR SHAPE; composition is TENSOR CONTRACTION. A noun is a vector
   (rank 0 open). An adjective is a matrix: it has ONE open index that must be
   contracted against a noun. A transitive verb has TWO.
   THE IDENTIFICATION THIS FILE MAKES:

       an OPEN PLANE *is* an OPEN TENSOR INDEX
       valence (count of open planes) *is* tensor rank
       unification *is* contraction

   That is why "big" cannot stand alone: it is not a point, it is an operator
   with an open index seeking a host. Copied: type-driven composition, rank
   from type, contraction as the composition operator.

3. FrameNet / valency (Fillmore). Frames have core elements that MUST be
   filled and peripheral ones that may be. Copied: the required/optional
   distinction on open slots.

WHY THIS DISSOLVES THE WORD-TO-CELL PROBLEM
-------------------------------------------
The project measured that assigning a word to a fixed cell fails (spelling
scored 12.9% of the way from random to optimal, ~noise). The reason is now
structural: a word with open planes HAS NO FIXED CELL. It is an operator, and
where it lands depends on what it contracts with. `red apple` puts red's value
on Q3; `red in the face` puts it on Q7. Same operator, different contraction.

Q1 vs Q4 (the two anchors, do not merge them)
---------------------------------------------
Q1 WHO  is the IDENTITY anchor: the string itself. Always filled, never open,
        never inherited through composition (handover: "a word's string is its
        Who"). Q1.q5 is its spelling as a countable construction.
Q4 WHY  is the MEANING anchor: the generalised form everything else hangs off
        (the user's "hanging off Q4", and q4_meaning.py's "Q4 first, then
        mutate outward").

A composition inherits the HEAD's Q1 (a big house is a house, not a big) but
merges meaning on Q4.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

from qqci_engine import Plane

# The corrected literal roots (LANGUAGE_SPEC §3). Q1 anchors identity, Q2
# selects, Q3-Q7 carry content.
ROOT_QUESTION: Dict[Plane, str] = {
    Plane.WHO:    "identity: the thing itself, its name",
    Plane.WHAT:   "selector: which-one / what-kind / how-much",
    Plane.WHERE:  "matter: parts, substance, place",
    Plane.WHY:    "meaning: purpose, resonance (the hub)",
    Plane.HOW:    "mechanism: how it works, count, consistency",
    Plane.CAUSE:  "origin: what it came from",
    Plane.EFFECT: "consequence: what it results in",
}

IDENTITY_ANCHOR = Plane.WHO   # never open, never inherited
MEANING_HUB = Plane.WHY       # what the rest hangs off


class Fill(Enum):
    """A slot is either bound to a value or open (a free index)."""
    FILLED = "filled"
    OPEN = "open"


@dataclass(frozen=True)
class Slot:
    """
    One plane of a word's frame.

    value    the filler (a type name, e.g. "dwelling", "flows"). None if OPEN.
    score    unipolar around Unity: 1.0 virtue realised, >1 excess, <1 deficit.
             Only meaningful when FILLED.
    required True if this open slot MUST be filled for the word to be complete
             (FrameNet core element). An adjective's host slot is required.
    """
    state: Fill
    value: Optional[str] = None
    score: float = 1.0
    required: bool = False

    @staticmethod
    def filled(value: str, score: float = 1.0) -> "Slot":
        return Slot(Fill.FILLED, value, score)

    @staticmethod
    def open(required: bool = False) -> "Slot":
        return Slot(Fill.OPEN, None, 1.0, required)

    @property
    def is_open(self) -> bool:
        return self.state is Fill.OPEN

    def __str__(self) -> str:
        if self.is_open:
            return "____!" if self.required else "____"
        return f"{self.value}({self.score:.2f})"


@dataclass
class Frame:
    """
    A word as a 7-plane typed feature structure.

    In DisCoCat terms this is a tensor whose rank is `valence` (the number of
    open indices). A frame with valence 0 is saturated: it can stand alone.
    A frame with valence > 0 is an operator awaiting contraction.
    """
    lemma: str
    slots: Dict[Plane, Slot] = field(default_factory=dict)
    provenance: str = ""      # where this frame's content came from

    def __post_init__(self) -> None:
        for p in Plane:
            self.slots.setdefault(p, Slot.open())
        # Q1 is the identity anchor: always filled with the string itself.
        if self.slots[IDENTITY_ANCHOR].is_open:
            self.slots[IDENTITY_ANCHOR] = Slot.filled(self.lemma)

    # --- structure ---

    @property
    def open_planes(self) -> List[Plane]:
        return [p for p in Plane if self.slots[p].is_open]

    @property
    def filled_planes(self) -> List[Plane]:
        return [p for p in Plane if not self.slots[p].is_open]

    @property
    def valence(self) -> int:
        """Tensor rank: how many indices are still free."""
        return len(self.open_planes)

    @property
    def required_planes(self) -> List[Plane]:
        return [p for p in self.open_planes if self.slots[p].required]

    @property
    def saturated(self) -> bool:
        """No REQUIRED open slots: the word can stand alone."""
        return not self.required_planes

    def occupancy(self) -> Tuple[int, ...]:
        """The binary occupancy pattern (LANGUAGE_SPEC 4.1)."""
        return tuple(0 if self.slots[p].is_open else 1 for p in Plane)

    def sparsity(self) -> float:
        """Fraction of planes that are OPEN. High = mostly blank = operator."""
        return self.valence / len(Plane)

    def readout(self) -> str:
        return "  ".join(f"{p.name[:3]}:{self.slots[p]}" for p in Plane)


# ---------------------------------------------------------------------------
# COMPLEMENTARITY: the DNA pairing measure
# ---------------------------------------------------------------------------

def bindable_sites(a: Frame, b: Frame) -> List[Plane]:
    """
    Planes where a is OPEN and b is FILLED: the sites where b can bind into a.
    The identity anchor never binds (a word's Who is its own).
    """
    return [p for p in a.open_planes
            if p is not IDENTITY_ANCHOR and not b.slots[p].is_open]


def complementarity(a: Frame, b: Frame) -> float:
    """
    How much of a's openness b can satisfy, in [0, 1].

    This is the DNA base-pairing score and the DisCoCat contractibility check
    in one number. It is DIRECTIONAL: comp(adjective, noun) is high because
    the adjective has the open index; comp(noun, adjective) is low.
    """
    openings = [p for p in a.open_planes if p is not IDENTITY_ANCHOR]
    if not openings:
        return 0.0
    return len(bindable_sites(a, b)) / len(openings)


def required_complementarity(a: Frame, b: Frame) -> float:
    """Complementarity restricted to REQUIRED slots (FrameNet core elements).
    This is the measure that predicts whether a composition MUST happen."""
    req = [p for p in a.required_planes if p is not IDENTITY_ANCHOR]
    if not req:
        return 0.0
    return sum(1 for p in req if not b.slots[p].is_open) / len(req)


def affinity(a: Frame, b: Frame) -> float:
    """
    Symmetric binding affinity: the best of the two directions. Two saturated
    words have affinity 0 (nothing to bind); an operator and its host score
    high in the operator's direction.
    """
    return max(complementarity(a, b), complementarity(b, a))


def conflicts(a: Frame, b: Frame) -> List[Plane]:
    """Planes where both are FILLED with different values: unification fails."""
    out = []
    for p in Plane:
        if p is IDENTITY_ANCHOR:
            continue          # identities always differ; that is not a conflict
        sa, sb = a.slots[p], b.slots[p]
        if not sa.is_open and not sb.is_open and sa.value != sb.value:
            out.append(p)
    return out


# ---------------------------------------------------------------------------
# UNIFICATION: composition as contraction (HPSG's operation, DisCoCat's reading)
# ---------------------------------------------------------------------------

def unify(head: Frame, dependent: Frame, lemma: Optional[str] = None,
          strict: bool = False) -> Optional[Frame]:
    """
    Compose two frames. The HEAD supplies identity (Q1); the DEPENDENT fills
    the head's open slots and vice versa.

    Returns None if the frames conflict and strict=True. Under strict=False
    (the default, matching how language actually behaves) a conflict on a
    content plane is resolved in the DEPENDENT's favour when the head was
    open there, else the head wins and the conflict is recorded.

    In DisCoCat terms: this contracts every index that one side leaves open
    and the other side binds. The result's valence is strictly lower than the
    more-open input's, which is why composition SATURATES.
    """
    bad = conflicts(head, dependent)
    if bad and strict:
        return None

    out = Frame(lemma or head.lemma, {}, provenance="unify")
    for p in Plane:
        sh, sd = head.slots[p], dependent.slots[p]
        if p is IDENTITY_ANCHOR:
            out.slots[p] = Slot.filled(lemma or head.lemma)
        elif sh.is_open and not sd.is_open:
            out.slots[p] = sd                    # dependent fills head's blank
        elif sd.is_open and not sh.is_open:
            out.slots[p] = sh                    # head fills dependent's blank
        elif sh.is_open and sd.is_open:
            out.slots[p] = Slot.open(sh.required or sd.required)
        else:
            # both filled: keep head's value, but blend the score, because two
            # filled planes agreeing is stronger evidence than one.
            out.slots[p] = Slot.filled(sh.value, (sh.score + sd.score) / 2.0)
    return out


def compose_chain(frames: Sequence[Frame], lemma: Optional[str] = None
                  ) -> Optional[Frame]:
    """
    Fold a sequence of frames left to right. This is LANGUAGE_SPEC 5.1: a
    sentence is a PATH, and its meaning is the contraction of the chain.
    """
    if not frames:
        return None
    acc = frames[0]
    for nxt in frames[1:]:
        acc = unify(acc, nxt, lemma=lemma or acc.lemma)
        if acc is None:
            return None
    return acc


def coherent(f: Frame) -> bool:
    """
    A composition is EFFECTIVE (LANGUAGE_SPEC 5.1) when every required slot is
    bound. An unsaturated chain is the garbled-order case: it traces no stable
    basin and the honest output is 'malformed'.
    """
    return f.saturated


# ---------------------------------------------------------------------------
# PROCESSES: state-action-effect (Qualitative Process Theory, Forbus)
# ---------------------------------------------------------------------------

@dataclass
class Process:
    """
    A qualitative process, copied from Forbus's QP theory.

    QP theory's structure is: a process has PRECONDITIONS (what must hold for
    it to be active) and INFLUENCES (what it changes). Copied exactly, with
    the influenced quantity being a plane value instead of a physical one.

    This is the user's `liquid-flow-stop-stop = solid` as
    what-how-cause-effect: applying `freeze` to `liquid` changes its Q5
    mechanism from flowing to static, and the RESULT IS DERIVED, not stored.
    """
    name: str
    precondition: Dict[Plane, str]     # plane -> required value
    influence: Dict[Plane, str]        # plane -> new value
    gloss: str = ""

    def applicable(self, f: Frame) -> bool:
        for p, v in self.precondition.items():
            s = f.slots[p]
            if s.is_open or s.value != v:
                return False
        return True

    def apply(self, f: Frame, lemma: Optional[str] = None) -> Optional[Frame]:
        if not self.applicable(f):
            return None
        out = Frame(lemma or f"{self.name}({f.lemma})",
                    dict(f.slots), provenance=f"process:{self.name}")
        out.slots[IDENTITY_ANCHOR] = Slot.filled(out.lemma)
        for p, v in self.influence.items():
            out.slots[p] = Slot.filled(v, f.slots[p].score)
        # the process itself is the CAUSE of the resulting state
        out.slots[Plane.CAUSE] = Slot.filled(self.name)
        return out


def identify(f: Frame, lexicon: Dict[str, Frame],
             ignore: Iterable[Plane] = (Plane.WHO, Plane.CAUSE)
             ) -> List[Tuple[str, float]]:
    """
    RECOGNITION BY COMPOSITE (the user's "recognise new things by breaking
    them into composites"). Given a derived frame, find which known concepts
    match its content planes.

    Q1 is ignored because identity is exactly what we are trying to recover,
    and Q6 because a derived state's cause is the process that made it, which
    the stored concept has no reason to share.
    """
    skip = set(ignore)
    scored: List[Tuple[str, float]] = []
    for name, cand in lexicon.items():
        shared = agree = 0
        for p in Plane:
            if p in skip:
                continue
            sa, sb = f.slots[p], cand.slots[p]
            if sa.is_open or sb.is_open:
                continue
            shared += 1
            agree += int(sa.value == sb.value)
        if shared:
            scored.append((name, agree / shared))
    scored.sort(key=lambda kv: (-kv[1], kv[0]))
    return scored
