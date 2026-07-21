# Implementation Plan - NSM Vocabulary Reduction using Scaling Modifiers

This plan outlines the design and compilation of a highly reduced English dictionary. It replaces specialized vocabulary with a minimal set of English base words (derived from Natural Semantic Metalanguage) and a direct scaling modifier grammar (using `+` and `-` stacks).

## Goal
To eliminate dictionary bloat and specialized words by mapping them to their isomorphic base concepts decorated with polarity scaling modifiers, preserving human readability and semantic nuance.

## Open Questions

> [!IMPORTANT]
> **1. Handling of Grammatical Tense & Aspect**
> How should we represent verb tenses (e.g., "sprinted" vs "sprinting")? Should we keep the base word root-only (e.g., `run+++`) and rely on context, or use a simple suffix (e.g., `run+++_past`)?
>
> **2. Base Word Set Expansion**
> Standard NSM primes are extremely limited (65 words). To remain functional, should we use an expanded set of basic English semantic molecules (e.g., `run`, `fly`, `sleep`, `write`, `hot`) as valid bases?

## Proposed Grammar Specification

The grammar uses actual English words as semantic anchors, modified directly by polarity stacks:

1. **The Base Axis:** A basic, human-readable English concept (e.g., `run`, `say`, `good`, `big`, `hot`).
2. **The Scale Stack:**
   * **No Modifier (`word`):** The typical, default state of the concept.
   * **Positive Scaling (`word+`, `word++`, `word+++`):** Shifting toward higher speed, intensity, volume, size, or quality. Three pluses (`+++`) represents the absolute limit of capability/degree.
   * **Negative Scaling (`word-`, `word--`, `word---`):** Shifting toward lower speed, intensity, volume, size, or quality. Three minuses (`---`) represents the absolute minimum.

### Examples:
* `run+++` $\rightarrow$ Sprint / Dash (as fast as possible)
* `run+` $\rightarrow$ Jog / Run fast
* `run` $\rightarrow$ Typical run
* `run-` $\rightarrow$ Slow jog / Trot
* `run---` $\rightarrow$ Crawl / Barely moving
* `say+++` $\rightarrow$ Scream / Shout / Shrill
* `say---` $\rightarrow$ Whisper / Mumble / Mutters

---

## Proposed Changes

### [New Project Directory] `_VFT MD/Actualism/Language/translating/nsm_reduction/`

We will create a dedicated project directory to store the reduced dictionary work.

#### [NEW] [reduced_dictionary.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/Actualism/Language/translating/nsm_reduction/reduced_dictionary.md)
A comprehensive reference mapping common complex English words to their simplified base-word and scale-stack equivalents across key categories:
* **Verbs of Motion** (Bases: `go`, `run`, `walk`, `fly`, etc.)
* **Verbs of Communication & Expression** (Bases: `say`, `laugh`, `cry`, etc.)
* **Adjectives of Size & Dimension** (Bases: `big`, `small`, `long`, `short`, etc.)
* **Adjectives of Quality & Value** (Bases: `good`, `bad`, `true`, etc.)
* **Verbs/Nouns of Sensation & Mind** (Bases: `think`, `know`, `feel`, `want`, `see`, `hear`)
* **Quantity & Collective Groups** (Bases: `people`, `thing`, `some`, `all`)

#### [NEW] [translation_example.md](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/Actualism/Language/translating/nsm_reduction/translation_example.md)
A document showcasing side-by-side translations of complex English text into this scaled NSM representation, demonstrating the readability and semantic preservation of the system.

---

## Verification Plan

### Manual Verification
* **Visual Audit:** Review the mapped dictionary with the user to ensure that the mappings match the requested format and semantic intent.
* **Readability Test:** Provide translation examples of varying complexity to prove that a human reader can instantly parse the scaled notation without learning abstract character tables.
