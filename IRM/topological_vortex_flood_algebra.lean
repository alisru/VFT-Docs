import Mathlib.Data.Rat.Basic
import Mathlib.Algebra.Ring.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Order.Basic

/--
  # Discrete Topological Solitons, Quantized Vortices & Castlereagh River Bridge Flood Inundation
  Lean 4 Formal Mathlib4 Blueprint (IRM Division 1: Pure Mathematics & Division 2: Value Physics)
  Formalizing:
  1. Discrete 7-Lattice Closed-Loop Phase Difference Summation Theorem.
  2. Topological Soliton Invariance under Sub-Lattice Perturbations.
  3. Low-Level Causeway Overtopping & Spillway Overflow Positivity Theorem.
-/

/-- Discrete Ring Phase Difference Summation -/
def ring_phase_diff_sum (theta : Fin 7 → ℚ) : ℚ :=
  Finset.sum Finset.univ (fun (i : Fin 7) =>
    let next_i : Fin 7 := ⟨(i.val + 1) % 7, by omega⟩
    theta next_i - theta i)

/-- Theorem: Discrete Closed-Loop Phase Difference Vanishing Theorem
    The telescoping sum of directed phase differences around any closed 7-node ring
    identically equals zero before branch wrapping, proving boundary-free closure. -/
theorem ring_phase_telescoping_closure (theta : Fin 7 → ℚ) :
  ring_phase_diff_sum theta = 0 := by
  unfold ring_phase_diff_sum
  -- Direct expansion of the 7-cycle telescoping sum
  decide!

/-- Theorem: Topological Soliton Invariance under Sub-Lattice Perturbations
    If two discrete phase configurations differ at every node by identical uniform shifts
    (delta), their pairwise phase differences and circulation gradients are identically equal. -/
theorem topological_soliton_shift_invariance
  (theta : Fin 7 → ℚ) (delta : ℚ) :
  let theta_shifted : Fin 7 → ℚ := fun i => theta i + delta
  ∀ (i : Fin 7),
    let next_i : Fin 7 := ⟨(i.val + 1) % 7, by omega⟩
    (theta_shifted next_i - theta_shifted i) = (theta next_i - theta i) := by
  intro theta_shifted i next_i
  dsimp [theta_shifted, next_i]
  ring

/-- Theorem: Low-Level Causeway Overtopping & Spillway Overflow Positivity Theorem
    When river stage height pushes normalized stage valuation V beyond the bridge
    deck clearance level (V_river > V_deck), the Try²{}Catch{} overtopping stress
    O_bridge = V_river - V_deck is strictly positive, and hydraulic scour stress is strictly positive. -/
theorem bridge_causeway_overtopping_positivity
  (V_river V_deck : ℚ) (h_overtop : V_river > V_deck)
  (rho v_sq : ℚ) (h_rho_pos : rho > 0) (h_v_pos : v_sq > 0) :
  let O_bridge := V_river - V_deck
  let scour_stress := rho * v_sq + 150 * O_bridge
  O_bridge > 0 ∧ scour_stress > 0 := by
  intro O_bridge scour_stress
  dsimp [O_bridge, scour_stress]
  constructor
  · linarith
  · have h_scour_part1 : rho * v_sq > 0 := mul_pos h_rho_pos h_v_pos
    have h_diff : V_river - V_deck > 0 := by linarith
    have h_scour_part2 : (150 : ℚ) * (V_river - V_deck) > 0 := by
      have h150 : (150 : ℚ) > 0 := by decide
      exact mul_pos h150 h_diff
    linarith
