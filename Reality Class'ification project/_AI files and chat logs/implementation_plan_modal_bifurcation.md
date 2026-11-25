# Implementation Plan - Modal Position Spectrum & coordinates

This plan designs the integration of the **Modal Position Spectrum** (the 2D relativity tile) into the SAEL-Tautonic template evaluation pipeline.

---

## 📐 Conceptual Design: Modal Tile Positions & Coordinates

Instead of using simple float truth scores, failure/success states are represented as positions on a 2D Modal Tile:

*   **`Are` (0,0)**: present actual assertion ("thing" / actual success).
*   **`CanBe` (+x,+y)**: open possibility / potential.
*   **`NotAll` (-x,+y)**: bounded negation ("not at all" / gone / destroyed).
*   **`NotReally` (-x,-y)**: soft negation ("was like" / decay / death).
*   **`WasLike` (+x,-y)**: analogical past ("similar to").

When projecting a SAEL expression onto a bifurcated template, each plane matches to a specific `ModalPosition` on the tile:
*   Success state $\to$ typically `ModalPosition.Are` `(0,0)`.
*   Failure states map to the `!not` negation spectrum:
    *   Vehicle destroyed (`What`) $\to$ `ModalPosition.NotAll` `(-x,+y)`.
    *   Destination is death (`Where`) $\to$ `ModalPosition.NotReally` `(-x,-y)`.

---

## 🛠️ Proposed C# Changes

### 1. Update `{Meaning}.cs` and `{Idea}.cs`
*   Define `enum ModalPosition` in `namespace TautonicLanguageEngine` (mirroring `RealityClassification.ModalPosition` but for the active engine namespace).
*   Add `public ModalPosition Position { get; set; } = ModalPosition.Are;` to `TautonicLanguageEngine.Meaning`.
*   Add a helper method `GetModalCoordinates(ModalPosition pos)` returning a string coordinate representation (e.g. `x-y+` for `NotAll`).

### 2. Update `SAELIntegration.cs`
*   Update `PlaneState` to store `SuccessPosition` and `FailurePosition`.
*   Update `SaelTemplateRegistry` to define the success/failure modal positions for each plane.
*   Update `SaelProjector.Project` to output `Dictionary<string, ModalPosition>` for the 7 planes.
*   Update `SaelTautonicBridge.MapToTautonicIdea` to set the `Position` of the meanings of the planes.
*   Update `SaelDemo.RunScenario` to print the matched modal position and coordinate (e.g. `NotAll [x-y+]` or `Are [0,0]`) alongside each plane's name and score.

---

## 🔍 Verification Plan

We will build the C# executable and run the console demo. We will verify that:
1.  In Scenario 2 (successful locomotion), all planes map to `Are [0,0]`.
2.  In the rocket explosion scenario, the failed planes map to their specific `!not` spectrum positions (e.g., `Where` maps to `NotReally [x-y-]` and `Effect` maps to `NotAll [x-y+]`).
3.  The demo shell displays the modal tile position and coordinate string.

Command to compile and run:
```powershell
$env:DOTNET_ROLL_FORWARD="Major"
dotnet run --project "e:\Vector Field Theory\VFT Docs\Reality Class'ification project\RealityClassification.csproj"
```
