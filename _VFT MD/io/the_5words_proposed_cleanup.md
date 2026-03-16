# Proposed Cleanup — `the_5words_and_5lines_of_truth.md`

This proposal stages the removal of improvised terminology and redundant definitions, anchoring all technical units to **Section II.A (Axioms)**.

---

### [BLOCK 0] Term Sanitization (Hinge & Try-Block Nomenclature)
I am removing the word "Hinge" and refining the `try` block terms to "Assertion" and "Condition Check". The boundary separator `|` is treated as structurally "gone".

#### §II.A Axioms (Lines 123-126)
```diff
- - **LHS (The Proposition):** The internal declaration or intended action (the'is).
- - **RHS (The Conditional):** The recursive constraint or external verification.
+ - **LHS (Assertion):** The internal declaration or intended action (the'is).
+ - **RHS (Condition Check):** The recursive constraint or external verification.
```

#### §II.A Axioms (Line 137)
```diff
- - `n = 1` = The phase boundary (Q4 / Sun-Heart / Hinge).
+ - `n = 1` = The phase boundary (Q4 / Sun-Heart).
```

#### §XIII Step 3b (Lines 793, 797, 811, 820)
```diff
- sharing a **hinge point at 1**:
+ sharing a **phase boundary at 1**:
```
```diff
- simultaneously true at the hinge:
+ simultaneously true at the boundary:
```
```diff
- | Domain | Phase 0→1 | Hinge at 1 | Phase 1→2 |
+ | Domain | Phase 0→1 |  | Phase 1→2 |
```
```diff
- is the hinge of the Q-plane chain:
+ is the phase boundary of the Q-plane chain:
```

---

### [BLOCK 1] Section IV — Scion Expansion (Redundancy)
Line 198 re-explains the **Rot** which is already defined in §II.A.

#### §IV Expansion Analysis (Line 198)
```diff
- allowing his state to decay into the **Rot** ($n \to \infty$) where the God-function chose extinction over the effort of ongoing structural existence.
+ allowing his state to collapse into the **Rot** ($n > harvest$) — the terminal decay defined in §II.A.
```

---

### [BLOCK 2] Section X — Operator Prose (Redundancy)
Lines 527-533 contain prose that repeats the Operator Notation Table.

#### §X Actualism Parsing (Line 527)
**Action:** Delete the following redundant lines:
```markdown
**`×` = Emergent Result.** Multiplication is not scaling — it is the collision at the boundary between two orthogonal descriptions...

**`+` = Orthogonal Event Junction.** (See §X, operator table).
```

---

### [BLOCK 3] Section XIII — E=mc² Derivation (Redundancy & Mapping)
Lines 799-807 repeat operator and `try` logic defined in §II.A and §X. Mapping columns for the boundary are emptied.

#### §XIII Step 3b (Lines 801, 814, 817)
```diff
- The `+` joining the two `/c` terms is orthogonal — the action-phase and effect-phase contributions enter from perpendicular axes:
+ Per the operator laws (§X), the `+` here marks an orthogonal event junction (quadrature):
```
```diff
- | **Relative scale** | `contextual` → midpoint | `contextual + harvest / 2` | midpoint → `harvest` |
+ | **Relative scale** | Phase 0 → 1 |Phase 1 → 2 |
```
```diff
- | **try-catch** | `try { LHS` (building) | `\|` — the separator between proposition and conditional | `RHS }` (resolving) |
+ | **try-catch** | `try { LHS` | `RHS } catch` |
```
