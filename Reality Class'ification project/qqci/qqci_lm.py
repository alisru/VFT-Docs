"""
THE QQCI LANGUAGE MODEL -- your engine, predicting text. No PyTorch, no
gradient descent, no borrowed architecture.

WHY THIS EXISTS
---------------
qqciformer.py forked Leech-LILA and swapped a matrix in. The ablation showed
the swap was a tautology (a named orthonormal basis and a random one span the
same space and the learnable layers absorb the rotation), and everything else
of yours was either identical across arms or measurably inert. It trained, and
it was not your model.

This is your model.

THE MECHANISM, FROM THE SCOPE DOC
---------------------------------
Section 12.3: "Meaning-finding is contraction down the ladder: the alphabet-TS
of a query string composes to a word-TS whose identity contracts against stored
higher-rank compositions. This is mathematically the same operation attention
performs (query-key contraction), performed over structured named ranks instead
of learned keys."

So there are NO learned query/key projections. The keys are the stored
content-addressed compositions. Prediction is contraction against them.

Section 7: "Learning is population, not architecture search." Reading the
corpus carves addresses and caches them (Query IS the Write). That is the
entire training procedure. No backprop anywhere in this file.

Section 13: prediction is PARALLAX INTERSECTION. Each context word is an
observer at its own plane position. Each casts a constraint RAY at candidate
continuations. Material earns its place only where rays from INDEPENDENT
vantages intersect. One-ray content is stealth and is penalised, not accepted.

Section 12.4 / 11.2: the accreted candidates go into a TruthState, the
Coherence Gate (R_net = 1/prod, NOT a mean) decides fill, and cross-plane
disagreement marks FALSE_FILL. A prediction that arrives by false fill is
reported as such instead of being emitted with confidence.

WHERE THE ADDRESSES COME FROM
-----------------------------
derive_addresses.py: PPMI co-occurrence -> SVD -> recursive 7-way partition to
depth 3. Every word gets a real Q.q.c. Not spelling (measured useless), not
hand-authored (the input read back).
"""

from __future__ import annotations

import collections
import json
import math
import os
import random
from typing import Dict, List, Optional, Sequence, Tuple

from derive_addresses import read_corpus
from qqci_engine import (
    FillState, MeaningRegistry, Plane, QqciAddress, Ray, TensorRank,
    TruthState, intersect,
)

ADDR_FILE = os.path.join(os.path.dirname(__file__), "derived_addresses.json")
ALPHABET = "abcdefghijklmnopqrstuvwxyz'"


def load_addresses() -> Dict[str, Tuple[int, int, int]]:
    with open(ADDR_FILE, "r", encoding="utf-8") as fh:
        return {w: tuple(a) for w, a in json.load(fh).items()}


def to_qqci(a: Tuple[int, int, int]) -> QqciAddress:
    """(Q,q,c) in 0..6  ->  a real depth-3 interrogative path."""
    return QqciAddress.of(Plane(a[0] + 1), Plane(a[1] + 1), Plane(a[2] + 1))


