# Implementation Plan: Horizontal Grid Timeline (32-Category Matrix)

This plan details the design and implementation of the Horizontal Grid Timeline view mode in the Timeline tab, alongside the un-baking of VFT categories into 32 distinct Optimisms/Pessimisms.

---

## 1. Proposed Changes

### 1.1 Category Translation Logic (32-Cell Split)
We will add a helper in the UI (`viewer.html`) to map raw VFT points/isms directly to the 32 distinct grid cells shown in your VFT diagram. 

We will map them using the specific `isms` and `node_name` properties returned by the `/api/timeline` endpoint:

* **16 Optimisms (GG / LG Quadrants):**
  * `"Reality (Truth)"` $\leftarrow$ matches `"Realism"` or `"Reality"`
  * `"History (Context)"` $\leftarrow$ matches `"Historicism"` or `"History"`
  * `"Language (Connection)"` $\leftarrow$ matches `"Language"` or `"Communication"` (under Optimism)
  * `"Psychology (Understanding)"` $\leftarrow$ matches `"Psychology"` (under Optimism)
  * `"The World (Fortitude)"` $\leftarrow$ matches `"The World"` or `"Nature"`
  * `"Internal Judgment (Justice)"` $\leftarrow$ matches `"Internal Judgment"` or `"Conscience"` (under Optimism)
  * `"Sociology (Empathy)"` $\leftarrow$ matches `"Sociology"` or `"Empathy"`
  * `"Society itself (Community)"` $\leftarrow$ matches `"Society"` or `"Community"`
  * `"Learning (Prudence)"` $\leftarrow$ matches `"Learning"` or `"Empiricism"`
  * `"Emotional-physics (Temperance)"` $\leftarrow$ matches `"Emotional-physics"` or `"Stoicism"`
  * `"Meta-Physics (Imagination)"` $\leftarrow$ matches `"Meta-Physics"` or `"Imagination"`
  * `"Physics (Objectivity)"` $\leftarrow$ matches `"Physics"` or `"Objectivity"`
  * `"Intelligence (Hope)"` $\leftarrow$ matches `"Intelligence"` or `"Hope"`
  * `"Religion (Charity)"` $\leftarrow$ matches `"Religion"` or `"Charity"`
  * `"Spirituality (Faith)"` $\leftarrow$ matches `"Spirituality"` or `"Faith"`
  * `"Maths (Order)"` $\leftarrow$ matches `"Maths"` or `"Order"`

* **16 Pessimisms / Isms (LE / GE Quadrants):**
  * `"Chaos (Structurelessness)"` $\leftarrow$ matches `"Chaos"`
  * `"Nihilism (Belief in Nothing)"` $\leftarrow$ matches `"Nihilism"`
  * `"Hatred (Active Ill-Will)"` $\leftarrow$ matches `"Hatred"`
  * `"Despair (Negative Conviction)"` $\leftarrow$ matches `"Despair"`
  * `"Denial (Rejection of Fact)"` $\leftarrow$ matches `"Denial"`
  * `"Dogma (Closed Mind)"` $\leftarrow$ matches `"Dogma"`
  * `"Indulgence (Lack of Control)"` $\leftarrow$ matches `"Indulgence"`
  * `"Folly (Willful Ignorance)"` $\leftarrow$ matches `"Folly"`
  * `"Anarchy (Dissolution)"` $\leftarrow$ matches `"Anarchy"`
  * `"Apathy (Inability to Care)"` $\leftarrow$ matches `"Apathy"`
  * `"Corruption (Perversion of Morality)"` $\leftarrow$ matches `"Corruption"`
  * `"Cowardice (Refusal to Facts)"` $\leftarrow$ matches `"Cowardice"`
  * `"Confusion (Self-Ignorance)"` $\leftarrow$ matches `"Confusion"`
  * `"Deceit (Ill-Will)"` $\leftarrow$ matches `"Deceit"`
  * `"Erasure (Denial of Record)"` $\leftarrow$ matches `"Erasure"`
  * `"Delusion (The Greater Lie)"` $\leftarrow$ matches `"Delusion"`

---

### 1.2 HTML UI Panel Updates (`viewer.html`)

#### 1.2.1 View Mode Toggles
We will add a toggle group at the top of the Timeline workspace:
```html
<div class="timeline-mode-toggles" style="display: flex; gap: 8px; margin-bottom: 12px;">
    <button class="cas-premium-btn active" id="btn-timeline-vertical" onclick="switchTimelineMode('vertical')">☰ List View</button>
    <button class="cas-premium-btn" id="btn-timeline-horizontal" onclick="switchTimelineMode('horizontal')">box⊞ Grid View</button>
</div>
```

#### 1.2.2 Horizontal Grid Container
We will insert `#timeline-grid-wrapper` (hidden by default) inside the Timeline workspace:
* Pinned left column showing the **32 VFT Categories** (vertical scroll).
* Pinned top row showing the sorted **Dates** (horizontal scroll).
* A sticky CSS table layout displaying intersecting notes as small clickable badges, preserving direct click-to-open logic.

---

## 2. Verification Plan

### 2.1 Visual Verification
* Check that both "List View" and "Grid View" buttons are visible.
* Toggle to "Grid View" and verify that *Physics* and *Meta-Physics* are separated into their own distinct rows.
* Check that *The Soul Orchid* maps to the `Learning` or `Emotional-physics` row (and any other categories based on its isms).

### 2.2 Navigation Verification
* Click a file card inside the 2D grid matrix and verify it opens the document reader.
