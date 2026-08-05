"""
HYPOTHESIS TESTS ON REAL DATA. Every result printed whether it passes or not.

WHY THESE AND NOT OTHERS
------------------------
primitives.py derives `solid` from `liquid`+`freeze` and plane_attention.py
routes a blank to its filler. BOTH ARE CONSTRUCTED: the author chose the seed
and the adversarial case, so neither is evidence about language. They show the
machinery runs, nothing more.

These tests use the REAL corpus (_VFT MD, 533k tokens) and an INDEPENDENT
plane assignment (the NSM reduction dictionaries shipped in the corpus, parsed
by q4_meaning.py). The plane labels were authored for translation work years
before this question existed, and they know nothing about bigram statistics,
so corpus agreement cannot be the labels read back.

THE CONTROL THAT MATTERS
------------------------
Every test compares the NAMED planes against RANDOM classes of identical size.
That is the same discipline as bottleneck_test.py (SVD ceiling vs random
floor): a structure that does not beat a random partition of the same shape is
decoration, however good the story is.
"""

from __future__ import annotations

import collections
import math
import os
import random
import re
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from q4_meaning import BASE_PLANE, load_dictionary
from qqci_engine import Plane

CORPUS_DIR = r"E:\Vector Field Theory\VFT Docs\_VFT MD"
WORD_RE = re.compile(r"[a-z']+")
SEED = 0


# ---------------------------------------------------------------------------
# DATA
# ---------------------------------------------------------------------------

# CRITICAL CONTROL: the corpus CONTAINS the NSM reduction dictionaries that
# supply the plane labels, and those files list synonyms adjacently
# ("hate, loathe, despise" -- all EFFECT). Leaving them in manufactures
# same-plane adjacency out of nothing but the label source's own formatting.
# Any file whose path matches these is excluded from every corpus statistic.
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


def word_planes() -> Dict[str, Plane]:
    """
    word -> plane, from the corpus's OWN NSM reduction dictionaries.
    Independent of every hypothesis below.
    """
    out: Dict[str, Plane] = {}
    for w, form in load_dictionary().items():
        p = BASE_PLANE.get(form.base)
        if p is not None:
            out[w] = p
    return out


# ---------------------------------------------------------------------------
# H1: do adjacent words in real text carry DIFFERENT planes more than chance?
#
# The claim under test (the user's DNA/blank-filling model): a word attaches to
# a word that FILLS what it leaves open. Under the one-plane-per-word model NSM
# gives us, "b fills one of a's open planes" is exactly "b's plane != a's
# plane". So the prediction is:
#
#     real adjacent pairs are MORE plane-diverse than chance.
#
# The rival model (attraction by similarity) predicts the opposite: adjacent
# words share a plane more than chance. Both are can-fail, and they disagree,
# which is what makes this worth running.
#
# CONTROL: the same words, same marginal frequencies, adjacency destroyed.
# ---------------------------------------------------------------------------

def h1_adjacency_complementarity(tokens: Sequence[str],
                                 wp: Dict[str, Plane]) -> Dict[str, float]:
    pairs = [(wp[a], wp[b]) for a, b in zip(tokens, tokens[1:])
             if a in wp and b in wp]
    if len(pairs) < 100:
        return {"n": len(pairs)}

    diff_real = sum(1 for a, b in pairs if a != b) / len(pairs)

    # Control: independent draws from the SAME marginal plane distribution.
    rng = random.Random(SEED)
    left = [a for a, _ in pairs]
    right = [b for _, b in pairs]
    trials = []
    for _ in range(20):
        shuf = right[:]
        rng.shuffle(shuf)
        trials.append(sum(1 for a, b in zip(left, shuf) if a != b) / len(pairs))
    diff_ctrl = sum(trials) / len(trials)
    sd = (sum((t - diff_ctrl) ** 2 for t in trials) / max(1, len(trials) - 1)) ** 0.5

    z = (diff_real - diff_ctrl) / sd if sd > 1e-12 else 0.0
    return {"n": len(pairs), "real_diff": diff_real, "shuffled_diff": diff_ctrl,
            "sd": sd, "z": z}


