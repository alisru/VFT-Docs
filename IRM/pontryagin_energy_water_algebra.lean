import Mathlib.Data.Rat.Basic
import Mathlib.Algebra.Ring.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Order.Basic

/--
  # Process Pontryagin Maximum Principle (P-PMP) & Energy-Water Co-Optimization
  Lean 4 Formal Mathlib4 Blueprint (IRM Division 1: Pure Mathematics & Division 2: Value Physics)
  Formalizing:
  1. Process Hamiltonian Maximization and Action Proportionality Theorem.
  2. Adjoint Co-State Invariance on Manifest Ground State [0, 2].
  3. Energy-Water Dual Storage Power Allocation Invariant.
-/

/-- Process Hamiltonian Valuation Function -/
def hamiltonian_val (λ I W c stress_penalty : ℚ) : ℚ :=
  λ * (I - W) - (1/2 * c * I ^ 2 + stress_penalty)

/-- Theorem: Hamiltonian Quadratic Maximization Theorem
    For c > 0 and optimal action I_opt = λ / c, the difference H(I_opt) - H(I)
    equals 1/2 * c * (I - I_opt)², which is non-negative for all I. -/
theorem hamiltonian_maximization
  (λ I W c stress_penalty : ℚ)
  (h_c_pos : c > 0) :
  let I_opt := λ / c
  hamiltonian_val λ I_opt W c stress_penalty - hamiltonian_val λ I W c stress_penalty =
    1/2 * c * (I - I_opt) ^ 2 := by
  intro I_opt
  dsimp [hamiltonian_val, I_opt]
  have h_c_ne : c ≠ 0 := by linarith
  calc
    (λ * (λ / c - W) - (1/2 * c * (λ / c) ^ 2 + stress_penalty)) -
    (λ * (I - W) - (1/2 * c * I ^ 2 + stress_penalty))
      = λ * (λ / c - I) - 1/2 * c * ((λ / c) ^ 2 - I ^ 2) := by ring
    _ = 1/2 * c * (I - λ / c) ^ 2 := by
      have h1 : λ * (λ / c - I) = (λ ^ 2 / c) - λ * I := by ring
      have h2 : 1/2 * c * (I - λ / c) ^ 2 = 1/2 * c * I ^ 2 - λ * I + (1/2 * λ ^ 2 / c) := by
        field_simp
        ring
      field_simp
      ring

/-- Theorem: Adjoint Invariance on Manifest Ground State
    When capital/storage valuation is inside the manifest interval 0 ≤ V_K ≤ 2,
    the gradient of quadratic stress ∂Stress²/∂K vanishes identically,
    preserving the adjoint co-state λ_{t+1} = λ_t. -/
theorem adjoint_invariance_in_manifest_interval
  (V_K λ_curr β : ℚ)
  (h_in_bounds : 0 ≤ V_K ∧ V_K ≤ 2) :
  let grad_stress := if V_K < 0 ∨ V_K > 2 then 2 * β * (V_K - 1) else 0
  let λ_next := λ_curr - grad_stress
  λ_next = λ_curr := by
  intro grad_stress λ_next
  dsimp [grad_stress, λ_next]
  have h_not : ¬ (V_K < 0 ∨ V_K > 2) := by
    push_neg
    exact h_in_bounds
  rw [if_neg h_not]
  ring

/-- Theorem: Energy-Water Dual Storage Power Allocation Invariant
    For any solar surplus P_solar and any shadow prices λ_e > 0, λ_w > 0,
    the sum of power allocated to battery storage and water pumping equals P_solar. -/
theorem energy_water_power_conservation
  (P_solar λ_e λ_w : ℚ)
  (h_sum_pos : λ_e + λ_w > 0) :
  let ratio_e := λ_e / (λ_e + λ_w)
  let P_bess := P_solar * ratio_e
  let P_pumps := P_solar * (1 - ratio_e)
  P_bess + P_pumps = P_solar := by
  intro ratio_e P_bess P_pumps
  dsimp [P_bess, P_pumps]
  ring
