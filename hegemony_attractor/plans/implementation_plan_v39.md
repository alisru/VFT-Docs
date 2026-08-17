# Implementation Plan - Actor Micro-Hegemony Envelopes (7-Parameter Growth System)

This plan upgrades the standard plotted points in hegemony_map.html to **Actors** (dynamic micro-hegemonies). Each actor represents a being or concept's sphere of understanding, defined by 7 parameters.

---

## Technical Specifications

### 1. State & Telemetry Upgrade
We will introduce 7 parameters to the actor points:
* **Confusion (`confusion`)**: Ranging from `0` to `100` (default: `30`). This represents unprocessed information and behaves as a gravitational pull towards the origin `(0,0)`:
  $$v_{\text{active}} = v_{\text{anchor}} \times (1 - \frac{\text{confusion}}{100})$$
  $$\psi_{\text{active}} = \psi_{\text{anchor}} \times (1 - \frac{\text{confusion}}{100})$$
  * When placing or dragging an actor, we store and update its anchor coordinates ($v_{\text{anchor}}, \psi_{\text{anchor}}$).
  * Rendered canvas positions and projections are calculated using the active coordinates ($v_{\text{active}}, \psi_{\text{active}}$).

* **6 Growth Parameters (Hexagonal Envelope Spokes)**: Ranging from `0` to `100` (default: `30`). A parameter value of $100 \approx 0.6$ coordinate units.
  1. **Preference 2 (Bad Preference, `pref2`)**: straight Right ($0^\circ$, vector: $[-1, 0]$)
  2. **Greater Evil (`greaterEvil`)**: Top-Right ($45^\circ$, vector: $[-1/\sqrt{2}, 1/\sqrt{2}]$)
  3. **Greater Good (`greaterGood`)**: Top-Left ($135^\circ$, vector: $[1/\sqrt{2}, 1/\sqrt{2}]$)
  4. **Preference 1 (Good Preference, `pref1`)**: straight Left ($180^\circ$, vector: $[1, 0]$)
  5. **Lesser Good (`lesserGood`)**: Bottom-Left ($225^\circ$, vector: $[1/\sqrt{2}, -1/\sqrt{2}]$)
  6. **Lesser Evil (`lesserEvil`)**: Bottom-Right ($315^\circ$, vector: $[-1/\sqrt{2}, -1/\sqrt{2}]$)

---

## Proposed Changes

### hegemony_attractor/hegemony_map.html

#### [MODIFY] hegemony_map.html

1. **State Upgrades**:
   * Change standard points initialization to contain `baseV`, `basePsi`, `v`, `psi`, and the 7 parameters.
   * Update click-to-place to initialize points as actors with:
     `baseV: v`, `basePsi: psi`, `confusion: 30`, and `30` for the 6 growth parameters.
   * Adjust dragging handlers (`handleCanvasMouseMove`) to calculate new base coordinate anchors under the confusion pull:
     $$v_{\text{anchor}} = \frac{v_{\text{mouse}}}{1 - \frac{\text{confusion}}{100}}$$

2. **Heptagonal/Hexagonal Shading on Canvas**:
   * In the `points.forEach` drawing loop:
     * Compute active coordinates $(v_c, \psi_c)$ using the confusion pull.
     * Calculate 6 vertex coordinate offsets in VFT space:
       $$v_i = v_c + \text{reach}_i \times u_{x, i}$$
       $$\psi_i = \psi_c + \text{reach}_i \times u_{y, i}$$
     * Convert offsets to pixel space using `toPixel(v_i, \psi_i)`.
     * Render the closed hexagon: fill with `combineColorAlpha(zone.color, 0.08)` and stroke boundary.
     * For the selected actor, render vertex indicators and abbreviated value overlays (e.g., `GE: 30`).

3. **Sidebar Editor Controls**:
   * Insert a panel containing 7 range inputs under the label/context settings.
   * Sync slider values and labels in real-time. Mutating any slider will update the active point object and redraw the canvas.

---

## Verification Plan

### Manual Verification
* **Confusion Pull Test**: Place an actor at $v=1, \psi=1$. Increase confusion to $100\%$ and verify the actor shifts to $(0,0)$. Decreasing confusion to $0\%$ restores it to its anchor.
* **Morality Alignment Test**: Drag the "Lesser Evil" slider and confirm that the Bottom-Right vertex ($315^\circ$) grows. Drag "Greater Evil" and verify the Top-Right vertex ($45^\circ$) grows.
* **Dragging Persistence**: Drag the actor on canvas and verify it stays in place when releasing mouse, updating coordinate readouts correctly.
