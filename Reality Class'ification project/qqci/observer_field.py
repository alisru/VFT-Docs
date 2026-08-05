"""
WORDS AS OBSERVERS OVER A SEMANTIC DENSITY FIELD.

    "we can model words like observers that can see densities of meaning all on
     a mega vector map, then we can view words position, angle, viewfilter,
     range and depth as they view the underlying semantic space"

WHY THE PREVIOUS ATTEMPT FAILED
-------------------------------
qqci_lm.py had each word cast rays at CANDIDATE NEXT TOKENS. That is
co-occurrence voting with parallax vocabulary painted on. Measured: requiring
intersection COST 32% perplexity (2557 vs 1942), every prediction returned
false_fill, and cross-plane disagreement was 0.000 because the context words
usually shared a plane. There was no parallax, because the observers were not
looking at anything -- they were comparing lookup tables.

THE CORRECTION
--------------
Observers look at THE FIELD. A word does not vote on the next word; a word
ILLUMINATES A REGION of the semantic space. What several observers jointly
illuminate is the prediction. That is a real intersection, because two words
with different positions and angles genuinely see different regions.

THE FIVE OBSERVER PARAMETERS, ALL DERIVED FROM CORPUS
-----------------------------------------------------
Nothing here is authored. Each is read off the distribution.

  position    where the word sits in the field.  = its embedding vector
  angle       WHERE IT LOOKS.                     = mean unit direction from
              A word looks toward what follows      itself to its observed
              it; that direction is its gaze.      continuations
  range       how far it sees.                    = mean distance to those
              Diffuse words see far and weakly.    continuations
  depth       how finely it resolves.             = concentration of its gaze
              Specific words resolve deep.         (1 / angular spread)
  viewfilter  WHAT KIND it can see.               = its plane (Q of its Q.q.c)
              A Cause-observer reads causes.

The field itself is a DENSITY over the space: where meaning-mass actually sits,
measured from token frequency in each region.

RELATION TO THE CORPUS
----------------------
- viewfilter is the Qqci plane; depth is the observability cone of the observer
  tree (an observer at tau_n resolves its own subtree, not finer).
- angle is the phase of Proof-by-Resonance 11 (Res = r*e^(i phi), phi the
  "orientation or abstraction angle") made concrete and derivable.
- range is conceptual mass / gravity reach (Proof-by-Resonance 16).
- intersection of view cones is Section 13 parallax, now over a FIELD rather
  than over a candidate list, which is what makes it non-trivial.
"""

from __future__ import annotations

import collections
import json
import math
import os
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from derive_addresses import cooccurrence, embed, read_corpus

ADDR_FILE = os.path.join(os.path.dirname(__file__), "derived_addresses.json")


