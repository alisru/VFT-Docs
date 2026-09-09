#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
eng4_realmodel.py - ENG-4.4. The Semantic Connection Hypothesis against a real
language model.

WHAT THIS IS FOR
----------------
Formal Paper 9 asserts that understanding is holonomy-free parallel transport
(F_mu_nu = 0) and that the structure group of Information Space is
SO(7) x Aut(chi). Until now those were sentences about symbols.
semantic_connection.py supplied the missing map from an embedding space to a
gauge connection, and validated the instrument against synthetic ground truth
(5 pass / 0 fail). This script points that instrument at a real learned
representation, which is the step that can produce a result or a refutation.

THE CHART ON CONTEXT SPACE
--------------------------
Paper 9's Delta^42 is 7 interrogative planes x 6 inquiry axes. Here a context
c in R^7 is the framing intensity of the 7 planes (WHO, WHAT, WHERE, WHY, HOW,
CAUSE, EFFECT).

Prompt space is discrete, so a naive template family gives no manifold to
differentiate over. Instead the framing acts CONTINUOUSLY by scaling the input
embeddings of the framing tokens before the forward pass:

    sequence = [CLS] [c_1 * e(who)] ... [c_7 * e(effect)] [probe tokens] [SEP]

c enters as a real coefficient on a token embedding and then passes through the
full non-linear transformer stack. This is a genuine smooth chart on a
submanifold of context space, and - critically - it is NOT linear in the output,
so it is capable of producing curvature rather than guaranteeing its absence.

The honest caveat from HYPOTHESIS section 6 stands: whether the connection is an
artifact of this chart is not settled by this run.

WHY THE MEASUREMENTS ARE REPORTED AGAINST CONTROLS
--------------------------------------------------
A non-zero number is meaningless on its own. Every quantity here is reported
against a control that is rigid by construction, so the reader can see the
noise floor rather than take the measurement on trust. The verdicts at the end
are COMPUTED from the measured values at runtime, not written in advance -
see CLAUDE_LOG.md Entry 004 section 4 for why that rule exists.

Run:  python eng4_realmodel.py [--model NAME] [--probes N]
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

import numpy as np

os.environ.setdefault("HF_HUB_OFFLINE", "1")   # never reach the network

import torch
from scipy.linalg import logm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from semantic_connection import (          # noqa: E402
    SemanticConnection, procrustes_transport, normalise,
)

PLANES = ["who", "what", "where", "why", "how", "cause", "effect"]

# A probe set spanning concrete objects, social roles, abstractions and
# processes, so the relational geometry has something to deform.
PROBES = [
    "bread", "water", "wheat", "flour", "oven", "farmer", "baker", "miller",
    "market", "price", "money", "debt", "interest", "wage", "labour", "cost",
    "value", "scarcity", "surplus", "exchange", "contract", "law", "justice",
    "power", "authority", "consent", "coercion", "freedom", "duty", "harm",
    "truth", "belief", "evidence", "proof", "meaning", "definition", "number",
    "measure", "time", "space", "motion", "energy", "heat", "light", "mass",
    "force", "cause", "effect", "process", "boundary", "limit", "infinity",
    "zero", "one", "whole", "part", "set", "point", "line", "curve",
    "distance", "scale", "order", "chaos",
]


