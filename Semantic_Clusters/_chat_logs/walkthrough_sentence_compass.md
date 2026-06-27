# Walkthrough - Linguistic Sentence Compass (2D Scatterplot)

We have successfully implemented the Linguistic Sentence Compass (2D Scatterplot) visualization mode and compiled a high-performance sentence-level indexing database.

## Changes Made

### 1. Sentence-Level Classifier & Indexer Pipeline
- **File:** [compile_granular_sentences.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/compile_granular_sentences.py) [NEW]
- **Functionality:**
  - Traverses the 1,196 project markdown files, parses 289,773 sentences, and filters out short snippets.
  - Utilizes a spaCy syntax dependency tree and Part-of-Speech (POS) tags pipeline to classify sentences into five linguistic roles:
    - `definition`: Axioms / Definitions (subject + Copula + complement)
    - `conditional`: Logic / Rule statements (contains conditionals like "if", "when", or modals like "must", "should")
    - `example`: Concrete examples or instances ("for example", "e.g.")
    - `reference`: Citations and external references ("ref.", "see Figure")
    - `assertion`: Declarative statements / claims (default)
  - Leverages a CUDA-accelerated `SentenceTransformer` (`all-MiniLM-L6-v2`) on the GPU to encode all 289,773 sentences.
  - Maps sentences to the 16 Hegemony coordinates using cosine similarity and writes the results to [granular_sentence_index.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/granular_sentence_index.json).

### 2. 2D Compass UI Integration
- **File:** [viewer.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/viewer.html) [MODIFY]
- **Added Features:**
  - **Linguistic Sentence Compass Mode:** A new attraction layout dropdown option `Linguistic Sentence Compass (2D Scatterplot)` (`value="sentence"`).
  - **Dynamic Document Selector Integration:** Automatically shows the document selector dropdown when this mode is selected (just like in granular topic mode).
  - **Performance Optimization (Selected-Doc Filtering):** Restricts the rendering of sentence nodes in the graph to the currently selected document to prevent browser freeze when handling the 289,773 records.
  - **2D Weighted Coordinates Projection:** Projects the sentence coordinates using a similarity-cubed gravity well formula:
    $$\upsilon = \frac{\sum (w_i^3 \times \upsilon_i)}{\sum w_i^3}$$
    $$\psi = \frac{\sum (w_i^3 \times \psi_i)}{\sum w_i^3}$$
  - **Visual Color Coding:** Color codes sentence nodes on the scatterplot according to their linguistic class (Axioms are Blue, Logic is Orange, Assertions are Slate, Examples are Green, References are Pink).
  - **Faint Attractor Anchors:** Sentence nodes are connected to their dominant Hegemony point attractor via extremely faint lines.
  - **Detailed Sidebar Inspector:** Clicking a sentence node shows its full text, parent file name, paragraph/sentence index, and its exact similarity match values for all 16 Hegemony coordinate points.

## Verification & Testing
- Ran the compilation pipeline successfully to build the 214 MB [granular_sentence_index.json](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Semantic_Clusters/granular_sentence_index.json) containing all 289,773 parsed and classified sentences.
- Modified the browser viewer to load and parse the index, then test-rendered selected documents.
- Confirmed that only the sentences from the selected document are visualized, ensuring high rendering frame rates and avoiding vis.js canvas bottlenecks.
