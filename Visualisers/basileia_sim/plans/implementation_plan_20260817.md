# Basileia of Understanding - 2D Simulation Implementation Plan

## Overview
An interactive 2D top-down simulation built in HTML5/Canvas exploring "The Psochic Basileia (Ruling Kingdom of the Mind)".
The player navigates an expansive conceptual world starting trapped inside the fortress of orthodox thought (Temple of the Mind). As the player explores and gains "Subjective Understanding", their line of sight (LoS) expands and dynamically pierces dogmatic walls, illuminating hidden pathways, bridging chasms, and transforming the landscape.

## Architectural Components

### 1. Canvas World & Geometry Engine (`index.html`)
- **Procedural & Cartographic Canvas Renderer**: High-fidelity map matching the provided classical Basileia parchment illustration:
  - **Center**: *Orthodox Basileia (Temple of the Mind)* - Concentric fortified stone walls, inner courtyard, cathedral sanctum, barricades, garden arcades.
  - **Top-Left**: *Phronetic Forest / Productive Realm (+υ, +ψ)* - Verdant shrines, winding rivers, mossy ancient ruins, overgrown bridges.
  - **Top-Right**: *Solar Pyre / High-Will Zeal (+ψ, -υ)* - Stepped ziggurat, radiant energy rings, heat fissures, crimson sand dunes.
  - **Bottom-Right**: *Caldera of Chaos / Smouldering Ruin (-υ, -ψ)* - Obsidian colosseum, dark smoke plumes, volcanic rifts, deep chasms.
  - **Bottom-Left**: *Nomadic Frontier / Praxis (+υ, -ψ)* - Winding streams, savannah trails, circular earthworks, tribal palisade camp.
- **Physics & Collision Boundaries**: Line segments representing walls, concentric battlements, gates, and terrain obstacles.

### 2. Dynamic Line-of-Sight & Raycasting (Shadow-Casting Visibility Polygon)
- 2D raycasting from player position to wall vertices (+/- epsilon offset).
- **Comprehension Piercing Algorithm**:
  - Walls have an occlusion opacity $O \in [0, 1]$ inversely proportional to the player's quadrant comprehension $C_q$.
  - When $C_q = 0$, walls are completely opaque (full shadow casting).
  - As $C_q$ increases, rays pierce through walls, rendering them translucent and illuminating the terrain beyond.
- **Fog of War & Memory Mesh**:
  - Unexplored regions: shrouded in mist/fog.
  - Explored regions: remembered in subtle sepia/ink linework.
  - Active Line of Sight: brightly illuminated with dynamic radiant aura.

### 3. Subjective Understanding & Progression System
- **Exploration Aura**: Moving through zones slowly accumulates regional comprehension.
- **Insight Shrines & Conceptual Nodes**: Interactive loci with philosophical reflections (e.g. *The Paradox of Dogma*, *The Biophilic Flow*, *The Furnace of Ambition*, *The Abyss of Instinct*, *The Grounded Flame*). Interacting grants massive understanding surges and unlocks hidden pathways.
- **Quadrant Resonance**: Real-time HUD showing $(υ, ψ)$ coordinates, quadrant mastery percentages, and total Basileia illumination.

### 4. Player Controls & Polish
- Smooth 2D movement via Keyboard (`WASD` / Arrows), Mouse click-to-move, and mobile on-screen virtual joystick.
- Smooth camera tracking with zoom controls (mouse wheel / UI buttons).
- Generative ambient audio using Web Audio API (soothing resonant drone that harmonically shifts per quadrant).
- Intuitive overlay controls: minimap toggle, illumination mode switch, reset, and insight journal.