# ==========================================================================
# The embedding map
# ==========================================================================
class FramedEncoder:
    """c in R^7 -> E(c) in R^{N x d}, differentiable-in-c by construction."""

    def __init__(self, model_name: str, probes: List[str], device: str):
        from transformers import AutoModel, AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(device).eval()
        self.device = device
        self.probes = probes
        self.emb_layer = self.model.get_input_embeddings()

        # Token id for each framing word (first sub-token if it splits).
        self.plane_ids = [
            self.tok(p, add_special_tokens=False)["input_ids"][0] for p in PLANES
        ]
        # Pre-tokenise probes once.
        self.probe_ids = [
            self.tok(t, add_special_tokens=False)["input_ids"] for t in probes
        ]
        self.cls = self.tok.cls_token_id
        self.sep = self.tok.sep_token_id
        self._cache: Dict[Tuple, np.ndarray] = {}
        self.calls = 0

    @torch.no_grad()
    def __call__(self, c: np.ndarray) -> np.ndarray:
        key = tuple(np.round(np.asarray(c, dtype=float), 9))
        if key in self._cache:
            return self._cache[key]

        c_t = torch.tensor(np.asarray(c, dtype=np.float32), device=self.device)
        plane_emb = self.emb_layer(
            torch.tensor(self.plane_ids, device=self.device))        # 7 x d
        framed = plane_emb * c_t.unsqueeze(1)                        # scaled

        rows, masks = [], []
        maxlen = max(len(p) for p in self.probe_ids) + 9
        for ids in self.probe_ids:
            body = self.emb_layer(torch.tensor(
                [self.cls] + ids + [self.sep], device=self.device))
            seq = torch.cat([body[:1], framed, body[1:]], dim=0)
            pad = maxlen - seq.shape[0]
            if pad > 0:
                seq = torch.cat(
                    [seq, torch.zeros(pad, seq.shape[1], device=self.device)])
            rows.append(seq)
            masks.append([1] * (maxlen - pad) + [0] * pad)

        inputs_embeds = torch.stack(rows)
        attn = torch.tensor(masks, device=self.device)
        out = self.model(inputs_embeds=inputs_embeds,
                         attention_mask=attn).last_hidden_state
        m = attn.unsqueeze(-1).float()
        pooled = (out * m).sum(1) / m.sum(1).clamp(min=1e-9)          # mean pool
        E = pooled.float().cpu().numpy()
        self.calls += 1
        self._cache[key] = E
        return E


def build_reduced_embed(enc: FramedEncoder, c0: np.ndarray, k: int,
                        delta: float = 0.35):
    """
    Reduce to R^k and rotate so the 7 framing directions are the FIRST 7
    coordinates, which is what makes subbundle_leakage(k=7) the actual test of
    Paper 9's SO(7) reduction rather than a test of an arbitrary subspace.
    """
    # Sample contexts to fit the reduction on.
    samples = [c0]
    for mu in range(7):
        for s in (+delta, -delta):
            cc = c0.copy(); cc[mu] += s
            samples.append(cc)
    stack = np.vstack([enc(c) for c in samples])
    stack = stack - stack.mean(axis=0, keepdims=True)
    U, S, Vt = np.linalg.svd(stack, full_matrices=False)
    B = Vt[:k].T                                        # d x k

    # Framing direction for each plane, in the reduced coordinates.
    G = []
    for mu in range(7):
        cp = c0.copy(); cp[mu] += delta
        cm = c0.copy(); cm[mu] -= delta
        g = (enc(cp) - enc(cm)).mean(axis=0) @ B
        G.append(g)
    G = np.array(G)                                     # 7 x k

    Q, _ = np.linalg.qr(np.column_stack([G.T, np.eye(k)]))
    Q = Q[:, :k]                                        # k x k orthonormal

    def embed(c: np.ndarray) -> np.ndarray:
        return enc(c) @ B @ Q

    return embed, B, Q, G


def _so_generators(k: int, seed: int, block: Optional[int] = None):
    """
    Seven skew-symmetric generators. If `block` is given, every generator is
    block-diagonal with blocks (block, k - block), so the first `block`
    coordinates span a subspace that transport preserves EXACTLY.
    """
    rng = np.random.default_rng(seed)
    gens = []
    for _ in range(7):
        g = rng.normal(size=(k, k))
        g = g - g.T
        if block is not None:
            m = np.zeros((k, k), dtype=bool)
            m[:block, :block] = True
            m[block:, block:] = True
            g = g * m                      # kill the off-block coupling
        gens.append(g / max(np.linalg.norm(g), 1e-12))
    return gens


