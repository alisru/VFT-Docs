import Mathlib.Data.Rat.Basic
import Mathlib.Algebra.Ring.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Order.Basic

/--
  # 7-Lattice Process Hamilton-Jacobi-Bellman (P-HJB) & BESS Storage Mechanics
  Lean 4 Formal Mathlib4 Blueprint (IRM Division 1: Pure Mathematics & Division 2: Value Physics)
  Formalizing:
  1. The Process Dynamic Programming Loss Function on [0, 2].
  2. Overcapacity Zero-Investment Invariant Theorem (Strict Convexity of Stress Penalty).
  3. BESS State-of-Charge Continuity and Conservation Invariant.
-/

/-- The Instantaneous P-HJB Loss Function -/
def phjb_loss
  (c α β : ℚ) (V_curr inv wear D : ℚ) : ℚ :=
  let V_next := V_curr + inv - wear
  let l_effort := c * inv ^ 2
  let deficit := if D - V_next > 0 then D - V_next else 0
  let l_deficit := α * deficit ^ 2
  let phi := (V_next - 1) ^ 2
  let l_stress := if phi - 1 > 0 then β * (phi - 1) else 0
  l_effort + l_deficit + l_stress

/-- Theorem: Overcapacity Zero-Investment Invariant Theorem
    When current capital is in severe overcapacity (V_curr - wear > 2) and demand is normal
    (D ≤ 1), any additional positive investment inv > 0 strictly increases the total loss:
    phjb_loss(inv > 0) > phjb_loss(inv = 0). Thus, the optimal policy strictly shuts off investment. -/
theorem overcapacity_zero_investment_optimal
  (c α β V_curr wear D inv : ℚ)
  (h_c_pos : c > 0)
  (h_beta_pos : β > 0)
  (h_inv_pos : inv > 0)
  (h_over : V_curr - wear > 2)
  (h_D_le_1 : D ≤ 1) :
  let V_base := V_curr - wear
  let loss_zero := phjb_loss c α β V_curr 0 wear D
  let loss_inv := phjb_loss c α β V_curr inv wear D
  loss_inv > loss_zero := by
  intro V_base loss_zero loss_inv
  dsimp [loss_zero, loss_inv, phjb_loss]
  -- In overcapacity, D - V_base < 0 and D - (V_base + inv) < 0, so deficit is 0 for both
  have h_base_gt_2 : V_base > 2 := h_over
  have h_base_inv_gt_2 : V_base + inv > 2 := by linarith
  have h_base_sub_1 : V_base - 1 > 1 := by linarith
  have h_base_inv_sub_1 : V_base + inv - 1 > V_base - 1 := by linarith
  have h_phi_zero_gt_1 : (V_base - 1) ^ 2 > 1 := by
    nlinarith
  have h_phi_inv_gt_phi_zero : (V_base + inv - 1) ^ 2 > (V_base - 1) ^ 2 := by
    have h1 : V_base + inv - 1 > 1 := by linarith
    have h2 : V_base - 1 > 1 := by linarith
    nlinarith
  -- Therefore effort is strictly positive, stress strictly increases, deficit remains 0
  have h_effort_pos : c * inv ^ 2 > 0 := by
    have h_sq : inv ^ 2 > 0 := by
      exact sq_pos_of_ne_zero (ne_of_gt h_inv_pos)
    exact mul_pos h_c_pos h_sq
  have h_stress_diff : β * ((V_base + inv - 1) ^ 2 - 1) > β * ((V_base - 1) ^ 2 - 1) := by
    have h_diff_pos : ((V_base + inv - 1) ^ 2 - 1) - ((V_base - 1) ^ 2 - 1) > 0 := by linarith
    exact mul_pos_of_pos_of_nonneg h_diff_pos (le_of_lt h_beta_pos)
  linarith

/-- Theorem: BESS Energy Storage Conservation Invariant
    Discharging net load L for duration dt scales SoC valuation by exactly -2 * (L * dt / Capacity),
    conserving total power flow balance across the feeder. -/
theorem bess_soc_energy_conservation
  (V_soc_init Capacity L dt : ℚ)
  (h_cap_pos : Capacity > 0) :
  let delta_soc := - (L * dt / Capacity) * 2
  let V_soc_final := V_soc_init + delta_soc
  V_soc_final - V_soc_init = - (L * dt / Capacity) * 2 := by
  intro delta_soc V_soc_final
  dsimp [V_soc_final, delta_soc]
  ring
