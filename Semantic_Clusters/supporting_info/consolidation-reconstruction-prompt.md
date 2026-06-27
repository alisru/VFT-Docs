# Consolidation Reconstruction Prompt: Specification

The problem with a retrieval dump is that it is a stack of fragments with no internal argument. The reconstruction prompt is the step that collapses that stack into a single coherent canonical document. It runs after retrieval and sorting, and before commit. This document specifies exactly what the prompt must do, why each instruction exists, and what the failure mode looks like without it.

---

## The core problem the prompt must solve

A retrieval dump has the right content in the wrong form. The information is there, scattered across sourced fragments, but the document has no spine. It does not open with a claim, develop that claim through structured reasoning, and close with a conclusion. It opens with a fragment, follows it with another fragment, and ends when the fragments run out.

The reconstruction prompt must impose a spine without adding new claims. Everything in the output must be traceable to the input fragments. The AI's job is grammar, flow, and structure, not generation. The moment the AI starts adding ideas that are not in the fragments, the document stops being a synthesis of your corpus and starts being a hallucination dressed as one.

---

## Pre-conditions before the prompt runs

These must be true before calling the reconstruction prompt, or the output will be worse than the dump.

The fragments have been sorted by layer: definitions first, assertions second, conditionals third, examples last. This ordering is non-negotiable. A synthesis that leads with an example before establishing the definition it illustrates is incoherent regardless of how well it reads.

Near-duplicate fragments have been collapsed to one. If three fragments say the same thing in slightly different words, only the clearest survives into the reconstruction pass. Feeding near-duplicates to the prompt produces a document that circles the same idea three times and reads as padding.

Cross-cluster bridge sentences have been extracted and flagged. These are fragments that sit between two topic clusters. They do not belong in the body of the canonical document. They become the reference links at the end.

The document type has been identified: axiom-level, concept-level, or program-level. The reconstruction prompt behaves differently for each.

---

## The reconstruction prompt: full specification

What follows is the complete prompt template. Variables in brackets are filled at runtime by the pipeline.

---

**SYSTEM**

You are a synthesis engine. Your only function is to reconstruct a coherent canonical document from a set of pre-sorted source fragments. You do not generate new ideas. You do not add claims that are not present in the fragments. You do not editorialize, evaluate, or comment on the content. You write in the first-person authorial voice of the corpus owner. Every sentence in your output must be directly traceable to at least one input fragment.

Your failure modes, in order of severity:

1. Adding a claim not present in any fragment. This is hallucination. It contaminates the canonical document with content that did not come from the corpus.
2. Preserving a near-duplicate instead of merging it. This produces a document that restates the same idea twice and reads as redundant.
3. Reordering the layer sequence. Definitions must precede assertions. Assertions must precede conditionals. Conditionals must precede examples. Violating this order produces an incoherent argument.
4. Preserving source citations inline. The output is a canonical document, not a retrieval dump. Source provenance belongs in the metadata, not in the body text. Remove all inline citations and source tags from the output.
5. Using connective phrases that imply a claim not in the fragments. "This proves that" and "therefore" and "it follows that" are claims. Use them only if the logical relationship they assert is explicitly stated in at least one fragment. Otherwise use neutral transitions: "this is expressed as," "the related formulation is," "the applied form of this is."

**DOCUMENT TYPE:** [axiom | concept | program]

**DOCUMENT TYPE INSTRUCTIONS:**

If axiom: The output is a definition document. It opens with the irreducible statement of the axiom. It develops only what is necessary to make that statement unambiguous. It closes when the definition is complete. Length is short. No examples unless an example is the only way to make the definition unambiguous.

If concept: The output is a framework document. It opens by naming the concept and stating its function. It develops the concept through its attributes, its methods, and its relationship to the axioms it rests on. It closes with the boundary conditions, what the concept does not cover and why. Length is medium.

If program: The output is an applied analysis document. It opens by stating the question or subject being analysed. It develops the analysis by instantiating the relevant concepts and axioms against the subject. It closes with the result coordinate and its interpretation. Length is as long as the analysis requires.

