"""
The fractal Qqci basis: a hierarchical, ultra-overcomplete geometric core.

This is the trainable counterpart to Leech-LILA's frozen Leech projection,
with three differences:

  Leech / E8                        Qqci
  ----------                        ----
  basis stored (24x24 QR, or        basis GENERATED from one 7x7 (49 floats)
  240 explicit roots)               at unbounded depth via Kronecker power
  flat: root 137 relates to         hierarchical: Q4.q5.c2 has a parent,
  root 138 not at all               siblings, and inheritance
  anonymous directions              named directions (MoralVectorDef)

CONSTRUCTION
------------
1. A 7x7 orthonormal generator B from the 42-Structure axis signature.
2. Depth-d cell basis = B (x) B (x) ... (x) B, d times. Orthonormal at every
   depth, because (A(x)B)^T(A(x)B) = (A^T A)(x)(B^T B) = I (x) I = I.
3. OVERCOMPLETENESS by isomorphic fractions: between any two cells lies
   another frame of the same kind. Adding the normalised sums and differences
   of cell pairs gives the "gap" directions; recursing gives finer ones.

WHY OVERCOMPLETE
----------------
E8 packs 240 roots into 8 dimensions (30 directions per dimension). That
overcompleteness is where "dense semantic packing" comes from. A plain
orthonormal basis has exactly 1 direction per dimension and cannot compete.
The fractions restore density WITHOUT losing names: a gap direction between
Q4 and Q5 is still readable as "between Why and How", which no E8 root is.

THE 42
------
At depth 2 there are 49 cells: 7 diagonal (Qi.qi, a plane read through
itself) and 42 off-diagonal (Qi.qj, plane i read through plane j). The
42-Structure is exactly the off-diagonal shell. This is arithmetic, not
numerology: 7 x 6 = 42.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

PLANE_NAMES = ["Who", "What", "Where", "Why", "How", "Cause", "Effect"]

# The 42-Structure axis signature: Q1 is the unpaired Driver; the six paired
# planes carry their axis signs (+x/-x, +y/-y, +z/-z).
AXIS_SIGNATURE = np.diag([1.0, +1.0, -1.0, +1.0, -1.0, +1.0, -1.0])


def generator(signature: np.ndarray = AXIS_SIGNATURE) -> np.ndarray:
    """The single 7x7 orthonormal generator. 49 floats; everything else is
    derived from it."""
    Q, _ = np.linalg.qr(signature)
    return Q


def cell_basis(depth: int, B: Optional[np.ndarray] = None) -> np.ndarray:
    """Depth-d orthonormal cell basis, 7^d x 7^d, via Kronecker power."""
    B = generator() if B is None else B
    M = B
    for _ in range(depth - 1):
        M = np.kron(M, B)
    return M


def apply_factored(B: np.ndarray, x: np.ndarray, depth: int) -> np.ndarray:
    """
    Apply the depth-d basis WITHOUT materialising the 7^d x 7^d matrix.

    Uses the Kronecker identity (A (x) B) vec(X) = vec(B X A^T) generalised
    to d factors: reshape to a d-way tensor of mode size 7 and contract each
    mode with B. Cost is O(d * 7 * 7^d) instead of O(7^(2d)).
    """
    n = 7 ** depth
    assert x.shape[-1] == n
    shape = x.shape[:-1]
    t = x.reshape(*shape, *([7] * depth))
    for mode in range(depth):
        axis = len(shape) + mode
        t = np.moveaxis(t, axis, -1)
        t = t @ B.T
        t = np.moveaxis(t, -1, axis)
    return t.reshape(*shape, n)


def cell_address(index: int, depth: int) -> str:
    """Cell index to its Qqci address. The index IS the interrogative path."""
    digits = []
    i = index
    for _ in range(depth):
        digits.append(i % 7)
        i //= 7
    digits.reverse()
    head = f"Q{digits[0] + 1}"
    tail = "".join(f".q{d + 1}" for d in digits[1:])
    return head + tail


def cell_name(index: int, depth: int) -> str:
    digits = []
    i = index
    for _ in range(depth):
        digits.append(i % 7)
        i //= 7
    digits.reverse()
    return " of ".join(PLANE_NAMES[d] for d in reversed(digits))


# ---------------------------------------------------------------------------
# ISOMORPHIC FRACTIONS: the gaps are frames too
# ---------------------------------------------------------------------------

@dataclass
class Direction:
    vector: np.ndarray
    address: str
    kind: str          # "cell" | "gap" | "subgap"
    parents: Tuple[int, ...] = ()


def shared_subobjects(i: int, j: int, depth: int) -> Tuple[int, Tuple[int, ...]]:
    """
    ISOMORPHIC FRACTIONS, correctly understood.

    Not interpolation between cells. SHARING: part of one composite IS part of
    another, the same specific sub-object, the way 6/8 and 9/12 share the
    reduced form 3/4.

    Q4.q5 and Q6.q5 do not merely resemble each other at position 2 -- they
    contain the SAME e5 factor. The Kronecker construction already implements
    this: every cell is built from the same seven generator columns, which is
    why 49 floats generate unbounded depth.

    Returns (count_shared, mask) over address positions.
    """
    a, b = _digits(i, depth), _digits(j, depth)
    mask = tuple(1 if x == y else 0 for x, y in zip(a, b))
    return sum(mask), mask


def _digits(i: int, depth: int) -> Tuple[int, ...]:
    out = []
    for _ in range(depth):
        out.append(i % 7)
        i //= 7
    return tuple(reversed(out))


def sharing_graph(depth: int, min_shared: int = 1
                  ) -> Dict[int, List[Tuple[int, int]]]:
    """
    The associative structure, for free and structural rather than learned.

    Lila-E8's GraphResonator has to LEARN token-to-token relations by
    co-occurrence during generation, because its 240 roots have no intrinsic
    relationship to one another. Here the relations are given by construction:
    two cells are linked exactly when they share sub-objects, and the link
    strength is how many.
    """
    n = 7 ** depth
    graph: Dict[int, List[Tuple[int, int]]] = {}
    for i in range(n):
        links = []
        for j in range(n):
            if i == j:
                continue
            k, _ = shared_subobjects(i, j, depth)
            if k >= min_shared:
                links.append((j, k))
        graph[i] = links
    return graph


def sharing_stats(depth: int) -> Dict[str, float]:
    """
    Overcompleteness lives in REUSE, not in atom count.

    E8:   240 atoms, each used once.
    Qqci: 7*depth atoms, each participating in 7^(depth-1) composites.

    So the packing density is a property of how often an atom is reused, and
    that is also exactly the parameter-sharing (weight tying) argument for
    running on small hardware.
    """
    cells = 7 ** depth
    atoms = 7 * depth
    return {
        "cells": cells,
        "independent_atoms": atoms,
        "compression": cells / atoms,
        "reuse_per_atom": 7 ** (depth - 1),
    }


def fractions_between(a: np.ndarray, b: np.ndarray, k: int = 5
                      ) -> List[np.ndarray]:
    """
    DEPRECATED. Kept only so the failed experiment stays on the record.

    This was a wrong reading of "isomorphic fractions" as interpolation
    between cells. Measured result: density 145 directions/dim (beating E8's
    30) but mutual coherence 0.9806 against E8's 0.5, meaning the atoms are
    near-duplicates and the dictionary cannot uniquely represent anything.
    Density bought this way is worthless.

    Restricting to pair sum/difference only gives coherence 0.7071 at 7
    directions/dim, which is the +-e_i +-e_j family that makes up 112 of E8's
    240 roots. Adding triples reaches 27/dim but degrades to 0.8165.

    None of these beat E8, and none of them were what was meant. See
    shared_subobjects() for the correct construction.
    """
    out = []
    for i in range(1, k + 1):
        t = i / (k + 1)
        v = (1 - t) * a + t * b
        n = np.linalg.norm(v)
        if n > 1e-12:
            out.append(v / n)
    return out


def overcomplete_dictionary(depth: int = 2, gap_k: int = 5,
                            include_signed: bool = True,
                            B: Optional[np.ndarray] = None
                            ) -> Tuple[np.ndarray, List[Direction]]:
    """
    Build the ultra-overcomplete dictionary at a given depth.

    Shell 0: the 7^d orthonormal cells.
    Shell 1: isomorphic fractions between every ordered pair of cells,
             gap_k of them per pair (the modal tile's five positions).
    Signed:  also the difference directions (a - b), which are the
             "opposition" readings: the same axis pair read as conflict
             rather than blend.
    """
    B = generator() if B is None else B
    M = cell_basis(depth, B)
    n = M.shape[0]

    dirs: List[Direction] = []
    for i in range(n):
        dirs.append(Direction(M[:, i], cell_address(i, depth), "cell", (i,)))

    for i, j in itertools.combinations(range(n), 2):
        a, b = M[:, i], M[:, j]
        for f_idx, v in enumerate(fractions_between(a, b, gap_k)):
            dirs.append(Direction(
                v, f"{cell_address(i, depth)}~{cell_address(j, depth)}#{f_idx}",
                "gap", (i, j)))
        if include_signed:
            d = a - b
            d = d / np.linalg.norm(d)
            dirs.append(Direction(
                d, f"{cell_address(i, depth)}!{cell_address(j, depth)}",
                "gap", (i, j)))

    D = np.stack([d.vector for d in dirs], axis=1)
    return D, dirs


# ---------------------------------------------------------------------------
# QUALITY MEASURES
# ---------------------------------------------------------------------------

def mutual_coherence(D: np.ndarray, sample: Optional[int] = 4000,
                     seed: int = 0) -> float:
    """
    Max |cos| between distinct dictionary directions. LOWER is better: a
    dictionary with high coherence has near-duplicate atoms and cannot
    uniquely represent a signal. E8's roots have max |cos| = 0.5 between
    distinct non-opposite roots.
    """
    n = D.shape[1]
    rng = np.random.default_rng(seed)
    idx = np.arange(n) if (sample is None or n <= sample) else rng.choice(
        n, sample, replace=False)
    S = D[:, idx]
    G = np.abs(S.T @ S)
    np.fill_diagonal(G, 0.0)
    # opposite directions (cos = -1) are the same atom signed; ignore them
    G[G > 1 - 1e-9] = 0.0
    return float(G.max())


def density(D: np.ndarray) -> float:
    """Directions per dimension. E8 = 240/8 = 30."""
    return D.shape[1] / D.shape[0]


def report(depth: int = 2, gap_k: int = 5) -> None:
    B = generator()
    print(f"generator orthonormal: "
          f"{np.allclose(B.T @ B, np.eye(7))}   (49 floats)")
    print()
    print("depth  cells    dim    orthonormal")
    for d in range(1, 5):
        M = cell_basis(d, B)
        print(f"  {d}   {7**d:7d} {M.shape[0]:6d}       "
              f"{np.allclose(M.T @ M, np.eye(M.shape[0]), atol=1e-8)}")
    print()

    D, dirs = overcomplete_dictionary(depth, gap_k, B=B)
    kinds: Dict[str, int] = {}
    for d in dirs:
        kinds[d.kind] = kinds.get(d.kind, 0) + 1
    print(f"OVERCOMPLETE DICTIONARY at depth {depth}, gap_k={gap_k}")
    print(f"  dimension        : {D.shape[0]}")
    print(f"  directions       : {D.shape[1]}  ({kinds})")
    print(f"  density          : {density(D):.1f} directions/dim")
    print(f"  mutual coherence : {mutual_coherence(D):.4f}  (lower is better)")
    print()
    print("  comparison:")
    print("    E8    : 240 dirs /  8 dim =  30.0/dim, coherence 0.5")
    print("    Leech : 196560   / 24 dim = 8190.0/dim")
    print()
    print("  named readout of the first cells and gaps:")
    for d in dirs[:3]:
        print(f"    {d.kind:<4} {d.address:<22} {cell_name(d.parents[0], depth)}")
    for d in dirs:
        if d.kind == "gap":
            print(f"    {d.kind:<4} {d.address:<22} between "
                  f"{cell_name(d.parents[0], depth)} and "
                  f"{cell_name(d.parents[1], depth)}")
            break
    print()
    print("  the 42: depth-2 cells split into diagonal and off-diagonal")
    diag = [i for i in range(49) if (i // 7) == (i % 7)]
    print(f"    diagonal  Qi.qi : {len(diag)}")
    print(f"    off-diag  Qi.qj : {49 - len(diag)}   <- the 42-Structure")


if __name__ == "__main__":
    report()
