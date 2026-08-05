"""
EXPAND THE WHOLE DICTIONARY. All senses, all reductions, all fundamentals.

Not two families as a demo -- the entire lexicon reduced to its roots, with the
axis words pulled from the definitions themselves.

WHAT THIS PRODUCES
------------------
  1. Every sense's REDUCTION CHAIN   hut -> shelter -> structure -> artifact
  2. The FUNDAMENTALS                the unique beginners the whole tree
                                     bottoms out on (WordNet's own TBE floor)
  3. FAMILIES at a chosen cut        every subtree under a fundamental
  4. TYPED AXES FROM GLOSSES         the size/quality word is usually IN the
                                     definition ("a LARGE and imposing house",
                                     "a SMALL crude shelter"), so positions come
                                     from the dictionary, not from a corpus that
                                     may not discuss the subject at all
  5. The xy TENSOR per node          each cell is a coordinate space (two typed
                                     axes), not a scalar

WHY GLOSSES AND NOT THE CORPUS
------------------------------
MEASURED, concept_families.py: projecting shelter words onto a corpus-derived
size direction returned noise (lowest "refuge, asylum, sanctuary", highest
"harbour, top, canvas"), because the VFT corpus is philosophical writing with
only 9 of 37 shelter lemmas present and nothing about physical size. The
dictionary states the magnitude in the definition. Use the dictionary.

THE FUNDAMENTALS ARE ALREADY THERE
----------------------------------
WordNet's noun hierarchy terminates in a small set of unique beginners. That is
the enumerable TBE floor of scope Section 8 -- "fundamentals are hit" becomes a
membership test, on a real lexicon, for the whole language rather than for a
seeded alphabet.
"""

from __future__ import annotations

import collections
import json
import os
import re
from typing import Dict, List, Optional, Sequence, Set, Tuple

from nltk.corpus import wordnet as wn

OUT = os.path.join(os.path.dirname(__file__), "dictionary_expanded.json")

# The only authored surface: which adjectives name a position on which axis.
# Two short lists per axis, applied to definition text.
AXIS_WORDS: Dict[str, Dict[str, List[str]]] = {
    "size": {
        "low":  ["small", "tiny", "little", "miniature", "narrow", "short",
                 "minor", "slight", "compact", "dwarf"],
        "high": ["large", "big", "huge", "great", "vast", "immense", "giant",
                 "massive", "enormous", "tall", "broad", "major"],
    },
    "complexity": {
        "low":  ["simple", "crude", "basic", "plain", "rough", "primitive",
                 "rude", "bare", "temporary", "makeshift"],
        "high": ["complex", "elaborate", "ornate", "sophisticated", "imposing",
                 "luxurious", "grand", "formal", "permanent", "detailed"],
    },
    "benefit": {   # the morality spread: everyone <-> no-one else
        "low":  ["harmful", "destructive", "damaging", "hostile", "evil",
                 "malicious", "selfish", "parasitic"],
        "high": ["beneficial", "helpful", "useful", "protective", "nourishing",
                 "generous", "supportive", "healing"],
    },
    "will": {      # active <-> passive/suppressive
        "low":  ["passive", "inert", "static", "dormant", "still", "inactive",
                 "suppressed", "restrained"],
        "high": ["active", "dynamic", "moving", "driving", "energetic",
                 "vigorous", "forceful", "propelling"],
    },
}

WORD_RE = re.compile(r"[a-z]+")


def reduction_chain(syn) -> List[str]:
    paths = syn.hypernym_paths()
    if not paths:
        return [syn.name().split(".")[0]]
    return [s.name().split(".")[0] for s in paths[0]]


def gloss_axis(gloss: str) -> Dict[str, float]:
    """
    Read a sense's position off its own definition.

    "a large and imposing house"  -> size +1, complexity +1
    "a small crude shelter"       -> size -1, complexity -1

    Absence is meaningful and returns nothing, rather than a guessed centre.
    """
    words = set(WORD_RE.findall(gloss.lower()))
    out: Dict[str, float] = {}
    for axis, poles in AXIS_WORDS.items():
        lo = len(words & set(poles["low"]))
        hi = len(words & set(poles["high"]))
        if lo or hi:
            out[axis] = (hi - lo) / (hi + lo)
    return out


