"""
QqciFormer -- the trainable core. Scope doc Sections 14, 17, 20.

WHAT THIS IS
------------
The "build the trainable core" item from Section 20, implemented:

    frozen Kronecker basis in the Q and K projections (Section 17),
    applied FACTORED, one head per plane, with the MLP block replaced by
    the Qqci block (Section 14), trained with a three-term loss.

Every architectural choice below is from the scope doc, not invented here.

SECTION 14 -- THE QQCI BLOCK, stage by stage
--------------------------------------------
    MLP stage        | pathology                  | replacement
    up-projection    | anonymous 4x width,        | CARVE: named slots, one per
                     | superposition              | (plane x modal position)
    GELU             | context-blind absolute     | contextual min-max gate
                     | gate                       | (14.2), self-sharpening
    down-projection  | opaque fact-writing        | LEGIBLE MIX: explicit
                     |                            | CoherenceVector weights
    residual         | gradient plumbing          | up-channel (never-fills
                     |                            | write diagnostics upward)

SECTION 17 -- THE BASIS
-----------------------
One 7x7 orthonormal generator (49 floats) generates every depth by Kronecker
power. Applied factored: d small multiplies via (A (x) B) vec(X) = vec(B X A^T),
never materialising 7^d x 7^d. The cell index IS the interrogative path.

THE ABLATION THAT MAKES IT SCIENCE
----------------------------------
--basis kron    the named Kronecker basis
--basis random  a random orthonormal frozen basis, same shape
--basis learned ordinary learnable Q/K (the vanilla control)

Lila-E8's decisive number was an ablation (removing geometric bias cost 0.0221
val loss, p<0.001). This exposes the same comparison. If kron == random, the
geometry is free but anonymous-equivalent; if kron == learned, freezing costs
nothing; the interesting result is either a win or a measured price.

NOTE ON R_net AS A LOSS (scope 17.4, unresolved)
-------------------------------------------------
R_net = 1/prod(scores) makes EVERY NOUN read INSULT, because any deficit
inflates the product's reciprocal. So R_net is NOT used as a training
objective here. What is used is its log-barrier form as an ANTI-COLLAPSE term
on plane occupancy -- keeping planes alive, not scoring words as virtuous.
That distinction is deliberate; see plane_barrier().
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import os
import re
import time
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from fractal_basis import cell_basis, generator

P = 7                      # planes
DEPTH = 3                  # Q.q.c
D_MODEL = P ** DEPTH       # 343
CORPUS_DIR = r"E:\Vector Field Theory\VFT Docs\_VFT MD"
WORD_RE = re.compile(r"[a-z']+")
EXCLUDE = ("nsm_reduction", "translating", "dictionary", "isomorphic")


# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------

def read_corpus(limit_files: int = 1400) -> List[str]:
    toks: List[str] = []
    seen = 0
    for root, _d, files in os.walk(CORPUS_DIR):
        if any(t in root.lower().replace("\\", "/") for t in EXCLUDE):
            continue
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


# ---------------------------------------------------------------------------
# SECTION 17: the frozen basis, applied factored
# ---------------------------------------------------------------------------

def kron_basis() -> torch.Tensor:
    """343x343 from 49 floats. Orthonormal at every depth by construction."""
    return torch.tensor(cell_basis(DEPTH), dtype=torch.float32)


def random_orthonormal(d: int, seed: int = 0) -> torch.Tensor:
    g = torch.Generator().manual_seed(seed)
    M = torch.randn(d, d, generator=g)
    Q, _ = torch.linalg.qr(M)
    return Q


def apply_factored(x: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    """
    Apply the depth-3 Kronecker basis WITHOUT materialising 343x343.

    (A (x) B) vec(X) = vec(B X A^T) generalised to d factors: reshape to a
    d-way tensor of mode size 7 and contract each mode with the 7x7 generator.
    Cost O(d * 7 * 7^d) instead of O(7^(2d)). Scope 17.1.
    """
    shape = x.shape[:-1]
    t = x.reshape(*shape, *([P] * DEPTH))
    for mode in range(DEPTH):
        axis = len(shape) + mode
        t = t.movedim(axis, -1) @ B.T
        t = t.movedim(-1, axis)
    return t.reshape(*shape, P ** DEPTH)


# ---------------------------------------------------------------------------
# SECTION 14.2: the contextual min-max gate (replaces GELU)
# ---------------------------------------------------------------------------

class ContextualGate(nn.Module):
    """
    Gates on RELATIVE POSITION IN THE POOL'S OWN RANGE, not absolute magnitude.

    GELU has the same shape everywhere. This one:
      - is smooth while the pool is disordered (wide range, gradients flow)
      - sharpens toward a hard staircase as the pool orders
      - makes fill a convergence statistic, not a magic constant

    Differentiable without surrogates: min/max via temperature-controlled
    logsumexp (scope 14.2 says exactly this), position-in-range is a smooth
    ratio.
    """

    def __init__(self, tau: float = 0.1):
        super().__init__()
        self.tau = tau
        # sharpness is learned: the model discovers how ordered its pools are
        self.sharp = nn.Parameter(torch.tensor(0.0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        smax = self.tau * torch.logsumexp(x / self.tau, dim=-1, keepdim=True)
        smin = -self.tau * torch.logsumexp(-x / self.tau, dim=-1, keepdim=True)
        pos = (x - smin) / (smax - smin + 1e-6)          # soft: position in range
        hard = torch.sigmoid((pos - 0.5) * 12.0)         # hard: staircase limit
        s = torch.sigmoid(self.sharp)
        return x * ((1 - s) * pos + s * hard)


# ---------------------------------------------------------------------------
# ATTENTION: frozen Q/K, one head per plane
# ---------------------------------------------------------------------------

class QqciAttention(nn.Module):
    def __init__(self, basis: str = "kron", n_head: int = P):
        super().__init__()
        self.n_head = n_head
        self.head_dim = D_MODEL // n_head
        self.basis_kind = basis

        if basis == "kron":
            self.register_buffer("gen", torch.tensor(generator(),
                                                     dtype=torch.float32))
            self.W_qk = None
        elif basis == "random":
            self.register_buffer("W_qk", random_orthonormal(D_MODEL))
            self.gen = None
        else:                                    # learned control
            self.W_q = nn.Linear(D_MODEL, D_MODEL, bias=False)
            self.W_k = nn.Linear(D_MODEL, D_MODEL, bias=False)

        self.W_v = nn.Linear(D_MODEL, D_MODEL, bias=False)
        self.W_o = nn.Linear(D_MODEL, D_MODEL, bias=False)

    def project(self, x: torch.Tensor) -> torch.Tensor:
        if self.basis_kind == "kron":
            return apply_factored(x, self.gen)   # factored, never materialised
        return x @ self.W_qk

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        B, T, C = x.shape
        if self.basis_kind == "learned":
            q, k = self.W_q(x), self.W_k(x)
        else:
            q = k = self.project(x)
        v = self.W_v(x)

        q = q.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        k = k.view(B, T, self.n_head, self.head_dim).transpose(1, 2)
        v = v.view(B, T, self.n_head, self.head_dim).transpose(1, 2)

        att = (q @ k.transpose(-2, -1)) / math.sqrt(self.head_dim)
        mask = torch.triu(torch.ones(T, T, device=x.device), 1).bool()
        att = att.masked_fill(mask, float("-inf"))
        att = F.softmax(att, dim=-1)

        y = (att @ v).transpose(1, 2).contiguous().view(B, T, C)
        return self.W_o(y), att


# ---------------------------------------------------------------------------
# SECTION 14.1: the Qqci block (replaces the MLP block)
# ---------------------------------------------------------------------------

class QqciBlock(nn.Module):
    """
    up-projection -> CARVE onto named slots (7 planes x 5 modal positions)
    GELU          -> contextual min-max gate
    down-proj     -> LEGIBLE MIX, explicit per-plane weights
    """

    N_MODAL = 5      # can-be / are / not-really / was-like / not+all

    def __init__(self, basis: str = "kron"):
        super().__init__()
        self.attn = QqciAttention(basis)
        self.ln1 = nn.LayerNorm(D_MODEL)
        self.ln2 = nn.LayerNorm(D_MODEL)

        self.n_slots = P * self.N_MODAL            # 35 named slots
        self.carve = nn.Linear(D_MODEL, self.n_slots * 8)
        self.gate = ContextualGate()
        self.mix = nn.Linear(self.n_slots * 8, D_MODEL)

    def forward(self, x: torch.Tensor):
        a, att = self.attn(self.ln1(x))
        x = x + a
        h = self.carve(self.ln2(x))
        h = self.gate(h)
        x = x + self.mix(h)
        return x, att


class QqciFormer(nn.Module):
    def __init__(self, vocab: int, n_layer: int = 4, basis: str = "kron",
                 block: int = 128):
        super().__init__()
        self.block_size = block
        self.tok = nn.Embedding(vocab, D_MODEL)
        self.pos = nn.Embedding(block, D_MODEL)
        self.blocks = nn.ModuleList([QqciBlock(basis) for _ in range(n_layer)])
        self.lnf = nn.LayerNorm(D_MODEL)
        self.head = nn.Linear(D_MODEL, vocab, bias=False)
        self.apply(self._init)

    @staticmethod
    def _init(m):
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, std=0.02)

    def forward(self, idx: torch.Tensor):
        B, T = idx.shape
        p = torch.arange(T, device=idx.device)
        x = self.tok(idx) + self.pos(p)
        atts = []
        for blk in self.blocks:
            x, att = blk(x)
            atts.append(att)
        x = self.lnf(x)
        return self.head(x), x, atts


# ---------------------------------------------------------------------------
# THE THREE-TERM LOSS (scope Section 20)
# ---------------------------------------------------------------------------

def resonance_loss(h: torch.Tensor, B: torch.Tensor) -> torch.Tensor:
    """
    Leech-LILA's term, verbatim: split the hidden state into blocks, take the
    max |cos| to any basis vector, L = 1 - mean. Softly pulls states toward
    cells. Scope 16.2 notes this IS the differentiable form of the fill gate.
    """
    x = h.reshape(-1, P, P ** (DEPTH - 1))
    x = F.normalize(x, dim=-1)
    Bn = F.normalize(B[: P ** (DEPTH - 1), : P ** (DEPTH - 1)], dim=-1)
    sim = (x @ Bn.T).abs().amax(dim=-1)
    return 1.0 - sim.mean()


def plane_barrier(h: torch.Tensor, eps: float = 1e-4) -> torch.Tensor:
    """
    ANTI-COLLAPSE, the log form of R_net = 1/prod(s).

    -sum_p log(s_p) diverges as any plane's mass goes to zero, so gradient
    descent cannot let an interrogative go dead. This is R_net used as a
    BARRIER on plane aliveness, NOT as a virtue score on words -- scope 17.4
    records that scoring nouns with R_net makes every noun read INSULT, so
    that use is deliberately avoided.
    """
    mass = h.reshape(-1, P, P ** (DEPTH - 1)).pow(2).mean(-1)   # per plane
    mass = mass / (mass.sum(-1, keepdim=True) + eps)
    return -(torch.log(mass + eps)).mean()


def anchor_loss(emb: torch.Tensor, anchor_idx: torch.Tensor,
                anchor_cell: torch.Tensor) -> torch.Tensor:
    """
    THE PRICE OF A NAMED BASIS (scope Section 20).

    Pins seed words to their cells so gradient descent cannot use the 343
    axes arbitrarily and leave the names as decoration. Lila models need no
    such term because anonymity costs them nothing.

    Equivalence, not value: words sharing a cell are pulled together and
    pushed from other cells. No score is ever supplied, so nothing can be
    read back.
    """
    if anchor_idx.numel() == 0:
        return torch.zeros((), device=emb.device)
    v = F.normalize(emb[anchor_idx], dim=-1)
    same = (anchor_cell[:, None] == anchor_cell[None, :]).float()
    same.fill_diagonal_(0)
    sim = v @ v.T
    pos = (sim * same).sum() / same.sum().clamp(min=1)
    neg = (sim * (1 - same)).sum() / (1 - same).sum().clamp(min=1)
    return (neg - pos + 1.0).clamp(min=0)


# ---------------------------------------------------------------------------
# TRAIN
# ---------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--basis", default="kron",
                    choices=["kron", "random", "learned"])
    ap.add_argument("--steps", type=int, default=1500)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--block", type=int, default=128)
    ap.add_argument("--layers", type=int, default=4)
    ap.add_argument("--vocab", type=int, default=6000)
    ap.add_argument("--lam_res", type=float, default=0.01)
    ap.add_argument("--lam_bar", type=float, default=0.02)
    ap.add_argument("--lam_anc", type=float, default=0.05)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    dev = "cuda" if torch.cuda.is_available() else "cpu"
    torch.manual_seed(0)

    print(f"basis={args.basis}  device={dev}")
    toks = read_corpus()
    counts = collections.Counter(toks)
    itos = ["<unk>"] + [w for w, _ in counts.most_common(args.vocab - 1)]
    stoi = {w: i for i, w in enumerate(itos)}
    data = torch.tensor([stoi.get(t, 0) for t in toks], dtype=torch.long)
    n = int(len(data) * 0.9)
    train, val = data[:n], data[n:]
    print(f"tokens {len(data):,}  vocab {len(itos)}  "
          f"train {len(train):,}  val {len(val):,}")

    # anchors from the derived Q.q.c assignment (co-occurrence, not spelling)
    anchor_idx: List[int] = []
    anchor_cell: List[int] = []
    apath = os.path.join(os.path.dirname(__file__), "derived_addresses.json")
    if os.path.exists(apath):
        with open(apath, "r", encoding="utf-8") as fh:
            for w, a in json.load(fh).items():
                if w in stoi:
                    anchor_idx.append(stoi[w])
                    anchor_cell.append(a[0] * 49 + a[1] * 7 + a[2])
    ai = torch.tensor(anchor_idx, dtype=torch.long, device=dev)
    ac = torch.tensor(anchor_cell, dtype=torch.long, device=dev)
    print(f"anchors: {len(anchor_idx)} words pinned to derived cells")

    model = QqciFormer(len(itos), args.layers, args.basis, args.block).to(dev)
    nparam = sum(p.numel() for p in model.parameters())
    nfrozen = sum(p.numel() for p in model.buffers())
    print(f"params {nparam/1e6:.2f}M trainable, {nfrozen} frozen basis floats")

    Bmat = kron_basis().to(dev)
    opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)

    def batch(split: torch.Tensor):
        ix = torch.randint(len(split) - args.block - 1, (args.batch,))
        x = torch.stack([split[i:i + args.block] for i in ix]).to(dev)
        y = torch.stack([split[i + 1:i + 1 + args.block] for i in ix]).to(dev)
        return x, y

    @torch.no_grad()
    def evaluate(iters: int = 40) -> float:
        model.eval()
        tot = 0.0
        for _ in range(iters):
            x, y = batch(val)
            logits, _, _ = model(x)
            tot += F.cross_entropy(logits.view(-1, logits.size(-1)),
                                   y.reshape(-1)).item()
        model.train()
        return tot / iters

    t0 = time.time()
    for step in range(1, args.steps + 1):
        x, y = batch(train)
        logits, h, _ = model(x)
        l_ce = F.cross_entropy(logits.view(-1, logits.size(-1)), y.reshape(-1))
        l_res = resonance_loss(h, Bmat)
        l_bar = plane_barrier(h)
        l_anc = anchor_loss(model.tok.weight, ai, ac)
        loss = (l_ce + args.lam_res * l_res
                + args.lam_bar * l_bar + args.lam_anc * l_anc)

        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()

        if step % 250 == 0 or step == 1:
            v = evaluate()
            print(f"  step {step:5d}  train {l_ce.item():6.3f}  val {v:6.3f}"
                  f"  ppl {math.exp(min(v,20)):8.1f}  res {l_res.item():.3f}"
                  f"  bar {l_bar.item():.3f}  anc {l_anc.item():.3f}"
                  f"  [{time.time()-t0:.0f}s]")

    final = evaluate(100)
    print(f"\nFINAL basis={args.basis}  val loss {final:.4f}  "
          f"ppl {math.exp(min(final,20)):.1f}")
    if args.out:
        with open(args.out, "a", encoding="utf-8") as fh:
            fh.write(f"{args.basis}\t{final:.4f}\t{math.exp(min(final,20)):.1f}\n")


if __name__ == "__main__":
    main()