# ---------------------------------------------------------------------------
# H2: is the NAMED plane a better predictive class than a RANDOM class?
#
# Class-based LM (Brown et al. 1992): P(w'|w) ~ P(class'|class) P(w'|class').
# If the 7 interrogatives carve language at a real joint, they beat a random
# 7-way partition of the same vocabulary with the same class sizes.
# This is the honest version of "are the planes real".
# ---------------------------------------------------------------------------

def _class_bigram_perplexity(tokens: Sequence[str], cls: Dict[str, int],
                             n_classes: int, alpha: float = 0.5
                             ) -> Optional[float]:
    """
    Perplexity of held-out NEXT-CLASS prediction given the current class.
    Measuring at class level (not word level) isolates exactly what the
    partition contributes and nothing else.
    """
    seq = [cls[t] for t in tokens if t in cls]
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


def h2_named_vs_random_classes(tokens: Sequence[str], wp: Dict[str, Plane],
                               n_random: int = 200) -> Dict[str, float]:
    named = {w: int(p) - 1 for w, p in wp.items()}
    pp_named = _class_bigram_perplexity(tokens, named, 7)
    if pp_named is None:
        return {}

    # random partitions preserving each class's SIZE exactly
    words = list(named)
    sizes = collections.Counter(named.values())
    rng = random.Random(SEED)
    scores = []
    for _ in range(n_random):
        shuffled = words[:]
        rng.shuffle(shuffled)
        rand: Dict[str, int] = {}
        i = 0
        for c, n in sizes.items():
            for w in shuffled[i:i + n]:
                rand[w] = c
            i += n
        pp = _class_bigram_perplexity(tokens, rand, 7)
        if pp is not None:
            scores.append(pp)

    arr = np.array(scores)
    better = int((arr <= pp_named).sum())
    return {"pp_named": pp_named, "pp_random_mean": float(arr.mean()),
            "pp_random_sd": float(arr.std(ddof=1)),
            "pp_random_best": float(arr.min()),
            "n_random": len(scores), "n_random_better_or_equal": better,
            "p_value": (better + 1) / (len(scores) + 1),
            "z": float((pp_named - arr.mean()) / arr.std(ddof=1))}


# ---------------------------------------------------------------------------
# H3: does the complementarity BIAS improve next-word ranking on real bigrams?
#
# Architectural test of plane_attention's contribution. For each real bigram
# (a,b), rank all candidate successors by (i) plain co-occurrence similarity
# and (ii) similarity + complementarity bias. Report mean reciprocal rank of
# the TRUE successor on held-out data.
# ---------------------------------------------------------------------------

def h3_complementarity_bias(tokens: Sequence[str], wp: Dict[str, Plane],
                            vocab_size: int = 400, bias: float = 1.0
                            ) -> Dict[str, float]:
    counts = collections.Counter(t for t in tokens if t in wp)
    vocab = [w for w, _ in counts.most_common(vocab_size)]
    idx = {w: i for i, w in enumerate(vocab)}
    V = len(vocab)
    if V < 30:
        return {}

    pairs = [(idx[a], idx[b]) for a, b in zip(tokens, tokens[1:])
             if a in idx and b in idx]
    split = int(len(pairs) * 0.9)
    train, test = pairs[:split], pairs[split:]
    if len(test) < 30:
        return {}

    C = np.zeros((V, V), dtype=np.float32)
    for i, j in train:
        C[i, j] += 1.0
    base = np.log(C + 0.1)

    plane_of = np.array([int(wp[w]) - 1 for w in vocab])
    # complementarity under the one-plane-per-word model: j can fill i's blank
    # iff their planes differ.
    comp = (plane_of[:, None] != plane_of[None, :]).astype(np.float32)

    def mrr(score: np.ndarray) -> float:
        tot = 0.0
        for i, j in test:
            row = score[i]
            rank = 1 + int((row > row[j]).sum())
            tot += 1.0 / rank
        return tot / len(test)

    return {"n_test": len(test), "vocab": V,
            "mrr_similarity": mrr(base),
            "mrr_with_bias": mrr(base + bias * comp),
            "bias": bias}


