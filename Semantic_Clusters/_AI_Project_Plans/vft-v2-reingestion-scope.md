# VFT v2 Re-Ingestion Scope

Full technical specification for rebuilding the VFT vector database from paragraph-level decontextualised embeddings (v1) to sentence-level contextualised embeddings (v2). This document covers what changes, why, the exact pipeline, the hardware profile, and the quality gate before v1 is retired.

---

## What is changing and why

Three specific decisions in v1 ingestion produced the cluster pollution problem:

**Decision 1: Paragraph-level chunking with no context.**
`content.split('\n\n')` treated every paragraph as a self-contained unit. A paragraph about information transfer in a consciousness paper and a paragraph about information transfer in a KPMG trade document embedded to similar positions because neither carried any signal about the document it came from. The consciousness paper paragraph did not know it was a consciousness paper paragraph.

**Decision 2: all-MiniLM-L6-v2 (22M params, 384 dims).**
Fast and small. Appropriate for general-purpose semantic similarity. Loses nuance on domain-specific philosophical and cross-domain vocabulary. Two paragraphs that are both written in dense academic register but discussing completely different domains can land close together because the model encodes register more strongly than domain meaning at this parameter count.

**Decision 3: Raw HDBSCAN without BERTopic.**
No c-TF-IDF, no auto-labelling. Cluster IDs came out as numbers. Keyword extraction ran as a separate step and inherited the pollution from the clusters it was labelling. The labels were noisy because the clusters were noisy.

**v2 fixes all three at the source.**

---

## The three changes

### Change 1: Sentence-level chunking with contextualised window

Every sentence is extracted individually using spaCy's sentence boundary detection rather than double-newline splitting.

Each sentence is embedded not as raw text but as a contextualised unit assembled as:

`[DOCUMENT TITLE] | [PARAGRAPH TOPIC SENTENCE] | [TARGET SENTENCE]`

The document title anchors the domain. The paragraph topic sentence (first sentence of the parent paragraph) anchors the local argument. The target sentence carries the actual content.

This means a consciousness paper sentence about information transfer embeds with "Information is Qualia | Information is not a physical quantity but a relational one | information transfer in this sense..." as its input. The KPMG sentence embeds with "Trade Policy Brief | The bilateral agreement establishes..." as its input. They no longer land in the same neighbourhood.

The practical consequence is that the 103/240 noise paragraphs in the consciousness paper test case almost entirely disappear. Paragraphs land in noise when they don't have enough distinctive signal to belong to any cluster. Contextualised sentences have more distinctive signal by construction.

### Change 2: all-mpnet-base-v2 (110M params, 768 dims)

Five times the parameters, double the embedding dimensions. Trained on 1 billion sentence pairs with contrastive learning.

Hardware cost on your machine:
- Model loaded in RAM: ~250MB at float16 with inference overhead
- VRAM on GTX 1660 Super (6GB): fits with room, inference runs on GPU
- Estimated throughput at sentence level batched: 2,000-4,000 sentences per second
- Corpus estimate at sentence level: 500,000 to 1,500,000 sentences depending on average document length
- Estimated re-ingestion time: 4-12 minutes for embedding pass alone

Storage cost in Qdrant:
- v1 vectors: 384 dims per paragraph
- v2 vectors: 768 dims per sentence
- Sentence count will be roughly 3-5x paragraph count
- Net storage: approximately 6-10x v1 collection size
- Check current v1 collection size before committing to ensure local disk is sufficient

### Change 3: BERTopic replacing raw HDBSCAN

BERTopic wraps HDBSCAN with UMAP dimensionality reduction and c-TF-IDF auto-labelling. The pipeline is:

1. UMAP reduces 768D vectors to 5D (same as v1, different input dims)
2. HDBSCAN clusters the 5D reduced vectors (same algorithm, cleaner input)
3. c-TF-IDF extracts the most statistically distinctive terms per cluster relative to all other clusters
4. Auto-labels each cluster with its top 4-5 distinctive terms

The output is named topic clusters rather than numbered ones. "consciousness qualia phenomenology experience information" instead of "cluster 2017". The auto-labels become the subject tag candidates without any manual taxonomy work.

BERTopic also produces a topic hierarchy by default, merging similar topics at increasing similarity thresholds. This gives you macro-topics (philosophy of mind, geopolitics, theology) and micro-topics (hard problem of consciousness, Australian housing economics, biblical philology) in the same pass without predefining either level.

---

## The full v2 ingestion pipeline

### Pre-ingestion: document preparation

