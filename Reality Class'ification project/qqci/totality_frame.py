"""
THE TOTALITY EVENT FRAME, integrated with the node tensor.

    Totality_Event_Frame[{when}] = [ past[{when_prev}],
                                     present[{when_now}],
                                     future[{when_nextPredicted}] ]

    when = [ who[{who_when}],   what[{what_when}],   why[{why_when}],
             where[{where_when}], how[{how_when}],   cause[{cause_when}],
             effect[{effect_when}] ]

THE INTEGRATION POINT
---------------------
This is not a new axis bolted on. The relativity map's y-axis ALREADY is the
three times:

        can_be    ->  future   (when_nextPredicted)   open possibility
        are       ->  present  (when_now)             the anchor, asserted
        was_like  ->  past     (when_prev)            analogical / resemblance

So concept_tensor.NodeTensor's 3x3 grid is a Totality Event Frame per cell,
and the x-axis (affirmed / mix / negated) is the polarity of each time.

WHY EACH PLANE CARRIES ITS OWN 'when'
--------------------------------------
`who[{who_when}]` is not the same clock as `cause[{cause_when}]`. The corpus
already specifies seven DIFFERENT KINDS of measure, one per plane (the Core
Metrics, scope Section 9 risk 4, recorded as CLOSED):

    Who     Directional Time     which way the identity is heading
    What    Resolution Time      how long until the possibility resolves
    Where   Euclidean Space      plain distance
    Why     Non-Euclidean Time   meaning-time, does not add linearly
    How     Computational Time   how many steps the mechanism costs
    Cause   Linear Time          ordinary sequence
    Effect  Energetic Time       strain: consequence per unit energy

This is why a single metric was always going to be wrong, and why the frame
needs a per-plane `when` rather than one timestamp per slice.

MEANING IS THE DELTA
--------------------
Actualism step 5: meaning emerges from CHANGE across a sequence, not from
static state. So the frame's payload is `delta()` -- which planes moved between
past and future, and by how much in their own metric. `L5 Temporal` has been
stored-but-unused since the start of the project; this is its job.

THE FUTURE SLICE IS MARKED PREDICTED
------------------------------------
Asserting the future rather than predicting it is exactly the false-fill
failure mode. The frame carries the flag, and cross-plane disagreement on the
future slice is reported rather than silently emitted.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from concept_tensor import (
    FAMILIES, MODE, POLARITY, ConceptTensor, NodeTensor, build_concept,
    family_of, score_axis,
)
from qqci_engine import Plane

# The seven Core Metrics: each plane's `when` is measured in its own kind.
CORE_METRIC: Dict[Plane, str] = {
    Plane.WHO:    "Directional Time",
    Plane.WHAT:   "Resolution Time",
    Plane.WHERE:  "Euclidean Space",
    Plane.WHY:    "Non-Euclidean Time",
    Plane.HOW:    "Computational Time",
    Plane.CAUSE:  "Linear Time",
    Plane.EFFECT: "Energetic Time (Strain)",
}

# the modal row -> which of the three times it is
ROW_TO_TIME = {"can_be": "future", "are": "present", "was_like": "past"}
TIME_TO_ROW = {v: k for k, v in ROW_TO_TIME.items()}


@dataclass
class PlaneWhen:
    """One plane's reading AND its own time coordinate in its own metric."""
    plane: Plane
    value: float = 0.0          # what the plane says
    when: float = 0.0           # where it sits in ITS OWN metric
    engaged: bool = False       # silent planes are not dissenting planes

    @property
    def metric(self) -> str:
        return CORE_METRIC[self.plane]

    def __str__(self) -> str:
        if not self.engaged:
            return f"{self.plane.name:<7} --      (silent)"
        return (f"{self.plane.name:<7} {self.value:+.2f}  "
                f"when {self.when:+.2f} [{self.metric}]")


@dataclass
class When:
    """A complete 7-plane slice: when = [who{}, what{}, ... effect{}]."""
    label: str
    planes: Dict[Plane, PlaneWhen] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for p in Plane:
            self.planes.setdefault(p, PlaneWhen(plane=p))

    def set(self, plane: Plane, value: float, when: float) -> None:
        self.planes[plane] = PlaneWhen(plane, value, when, engaged=True)

    @property
    def engaged(self) -> List[Plane]:
        return [p for p in Plane if self.planes[p].engaged]

    @property
    def disagreement(self) -> float:
        """Max spread across ENGAGED planes only. A silent plane is silent."""
        v = [self.planes[p].value for p in self.engaged]
        return (max(v) - min(v)) if len(v) > 1 else 0.0

    def render(self, indent: str = "      ") -> str:
        return "\n".join(indent + str(self.planes[p]) for p in Plane)


