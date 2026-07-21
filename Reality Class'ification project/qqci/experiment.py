"""
Experiment 1: semantic linking in a small context.

Four tests, in order of how much they can hurt the framework:

  A. Isomorphic retelling      - can the skeleton survive a domain change?
  B. Round-trip identity       - does the retold story abstract back to the
                                 same skeleton? (Actualism step 8)
  C. Pair discrimination       - does canonical collapse beat bag-of-words on
                                 paraphrase pairs AND on role-reversal pairs?
                                 This is the PAWS-style vicious case.
  D. Parallax intersection     - do independent plane observers converge on
                                 one voxel, and does a fabricated claim fail
                                 to intersect?

Test C is the one that can falsify. A and B are demonstrations; C is a
measurement against a baseline that is genuinely hard to beat on one of the
two pair types and genuinely easy to beat on the other.
"""

from __future__ import annotations

import math
from collections import Counter
from typing import List, Tuple

from qqci_engine import (
    FillState, Meaning, MeaningRegistry, Plane, QqciAddress, TruthState,
    intersect, depth_map,
)
from sael import parse_sentence, parse_story, validate_domain
from isomorph import abstract, retell
from domains import SEA, STARTUP, ORBIT, SEA_STORY, ALL_DOMAINS


LINE = "=" * 72


# ---------------------------------------------------------------------------
# Baseline: bag-of-words cosine. The thing to beat.
# ---------------------------------------------------------------------------

def bow_cosine(a: str, b: str) -> float:
    ta = Counter(a.lower().rstrip(".").replace(",", "").split())
    tb = Counter(b.lower().rstrip(".").replace(",", "").split())
    keys = set(ta) | set(tb)
    dot = sum(ta[k] * tb[k] for k in keys)
    na = math.sqrt(sum(v * v for v in ta.values()))
    nb = math.sqrt(sum(v * v for v in tb.values()))
    return dot / (na * nb) if na and nb else 0.0


def sael_same(a: str, b: str, domain) -> Tuple[bool, str, str]:
    ta, tb = parse_sentence(a, domain), parse_sentence(b, domain)
    va = ta.voxel() if ta else "<unparsed>"
    vb = tb.voxel() if tb else "<unparsed>"
    return (va == vb and ta is not None), va, vb


# ---------------------------------------------------------------------------
# A. Isomorphic retelling
# ---------------------------------------------------------------------------

def test_a_retelling() -> None:
    print(LINE)
    print("A. ISOMORPHIC RETELLING")
    print(LINE)

    for d in ALL_DOMAINS.values():
        problems = validate_domain(d)
        if problems:
            print("  DOMAIN VALIDATION FAILED:", problems)
            return
    print("  domain validation: all Collapse Dictionary entries closed. OK\n")

    print("  SOURCE (sea):")
    for s in SEA_STORY:
        print("   ", s)

    transitions = parse_story(SEA_STORY, SEA)
    print("\n  CANONICAL FORM (what the story IS, stripped of setting):")
    for t in transitions:
        print("   ", t.voxel())

    print("\n  PLANE-STATE TRACE (Actualism steps 2, 4, 6):")
    print("    %-12s %-8s %-7s %-22s %s" %
          ("action", "belief", "system", "functional identity", "address"))
    for t in transitions:
        print("    %-12s %-8s %-7s %-22s %s" %
              (t.action, t.belief.value, t.systemic.value,
               t.identity.value, t.address))

    for target in (STARTUP, ORBIT):
        rendered, skel, mapping, _ = retell(SEA_STORY, SEA, target)
        print(f"\n  RETOLD IN '{target.name}' DOMAIN:")
        for s in rendered:
            print("   ", s)
        print("    type-preserving bijection:")
        for sid, ent in mapping.items():
            print(f"      {sid:<12} -> {target.pretty(ent)}")


# ---------------------------------------------------------------------------
# B. Round-trip structural identity
# ---------------------------------------------------------------------------

def test_b_roundtrip() -> float:
    print("\n" + LINE)
    print("B. ROUND-TRIP STRUCTURAL IDENTITY (Actualism step 8)")
    print(LINE)
    print("  Retell, then re-parse the retelling and abstract it again.")
    print("  If the framework captures what the story IS, the skeletons match.\n")

    scores = []
    for target in (STARTUP, ORBIT):
        rendered, skel, _, _ = retell(SEA_STORY, SEA, target)
        back = parse_story(rendered, target)
        skel2 = abstract(back, target)
        score, rows = skel.score_against(skel2)
        scores.append(score)
        print(f"  sea -> {target.name:<8} parsed {len(back)}/{len(skel.steps)} steps"
              f" | structural identity {score*100:5.1f}%")
        for row in rows:
            bad = [k for k, v in row.items() if k != "step" and v is False]
            if bad:
                print(f"      step {row['step']} mismatch: {bad}")

    # Chain test: sea -> startup -> orbit. Meaning must survive two hops.
    rendered1, _, _, _ = retell(SEA_STORY, SEA, STARTUP)
    rendered2, _, _, _ = retell(rendered1, STARTUP, ORBIT)
    direct, _, _, _ = retell(SEA_STORY, SEA, ORBIT)
    chained_ok = rendered2 == direct
    print(f"\n  chain test  sea -> startup -> orbit  equals  sea -> orbit : "
          f"{'YES' if chained_ok else 'NO'}")
    if not chained_ok:
        for a, b in zip(rendered2, direct):
            if a != b:
                print(f"      chained: {a}\n      direct : {b}")

    mean = sum(scores) / len(scores)
    print(f"\n  mean structural identity: {mean*100:.1f}%")
    return mean


# ---------------------------------------------------------------------------
# C. Pair discrimination: the falsifier
# ---------------------------------------------------------------------------

PARAPHRASE_PAIRS = [
    ("The harbourmaster rescued the fisherman.",
     "The fisherman was rescued by the harbourmaster."),
    ("The fisherman gave the charts to the harbourmaster.",
     "The fisherman handed the charts to the harbourmaster."),
    ("The storm wrecked the boat.",
     "The storm destroyed the boat."),
    ("The fisherman built a boat from oak.",
     "The fisherman crafted a boat from oak."),
    ("The storm wrecked the boat.",
     "The boat was wrecked by the storm."),
]

REVERSAL_PAIRS = [
    ("The storm wrecked the boat.",
     "The boat wrecked the storm."),
    ("The fisherman gave the charts to the harbourmaster.",
     "The harbourmaster gave the charts to the fisherman."),
    ("The harbourmaster rescued the fisherman.",
     "The fisherman rescued the harbourmaster."),
    ("The fisherman sailed the boat to the reef.",
     "The reef sailed the boat to the fisherman."),
]


def test_c_discrimination(bow_threshold: float = 0.80) -> Tuple[float, float]:
    print("\n" + LINE)
    print("C. PAIR DISCRIMINATION vs BAG-OF-WORDS BASELINE")
    print(LINE)
    print("  Paraphrase pairs SHOULD collapse to one referent.")
    print("  Role-reversal pairs SHOULD NOT (same words, different transition).")
    print(f"  Baseline calls a pair 'same' when BoW cosine >= {bow_threshold}.\n")

    bow_right = sael_right = total = 0

    def run(pairs, expect_same: bool, label: str):
        nonlocal bow_right, sael_right, total
        print(f"  {label}  (expected: {'SAME' if expect_same else 'DIFFERENT'})")
        for a, b in pairs:
            cos = bow_cosine(a, b)
            bow_says = cos >= bow_threshold
            sael_says, va, vb = sael_same(a, b, SEA)
            bow_ok = bow_says == expect_same
            sael_ok = sael_says == expect_same
            bow_right += bow_ok
            sael_right += sael_ok
            total += 1
            print(f"    {'OK ' if bow_ok else 'X  '}BoW  cos={cos:.2f} -> "
                  f"{'same' if bow_says else 'diff'}"
                  f"   |  {'OK ' if sael_ok else 'X  '}SAEL -> "
                  f"{'same' if sael_says else 'diff'}")
            print(f"        {a}")
            print(f"        {b}")
            if not sael_ok or not expect_same:
                print(f"        voxel A: {va}")
                print(f"        voxel B: {vb}")
        print()

    run(PARAPHRASE_PAIRS, True, "PARAPHRASE")
    run(REVERSAL_PAIRS, False, "ROLE REVERSAL")

    bow_acc = bow_right / total
    sael_acc = sael_right / total
    print(f"  RESULT over {total} pairs:")
    print(f"    bag-of-words baseline : {bow_right}/{total}  ({bow_acc*100:.0f}%)")
    print(f"    SAEL canonical form   : {sael_right}/{total}  ({sael_acc*100:.0f}%)")
    return bow_acc, sael_acc


# ---------------------------------------------------------------------------
# D. Parallax intersection and the false-fill check
# ---------------------------------------------------------------------------

def test_d_parallax() -> None:
    print("\n" + LINE)
    print("D. PARALLAX INTERSECTION AND FALSE-FILL DETECTION")
    print(LINE)
    print("  Each active plane casts a constraint ray, not a verdict.")
    print("  Material earns its place only where independent vantages"
          " intersect.\n")

    transitions = parse_story(SEA_STORY, SEA)
    rays = []
    for t in transitions:
        rays.extend(t.rays())

    hits = intersect(rays, min_observers=2)
    depths = depth_map(rays)
    print("  intersections (voxel, observers, strength, deepest first):")
    for target, n_obs, strength, planes in hits:
        plane_names = ",".join(p.name for p in planes)
        print(f"    {n_obs} observers  depth={depths[target]:.3f}  [{plane_names}]")
        print(f"      {target}")

    # A fabricated claim: no plane engages it, so it casts too few rays.
    print("\n  stealth test: a claim with only one vantage supporting it")
    lone = [r for r in transitions[0].rays()][:1]
    lone_hits = intersect(lone, min_observers=2)
    print(f"    rays cast: {len(lone)}  intersections found: {len(lone_hits)}"
          f"  -> {'ADMITTED' if lone_hits else 'REJECTED (one-ray content)'}")

    # The fill cycle over one transition's pool.
    reg = MeaningRegistry()
    reg.seed_alphabet("abcdefghijklmnopqrstuvwxyz")
    t = transitions[2]  # the storm wrecking the boat

    def run_fill(label: str, dissent_plane=None, dissent_value: float = 0.4):
        print(f"\n  fill cycle: {label}")
        ts = TruthState(address=t.address)
        print(f"    carved at {ts.address}  state={ts.state.value}")
        for plane, engagement in sorted(t.planes.items()):
            m = reg.contract(t.roles.get("patient", "boat"),
                             QqciAddress.of(plane))
            assertion = dissent_value if plane == dissent_plane else 1.0
            ts.accrete(m, engagement=engagement, assertion=assertion)
            state = ts.evaluate_fill()
            flag = "  <-- dissenting vantage" if plane == dissent_plane else ""
            print(f"    accrete {plane.name:<7} engage={engagement:.2f} "
                  f"assert={assertion:.2f}  sharpness={ts.sharpness:.2f}  "
                  f"state={state.value}{flag}")
        print(f"    mix readout (engagement): {ts.engagement.readout()}")
        print(f"    assertion disagreement  : {ts.coherence.disagreement:.3f}")
        if ts.state == FillState.FILLED:
            child = ts.drill_into(Plane.WHY)
            print(f"    === reached, staircase overflows -> child at "
                  f"{child.address}")
        else:
            try:
                ts.drill_into(Plane.WHY)
                print("    ERROR: gate should have refused")
            except RuntimeError:
                print(f"    staircase gate correctly refused to overflow "
                      f"(state={ts.state.value})")
            up = ts.escalate()
            print(f"    up-channel: {'escalated to parent' if up else 'root reached, marked ' + ts.state.value}")

    run_fill("all vantages agree (a real transition)")
    run_fill("one vantage dissents (stealth content)",
             dissent_plane=Plane.EFFECT)


# ---------------------------------------------------------------------------

def main() -> None:
    print("\nQQCI SEMANTIC LINKING EXPERIMENT 1")
    print("symbolic engine, no training, no learned weights\n")
    test_a_retelling()
    mean_identity = test_b_roundtrip()
    bow_acc, sael_acc = test_c_discrimination()
    test_d_parallax()

    print("\n" + LINE)
    print("SUMMARY")
    print(LINE)
    print(f"  B  round-trip structural identity : {mean_identity*100:.1f}%")
    print(f"  C  bag-of-words baseline accuracy : {bow_acc*100:.0f}%")
    print(f"  C  SAEL canonical form accuracy   : {sael_acc*100:.0f}%")
    verdict = "PASS" if (sael_acc > bow_acc and mean_identity > 0.95) else "FAIL"
    print(f"\n  verdict: {verdict}")
    print("  (PASS means: meaning survived domain translation, and canonical")
    print("   collapse discriminated referents better than surface overlap.)")


if __name__ == "__main__":
    main()
