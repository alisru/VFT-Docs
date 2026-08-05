"""
THE EGG: the pre-defined seed ontology from which the chicken emerges.

The user's answer to the chicken-and-egg problem: "we pre-define the egg and
the chicken is emergent." This file IS the egg. Nothing here is learned; it is
the minimal seeded substrate. Everything derived FROM it (see derive.py and
run_experiments.py) is the chicken.

WHOSE SOLUTIONS ARE COPIED HERE
-------------------------------
1. QUALITATIVE PROCESS THEORY (Forbus 1984, MIT AI Lab).
   "Objects move, collide, flow, bend, heat up, cool down... these things that
   cause changes in objects over time are intuitively characterized as
   processes." QP represents a process as PRECONDITIONS + INFLUENCES over a
   quantity space of inequalities.
   Copied: the process structure (slots.Process), the seeded material states
   below, and the derivation of new states by applying processes rather than
   by storing them. `solid` is NOT stored as a concept: it is DERIVED by
   applying `freeze` to `liquid`, exactly as the user specified
   (liquid-flow-stop-stop = solid).

2. NSM SEMANTIC PRIMES (Wierzbicka). A small closed set of undefinable
   primitives from which everything else is paraphrased. This is the
   justification for having an egg at all: SOMETHING must be undefined, or
   definition is circular. The project's own corpus already uses NSM.
   Copied: the closed-set discipline. The seed here is deliberately tiny.

3. REICHENBACH (1947) tense structure, and ISO-TimeML.
   Reichenbach's three times -- S (speech), E (event), R (reference) -- are
   the solved model for the user's Totality_Event_Frame
   [past{when_prev}, present{when_now}, future{when_next}].
   Copied: three-time structure, with each time carrying a full 7-plane frame.

WHAT IS AUTHORED HERE AND WHY THAT IS LEGITIMATE
-------------------------------------------------
Everything in this file is authored. That is allowed under LANGUAGE_SPEC 13
because it is (a) FORM and SEED, not measured content, and (b) every test that
judges it (run_experiments.py) is independent of it: the seed does not know
about the corpus, so corpus agreement cannot be the seed read back.

The seed must stay SMALL. If it grows to cover the phenomena it is meant to
predict, it stops being an egg and becomes the answer written down. Current
size is asserted by test_seed_is_small().
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from qqci_engine import Plane
from slots import (
    IDENTITY_ANCHOR, MEANING_HUB, Frame, Process, Slot, identify, unify,
)

# ---------------------------------------------------------------------------
# SEED 1: matter and its states (Qualitative Process Theory)
# ---------------------------------------------------------------------------
# Read a row as: what KIND (Q2), what MATTER (Q3), what MEANING (Q4),
# what MECHANISM (Q5), what CONSEQUENCE (Q7).
# Q6 (origin) is left OPEN on purpose: a substance's origin is not intrinsic,
# it is supplied by whatever process produced it. That open slot is what the
# process binds -- the DNA site.


def _mk(lemma: str, **kw: str) -> Frame:
    slots = {}
    for key, val in kw.items():
        slots[getattr(Plane, key.upper())] = Slot.filled(val)
    return Frame(lemma, slots, provenance="seed")


MATTER: Dict[str, Frame] = {
    # the three states of matter, defined ONLY by mechanism and shape
    "liquid": _mk("liquid", what="substance", where="takes-container-shape",
                  why="matter-state", how="flows", effect="wets"),
    "gas":    _mk("gas", what="substance", where="fills-container",
                  why="matter-state", how="disperses", effect="pervades"),
    # NOTE: "solid" is deliberately NOT seeded. It must be DERIVED.
    # See derive_solid() below. This is the whole point of the egg.
}

SUBSTANCE: Dict[str, Frame] = {
    "water": _mk("water", what="substance", where="takes-container-shape",
                 why="matter-state", how="flows", effect="wets"),
    "rock":  _mk("rock", what="substance", where="holds-own-shape",
                 why="matter-state", how="static", effect="resists"),
    "air":   _mk("air", what="substance", where="fills-container",
                 why="matter-state", how="disperses", effect="pervades"),
}

# ---------------------------------------------------------------------------
# SEED 2: processes (QP theory: preconditions + influences)
# ---------------------------------------------------------------------------
# The user's formulation: liquid-flow-stop-stop. The process `freeze` takes a
# thing whose mechanism is `flows` and stops it. The RESULT is a new frame
# nobody stored.

PROCESSES: Dict[str, Process] = {
    "freeze": Process(
        "freeze",
        precondition={Plane.HOW: "flows"},
        influence={Plane.HOW: "static", Plane.WHERE: "holds-own-shape",
                   Plane.EFFECT: "resists"},
        gloss="stop the flow: liquid-flow-stop-stop"),
    "melt": Process(
        "melt",
        precondition={Plane.HOW: "static"},
        influence={Plane.HOW: "flows", Plane.WHERE: "takes-container-shape",
                   Plane.EFFECT: "wets"},
        gloss="start the flow"),
    "boil": Process(
        "boil",
        precondition={Plane.HOW: "flows"},
        influence={Plane.HOW: "disperses", Plane.WHERE: "fills-container",
                   Plane.EFFECT: "pervades"},
        gloss="unbind the flow entirely"),
}


def derive_solid() -> Frame:
    """
    THE DEMONSTRATION: derive `solid` without ever having defined it.

    liquid --[freeze: stop the flow]--> ?

    The result should be recognisable as `rock`-like on its content planes,
    because `solid` is not a stored concept but the END-PLACE that the process
    routes `liquid` to. This is LANGUAGE_SPEC 7's field: F(inputs) -> basin.
    """
    return PROCESSES["freeze"].apply(MATTER["liquid"], lemma="?derived")


# ---------------------------------------------------------------------------
# SEED 3: operators (words that are mostly BLANK -- the DisCoCat matrices)
# ---------------------------------------------------------------------------
# These have HIGH valence: almost every plane open. They cannot stand alone;
# they must contract with a host. This is LANGUAGE_SPEC 3.1: What-selectors
# live at the q sub-address and borrow their root from the host.


def _op(lemma: str, plane: Plane, value: str, score: float) -> Frame:
    """An operator: fills exactly ONE plane, requires a host for the rest."""
    f = Frame(lemma, {plane: Slot.filled(value, score)}, provenance="seed-op")
    # every other content plane is a REQUIRED open index: it needs a host
    for p in Plane:
        if p not in (IDENTITY_ANCHOR, plane):
            f.slots[p] = Slot.open(required=(p is MEANING_HUB))
    return f


OPERATORS: Dict[str, Frame] = {
    # degree/magnitude operators: they write a SIZE onto the host's Q3 matter
    "big":    _op("big", Plane.WHERE, "large-extent", 1.30),
    "small":  _op("small", Plane.WHERE, "small-extent", 0.70),
    # manner operators: they write onto the host's Q5 mechanism
    "quickly": _op("quickly", Plane.HOW, "fast", 1.25),
    "slowly":  _op("slowly", Plane.HOW, "slow", 0.75),
    # affect operators: they write onto the host's Q7 consequence
    "good":   _op("good", Plane.EFFECT, "benefits", 1.00),
    "bad":    _op("bad", Plane.EFFECT, "harms", 1.60),
}

HOSTS: Dict[str, Frame] = {
    "house": _mk("house", what="dwelling", where="built-structure",
                 why="shelter", how="encloses", cause="built", effect="houses"),
    "boat":  _mk("boat", what="vessel", where="hull", why="transport",
                 how="floats", cause="built", effect="carries"),
}


# ---------------------------------------------------------------------------
# SEED 4: the Totality Event Frame (Reichenbach's three times)
# ---------------------------------------------------------------------------

@dataclass
class When:
    """
    One temporal slice, carrying a full 7-plane frame.

    The user's form:
      when = [who{}, what{}, why{}, where{}, how{}, cause{}, effect{}]
    """
    label: str
    frame: Optional[Frame] = None

    @property
    def known(self) -> bool:
        return self.frame is not None


@dataclass
class TotalityEventFrame:
    """
    The user's Totality_Event_Frame[{when}] =
        [past{when_prev}, present{when_now}, future{when_nextPredicted}]

    Reichenbach's insight, copied: you need THREE times, not two, because the
    reference point is independent of the event point. Here:

      past    = the PRECONDITION state   (QP theory's precondition)
      present = the state DURING         (the process active)
      future  = the PREDICTED state      (QP theory's influence, resolved)

    The future slice is explicitly a PREDICTION, and marking it as such is the
    whole point: an event frame whose future is asserted rather than predicted
    is the false-fill failure mode (LANGUAGE_SPEC 7.1).
    """
    action: str
    past: When = field(default_factory=lambda: When("past"))
    present: When = field(default_factory=lambda: When("present"))
    future: When = field(default_factory=lambda: When("future", None))
    predicted: bool = True

    @staticmethod
    def from_process(proc: Process, before: Frame) -> "TotalityEventFrame":
        """Build the three times by running the process forward."""
        after = proc.apply(before)
        during = Frame(f"{proc.name}ing", dict(before.slots),
                       provenance="event:during")
        during.slots[Plane.CAUSE] = Slot.filled(proc.name)
        return TotalityEventFrame(
            action=proc.name,
            past=When("past", before),
            present=When("present", during),
            future=When("future", after),
            predicted=True)

    def delta(self) -> Dict[Plane, str]:
        """Which planes CHANGED across the event. This is the meaning of the
        event: Actualism step 5 says meaning emerges from CHANGE, not state."""
        if not (self.past.known and self.future.known):
            return {}
        out = {}
        for p in Plane:
            a, b = self.past.frame.slots[p], self.future.frame.slots[p]
            if a.value != b.value:
                out[p] = f"{a.value} -> {b.value}"
        return out

    def readout(self) -> str:
        lines = [f"EVENT '{self.action}'"
                 f"{'  (future is PREDICTED)' if self.predicted else ''}"]
        for w in (self.past, self.present, self.future):
            tag = w.frame.lemma if w.known else "(unknown)"
            lines.append(f"  {w.label:<8} {tag}")
        for p, ch in self.delta().items():
            lines.append(f"    change {p.name:<7} {ch}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# SEED SIZE DISCIPLINE
# ---------------------------------------------------------------------------

def seed_size() -> Dict[str, int]:
    return {
        "matter_states": len(MATTER),
        "substances": len(SUBSTANCE),
        "processes": len(PROCESSES),
        "operators": len(OPERATORS),
        "hosts": len(HOSTS),
        "total_frames": len(MATTER) + len(SUBSTANCE) + len(OPERATORS) + len(HOSTS),
    }


def test_seed_is_small(limit: int = 40) -> bool:
    """The egg must stay an egg. If the seed grows past `limit` frames it is
    no longer a seed, it is the answer written down."""
    return seed_size()["total_frames"] <= limit


ALL_CONCEPTS: Dict[str, Frame] = {**MATTER, **SUBSTANCE, **HOSTS}


if __name__ == "__main__":
    print("THE EGG (seeded, authored, deliberately tiny)")
    print("=" * 70)
    for k, v in seed_size().items():
        print(f"  {k:<16}{v}")
    print(f"  seed stays small: {test_seed_is_small()}")
    print()

    print("DERIVING A CONCEPT THAT WAS NEVER SEEDED")
    print("=" * 70)
    print("  seeded matter states :", ", ".join(MATTER))
    print("  'solid' seeded?      :", "solid" in MATTER)
    print()
    d = derive_solid()
    print("  liquid --[freeze]-->")
    print("   ", d.readout())
    print()
    print("  recognised as (by content planes, identity ignored):")
    for name, sc in identify(d, ALL_CONCEPTS)[:4]:
        print(f"    {name:<10}{sc:.0%}")
    print()

    print("OPERATOR CONTRACTION (a blank word binding to a host)")
    print("=" * 70)
    big, house = OPERATORS["big"], HOSTS["house"]
    print(f"  'big'   valence {big.valence} (open indices), saturated={big.saturated}")
    print(f"  'house' valence {house.valence}, saturated={house.saturated}")
    bh = unify(house, big, lemma="big house")
    print(f"  contract -> 'big house' valence {bh.valence}, saturated={bh.saturated}")
    print("   ", bh.readout())
    print()

    print("TOTALITY EVENT FRAME (Reichenbach three times)")
    print("=" * 70)
    tef = TotalityEventFrame.from_process(PROCESSES["freeze"], MATTER["liquid"])
    print(tef.readout())