# ---------------------------------------------------------------------------
# H4: does composition SATURATE? (structural, not corpus)
#
# DisCoCat predicts valence strictly decreases under contraction and that a
# saturated phrase can stand alone. Cheap structural check that the algebra in
# slots.py behaves like a tensor calculus rather than a bag of merges.
# ---------------------------------------------------------------------------

def h5_operator_avoids_operator(tokens: Sequence[str]) -> Dict[str, float]:
    """
    H5: THE FAIR TEST OF COMPLEMENTARITY.

    H1 tested raw adjacency of NSM content words, which is the wrong level:
    adjacent words in running text are mostly not in a head-dependent
    relation, and topical coherence makes same-field words cluster. That
    tests topic, not composition.

    Here is a prediction the blank-filling model makes that similarity does
    NOT, at a level where composition genuinely happens:

      An OPERATOR (a word with required open slots) cannot be completed by
      another operator, because the other has the same slots open. So
      operators must AVOID operators and SEEK hosts.

    Operator proxy: -ly adverbs. Unambiguous modifiers, high valence, need a
    host, and identified WITHOUT NSM or any authored table, so this is
    independent of every label in this project.

    Prediction: P(next is -ly | current is -ly) < P(-ly) base rate.
    Similarity-attraction predicts the opposite (like attracts like), so the
    two models disagree and the test can fail either way.
    """
    LY = re.compile(r"^[a-z]{4,}ly$")
    flags = [bool(LY.match(t)) for t in tokens]
    n = len(flags)
    if n < 1000:
        return {}
    base = sum(flags) / n
    after_op = [flags[i + 1] for i in range(n - 1) if flags[i]]
    if len(after_op) < 100:
        return {}
    cond = sum(after_op) / len(after_op)
    # binomial z for the conditional rate against the base rate
    sd = math.sqrt(max(base * (1 - base) / len(after_op), 1e-18))
    return {"n_tokens": n, "base_rate": base, "n_after_operator": len(after_op),
            "cond_rate": cond, "z": (cond - base) / sd,
            "ratio": cond / base if base > 0 else 0.0}


def h4_saturation() -> Dict[str, float]:
    from primitives import HOSTS, OPERATORS
    from slots import unify

    ok = tot = 0
    drops: List[int] = []
    for opn, op in OPERATORS.items():
        for hn, host in HOSTS.items():
            out = unify(host, op, lemma=f"{opn} {hn}")
            tot += 1
            drops.append(op.valence - out.valence)
            if out.valence <= op.valence and out.saturated:
                ok += 1
    return {"compositions": tot, "saturated": ok,
            "mean_valence_drop": sum(drops) / len(drops) if drops else 0.0}


# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 72)
    print("HYPOTHESIS TESTS  --  real corpus, independent plane labels")
    print("=" * 72)

    tokens = read_corpus()
    wp = word_planes()
    covered = sum(1 for t in tokens if t in wp)
    print(f"corpus tokens      : {len(tokens):,}")
    print(f"NSM-labelled types : {len(wp)}")
    print(f"labelled tokens    : {covered:,} ({covered/max(1,len(tokens)):.1%})")
    print()

    print("-" * 72)
    print("H1  adjacent words carry DIFFERENT planes more often than chance?")
    print("    (blank-filling predicts MORE diversity; similarity predicts LESS)")
    r1 = h1_adjacency_complementarity(tokens, wp)
    if r1.get("n", 0) < 100:
        print(f"    INSUFFICIENT DATA (n={r1.get('n', 0)})")
    else:
        print(f"    pairs                 : {r1['n']:,}")
        print(f"    real adjacent  differ : {r1['real_diff']:.4f}")
        print(f"    shuffled       differ : {r1['shuffled_diff']:.4f}"
              f"  (sd {r1['sd']:.4f})")
        print(f"    z                     : {r1['z']:+.2f}")
        if abs(r1["z"]) < 2:
            print("    VERDICT: NO EFFECT. Adjacency is plane-indifferent.")
        elif r1["z"] > 0:
            print("    VERDICT: supports COMPLEMENTARITY (blanks seek fillers).")
        else:
            print("    VERDICT: supports SIMILARITY attraction, NOT the blank"
                  " model.")
    print()

    print("-" * 72)
    print("H2  are the NAMED planes a better predictive class than RANDOM")
    print("    classes of identical size? (lower perplexity is better)")
    r2 = h2_named_vs_random_classes(tokens, wp)
    if not r2:
        print("    INSUFFICIENT DATA")
    else:
        print(f"    named planes      : {r2['pp_named']:.3f}")
        print(f"    random partitions : {r2['pp_random_mean']:.3f} "
              f"(sd {r2['pp_random_sd']:.3f}, best {r2['pp_random_best']:.3f})")
        print(f"    random better/equal: {r2['n_random_better_or_equal']}"
              f"/{r2['n_random']}   p = {r2['p_value']:.4f}   "
              f"z = {r2['z']:+.2f}")
        if r2["p_value"] <= 0.05:
            print("    VERDICT: named planes BEAT random classes. The partition"
                  " is real.")
        else:
            print("    VERDICT: NOT distinguishable from a random 7-way split.")
    print()

    print("-" * 72)
    print("H3  does the complementarity BIAS improve next-word ranking?")
    r3 = h3_complementarity_bias(tokens, wp)
    if not r3:
        print("    INSUFFICIENT DATA")
    else:
        print(f"    held-out bigrams : {r3['n_test']:,}  vocab {r3['vocab']}")
        print(f"    MRR similarity   : {r3['mrr_similarity']:.4f}")
        print(f"    MRR + bias       : {r3['mrr_with_bias']:.4f}")
        d = r3["mrr_with_bias"] - r3["mrr_similarity"]
        print(f"    delta            : {d:+.4f}")
        print("    VERDICT: " + ("bias HELPS." if d > 0.001 else
                                 "bias HURTS." if d < -0.001 else
                                 "no measurable effect."))
    print()

    print("-" * 72)
    print("H5  FAIR TEST: do OPERATORS avoid OPERATORS and seek hosts?")
    print("    (-ly adverbs, identified without NSM or any authored label)")
    r5 = h5_operator_avoids_operator(tokens)
    if not r5:
        print("    INSUFFICIENT DATA")
    else:
        print(f"    tokens                    : {r5['n_tokens']:,}")
        print(f"    base rate of operators    : {r5['base_rate']:.4f}")
        print(f"    rate right after operator : {r5['cond_rate']:.4f}"
              f"   ({r5['ratio']:.2f}x base)")
        print(f"    z                         : {r5['z']:+.2f}")
        if r5["z"] < -2:
            print("    VERDICT: operators AVOID operators. Supports"
                  " COMPLEMENTARITY.")
        elif r5["z"] > 2:
            print("    VERDICT: operators CLUSTER. Supports similarity, not"
                  " the blank model.")
        else:
            print("    VERDICT: no effect.")
    print()

    print("-" * 72)
    print("H4  does composition saturate (DisCoCat: valence must fall)?")
    r4 = h4_saturation()
    print(f"    compositions      : {r4['compositions']}")
    print(f"    saturated results : {r4['saturated']}")
    print(f"    mean valence drop : {r4['mean_valence_drop']:.2f}")
    print("    VERDICT: " + ("contraction behaves as a tensor calculus."
                             if r4["saturated"] == r4["compositions"]
                             else "SOME COMPOSITIONS FAILED TO SATURATE."))


if __name__ == "__main__":
    main()
