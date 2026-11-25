import Mathlib.Data.Rat.Basic
import Mathlib.Algebra.Ring.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Order.Basic

/--
  # 7-Lattice Process Mean-Field Game (P-MFG) & Pastoral Soil Carbon Mechanics
  Lean 4 Formal Mathlib4 Blueprint (IRM Division 1: Pure Mathematics & Division 2: Value Physics)
  Formalizing:
  1. Discrete 7-Lattice Mean-Field Congestion Loss Function.
  2. P-MFG Overcapacity Investment Shutoff Invariant Theorem.
  3. Pastoral Soil Carbon Sequestration and Mass Conservation Invariant.
-/

/-- P-MFG Agent Loss Function with Common-Pool Scarcity Tax -/
def pmfg_agent_loss
  (c α β γ : ℚ) (V_k inv wear D lambda_shared : ℚ) : ℚ :=
  let V_next := V_k + inv - wear
  let l_effort := c * inv ^ 2
  let deficit := if D - V_next > 0 then D - V_next else 0
  let l_deficit := α * deficit ^ 2
  let phi := (V_next - 1) ^ 2
  let l_stress := if phi - 1 > 0 then β * (phi - 1) else 0
  let l_congestion := γ * lambda_shared * inv
  l_effort + l_deficit + l_stress + l_congestion

/-- Theorem: P-MFG Overcapacity Investment Shutoff Invariant Theorem
    When base capital is in overcapacity (V_k - wear > 2), demand is normal (D ≤ 1),
    and common-pool congestion tax is non-negative (λ_shared ≥ 0), any positive
    investment inv > 0 strictly increases the agent loss.
    Therefore, the best-response policy in overcapacity strictly shuts off investment. -/
theorem pmfg_overcapacity_shutoff_optimal
  (c α β γ V_k wear D lambda_shared inv : ℚ)
  (h_c_pos : c > 0)
  (h_beta_pos : β > 0)
  (h_gamma_nonneg : γ ≥ 0)
  (h_lam_nonneg : lambda_shared ≥ 0)
  (h_inv_pos : inv > 0)
  (h_over : V_k - wear > 2)
  (h_D_le_1 : D ≤ 1) :
  let loss_zero := pmfg_agent_loss c α β γ V_k 0 wear D lambda_shared
  let loss_inv := pmfg_agent_loss c α β γ V_k inv wear D lambda_shared
  loss_inv > loss_zero := by
  intro loss_zero loss_inv
  dsimp [loss_zero, loss_inv, pmfg_agent_loss]
  have h_base : V_k - wear > 2 := h_over
  have h_base_inv : V_k - wear + inv > 2 := by linarith
  have h_effort_pos : c * inv ^ 2 > 0 := by
    have h_sq : inv ^ 2 > 0 := sq_pos_of_ne_zero (ne_of_gt h_inv_pos)
    exact mul_pos h_c_pos h_sq
  have h_phi_diff : (V_k - wear + inv - 1) ^ 2 > (V_k - wear - 1) ^ 2 := by
    have h1 : V_k - wear + inv - 1 > 1 := by linarith
    have h2 : V_k - wear - 1 > 1 := by linarith
    nlinarith
  have h_stress_diff : β * ((V_k - wear + inv - 1) ^ 2 - 1) > β * ((V_k - wear - 1) ^ 2 - 1) := by
    have h_diff_pos : ((V_k - wear + inv - 1) ^ 2 - 1) - ((V_k - wear - 1) ^ 2 - 1) > 0 := by linarith
    exact mul_pos_of_pos_of_nonneg h_diff_pos (le_of_lt h_beta_pos)
  have h_congestion_nonneg : γ * lambda_shared * inv ≥ 0 := by
    have h_gl : γ * lambda_shared ≥ 0 := mul_nonneg h_gamma_nonneg h_lam_nonneg
    exact mul_nonneg h_gl (le_of_lt h_inv_pos)
  linarith

/-- Theorem: Pastoral Soil Organic Carbon (SOC) Mass Conservation Invariant
    Given initial soil carbon V_init, rotational root biomass sequestration RootSeq,
    and grazing trampling depletion TrampleLoss, the updated soil carbon valuation
    satisfies exact additive conservation: V_final - V_init = RootSeq - TrampleLoss. -/
theorem soil_carbon_mass_conservation
  (V_init RootSeq TrampleLoss : ℚ) :
  let V_final := V_init + RootSeq - TrampleLoss
  V_final - V_init = RootSeq - TrampleLoss := by
  intro V_final
  dsimp [V_final]
  ring
