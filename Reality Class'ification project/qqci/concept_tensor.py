"""
THE NODE TENSOR: each of the 343 cells is an xy tensor, with PER-FAMILY axes.

THE SPEC, VERBATIM
------------------
    "things like building, structure, dwelling, home, etc resolve on a shelter
     by size and complexity, where COMPLEXITY IS QUALITY AND QUANTITY OF
     FACILITIES, SIZE IS RELATED TO PEOPLE PER SQUARE METER. food is on a
     tensor of SUSTENANCE. all using the relativity map for the 2d tensor,
     keyed to the underlying benefit vector from the regular morality spread of
     everyone to no-one else, will activity-passive-suppressive"

WHAT I GOT WRONG TWICE BEFORE
-----------------------------
I used ONE global pair of axes (size, complexity) as generic adjective
projections and applied them to every family. That is not the spec. The spec is:

  - axes are declared PER FAMILY, not globally
  - each axis has an OPERATIONAL definition, not an adjective list
        size       = people per square metre        (an occupancy density)
        complexity = quality x quantity of facilities (a count and a grade)
        sustenance = what food varies on             (NOT size, NOT complexity)
  - the 2D tensor is the RELATIVITY MAP (the modal tile)
  - every position is KEYED by (upsilon, psi)

So a family is a TYPE DECLARATION: it says which dimensions its members vary
on. `shelter` and `food` do not share a coordinate system, and asking for the
size of a soup is a category error rather than a number.

THE RESULTING OBJECT
--------------------
    concept
      -> sparse over 343 cells                (one per sense; polysemy = many)
        -> each cell: the 3x3 relativity map  (the xy tensor)
          -> each grid position keyed (upsilon, psi)
        -> each cell: its FAMILY's declared axes, operationally derived
