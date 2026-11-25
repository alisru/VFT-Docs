# Qqci Experiment 1: Semantic Linking in a Small Context

Symbolic engine. No training, no learned weights, no GPU. Runs on CPU in under a second.

Run it:

    python3 experiment.py

## What this tests

Whether the 7-plane structure captures what a story IS, well enough that the story can be retold in an unrelated domain and abstract back to the same skeleton. Actualism step 7 (remove names, preserve plane-state patterns, let a new narrative emerge) executed as code, with step 8 ("survive translation into a different setting") as the pass condition.

## Files

- `qqci_engine.py` — the fixed 7-plane metaclass, QqciAddress (the interrogative path IS the identity), SignedSpan, CoherenceVector, the contextual min-max gate, TruthState (carve, accrete, fill, staircase overflow, up-channel escalation), parallax ray intersection, belief states and functional identities from Actualism.
- `sael.py` — the Collapse Dictionary, the parser Phi(L) → ⟨C, α, Δ, σ⟩, plane signatures per canonical action, effect templates.
- `domains.py` — three domain lexicons (sea, startup, orbit) mapping surface nouns to functional types, plus the source story.
- `isomorph.py` — abstract (quotient to typed skeleton), rebind (type-preserving bijection), render (re-clothe in target domain).
- `experiment.py` — the four tests.
- `RESULTS.txt` — full output of the last run.

## Results

| Test | Result |
|---|---|
| B. Round-trip structural identity, sea→startup and sea→orbit | 100.0% |
| B. Chain test, sea→startup→orbit equals sea→orbit | YES |
| C. Bag-of-words baseline, 9 pairs | 56% (5/9) |
| C. SAEL canonical form, 9 pairs | 100% (9/9) |
| D. One-ray content admitted | rejected |
| D. Late dissent on a filled hole | reopened as false_fill, overflow refused |

The baseline fails exactly where predicted: every role-reversal pair scores bag-of-words cosine 1.00 (identical word multisets) and is called "same". The canonical form separates them because the role tuple differs even when the words do not.

## Honest scope limits

1. The parser is hand-seeded over constrained declarative English. It is not open-domain NLP. It exists to test whether the structure holds, not to demonstrate coverage.
2. The plane signatures per canonical action are authored, not learned. The claim under test is that the structure is coherent and preserves meaning, not that the specific weights are optimal.
3. Test C uses 9 hand-built pairs. The real version runs against MRPC and PAWS (Experiment 0.5 in the SAEL proposal). This is a demonstration of the mechanism, not a benchmark result.
4. The functional-type bijection requires the target domain to cover every type in the source. Type coverage is checked and raises rather than inventing a binding.

## Three bugs found by running it, and what they mean

1. **Verb coverage gap.** A domain-flavoured verb absent from the Collapse Dictionary caused the sentence to silently fail to parse, which misaligned every subsequent step and dropped round-trip identity to 25%. Fixed by closing the dictionary and adding `validate_domain()` as a build-time check. The design lesson: a never-parse must be a loud diagnostic, not a silent gap.
2. **Multi-word surface forms broke re-parsing.** "solar flare" could not contract back to the `solarflare` node. Fixed with a rank-2 pre-pass that recomposes known display forms before rank-1 tokenisation. This is the rank ladder doing real work rather than being decorative.
3. **Engagement was conflated with assertion.** The fill logic read a weakly-engaged plane as a dissenting one, so legitimate transitions were flagged false_fill. Split into two quantities: engagement (how involved a plane is, feeds the interpretable mix readout) and assertion (what the plane says, feeds the disagreement detector). A plane that is barely engaged is silent, not dissenting.

A fourth, found in the same pass: a FILLED TruthState refused further material, which made false fill undetectable the moment it was marked resolved. Fill is now provisional — agreeable material adds nothing to a filled hole, dissenting material reopens it. Only TBE (fundamentals) is terminal.

## Next

- Swap the hand-built pairs for MRPC and PAWS subsets (Experiment 0.5).
- Add the reverse rendering inverse and measure round-trip fidelity on free text.
- Port the engagement/assertion split back to `RealityClassification.v2.cs`, which still has the conflated version.
