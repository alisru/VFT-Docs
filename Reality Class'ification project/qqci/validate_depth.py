"""
THE REAL 343 TEST: is the recursion load-bearing, at proper coverage?

Addresses come from derive_addresses.py (co-occurrence, 2973 words, 338/343
cells occupied, 8.8 words/cell). Nothing here uses spelling, NSM, or any
authored label.

HONEST PROTOCOL
---------------
Addresses are derived on the FIRST 90% of the corpus and every number below is
measured on the HELD-OUT LAST 10%. The clustering never sees the test data, so
"words in a cell behave alike" cannot be the clustering read back.

THE QUESTION
------------
Not "do the planes work" -- that was always the wrong question at depth 1.
The question is whether ADDING DEPTH adds structure:

  if the recursion is load-bearing, deeper prefixes predict better, and the
  named-vs-random separation grows from depth 1 to depth 3.

  if the recursion is decoration, depth 1 already has whatever signal exists
  and depths 2 and 3 add nothing beyond finer slicing.

Both are can-fail and they disagree.
"""

from __future__ import annotations

import collections
import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from derive_addresses import (
    cell_id, cooccurrence, embed, read_corpus, recursive_address,
    shared_prefix,
)

SEED = 0


def build_split(vocab_size: int = 3000, dim: int = 100, window: int = 5):
    tokens = read_corpus()
    split = int(len(tokens) * 0.9)
    train, test = tokens[:split], tokens[split:]

    counts = collections.Counter(train)
    vocab = [w for w, c in counts.most_common(vocab_size) if len(w) > 1]
    C = cooccurrence(train, vocab, window)          # TRAIN ONLY
    X = embed(C, dim)
    addrs = dict(zip(vocab, recursive_address(X, depth=3, k=7)))
    return train, test, vocab, addrs


# ---------------------------------------------------------------------------
# V1: does shared address depth predict HELD-OUT co-occurrence?
# ---------------------------------------------------------------------------

def v1_shared_predicts_heldout(test: Sequence[str], vocab: List[str],
                               addrs: Dict[str, Tuple[int, ...]],
                               window: int = 5) -> Dict[str, object]:
    Ct = cooccurrence(test, vocab, window)
    n = len(vocab)
    sums: Dict[int, float] = collections.defaultdict(float)
    cnts: Dict[int, int] = collections.defaultdict(int)
    for i in range(n):
        ai = addrs[vocab[i]]
        for j in range(i + 1, n):
            k = shared_prefix(ai, addrs[vocab[j]])
            sums[k] += Ct[i, j]
            cnts[k] += 1
    rows = [(k, cnts[k], sums[k] / cnts[k]) for k in sorted(cnts) if cnts[k]]
    vals = [m for _, _, m in rows]
    return {"rows": rows, "monotonic": all(b >= a for a, b in zip(vals, vals[1:]))}


# ---------------------------------------------------------------------------
# V2: named cells vs RANDOM cells of identical size, per depth, HELD OUT
# ---------------------------------------------------------------------------

def _class_bigram_pp(seq: Sequence[int], n_classes: int,
                     train_seq: Sequence[int], alpha: float = 0.5
                     ) -> Optional[float]:
    """Fit transition table on TRAIN classes, score HELD-OUT classes."""
    if len(seq) < 200 or len(train_seq) < 200:
        return None
    C = np.zeros((n_classes, n_classes), dtype=np.float64)
    for a, b in zip(train_seq, train_seq[1:]):
        C[a, b] += 1.0
    P = C + alpha
    P /= P.sum(axis=1, keepdims=True)
    logp = sum(math.log(P[a, b]) for a, b in zip(seq, seq[1:]))
    return math.exp(-logp / max(1, len(seq) - 1))


def v2_named_vs_random(train: Sequence[str], test: Sequence[str],
                       addrs: Dict[str, Tuple[int, ...]], depth: int,
                       n_random: int = 100) -> Dict[str, float]:
    n_cells = 7 ** depth
    named = {w: cell_id(a, depth) for w, a in addrs.items()}
    tr = [named[t] for t in train if t in named]
    te = [named[t] for t in test if t in named]
    pp = _class_bigram_pp(te, n_cells, tr)
    if pp is None:
        return {}

    words = list(named)
    sizes = collections.Counter(named.values())
    rng = random.Random(SEED)
    scores = []
    for _ in range(n_random):
        sh = words[:]
        rng.shuffle(sh)
        rand: Dict[str, int] = {}
        i = 0
        for cell, cnt in sizes.items():
            for w in sh[i:i + cnt]:
                rand[w] = cell
            i += cnt
        rtr = [rand[t] for t in train if t in rand]
        rte = [rand[t] for t in test if t in rand]
        p = _class_bigram_pp(rte, n_cells, rtr)
        if p is not None:
            scores.append(p)
    arr = np.array(scores)
    occupied = len(set(named.values()))
    return {"depth": depth, "cells": n_cells, "occupied": occupied,
            "words_per_cell": len(named) / max(1, occupied),
            "pp_named": pp, "pp_random_mean": float(arr.mean()),
            "pp_random_sd": float(arr.std(ddof=1)),
            "pp_random_best": float(arr.min()),
            "n_random": len(scores),
            "better_or_equal": int((arr <= pp).sum()),
            "p_value": (int((arr <= pp).sum()) + 1) / (len(scores) + 1),
            "z": float((pp - arr.mean()) / arr.std(ddof=1)),
            "improvement": float(arr.mean() / pp)}


# ---------------------------------------------------------------------------
# V3: does each ADDED LEVEL buy anything the previous one did not?
#
# The direct test of "the recursion is not decoration": compare predicting the
# held-out next word using the depth-d cell as context. If depth 3 beats depth
# 2 beats depth 1, the recursion carries information. If it flattens, it does
# not.
# ---------------------------------------------------------------------------

def v3_depth_gain(train: Sequence[str], test: Sequence[str],
                  vocab: List[str], addrs: Dict[str, Tuple[int, ...]],
                  alpha: float = 0.1) -> Dict[int, float]:
    idx = {w: i for i, w in enumerate(vocab)}
    V = len(vocab)
    out: Dict[int, float] = {}
    for depth in (0, 1, 2, 3):
        n_cells = 1 if depth == 0 else 7 ** depth
        ctx = ({w: 0 for w in vocab} if depth == 0
               else {w: cell_id(addrs[w], depth) for w in vocab})
        M = np.zeros((n_cells, V), dtype=np.float64)
        for a, b in zip(train, train[1:]):
            if a in ctx and b in idx:
                M[ctx[a], idx[b]] += 1.0
        P = M + alpha
        P /= P.sum(axis=1, keepdims=True)
        logp = cnt = 0.0
        for a, b in zip(test, test[1:]):
            if a in ctx and b in idx:
                logp += math.log(P[ctx[a], idx[b]])
                cnt += 1
        out[depth] = math.exp(-logp / cnt) if cnt else float("inf")
    return out


def main() -> None:
    print("=" * 74)
    print("THE REAL 343 TEST  --  derived addresses, held-out evaluation")
    print("=" * 74)
    train, test, vocab, addrs = build_split()
    print(f"train tokens : {len(train):,}   test tokens : {len(test):,}")
    print(f"vocabulary   : {len(vocab)}")
    occ = collections.Counter(cell_id(a, 3) for a in addrs.values())
    print(f"depth-3 cells: {len(occ)}/343 occupied, "
          f"{len(addrs)/len(occ):.1f} words/cell")
    print("addresses derived on TRAIN ONLY; all numbers below are HELD OUT")
    print()

    print("-" * 74)
    print("V1  does shared address depth predict HELD-OUT co-occurrence?")
    r1 = v1_shared_predicts_heldout(test, vocab, addrs)
    print(f"    {'shared':<10}{'pairs':>12}{'mean co-occur':>16}")
    for k, cnt, mean in r1["rows"]:
        lbl = {0: "none", 1: "Q", 2: "Q.q", 3: "Q.q.c"}[k]
        print(f"    {lbl:<10}{cnt:>12,}{mean:>16.3f}")
    print(f"    monotonic in depth: {r1['monotonic']}")
    if r1["rows"]:
        base = r1["rows"][0][2]
        deep = r1["rows"][-1][2]
        print(f"    deepest / baseline: {deep/max(base,1e-9):.2f}x")
    print()

    print("-" * 74)
    print("V2  named cells vs RANDOM cells of identical size, per depth")
    print("    (does the separation GROW with depth?)")
    print()
    for depth in (1, 2, 3):
        r = v2_named_vs_random(train, test, addrs, depth)
        if not r:
            print(f"    depth {depth}: INSUFFICIENT DATA")
            continue
        print(f"    depth {depth}  ({r['occupied']}/{r['cells']} occupied, "
              f"{r['words_per_cell']:.1f} words/cell)")
        print(f"      named  : {r['pp_named']:.3f}")
        print(f"      random : {r['pp_random_mean']:.3f} "
              f"(sd {r['pp_random_sd']:.3f}, best {r['pp_random_best']:.3f})")
        print(f"      random >= named : {r['better_or_equal']}/{r['n_random']}"
              f"   p = {r['p_value']:.4f}   z = {r['z']:+.2f}")
        print(f"      named is {r['improvement']:.2f}x better than random")
        print()

    print("-" * 74)
    print("V3  does each ADDED LEVEL reduce held-out next-word perplexity?")
    print("    depth 0 = no context (unigram). Lower is better.")
    r3 = v3_depth_gain(train, test, vocab, addrs)
    prev = None
    for d in (0, 1, 2, 3):
        gain = "" if prev is None else f"   ({(prev-r3[d])/prev:+.1%} vs prev)"
        lbl = {0: "no context", 1: "Q  (7)", 2: "Q.q  (49)",
               3: "Q.q.c (343)"}[d]
        print(f"    {lbl:<14}{r3[d]:10.1f}{gain}")
        prev = r3[d]
    improving = all(r3[d] < r3[d - 1] for d in (1, 2, 3))
    print()
    print(f"    monotonically improving with depth: {improving}")
    print("    VERDICT: " + ("RECURSION IS LOAD-BEARING -- each level adds."
                             if improving else
                             "depth stops paying at some level (see above)."))


if __name__ == "__main__":
    main()