def expand(pos_list: Sequence[str] = ("n", "v", "a")) -> Dict[str, object]:
    senses: Dict[str, dict] = {}
    roots: collections.Counter = collections.Counter()
    depth_hist: collections.Counter = collections.Counter()
    axis_hits: collections.Counter = collections.Counter()

    for pos in pos_list:
        for syn in wn.all_synsets(pos):
            chain = reduction_chain(syn)
            name = syn.name()
            g = syn.definition() or ""
            ax = gloss_axis(g)
            for a in ax:
                axis_hits[a] += 1
            roots[chain[0]] += 1
            depth_hist[len(chain)] += 1
            senses[name] = {
                "pos": pos,
                "lemmas": [l.name().lower() for l in syn.lemmas()],
                "chain": chain,
                "depth": len(chain),
                "gloss": g,
                "axes": ax,
            }
    return {"senses": senses, "roots": roots, "depths": depth_hist,
            "axis_hits": axis_hits}


def families_at(senses: Dict[str, dict], cut: int = 3
                ) -> Dict[str, List[str]]:
    """
    Cut the forest at a fixed depth. Everything below a node at that depth is
    one FAMILY -- the level at which 'shelter' and 'food' live.
    """
    fam: Dict[str, List[str]] = collections.defaultdict(list)
    for name, rec in senses.items():
        chain = rec["chain"]
        if len(chain) > cut:
            fam[chain[cut]].append(name)
        elif chain:
            fam[chain[-1]].append(name)
    return fam


def axis_positions(senses: Dict[str, dict], members: Sequence[str],
                   axis: str) -> List[Tuple[str, float]]:
    out = []
    for m in members:
        v = senses[m]["axes"].get(axis)
        if v is not None:
            out.append((senses[m]["lemmas"][0], v))
    out.sort(key=lambda kv: kv[1])
    return out


def main() -> None:
    print("=" * 74)
    print("EXPANDING THE WHOLE DICTIONARY")
    print("=" * 74)

    data = expand()
    senses = data["senses"]
    roots = data["roots"]
    print(f"senses expanded      : {len(senses):,}")
    print(f"distinct reductions  : every sense carries its chain to a root")
    print(f"depth of reduction   : min {min(data['depths'])}, "
          f"max {max(data['depths'])}, "
          f"mode {data['depths'].most_common(1)[0][0]}")
    print()

    print("THE FUNDAMENTALS (WordNet's unique beginners = the TBE floor)")
    print(f"    {len(roots)} roots for {len(senses):,} senses")
    for r, c in roots.most_common(12):
        print(f"      {r:<22} {c:>6,} senses reduce to this")
    print()

    fam = families_at(senses, cut=3)
    big = sorted(fam.items(), key=lambda kv: -len(kv[1]))
    print(f"FAMILIES at cut depth 3: {len(fam)}")
    for name, members in big[:14]:
        print(f"      {name:<24} {len(members):>6,} senses")
    print()

    print("AXIS COVERAGE FROM GLOSSES (position read from the definition)")
    for a, c in data["axis_hits"].most_common():
        print(f"      {a:<12} {c:>6,} senses state a position on this axis")
    print()

    print("-" * 74)
    print("WORKED FAMILIES: position read from the dictionary's own words")
    for probe in ("structure", "food", "person", "communication"):
        members = None
        for name, mem in fam.items():
            if name == probe:
                members = mem
                break
        if not members:
            continue
        for axis in ("size", "complexity"):
            pos = axis_positions(senses, members, axis)
            if len(pos) < 6:
                continue
            print(f"  {probe} / {axis}  ({len(pos)} senses positioned)")
            print(f"    low : " + ", ".join(w for w, _ in pos[:9]))
            print(f"    high: " + ", ".join(w for w, _ in pos[-9:]))
        print()

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({k: v for k, v in list(senses.items())}, fh)
    print(f"written: {OUT}  ({os.path.getsize(OUT)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
