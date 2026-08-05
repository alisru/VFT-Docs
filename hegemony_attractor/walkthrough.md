# Walkthrough - Hegemony Attractor Shader & Zoom Alignment (v40)

We have successfully refined the Hegemony map visualizer with real-time blending controls, zoom alignment, lag-free caching, physical metric sorting, and the 8-arms constraint.

---

## 🚀 Key Improvements

### 🎛️ 1. Real-time Shader Blending & Focus Controls
- Exposes sliders in the sidebar for:
  - **Divisor**: Normalizes the axis sum. Lowering this increases color vibrancy.
  - **Exponent**: Changes contrast. Lowering this fills in the dim center gradient.
  - **Opacity**: Adjusts transparency of the background shader layer.
  - **Cancel Strength**: Adjusts color cancellation between green and red fields.
  - **Observer N**: Restricts color rendering and guide handle displays to only the $N$ nearest axes.

### 🔍 2. Lag-Free Zoom & Scroll Caching
- Increased maximum zoom factor from $200\%$ to $800\%$ for extreme coordinate inspection.
- Decoupled the shader calculation from screen dimensions. The shader now calculates at a fixed $300\times300$ resolution in coordinate space, and is drawn stretched using `drawImage`.
- Zooming and scrolling now require **zero pixel-by-pixel recalculation of the shader**, maintaining a locked 60 FPS.

### 🎯 3. Perfect Mouse-Pointer Tracking
- Added zoom-debiasing to `toCoord(px, py)` so that client clicks and mouse-hover coordinates align precisely with the visual grid elements at any zoom level.

### 🧠 4. Metric Physical Distance Sorting for Observer N
- Fixed sorting in the shader loop to sort by **actual physical distance (`dist`) ascending** rather than fanned proximity (`prox`). This prevents longer, further arms from squeezing out shorter, closer ones.
- Modified the canvas hovered projection handle and the sidebar list to only display/highlight the $N$ closest active axes (active ones bolded with `●`, inactive ones faded out with `○` and $20\%$ opacity).

### 📐 5. Constraint to the 8 Subdivision Arms
- Bypassed all central, diagonal, and edge axes from the shader field. The colors, canvas guides, and sidebar projections are now driven strictly by the 8 key subdivision arms:
  1. `Productive ← Potential` (PP)
  2. `Constructive ← Potential` (CP)
  3. `Anti-Potential → Reductive` (RA)
  4. `Anti-Potential → Regressive` (Reg)
  5. `Constructive ← Suppressive` (CS)
  6. `Suppressive → Regressive` (RS)
  7. `Productive ← Active` (PA)
  8. `Active → Reductive` (ReA)

### 🌌 6. Mind & Body Dualism Labels
- Re-labeled the canvas coordinates:
  - Horizontal Axis ($\upsilon$): **Morality (Mind / Benefit)**
  - Vertical Axis ($\psi$): **Will (Body / Action)**
