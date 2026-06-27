# Implementation Plan - Macro Attractors & Isms Visualizer

We will integrate high-level categorical clusters ("attractors") into the Vis.js semantic map based on the 16-point Hegemony Map (incorporating the 32 philosophical Isms - 16 optimisms and 16 pessimisms).

## Proposed Changes

### 1. Document Classification Script
- **Script:** [classify_documents.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/classify_documents.py) [NEW]
- **Functionality:**
  - Loads `cluster_mapping.json`.
  - Groups paragraphs by file.
  - Defines the 16 points, their quadrants (GG, LG, LE, GE), sub-vectors (e.g. `gg-gg`), and the 32 philosophical Isms (e.g., `Realism / Historicism`).
  - Uses `SentenceTransformer("all-MiniLM-L6-v2")` to embed the description of each of the 16 points.
  - For each document, embeds the document's filename and first 3 paragraphs, then calculates cosine similarity to the 16 point embeddings.
  - Assigns each document to its highest-scoring point, recording the main quadrant, sub-vector, and philosophical Isms.
  - Outputs the classification mapping to `doc_ism_mapping.json`.

### 2. Update Semantic Web Visualizer
- **File:** [viewer.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/viewer.html) [MODIFY]
- **Changes:**
  - Load both `cluster_mapping.json` and the new `doc_ism_mapping.json`.
  - **Macro Attractors in the Graph:**
    - Inject 4 central quadrant nodes:
      - **Greater Good (GG)** (Reality Cluster, Purple)
      - **Lesser Good (LG)** (Human/Spirit Cluster, Blue)
      - **Lesser Evil (LE)** (Social/Abstract Cluster, Orange)
      - **Greater Evil (GE)** (Base/Material Cluster, Red)
    - Inject 16 sub-node points connected to their respective main quadrant nodes. Each sub-node is labeled with its sub-vector and the two Philosophical Isms (e.g. `gg-gg: Realism / Historicism`).
  - **Document Nodes Alignment:**
    - Color-code document bubbles based on their assigned quadrant (Purple, Blue, Orange, Red) to make quadrants instantly recognizable.
    - Connect each document node to its assigned 16-point sub-node via a faint, low-spring-constant physical edge, causing document bubbles to cluster beautifully around their semantic gravity wells.
  - **UI Controls and Sidebar:**
    - Add a collapsible legend explaining the 4 quadrants and their corresponding Isms (optimisms and pessimisms).
    - Add filter controls to highlight specific quadrants, or filter by individual Isms.
    - When a document is clicked, display its dominant quadrant, sub-vector, and Isms in the info sidebar.

## Verification Plan

### Automated/Local Execution
1. Run `python classify_documents.py` to generate `doc_ism_mapping.json`.
2. Inspect `doc_ism_mapping.json` to verify that classifications make sense.

### Manual Verification
1. Start the local server `start_viewer.py`.
2. Open `http://localhost:8000/viewer.html` and verify the network graph shows the 4 main quadrants and 16 ism nodes.
3. Drag nodes and toggle physics to ensure the layout settles nicely.
