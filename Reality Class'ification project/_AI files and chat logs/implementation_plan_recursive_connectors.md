# Implementation Plan - Recursive +i Connectors & Nested Node Mapping

This plan integrates the **`+i` connection operator** (represented by the dot `.` separator) to link planes/slots recursively to other classes or sub-nodes, fulfilling the **fractal Qqci plane bifurcation** design.

---

## 📐 Conceptual Design: +i Drilling & Path-Based Addressing

In the SAEL grammar, variables are represented as `Entity.Property` (e.g., `rocket.position` or `Alice.balance`). 

Instead of treating these as flat string keys, we project them geometrically:
1.  **The Class/Entity Node**: `rocket` is a parent `TruthState` / class node in the registry.
2.  **The +i Connector**: The dot `.` operator is the `+i` (Drill) operator.
3.  **The Sub-Node Slot**: `position` represents a sub-plane (e.g., Locus `Where` or Substance `What`) inside the `rocket` class definition.

When evaluating a SAEL statement:
*   The parent state (`@RELOCATE` or `@TRANSFER`) has slots containing the entities.
*   If an effect mutates a sub-property (`rocket.position`), the parent state drills down using `+i` into the child `TruthState` representing the entity's internal properties.
*   The target property's state determines if that child step is `Filled`, `NeverFilled`, or evaluates to a boundary position like `InGap` (which triggers further drill-down).

---

## 🛠️ Proposed C# Changes

### 1. Update `SAELIntegration.cs`
*   **Path-Based Parsing**: Support parsing and validating nested variables `entity.property` as recursive paths.
*   **Recursive TruthState Generator**:
    *   Build a helper `SaelTautonicBridge.BuildStateTree(SaelExpression expr)` that constructs a nested tree of `TruthState` objects from `RealityClassification.v2.cs`.
    *   For each parameter and effect, look up or carve the entity as a parent class `TruthState` at the root address, then use `DrillInto` to instantiate property sub-states.
*   **Coherence and Gate Evaluation**:
    *   Evaluate the fill states of the sub-states recursively. If a nested property fails (e.g., `rocket.position` is `exploded`), the parent entity state resolves to a failed state (`NotAll` or `NotReally`), which escalates up to the root action.

### 2. Update `SaelDemoRunner`
*   Add a new scenario or test case demonstrating a recursive SAEL expression.
*   Print the constructed `TruthState` tree, showing the active recursive addresses (e.g., `Root/physics/rocket/position`) and their fill/coherence status.

---

## 🔍 Verification Plan

We will build the C# executable and run the demo runner. We will verify that:
1.  Variables like `rocket.position` are correctly parsed into a hierarchical `TruthState` tree.
2.  Drilling into properties follows the staircase gating rule (throwing or escalating when step coherence fails).
3.  The console visualizes the address paths and fill states.

Command to compile and run:
```powershell
$env:DOTNET_ROLL_FORWARD="Major"
dotnet run --project "e:\Vector Field Theory\VFT Docs\Reality Class'ification project\RealityClassification.csproj"
```
