# Implementation Plan - Sentence-Level Hegemony Compass Integration

We will build a pipeline script to extract sentences, classify their types (definitions, assertions, conditionals, examples), compute their 2D Hegemony coordinates, and build an interactive 2D Compass visualizer mode inside the Explorer UI.

## Proposed Changes

### 1. Sentence Projection Pipeline Script
- **File:** [compile_granular_sentences.py](file:///e:/Vector%20Field%20Theory%20Docs/Semantic_Clusters/compile_granular_sentences.py) [NEW/MODIFY]
- **Functionality:**
  - Segment all markdown files in `_VFT MD` down to individual sentences.
  - **Linguistic Classification (POS tagging vs. Regex Fallback):**
    - Detect if `spacy` is installed and load the English model (`en_core_web_sm`).
    - **With spaCy:** Analyze syntax tree. Tag sentences as:
      - `definition`: e.g. Noun + Verb (is/defines/represents) + ADP (as/to).
      - `conditional`: e.g. Modal Verb + Conjunction (if/then/when/implies).
    - **Without spaCy (Fallback):** Use optimized regex templates mapping structural keywords.
  - **Semantic Cosine Similarity Projection:**
    - Embed the 16 Hegemony points' profiles.
    - Embed each sentence.
    - Compute cosine similarities ($w_i$).
  - **Calculate 2D Coordinates:**
    - Calculate the weighted center of gravity for each sentence on the $[-2.0, +2.0] \times [-2.0, +2.0]$ grid:
      $$\upsilon = \frac{\sum (w_i \times \upsilon_i)}{\sum w_i}$$
      $$\psi = \frac{\sum (w_i \times \psi_i)}{\sum w_i}$$
  - Outputs a structured array database to `granular_sentence_index.json`.

### 2. Update Visualizer Interface
- **File:** [viewer.html](file:///e:/Vector%20Field%20Theory%20Docs/Semantic_Clusters/viewer.html) [MODIFY]
- **Changes:**
  - Load `granular_sentence_index.json` along with topic/document indices.
  - Add **Hegemony Compass Scatterplot** mode/layout inside the Hegemony tab controls.
  - **2D Compass Scatterplot Rendering:**
    - Render a 2D coordinate grid with horizontal axis $\upsilon$ [-2 to 2] and vertical axis $\psi$ [-2 to 2].
    - Plot the 16 fixed point attractors as large anchor nodes.
    - Plot each sentence as a small circle node at its calculated $(\upsilon, \psi)$ coordinate.
    - Color-code the sentence nodes by their linguistic class:
      - Definitions: Purple (Axioms)
      - Conditionals: Orange (Logic)
      - Assertions: Blue (Claims)
      - Examples: Green (Instances)
      - References: Grey (Citations)
  - **Search & Highlighting:**
    - Integrate the keyword filter to highlight matching sentences on the 2D grid.
  - **Selected Sentence Analysis:**
    - Clicking a sentence on the scatterplot displays its full text, parent document link, paragraph/sentence index, and detailed similarity breakdown to the 16 points in the sidebar info panel.

## Verification Plan

### Automated Tests
1. Run `python Semantic_Clusters/compile_granular_sentences.py`.
2. Verify `granular_sentence_index.json` generates correctly with `text`, `type`, and coordinate values.

### Manual Verification
1. Run the local explorer `run_viewer.bat`.
2. Toggle the visualizer mode to **Granular Sentence Compass** and verify the 2D scatterplot distributes sentences correctly.
3. Click nodes and verify coordinates align with their conceptual categories.