def rigid_control(embed, c0: np.ndarray, k: int, seed: int = 7,
                  block: Optional[int] = None):
    """
    Control: a context action that is EXACTLY rigid by construction. Same probe
    geometry, same dimension, same estimator - only the context action is
    replaced by a pure rotation, so curvature here is the numerical noise floor.

    IMPORTANT (defect corrected 2026-08-27, CLAUDE_LOG.md Entry 006 section 4).
    Rigidity and subbundle-parallelism are DIFFERENT properties and the first
    version of this file conflated them. A rigid action has zero curvature, but
    a rotation generated by dense skew matrices does NOT preserve any
    distinguished coordinate subspace - so the "rigid control" was reported as
    "parallel by construction" while leaking MORE than the real model, which is
    what invalidated the R-4 verdict.

    Pass block=7 for a control whose 7-dimensional subbundle really is parallel
    (leakage must be ~0), and block=None for one that is rigid but generic
    (leakage must be large). The two together bracket the measurement.
    """
    E0 = embed(c0)
    gens = _so_generators(k, seed, block)

    def embed_rigid(c: np.ndarray) -> np.ndarray:
        M = sum((c[mu] - c0[mu]) * gens[mu] for mu in range(7))
        w, V = np.linalg.eig(M)
        R = np.real(V @ np.diag(np.exp(w)) @ np.linalg.inv(V))
        return E0 @ R

    return embed_rigid


