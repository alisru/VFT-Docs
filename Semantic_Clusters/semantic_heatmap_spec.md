# VFT Semantic Heatmap Specification (v1.0)

This document specifies the architecture, data structures, and user interface for the **VFT Semantic Heatmap** category mapper. The system bridges the logical mathematical constraints of the 7 moral vectors with the lyrical readability of a 7-word "defining poem."

---

## 1. Conceptual Framework: Decoupled Poetic Taxonomy

Instead of grouping documents into flat semantic clusters or using verbose multi-word tag titles, categories are defined as **7-word propositions** where each word corresponds to one of the 7 interrogative vectors of Vector Field Theory (VFT):

$$\text{Category} = \big( w_{\text{who}}, w_{\text{what}}, w_{\text{where}}, w_{\text{why}}, w_{\text{how}}, w_{\text{cause}}, w_{\text{effect}} \big)$$

### Vector to Plane Mapping
1. **Who (Identity):** The MetaPhysical Plane (Agent / Identity)
2. **What (Substance):** The Possible Plane (Action / State / Probability)
3. **Where (Locus):** The Physical Plane (Local Space / Distance)
4. **Why (Purpose):** The Lyrical Plane (Narrative Drive / Intent)
5. **How (Method):** The Logical Plane (Mechanism / Structure)
6. **Cause (Origin):** The Historical Plane (Chronology / Precedent / Sibling Context)
7. **Effect (Consequence):** The Emotive Plane (Impact / Passion / Sibling Context)

---

## 2. Server-Side Alignment Engine

The Flask server (`start_viewer.py`) exposes an endpoint `/api/align` that dynamically computes the similarity between a paragraph's constituent sentences and the 7-word category poem.

### 2.1 The Contextualized Query Protocol
To prevent semantic dilution when comparing a full sentence against a single isolated word, the system wraps each category word in an interrogative template before embedding:

```python
TEMPLATES = {
    "who":     "Identity: {}",
    "what":    "Action/State: {}",
    "where":   "Space/Locality: {}",
    "why":     "Purpose/Drive: {}",
    "how":     "Method/Process: {}",
    "cause":   "Origin/Cause: {}",
    "effect":  "Consequence/Effect: {}"
}
```

### 2.2 Alignment Calculation
For a paragraph $P$ consisting of sentences $S = [s_0, s_1, \dots, s_n]$ and a category poem $C$ composed of words $W = [w_0, w_1, \dots, w_6]$:

1. Generate target query strings:
   $$q_i = \text{TEMPLATES}[i].\text{format}(w_i) \quad \text{for } i \in [0, 6]$$
2. Generate embeddings using `all-mpnet-base-v2`:
   $$\vec{v}_{q_i} = \text{model.encode}(q_i, \text{normalize}=\text{True})$$
   $$\vec{v}_{s_j} = \text{model.encode}(s_j, \text{normalize}=\text{True})$$
3. Compute the $n \times 7$ cosine similarity matrix $M$:
   $$M_{j, i} = \vec{v}_{s_j} \cdot \vec{v}_{q_i}$$

---

## 3. Data Schema & Serialization

Categories are stored in a dynamic registry file `category_registry.json`:

```json
{
  "categories": [
    {
      "id": "cat_awakening",
      "poem": "Ruler acts here seeking truth through memory",
      "vectors": {
        "who": "Ruler",
        "what": "acts",
        "where": "here",
        "why": "seeking",
        "how": "truth",
        "cause": "through",
        "effect": "memory"
      }
    }
  ]
}
```

### API Endpoint: `POST /api/align`
**Request Body:**
```json
{
  "paragraph_text": "The ruler asserts absolute direction here. By analyzing the lineage, we verify the coherence.",
  "category_id": "cat_awakening"
}
```

**Response Body:**
```json
{
  "sentences": [
    "The ruler asserts absolute direction here.",
    "By analyzing the lineage, we verify the coherence."
  ],
  "matrix": [
    [0.90, 0.35, 0.40, 0.20, 0.10, 0.30, 0.15],
    [0.15, 0.45, 0.10, 0.25, 0.80, 0.70, 0.35]
  ]
}
```

---

## 4. Frontend UI Explorer Design

In the explorer (`viewer.html`), the **Semantic Heatmap** is rendered as a clean, interactive 2D grid overlay for paragraphs:

```
+---------------------------------------------------------------------------------------+
|  SENTENCE                         |  WHO   |  WHAT  |  WHERE  |  WHY   |  HOW   |  EFF  |
|                                   | (Ruler)| (acts) |  (here) |(seek.) | (tr.)  | (mem.)|
+---------------------------------------------------------------------------------------+
| s0: The ruler asserts direction...|  [90%] |  [35%] |  [40%]  |  [20%] |  [10%] |  [30%]|
| s1: By analyzing the lineage...   |  [15%] |  [45%] |  [10%]  |  [25%] |  [80%] |  [70%]|
+---------------------------------------------------------------------------------------+
```

### Visual Specifications:
* **Color Mapping:** Cells are colored using a HSL gradient based on similarity score:
  * $\text{Score} < 20\%$: Transparent / Neutral text.
  * $20\% \le \text{Score} \le 50\%$: Low-intensity background tint (e.g. `rgba(56, 189, 248, 0.1)`).
  * $\text{Score} > 50\%$: Rich, vibrant background fill (e.g. `rgba(56, 189, 248, 0.3)` up to `0.8` for $90\%+$).
* **Interactive Tooltips:** Hovering over a cell shows the VFT slot details, e.g.:
  * *Slot: Who (MetaPhysical)*
  * *Target concept: "Ruler"*
  * *Alignment: 90.2% match*
* **Dynamic Creation:** A simple input bar allows the user to write a new 7-word category poem in the sidebar. Typing the poem immediately runs the alignment math across the active document, updating the heatmap visualization in real time.
