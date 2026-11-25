import Mathlib.Data.Rat.Basic
import Mathlib.Algebra.Ring.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Order.Basic

/--
  # 7-Plane Stochastic Process Bellman Dynamic Programming & Aquifer Resilience
  Lean 4 Formal Mathlib4 Blueprint (IRM Division 1: Pure Mathematics & Division 2: Value Physics)
  Formalizing:
  1. Discrete Regime-Switching Stochastic Loss Functional.
  2. Stochastic Overcapacity Zero-Investment Invariant Theorem.
  3. Aquifer-Irrigation Mass Conservation Invariant.
-/

/-- Single-Regime Instantaneous Loss Function -/
def single_regime_loss
  (c α β V_curr inv influx loss D : ℚ) : ℚ :=
  let V_next := V_curr + inv + influx - loss
  let l_effort := c * inv ^ 2
  let deficit := if D - V_next > 0 then D - V_next else 0
  let l_deficit := α * deficit ^ 2
  let phi := (V_next - 1) ^ 2
  let l_stress := if phi - 1 > 0 then β * (phi - 1) else 0
  l_effort + l_deficit + l_stress

/-- Expected Loss across 3 Discrete Climatic Regimes -/
def expected_stochastic_loss
  (c α β V_curr inv D : ℚ)
  (p₁ p₂ p₃ : ℚ)
  (inf₁ inf₂ inf₃ loss₁ loss₂ loss₃ : ℚ) : ℚ :=
  p₁ * single_regime_loss c α β V_curr inv inf₁ loss₁ D +
  p₂ * single_regime_loss c α β V_curr inv inf₂ loss₂ D +
  p₃ * single_regime_loss c α β V_curr inv inf₃ loss₃ D

/-- Theorem: Stochastic Overcapacity Zero-Investment Invariant Theorem
    When base valuation in all weather regimes exceeds the saturation limit wall (V_base > 2)
    and demand is normal (D ≤ 1), any positive investment inv > 0 strictly increases the expected loss.
    Therefore, the stochastic optimal policy strictly shuts off investment. -/
theorem stochastic_overcapacity_zero_investment
  (c α β V_curr D inv : ℚ)
  (p₁ p₂ p₃ : ℚ)
  (inf₁ inf₂ inf₃ loss₁ loss₂ loss₃ : ℚ)
  (h_c_pos : c > 0)
  (h_beta_pos : β > 0)
  (h_inv_pos : inv > 0)
  (h_p1_pos : p₁ > 0)
  (h_p2_pos : p₂ ≥ 0)
  (h_p3_pos : p₃ ≥ 0)
  (h_over1 : V_curr + inf₁ - loss₁ > 2)
  (h_over2 : V_curr + inf₂ - loss₂ > 2)
  (h_over3 : V_curr + inf₃ - loss₃ > 2)
  (h_D_le_1 : D ≤ 1) :
  expected_stochastic_loss c α β V_curr inv D p₁ p₂ p₃ inf₁ inf₂ inf₃ loss₁ loss₂ loss₃ >
  expected_stochastic_loss c α β V_curr 0 D p₁ p₂ p₃ inf₁ inf₂ inf₃ loss₁ loss₂ loss₃ := by
  -- Follows from strict positivity of effort cost and strict convexity of stress in each regime
  unfold expected_stochastic_loss single_regime_loss
  dsimp
  have h_effort_pos : c * inv ^ 2 > 0 := by
    have h_sq : inv ^ 2 > 0 := sq_pos_of_ne_zero (ne_of_gt h_inv_pos)
    exact mul_pos h_c_pos h_sq
  -- In each regime, stress strictly increases with inv > 0 when base > 2
  have h_diff_phi : ∀ V_base, V_base > 2 → (V_base + inv - 1) ^ 2 > (V_base - 1) ^ 2 := by
    intro V_base h_b
    have h1 : V_base + inv - 1 > 1 := by linarith
    have h2 : V_base - 1 > 1 := by linarith
    nlinarith
  -- Therefore every term in the sum for inv > 0 is strictly greater than for inv = 0
  have h_term1_gt : single_regime_loss c α β V_curr inv inf₁ loss₁ D >
                    single_regime_loss c α β V_curr 0 inf₁ loss₁ D := by
    unfold single_regime_loss
    dsimp
    have h_b1 : V_curr + inf₁ - loss₁ > 2 := h_over1
    have h_sq_diff : (V_curr + inv + inf₁ - loss₁ - 1) ^ 2 > (V_curr + inf₁ - loss₁ - 1) ^ 2 := by
      have h_rw : V_curr + inv + inf₁ - loss₁ - 1 = (V_curr + inf₁ - loss₁) + inv - 1 := by ring
      rw [h_rw]
      exact h_diff_phi (V_curr + inf₁ - loss₁) h_b1
    linarith
  have h_weighted1 : p₁ * single_regime_loss c α β V_curr inv inf₁ loss₁ D >
                     p₁ * single_regime_loss c α β V_curr 0 inf₁ loss₁ D := by
    exact mul_lt_mul_of_pos_left h_term1_gt h_p1_pos
  linarith

/-- Theorem: Aquifer Water Table Mass Conservation Invariant
    Given initial water table V_init, natural recharge R, and irrigation extraction I,
    the updated water table valuation V_final satisfies exact additive conservation:
    V_final - V_init = R - I. -/
theorem aquifer_mass_conservation
  (V_init Recharge Irrig : ℚ) :
  let V_final := V_init + Recharge - Irrig
  V_final - V_init = Recharge - Irrig := by
  intro V_final
  dsimp [V_final]
  ring
