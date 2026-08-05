"""
Q4 first: populate the generalised form, then mutate outward.

THE CORRECTION THIS IMPLEMENTS
------------------------------
tautonic3.py derives from SPELLING and was measured useless as a semantic
anchor (same-type cosine 0.106, different-type 0.064, gap +0.042 = noise).
The reason is now clear: it was deriving MEANING from IDENTITY.

    Q1 (Who)  = the string. Identity. What the thing is CALLED.
    Q4 (Why)  = the generalised form. Meaning and Resonance. What it IS.

These are different planes and Q1 cannot produce Q4. 'storm' and 'recession'
share no letters and the same meaning; 'storm' and 'store' share almost every
letter and no meaning.

So Q4 is populated FIRST, from the generalised form, and the remaining planes
are mutations of it.

THE SOURCE
----------
_VFT MD/Actualism/Language/translating/nsm_reduction/
    reduced_dictionary.md
    comprehensive_isomorphic_dictionary.md

Complex English mapped onto NSM base primitives plus the ---word+++ spectrum:

    love / adore / cherish   -> feel+++     maximum positive affinity
    hate / despise / loathe  -> feel---     maximum negative affinity
    prove / verify           -> know+++
    huge / gigantic          -> big+++

Note what that does that spelling cannot: love and hate land on the SAME base
(feel) at opposite degrees. One axis, signed, which is the SignedSpan done on
the semantic axis instead of the orthographic one.

MUTATION ORDER
--------------
    Q4  the generalised form (base + degree)          <- populated first
    Q5  How    the base's category is its mechanism   <- count/consistency
    Q3  Where  spatial bases                          <- matter/distance
    Q6  Cause  temporal bases                         <- sequence
    Q2  What   action/possibility bases               <- probability
    Q7  Effect evaluative and affective bases         <- consequence
    Q1  Who    NOT derived: it is the string itself
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from qqci_engine import Plane
from tautonic import SPECTRUM
from vft import FieldMath, MoralVectors

NSM_DIR = (r"E:\Vector Field Theory\VFT Docs\_VFT MD\Actualism"
           r"\Language\translating\nsm_reduction")


# --- which plane does each NSM base speak on? ---
# Grouped by the dictionary's own section headings, so this follows the
# corpus's categories rather than inventing new ones.
BASE_PLANE: Dict[str, Plane] = {}


def _assign(planes_bases: Dict[Plane, str]) -> None:
    for plane, bases in planes_bases.items():
        for b in bases.split():
            BASE_PLANE[b] = plane


_assign({
    # Substantives: who is involved. The Driver.
    Plane.WHO:    "i you someone people body person self",
    # Evaluators and affect: value and consequence felt.
    Plane.EFFECT: "good bad feel want hot cold",
    # Mind and meaning: what is known, thought, meant.
    Plane.WHY:    "know think true false say word mean",
    # Count, size, logic: consistency and quantity.
    Plane.HOW:    "one two some many all big small more very not maybe can if",
    # Space and matter.
    Plane.WHERE:  "place near far above below side inside touch move thing part",
    # Time and sequence.
    Plane.CAUSE:  "time now before after long short moment because",
    # Action and possibility.
    Plane.WHAT:   "do happen live die there be have make see hear",
})

DEGREE_RE = re.compile(r"^([a-z]+)((?:\+{1,3})|(?:-{1,3}))?$")
ROW_RE = re.compile(r"^\|\s*\*{0,2}([^|*]+?)\*{0,2}\s*\|\s*`([^`]+)`\s*\|")


@dataclass
class GeneralForm:
    """A word's Q4: its generalised form as base plus degree."""
    word: str
    base: str
    degree: int                  # -3..+3
    gloss: str = ""

    @property
    def plane(self) -> Optional[Plane]:
        return BASE_PLANE.get(self.base)

    @property
    def score(self) -> float:
        return SPECTRUM[max(-3, min(3, self.degree))]

    def notation(self) -> str:
        sign = "+" * self.degree if self.degree > 0 else "-" * -self.degree
        return f"{self.base}{sign}"


def parse_scaled(token: str) -> Optional[Tuple[str, int]]:
    m = DEGREE_RE.match(token.strip())
    if not m:
        return None
    base, mods = m.group(1), m.group(2) or ""
    deg = len(mods) if mods.startswith("+") else -len(mods)
    return base, deg


