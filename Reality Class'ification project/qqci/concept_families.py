"""
CONCEPT FAMILIES FROM A REAL DICTIONARY, POSITIONED ON TYPED AXES.

    "take an actual dictionary, expand all the meanings and find and connect the
     reduced forms and fundamentals that way? so things like building,
     structure, dwelling, home, etc resolve on a shelter by size and
     complexity, where complexity is quality and quantity of facilities, size
     is related to people per square meter."

WHY THIS AND NOT THE DERIVED CLUSTERS
-------------------------------------
derive_addresses.py gives every word a Q.q.c from co-occurrence, and the
coverage is real (343/343 cells, 8.7 words/cell). But the cells are NUMBERED.
There is no way to say what cell 172 means, so the naming claim cannot be
checked and no typed constraint can be written.

A dictionary has already done the reduction. WordNet's hypernym chain IS an
address made of real words:

    hut  ->  shelter  ->  structure  ->  artifact  ->  whole

Every level is nameable, the tree bottoms out in a small set of unique
beginners, and the whole thing is machine-readable. That is the reduction to
fundamentals, already built, for 82,115 noun senses.

THE DIVISION OF LABOUR
----------------------
    WordNet supplies  the STRUCTURE   (which family, what is a part of what)
    the corpus supplies the POSITION  (where on the family's axes)

Nothing is hand-positioned. An axis is defined by ONE seed pair (small/large),
and every member's position is its projection onto that direction in the
corpus embedding -- the Turney-Littman seed-and-propagate method the scope doc
Section 20 already names as the ranked option.

WHY THIS MATTERS FOR SENTENCE FORMING (scope Section 15)
--------------------------------------------------------
    "Autocomplete becomes slot completion. Given a context and action,
     remaining parameters and the effect signature are type-determined...
     Prediction becomes constraint satisfaction over a template: checkable, and
     wrong in detectable ways rather than plausible ways."

    "he lived in a small ___"  -> SHELTER family, size below median
    "he ate a ___"             -> SUSTENANCE family; `house` is TYPE-EXCLUDED,
                                  not merely improbable

A transformer assigns "he ate a house" a low probability. This assigns it zero
by type. That is the difference between wrong-in-plausible-ways and
wrong-in-detectable-ways.

THE FALSIFIER
-------------
If the corpus-derived size ordering of shelter words does not recover the
obvious one (shack/hut below house below mansion/palace), the axes are not
derivable this way and the approach fails. Reported either way.
"""

from __future__ import annotations

import collections
import json
import os
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np
from nltk.corpus import wordnet as wn

from derive_addresses import cooccurrence, embed, read_corpus

# The ONLY authored input: one seed pair per axis. Everything else is derived.
AXES: Dict[str, Tuple[List[str], List[str]]] = {
    "size":       (["small", "tiny", "little"], ["large", "big", "huge"]),
    "complexity": (["simple", "basic", "crude"], ["complex", "elaborate",
                                                  "sophisticated"]),
}


def family_members(root: str, pos: str = "n", max_depth: int = 6
                   ) -> List[str]:
    """
    Every lemma under a family root in the WordNet hierarchy.
    The tree is the dictionary's, not ours.
    """
    try:
        roots = wn.synsets(root, pos)
    except Exception:
        return []
    if not roots:
        return []
    out: set = set()
    frontier = [(roots[0], 0)]
    while frontier:
        syn, d = frontier.pop()
        if d > max_depth:
            continue
        for lem in syn.lemmas():
            name = lem.name().lower().replace("_", "-")
            if "-" not in name and name.isalpha():
                out.add(name)
        for hypo in syn.hyponyms():
            frontier.append((hypo, d + 1))
    return sorted(out)


def hypernym_address(word: str, pos: str = "n") -> List[str]:
    """The reduction path: the dictionary's own chain to a fundamental."""
    s = wn.synsets(word, pos)
    if not s:
        return []
    return [x.name().split(".")[0] for x in s[0].hypernym_paths()[0]]


class FamilyTensor:
    """A concept family positioned on axes derived from the corpus."""

    def __init__(self, vocab: List[str], X: np.ndarray):
        self.vocab = vocab
        self.idx = {w: i for i, w in enumerate(vocab)}
        self.X = X

    def axis(self, neg: Sequence[str], pos: Sequence[str]
             ) -> Optional[np.ndarray]:
        """
        A named direction in the corpus embedding, from ONE seed pair.
        This is the whole authored surface: two short word lists.
        """
        n = [self.X[self.idx[w]] for w in neg if w in self.idx]
        p = [self.X[self.idx[w]] for w in pos if w in self.idx]
        if not n or not p:
            return None
        v = np.mean(p, axis=0) - np.mean(n, axis=0)
        nv = np.linalg.norm(v)
        return v / nv if nv > 1e-8 else None

    def position(self, words: Sequence[str], axis: np.ndarray
                 ) -> List[Tuple[str, float]]:
        out = []
        for w in words:
            i = self.idx.get(w)
            if i is not None:
                out.append((w, float(self.X[i] @ axis)))
        out.sort(key=lambda kv: kv[1])
        return out

    def typed_slot(self, family: Sequence[str], axis: np.ndarray,
                   want: str = "low", k: int = 6) -> List[Tuple[str, float]]:
        """
        SLOT COMPLETION: given a family and a constraint on one of its axes,
        return the admissible fillers, ranked. This is the transformer
        replacement -- a typed constraint, not a softmax over everything.
        """
        pos = self.position(family, axis)
        return pos[:k] if want == "low" else pos[::-1][:k]


def main() -> None:
    print("=" * 74)
    print("CONCEPT FAMILIES FROM A DICTIONARY, AXES FROM THE CORPUS")
    print("=" * 74)

    print("the dictionary has already done the reduction:")
    for w in ("hut", "house", "cottage", "bread", "soup"):
        chain = hypernym_address(w)
        if chain:
            print(f"    {w:<9} " + " -> ".join(chain[-5:]))
    print()

    tokens = read_corpus()
    counts = collections.Counter(tokens)
    vocab = [w for w, c in counts.most_common(12000) if len(w) > 1]
    C = cooccurrence(tokens, vocab, 5)
    X = embed(C, 100).astype(np.float32)
    ft = FamilyTensor(vocab, X)
    print(f"corpus vocabulary embedded: {len(vocab)}")
    print()

    for root, axis_name in (("shelter", "size"), ("shelter", "complexity"),
                            ("food", "size")):
        fam = family_members(root)
        present = [w for w in fam if w in ft.idx]
        neg, pos = AXES[axis_name]
        ax = ft.axis(neg, pos)
        if ax is None or len(present) < 6:
            print(f"{root}/{axis_name}: insufficient coverage "
                  f"({len(present)} members in corpus)")
            continue

        print("-" * 74)
        print(f"FAMILY '{root}'  ({len(fam)} lemmas in WordNet, "
              f"{len(present)} present in corpus)")
        print(f"AXIS '{axis_name}'  seeded by {neg} <-> {pos}")
        ranked = ft.position(present, ax)
        print(f"    lowest : " + ", ".join(f"{w}" for w, _ in ranked[:8]))
        print(f"    highest: " + ", ".join(f"{w}" for w, _ in ranked[-8:]))
        print()

    print("-" * 74)
    print("TYPED SLOT COMPLETION (scope Section 15)")
    fam = [w for w in family_members("shelter") if w in ft.idx]
    ax = ft.axis(*AXES["size"])
    if ax is not None and fam:
        lo = ft.typed_slot(fam, ax, "low")
        hi = ft.typed_slot(fam, ax, "high")
        print("    'he lived in a small ___'  ->  " +
              ", ".join(f"{w}" for w, _ in lo))
        print("    'he lived in a large ___'  ->  " +
              ", ".join(f"{w}" for w, _ in hi))
    food = set(family_members("food"))
    print(f"    'he ate a ___'  -> SUSTENANCE family only. "
          f"'house' admissible? {'house' in food}")
    print("       (a transformer gives that low probability; "
          "this gives it ZERO by type)")


if __name__ == "__main__":
    main()
