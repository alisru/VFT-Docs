# Implementation Plan 01 — Expand Master Index & Topic/Category Landscape Mode

**Date**: 2026-10-24  
**Status**: Ready to Implement  
**Author**: Antigravity  
**Target Workspace**: `e:\Vector Field Theory\VFT Docs` & cross-workspace projects  

---

## 1. Problem Statement & User Request

The user asked:
> *"expand the master index, also like, i wonder if you can't make a landscape mode like is being developed in the @docs/PEEK_EXPLORER.md project. But where 'folders' are topics and categories"*

### Current Limitations:
1. **Narrow Index Scope**: `generate_vft_index.py` and `index_data.json` only scan `_VFT MD` for `.md` files. They miss:
   - `value-physics` (Econophysics papers, empirical audits, state space, data deliverables)
   - `12axes` (Hegemonic Grid Quiz frontend, backend, audit profiles)
   - `peek_explorer` (Desktop file explorer, documentation, plans)
   - `bluesky_bot` (Aletheia bot, social agents, trinary synthesis)
   - `Reality Class'ification project` & `Reality Classification v2` (QQCI dictionaries, ontology)
   - `Visualisers` (Polytrope, Hegemony Triangle, Basileia sim, 3D models)
   - `_Navigation` (Repo master, taxonomy reviews, topic maps)
   - `chat_context` (Conversation archive & semantic canvas explorer)
   - Key interactive file types like `.html` visualizers, `.py` tools/scripts, and `.json` data.
2. **Missing Spatial / Landscape Overview**: `Master_Index.html` currently only offers a standard 2-column layout (Left: Tree view, Right: Search results). There is no high-level thematic map or spatial landscape to visually explore topics as connected territories.

---

## 2. Solution Architecture

### A. Comprehensive Workspace Index Expansion (`generate_master_index.py`)
Create an expanded, high-performance Python indexer that:
1. Scans the major workspace directories:
   - `_VFT MD` (Vector Field Theory, Actualism, Physics, Protocols, WWSUTRU)
   - `value-physics` (Papers, empirical audits, state space models)
   - `12axes` (Hegemonic quiz frontend, backend, profiles)
   - `peek_explorer` (Windows 11 file manager, landscape architecture, documentation)
   - `bluesky_bot` (Aletheia bot engine, trinary synthesis)
   - `Reality Class'ification project` & `Reality Classification v2` (QQCI semantic dictionary)
   - `Visualisers` & `hegemony_attractor` (Interactive HTML visualizers, 3D models)
   - `_Navigation` (Repo master, topic maps, inventories)
   - `chat_context` (Chat search & canvas database)
2. Categorizes files into **9 Thematic Topics & Categories**:
   - `⚛️ Vector Field Theory & Physics` (Core VFT, 7 planes, harmonic tensor, 2c boundary)
   - `🧭 Actualism & Consciousness` (252 states of being, soul/belief states, AE-C translation)
   - `🏛️ Hegemonic Kanon & Audits` (WWSUTRU, Australian & American Kanon, Hegemony Attractor)
   - `📈 Value Physics & Econophysics` (Thermodynamic state space, empirical pricing audits, logistics)
   - `🤖 Autonomous Bots & Social Agents` (Bluesky Aletheia Bot, Trinary Synthesis, Scribe)
   - `🌌 Interactive Visualizers & 3D` (Spherical Polytrope, Hegemony Triangle, Basileia sim, 12Axes)
   - `📖 Ontology & Semantic Dictionaries` (QQCI dictionary, Reality Classification, AEC primitives)
   - `🛠️ Desktop & Workspace Tools` (Peek Explorer, Chat Context, Auto Scribe, LaTeX Exporter)
   - `🗺️ Navigation & Protocols` (Repo Master, Topic Maps, System Protocols, Master Indexes)
3. Extracts rich metadata: title, relative web path, file size, extension, brief summary/excerpt, and category tags.
4. Outputs:
   - `index_data.json` (Structured JSON consumed by the frontend)
   - `Master_Index.md` (Updated markdown documentation index)

### B. Landscape Mode (Adapted from `peek_explorer` for Topics & Categories)
Add a seamless mode toggle in the header: `[ 🗺️ Landscape Map Mode ]` / `[ ☰ Tree & Search View ]`.

When in **`🗺️ Landscape Mode`**:
1. **2D Pannable & Zoomable Canvas (`.map-world`)**:
   - Subtle infinite blueprint/grid background.
   - Smooth mouse-drag panning, wheel zoom, and pinch support.
2. **Category Rooms / Islands (`.map-room`)**:
   - Instead of ordinary folder boxes, each room represents a **Thematic Topic / Category**.
   - Positioned in a clean, collision-free radial layout around a central **Core Nexus Room** (`🌌 VFT Unified Nexus`).
   - Each Room features:
     - Header with Topic Icon, Title, File Count, and category badge.
     - Action buttons: `⤢ Focus/Zoom`, `☷ Toggle List/Grid`.
     - Subcategory badges / doorways (`📁 Subtopic`).
     - Interactive File Cards with file type badges (`📄 MD`, `🌐 HTML View`, `🐍 Python`, `📊 Data`), title, and quick open link.
3. **SVG Bridges (`.map-bridges`)**:
   - Stylized map walkways linking the central hub to each category room, and linking conceptually adjacent topics (e.g. *Theory & Physics* ──bridge──> *Actualism* ──bridge──> *Ontology* ──bridge──> *Kanon Audits* ──bridge──> *Value Physics*).
4. **Two-Rectangle Edge Lens (from Peek Explorer)**:
   - An inner normal viewport frame.
   - When the user zooms in or pans away, any off-screen Category Rooms project onto the perimeter margin as clickable indicator badges.
   - Clicking any edge proxy badge smoothly flies the camera to that category!
5. **Map HUD Toolbar**:
   - `🗺️ World Overview` (pulls back camera to see all 9 topic islands)
   - `🔍 Zoom In` / `Zoom Out` / Zoom Level readout
   - `⊞ Tidy Layout` (smoothly arranges rooms without overlapping)
   - `🖼️ Edge Lens: ON/OFF`
   - `☷ Indoor: Grid/List` toggle
6. **Live Search Integration**:
   - Typing in the global search bar highlights matching rooms and filters files inside every room in real time.

---

## 3. Step-by-Step Implementation Steps

1. **Create Indexing Script**:
   - Implement `E:\Vector Field Theory\VFT Docs\_AI files and chat logs\generate_master_index.py`.
   - Run the script to generate comprehensive `index_data.json` covering all 9 topics across workspaces.
2. **Update Master Index Web App**:
   - Update `E:\Vector Field Theory\VFT Docs\Master_Index.html` (and mirror to `_VFT MD\System\Master_Index.html`).
   - Add the Landscape Mode canvas, SVG bridges, Category Rooms, Two-Rectangle Edge Lens, HUD controls, and responsive styling.
3. **Verify and Test**:
   - Test serving via `http://localhost:8000/Master_Index.html`.
   - Verify panning, zooming, Edge Lens proxies, topic room filtering, search, and file opening.
4. **Log & Documentation**:
   - Document the new architecture and usage in `plans/task.md` and walkthrough.