@dataclass
class TotalityEventFrame:
    """past[when_prev], present[when_now], future[when_nextPredicted]."""
    subject: str
    past: When = field(default_factory=lambda: When("past"))
    present: When = field(default_factory=lambda: When("present"))
    future: When = field(default_factory=lambda: When("future"))
    predicted: bool = True

    @staticmethod
    def from_node(subject: str, nt: NodeTensor) -> "TotalityEventFrame":
        """
        Read a Totality Event Frame straight out of a node tensor: the modal
        grid's rows ARE the three times, and the cell's plane is where its
        reading lands.
        """
        tef = TotalityEventFrame(subject=subject)
        plane = Plane(nt.cell[0] + 1)          # the cell's root plane
        slices = {"past": tef.past, "present": tef.present, "future": tef.future}

        for i, row in enumerate(MODE):
            occ = float(nt.grid[i].sum())
            if occ <= 0:
                continue
            when_slice = slices[ROW_TO_TIME[row]]
            # polarity centroid: where on affirmed<->negated the mass sits
            w = nt.grid[i]
            pol = float((w * np.array([-1.0, 0.0, 1.0])).sum() / max(w.sum(), 1e-9))
            when_slice.set(plane, value=occ, when=pol)
            # the (upsilon, psi) key rides along on the same position
            for j in range(3):
                if nt.grid[i, j] > 0:
                    u, ps = nt.key[i, j]
                    when_slice.planes[plane].value = float(occ)
                    when_slice.planes[plane].when = float(pol)
                    break
        return tef

    def delta(self) -> Dict[Plane, Tuple[float, float, str]]:
        """
        MEANING IS THE CHANGE (Actualism step 5). Which planes moved from past
        to future, by how much, in their own metric.
        """
        out: Dict[Plane, Tuple[float, float, str]] = {}
        for p in Plane:
            a, b = self.past.planes[p], self.future.planes[p]
            if not (a.engaged or b.engaged):
                continue
            out[p] = (b.value - a.value, b.when - a.when, CORE_METRIC[p])
        return out

    @property
    def false_fill(self) -> bool:
        """Asserting the future rather than predicting it, or planes at odds."""
        return (not self.predicted) or self.future.disagreement > 0.5

    def render(self) -> str:
        lines = [f"TOTALITY EVENT FRAME  subject='{self.subject}'"
                 f"{'   [future is PREDICTED]' if self.predicted else ''}"]
        for w in (self.past, self.present, self.future):
            eng = w.engaged
            lines.append(f"  {w.label:<8} ({len(eng)}/7 planes engaged"
                         f", disagreement {w.disagreement:.2f})")
            if eng:
                lines.append(w.render())
        d = self.delta()
        if d:
            lines.append("  DELTA past -> future  (meaning is the change)")
            for p, (dv, dw, metric) in d.items():
                lines.append(f"      {p.name:<7} value {dv:+.2f}  "
                             f"when {dw:+.2f}  [{metric}]")
        lines.append(f"  false_fill: {self.false_fill}")
        return "\n".join(lines)


def frame_from_event(subject: str, before: Dict[Plane, float],
                     after: Dict[Plane, float],
                     during: Optional[Dict[Plane, float]] = None
                     ) -> TotalityEventFrame:
    """
    Build a frame from an actual transition: the plane readings before, during
    and after. Each plane's `when` is its own displacement in its own metric.
    """
    tef = TotalityEventFrame(subject=subject)
    during = during or {}
    for p, v in before.items():
        tef.past.set(p, v, when=0.0)
    for p, v in during.items():
        tef.present.set(p, v, when=0.5)
    for p, v in after.items():
        base = before.get(p, 0.0)
        tef.future.set(p, v, when=(v - base))
    return tef


def main() -> None:
    print("=" * 74)
    print("TOTALITY EVENT FRAME  --  three times, seven planes, seven metrics")
    print("=" * 74)
    print("the relativity map's y-axis IS the three times:")
    for row, t in ROW_TO_TIME.items():
        print(f"    {row:<10} -> {t}")
    print()
    print("each plane carries its OWN kind of when (the Core Metrics):")
    for p in Plane:
        print(f"    {p.name:<7} {CORE_METRIC[p]}")
    print()

    dpath = os.path.join(os.path.dirname(__file__), "dictionary_expanded.json")
    apath = os.path.join(os.path.dirname(__file__), "derived_addresses.json")
    with open(dpath, "r", encoding="utf-8") as fh:
        senses = json.load(fh)
    with open(apath, "r", encoding="utf-8") as fh:
        addrs = {w: tuple(a) for w, a in json.load(fh).items()}

    print("-" * 74)
    print("A: frame read out of a concept's node tensor")
    ct = build_concept("hut", senses, addrs)
    if ct:
        nt = next(iter(ct.nodes.values()))
        print(TotalityEventFrame.from_node("hut", nt).render())
    print()

    print("-" * 74)
    print("B: frame from a real transition (liquid --freeze--> solid)")
    tef = frame_from_event(
        "freeze(liquid)",
        before={Plane.WHERE: 0.2, Plane.HOW: 1.0, Plane.EFFECT: 0.8},
        during={Plane.CAUSE: 1.0, Plane.HOW: 0.5},
        after={Plane.WHERE: 1.0, Plane.HOW: 0.0, Plane.EFFECT: 0.3,
               Plane.CAUSE: 1.0})
    print(tef.render())


if __name__ == "__main__":
    main()
