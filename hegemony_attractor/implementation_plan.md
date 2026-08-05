# Implementation Plan - Hegemony Attractor Shader & Zoom Alignment (v39)

This plan aligns the background proximity shader with the exact mathematical model used for cursor and point readout parameter projections. 

---

## 🏛️ Section 1: Rationale & Mechanism

Currently, the background shader splits its proximity contribution using a custom, sharp hemispheric cutoff line perpendicular to each subdivision arm. This mismatch creates triangular "shards" of color and uneven cancellation wedges near the vertical midline.

We will refactor the shader to use the exact `[dir, mag]` coordinate projection parameters calculated for the user readout.

1. **Axes Magnitude Decay (`mag`)**:
   - Proximity decay will use a constant width (`WIDTH = 0.7`) in coordinate units instead of dividing by `len`. This keeps the arms' glow sizes uniform and prevents overlapping cancellation across the entire canvas.
2. **Transition Arm Projection (`dir`)**:
   - For all transition axes (edges and the 8 subdivision arms), we calculate the projection parameter `t = dir / 100` (clamped to `[0, 1]`).
   - If an axis transitions from Red at the start to Green at the end, the magnitude is divided as:
     - `gSum += (mag / 100) * t`
     - `rSum += (mag / 100) * (1 - t)`
   - This aligns the color contribution smoothly along the length of the axis, matching the cursor coordinates.

---

## 🛠️ Section 2: Proposed File Modifications

### [MODIFY] [hegemony_map.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/hegemony_attractor/hegemony_map.html)

- **Update `getProx` to return both `dir` and `mag`**:
  ```javascript
  function getProx(u, psi, x1, y1, x2, y2) {
    const dx = x2 - x1, dy = y2 - y1;
    const len = Math.hypot(dx, dy);
    if (len === 0) return { dir: 0, mag: 0 };
    const ux = dx / len, uy = dy / len;
    const along = (u - x1) * ux + (psi - y1) * uy;
    const alongC = Math.max(0, Math.min(len, along));
    const projU = x1 + ux * alongC;
    const projPsi = y1 + uy * alongC;
    const dist = Math.hypot(u - projU, psi - projPsi);
    const dir = (along / len) * 100;
    const mag = Math.max(0, 100 * (1 - dist / 0.7)); // Fixed width = 0.7
    return { dir, mag };
  }
  ```
- **Update Shader Loop**:
  - Remove all hard `if (uPP >= 0)` condition checks for the 8 arms.
  - Map static axes directly:
    - Good/Truth/LHS: `gSum += mag / 100`
    - Bad/Lies/RHS: `rSum += mag / 100`
  - Map transition axes using the `t` (directional percentage) interpolation.

---

## 🧪 Section 3: Verification Plan

### Manual Verification
1. Open [hegemony_map.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/hegemony_attractor/hegemony_map.html) in a web browser.
2. Confirm the background colors are smoothly blended.
3. Check that the meeting of the green/red regions along the vertical midline is clean, vertical, and free of jagged overlapping shards.
4. Verify the zoom slider and mouse-scroll zoom still function properly.
