"""
The decisive cheap test: do 7 NAMED planes carry the predictive structure of
language, or not?

THE QUESTION
------------
Next-word prediction is the task. Compress the context through a
7-dimensional bottleneck and measure how much predictive power survives.
Three bottlenecks:

    SVD-7    the top 7 singular directions. The mathematical CEILING: no
             7-dimensional linear compression can beat it.
    PLANE-7  the frozen 7-plane basis, with words assigned to planes by the
             character tensor (the only plane assignment we have).
    RANDOM-7 seven random orthonormal directions. The FLOOR.

If PLANE-7 lands near SVD-7, the planes capture near-optimal predictive
structure and the thesis is supported. If it lands near RANDOM-7, they do not,
and no amount of architecture will fix that.

WHY THIS BEFORE ANY TRAINING RUN
--------------------------------
It costs minutes on CPU and it can falsify the core claim. Every previous
attempt this session tried to hand-populate a lexicon; this asks whether the
geometry is worth populating at all.

HONEST FRAMING OF WHAT IT CAN AND CANNOT SHOW
---------------------------------------------
A weak PLANE-7 result does NOT prove the seven planes are wrong. It proves
that THIS plane assignment (from the character tensor) is wrong, which is
already known: the character tensor was measured useless as a semantic anchor
(gap +0.042). The test is therefore near-worst-case for PLANE-7, and any
result above RANDOM-7 is meaningful while a result near it is uninformative
about the planes themselves.

The unambiguous quantity is SVD-7 vs FULL: how much of language's predictive
structure fits in seven dimensions AT ALL. If that is high, a 7-plane
architecture is viable in principle regardless of our current assignment. If
it is low, seven dimensions is simply too few and the fractal depth is doing
all the work.
"""

from __future__ import annotations

import collections
import math
import os
import re
from typing import Dict, List, Tuple

import numpy as np

from qqci_engine import Plane
from tautonic import ANCHOR_PLANE, CHAR_TENSOR, POLARITY_PUSH

CORPUS_DIR = "/sessions/admiring-sweet-albattani/mnt/_VFT MD"
WORD_RE = re.compile(r"[a-z']+")


def read_corpus(limit_files: int = 250) -> List[str]:
    toks: List[str] = []
    seen = 0
    for root, _d, files in os.walk(CORPUS_DIR):
        for fn in files:
            if not fn.endswith(".md"):
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


def build_matrix(tokens: List[str], vocab_size: int = 3000
                 ) -> Tuple[np.ndarray, List[str], List[Tuple[int, int]]]:
    """
    Co-occurrence counts C[i, j] = times word j follows word i.
    Held-out bigrams are returned separately for honest evaluation.
    """
    counts = collections.Counter(tokens)
    vocab = [w for w, _ in counts.most_common(vocab_size)]
    idx = {w: i for i, w in enumerate(vocab)}

    pairs = [(idx[a], idx[b]) for a, b in zip(tokens, tokens[1:])
             if a in idx and b in idx]
    split = int(len(pairs) * 0.9)
    train, test = pairs[:split], pairs[split:]

    C = np.zeros((len(vocab), len(vocab)), dtype=np.float32)
    for i, j in train:
        C[i, j] += 1.0
    return C, vocab, test


def plane_assignment(vocab: List[str]) -> np.ndarray:
    """
    A |V| x 7 indicator: which plane each word's characters put it on.
    This is the only plane assignment available, and it is known weak.
    """
    A = np.zeros((len(vocab), 7), dtype=np.float32)
    for i, w in enumerate(vocab):
        for ch in w:
            ct = CHAR_TENSOR.get(ch)
            if ct is None:
                continue
            p, _ = ANCHOR_PLANE[ch]
            A[i, int(p) - 1] += 1.0 + abs(POLARITY_PUSH[ct.polarity])
        s = A[i].sum()
        if s > 0:
            A[i] /= s
        else:
            A[i] = 1.0 / 7.0
    return A


def orthonormalise(M: np.ndarray) -> np.ndarray:
    Q, _ = np.linalg.qr(M)
    return Q


