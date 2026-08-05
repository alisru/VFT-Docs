"""
THE SAME TESTS, AT DEPTH. Q.q.c, not Q.

WHY THIS FILE EXISTS (an error, recorded rather than quietly patched)
--------------------------------------------------------------------
run_experiments.py H1/H2/H3 used `int(plane)` -- ONE OF SEVEN. That is flat 7,
which HANDOVER.md names explicitly as the strawman:

    "FLAT 7 DOES NOT WORK. SVD-7 scores 728 vs unigram 736 -- seven dimensions
     retain only 2% of what context provides. 49 dims retain 48%, 343 retain
     82%. The recursion is not decoration; it is doing all the work. The
     operative unit is Q.q.c, never Q."

bottleneck_test.py reproduces those exact numbers on this machine. So H2's
null result ("named planes do not beat random 7-way classes") was never
evidence about the plane structure: it re-derives the known fact that SEVEN
DIMENSIONS ARE TOO FEW, whatever they are named. A flat-7 null cannot license
any conclusion about Qqci, and the conclusion drawn from it in LANGUAGE_SPEC
17.2 was wrong.

THE HONEST ADDRESS, DERIVED NOT AUTHORED
-----------------------------------------
The NSM reduction dictionary already contains three levels, and none of them
were invented for this test:

    Q  = the PLANE of the NSM base          (7 values; from BASE_PLANE)
    q  = WHICH BASE within that plane       (2-6 per plane, fits 7)
    c  = the DEGREE on the spectrum         (-3..+3 = EXACTLY 7 values)

`feel---` is Q7(Effect) . q(feel) . c(-3). That is a genuine Q.q.c address for
151 words, read off a dictionary written years ago for translation work.

THE PREDICTION THE PROJECT MAKES
--------------------------------
If the recursion is doing the work, the named structure should beat random
partitions MORE at depth 2 and 3 than at depth 1, because depth is where the
retained signal lives (2% -> 48% -> 82%). If named cells are indistinguishable
from random cells at EVERY depth, that is a real negative. If they separate
only at depth, flat-7 was the strawman and the recursion is load-bearing.

HONEST LIMITATION, STATED UP FRONT
----------------------------------
151 labelled word types over 343 cells is sparse: most depth-3 cells hold zero
or one word. Depth-3 estimates are therefore weak and are reported with their
occupancy so the reader can discount them. Depth 2 (49 cells, ~3 words/cell)
is the strongest honestly-supported test here. This is a data-coverage limit,
not a result.
"""

from __future__ import annotations

import collections
import math
import random
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from q4_meaning import BASE_PLANE, load_dictionary
from qqci_engine import Plane
from run_experiments import read_corpus

SEED = 0
DEGREES = [-3, -2, -1, 0, 1, 2, 3]     # the c level: exactly 7


def qqc_addresses() -> Dict[str, Tuple[int, int, int]]:
    """
    word -> (Q, q, c), each in 0..6.

    Q  plane of the base
    q  index of the base WITHIN its plane (stable, alphabetical)
    c  degree, mapped -3..+3 -> 0..6
    """
    forms = load_dictionary()
    # bases grouped by plane, alphabetical so the q index is deterministic
    by_plane: Dict[Plane, List[str]] = collections.defaultdict(list)
    for base, plane in BASE_PLANE.items():
        by_plane[plane].append(base)
    q_index: Dict[str, int] = {}
    for plane, bases in by_plane.items():
        for i, b in enumerate(sorted(bases)):
            q_index[b] = i % 7

    out: Dict[str, Tuple[int, int, int]] = {}
    for w, f in forms.items():
        plane = BASE_PLANE.get(f.base)
        if plane is None:
            continue
        c = max(-3, min(3, f.degree)) + 3
        out[w] = (int(plane) - 1, q_index[f.base], c)
    return out


def cell_id(addr: Tuple[int, int, int], depth: int) -> int:
    """Address -> flat cell index at the given depth (7, 49, or 343)."""
    Q, q, c = addr
    if depth == 1:
        return Q
    if depth == 2:
        return Q * 7 + q
    return Q * 49 + q * 7 + c


