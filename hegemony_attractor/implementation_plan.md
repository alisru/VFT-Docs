# Implementation Plan - The Psochic Hegemony Attractor Engine (v38 - Cumulative Zero-Omission Plan)

This document contains the complete, unredacted, cumulative technical implementation plan for **[hegemony_attractor_map.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/hegemony_attractor/hegemony_attractor_map.html)**. Every single feature, physics parameter, code snippet, and verification step from all previous versions is preserved in full detail.

---

## 🏛️ Section 1: Pristine Base Attractors & Transient Landscape Events

1. **Immutable Base Biomes**:
   - The 4 core attractors (Good {Truth}, The Bad Lie, Good Lie, The Bad {Truth}) maintain constant fixed mass ($3.0$) and positions $(u, \psi)$.
2. **Transient Event Nodes**:
   - **🌱 Trigger Food Bloom**: Spawns temporary transient Bloom nodes on the field and fills cell energy pockets without altering base biome masses.
   - **🌊 Flood Field Actions**: Spawns temporary transient Flood nodes in target biomes without mutating the fixed landscape potential anchors.

---

## 🎛️ Section 2: All 7 Physics Sliders & Ecosystem Controls

All 7 real-time calibration sliders are permanently preserved in the Physics Controls panel:

1. **Attractor Biome Mass / Field Strength** ($0.5\text{x} - 6.0\text{x}$)
2. **Food Gradient Thruster Acceleration** ($0.2\text{x} - 4.0\text{x}$)
3. **Like-Pulls-Like Dimensional Gravity** ($0.1\text{x} - 3.0\text{x}$)
4. **Membrane Elasticity & Wobble Stiffness** ($0.2\text{x} - 3.0\text{x}$)
5. **Field Velocity Drag / Resistance** ($0.80 - 0.99$)
6. **Ambient Biome Food Yield Rate** ($0.2\text{x} - 3.0\text{x}$)
7. **Metabolic Fuel Conversion Efficiency** ($0.2\text{x} - 3.0\text{x}$)

---

## 🦠 Section 3: Full Verbose 7-Card Organism Inspector

Every organism selected on the canvas displays 7 verbose telemetry cards:

1. **Card 1: Cytoplasm Storage & Mass Inertia**: Stored Good, Bad, Truth, Lie, total energy, and mass inertia calculation.
2. **Card 2: Reaction Propulsion Thruster Engine**: Firing state, force vector, and exhaust particle type.
3. **Card 3: 4 Internal Micro-Hegemony Cores**: Air, Fire, Water, Earth core health and repair status.
4. **Card 4: Climate Identity & Dynamic Need AI**: 4-Plane Climate Identity badge (Air, Fire, Water, Earth), current target need, and climate toxicity status.
5. **Card 5: Sampled Field Volume**: Local field potential concentrations directly under the membrane.
6. **Card 6: 6 Radial Axes Decomposition**: Real-time breakdown across all 6 radial vectors ($0.0 - 2.0$).
7. **Card 7: Membrane Vitality & Log**: Health bar ($0 - 100\text{ HP}$) and scrollable event log.

---

## 🚀 Section 4: Dual-Fuel Reaction Thruster Engine

Organisms of all climate identities can burn EITHER **Truth** or **Lie** fuel for reaction propulsion.

### Code Implementation Detail:
```javascript
let fuelToBurn = null;
if (cell.pocket.truth > 0 && cell.pocket.lie > 0) {
    // Burn higher concentration fuel
    fuelToBurn = cell.pocket.truth >= cell.pocket.lie ? 'truth' : 'lie';
} else if (cell.pocket.truth > 0) {
    fuelToBurn = 'truth';
} else if (cell.pocket.lie > 0) {
    fuelToBurn = 'lie';
}

if (fuelToBurn === 'truth') {
    const fuelBurn = Math.min(cell.pocket.truth, 3.5 * delta);
    cell.pocket.truth = Math.max(0, cell.pocket.truth - fuelBurn);
    cell.vx += Math.cos(foodAngle) * 0.6 * thrusterForceScale * massInertia;
    cell.vy += Math.sin(foodAngle) * 0.6 * thrusterForceScale * massInertia;
    spawnThrusterParticle(cell.px, cell.py, -Math.cos(foodAngle), -Math.sin(foodAngle), 'truth');
} else if (fuelToBurn === 'lie') {
    const fuelBurn = Math.min(cell.pocket.lie, 3.5 * delta);
    cell.pocket.lie = Math.max(0, cell.pocket.lie - fuelBurn);
    cell.vx += Math.cos(foodAngle) * 0.6 * thrusterForceScale * massInertia;
    cell.vy += Math.sin(foodAngle) * 0.6 * thrusterForceScale * massInertia;
    spawnThrusterParticle(cell.px, cell.py, -Math.cos(foodAngle), -Math.sin(foodAngle), 'lie');
}
```