def load_dictionary() -> Dict[str, GeneralForm]:
    """
    Parse the corpus tables: | **english / synonyms** | `base+++` | gloss |
    Every synonym on the left maps to the same generalised form, which is the
    isomorphic collapse operating at word rank.
    """
    forms: Dict[str, GeneralForm] = {}
    for fn in ("comprehensive_isomorphic_dictionary.md",
               "reduced_dictionary.md"):
        path = os.path.join(NSM_DIR, fn)
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                m = ROW_RE.match(line.strip())
                if not m:
                    continue
                english, scaled = m.group(1), m.group(2)
                parsed = parse_scaled(scaled)
                if parsed is None:
                    continue
                base, deg = parsed
                for w in re.split(r"[/,]", english):
                    w = w.strip().lower()
                    if w and w.isalpha():
                        forms.setdefault(w, GeneralForm(w, base, deg, scaled))
    return forms


# ---------------------------------------------------------------------------
# MUTATION: from the Q4 general form to the other planes
# ---------------------------------------------------------------------------

def mutate(form: GeneralForm) -> Dict[Plane, float]:
    """
    The generalised form sits on ONE plane at its degree. The remaining planes
    are not invented: they stay at Unity unless the base implies them.

    This is deliberately conservative. A word whose general form says nothing
    about causality should read Redemption (1.0) on Q6, not a guessed value.
    Absence is meaningful; a fabricated score is not.
    """
    scores = {p: 1.0 for p in Plane if p != Plane.WHO}
    p = form.plane
    if p is not None and p != Plane.WHO:
        scores[p] = form.score
    return scores


@dataclass
class Q4Word:
    word: str
    form: Optional[GeneralForm]
    scores: Dict[Plane, float] = field(default_factory=dict)

    @property
    def covered(self) -> bool:
        return self.form is not None and self.form.plane is not None

    def r_net(self) -> float:
        return FieldMath.fractal_ratio(list(self.scores.values()))

    def report(self) -> str:
        if not self.covered:
            return f"  '{self.word}'  NOT COVERED by the generalised dictionary"
        f = self.form
        return (f"  '{self.word}'  Q4 general form = {f.notation():<10} "
                f"plane {f.plane.name:<7} score {f.score:.2f}  ({f.gloss})")


def lookup(word: str, forms: Dict[str, GeneralForm]) -> Q4Word:
    f = forms.get(word.lower())
    return Q4Word(word=word, form=f, scores=mutate(f) if f else
                  {p: 1.0 for p in Plane if p != Plane.WHO})


if __name__ == "__main__":
    forms = load_dictionary()
    print(f"generalised dictionary: {len(forms)} english words -> "
          f"{len(set(f.notation() for f in forms.values()))} distinct forms")
    print(f"bases mapped to planes: {len(BASE_PLANE)}")
    print()

    print("ISOMORPHIC COLLAPSE AT WORD RANK (many surface forms, one meaning)")
    buckets: Dict[str, List[str]] = {}
    for w, f in forms.items():
        buckets.setdefault(f.notation(), []).append(w)
    for notation, ws in sorted(buckets.items(),
                               key=lambda kv: -len(kv[1]))[:8]:
        plane = BASE_PLANE.get(notation.rstrip("+-"))
        pn = plane.name if plane else "UNMAPPED"
        print(f"  {notation:<12} [{pn:<7}] {', '.join(sorted(ws)[:8])}")
    print()

    print("SIGNED AXIS: opposites share a base, at opposite degrees")
    for a, b in (("love", "hate"), ("prove", "disbelieve"),
                 ("huge", "tiny"), ("boiling", "freezing")):
        fa, fb = forms.get(a), forms.get(b)
        if fa and fb:
            print(f"  {a:<12}{fa.notation():<10} vs {b:<12}{fb.notation():<10}"
                  f"  same base: {fa.base == fb.base}")
    print()

    print("COVERAGE against the retelling vocabulary")
    from domains import SEA, STARTUP, ORBIT
    vocab = list(SEA.entities) + list(STARTUP.entities) + list(ORBIT.entities)
    cov = [w for w in vocab if lookup(w, forms).covered]
    print(f"  {len(cov)}/{len(vocab)} covered")
    if cov:
        for w in cov:
            print("  " + lookup(w, forms).report().strip())
    missing = [w for w in vocab if w not in cov]
    print(f"  missing: {', '.join(missing)}")
