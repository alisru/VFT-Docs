# Master Design Document - The Psochic Hegemony Attractor Engine (v40 - Additive Master Revision)

This document is the **Permanent, Cumulative Master Design Document** for the Psochic Hegemony Attractor Map visualizer. It is strictly cumulative: no sections, equations, rules, or controls will ever be removed or overwritten.

---

## 🏛️ 1. Architecture & Base Landscape Principles

1. **Immutable Base Biomes**:
   - The 4 core quadrant attractors maintain constant fixed mass ($3.0$) and positions $(u, \psi)$:
     - **Good {Truth} Biome (Air)**: $(+1.0, +1.0)$, Greek: $\alpha\gamma\acute{\alpha}\pi\eta$, Color: Green/Sky-Blue.
     - **The Bad Lie Biome (Fire)**: $(-1.0, +1.0)$, Greek: $\sigma o\phi\iota\sigma\tau\epsilon\acute{\iota}\alpha$, Color: Red/Amber.
     - **Good Lie Biome (Water)**: $(+1.0, -1.0)$, Greek: $\alpha\tau\alpha\rho\alpha\xi\acute{\iota}\alpha$, Color: Teal/Cyan.
     - **The Bad {Truth} Biome (Earth)**: $(-1.0, -1.0)$, Greek: $\tau\upsilon\rho\alpha\nu\nu\acute{\iota}\varsigma$, Color: Rose/Magenta.

2. **Transient Landscape Events**:
   - **🌱 Trigger Food Bloom**: Spawns temporary transient Bloom patches with finite food reserves ($100\text{U}$) without altering base biome masses.
   - **⛈️ Trigger Vector Storm**: Injects high-frequency vector field turbulence to dislodge static equilibrium.
   - **🌊 Global Field Flooding Actions**: Spawns temporary transient Flood nodes in Air, Fire, Water, or Earth quadrants.

---

## 🎛️ 2. Complete Physics Controls Suite (7 Sliders)

All 7 real-time calibration sliders are permanently preserved in the Physics Controls panel:

1. **Attractor Biome Mass / Field Strength** ($0.5\text{x} - 6.0\text{x}$): Scales global gravitational potential of attractors.
2. **Food Gradient Thruster Acceleration** ($0.2\text{x} - 4.0\text{x}$): Controls cell acceleration along $+\nabla D_{\text{diet}}$.
3. **Like-Pulls-Like Dimensional Gravity** ($0.1\text{x} - 3.0\text{x}$): Controls return pull of ejected particles to home biomes.
4. **Membrane Elasticity & Wobble Stiffness** ($0.2\text{x} - 3.0\text{x}$): Controls soft-body cell deformation and spring tension.
5. **Field Velocity Drag / Resistance** ($0.80 - 0.99$): Controls fluid medium friction acting on cell velocity.
6. **Ambient Biome Food Yield Rate** ($0.2\text{x} - 3.0\text{x}$): Controls continuous food regeneration in biomes.
7. **Metabolic Fuel Conversion Efficiency** ($0.2\text{x} - 3.0\text{x}$): Controls speed of digesting diet food into thruster fuel.

---

## 🧪 3. Altruistic vs Selfish Metabolic Extraction Mechanics (NEW ADDITION)

1. **Altruistic Extraction (Good Core)**:
   - Altruistic actors use Good energy ($E_{\text{good}}$) to **extract Truth from Lies**:
     \[
     E_{\text{lie}} \xrightarrow{E_{\text{good}}} E_{\text{truth}}
     \]
   - Converts deceptive/manipulative field inputs into verifiable Truth fuel.

2. **Selfish Extraction (Bad Core)**:
   - Selfish actors use Bad energy ($E_{\text{bad}}$) to **extract Lies from Truth**:
     \[
     E_{\text{truth}} \xrightarrow{E_{\text{bad}}} E_{\text{lie}}
     \]
   - Distorts verified Truth inputs into deceptive Lie fuel for self-serving propulsion.

---

## ⚖️ 4. Dynamic Visual Radius & Physical Mass Scaling per Held Resources (NEW ADDITION)

Cells dynamically expand visually and physically based on total cytoplasm energy ($E_{\text{total}} = E_{\text{good}} + E_{\text{bad}} + E_{\text{truth}} + E_{\text{lie}}$):

1. **Visual Canvas Radius ($R$)**:
   \[
   R = 16.0 + \sqrt{E_{\text{total}}} \times 2.2
   \]
   - A cell holding $0\text{U}$ energy has a lean visual radius of $16\text{px}$.
   - A cell holding $100\text{U}$ energy visually swells to $38\text{px}$.

