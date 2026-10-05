# Plan 002 – Pure Semantic Topic Detection & KeyBERT Representation – 2026-10-04

Historic log. Maintained alongside plan_001.

## Problem Identified
The initial clustering used raw uncentered mean embeddings and simple word-frequency counts. This resulted in:
1. Hubness / anisotropy: conversational assistant boilerplate pulled different chats into generic catch-alls.
2. Inaccurate topic names: relying on frequency picked up common words rather than distinct conceptual topics.
3. Path heuristics were considered but rejected: they do not generalize to external Gemini web chats or browser-captured threads.

## Solution Implemented (Pure Semantics)
1. **Anisotropy Correction**:
   - Chat embeddings are mean-centered against the corpus mean vector $\mu$, eliminating generic dialogue bias without external signals.
   - Cosine distance matrix is computed on normalized mean-centered vectors.
2. **Agglomerative Average-Linkage Clustering**:
   - Pure NumPy implementation clustering chats with distance threshold ~0.78.
   - Preserves user-renamed and locked topics.
3. **KeyBERT + Contrastive c-TF-IDF Topic Representation**:
   - Cleans markdown syntax, brackets, code blocks, URLs, and percent encodings.
   - Extracts clean n-gram phrase candidates (1-grams, 2-grams).
   - Computes cross-cluster document frequency $df$.
   - Embeds candidate phrases via local `BAAI/bge-small-en-v1.5`.
   - Scores each candidate against cluster centroid vector:
     $$\text{Score} = \text{cosine\_sim}(v_{\text{cand}}, v_{\text{centroid}}) \times \ln(1 + N / df)$$
   - Discovers distinct, human-readable semantic topic names (e.g. `audit words / qqci dictionary / project qqci` for the QQCI dictionary audit, `australian kanon / parlinfo` for Kanon audit, `bluesky bot / bot / article` and `bluesky bot / aletheialauncher pyw` for the Bluesky bot).
   - Removed c-TF-IDF inverse-frequency distortion where coding syntax (e.g. `str`, `def`) drowned out the subject. Normalized compound terms (e.g. `bluesky_bot` -> `bluesky bot`) and prioritized cosine similarity to the cluster centroid.
4. **"Related - How?" Invariant**:
   - Pairwise chunk similarity between chats extracts the closest matching passage pair and shared semantic vocabulary.

## Current State
- `ctx.server` running locally at `http://127.0.0.1:8765`.
- Ingested 75 chats (5,630 chunks embedded offline via ONNX runtime).
- 17 coherent semantic topics identified and served via `/api/tree`.
- Next: Gemini web import adapter (Takeout / JSON drop folder / extension receiver).
