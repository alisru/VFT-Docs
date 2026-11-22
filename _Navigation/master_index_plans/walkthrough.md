# Walkthrough: Master Index Expansion & Topic Landscape Mode

## Overview
We expanded the **Master Project Index** from a narrow `_VFT MD`-only documentation list into a unified ecosystem catalog indexing **5,036 files across 9 sovereign thematic categories**. We also implemented a full **Landscape Map Mode** directly inspired by the video-game map geometry developed in `peek_explorer`, where folders are treated as spatial topic territories and categories.

---

## What Was Added & Upgraded

### 1. Expanded Indexing Engine
- **File**: [`_AI files and chat logs/generate_master_index.py`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_AI%20files%20and%20chat%20logs/generate_master_index.py)
- **Coverage**: Scans across `_VFT MD`, `Visualisers`, `bluesky_bot`, `Reality Class'ification project`, `Reality Classification v2`, `hegemony_attractor`, `_Navigation`, `chat_context`, `_Personal_Files`, plus sibling projects (`value-physics`, `peek_explorer`, and `12axes`) linked seamlessly via `_projects`.
- **9 Thematic Topic Domains**:
  1. `⚛️ Vector Field Theory & Physics` (476 files)
  2. `🧭 Actualism & Consciousness` (863 files)
  3. `🏛️ Hegemonic Kanon & Political Audits` (1,186 files)
  4. `📈 Value Physics & Econophysics` (241 files)
  5. `🤖 Autonomous Bots & Social Agents` (272 files)
  6. `🌌 Interactive Visualizers & Simulations` (1,316 files)
  7. `📖 Ontology & Semantic Dictionaries` (143 files)
  8. `🛠️ Desktop & Workspace Tools` (457 files)
  9. `🗺️ Navigation & Master Protocols` (82 files)

### 2. Landscape Map Mode (`Master_Index.html`)
- **File**: [`Master_Index.html`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Master_Index.html) (synced to [`_VFT MD/System/Master_Index.html`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/System/Master_Index.html))
- **Live URL**: `http://localhost:8000/Master_Index.html`
- **Spatial Features**:
  - **Infinite Canvas & Camera**: Smooth mouse-drag panning, mouse-wheel zooming (from 35% bird's-eye to 180% inspection), and animated camera centering.
  - **Central Nexus & Topic Islands**: The central `🏰 VFT Unified Nexus` connects to each of the 9 category rooms via glowing **SVG Bridges**, with peripheral links between conceptually adjacent domains.
  - **Two-Rectangle Edge Lens**: A 64px perimeter inner frame. Any Topic Islands outside the current camera view project onto the margin border as clickable proxy badges (`.lens-proxy`). Clicking any proxy smoothly flies the camera to that territory.
  - **Indoor Room Controls**:
    - Subcategory doorway pills (e.g. `7 Planes`, `Harmonic Tensor`, `Astrology`, `WWSUTRU`) to filter files inside a room in real time.
    - File cards with distinctive badges (`📄 MD`, `🌐 HTML APP`, `🐍 Python`, `📊 Data`, `📑 Doc`).
    - Focus button (`⤢`) to center and zoom in on any room.
  - **HUD Controls**: World View button, Zoom `+`/`-`, Zoom scale readout, Edge Lens toggle, and List/Card toggle.
  - **Real-Time Global Search**: Typing in `/` filters across all 5,000+ files, highlighting matching rooms and dimming non-matching rooms.
  - **Dual Mode**: Instantly toggle between `🗺️ Landscape Mode` and `☰ Tree & Search View`.

### 3. "Web of Things" Subcategory Child Room Spawner
- Clicking any subcategory pill (e.g., `bluesky_bot (83)`) in a room tile dynamically spawns an independent child room on the landscape map.
- The child room is permanently connected to its parent room via a dynamic, glowing SVG bridge.
- Child rooms can be freely dragged, rearranged, focused, and closed.

### 4. In-HTML File Reader & Application Runner
- Clicking any file card opens the file directly on the canvas as an interactive floating window.
- **Markdown (`.md`)**: Rendered directly inside the reader using an integrated Markdown-to-HTML parser.
- **HTML Apps (`.html`)**: Launched inside an interactive `<iframe>` directly within the window.
- **Source Code (`.py`, `.js`, etc.)**: Displayed with formatted monospace code styling.
- Windows feature expand/collapse controls, full drag-repositioning, and close buttons.

### 5. Scroll Collision Fix
- Hovering the mouse over a room tile's file list or a document viewer's content area allows natural, unconstrained scrolling of the content.
- Canvas zooming is prevented during content scrolling.
- Pressing `Shift` while rolling the mouse wheel allows zooming the canvas even when the cursor is positioned over a tile.

### 6. Semantic Gluon & Dynamic Trajectory Theory
- Formal theoretical document drafted and synchronized:
  - [`_VFT MD/Physics/Semantic_Gluon_and_Dynamic_Trajectory_Theory.md`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_VFT%20MD/Physics/Semantic_Gluon_and_Dynamic_Trajectory_Theory.md)
  - [`_Navigation/master_index_plans/semantic_gluon_dynamic_trajectory_theory.md`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/_Navigation/master_index_plans/semantic_gluon_dynamic_trajectory_theory.md)
- Incorporates the complete three-tier geometry of the user's Relativity Map diagrams:
  - **Tier 1 (Singularity)**: Central `[IS]` ground state with four diagonal projection ray channels.
  - **Tier 2 (Inner Ring)**: Closed perimeter clockwise process loop: `Constructive` $\to$ `Productive` $\to$ `Reductive` $\to$ `Regress` $\to$ `Constructive`.
  - **Tier 3 (Boundary Ring)**: Eight modal boundary states (`will be`, `can be`, `is not`, `can't be`, `won't be`, `was like`, `is like`, `may be`) mapped across the two global super-axes: **Solution** (Left) vs. **Problem** (Right), **Active** (Top) vs. **Counteractive** (Bottom), and **Inclusive** (Left) vs. **Exclusive** (Right).
  - **The Four Verbatim Operational Derivation Laws**: Fully documented and analyzed for defining `IS` into `can't be`, `will be`, `won't be`, and `may be`.
  - **The Four Colored Force Vectors**: 🔴 Red (Active Opposition), 🟢 Green (Possibility Testing), 🔵 Blue (Realization Tension), and 🟣 Magenta (Analogical Elevation).
  - **Dynamic Trajectory Path Integral**: Formulated mathematically as $\mathbf{B}_{D, k} = \int_0^1 w_k(t) \cdot \vec{\sigma}_k(t) \, dt$ for continuous document path analysis and Semantic Git interaction physics.

---

## Verification & Status
- Serving on `http://localhost:8000/Master_Index.html` with HTTP 200 OK.
- `index_data.json` verified with HTTP 200 OK (6.53 MB payload).
- All sibling project deliverables (e.g., `_projects/value-physics/site/index.html`, `_projects/12axes/frontend/dist/index.html`) resolve directly in browser.