class QqciLM:
    """
    Population, not training. Contraction, not attention. Parallax, not softmax.
    """

    def __init__(self, addrs: Dict[str, Tuple[int, int, int]],
                 window: int = 4, min_observers: int = 2):
        self.addrs = addrs
        self.window = window
        self.min_observers = min_observers

        # Rank-0 seed: the enumerable TBE floor (Section 8 / 12.3).
        self.registry = MeaningRegistry()
        self.registry.seed_alphabet(ALPHABET)

        # The populated store. Query IS the Write: reading carves these.
        #   assoc[context_word][next_word] = count
        self.assoc: Dict[str, collections.Counter] = {}
        self.unigram: collections.Counter = collections.Counter()
        self.total = 0
        self.carved = 0

    # -- LEARNING = POPULATION (Section 7) -----------------------------------

    def populate(self, tokens: Sequence[str], limit: Optional[int] = None
                 ) -> None:
        """
        Read the corpus and carve. Every (context word -> next word) pair is a
        rank-2 composition cached at a content-addressed identity. No gradients.
        """
        n = len(tokens) if limit is None else min(limit, len(tokens))
        for i in range(n - 1):
            w = tokens[i]
            if w not in self.addrs:
                continue
            self.unigram[tokens[i + 1]] += 1
            self.total += 1
            # look back over the window: each prior word observes this one
            lo = max(0, i - self.window + 1)
            for j in range(lo, i + 1):
                ctx = tokens[j]
                if ctx not in self.addrs:
                    continue
                self.assoc.setdefault(ctx, collections.Counter())
                self.assoc[ctx][tokens[i + 1]] += 1

    def carve_word(self, w: str):
        """Contraction down the rank ladder: chars -> word-TS, cached."""
        if w not in self.addrs:
            return None
        self.carved += 1
        return self.registry.contract(w, to_qqci(self.addrs[w]))

    # -- PREDICTION = PARALLAX INTERSECTION (Section 13) ---------------------

    def rays_for(self, context: Sequence[str], top_k: int = 40) -> List[Ray]:
        """
        Each context word is an OBSERVER positioned at its own plane. It casts
        constraint rays at the continuations it has seen. Strength is that
        observer's own evidence, normalised so a frequent word does not
        outvote a rare one by volume alone.
        """
        rays: List[Ray] = []
        for w in context:
            seen = self.assoc.get(w)
            if not seen:
                continue
            plane = Plane(self.addrs[w][0] + 1)     # the observer's position
            tot = sum(seen.values())
            for nxt, c in seen.most_common(top_k):
                rays.append(Ray(observer=w, plane=plane, target=nxt,
                                strength=c / tot))
        return rays

    def predict(self, context: Sequence[str], top_k: int = 40
                ) -> Tuple[Dict[str, float], List[Tuple[str, int, float, List[Plane]]]]:
        """
        Returns (distribution, intersections).

        Candidates supported by >= min_observers INDEPENDENT context words are
        admitted. One-ray content is stealth (Section 13.2): admitted only at a
        heavy discount, never on equal footing.
        """
        rays = self.rays_for(context, top_k)
        if not rays:
            return {}, []

        hits = intersect(rays, min_observers=self.min_observers)
        dist: Dict[str, float] = {}
        for target, n_obs, strength, _planes in hits:
            dist[target] = strength * n_obs          # intersection depth

        # one-ray fallback, discounted: stealth is not refused outright at
        # prediction time, it is admitted weakly and flagged.
        if not dist:
            for r in rays:
                dist[r.target] = dist.get(r.target, 0.0) + r.strength * 0.10
        return dist, hits

    def fill_state(self, context: Sequence[str],
                   hits: Sequence[Tuple[str, int, float, List[Plane]]]
                   ) -> Tuple[FillState, float]:
        """
        Run the winning candidate through the actual TruthState gate: accrete
        one observation per supporting plane, then evaluate. FALSE_FILL means
        the planes disagree about this prediction -- structural low confidence
        that softmax cannot express.
        """
        if not hits:
            return FillState.NEVER_FILLED, 0.0
        target, n_obs, strength, planes = hits[0]
        ts = TruthState(address=to_qqci(self.addrs.get(target, (0, 0, 0))))
        per = min(1.0, strength / max(1, len(planes)))
        for p in planes:
            m = self.registry.carve_or_recall(
                target, QqciAddress.of(p), rank=TensorRank.WORD)
            ts.accrete(m, engagement=1.0, assertion=max(0.05, per))
        st = ts.evaluate_fill()
        return st, ts.coherence.disagreement

    # -- EVALUATION ----------------------------------------------------------

    def perplexity(self, tokens: Sequence[str], n_eval: int = 3000,
                   alpha: float = 0.4) -> Tuple[float, Dict[str, int]]:
        """
        Held-out perplexity, smoothed against the unigram so an unseen
        continuation is finite rather than infinite.
        """
        vocab = len(self.unigram)
        uni_tot = max(1, self.total)
        logp = 0.0
        cnt = 0
        states: Dict[str, int] = collections.Counter()

        step = max(1, (len(tokens) - self.window - 1) // n_eval)
        for i in range(self.window, len(tokens) - 1, step):
            ctx = [t for t in tokens[i - self.window:i] if t in self.addrs]
            gold = tokens[i]
            if not ctx:
                continue
            dist, hits = self.predict(ctx)
            st, _dis = self.fill_state(ctx, hits)
            states[st.value] += 1

            z = sum(dist.values())
            p_model = (dist.get(gold, 0.0) / z) if z > 0 else 0.0
            p_uni = (self.unigram.get(gold, 0) + 1) / (uni_tot + vocab + 1)
            p = (1 - alpha) * p_model + alpha * p_uni
            logp += math.log(max(p, 1e-12))
            cnt += 1
            if cnt >= n_eval:
                break
        return (math.exp(-logp / max(1, cnt)), dict(states))

    def explain(self, context: Sequence[str]) -> str:
        """
        The legibility payoff: WHY this prediction, by named plane. No
        transformer can produce this line about its own forward pass.
        """
        dist, hits = self.predict(context)
        if not hits:
            return f"  context {list(context)} -> no intersection (one-ray only)"
        lines = [f"  context {list(context)}"]
        for target, n_obs, strength, planes in hits[:5]:
            names = ", ".join(p.name for p in planes)
            lines.append(f"    {target:<14} {n_obs} observers  "
                         f"depth {strength:.3f}   planes: {names}")
        st, dis = self.fill_state(context, hits)
        lines.append(f"    gate: {st.value}   cross-plane disagreement {dis:.3f}")
        return "\n".join(lines)


def main() -> None:
    print("=" * 74)
    print("QQCI LM  --  population, contraction, parallax. No backprop.")
    print("=" * 74)

    addrs = load_addresses()
    tokens = read_corpus()
    split = int(len(tokens) * 0.9)
    train, test = tokens[:split], tokens[split:]
    print(f"tokens {len(tokens):,}   addressed vocabulary {len(addrs)}")

    lm = QqciLM(addrs, window=4, min_observers=2)
    lm.populate(train)
    print(f"populated: {len(lm.assoc):,} observer words, "
          f"{sum(len(v) for v in lm.assoc.values()):,} cached associations")
    print(f"registry:  {lm.registry.size:,} carved nodes "
          f"(rank-0 alphabet seeded as the TBE floor)")
    print()

    print("-" * 74)
    print("HELD-OUT PERPLEXITY (parallax intersection as the predictor)")
    pp, states = lm.perplexity(test)
    print(f"    perplexity : {pp:,.1f}")
    print(f"    gate states: {states}")
    print()

    print("-" * 74)
    print("ABLATION: does PARALLAX matter, or is one observer enough?")
    lm1 = QqciLM(addrs, window=4, min_observers=1)
    lm1.assoc, lm1.unigram, lm1.total = lm.assoc, lm.unigram, lm.total
    pp1, _ = lm1.perplexity(test)
    print(f"    min_observers=1 (no intersection required) : {pp1:,.1f}")
    print(f"    min_observers=2 (parallax required)        : {pp:,.1f}")
    better = "PARALLAX HELPS" if pp < pp1 else "parallax costs"
    print(f"    -> {better}  ({(pp1-pp)/pp1:+.1%})")
    print()

    print("-" * 74)
    print("LEGIBILITY: why each prediction, by NAMED plane")
    rng = random.Random(0)
    starts = [i for i in range(lm.window, len(test) - 1, 977)][:4]
    for i in starts:
        ctx = [t for t in test[i - lm.window:i] if t in addrs]
        if len(ctx) >= 2:
            print(lm.explain(ctx))
            print()


if __name__ == "__main__":
    main()