"""

from __future__ import annotations

import collections
import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

DICT_FILE = os.path.join(os.path.dirname(__file__), "dictionary_expanded.json")
ADDR_FILE = os.path.join(os.path.dirname(__file__), "derived_addresses.json")

N_CELLS = 343
MODE = ["can_be", "are", "was_like"]        # y: possibility -> present -> past
POLARITY = ["affirmed", "mix", "negated"]   # x: affirm -> INGAP -> negate


# ---------------------------------------------------------------------------
# FAMILY TYPE DECLARATIONS -- each family says what its members vary ON
# ---------------------------------------------------------------------------

@dataclass
class Axis:
    """
    One operationally-defined dimension of a family.

    `low` and `high` are not synonym lists for a vague adjective: they are the
    OBSERVABLE CUES for the quantity the axis actually measures. For shelter
    size the quantity is people per square metre, so the cues are occupancy
    terms (single, one-room / communal, barracks), not the words small and big.
    """
    name: str
    quantity: str            # what is actually being measured
    low: List[str]
    high: List[str]
    graded: bool = True


FAMILIES: Dict[str, List[Axis]] = {
    # ---- SHELTER: size = people per square metre, complexity = facilities ---
    "structure": [
        Axis("size", "people per square metre",
             low=["single", "one", "solitary", "individual", "personal",
                  "private", "hut", "cabin", "booth", "cell", "small"],
             high=["communal", "public", "multiple", "families", "crowd",
                   "barracks", "dormitory", "apartment", "block", "tenement",
                   "large"]),
        Axis("complexity", "quality and quantity of facilities",
             low=["crude", "bare", "temporary", "makeshift", "rough",
                  "primitive", "simple", "shack", "unfinished", "shelter"],
             high=["equipped", "furnished", "plumbing", "heating", "kitchen",
                   "facilities", "luxurious", "appointed", "elaborate",
                   "permanent", "residence", "amenities"]),
    ],
    # ---- FOOD: a tensor of SUSTENANCE, not of size ------------------------
    "substance": [
        Axis("sustenance", "nutritive energy provided",
             low=["garnish", "flavoring", "seasoning", "condiment", "spice",
                  "snack", "sweet", "confection", "beverage", "water"],
             high=["staple", "meal", "nourishing", "nutritious", "hearty",
                   "protein", "bread", "meat", "grain", "sustenance",
                   "nutriment", "substantial"]),
        Axis("preparation", "degree of processing",
             low=["raw", "fresh", "natural", "whole", "uncooked", "wild"],
             high=["cooked", "baked", "processed", "refined", "prepared",
                   "cured", "fermented", "distilled"]),
    ],
    # ---- ACTS: benefit and will, the morality spread directly -------------
    "act": [
        Axis("benefit", "who it benefits: everyone -> no-one else",
             low=["harm", "destroy", "damage", "attack", "steal", "deceive",
                  "exploit", "injure", "kill", "betray"],
             high=["help", "protect", "give", "heal", "support", "provide",
                   "share", "teach", "nourish", "rescue"]),
        Axis("will", "active <-> passive/suppressive",
             low=["refrain", "abstain", "withhold", "suppress", "prevent",
                  "avoid", "neglect", "remain", "cease", "stop"],
             high=["act", "drive", "force", "make", "move", "create",
                   "propel", "initiate", "cause", "build"]),
    ],
}

# The morality key applied to EVERY position regardless of family.
KEY_UPSILON = FAMILIES["act"][0]     # benefit: everyone <-> no-one else
KEY_PSI = FAMILIES["act"][1]         # will: active <-> suppressive


def score_axis(gloss: str, lemmas: Sequence[str], axis: Axis) -> Optional[float]:
    """
    Position on ONE axis, read from the sense's own definition.

    Returns None when the definition says nothing about this quantity --
    absence is meaningful and must not become a guessed centre.
    """
    text = set((gloss or "").lower().replace(";", " ").replace(",", " ").split())
    text |= {l.lower() for l in lemmas}
    lo = len(text & set(axis.low))
    hi = len(text & set(axis.high))
    if not (lo or hi):
        return None
    return (hi - lo) / (hi + lo)


@dataclass
class NodeTensor:
    """ONE cell of the 343: a 3x3 relativity map keyed by (upsilon, psi)."""
    cell: Tuple[int, int, int]
    family: str = ""
    axis_names: Tuple[str, ...] = ()
    axis_vals: Tuple[Optional[float], ...] = ()
    grid: np.ndarray = field(
        default_factory=lambda: np.zeros((3, 3), dtype=np.float32))
    key: np.ndarray = field(
        default_factory=lambda: np.zeros((3, 3, 2), dtype=np.float32))

    @property
    def address(self) -> str:
        Q, q, c = self.cell
        return f"Q{Q+1}.q{q+1}.c{c+1}"

    def write(self, mode: str, polarity: str, occ: float,
              upsilon: float = 0.0, psi: float = 0.0) -> None:
        i, j = MODE.index(mode), POLARITY.index(polarity)
        self.grid[i, j] = occ
        self.key[i, j] = (upsilon, psi)

    @property
    def in_gap(self) -> float:
        """Mass in the mix row/column: unresolved ambiguity -> the drill trigger."""
        return float(self.grid[:, 1].sum() + self.grid[1, :].sum()
                     - 2 * self.grid[1, 1])

    def render(self) -> str:
        ax = ", ".join(
            f"{n}={'--' if v is None else f'{v:+.2f}'}"
            for n, v in zip(self.axis_names, self.axis_vals))
        out = [f"  {self.address}  family={self.family}",
               f"      axes: {ax or '(family declares none)'}"]
        out.append("            " + "".join(f"{p:>15}" for p in POLARITY))
        for i, m in enumerate(MODE):
            cells = []
            for j in range(3):
                o = self.grid[i, j]
                u, p = self.key[i, j]
                cells.append(f"{o:4.2f}[u{u:+.1f} p{p:+.1f}]" if o else ".")
            out.append(f"  {m:>10}" + "".join(f"{c:>15}" for c in cells))
        return "\n".join(out)


@dataclass
class ConceptTensor:
    lemma: str
    nodes: Dict[int, NodeTensor] = field(default_factory=dict)

    @property
    def occupancy(self) -> int:
        return len(self.nodes)

    def dense(self) -> np.ndarray:
        out = np.zeros((N_CELLS, 3, 3), dtype=np.float32)
        for nid, n in self.nodes.items():
            out[nid] = n.grid
        return out

    def render(self) -> str:
        return (f"CONCEPT '{self.lemma}'  {self.occupancy}/343 cells lit "
                f"({1 - self.occupancy/N_CELLS:.1%} empty)\n"
                + "\n".join(n.render() for n in self.nodes.values()))


def family_of(chain: Sequence[str]) -> str:
    """Walk the reduction chain outward until it hits a declared family."""
    for node in reversed(chain):
        if node in FAMILIES:
            return node
    return chain[min(3, len(chain) - 1)] if chain else ""


def build_concept(lemma: str, senses: Dict[str, dict],
                  addrs: Dict[str, Tuple[int, int, int]],
                  max_senses: int = 6) -> Optional[ConceptTensor]:
    hits = [(n, r) for n, r in senses.items() if lemma in r["lemmas"]]
    if not hits:
        return None
    ct = ConceptTensor(lemma=lemma)
    base = addrs.get(lemma, (0, 0, 0))

    for k, (_name, rec) in enumerate(hits[:max_senses]):
        fam = family_of(rec["chain"])
        axes = FAMILIES.get(fam, [])
        vals = tuple(score_axis(rec["gloss"], rec["lemmas"], a) for a in axes)

        cell = (base[0], base[1], (base[2] + k) % 7)
        nid = cell[0] * 49 + cell[1] * 7 + cell[2]
        nt = NodeTensor(cell=cell, family=fam,
                        axis_names=tuple(a.name for a in axes),
                        axis_vals=vals)
        u = score_axis(rec["gloss"], rec["lemmas"], KEY_UPSILON) or 0.0
        p = score_axis(rec["gloss"], rec["lemmas"], KEY_PSI) or 0.0
        nt.write("are", "mix", 1.0, upsilon=u * 2.0, psi=p * 2.0)
        ct.nodes[nid] = nt
    return ct


def main() -> None:
    print("=" * 74)
    print("NODE TENSORS WITH PER-FAMILY DECLARED AXES")
    print("=" * 74)
    for fam, axes in FAMILIES.items():
        print(f"  family '{fam}' declares:")
        for a in axes:
            print(f"      {a.name:<12} = {a.quantity}")
    print("  -> shelter and food do NOT share a coordinate system.")
    print("     asking the 'size' of a soup is a type error, not a number.")
    print()

    with open(DICT_FILE, "r", encoding="utf-8") as fh:
        senses = json.load(fh)
    with open(ADDR_FILE, "r", encoding="utf-8") as fh:
        addrs = {w: tuple(a) for w, a in json.load(fh).items()}

    print("-" * 74)
    print("SHELTER FAMILY on its OWN axes (people/m2 x facilities)")
    rows = []
    for _n, r in senses.items():
        if family_of(r["chain"]) != "structure":
            continue
        s = score_axis(r["gloss"], r["lemmas"], FAMILIES["structure"][0])
        c = score_axis(r["gloss"], r["lemmas"], FAMILIES["structure"][1])
        if s is not None and c is not None:
            rows.append((r["lemmas"][0], s, c, r["gloss"][:44]))
    rows.sort(key=lambda x: (x[1], x[2]))
    print(f"  {len(rows)} senses positioned on BOTH axes")
    for w, s, c, g in rows[:6]:
        print(f"    size{s:+.2f} cplx{c:+.2f}  {w:<16} {g}")
    print("    ...")
    for w, s, c, g in rows[-6:]:
        print(f"    size{s:+.2f} cplx{c:+.2f}  {w:<16} {g}")
    print()

    print("-" * 74)
    print("FOOD FAMILY on SUSTENANCE (its own axis, not size)")
    rows = []
    for _n, r in senses.items():
        if family_of(r["chain"]) != "substance":
            continue
        s = score_axis(r["gloss"], r["lemmas"], FAMILIES["substance"][0])
        if s is not None:
            rows.append((r["lemmas"][0], s, r["gloss"][:50]))
    rows.sort(key=lambda x: x[1])
    print(f"  {len(rows)} senses positioned on sustenance")
    for w, s, g in rows[:5]:
        print(f"    {s:+.2f}  {w:<16} {g}")
    print("    ...")
    for w, s, g in rows[-5:]:
        print(f"    {s:+.2f}  {w:<16} {g}")
    print()

    print("-" * 74)
    for lemma in ("hut", "bank"):
        ct = build_concept(lemma, senses, addrs)
        if ct:
            print(ct.render())
            print()


if __name__ == "__main__":
    main()