---

## 🔄 Section 5: 4-Phase Psochic Migration Lifecycle & Cytoplasm Coordinate Coupling

An organism's position and climate trajectory across the 4 planes are dynamically coupled to its internal cytoplasm composition ($E_{\text{good}}, E_{\text{bad}}, E_{\text{truth}}, E_{\text{lie}}$).

```
[ Phase 1: Air / Greater Good (+u, +ψ) ]
    │  • Absorbing/storing Lie energy generates repulsion from pure GG
    ▼
[ Phase 2: Water / Lesser Good (+u, -ψ) ]
    │  • Metabolizing Lie energy generates internal Bad energy (-u)
    ▼
[ Phase 3: Fire / Greater Evil (-u, +ψ / -ψ) ]
    │  • Repelled by Truth, reliance on Lies sends position further into GE
    ▼
[ Phase 4: Lesser Evil & Fire Body Decay ]
    └─► Organism is starved of Truth fuel (E_truth = 0.0 U).
        Its Fire Body slowly decays in HP (-3.0 HP/s) unless it migrates
        back toward Truth gradients to repair its Air Core!
```

### 🧮 Mathematical Dynamic Coordinate Coupling
\[
u_{\text{cell}} = \frac{E_{\text{good}} - E_{\text{bad}}}{E_{\text{total}} + 1.0} \times 2.0
\]
\[
\psi_{\text{cell}} = \frac{E_{\text{truth}} - E_{\text{lie}}}{E_{\text{total}} + 1.0} \times 2.0
\]

---

## ⚠️ Section 6: Contradiction Flags & Compatibility Notes

> [!WARNING]
> **Contradiction Flag 1: Dynamic Coordinate Drift vs Fixed Canvas Spawns**
> *Previous Logic*: Organisms remained anchored near their physical spawn coordinates $(p_x, p_y)$ and only moved via thruster vectors $(v_x, v_y)$.
> *New Logic*: Physical canvas coordinates $(p_x, p_y)$ are smoothly biased by internal cytoplasm energy $(u_{\text{cell}}, \psi_{\text{cell}})$, meaning internal metabolic state directly shifts the cell across climate quadrants.
> *Resolution*: We preserve velocity vector thrusters $(v_x, v_y)$ as physical momentum, while applying cytoplasm drift as a continuous metabolic bias force $\mathbf{F}_{\text{drift}} = k_{\text{drift}} \cdot (\mathbf{x}_{\text{target}} - \mathbf{x}_{\text{current}})$.

---

## 🛠️ Section 7: Proposed File Modifications

### [MODIFY] [hegemony_attractor_map.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/hegemony_attractor/hegemony_attractor_map.html)

- **Update Thruster Logic**: Implement dual-fuel execution (Truth or Lie).
- **Update Inspector Card 2**: Display live status indicating whether the cell is currently burning Truth Fuel, Lie Fuel, or out of all fuel.
- **Preserve All 7 Physics Sliders**: Attractor Mass, Thruster Force, Home Gravity, Elasticity, Drag, Yield Rate, Metabolic Efficiency.
- **Preserve All 7 Telemetry Cards**: 1. Cytoplasm & Drag, 2. Thrusters, 3. Cores, 4. Climate & Need, 5. Volume, 6. 6 Axes, 7. Vitality.
- **Add Psochic Migration Drift**: Compute $(u_{\text{cell}}, \psi_{\text{cell}})$ per frame and apply metabolic drift force.

---

## 🧪 Section 8: Verification Plan

### Manual Verification
1. Open [hegemony_attractor_map.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/hegemony_attractor/hegemony_attractor_map.html) in a web browser.
2. Inject Lie field nodes near an Air cell using the top mode bar.
3. Inspect the organism to verify Card 2 shows dynamic dual-fuel thruster status.
4. Observe the cell absorb Lie energy, drift southward into Water ($+u, -\psi$), digest Lie into Bad energy, and drift westward into Fire/Earth ($-u$).