# ==========================================================================
# Measurement
# ==========================================================================
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--probes", type=int, default=len(PROBES))
    ap.add_argument("--k", type=int, default=16)
    ap.add_argument("--h", type=float, default=0.08)
    ap.add_argument("--drop", default="", help="comma-separated probe words to remove; breaks the confound where a word is both a framing token and a probe (CLAUDE_LOG.md Entry 006 s4)")
    args = ap.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dropped = [w.strip() for w in args.drop.split(",") if w.strip()]
    probes = [p for p in PROBES[:args.probes] if p not in dropped]
    k = args.k
    assert len(probes) > k, "need more probes than reduced dimensions"

    print("=" * 78)
    print("ENG-4.4  SEMANTIC CURVATURE AGAINST A REAL MODEL")
    print("=" * 78)
    print("model        : %s" % args.model)
    print("device       : %s" % device)
    print("probes       : %d concepts%s" % (
        len(probes),
        ("  (dropped: %s)" % ", ".join(dropped)) if dropped else ""))
    print("context      : R^7, framing intensity of %s" % ", ".join(PLANES))
    print("reduction    : %d dims, first 7 = the interrogative subbundle" % k)
    print("step h       : %.3f" % args.h)
    print()

    t0 = time.time()
    enc = FramedEncoder(args.model, probes, device)
    c0 = np.ones(7) * 0.6
    embed, B, Q, G = build_reduced_embed(enc, c0, k)
    conn = SemanticConnection(embed, h=args.h)
    conn_ctl = SemanticConnection(rigid_control(embed, c0, k), h=args.h)

    results: Dict[str, float] = {}

    # ---- 1. Is the context action rigid? -------------------------------
    print("-" * 78)
    print("1. RIGIDITY OF THE CONTEXT ACTION")
    print("-" * 78)
    print("   Curvature can only arise where the Procrustes fit is INEXACT")
    print("   (HYPOTHESIS section 2). So this residual gates everything below.")
    print()
    res_real, res_ctl = [], []
    for mu in range(7):
        cp = c0.copy(); cp[mu] += args.h
        res_real.append(procrustes_transport(
            normalise(embed(c0)), normalise(embed(cp))).residual)
        res_ctl.append(procrustes_transport(
            normalise(conn_ctl.embed(c0)),
            normalise(conn_ctl.embed(cp))).residual)
    results["residual_real"] = float(np.mean(res_real))
    results["residual_ctl"] = float(np.mean(res_ctl))
    print("   %-28s %s" % ("plane", "Procrustes residual (step h)"))
    for mu, p in enumerate(PLANES):
        print("   %-28s %.6f" % (p, res_real[mu]))
    print("   %-28s %.6f" % ("MEAN (real model)", results["residual_real"]))
    print("   %-28s %.3e   <- rigid by construction" % (
        "MEAN (rigid control)", results["residual_ctl"]))
    print()

    # ---- 2. Curvature over the 21 plane pairs --------------------------
    print("-" * 78)
    print("2. SEMANTIC CURVATURE ||F_mu_nu||   (Paper 9 Theorem 3.1)")
    print("-" * 78)
    pairs: List[Tuple[int, int, float]] = []
    for mu in range(7):
        for nu in range(mu + 1, 7):
            _, f = conn.plaquette(c0, mu, nu)
            pairs.append((mu, nu, f))
    pairs.sort(key=lambda x: -x[2])
    _, ctl_f = conn_ctl.plaquette(c0, 0, 1)
    results["F_max"] = pairs[0][2]
    results["F_mean"] = float(np.mean([p[2] for p in pairs]))
    results["F_ctl"] = ctl_f

    print("   strongest non-commuting framing pairs:")
    for mu, nu, f in pairs[:5]:
        print("     %-16s ||F|| = %10.4f" % (
            "%s / %s" % (PLANES[mu], PLANES[nu]), f))
    print("   weakest:")
    for mu, nu, f in pairs[-3:]:
        print("     %-16s ||F|| = %10.4f" % (
            "%s / %s" % (PLANES[mu], PLANES[nu]), f))
    print()
    print("   %-30s %10.4f" % ("mean over 21 pairs", results["F_mean"]))
    print("   %-30s %10.3e   <- noise floor" % (
        "rigid control ||F||", ctl_f))
    ratio = results["F_mean"] / ctl_f if ctl_f > 0 else float("inf")
    results["F_ratio"] = ratio
    print("   %-30s %10.3e" % ("signal / noise", ratio))
    print()

    # ---- 3. Loop hysteresis --------------------------------------------
    print("-" * 78)
    print("3. LOOP HYSTERESIS   (HYPOTHESIS H3: prompt-order effects)")
    print("-" * 78)
    loop_specs = [(0, 3, "who -> why"), (1, 4, "what -> how"),
                  (5, 6, "cause -> effect")]
    hys = []
    for mu, nu, label in loop_specs:
        s = 0.45
        a = c0.copy()
        b = c0.copy(); b[mu] += s
        d = c0.copy(); d[mu] += s; d[nu] += s
        e = c0.copy(); e[nu] += s
        _, dev = conn.holonomy([a, b, d, e])
        _, devc = conn_ctl.holonomy([a, b, d, e])
        hys.append(dev)
        print("   %-22s ||U - I|| = %8.5f   (control %.3e)" % (
            label, dev, devc))
    results["hysteresis"] = float(np.mean(hys))
    print("   %-22s %11.5f" % ("mean", results["hysteresis"]))
    print()

    # ---- 4. The SO(7) test ---------------------------------------------
    print("-" * 78)
    print("4. IS THE 7-PLANE SUBBUNDLE PARALLEL?   (Paper 9's SO(7) reduction)")
    print("-" * 78)
    print("   Paper 9 reduces the structure group to SO(7). That is valid only")
    print("   if the 7-plane subbundle is preserved by transport.")
    print()
    print("   Bracketed between TWO controls (defect fix, Entry 006 section 4):")
    print("     PARALLEL control - block-diagonal generators, subbundle exactly")
    print("       preserved, so leakage MUST be ~0 at every step.")
    print("     GENERIC control  - dense generators, rigid but no preserved")
    print("       subspace, so leakage MUST be large once the step is big enough.")
    print("   If those two do not separate, the step is too small and the")
    print("   measurement is void regardless of what the real model reads.")
    print()

    conn_par = SemanticConnection(
        rigid_control(embed, c0, k, seed=7, block=7), h=args.h)
    conn_gen = SemanticConnection(
        rigid_control(embed, c0, k, seed=7, block=None), h=args.h)

    def sweep(cn, step):
        return float(np.mean(
            [cn.subbundle_leakage(c0, mu, 7, step=step) for mu in range(7)]))

    def rot_size(cn, step):
        """||R - I|| for a step: shows whether transport is doing anything."""
        vals = []
        for mu in range(7):
            cp = c0.copy(); cp[mu] += step
            R = procrustes_transport(
                normalise(cn.embed(c0)), normalise(cn.embed(cp))).R
            vals.append(np.linalg.norm(R - np.eye(R.shape[0])))
        return float(np.mean(vals))

    # ---- rotation-magnitude matching --------------------------------
    # A nominal step is NOT a fair basis for comparison. The generic control's
    # rotation grows without bound in the step, while the real model's
    # saturates around ||R - I|| ~ 0.1. Comparing leakage at equal STEP
    # therefore compares a large rotation against a small one, and a small
    # rotation leaks little out of ANY subspace. The controls must be matched
    # on ||R - I||, not on step, or the bracket is rigged in the paper's favour.
    def generic_at_rotation(target: float) -> Tuple[float, float]:
        """Bisect the generic control's step to match a target ||R - I||."""
        lo, hi = 1e-3, 64.0
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if rot_size(conn_gen, mid) < target:
                lo = mid
            else:
                hi = mid
        st = 0.5 * (lo + hi)
        return st, sweep(conn_gen, st)

    steps = [0.5, 1.0, 2.0, 4.0, 8.0]
    print("   %-6s %9s %9s %9s %9s %11s" % (
        "step", "PARALLEL", "real", "GENERIC", "|R-I|real", "GEN@matched"))
    table = []
    for st in steps:
        lp, lr, lg = sweep(conn_par, st), sweep(conn, st), sweep(conn_gen, st)
        rr = rot_size(conn, st)
        _, lgm = generic_at_rotation(rr)          # generic, same rotation size
        table.append((st, lp, lr, lgm, lg, rr))
        print("   %-6.2f %8.2f%% %8.2f%% %8.2f%% %9.4f %10.2f%%" % (
            st, 100 * lp, 100 * lr, 100 * lg, rr, 100 * lgm))
    print()
    print("   GEN@matched is the generic control re-measured at the step where")
    print("   ITS rotation size equals the real model's. That column, not the")
    print("   raw GENERIC one, is the honest comparison.")
    print()

    # Pick the smallest step at which the controls actually separate.
    # Validity now requires the MATCHED generic control (t[3]) to separate
    # from the parallel control (t[1]). Raw generic (t[4]) is not admissible.
    valid = [t for t in table if t[3] - t[1] > 0.02 and t[1] < 0.05]
    results["r4_valid"] = bool(valid)
    if valid:
        st, lp, lr, lg = valid[0][0], valid[0][1], valid[0][2], valid[0][3]
        results["leak_step"] = st
        results["leak_parallel"] = lp
        results["leak_7plane"] = lr
        results["leak_generic"] = lg
        print("   Controls separate first at step = %.2f "
              "(parallel %.2f%%, matched-generic %.2f%%)." % (st, 100 * lp, 100 * lg))
        print("   R-4 is measurable at that step; verdict below uses it.")
    else:
        print("   CONTROLS NEVER SEPARATE across the swept range.")
        print("   R-4 remains void - do not read the real-model column.")
    print()

    # ---- Verdicts, COMPUTED from the measurements ----------------------
    print("=" * 78)
    print("FINDINGS")
    print("=" * 78)
    print("(each verdict below is derived from the numbers above at runtime)")
    print()

    rigid = results["residual_real"] < 10 * max(results["residual_ctl"], 1e-12)
    print("R-1  Is the context action rigid?")
    if rigid:
        print("     RIGID. Residual is at the control level, so the")
        print("     representation carries no measurable curvature and Paper 9's")
        print("     F = 0 holds trivially on this chart.")
    else:
        print("     NOT RIGID. Mean residual %.4f against a control of %.1e."
              % (results["residual_real"], results["residual_ctl"]))
        print("     Reframing DEFORMS the relational geometry of the probe set;")
        print("     it does not merely rotate the frame. By HYPOTHESIS section 2")
        print("     this is exactly the condition under which curvature exists,")
        print("     so a non-zero F below is a real property of the model and")
        print("     not an artifact of the estimator.")
    print()

    curved = results["F_ratio"] > 100
    print("R-2  Paper 9 Theorem 3.1: understanding as F_mu_nu = 0")
    if curved:
        print("     REFUTED AS A DESCRIPTION OF THIS MODEL. Mean ||F|| = %.4f"
              % results["F_mean"])
        print("     against a noise floor of %.1e - a factor of %.1e."
              % (results["F_ctl"], results["F_ratio"]))
        print("     The strongest non-commuting pair is %s / %s."
              % (PLANES[pairs[0][0]], PLANES[pairs[0][1]]))
        print("     This does NOT falsify the framework. It says a real learned")
        print("     representation sits far from the flat connection the paper")
        print("     treats as the normal case, so F = 0 is a limit to be")
        print("     approached, not a property to be assumed.")
    else:
        print("     CONSISTENT. ||F|| is within %.0fx of the noise floor."
              % results["F_ratio"])
    print()

    print("R-3  HYPOTHESIS H3: loop hysteresis / prompt-order effects")
    print("     Mean ||U - I|| = %.5f over three closed framing loops."
          % results["hysteresis"])
    if results["hysteresis"] > 1e-3:
        print("     Present and measurable. Order of framing changes the")
        print("     representation you end up with, which is H3 confirmed on")
        print("     this chart and is the same tensor as R-2.")
    else:
        print("     Not detected above threshold on these loops.")
    print()

    print("R-4  Paper 9's SO(7) reduction")
    if not results["r4_valid"]:
        print("     VOID - NOT A RESULT. The parallel and generic controls did")
        print("     not separate at any swept step, so the leakage measure has")
        print("     no discriminating power here and the real-model column")
        print("     carries no information. Reported as a broken measurement")
        print("     rather than as weak evidence either way.")
    else:
        lp = results["leak_parallel"]
        lk = results["leak_7plane"]
        lg = results["leak_generic"]
        st = results["leak_step"]
        print("     At step = %.2f, with controls verified to bracket:" % st)
        print("       parallel-by-construction  %6.2f%%" % (100 * lp))
        print("       7 interrogative planes    %6.2f%%" % (100 * lk))
        print("       generic subspace (rotation-matched)  %6.2f%%" % (100 * lg))
        # Where does the real reading sit between the two controls?
        span = max(lg - lp, 1e-12)
        frac = (lk - lp) / span
        print("     The 7-plane reading sits %.0f%% of the way from the parallel"
              % (100 * frac))
        print("     control to the generic one.")
        if frac < 0.25:
            print("     SO(7) IS DEFENSIBLE on this chart. The interrogative")
            print("     planes behave much more like a parallel subbundle than")
            print("     like an arbitrary subspace, which is what the paper's")
            print("     structure-group reduction requires.")
        elif frac > 0.75:
            print("     SO(7) IS NOT SUPPORTED on this chart. The 7 planes leak")
            print("     about as badly as an arbitrary subspace, so they do not")
            print("     span a parallel subbundle and SO(7) is a LOSSY CHART of")
            print("     an SO(d) connection. Paper 9 must restate the reduction")
            print("     as an approximation rather than a structural fact.")
        else:
            print("     PARTIAL. The planes are measurably better than arbitrary")
            print("     but well short of parallel, so the reduction is an")
            print("     approximation whose error is now quantified rather than")
            print("     either vindicated or refuted.")
    print()

    print("-" * 78)
    print("SCOPE. One model, one chart, one probe set. The caveat in")
    print("HYPOTHESIS section 6 stands: the connection may depend on this")
    print("framing construction. What has changed is that the claim is now")
    print("attached to a measurement that could have come out the other way.")
    print("-" * 78)
    print("forward batches: %d   elapsed: %.1fs" % (enc.calls, time.time() - t0))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