def shared_prefix(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> int:
    """
    How many leading address positions two words share: 0..3.

    This is fractal_basis.shared_subobjects applied to real words: two cells
    are related exactly when they share sub-objects, and the strength is how
    many. Flat 7 can only see prefix 0 vs >0, which is why it discards almost
    everything the address carries.
    """
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


# ---------------------------------------------------------------------------
# D1: graded relatedness of adjacent words (H1 done properly)
# ---------------------------------------------------------------------------

def d1_graded_adjacency(tokens: Sequence[str],
                        addrs: Dict[str, Tuple[int, int, int]]
                        ) -> Dict[str, object]:
    pairs = [(addrs[a], addrs[b]) for a, b in zip(tokens, tokens[1:])
             if a in addrs and b in addrs]
    if len(pairs) < 100:
        return {"n": len(pairs)}

    real = collections.Counter(shared_prefix(a, b) for a, b in pairs)
    rng = random.Random(SEED)
    right = [b for _, b in pairs]
    left = [a for a, _ in pairs]
    trials: List[collections.Counter] = []
    for _ in range(20):
        sh = right[:]
        rng.shuffle(sh)
        trials.append(collections.Counter(
            shared_prefix(a, b) for a, b in zip(left, sh)))

    n = len(pairs)
    rows = []
    for k in (0, 1, 2, 3):
        r = real[k] / n
        vals = [t[k] / n for t in trials]
        m = sum(vals) / len(vals)
        sd = (sum((v - m) ** 2 for v in vals) / max(1, len(vals) - 1)) ** 0.5
        rows.append((k, r, m, sd, (r - m) / sd if sd > 1e-12 else 0.0))
    return {"n": n, "rows": rows}


# ---------------------------------------------------------------------------
# D2: named cells vs random cells, AT EACH DEPTH (H2 done properly)
# ---------------------------------------------------------------------------

def _class_bigram_perplexity(seq: Sequence[int], n_classes: int,
                             alpha: float = 0.5) -> Optional[float]:
    if len(seq) < 200:
        return None
    split = int(len(seq) * 0.9)
    train, test = seq[:split], seq[split:]
    C = np.zeros((n_classes, n_classes), dtype=np.float64)
    for a, b in zip(train, train[1:]):
        C[a, b] += 1.0
    P = C + alpha
    P /= P.sum(axis=1, keepdims=True)
    logp = sum(math.log(P[a, b]) for a, b in zip(test, test[1:]))
    return math.exp(-logp / max(1, len(test) - 1))


def d2_named_vs_random(tokens: Sequence[str],
                       addrs: Dict[str, Tuple[int, int, int]],
                       depth: int, n_random: int = 200) -> Dict[str, float]:
    n_cells = 7 ** depth
    named = {w: cell_id(a, depth) for w, a in addrs.items()}
    seq = [named[t] for t in tokens if t in named]
    pp_named = _class_bigram_perplexity(seq, n_cells)
    if pp_named is None:
        return {}

    occupied = len(set(named.values()))
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
        pp = _class_bigram_perplexity([rand[t] for t in tokens if t in rand],
                                      n_cells)
        if pp is not None:
            scores.append(pp)
    arr = np.array(scores)
    better = int((arr <= pp_named).sum())
    return {"depth": depth, "cells": n_cells, "occupied": occupied,
            "words_per_occupied": len(named) / max(1, occupied),
            "pp_named": pp_named, "pp_random_mean": float(arr.mean()),
            "pp_random_sd": float(arr.std(ddof=1)),
            "pp_random_best": float(arr.min()),
            "n_random": len(scores), "better_or_equal": better,
            "p_value": (better + 1) / (len(scores) + 1),
            "z": float((pp_named - arr.mean()) / arr.std(ddof=1))}


# ---------------------------------------------------------------------------
# D3: does SUB-OBJECT SHARING predict co-occurrence? (the recursion's own claim)
#
# fractal_basis.sharing_graph says two cells are linked exactly when they share
# sub-objects, and the link strength is HOW MANY. That is a prediction about
# real words that flat 7 cannot even express: words sharing Q.q should
# co-occur more than words sharing only Q, which should beat sharing nothing.
# ---------------------------------------------------------------------------

def d3_sharing_predicts_cooccurrence(tokens: Sequence[str],
                                     addrs: Dict[str, Tuple[int, int, int]],
                                     window: int = 5) -> Dict[str, object]:
    idx = {w: i for i, w in enumerate(addrs)}
    words = list(addrs)
    n = len(words)
    co = np.zeros((n, n), dtype=np.float64)
    buf: List[int] = []
    for t in tokens:
        if t not in idx:
            continue
        i = idx[t]
        for j in buf[-window:]:
            co[i, j] += 1.0
            co[j, i] += 1.0
        buf.append(i)

    tot = co.sum()
    if tot < 100:
        return {}
    by_share: Dict[int, List[float]] = collections.defaultdict(list)
    for i in range(n):
        for j in range(i + 1, n):
            k = shared_prefix(addrs[words[i]], addrs[words[j]])
            by_share[k].append(co[i, j])
    rows = []
    for k in (0, 1, 2, 3):
        v = by_share.get(k, [])
        if v:
            rows.append((k, len(v), float(np.mean(v))))
    return {"rows": rows, "total_cooccurrence": float(tot)}


def main() -> None:
    print("=" * 74)
    print("DEPTH TESTS  --  Q.q.c (343), not flat Q (7)")
    print("=" * 74)
    print("Flat 7 is the strawman HANDOVER.md names; bottleneck_test.py")
    print("measures it at 2% retention vs 82% for 343. These are the same")
    print("questions asked at the depth the project actually claims.")
    print()

    tokens = read_corpus()
    addrs = qqc_addresses()
    print(f"corpus tokens        : {len(tokens):,}")
    print(f"words with Q.q.c     : {len(addrs)}")
    print(f"labelled tokens      : "
          f"{sum(1 for t in tokens if t in addrs):,}")
    print()

    print("-" * 74)
    print("D1  graded adjacency: how much address do adjacent words SHARE?")
    print("    (flat 7 can only see prefix 0 vs >0 and discards the rest)")
    r1 = d1_graded_adjacency(tokens, addrs)
    if r1.get("n", 0) < 100:
        print(f"    INSUFFICIENT DATA (n={r1.get('n', 0)})")
    else:
        print(f"    pairs: {r1['n']:,}")
        print(f"    {'shared':<8}{'real':>10}{'shuffled':>12}{'sd':>9}{'z':>9}")
        for k, r, m, sd, z in r1["rows"]:
            lbl = {0: "none", 1: "Q", 2: "Q.q", 3: "Q.q.c"}[k]
            print(f"    {lbl:<8}{r:>10.4f}{m:>12.4f}{sd:>9.4f}{z:>+9.2f}")
    print()

    print("-" * 74)
    print("D2  named cells vs RANDOM cells of identical size, PER DEPTH")
    print("    prediction: separation should grow with depth if the")
    print("    recursion is load-bearing rather than decorative")
    print()
    for depth in (1, 2, 3):
        r = d2_named_vs_random(tokens, addrs, depth)
        if not r:
            print(f"    depth {depth}: INSUFFICIENT DATA")
            continue
        print(f"    depth {depth}  ({r['cells']} cells, {r['occupied']} occupied, "
              f"{r['words_per_occupied']:.1f} words/occupied cell)")
        print(f"      named           : {r['pp_named']:.3f}")
        print(f"      random          : {r['pp_random_mean']:.3f} "
              f"(sd {r['pp_random_sd']:.3f}, best {r['pp_random_best']:.3f})")
        print(f"      random >= named : {r['better_or_equal']}/{r['n_random']}"
              f"   p = {r['p_value']:.4f}   z = {r['z']:+.2f}")
        verdict = ("NAMED BEATS RANDOM" if r["p_value"] <= 0.05
                   else "not distinguishable")
        print(f"      -> {verdict}")
        if r["words_per_occupied"] < 2.0:
            print("      (WARNING: under 2 words per cell -- estimate is weak)")
        print()

    print("-" * 74)
    print("D3  does SUB-OBJECT SHARING predict co-occurrence?")
    print("    fractal_basis: cells are linked when they share sub-objects,")
    print("    strength = how many. Flat 7 cannot express this at all.")
    r3 = d3_sharing_predicts_cooccurrence(tokens, addrs)
    if not r3:
        print("    INSUFFICIENT DATA")
    else:
        print(f"    {'shared':<8}{'pairs':>10}{'mean co-occur':>16}")
        for k, cnt, mean in r3["rows"]:
            lbl = {0: "none", 1: "Q", 2: "Q.q", 3: "Q.q.c"}[k]
            print(f"    {lbl:<8}{cnt:>10,}{mean:>16.3f}")
        vals = [m for _, _, m in r3["rows"]]
        rising = all(b >= a for a, b in zip(vals, vals[1:]))
        print(f"    monotonic in shared depth: {rising}")


if __name__ == "__main__":
    main()
