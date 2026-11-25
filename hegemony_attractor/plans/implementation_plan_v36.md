# Implementation Plan - Dual-Fuel Reaction Thrusters (v36 Historical Archive)

We are proposing an update to **[hegemony_attractor_map.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/hegemony_attractor/hegemony_attractor_map.html)** to allow organisms of ALL climate identities to utilize EITHER **Truth** or **Lie** fuel for reaction propulsion.

---

## 🏛️ Rationale & Mechanism

Currently, thruster firing logic is locked by climate identity (Air/Earth burn only Truth; Fire/Water burn only Lie). If an Air organism possesses stored Lie fuel in its cytoplasm pocket, it cannot burn it.

### Proposed Changes:
1. **Dual-Fuel Thruster Engine**:
   - Organisms will burn **EITHER** `truth` fuel OR `lie` fuel for propulsion.
   - If an organism runs out of Truth fuel but possesses Lie fuel, it automatically switches thrusters to burn Lie fuel (and vice-versa)!
2. **Visual Exhaust Particles**:
   - Firing Truth fuel ejects Cyan/Blue particles ($+\psi$).
   - Firing Lie fuel ejects Amber/Gold particles ($-\psi$).
3. **Flexible Metabolism**:
   - Cells can process Good food into Truth fuel AND Bad food into Lie fuel, storing both fuel reserves in their cytoplasm pockets.

---

## 🛠️ Proposed File Modifications

### [MODIFY] [hegemony_attractor_map.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/hegemony_attractor/hegemony_attractor_map.html)

- **Update Thruster Logic**:
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
  ```
- **Update Inspector Card 2**: Display live status indicating whether the cell is currently burning Truth Fuel, Lie Fuel, or out of all fuel.

---

## 🧪 Verification Plan

### Manual Verification
1. Open [hegemony_attractor_map.html](file:///e:/Vector%20Field%20Theory/VFT%20Docs/hegemony_attractor/hegemony_attractor_map.html) in a web browser.
2. Inject both Truth and Lie field nodes using the mode bar.
3. Inspect an organism to verify Card 2 shows it dynamically burning whichever fuel is available.
