# Implementation Plan - Fractally Bifurcated Qqci Templates

This plan designs the integration of a **generic, fractally bifurcated template structure** along the 7 planes of reality (Qqci) for SAEL/Tautonic transitions.

---

## 📐 Conceptual Design: Fractal Bifurcation

Every potential action or concept (e.g. `relocate`, `transfer`) is represented as a template containing both a **Success (Order/Virtue)** state and a **Failure (Chaos/Sin/Deficit)** state for each of the 7 planes. 

Because the structure is **fractal**, any slot in the template can be nested with another sub-template (resolving sub-planes like $Q_i.q_j$).

### Example: `@RELOCATE` Bifurcated Template

| Plane (Q) | Success Branch (Order) | Failure Branch (Chaos/Deficit) |
| :--- | :--- | :--- |
| **Q1: Who (Identity)** | `active_agent` (Sovereignty) | `victim` / `uncontrolled` (Tyranny) |
| **Q2: What (Substance)** | `intact_vehicle` (Stewardship) | `exploded_vehicle` (Greed/Destruction) |
| **Q3: Where (Locus)** | `target_destination` (Thriving) | `death` / `stuck` (Mere Survival) |
| **Q4: Why (Purpose)** | `locomotion` (Truth-Telling) | `accident` / `failure` (Delusion) |
| **Q5: How (Method)** | `valid_path` (Wisdom) | `invalid_path` (Sophistry) |
| **Q6: Cause (History)** | `physics` context | `physics` context |
| **Q7: Effect (Outcome)** | `arrival` (Love/Unity) | `destruction` / `scatter` (Parasitism) |

---

## 🛠️ Proposed C# Architecture

### 1. AST & Registry Extensions in [`SAELIntegration.cs`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/Reality%20Class'ification%20project/SAELIntegration.cs)

We will introduce:
*   **`BifurcatedState`**: A container holding a `Success` concept definition and a `Failure` concept definition. It can optionally reference a nested `BifurcatedTemplate` for fractal sub-plane recursion.
*   **`BifurcatedTemplate`**: Maps each of the 7 planes (`Who`, `What`, `Where`, `Why`, `How`, `Cause`, `Effect`) to a `BifurcatedState`.
*   **`SaelTemplateRegistry`**: A global database of pre-defined bifurcated templates for canonical actions (`relocate`, `transfer`, `terminate`, etc.).
*   **`SaelProjector`**: A matching engine that:
    1.  Takes a parsed SAEL expression.
    2.  Projects the input values onto the action's bifurcated template.
    3.  Scores the similarity to the **Success** branch vs the **Failure** branch (using synonym lookups or simple string matching).
    4.  Assigns the resulting truth scores (closer to `1.0f` for success, or deviant `0.4f - 1.5f` for failure).
    5.  Evaluates the final Tautonic `Idea` through the coherence gate.

---

## 🔍 Verification Plan

We will build the C# executable and run the console demo with the updated interactive REPL. We will verify that:
1.  Entering a successful relocation (e.g. `destination=grocery_store`, `position => to grocery_store`) matches the **Success** template and outputs `Y=1 (TRUTH)`.
2.  Entering a failed relocation (e.g. `destination=death`, `position => exploded`) matches the **Failure** template and outputs `INSULT > 1 (CHAOS/TYRANNY)`.
3.  The demo prints the matched branch and the similarity projection details.

Command to compile and run:
```powershell
$env:DOTNET_ROLL_FORWARD="Major"
dotnet run --project "e:\Vector Field Theory\VFT Docs\Reality Class'ification project\RealityClassification.csproj"
```
