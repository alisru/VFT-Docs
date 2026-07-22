"""
The 7D dictionary, rebuilt on the project's OWN geometry.

WHAT WAS WRONG BEFORE
---------------------
The previous version invented bipolar axes (patient..agent, immaterial..material)
with positions in [-1,+1]. That is not this project's geometry and it discards
the moral content.

MoralVectorDef defines the real axes, and they are UNIPOLAR AROUND UNITY:

    1.0            = the virtue realised
    above 1.0      = Excess of the sin
    below 1.0      = Deficit of the same sin

    Who     Sovereignty   / Tyranny
    Where   Thriving      / Mere Survival
    What    Stewardship   / Greed
    Why     Truth-Telling / Delusion
    How     Wisdom        / Sophistry
    Cause   Redemption    / Revisionism
    Effect  Love/Unity    / Parasitism

This matters because a bipolar span cannot express "too much and too little are
the same failure". Truth is the ratio of 1, and both directions away from it are
the sin. Storing a position on a bipolar axis throws that away.

A word is therefore stored as seven scores around Unity. Its own R_net (the
fractal ratio) is then a real quantity: how coherent the word is AS A THING.
Agents sit near 1.0; forces sit far from it. Nothing else had to be added to
get that, which is the sign the geometry was already right.

HONESTY NOTE
------------
These 189 scores are authored, and the author knew which cross-domain pairs
were expected. This shows the axes CAN carry the distinctions, not that the
distinctions were discovered. The unconstrained test in test_lexicon() is the
fairer measure and it is reported whether it passes or not.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from qqci_engine import (
    Meaning, MeaningRegistry, Plane, QqciAddress, SemanticRelation, TensorRank,
)
from vft import FieldMath, Idea, Judgement, MoralVectorDef, MoralVectors

REGISTRY = MeaningRegistry()
REGISTRY.seed_alphabet("abcdefghijklmnopqrstuvwxyz")

# The bridge: the engine's Plane enum and the project's MoralVectorDef are the
# same seven axes named in two files. Bound here so neither has to move.
PLANE_TO_VECTOR: Dict[Plane, MoralVectorDef] = {
    Plane.WHO: MoralVectors.WHO,
    Plane.WHAT: MoralVectors.WHAT,
    Plane.WHERE: MoralVectors.WHERE,
    Plane.WHY: MoralVectors.WHY,
    Plane.HOW: MoralVectors.HOW,
    Plane.CAUSE: MoralVectors.CAUSE,
    Plane.EFFECT: MoralVectors.EFFECT,
}

_ORDER = ["who", "where", "what", "why", "how", "cause", "effect"]
_KEY_TO_PLANE = {"who": Plane.WHO, "where": Plane.WHERE, "what": Plane.WHAT,
                 "why": Plane.WHY, "how": Plane.HOW, "cause": Plane.CAUSE,
                 "effect": Plane.EFFECT}


def _w(word: str, who: float, where: float, what: float, why: float,
       how: float, cause: float, effect: float,
       pron: Optional[str] = None) -> Meaning:
    """
    Carve a word at its seven scores around Unity. The Meaning's TruthScore
    per plane lives in .plane_scores; the address is derived from which plane
    deviates most, because the strongest deviation from virtue is what the
    word most IS.
    """
    scores = dict(zip(
        [Plane.WHO, Plane.WHERE, Plane.WHAT, Plane.WHY, Plane.HOW,
         Plane.CAUSE, Plane.EFFECT],
        [who, where, what, why, how, cause, effect]))

    ranked = sorted(scores.items(),
                    key=lambda kv: (-FieldMath.vft_entropy(kv[1]), kv[0]))
    addr = QqciAddress.of(ranked[0][0], ranked[1][0])

    m = REGISTRY.carve_or_recall(word, addr, rank=TensorRank.WORD)
    m.plane_scores = scores          # the 7D position
    m.pronunciation = pron
    return m


def entropy_vector(m: Meaning) -> Dict[Plane, float]:
    return {p: FieldMath.vft_entropy(s) for p, s in m.plane_scores.items()}


def word_coherence(m: Meaning) -> float:
    """R_net for the word itself: 1 / product of its seven scores."""
    return FieldMath.fractal_ratio(list(m.plane_scores.values()))


def as_idea(m: Meaning) -> Idea:
    """A word IS an Idea: seven Beliefs, one per moral vector."""
    return Idea.of(**{k: (m.word, m.plane_scores[_KEY_TO_PLANE[k]])
                      for k in _ORDER})


def alignment_report(m: Meaning) -> str:
    lines = []
    for p, s in sorted(m.plane_scores.items()):
        v = PLANE_TO_VECTOR[p]
        if abs(s - 1.0) < 0.001:
            tag = v.virtue
        elif s > 1.0:
            tag = f"Excess: {v.sin}"
        else:
            tag = f"Deficit: {v.sin}"
        lines.append(f"    {v.interrogative:<7}{s:5.2f}  {tag}")
    return "\n".join(lines)


def plane_distance_vft(a: Meaning, b: Meaning) -> float:
    """Euclidean distance in the seven-score space around Unity."""
    total = sum((a.plane_scores[p] - b.plane_scores[p]) ** 2 for p in Plane)
    return (total / 7.0) ** 0.5


dist = plane_distance_vft


# ---------------------------------------------------------------------------
# THE LEXICON
#
# Read each row as: how does this word stand to each virtue?
#   1.0 = the virtue realised.  >1.0 = excess of the sin.  <1.0 = deficit.
# ---------------------------------------------------------------------------

LEXICON: Dict[str, Meaning] = {m.word: m for m in [

    # --- agents: answerable will, near Unity, venturing so slightly loose ---
    #        who   where  what   why    how    cause  effect
    _w("fisherman",   1.00, 0.90, 1.00, 1.05, 0.90, 1.00, 1.00),
    _w("founder",     1.05, 0.85, 1.10, 1.10, 0.85, 1.05, 0.95),
    _w("engineer",    1.00, 0.95, 1.00, 1.00, 1.05, 1.00, 1.00),

    # --- patrons: hold order, conserve, slightly over-ordered ---
    _w("harbourmaster", 1.10, 1.05, 0.95, 0.95, 1.15, 0.90, 1.05),
    _w("investor",      1.15, 1.00, 1.20, 0.90, 1.20, 0.85, 1.10),
    _w("director",      1.15, 1.05, 0.95, 0.95, 1.20, 0.90, 1.05),

    # --- forces: unanswerable will, no meaning, parasitic consequence ---
    _w("storm",       1.80, 0.40, 1.60, 0.30, 0.40, 1.50, 1.90),
    _w("recession",   1.70, 0.35, 1.75, 0.35, 0.50, 1.45, 1.85),
    _w("solarflare",  1.85, 0.40, 1.55, 0.30, 0.40, 1.55, 1.90),

    # --- vessels: made things, held in stewardship, fragile ---
    _w("boat",        0.70, 1.00, 1.00, 1.00, 1.05, 0.90, 1.00),
    _w("product",     0.65, 0.95, 1.10, 1.05, 1.00, 0.90, 0.95),
    _w("probe",       0.70, 1.00, 1.00, 1.00, 1.10, 0.90, 1.00),

    # --- materials: substrate, no will, no purpose of their own ---
    _w("oak",         0.40, 1.10, 0.95, 0.60, 1.00, 1.05, 0.95),
    _w("opensource",  0.35, 1.00, 0.85, 0.65, 1.05, 1.10, 0.90),
    _w("alloy",       0.40, 1.10, 0.95, 0.60, 1.05, 1.05, 0.95),

    # --- ground: indifferent, hazardous, tests the venture ---
    _w("reef",        0.55, 1.35, 0.90, 0.55, 0.85, 1.10, 1.35),
    _w("market",      0.60, 1.30, 1.15, 0.60, 0.80, 1.05, 1.30),
    _w("asteroid",    0.55, 1.35, 0.90, 0.55, 0.85, 1.10, 1.35),

    # --- havens: where thriving is restored ---
    _w("harbour",     0.75, 0.95, 0.95, 1.05, 1.05, 0.90, 0.90),
    _w("incubator",   0.70, 0.95, 1.05, 1.05, 1.00, 0.90, 0.90),
    _w("station",     0.75, 0.95, 0.95, 1.05, 1.05, 0.90, 0.90),

    # --- tokens: transferable, valued by convention, over-counted ---
    _w("charts",      0.45, 1.00, 1.10, 1.00, 1.20, 0.95, 0.95),
    _w("equity",      0.45, 1.05, 1.30, 0.95, 1.25, 0.95, 1.00),
    _w("telemetry",   0.45, 1.00, 1.10, 1.00, 1.20, 0.95, 0.95),

    # --- knowledge: pattern, high order, low agency ---
    _w("tides",       0.35, 1.00, 1.00, 1.05, 1.25, 1.10, 0.95),
    _w("retention",   0.35, 1.00, 1.05, 1.05, 1.30, 1.05, 0.95),
    _w("drift",       0.35, 1.00, 1.00, 1.05, 1.25, 1.10, 0.95),
]}


# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------

def nearest(word: str, candidates: List[str], k: int = 3
            ) -> List[Tuple[str, float]]:
    a = LEXICON[word]
    scored = [(c, dist(a, LEXICON[c])) for c in candidates if c != word]
    scored.sort(key=lambda kv: kv[1])
    return scored[:k]


def derive_bijection(source_words: List[str], target_words: List[str]
                     ) -> Dict[str, str]:
    """Greedy type-free rebinding by seven-score distance alone."""
    pairs = sorted((dist(LEXICON[s], LEXICON[t]), s, t)
                   for s in source_words for t in target_words)
    mapping, used = {}, set()
    for _, s, t in pairs:
        if s in mapping or t in used:
            continue
        mapping[s] = t
        used.add(t)
    return mapping


def link_relations(similar_at: float = 0.12) -> int:
    """Related, derived from geometry. Opposite = the two words' entropies
    point opposite ways on four or more planes."""
    words, links = list(LEXICON.values()), 0
    for i, a in enumerate(words):
        for b in words[i + 1:]:
            d = dist(a, b)
            opposed = sum(1 for p in Plane
                          if (a.plane_scores[p] - 1.0) * (b.plane_scores[p] - 1.0) < 0
                          and abs(a.plane_scores[p] - b.plane_scores[p]) > 0.5)
            if d <= similar_at:
                a.add_related(b, SemanticRelation.SIMILAR)
                b.add_related(a, SemanticRelation.SIMILAR)
                links += 2
            elif opposed >= 4:
                a.add_related(b, SemanticRelation.OPPOSITE)
                b.add_related(a, SemanticRelation.OPPOSITE)
                links += 2
    return links
