import Mathlib.Data.Rat.Basic
import Mathlib.Algebra.Ring.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Order.Basic

/--
  # 7-Plane Bounded Metabolic Equilibrium & Spatial Friction Algebra
  Lean 4 Formal Mathlib4 Blueprint (IRM Division 1: Pure Mathematics & Division 2: Value Physics)
  Formalizing:
  1. The Bounded Metabolic Operator T on [0, 2]⁷.
  2. Bounded Fixed-Point Invariant: T maps the manifest hypercube [0, 2]⁷ into itself.
  3. Spatial Friction and Distance Monotonicity Theorem.
-/

/-- Manifest Clamping Projection onto [0, 2] -/
def manifest_clamp (v : ℚ) : ℚ :=
  if v < 0 then 0
  else if v > 2 then 2
  else v

/-- Theorem: Manifest Clamp is Bounded in [0, 2] -/
theorem manifest_clamp_bounded (v : ℚ) :
  0 ≤ manifest_clamp v ∧ manifest_clamp v ≤ 2 := by
  unfold manifest_clamp
  split_ifs with h1 h2
  · constructor <;> decide
  · constructor <;> decide
  · push_neg at h1 h2
    exact ⟨h1, h2⟩

/-- 7-Plane Bounded Metabolic Operator Step -/
def metabolic_operator_step
  (A : Fin 7 → Fin 7 → ℚ) (C : Fin 7 → ℚ) (P : Fin 7 → ℚ) (j : Fin 7) : ℚ :=
  let input_cost := Finset.sum Finset.univ (fun i => A i j * manifest_clamp (P i))
  manifest_clamp (input_cost + C j)

/-- Theorem: 7-Plane Bounded Fixed-Point Invariant
    The Bounded Metabolic Operator strictly preserves the manifest bounds [0, 2]⁷
    for any non-negative matrix A and vector C. -/
theorem metabolic_operator_preserves_bounds
  (A : Fin 7 → Fin 7 → ℚ) (C : Fin 7 → ℚ) (P : Fin 7 → ℚ) (j : Fin 7) :
  0 ≤ metabolic_operator_step A C P j ∧ metabolic_operator_step A C P j ≤ 2 := by
  unfold metabolic_operator_step
  dsimp
  exact manifest_clamp_bounded _

/-- Theorem: Spatial Distance Monotonicity Theorem
    Given two spatial distance matrices d₁ ≤ d₂ component-wise, with non-negative
    technology coefficients A, transport friction κ > 0, and non-negative inputs P,
    the un-clamped input cost is monotonically non-decreasing with distance. -/
theorem spatial_cost_monotone
  (A : Fin 7 → Fin 7 → ℚ) (C : Fin 7 → ℚ) (P : Fin 7 → ℚ)
  (d₁ d₂ : Fin 7 → Fin 7 → ℚ) (κ : ℚ) (j : Fin 7)
  (h_kappa_nonneg : 0 ≤ κ)
  (h_d_le : ∀ i, d₁ i j ≤ d₂ i j)
  (h_P_nonneg : ∀ i, 0 ≤ manifest_clamp (P i)) :
  (Finset.sum Finset.univ (fun i => (A i j + κ * d₁ i j) * manifest_clamp (P i)) + C j) ≤
  (Finset.sum Finset.univ (fun i => (A i j + κ * d₂ i j) * manifest_clamp (P i)) + C j) := by
  have h_sum_le :
    Finset.sum Finset.univ (fun i => (A i j + κ * d₁ i j) * manifest_clamp (P i)) ≤
    Finset.sum Finset.univ (fun i => (A i j + κ * d₂ i j) * manifest_clamp (P i)) := by
    apply Finset.sum_le_sum
    intro i _
    have h_d_term : κ * d₁ i j ≤ κ * d₂ i j := by
      exact mul_le_mul_of_nonneg_left (h_d_le i) h_kappa_nonneg
    have h_coeff_le : A i j + κ * d₁ i j ≤ A i j + κ * d₂ i j := by
      linarith
    exact mul_le_mul_of_nonneg_right h_coeff_le (h_P_nonneg i)
  linarith
