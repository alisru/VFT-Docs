"""
Build and TEST a structured training set.

WHAT A TRAINING SET HAS TO BE HERE
----------------------------------
The three-term objective is L = L_CE + lambda_geo*L_resonance + lambda_anchor*L_anchor.

  L_CE         needs a text corpus. Any corpus. Not the hard part.
  L_resonance  needs no data at all; it is geometry.
  L_anchor     needs (word -> 7 plane scores) pairs, and this is the hard part,
               because the anchor term is what stops gradient descent from
               using the frozen axes for whatever it likes and leaving the
               names as decoration.

So the training set that matters is the ANCHOR SET, and the point of
tautonic.py is that it can be generated mechanically from the character
tensor instead of hand-authored. This script builds it and then tries to
break it.

THE TEST THAT MATTERS
---------------------
An anchor set is only useful if it carries information. Two failure modes:

  1. COLLISION. If many distinct words map to the same 7-vector, the anchor
     term pins them to the same place and destroys the distinctions the model
     needs. Measured as distinct-vectors / distinct-words.

  2. ORDER BLINDNESS. The current decomposition SUMS character contributions,
     so it is a bag of characters. Anagrams must collide by construction.
     If 'listen' and 'silent' are identical, the decomposition has thrown away
     the thing that Q1 was supposed to be: the string as identity.

Both are measured below. Neither is assumed.
"""

from __future__ import annotations

import collections
import json
import os
import re
from typing import Dict, List, Tuple

from qqci_engine import Plane
from tautonic import decompose, SPECTRUM

CORPUS_DIR = "/sessions/admiring-sweet-albattani/mnt/_VFT MD"
OUT = "anchor_set.jsonl"

WORD_RE = re.compile(r"[a-z]{2,}")
STOP = set("""the a an and or but if of to in on at by for with from as is are
was were be been being do does did have has had will would can could shall
should may might must not no yes it its this that these those there here
they them their he she his her him we us our you your i me my""".split())


def harvest_vocab(limit_files: int = 400, min_count: int = 3
                  ) -> collections.Counter:
    """Vocabulary from the user's own corpus: domain-matched by construction."""
    counts: collections.Counter = collections.Counter()
    seen = 0
    for root, _dirs, files in os.walk(CORPUS_DIR):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            seen += 1
            if seen > limit_files:
                break
            try:
                with open(os.path.join(root, fn), "r", encoding="utf-8",
                          errors="ignore") as fh:
                    for w in WORD_RE.findall(fh.read().lower()):
                        if w not in STOP:
                            counts[w] += 1
            except OSError:
                continue
        if seen > limit_files:
            break
    return collections.Counter({w: c for w, c in counts.items()
                                if c >= min_count})


def build_anchors(vocab: List[str]) -> Dict[str, Dict]:
    anchors = {}
    for w in vocab:
        d = decompose(w)
        s = d.scores
        anchors[w] = {
            "word": w,
            "scores": {p.name: round(s[p], 2) for p in sorted(s)},
            "scope": d.scope,
            "address": str(d.address),
            "r_net": round(d.r_net(), 4),
        }
    return anchors


def vec(a: Dict) -> Tuple[float, ...]:
    return tuple(a["scores"][p] for p in
                 ["WHAT", "WHERE", "WHY", "HOW", "CAUSE", "EFFECT"])


def test_collision(anchors: Dict[str, Dict]) -> str:
    buckets: Dict[Tuple, List[str]] = {}
    for w, a in anchors.items():
        buckets.setdefault(vec(a), []).append(w)
    distinct = len(buckets)
    n = len(anchors)
    worst = sorted(buckets.items(), key=lambda kv: -len(kv[1]))[:3]

    lines = ["TEST 1: COLLISION",
             f"  words                : {n}",
             f"  distinct 7-vectors   : {distinct}",
             f"  information retention: {distinct / n:.4f}  "
             f"(1.0 = every word unique)",
             f"  mean words per vector: {n / distinct:.1f}"]
    lines.append("  largest collision buckets:")
    for v, ws in worst:
        lines.append(f"    {len(ws):5d} words share {v}")
        lines.append(f"          e.g. {', '.join(ws[:10])}")
    return "\n".join(lines)


def test_order_blindness(anchors: Dict[str, Dict]) -> str:
    """Anagrams must collide if the decomposition is a bag of characters."""
    by_sorted: Dict[str, List[str]] = {}
    for w in anchors:
        by_sorted.setdefault("".join(sorted(w)), []).append(w)
    anagram_sets = {k: v for k, v in by_sorted.items() if len(v) > 1}

    identical = 0
    total = 0
    examples = []
    for k, ws in anagram_sets.items():
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                total += 1
                if vec(anchors[ws[i]]) == vec(anchors[ws[j]]):
                    identical += 1
                    if len(examples) < 8:
                        examples.append((ws[i], ws[j]))

    lines = ["TEST 2: ORDER BLINDNESS (anagrams)",
             f"  anagram pairs found      : {total}",
             f"  pairs with IDENTICAL vec : {identical}"]
    if total:
        lines.append(f"  order information lost   : {identical / total:.1%}")
    for a, b in examples:
        lines.append(f"    '{a}' == '{b}'")
    lines.append("  NOTE: Q1 (the string) still distinguishes them, because the")
    lines.append("  string IS the identity. But the six PAIRED planes cannot,")
    lines.append("  so any anchor term built on them alone under-constrains.")
    return "\n".join(lines)


def test_spread(anchors: Dict[str, Dict]) -> str:
    """Are the scores actually using the range, or bunched at Unity?"""
    per_plane: Dict[str, collections.Counter] = {}
    for a in anchors.values():
        for p, s in a["scores"].items():
            per_plane.setdefault(p, collections.Counter())[s] += 1

    lines = ["TEST 3: SCORE SPREAD (is the ladder used?)"]
    ladder = sorted(SPECTRUM.values())
    lines.append("  plane     " + "".join(f"{v:>7.2f}" for v in ladder))
    for p in ["WHAT", "WHERE", "WHY", "HOW", "CAUSE", "EFFECT"]:
        c = per_plane.get(p, collections.Counter())
        tot = sum(c.values()) or 1
        row = "".join(f"{100*c.get(v,0)/tot:6.1f}%" for v in ladder)
        lines.append(f"  {p:<10}{row}")
    lines.append("  (percentages per plane; heavy mass at 1.00 means the plane")
    lines.append("   is rarely engaged and contributes little to the anchor)")
    return "\n".join(lines)


def test_scope(anchors: Dict[str, Dict]) -> str:
    c = collections.Counter(a["scope"] for a in anchors.values())
    tot = sum(c.values())
    lines = ["TEST 4: ENCAPSULATION SCOPE (the noun-structure axis)"]
    for k, v in c.most_common():
        lines.append(f"  {k:<12}{v:6d}  {100*v/tot:5.1f}%")
    return "\n".join(lines)


def main() -> None:
    print("harvesting vocabulary from the corpus...")
    counts = harvest_vocab()
    vocab = [w for w, _ in counts.most_common()]
    print(f"  {len(vocab)} word types (count >= 3)\n")

    anchors = build_anchors(vocab)
    with open(OUT, "w", encoding="utf-8") as fh:
        for a in anchors.values():
            fh.write(json.dumps(a) + "\n")
    print(f"wrote {OUT}  ({len(anchors)} anchors)\n")

    for t in (test_collision, test_order_blindness, test_spread, test_scope):
        print(t(anchors))
        print()


if __name__ == "__main__":
    main()