Scan the corpus for files that should be excluded from ingestion entirely: pure reference lists, bibliography entries, stray metadata files, temp drafts marked DELETEME (several appear in the v1 dump). Create an exclusion list. These files pollute the embedding space with noise that doesn't belong to any real topic.

Input: raw corpus directory
Output: `corpus_manifest.json` listing every file to be ingested with its full path, document title extracted from H1 header or filename, and file type

### Step 1: Sentence extraction with contextualisation

For each file in the corpus manifest:
1. Parse the document into paragraphs (double-newline split as before)
2. For each paragraph, identify the topic sentence (first sentence)
3. Use spaCy `en_core_web_sm` or `en_core_web_trf` (transformer-based, more accurate) to split each paragraph into sentences
4. For each sentence, assemble the contextualised input string: `[doc_title] | [paragraph_topic_sentence] | [sentence_text]`
5. Assign a unique ID to each sentence: `{file_hash}_{paragraph_index}_{sentence_index}`
6. Store: sentence_id, raw_sentence_text, contextualised_input, source_file, paragraph_index, sentence_index, document_title

Input: corpus directory
Output: `sentence_manifest.parquet` (parquet for efficient columnar access at this volume)

Estimated row count: 500,000 to 1,500,000 rows

### Step 2: Embedding pass

Batch embed every contextualised input string using all-mpnet-base-v2 via sentence-transformers.

Batch size: 256 sentences per batch (tunable based on VRAM headroom during the run)
Device: CUDA (GTX 1660 Super)
Output per sentence: 768-dimensional float32 vector

Checkpointing: write embeddings to disk in batches of 10,000 to a `.npy` file. If the run fails mid-way, resume from the last checkpoint rather than restarting. At 1 million sentences a crash without checkpointing wastes the full run.

Input: `sentence_manifest.parquet`
Output: `embeddings_v2.npy` + updated `sentence_manifest.parquet` with embedding index column

### Step 3: VFT layer stratification

Run VFT-domain heuristics on raw sentence text (not contextualised input) to assign layer type. Heuristics run on the raw sentence because the contextualised prefix would trigger false positives on the document title.

Definition triggers: υ, ψ, upsilon, psi, hēgemonikon, hegemonikon, psochic hegemony, logos, phronesis, attractor, rNet, delta H, ΔH, is defined as, refers to, means, denotes
Conditional triggers: if, when, unless, threshold, limit, gap, dissonance, provided that, given that, requires
Example triggers: case, for example, for instance, applied to, in the case of, auditee names (Hanson, Dutton, Albanese, Taylor, etc.), specific country or institution names in analytical context
Assertion triggers: default category for everything that doesn't match above

Pre-filter: discard any sentence under 8 words as metadata noise. Discard sentences that are purely a URL, a citation number, a file path, or a header fragment.

Input: `sentence_manifest.parquet`
Output: `layer_tags.parquet` with sentence_id and layer_type columns

### Step 4: BERTopic clustering

Run BERTopic on the full embedding matrix.

Configuration:
- UMAP: n_components=5, n_neighbors=15, min_dist=0.0, metric=cosine
- HDBSCAN: min_cluster_size=50 (larger than v1 to reduce micro-cluster noise at sentence granularity), min_samples=10
- c-TF-IDF: default BERTopic settings
- Representation model: KeyBERTInspired() for better topic label quality (optional, adds compute)

Output: topic ID per sentence, topic label (auto-generated), topic probability score

Topics with label -1 (noise) are not discarded. They are retained in the manifest with noise flag and reviewed separately. A high noise rate on a specific document is a diagnostic signal that the document is genuinely cross-domain.

