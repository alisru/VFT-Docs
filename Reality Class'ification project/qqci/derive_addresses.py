"""
WORD -> Q.q.c, DERIVED FROM CO-OCCURRENCE. Full vocabulary, depth 3, no
spelling and no hand-authoring.

WHY THIS EXISTS
---------------
Every address source in the project was unusable for a real 343 test:

  NSM (q4_meaning.py)      151 words. Real Q.q.c, but 151 words over 343 cells
                           is 0.4 words per cell. Arithmetic, not a finding.
  anchor_set.jsonl         14,258 words, but built by build_trainset.py from
                           `tautonic.decompose` -- THE CHARACTER TENSOR, which
                           the handover records as measured useless for meaning
                           (same-type vs different-type cosine gap +0.042 =
                           noise; PLANE-7 at 12.9% of the way to optimal).
                           It collapses: FIVE distinct addresses for 14,258
                           words, 7,335 of them in a single cell.

HANDOVER.md already said where addresses must come from:

    "Plane scores must come from the CO-OCCURRENCE distribution (where the
     predictive signal demonstrably lives), not from spelling and not from
     hand-authoring."

and bottleneck_test.py measured that the signal is there: 343 dimensions of
co-occurrence retain 82% of what context provides.

THE CONSTRUCTION
----------------
A Qqci address is recursive same-kind: Q, then q within Q, then c within Q.q.
So the assignment is a 7-ary tree of depth 3, and each level is the same
operation applied to a smaller pool -- which is exactly the bounded-pool
recursion the cowork thread specified ("the accreted information is a new
bounded space to perform new TS===TBE across the fractal qqci... a smaller
pool of info for more ordered events").

  1. PPMI-weighted co-occurrence over a symmetric window.
  2. SVD to a dense space (the 82%-retaining representation).
  3. k-means with k=7 -> the Q level.
  4. Recurse INSIDE each cell -> the q level. Recurse again -> the c level.

Every word in the vocabulary gets a full (Q, q, c). With a 3000-word
vocabulary that is ~9 words per cell, which is real coverage rather than 0.4.

WHAT THIS IS AND IS NOT
-----------------------
IS: a mechanical, reproducible word-to-cell assignment from distribution,
which is what the project has wanted since the handover named it "THE
unsolved problem".
IS NOT: named. The clusters are numbered, not interpreted. Attaching the
seven interrogatives to the seven top-level clusters is a SEPARATE claim that
needs its own evidence (see validate.py / D-tests). Naming them here would be
exactly the hand-authoring this file exists to avoid.
"""

from __future__ import annotations

import collections
import math
import os
import re
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

CORPUS_DIR = r"E:\Vector Field Theory\VFT Docs\_VFT MD"
WORD_RE = re.compile(r"[a-z']+")
SEED = 0

# The corpus contains the dictionaries that other parts of this project draw
# labels from; excluded so no test can be contaminated by their formatting.
EXCLUDE_PATH = ("nsm_reduction", "translating", "dictionary", "isomorphic")


def _excluded(path: str) -> bool:
    low = path.lower().replace("\\", "/")
    return any(tag in low for tag in EXCLUDE_PATH)


def read_corpus(limit_files: int = 1400) -> List[str]:
    toks: List[str] = []
    seen = 0
    for root, _d, files in os.walk(CORPUS_DIR):
        if _excluded(root):
            continue
        for fn in files:
            if not fn.endswith(".md") or _excluded(fn):
                continue
            seen += 1
            if seen > limit_files:
                return toks
            try:
                with open(os.path.join(root, fn), "r", encoding="utf-8",
                          errors="ignore") as fh:
                    toks.extend(WORD_RE.findall(fh.read().lower()))
            except OSError:
                continue
    return toks


# ---------------------------------------------------------------------------
# REPRESENTATION: PPMI + SVD (where the 82% lives)
# ---------------------------------------------------------------------------

def cooccurrence(tokens: Sequence[str], vocab: List[str], window: int = 5
                 ) -> np.ndarray:
    idx = {w: i for i, w in enumerate(vocab)}
    V = len(vocab)
    C = np.zeros((V, V), dtype=np.float32)
    buf: List[int] = []
    for t in tokens:
        i = idx.get(t)
        if i is None:
            continue
        for j in buf[-window:]:
            C[i, j] += 1.0
            C[j, i] += 1.0
        buf.append(i)
        if len(buf) > window:
            buf.pop(0)
    return C


def ppmi(C: np.ndarray) -> np.ndarray:
    """Positive pointwise mutual information: the standard fix for raw counts
    over-weighting frequent words."""
    total = C.sum()
    if total <= 0:
        return C
    row = C.sum(axis=1, keepdims=True)
    col = C.sum(axis=0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        M = np.log((C * total) / (row * col + 1e-12) + 1e-12)
    return np.maximum(M, 0.0)


def embed(C: np.ndarray, dim: int = 100) -> np.ndarray:
    M = ppmi(C)
    U, S, _ = np.linalg.svd(M, full_matrices=False)
    k = min(dim, len(S))
    X = U[:, :k] * np.sqrt(S[:k])
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    return X / np.maximum(norms, 1e-9)


# ---------------------------------------------------------------------------
# RECURSIVE 7-WAY PARTITION: the address IS the tree path
# ---------------------------------------------------------------------------

def kmeans(X: np.ndarray, k: int, seed: int = SEED, iters: int = 60
           ) -> np.ndarray:
    """Plain k-means with k-means++ init. Returns a label per row."""
    n = X.shape[0]
    if n <= k:
        return np.arange(n) % k
    rng = np.random.default_rng(seed)
    # k-means++ seeding
    centres = [X[rng.integers(n)]]
    for _ in range(k - 1):
        d = np.min(np.stack([((X - c) ** 2).sum(1) for c in centres]), axis=0)
        probs = d / max(d.sum(), 1e-12)
        centres.append(X[rng.choice(n, p=probs)])
    Cn = np.stack(centres)

    labels = np.zeros(n, dtype=int)
    for _ in range(iters):
        d = ((X[:, None, :] - Cn[None, :, :]) ** 2).sum(-1)
        new = d.argmin(1)
        if np.array_equal(new, labels):
            break
        labels = new
        for c in range(k):
            m = labels == c
            if m.any():
                Cn[c] = X[m].mean(0)
    return labels


def recursive_address(X: np.ndarray, depth: int = 3, k: int = 7,
                      seed: int = SEED) -> List[Tuple[int, ...]]:
    """
    Assign every row a depth-`depth` address by recursively partitioning each
    cell into k. This is the bounded-pool recursion: each level operates on a
    smaller, already-ordered pool.
    """
    n = X.shape[0]
    addr: List[List[int]] = [[] for _ in range(n)]
    groups: List[np.ndarray] = [np.arange(n)]
    for level in range(depth):
        nxt: List[np.ndarray] = []
        for gi, g in enumerate(groups):
            if len(g) == 0:
                continue
            lab = kmeans(X[g], k, seed=seed + level * 97 + gi)
            for c in range(k):
                sub = g[lab == c]
                for r in sub:
                    addr[r].append(c)
                nxt.append(sub)
        groups = nxt
    return [tuple(a) for a in addr]


def cell_id(a: Tuple[int, ...], depth: int) -> int:
    out = 0
    for x in a[:depth]:
        out = out * 7 + x
    return out


def shared_prefix(a: Tuple[int, ...], b: Tuple[int, ...]) -> int:
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


# ---------------------------------------------------------------------------

def build(vocab_size: int = 3000, dim: int = 100, window: int = 5
          ) -> Tuple[List[str], Dict[str, Tuple[int, ...]], List[str]]:
    tokens = read_corpus()
    counts = collections.Counter(tokens)
    vocab = [w for w, c in counts.most_common(vocab_size) if len(w) > 1]
    C = cooccurrence(tokens, vocab, window)
    X = embed(C, dim)
    addrs = recursive_address(X, depth=3, k=7)
    return tokens, dict(zip(vocab, addrs)), vocab


def occupancy_report(addrs: Dict[str, Tuple[int, ...]]) -> Dict[str, float]:
    out = {}
    for d in (1, 2, 3):
        cells = collections.Counter(cell_id(a, d) for a in addrs.values())
        out[f"depth{d}_occupied"] = len(cells)
        out[f"depth{d}_possible"] = 7 ** d
        out[f"depth{d}_words_per_cell"] = len(addrs) / max(1, len(cells))
        out[f"depth{d}_largest"] = max(cells.values())
    return out


if __name__ == "__main__":
    print("DERIVING Q.q.c FROM CO-OCCURRENCE (no spelling, no authoring)")
    print("=" * 70)
    tokens, addrs, vocab = build()
    print(f"corpus tokens : {len(tokens):,}")
    print(f"vocabulary    : {len(addrs)}")
    print()
    rep = occupancy_report(addrs)
    for d in (1, 2, 3):
        print(f"  depth {d}: {rep[f'depth{d}_occupied']}/"
              f"{rep[f'depth{d}_possible']} cells occupied, "
              f"{rep[f'depth{d}_words_per_cell']:.1f} words/cell, "
              f"largest {rep[f'depth{d}_largest']}")
    print()
    print("SAMPLE CELLS AT DEPTH 3 (numbered, deliberately NOT named)")
    by_cell: Dict[int, List[str]] = collections.defaultdict(list)
    for w, a in addrs.items():
        by_cell[cell_id(a, 3)].append(w)
    shown = 0
    for cid, ws in sorted(by_cell.items(), key=lambda kv: -len(kv[1])):
        if len(ws) < 4 or shown >= 10:
            continue
        a = next(a for w, a in addrs.items() if cell_id(a, 3) == cid)
        print(f"  Q{a[0]+1}.q{a[1]+1}.c{a[2]+1}  {', '.join(sorted(ws)[:9])}")
        shown += 1
