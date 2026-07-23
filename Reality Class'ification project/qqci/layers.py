"""
TWO SEPARATE STRUCTURES. Do not conflate them. This file exists mainly to
keep them apart, because conflating them has now been done twice.

A. THE QQCI FORM  --  the semantic space
   7 planes, addressed recursively: Q.q.c is plane drilled by plane drilled
   by plane, same kind at every level. 7 / 49 / 343. This is the geometry a
   meaning HAS. Implemented as the Kronecker basis in fractal_basis.py, and
   one 7x7 generator serves every depth.

B. THE DICTIONARY SCALES  --  the filing system
   From {Meaning}.cs, nesting outermost first:

       Registry > Temporal > Language > Phrase > Word > Char > Meaning

   Six dimensions saying WHERE AN ENTRY IS STORED. Each scale stores THAT
   SCALE'S CONTENT: Char holds characters, Word holds words, Phrase holds
   phrases, Language holds the language RULES themselves (the collapse
   dictionaries, NSM reduction, grammar), Temporal holds versioning,
   Registry holds which contextual dictionary. When
   General_Contextual_Dictionary.cs writes `wordLayer: 7 // Effect`, the 7
   is an integer KEY, not a plane reading -- it does not mean "this word
   reads Effect." It is not a semantic composition and it is not a
   transformer layer.

The two are orthogonal. A meaning has a Qqci form AND a filing location, the
same way a book has a subject and a shelf number. Neither determines the other.

WHAT THE TRANSFORMER DEPTH IS
-----------------------------
Not settled here, and deliberately not invented. What the prior art does
(Lila-E8, Leech-LILA) is keep depth an ordinary free hyperparameter -- 12
layers -- and put the geometry in the frozen Q/K projections. On that pattern
the 7x7x7 lives in the BASIS, not in the layer count, and depth is tuned like
any other transformer's. That is the conservative default until there is a
reason to do otherwise.

An earlier version of this file claimed the six dictionary scales WERE the
transformer layers, each running the 7-plane operation. That was wrong and is
recorded in the scope doc errata.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


# ---------------------------------------------------------------------------
# B. THE DICTIONARY SCALES -- filing, not semantics
# ---------------------------------------------------------------------------

@dataclass
class Scale:
    index: int
    name: str
    granularity: str        # what one entry at this scale IS
    key_holds: str          # what the stored integer means
    implemented_by: str
    status: str


SCALES: List[Scale] = [
    Scale(1, "Char", "one character",
          "the character itself",
          "MeaningMetaRegistry (rank index) + tautonic.CHAR_TENSOR", "done"),
    Scale(2, "Word", "one word string",
          "the word itself",
          "MeaningMetaRegistry.get_meaning(rank=WORD, word=...)", "done"),
    Scale(3, "Phrase", "one phrase or transition",
          "the phrase itself",
          "MeaningMetaRegistry (rank=PHRASE) + sael.Transition", "done"),
    Scale(4, "Language", "one language system",
          "which language plane",
          "QqciAddress.language", "partial: only L0 is ever populated"),
    Scale(5, "Temporal", "when the entry was carved",
          "day of year",
          "Meaning.carved_at", "partial: stored, never used"),
    Scale(6, "Registry", "which contextual dictionary",
          "0 = General, 7 = Conflict (per the corpus .cs files)",
          "MeaningMetaRegistry indices; domains.py invents its own instead",
          "partial: corpus registries not wired in"),
]


# ---------------------------------------------------------------------------
# A. THE QQCI FORM -- semantics, recursive, same kind at every level
# ---------------------------------------------------------------------------

QQCI_DEPTHS = [
    (1, 7, "Q", "the seven planes"),
    (2, 49, "Q.q", "each plane read through each plane; the 42 off-diagonal "
                   "cells are the 42-Structure, the 7 diagonal are Qi.qi"),
    (3, 343, "Q.q.c", "the full 7x7x7"),
]


def separation_report() -> str:
    lines = ["TWO STRUCTURES, KEPT APART", "=" * 70, "",
             "A. QQCI FORM  (semantic; what a meaning IS)"]
    for depth, cells, notation, desc in QQCI_DEPTHS:
        lines.append(f"   depth {depth}  {cells:>4} cells  {notation:<8} {desc}")
    lines.append("   recursive, same kind at every level, one 7x7 generator")
    lines.append("   implemented: fractal_basis.py")
    lines.append("")
    lines.append("B. DICTIONARY SCALES  (filing; where an entry LIVES)")
    for s in reversed(SCALES):
        lines.append(f"   L{s.index} {s.name:<9} {s.granularity:<26} "
                     f"[{s.status}]")
        lines.append(f"        key holds: {s.key_holds}")
    lines.append("   nesting: Registry > Temporal > Language > Phrase > Word "
                 "> Char > Meaning")
    lines.append("   implemented: qqci_engine.MeaningMetaRegistry")
    lines.append("")
    lines.append("ORTHOGONAL. A meaning has a Qqci form AND a filing location,")
    lines.append("like a book has a subject and a shelf number. Neither")
    lines.append("determines the other, and summing them into a single")
    lines.append("dimensionality is the category error to avoid.")
    return "\n".join(lines)


def outstanding() -> str:
    return "\n".join([
        "OUTSTANDING", "=" * 70,
        "1. L4 Language: only L0 is ever populated, so cross-language",
        "   disagreement -- a central claim -- has never been measured.",
        "2. L5 Temporal: carved_at is stored and unused. Actualism step 5 says",
        "   meaning emerges from CHANGE across a sequence; the retelling",
        "   compares static skeletons and would not notice belief-state",
        "   transitions or multi-plane convergence points.",
        "3. L6 Registry: wire in the corpus registries (0 General, 7 Conflict)",
        "   instead of the domains invented in domains.py, and derive the",
        "   functional types from geometry rather than hand-authoring them.",
        "4. Transformer depth: left as a free hyperparameter, per prior art.",
        "   The geometry goes in the frozen Q/K basis, not the layer count.",
    ])


if __name__ == "__main__":
    print(separation_report())
    print()
    print(outstanding())