Roll-up: aggregate sentence topic assignments to paragraph level (majority vote weighted by topic probability score), then to document level (full tag set of all topics that exceed 5% of the document's sentences).

Input: `embeddings_v2.npy`
Output: `topic_assignments.parquet` with sentence_id, topic_id, topic_label, topic_probability columns

### Step 5: Moral attractor projection

For each sentence embedding, compute the (υ,ψ) coordinate using the centre-of-gravity formula against the 16 attractor base vectors.

This step requires the full 16 attractor definitions with confirmed (υ,ψ) coordinates and their associated ism pairs. This data lives in `The Philosophical Isms of the Hegemony Map.md`. Extract and encode the 16 attractor definitions as short descriptive sentences, embed them with all-mpnet-base-v2 to get 16 base vectors, then assign fixed (υ,ψ) coordinates to each.

For each sentence vector s:
1. Compute cosine similarity w_i between s and each of the 16 attractor vectors
2. Apply softmax normalisation to convert similarities to weights (ensures weights sum to 1 and handles negative similarities correctly)
3. Compute weighted centroid: υ = Σ(w_i × υ_i) / Σw_i, ψ = Σ(w_i × ψ_i) / Σw_i
4. Assign nearest zone anchor based on (υ,ψ) coordinate

Roll-up: paragraph coordinate is the sentence-length-weighted average of its sentence coordinates. Document coordinate is the paragraph-length-weighted average of its paragraph coordinates.

Input: `embeddings_v2.npy` + confirmed attractor definitions
Output: `moral_coordinates.parquet` with sentence_id, upsilon, psi, zone_anchor columns

### Step 6: Bridge sentence extraction

For each sentence, check affinity to its two highest-scoring topic clusters. If the sentence scores ≥0.65 similarity to cluster A AND ≥0.65 similarity to cluster B simultaneously, flag as bridge sentence.

Bridge sentences are tagged with both cluster IDs and extracted to `bridge_sentences.parquet`. They are retained in the main manifest but flagged so the reconstruction prompt routes them to cross-reference sections rather than document body slots.

The 0.65/0.65 dual threshold prevents the false positive problem of a sentence with broad relevance being incorrectly flagged as a bridge. A sentence must genuinely belong to two clusters simultaneously, not just have moderate affinity to a neighbour.

Input: `embeddings_v2.npy` + `topic_assignments.parquet`
Output: `bridge_sentences.parquet` with sentence_id, cluster_a, cluster_b columns

### Step 7: Qdrant v2 collection build

Create a new Qdrant collection `vft_v2` with vector size 768 and cosine distance metric.

Upsert every sentence as a point:
- id: sentence_id (hashed to uint64 for Qdrant compatibility)
- vector: 768-dim embedding
- payload: raw_sentence_text, source_file, paragraph_index, sentence_index, document_title, layer_type, topic_id, topic_label, upsilon, psi, zone_anchor, is_bridge, bridge_clusters (if bridge)

The payload carries the full tag set so every query result is self-describing. No joins required to interpret a result.

Create payload indices on: source_file, layer_type, topic_id, zone_anchor, is_bridge for fast filtered queries.

Input: all parquet files from steps 1-6
Output: `vft_v2` Qdrant collection

---

## Quality gate before v1 retirement

Run three test queries against v2 before switching the active pipeline:

**Test 1: Consciousness paper neighbours.**
Query for nearest neighbours of a known consciousness paper sentence. All top-10 results should be from consciousness, philosophy of mind, or VFT phenomenology documents. Any KPMG, trade policy, or climate documents in the top-10 means contamination persists. v2 fails this gate.

**Test 2: Ism coordinate accuracy.**
Take five sentences with known expected coordinates (hand-labelled from documents you know well). Run attractor projection. Check that the output coordinates land in the correct quadrant. If more than one of five lands in the wrong quadrant, the attractor definitions need recalibration before the collection is used for generation.

**Test 3: BERTopic label coherence.**
Take the five largest topic clusters by sentence count. Read the auto-generated labels. Assess whether the labels match the actual content of the sentences assigned to them. If cluster labels are incoherent (mixing clearly unrelated terms), HDBSCAN parameters need tuning and re-clustering before the collection is used.

All three gates must pass before v1 is marked read-only and v2 becomes the active collection.

---

## What v1 becomes after v2 passes the quality gate

v1 is not deleted. It becomes the audit baseline. If v2 produces unexpected results on a document, v1 can be queried to check whether the result is a v2 artefact or a genuine property of the content. It is also the working collection for Antigravity's current pipeline runs, which should continue uninterrupted during v2 build.

Retirement of v1 is a separate decision made after v2 has been in active use for a sufficient number of document reconstruction runs to confirm stability.

---

## Files produced by this pipeline

`corpus_manifest.json` — file inventory with exclusions marked
`sentence_manifest.parquet` — all sentences with contextualised inputs and source metadata
`embeddings_v2.npy` — raw embedding matrix, checkpointed
`layer_tags.parquet` — VFT layer type per sentence
`topic_assignments.parquet` — BERTopic cluster assignments per sentence with auto-labels
`moral_coordinates.parquet` — (υ,ψ) coordinates per sentence
`bridge_sentences.parquet` — cross-cluster bridge sentence registry
`vft_v2` Qdrant collection — the live queryable database

All parquet files are retained as the ground truth source for the v2 collection. If the Qdrant collection needs to be rebuilt (schema change, corruption, migration), it can be reconstructed from the parquet files without re-running the embedding pass.