**CLUSTER LABEL:** [the semantic cluster this document belongs to, e.g. "moral-coordinate-system" or "hegemony-foundations"]

**ATTRACTOR COORDINATE:** [the (υ,ψ) coordinate of the cluster centroid, e.g. (+1.2, +0.8)]

**NEAREST ZONE ANCHOR:** [e.g. "Greater Good"]

**SOURCE FRAGMENTS (pre-sorted by layer, near-duplicates collapsed):**

[LAYER: DEFINITION]
[fragment 1]
[fragment 2]
...

[LAYER: ASSERTION]
[fragment n]
...

[LAYER: CONDITIONAL]
[fragment n]
...

[LAYER: EXAMPLE]
[fragment n]
...

**BRIDGE SENTENCES (do not include in body, list as cross-references at end):**
[bridge fragment 1 — links to cluster X]
[bridge fragment 2 — links to cluster Y]

**TASK:**

Write a single canonical document from these fragments. Apply the document type instructions above. Merge near-duplicates into the clearest single statement. Write connective prose between fragments only where the transition requires it. Do not add claims. Do not preserve inline citations. Preserve the layer order. End with a cross-reference section listing the bridge sentences and the clusters they link to.

Output the document only. No preamble, no explanation of what you did, no meta-commentary about the synthesis process.

---

## Why each instruction exists

**"You do not generate new ideas"** exists because the output is supposed to be a canonical representation of the corpus, not an AI expansion of it. The moment new ideas enter, the document is no longer yours.

**"Remove all inline citations"** exists because inline citations are the signature of a retrieval dump. A canonical document has a unified authorial voice. The provenance is preserved in the metadata layer of the vector DB, not in the body text.

**"Layer order is non-negotiable"** exists because definition-before-example is the minimum requirement for a coherent argument. Any synthesis tool that does not enforce this will produce documents that illustrate concepts before establishing them.

**"Do not use 'therefore' unless the relationship is in a fragment"** exists because logical connectives are claims. "A, therefore B" asserts that A causes or implies B. If no fragment makes that assertion, the synthesis is fabricating a logical relationship that may not hold.

**"Output the document only"** exists because meta-commentary about the synthesis process is noise in a canonical document. The pipeline log captures what was done. The document captures what is true.

---

## The gap detection pass (runs after reconstruction)

After the reconstruction prompt produces its output, one more pass runs before commit.

Re-embed the output document. Compare its vector to the cluster centroid. Compute cosine distance.

If distance is below 0.1: full coverage. The output faithfully represents the cluster. Commit.

If distance is between 0.1 and 0.25: partial coverage. The output captures the cluster but there is meaningful semantic territory in the cluster that did not make it into the document. Flag for review. The flagged gap describes a sub-concept that needs its own document.

If distance is above 0.25: poor coverage. The fragments were not representative of the cluster, or the reconstruction lost too much in merging. Do not commit. Return to the retrieval step with a wider similarity radius.

The gap coordinate is the vector subtraction between the output embedding and the cluster centroid. That vector points in the direction of the missing content. It can be used as a query to retrieve the specific fragments that were underrepresented.

---

## Applying this to the Psochic Hegemony dump specifically

The document you received is a program-level dump masquerading as a concept-level synthesis. It has fragments from at least four distinct clusters mixed together: foundational philosophy (the Hēgemonikon), worldview construction math, the attractor coordinate system, and the Helixis Tensor auditing protocol.

These are four separate canonical documents, not one. The reconstruction prompt should not be run on the full dump. The dump needs to be split by cluster first, then each cluster reconstructed independently, then the four resulting documents cross-referenced to each other via their bridge sentences.

The correct pipeline for that dump:

Run HDBSCAN on the fragments to confirm the four clusters.
Run the reconstruction prompt four times, once per cluster, with the appropriate document type for each.
Extract the bridge sentences that cross cluster boundaries.
The four canonical documents plus their cross-reference links replace the single messy dump.

The result is four short, precise, coherent documents instead of one long incoherent one. Each document knows exactly what it is, what layer it belongs to, and what other documents it connects to. That is the semantic programming architecture expressed as actual documents.
