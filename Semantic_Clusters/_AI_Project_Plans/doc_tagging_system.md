# Document Tagging System — Implementation Log

## Goal
Build a two-layer semantic tag system for all VFT documents:
1. **Ism tags** — philosophical/moral coordinate (e.g., `Relationalism`, `Chaos`, `Faith`)
2. **Subject tags** — plain English literal topics (e.g., `consciousness`, `qualia`, `hard problem`, `philosophy of mind`)

These tags will be used to intelligently group documents into NotebookLM notebooks by actual content affinity rather than alphabetical or folder structure.

---

## Architecture (Agreed)

```
Topic Cluster
    +-- Ism label       → already done via topic_ism_mapping.json ✓
    +-- Subject label   → MISSING — this is what we're building
```

Documents get the FULL SET of labels from ALL clusters their paragraphs significantly hit (not just the dominant one), filtered by frequency threshold (>=N paragraphs per cluster to count).

Three layers per document:
- `ism_tags`: list of ism coordinates from significant clusters
- `subject_tags`: list of plain English subject labels from significant clusters
- `discipline_tags`: high-level field (philosophy, geopolitics, economics, theology, etc.)

---

## Key Discovery — Cluster Quality Problem

**Test document:** `_VFT MD/io/information_is_qualia (3).md`

This document is clearly about:
- Consciousness theory / philosophy of mind
- Qualia / the hard problem of consciousness
- VFT 7-plane model applied to phenomenology
- Information theory as it relates to experience
- Critique of IIT, Functionalism, Panpsychism, Eliminative Materialism, etc.

**Actual cluster assignments from vdb:**
- 103/240 paragraphs → Topic -1 (noise/unclustered)
- Topic 1578 (30 paragraphs): `kpmg, demystifying, foi` — WRONG (Australia trade docs)
- Topic 1083 (16 paragraphs): `blending, q41, q42, gap` — partial VFT
- Topic 2017 (14 paragraphs): `neuroscience, brain, frontiersin` — closest match
- Topic 1690 (8 paragraphs): `capex, budgetary, allocation` — WRONG (energy policy)
- Topic 1686 (7 paragraphs): `co2e, emissions, electricity` — WRONG (climate)

**Conclusion:** The HDBSCAN clusters are NOT reliable as a semantic tagging source.
They group paragraphs by surface-level word co-occurrence with random other documents in the corpus,
not by the actual topic of the document. Using cluster → subject label mapping will produce garbage tags.

---

## Options — How to Actually Get Good Subject Tags

### Option A: Cluster relabelling (does not fix root problem)
Label the clusters better, but the clusters themselves are still semantically polluted.
A consciousness paper should not be in the same cluster as KPMG trade reports
just because they share incidental vocabulary.

### Option B: Per-document keyword extraction with a curated taxonomy
Define a taxonomy of subject keywords manually. Scan each document for those keywords.
Tags are assigned when keyword density exceeds a threshold. No reliance on cluster quality.

Pros: Deterministic, human-interpretable, you control the vocabulary
Cons: Requires building and maintaining the taxonomy

### Option C: LLM-based per-document tagging
Ruled out — no API calls without explicit user instruction.

### Option D: Use document-level embeddings (not paragraph clusters)
Embed the whole document as one vector, then find nearest neighbours from a set of
pre-defined "anchor" topic vectors. More semantically accurate than paragraph-level HDBSCAN.

---

## Current Status

- [x] cluster_mapping.json — paragraph-level cluster assignments (exists, but unreliable for tagging)
- [x] topic_ism_mapping.json — cluster → ism label (exists)
- [x] doc_ism_mapping.json — document → ism (exists, inherited cluster quality problem)
- [ ] topic_subject_mapping.json — cluster → plain English subject (NOT BUILT)
- [ ] doc_subject_tags.json — document → subject tags (NOT BUILT)

---

## Next Steps (pending user decision on approach)

1. Decide on tagging method (B vs D vs hybrid)
2. If B: draft the subject taxonomy — disciplines + concrete subject list
3. If D: script to embed anchor topic vectors + score each document against them
4. Build doc_subject_tags.json
5. Combine with doc_ism_mapping.json for full two-layer per-document tag set
6. Use combined tags to validate/re-evaluate notebook groupings

---
Log started: 2026-06-28