class ObserverField:
    def __init__(self, dim: int = 64, window: int = 5, cone: float = 0.0,
                 use_density: bool = False, differenced: bool = True):
        self.dim = dim
        self.window = window
        self.cone = cone            # minimum cos(angle) to be inside the view
        self.use_density = use_density
        self.differenced = differenced

    # -- BUILD THE FIELD -----------------------------------------------------

    def fit(self, tokens: Sequence[str], vocab_size: int = 3000) -> None:
        counts = collections.Counter(tokens)
        self.vocab = [w for w, c in counts.most_common(vocab_size) if len(w) > 1]
        self.idx = {w: i for i, w in enumerate(self.vocab)}
        V = len(self.vocab)

        C = cooccurrence(tokens, self.vocab, self.window)
        self.X = embed(C, self.dim).astype(np.float32)      # positions

        # DENSITY of the field: where meaning-mass sits.
        f = np.array([counts[w] for w in self.vocab], dtype=np.float32)
        self.density = f / f.sum()

        # planes = viewfilter, from the derived Q.q.c
        with open(ADDR_FILE, "r", encoding="utf-8") as fh:
            addrs = json.load(fh)
        self.plane = np.array([addrs.get(w, [0, 0, 0])[0] for w in self.vocab],
                              dtype=np.int32)

        # ANGLE / RANGE / DEPTH: read off where each word's continuations lie.
        gaze = np.zeros((V, self.dim), dtype=np.float32)
        dists = np.zeros(V, dtype=np.float32)
        seen = np.zeros(V, dtype=np.float32)
        spread = np.zeros(V, dtype=np.float32)

        prev: List[int] = []
        for t in tokens:
            i = self.idx.get(t)
            if i is None:
                continue
            for j in prev[-self.window:]:
                d = self.X[i] - self.X[j]
                n = np.linalg.norm(d)
                if n < 1e-8:
                    continue
                gaze[j] += d / n            # unit direction j -> i
                dists[j] += n
                seen[j] += 1
            prev.append(i)
            if len(prev) > self.window:
                prev.pop(0)

        seen_c = np.maximum(seen, 1.0)
        self.range_ = dists / seen_c                       # how far it sees
        mean_gaze = gaze / seen_c[:, None]

        # FRAME DIFFERENCING (Section 13.1: "each camera frame-differences to
        # cancel everything static, leaving only moved pixels").
        #
        # MEASURED: without this every observer's parameters were nearly
        # identical (range mean 1.207 in a 1.1-1.33 band, depth mean 0.676 in
        # 0.47-0.81), because every word's continuations are dominated by the
        # SAME dense region. Their view cones coincided, so intersection was
        # identical to union by construction -- no baseline, no parallax.
        #
        # An observer's real view is what it sees DIFFERENTLY from the static
        # background. Subtracting the global mean gaze cancels the background
        # and leaves the displacement that triangulation needs.
        self.background = mean_gaze.mean(axis=0, keepdims=True)
        moved = mean_gaze - self.background if self.differenced else mean_gaze

        norms = np.linalg.norm(moved, axis=1, keepdims=True)
        # ANGLE: the differenced gaze direction.
        self.angle = moved / np.maximum(norms, 1e-8)
        # DEPTH: magnitude of the displacement. A word whose view is just the
        # background has near-zero displacement and therefore no resolving
        # power; a word that looks somewhere distinctive resolves deeply.
        self.depth = norms[:, 0]
        self.depth = self.depth / max(self.depth.max(), 1e-8)
        self.observed = seen

    # -- WHAT AN OBSERVER SEES ----------------------------------------------

    def view(self, i: int) -> np.ndarray:
        """
        Illumination that observer i casts over the whole field.

        A target is seen if it lies within RANGE, inside the ANGULAR CONE
        around the observer's gaze, and it is lit in proportion to the field's
        DENSITY there. DEPTH sharpens the cone: a focused observer illuminates
        a narrow region brightly, a diffuse one a wide region faintly.
        """
        d = self.X - self.X[i]
        dist = np.linalg.norm(d, axis=1)
        dist = np.maximum(dist, 1e-8)
        cos = (d / dist[:, None]) @ self.angle[i]          # inside the cone?

        falloff = np.exp(-dist / max(self.range_[i], 1e-6))   # range limit
        sharp = 1.0 + 8.0 * self.depth[i]                     # depth sharpens
        lobe = np.clip(cos, 0.0, None) ** sharp               # the view cone
        lit = lobe * falloff
        if self.use_density:
            # MEASURED BUG: weighting illumination by raw frequency makes every
            # view cone unigram-dominated -- every prediction came back
            # "the / of / and". What an observer contributes is GEOMETRY (can I
            # see there), not how common the target is. Frequency belongs in
            # the smoothing prior, not in the visibility term.
            lit = lit * self.density
        lit[i] = 0.0
        return lit

    def filtered_view(self, i: int) -> np.ndarray:
        """
        VIEWFILTER: an observer reads the field through its own plane. Targets
        on its plane are seen at full strength, others attenuated. This is what
        makes two observers on DIFFERENT planes see genuinely different things,
        which is the precondition for parallax to mean anything.
        """
        lit = self.view(i)
        same = (self.plane == self.plane[i]).astype(np.float32)
        return lit * (0.35 + 0.65 * same)

    # -- PREDICTION = JOINT ILLUMINATION ------------------------------------

    def predict(self, context: Sequence[str], mode: str = "intersect"
                ) -> np.ndarray:
        idxs = [self.idx[w] for w in context if w in self.idx]
        if not idxs:
            return np.zeros(len(self.vocab), dtype=np.float32)

        views = [self.filtered_view(i) for i in idxs]
        if mode == "intersect":
            # PARALLAX: the region ALL observers illuminate. Geometric mean,
            # so a target unseen by any single observer is extinguished --
            # one-ray content cannot survive.
            acc = np.ones_like(views[0])
            for v in views:
                acc = acc * (v + 1e-9)
            out = acc ** (1.0 / len(views))
        else:
            out = np.mean(views, axis=0)                # union: any observer
        s = out.sum()
        return out / s if s > 0 else out

    # -- EVALUATION ----------------------------------------------------------

    def perplexity(self, tokens: Sequence[str], mode: str = "intersect",
                   n_eval: int = 2000, alpha: float = 0.35) -> float:
        uni = self.density
        logp = 0.0
        cnt = 0
        step = max(1, (len(tokens) - self.window - 1) // n_eval)
        for i in range(self.window, len(tokens) - 1, step):
            ctx = [t for t in tokens[i - self.window:i] if t in self.idx]
            g = self.idx.get(tokens[i])
            if not ctx or g is None:
                continue
            p = self.predict(ctx, mode)
            pm = (1 - alpha) * p[g] + alpha * uni[g]
            logp += math.log(max(pm, 1e-12))
            cnt += 1
            if cnt >= n_eval:
                break
        return math.exp(-logp / max(1, cnt))

    def explain(self, context: Sequence[str], k: int = 5) -> str:
        idxs = [self.idx[w] for w in context if w in self.idx]
        lines = [f"  context {list(context)}"]
        for i in idxs:
            lines.append(f"    observer {self.vocab[i]:<12} "
                         f"plane Q{self.plane[i]+1}  "
                         f"range {self.range_[i]:.3f}  "
                         f"depth {self.depth[i]:.3f}")
        p = self.predict(context)
        top = np.argsort(-p)[:k]
        lines.append("    jointly illuminated:")
        for t in top:
            lines.append(f"      {self.vocab[t]:<14} {p[t]:.4f}  "
                         f"(Q{self.plane[t]+1})")
        return "\n".join(lines)


def main() -> None:
    print("=" * 74)
    print("WORDS AS OBSERVERS OVER A SEMANTIC DENSITY FIELD")
    print("=" * 74)

    tokens = read_corpus()
    split = int(len(tokens) * 0.9)
    train, test = tokens[:split], tokens[split:]

    fld = ObserverField(dim=64, window=5)
    fld.fit(train)
    print(f"tokens {len(tokens):,}   vocab {len(fld.vocab)}   dim {fld.dim}")
    print(f"observer params derived, nothing authored:")
    print(f"    range  min {fld.range_.min():.3f}  "
          f"mean {fld.range_.mean():.3f}  max {fld.range_.max():.3f}")
    print(f"    depth  min {fld.depth.min():.3f}  "
          f"mean {fld.depth.mean():.3f}  max {fld.depth.max():.3f}")
    print()

    print("MOST FOCUSED observers (high depth = narrow, deep view):")
    for i in np.argsort(-fld.depth)[:8]:
        print(f"    {fld.vocab[i]:<14} depth {fld.depth[i]:.3f}  "
              f"range {fld.range_[i]:.3f}  Q{fld.plane[i]+1}")
    print("MOST DIFFUSE observers (low depth = sees everywhere, weakly):")
    for i in np.argsort(fld.depth)[:8]:
        print(f"    {fld.vocab[i]:<14} depth {fld.depth[i]:.3f}  "
              f"range {fld.range_[i]:.3f}  Q{fld.plane[i]+1}")
    print()

    print("-" * 74)
    print("DOES JOINT ILLUMINATION (parallax) BEAT UNION (any observer)?")
    pp_i = fld.perplexity(test, "intersect")
    pp_u = fld.perplexity(test, "union")
    raw = ObserverField(dim=64, window=5, differenced=False)
    raw.fit(train)
    pp_ri = raw.perplexity(test, "intersect")
    pp_ru = raw.perplexity(test, "union")
    print(f"    [no frame-differencing] intersect {pp_ri:,.1f}  union {pp_ru:,.1f}"
          f"   parallax {(pp_ru-pp_ri)/pp_ru:+.1%}")
    print(f"    intersect (all observers must see it) : {pp_i:,.1f}")
    print(f"    union     (any observer suffices)     : {pp_u:,.1f}")
    verdict = "PARALLAX HELPS" if pp_i < pp_u else "parallax costs"
    print(f"    -> {verdict}  ({(pp_u - pp_i) / pp_u:+.1%})")
    print()

    print("-" * 74)
    print("LEGIBILITY: observer parameters and what they jointly light")
    for i in range(fld.window, len(test) - 1, 4211):
        ctx = [t for t in test[i - fld.window:i] if t in fld.idx]
        if len(ctx) >= 3:
            print(fld.explain(ctx))
            print()
            if i > 20000:
                break


if __name__ == "__main__":
    main()
