# Walkthrough - Bible & Global Topic Modeling

We have successfully performed a complete global topic modeling run on the entire markdown corpus—including the 66 books of the Bible—and restarted the visualizer server.

## Summary of Accomplishments

### 1. Global Topic Modeling Run
- **Script:** [cluster_topics.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/cluster_topics.py)
- **Data Extracted:**
  - Scanned all 1,262 markdown documents (including the Bible books in `_VFT MD/bible/by_book/`).
  - Chunked and parsed **169,791 paragraphs** of text.
- **Embedding & Clustering:**
  - Generated 384-dimensional embeddings using `all-MiniLM-L6-v2` on the GPU.
  - Reduced dimensionality to 5 dimensions using UMAP (with `n_neighbors=15`, `cosine` metric, and fixed `random_state=42`).
  - Clustered the reduced dimensions using HDBSCAN (`min_cluster_size=15`, `min_samples=5`).
  - Identified **2,646 semantic topics** across the corpus.
  - Successfully mapped all paragraphs to their corresponding topic IDs and wrote the mappings to [cluster_mapping.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/cluster_mapping.json).

### 2. Topic Hegemony Classification
- **Script:** [classify_documents.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/classify_documents.py)
- **Process:**
  - Automatically triggered by `cluster_topics.py` upon successful mapping.
  - Extracted semantic fingerprint keywords for each of the 2,646 topics.
  - Embedded each topic's keyword signature and computed cosine similarities against the descriptions of the 16 Hegemony Points.
  - Classified all 2,646 topics to their dominant Hegemony point and saved coordinates to [topic_ism_mapping.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/topic_ism_mapping.json).

### 3. Visualizer Server Restart
- **Script:** [start_viewer.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/start_viewer.py)
- **Status:** Launched and running in the background on port 8000.
- **URL:** [http://localhost:8000/viewer.html](http://localhost:8000/viewer.html)

## Verification
1. Checked that `cluster_mapping.json` (60 MB) and `topic_ism_mapping.json` (3.3 MB) have been fully populated with the latest runs.
2. Verified that the background HTTP server is running actively on port 8000.
3. Open the web browser at [http://localhost:8000/viewer.html](http://localhost:8000/viewer.html). In **Linguistic Sentence Compass** mode, you can select any Bible book (e.g. `63_II_John.md` or `01_Genesis.md`) to view the mapped sentence clusters and their Hegemony vector mappings.
