"""
THE TRANSFORMER ANALOGUE: attention gated by SLOT COMPLEMENTARITY.

This is the answer to "how does any of this turn into an AI model".

THE ONE ARCHITECTURAL IDEA
--------------------------
Standard attention routes by SIMILARITY:      A = softmax(QK^T / sqrt(d))
A token attends to tokens that RESEMBLE it.

This routes additionally by COMPLEMENTARITY:  A_p = softmax(QK^T/sqrt(d) + b*C_p)
where  C_p[i,j] = 1  iff  token i is OPEN on plane p and token j FILLS plane p.

A token attends to tokens that COMPLETE it. That is the DNA base-pairing the
user described, and it is a different relation from similarity: `big` is not
similar to `house`, it BINDS to `house`. Cosine similarity cannot express that;
an open index seeking a bound one can.

WHOSE SOLUTION IS COPIED
------------------------
- Lila-E8 (RESEARCH_NOTES 1) adds a learnable GEOMETRIC BIAS to attention
  scores and ablates it to prove it contributes (p<0.001). The additive-bias
  mechanism is copied exactly; the bias content is complementarity instead of
  E8 root alignment.
- Leech-LILA (RESEARCH_NOTES 2) replaces the learnable Q/K projections with a
  FROZEN orthonormal basis and keeps V learnable. Copied verbatim, with the
  frozen basis being our Kronecker 7^d basis (fractal_basis.cell_basis).
- DisCoCat: composition is contraction of open indices. The per-plane head
  structure IS the index structure: head p contracts index p.
- Class-based LMs (Brown et al. 1992): factor P(word|ctx) into
  P(class|ctx) * P(word|class,ctx). Copied as plane-factored prediction, which
  is what the 7 heads make available for free.

WHY ONE HEAD PER PLANE
----------------------
"Multi-head attention as an atlas of charts" (Curved Spacetime, RESEARCH_NOTES
3): each head is a local chart on the manifold, W_O is the transition map.
Seven NAMED charts = seven interrogatives = the parallax construction with
established vocabulary. Head p answers exactly one question, so the attention
map is readable: you can say WHY token i attended to token j (it needed its
Q5 filled and j supplied it).

HONEST STATUS
-------------
The mechanism runs and is tested (test_complementarity_routing). Whether the
complementarity bias helps on real language is measured in run_experiments.py,
H3, and reported whether it passes or not.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from fractal_basis import cell_basis, generator
from qqci_engine import Plane
from slots import Frame

N_PLANES = 7


def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - np.max(x, axis=axis, keepdims=True)
    e = np.exp(x)
    return e / np.sum(e, axis=axis, keepdims=True)


def occupancy_matrix(frames: Sequence[Frame]) -> np.ndarray:
    """
    O[i, p] = 1 if token i is OPEN on plane p, else 0.
    This is the sparse binary occupancy of LANGUAGE_SPEC 4.1, as a matrix.
    """
    O = np.zeros((len(frames), N_PLANES), dtype=np.float32)
    for i, f in enumerate(frames):
        for j, p in enumerate(Plane):
            O[i, j] = 1.0 if f.slots[p].is_open else 0.0
    return O


def complementarity_bias(O: np.ndarray) -> np.ndarray:
    """
    C[p, i, j] = 1 iff i is OPEN on p and j is FILLED on p.

    This is the whole contribution: an n x n routing map PER PLANE saying
    "who can complete me here". Note it is ASYMMETRIC, which is correct --
    binding has a direction (the operator seeks the host, not vice versa).
    """
    n, k = O.shape
    C = np.zeros((k, n, n), dtype=np.float32)
    for p in range(k):
        open_i = O[:, p][:, None]         # (n,1) 1 if i open
        filled_j = (1.0 - O[:, p])[None, :]  # (1,n) 1 if j filled
        C[p] = open_i * filled_j
        np.fill_diagonal(C[p], 0.0)       # a token cannot fill its own blank
    return C


@dataclass
class PlaneAttention:
    """
    One block: 7 heads, one per interrogative, frozen Q/K, learnable V,
    complementarity-biased routing.

    d_model must be divisible by 7 so each plane-head owns a slice.
    """
    d_model: int = 49
    bias_strength: float = 4.0     # lambda on the complementarity term
    seed: int = 0

    def __post_init__(self) -> None:
        assert self.d_model % N_PLANES == 0, "d_model must be a multiple of 7"
        self.head_dim = self.d_model // N_PLANES
        depth = 1
        while 7 ** depth < self.d_model:
            depth += 1
        # FROZEN basis (Leech-LILA's move). Kronecker power of one 7x7.
        full = cell_basis(depth) if 7 ** depth == self.d_model else None
        if full is None:
            B = generator()
            full = np.kron(B, np.eye(self.d_model // 7))
        self.W_frozen = full[: self.d_model, : self.d_model].astype(np.float32)
        rng = np.random.default_rng(self.seed)
        # V stays learnable, exactly as in Leech-LILA.
        self.W_v = (rng.normal(size=(self.d_model, self.d_model))
                    .astype(np.float32) / np.sqrt(self.d_model))

    def head_slice(self, p: int) -> slice:
        return slice(p * self.head_dim, (p + 1) * self.head_dim)

    def forward(self, X: np.ndarray, O: Optional[np.ndarray] = None,
                use_bias: bool = True
                ) -> Tuple[np.ndarray, np.ndarray]:
        """
        X : (n_tokens, d_model)
        O : (n_tokens, 7) openness matrix, or None to disable gating

        Returns (output, attention) where attention is (7, n, n) so every
        routing decision is inspectable per NAMED plane.
        """
        n = X.shape[0]
        Q = X @ self.W_frozen
        K = X @ self.W_frozen
        V = X @ self.W_v

        C = (complementarity_bias(O)
             if (O is not None and use_bias)
             else np.zeros((N_PLANES, n, n), dtype=np.float32))

        out = np.zeros_like(V)
        attn = np.zeros((N_PLANES, n, n), dtype=np.float32)
        for p in range(N_PLANES):
            sl = self.head_slice(p)
            scores = (Q[:, sl] @ K[:, sl].T) / np.sqrt(self.head_dim)
            A = softmax(scores + self.bias_strength * C[p], axis=-1)
            attn[p] = A
            out[:, sl] = A @ V[:, sl]
        return out, attn

    def explain(self, attn: np.ndarray, lemmas: Sequence[str], i: int
                ) -> List[str]:
        """
        WHY did token i attend where it did, per named plane. This is the
        legibility payoff: an anonymous transformer cannot produce this line.
        """
        lines = []
        for p, plane in enumerate(Plane):
            j = int(np.argmax(attn[p, i]))
            w = attn[p, i, j]
            lines.append(f"  {plane.name:<7} -> {lemmas[j]:<12} ({w:.2f})")
        return lines


# ---------------------------------------------------------------------------
# PLANE-FACTORED PREDICTION (class-based LM, Brown et al. 1992)
# ---------------------------------------------------------------------------

def plane_factored_predict(counts_plane: np.ndarray,
                           counts_word_given_plane: np.ndarray,
                           ctx: int, alpha: float = 0.1) -> np.ndarray:
    """
    P(next word | ctx) = sum_p P(plane p | ctx) * P(word | plane p, ctx)

    The factorisation Brown et al. use for word classes, with the classes
    being the 7 NAMED planes instead of induced anonymous ones. The win, when
    there is one, comes from the plane-level distribution having far more
    counts per parameter than the word-level one.
    """
    p_plane = counts_plane[ctx] + alpha
    p_plane = p_plane / p_plane.sum()
    joint = counts_word_given_plane + alpha
    joint = joint / joint.sum(axis=1, keepdims=True)
    return p_plane @ joint


# ---------------------------------------------------------------------------
# SELF-TEST: does the gate actually route blanks to fillers?
# ---------------------------------------------------------------------------

def test_complementarity_routing() -> Dict[str, float]:
    """
    Construct a case where similarity and complementarity DISAGREE, and check
    the gate follows complementarity.

    Tokens: an operator OPEN on Q5-How ('big' fills Where, so How is one of
    its free indices), a host that FILLS Q5 ('house' -> encloses), and a
    distractor that is near-identical to the operator in vector space but is
    ALSO open on Q5, so it cannot complete it.

    A similarity-only model attends operator -> distractor.
    A complementarity-gated model must attend operator -> host.
    """
    from primitives import HOSTS, OPERATORS

    big = OPERATORS["big"]
    house = HOSTS["house"]
    small = OPERATORS["small"]      # fills Where like big; open on How like big
    frames = [big, house, small]
    lemmas = [f.lemma for f in frames]
    assert big.slots[Plane.HOW].is_open, "test needs How OPEN on the operator"
    assert not house.slots[Plane.HOW].is_open, "test needs How FILLED on host"
    assert small.slots[Plane.HOW].is_open, "distractor must not fill How"

    rng = np.random.default_rng(0)
    d = 49
    X = rng.normal(size=(3, d)).astype(np.float32) * 0.1
    # make 'small' nearly identical to 'big' in raw vector space: this is the
    # adversarial part -- similarity says they belong together.
    X[2] = X[0] + rng.normal(size=d).astype(np.float32) * 0.01

    blk = PlaneAttention(d_model=d, bias_strength=6.0)
    O = occupancy_matrix(frames)

    _, attn_off = blk.forward(X, O, use_bias=False)
    _, attn_on = blk.forward(X, O, use_bias=True)

    how_idx = list(Plane).index(Plane.HOW)
    # token 0 = 'big' (How OPEN). token 1 = 'house' (How FILLED).
    # token 2 = 'small' (How OPEN, near-identical vector to 'big').
    return {
        "similarity_only_to_host": float(attn_off[how_idx, 0, 1]),
        "similarity_only_to_distractor": float(attn_off[how_idx, 0, 2]),
        "gated_to_host": float(attn_on[how_idx, 0, 1]),
        "gated_to_distractor": float(attn_on[how_idx, 0, 2]),
    }


if __name__ == "__main__":
    from primitives import HOSTS, OPERATORS

    print("COMPLEMENTARITY-GATED ATTENTION")
    print("=" * 70)
    print("Standard attention routes by similarity. This adds a bias term so a")
    print("token with an OPEN plane routes to a token that FILLS it.")
    print()

    r = test_complementarity_routing()
    print("adversarial case: 'big' (OPEN on How) vs host filling How and a")
    print("distractor near-identical in vector space but ALSO open on How:")
    print(f"  similarity only : host {r['similarity_only_to_host']:.3f}   "
          f"distractor {r['similarity_only_to_distractor']:.3f}")
    print(f"  with gate       : host {r['gated_to_host']:.3f}   "
          f"distractor {r['gated_to_distractor']:.3f}")
    ok = (r["gated_to_host"] > r["gated_to_distractor"]
          and r["gated_to_host"] > r["similarity_only_to_host"])
    print(f"  gate routes blank -> filler: {ok}")
    print()

    frames = [OPERATORS["big"], HOSTS["house"]]
    lemmas = [f.lemma for f in frames]
    rng = np.random.default_rng(1)
    X = rng.normal(size=(2, 49)).astype(np.float32) * 0.1
    blk = PlaneAttention(d_model=49, bias_strength=6.0)
    _, attn = blk.forward(X, occupancy_matrix(frames))
    print("PER-PLANE EXPLANATION for 'big' (what an anonymous model cannot say)")
    for line in blk.explain(attn, lemmas, 0):
        print(line)