def perplexity(P: np.ndarray, test: List[Tuple[int, int]],
               floor: float = 1e-9) -> float:
    """Perplexity of the held-out bigrams under a row-normalised P."""
    if not test:
        return float("inf")
    logp = 0.0
    for i, j in test:
        logp += math.log(max(float(P[i, j]), floor))
    return math.exp(-logp / len(test))


def row_normalise(M: np.ndarray, alpha: float = 0.1) -> np.ndarray:
    M = np.clip(M, 0.0, None) + alpha          # additive smoothing
    return M / M.sum(axis=1, keepdims=True)


def reconstruct(C: np.ndarray, B: np.ndarray) -> np.ndarray:
    """
    Project rows of C onto the column space of B (|V| x k), then back.
    This is the 'squeeze through k dimensions' operation.
    """
    proj = C @ B                # |V| x k
    return proj @ B.T           # |V| x |V|


def main() -> None:
    print("reading corpus...")
    tokens = read_corpus()
    print(f"  {len(tokens):,} tokens")

    C, vocab, test = build_matrix(tokens)
    V = len(vocab)
    print(f"  vocab {V}, held-out bigrams {len(test):,}\n")

    results: Dict[str, float] = {}

    # --- FULL: the unbottlenecked bigram model ---
    results["FULL bigram (no bottleneck)"] = perplexity(row_normalise(C), test)

    # --- UNIGRAM: predict from frequency alone, ignoring context ---
    uni = np.tile(C.sum(axis=0), (V, 1))
    results["UNIGRAM (context ignored)"] = perplexity(row_normalise(uni), test)

    rng = np.random.default_rng(0)

    for k in (7, 49, 343):
        # SVD-k: the ceiling for a k-dimensional linear compression
        U, S, Vt = np.linalg.svd(C, full_matrices=False)
        Ck = (U[:, :k] * S[:k]) @ Vt[:k]
        results[f"SVD-{k} (optimal ceiling)"] = perplexity(
            row_normalise(Ck), test)

        # RANDOM-k: the floor
        R = orthonormalise(rng.normal(size=(V, k)).astype(np.float32))
        results[f"RANDOM-{k} (floor)"] = perplexity(
            row_normalise(reconstruct(C, R)), test)

        if k == 7:
            # PLANE-7: the frozen named basis, assignment from char tensor
            A = orthonormalise(plane_assignment(vocab))
            results["PLANE-7 (char-tensor assignment)"] = perplexity(
                row_normalise(reconstruct(C, A)), test)

    print("PERPLEXITY on held-out bigrams (LOWER is better)")
    print("=" * 62)
    for name, pp in sorted(results.items(), key=lambda kv: kv[1]):
        print(f"  {name:<38}{pp:12.1f}")

    print()
    full = results["FULL bigram (no bottleneck)"]
    unig = results["UNIGRAM (context ignored)"]
    svd7 = results["SVD-7 (optimal ceiling)"]
    rnd7 = results["RANDOM-7 (floor)"]
    pl7 = results["PLANE-7 (char-tensor assignment)"]

    print("READING THE RESULT")
    print("=" * 62)
    span = unig - full
    print(f"  context is worth {span:,.0f} perplexity "
          f"(unigram {unig:,.0f} -> full bigram {full:,.0f})")
    if span > 0:
        keep7 = (unig - svd7) / span
        print(f"  7 dimensions retain {keep7:6.1%} of what context buys")
        for k in (49, 343):
            key = f"SVD-{k} (optimal ceiling)"
            print(f"  {k} dimensions retain "
                  f"{(unig - results[key]) / span:6.1%}")
    print()
    if rnd7 - svd7 != 0:
        pos = (rnd7 - pl7) / (rnd7 - svd7)
        print(f"  PLANE-7 sits at {pos:.1%} of the way from RANDOM to OPTIMAL")
        print("  (0% = the plane assignment is no better than noise,")
        print("   100% = it is as good as the best possible 7 dimensions)")


if __name__ == "__main__":
    main()
