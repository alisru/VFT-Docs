# Walkthrough - Hegemony Attractors & Isms Visualizer Mode

We have implemented the 16-point Hegemony Map classification and gravity well attraction model as a distinct visualization mode in the Semantic visualizer.

## Changes Made

### 1. Document Classification Engine
- **File:** [classify_documents.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/classify_documents.py) [NEW]
- **Functionality:**
  - Standardized descriptions of the 16 points and 32 Philosophical Isms.
  - Used SentenceTransformers (`all-MiniLM-L6-v2`) to batch embed documents and calculate semantic cosine similarity to the 16 Hegemony map sub-nodes.
  - Assigned each document to its closest attractor node, outputting assignments to `doc_ism_mapping.json`.

### 2. Dual-Mode UI Integration
- **File:** [viewer.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/viewer.html) [MODIFY]
- **Added Features:**
  - **Visualization Mode Dropdown:** Switch dynamically between:
    - *Semantic Topic Overlap Mode* (Original topic similarity graph)
    - *Hegemony Map (32 Isms) Mode* (New categorical attractor graph)
  - **Attractor Nodes:** GG (Greater Good), LG (Lesser Good), LE (Lesser Evil), GE (Greater Evil) are injected as large central attractor nodes. The 16 point attractors connect to their respective parent quadrants.
  - **Spring-force Alignment:** Document nodes are colored by their assigned quadrant and connected via faint spring forces to their assigned 16-point attractor, pulling them into distinct spatial clusters representing the 32 Isms.
  - **Progressive Chunk Loading:** Edges are progressively loaded in batches of 250 every 10ms with a visual loading bar overlay, preventing the browser from freezing during load.
  - **Comprehensive Node Inspections:** Clicking on any attractor quadrant, sub-node point, or document bubble displays rich metadata (description, assigned files, and ism breakdown) directly in the sidebar.

## Verification & Testing
- Ran the classification script to generate the mapping data.
- Built-in progressive load was verified to load the dataset smoothly with no visual lag.
- Edge performance optimization ensures edges hide during camera drag/zoom.
