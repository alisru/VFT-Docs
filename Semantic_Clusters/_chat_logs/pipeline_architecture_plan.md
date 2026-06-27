# Pipeline Architecture Plan: Semantic Programming & Document Reconstruction (Calibrated v2)

This document outlines the end-to-end technical pipeline to transform the VFT corpus into a structured, templated, and navigable knowledge base. It incorporates corrections and feedback from the Claude audit.

---

## Calibrated Pipeline Flow

```
   [Raw Vector DB (Qdrant)]
              │
              ▼
   Step 1: Semantic Clustering  ──► [UMAP/HDBSCAN topic boundary mapping]
              │
              ▼
   Step 2: Pre-Filter & Sorting ──► [Filter fragments < 8 words; Sort by Layer using VFT domain keywords]
              │
              ▼
   Step 3: Pruning / Deduplication ─► [Prune duplicates at strict 0.92 cosine similarity]
              │
              ▼
   Step 4: Bridge Sentence Pass ──► [EXTRACT fragments with >= 0.65 affinity to BOTH clusters simultaneously]
              │
              ▼
   Step 5: Template Slotting    ──► [Map clean, isolated fragments to Concept/Axiom slots]
              │
              ▼
   Step 6: Sequential Reconstruction ─► [AI AGENT (LLM) CALL: One document at a time]
              │
              ▼
   Step 7: Gap & Coverage Scan  ──► [Re-embed and verify distance < 0.25]
```

---

## Detailed Step Specification & Calibrations

### Step 1: Semantic Clustering & Inventory
* **Objective**: Group paragraphs into distinct topic clusters.
* **Process**: Deterministic Python (UMAP to 5D, HDBSCAN to find centroids).

### Step 2: Pre-Filter & VFT-Domain Stratification (Calibrated)
* **Pre-Filter**: Discard any retrieved fragment containing fewer than **8 words** to strip out metadata, headers, stray reference numbers, and page links.
* **VFT-Domain Sorting**: Categorize paragraphs into layers (Definition, Assertion, Conditional, Example) using **VFT-specific domain heuristics**:
  * **DEFINITION**: Triggered by VFT glossary terms (e.g. `υ axis`, `psi axis`, `Upsilon`, `Psi`, `hēgemonikon`, `psochic hegemony`, `logos`, `phronesis`, `attractor`).
  * **CONDITIONAL**: Triggered by logic thresholds, limits, and rules (e.g. `if `, `when `, `unless`, `threshold`, `limit`, `gap`, `dissonance`, `rNet`, `delta H`).
  * **EXAMPLE**: Triggered by case studies, auditee names, or historical scenarios (e.g. `case p`, `case n`, `Taylor`, `Hanson`, `Dutton`, `Medicare`).
  * **ASSERTION**: Core claims, mathematical tensor statements, and equations (default category).

### Step 3: Pruning & Deduplication
* **Calibration**: The cosine similarity threshold is set to **$0.92$** to drop syntactically identical sentences while preserving conceptual nuances.

### Step 4: Bridge Sentence Extraction (Calibrated)
* **Objective**: Extract paragraphs that genuinely sit between two clusters.
* **Calibration**: A paragraph is only flagged as a bridge if it has a high affinity (**$\ge 0.65$ cosine similarity to both Cluster A and Cluster B simultaneously**). They are removed from the main fragment pools and routed directly to the footer as **Cross-References**.

### Step 5: Template Slot Mapping
* **Process**: Map clean fragments to template slots.

### Step 6: Sequential Narrative Reconstruction
* **Calibration**: staged JSON files will be outputted for **one document at a time** (e.g., `staged_hegemonikon.json`). I (Antigravity) will read and reconstruct each document sequentially in the chat window, preventing context window truncation.

### Step 7: Gap & Coverage Scan
* **Process**: Re-embed completed documents and verify cosine distance to centroid is $< 0.25$.

---

## The Four Target Documents to Reconstruct

1. **`Concept: Worldview_Construction_Math.md`** (Concept template)
   * *Axiom dependency*: Built upon the primitives of Consciousness as an anti-entropic ordering force ($\infty^{++}$) and Spacetime as a negating potential ($\infty^{--}$).
   * *Concept attributes*: Matrix equations, saddle-shape geometry, and the scales of judgment.
2. **`Concept: The_Hegemonikon.md`** (Concept template)
   * *Core focus*: Stoic foundations, Epictetus' dichotomy of control, rational mind compass.
3. **`Concept: Four_Quadrants_and_Attractors.md`** (Concept template)
   * *Core focus*: GG/LG/LE/GE quadrants and the 16 coordinate alignments.
4. **`Concept: Ontological_Auditing_and_Helixis.md`** (Concept template)
   * *Core focus*: 7-Vector Audit, $rNet$, $\Delta H$, and Helixis Tensor deconstruction.
