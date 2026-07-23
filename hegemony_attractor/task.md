# Task Checklist - Hegemony Attractor Map Visualizer

- [x] **Phase 1: Project Setup & Structure**
  - [x] Create project directory `hegemony_attractor`
  - [x] Write `implementation_plan.md`
  - [x] Initialize `hegemony_attractor_map.html` shell with Tailwind CSS & Google Fonts

- [x] **Phase 2: Core Physics Engine & Topographical Potential Field**
  - [x] Implement low-res Canvas ($360\times360$) with retro pixel scaling (`image-rendering: pixelated`)
  - [x] Implement VFT coordinate transform mapping ($(u, \psi) \leftrightarrow (x, y)$) with $+u$ on left
  - [x] Implement compounding potential field equation $V(u, \psi)$ for like-type attractors
  - [x] Implement vector field gradient physics $\vec{F}_{\text{slope}} = -\nabla V$
  - [x] Implement particle/actor kinetic dynamics and friction

- [x] **Phase 3: Pixelized Topographical Landscape & Togglable Layers**
  - [x] Render 8-bit elevation bands (color gradients) for mountains and basins
  - [x] Render vector flow field streamlets / arrows
  - [x] Render resource spectrum heatmap overlay
  - [x] Render fading actor trails

- [x] **Phase 4: Simulation Entities (Actors, Resources, Attractors)**
  - [x] Define the 4 cardinal types (Good {Truth}, Bad Lie, Good Lie, Bad {Truth})
  - [x] Build resource spawner for the 4 resource types
  - [x] Implement actor collection, spectrum shift, and moral trajectory updates
  - [x] Implement fixed and custom attractors with compounding fields

- [x] **Phase 5: Glassmorphic Dashboard & Data Integration**
  - [x] Import `../hegemony_db.js` (`window.hegemonyLovesExternal`)
  - [x] Create search & filter database table to add any of the 300+ items as attractors
  - [x] Implement Simulation Control Panel (Play, Pause, Reset, Sliders for Speed, Gravity, Spawn Rate)
  - [x] Implement Presets (Agape Ascension, Sophist Epidemic, Singularity Collapse, SON Equilibrium)
  - [x] Implement Actor Inspector with live spectrum breakdown and trajectory history

- [x] **Phase 6: Polish & Verification**
  - [x] Apply retro CRT scanline overlay and micro-animations
  - [x] Verify pixel art aesthetics and UI responsiveness
  - [x] Test all layer toggles and preset scenarios