2. **Physical Inertial Mass ($m$) & Medium Drag ($\mu_{\text{drag}}$)**:
   \[
   m = 1.0 + \frac{E_{\text{total}}}{20.0}
   \]
   \[
   \text{Acceleration} = \mathbf{F}_{\text{thrust}} \times \frac{1.0}{m}
   \]
   - Resource-heavy cells visually loom large and move with heavy sluggish momentum.
   - Resource-starved cells are visually tiny and sprint rapidly across the field.

---

## 🦠 5. Full Verbose 7-Card Organism Inspector

Selecting any cell on the canvas displays 7 verbose telemetry cards:

1. **Card 1: Cytoplasm Storage & Mass Inertia**: Displays stored Good, Bad, Truth, Lie, total energy, cell radius ($R = 16 + \sqrt{E_{\text{total}}} \times 2.2$), mass ($m = 1.0 + \frac{E_{\text{total}}}{20.0}$), and drag inertia.
2. **Card 2: Reaction Propulsion Thruster Engine**: Firing state, force vector ($1.5\text{x} \nabla F / m$), and active exhaust particle color (Cyan/Blue for Truth, Amber/Gold for Lie).
3. **Card 3: 4 Internal Micro-Hegemony Cores**: Health and repair state of Air, Fire, Water, and Earth cores.
4. **Card 4: Climate Identity & Dynamic Need AI**: 4-Plane Climate Identity badge (Air, Fire, Water, Earth), current target need, and climate toxicity status.
5. **Card 5: Sampled Field Volume**: Local field potential concentrations directly under the cell membrane.
6. **Card 6: 6 Radial Axes Decomposition**: Real-time breakdown across all 6 radial vectors ($0.0 - 2.0$).
7. **Card 7: Membrane Vitality & Log**: Health bar ($0 - 100\text{ HP}$) and scrollable event log.

---

## 🍖 6. Resource Mechanics, Depletion & Starvation Physics

1. **Depletable Local Food Pools**: Attractors have finite food pools ($F_{\text{local}}$ shown e.g. `(150U)`). Grazing directly depletes node food reserves.
2. **Basal Metabolic Burn**: Cells burn $1.0\text{U/s}$ of stored cytoplasm energy for basic core maintenance.
3. **Absolute Zero Fuel Exhaustion ($0.0\text{U}$)**: Thrusters shut off completely when fuel reaches zero (`🔴 FUEL EXHAUSTED (0.0 U)`).
4. **Starvation Damage & Death**: At $0.0\text{U}$ total energy, cores suffer starvation decay ($-6\text{ HP/s}$). At $0\text{ HP}$, the cell dies and dissolves.

---

## 🧠 7. Dynamic Need-Based Seeking & Mass Drag Physics

1. **Dynamic Need-Based Seeking AI**: Organisms continuously evaluate their internal resource deficits (Fuel vs Diet Food vs Home Preference Food) and navigate toward the gradient of highest urgency.
2. **Opposite Field Repulsion Physics**: Good cells are repulsed by Bad potential nodes ($+\nabla \Phi_{\text{bad}}$ repulsion); Bad cells are repulsed by Good potential nodes ($+\nabla \Phi_{\text{good}}$ repulsion).

---

## 🚀 8. Universal Dual-Fuel Reaction Thruster Engine

Organisms of all climate identities can burn EITHER **Truth** fuel OR **Lie** fuel for reaction propulsion.

### Thruster Logic:
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

## 🔄 9. The 4-Phase Psochic Migration Lifecycle & Cytoplasm Coordinate Coupling

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

### Detailed 4-Point Migration Rules:
1. **Cytoplasm Coordinate Drift**: Shifts $(u_{\text{cell}}, \psi_{\text{cell}})$ dynamically based on internal cytoplasm energy ratios.
2. **Lie Repulsion from Greater Good (GG)**: Storing Lie energy ($E_{\text{lie}}$) creates a southward repulsive force ($-\psi$) pushing Air organisms out of Air ($+u, +\psi$) into Water ($+u, -\psi$).
3. **Internal Bad Energy Generation**: Digesting Lie energy converts cytoplasm into Bad energy ($E_{\text{bad}}$), pushing the cell westward ($-u$) into Fire/Earth.
4. **Truth Starvation & Fire Body Decay**: When a cell in the Fire/Earth domain reaches $0.0\text{U}$ Truth fuel, it cannot repair its Air Core, causing its Fire body to slowly starve ($-3.0\text{ HP/s}$) until it finds a Truth source or dies.

---

## 🧪 10. Verification Plan

### Manual Verification
1. Open [hegemony_attractor_map.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/hegemony_attractor/hegemony_attractor_map.html) in any modern web browser.
2. Observe Altruistic (Good) organisms extract Truth from Lies, and Selfish (Bad) organisms extract Lies from Truth.
3. Feed an organism with abundant food and observe its visual canvas radius ($R$) swell dynamically from $16\text{px}$ up to $38\text{px}+$, accompanied by sluggish physical mass inertia.
