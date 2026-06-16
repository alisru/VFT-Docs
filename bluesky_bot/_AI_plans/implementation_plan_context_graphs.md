# Implementation Plan: Nested Context-in-Context Graphs

Introduce a nested, multi-layered coordinate system to visually display a micro-event's evaluation inside its overarching macro-context event (e.g. evaluating a sports title win within the context of a political photo-op event).

## Proposed Changes

### 1. Evaluator Prompt & Schema Changes
#### [MODIFY] [google_ai_studio_one_shot.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/google_ai_studio_one_shot.py)
* Update system prompts and examples to instruct the model to identify and evaluate the **macro-context event** if the story contains one.
* Expand the JSON output list schema from 11 items to 16 items by appending:
  * `item[11]`: `macro_event` (string; name of the overarching context/venue, or `""` if none)
  * `item[12]`: `macro_claim_u` (float or `null`)
  * `item[13]`: `macro_claim_psi` (float or `null`)
  * `item[14]`: `macro_real_u` (float or `null`)
  * `item[15]`: `macro_real_psi` (float or `null`)
* Update `transpose_flat_to_json` to parse these 5 new elements if they exist (gracefully defaulting to `""` and `None` for backward compatibility with older 11-element JSONs).

### 2. Validation & Registry Processing
#### [MODIFY] [post_batch.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/post_batch.py) and [validate_batch.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/validate_batch.py)
* Ensure validation does not fail if new optional macro keys (`macro_event`, `macro_claim_u`, etc.) are present in the JSON story configs.

#### [MODIFY] [rebuild_registries.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/rebuild_registries.py)
* Update calls to `draw_graph` to pass the new macro parameters from the config dictionary if present.

### 3. Graph Generation Logic
#### [MODIFY] [generate_graph.py](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/generate_graph.py)
* Update `draw_graph` signature to accept optional macro parameters:
  ```python
  def draw_graph(claim_u, claim_psi, real_u, real_psi, title, filename,
                 macro_event="", macro_claim_u=None, macro_claim_psi=None, macro_real_u=None, macro_real_psi=None)
  ```
* If `macro_event` is present:
  1. Plot the **macro-event** coordinates `(macro_claim_u, macro_claim_psi)` and `(macro_real_u, macro_real_psi)` on the outer axes as standard Stated (yellow circle) and Actual (red star) points.
  2. Draw an **inner nested box** centered at `(0, 0)` spanning `[-0.5, 0.5]` on both outer axes.
  3. Determine if the macro-context is **selfish** (`macro_real_u < 0`). If so, **mirror the inner coordinate space horizontally (flipped on the vertical y-axis)** (`is_mirrored = True`).
  4. Write inner quadrant labels (`The Greater Good`, `The Greatest Lie`, etc.) and corner tags (`JUSTICE`, `TYRANNY`, etc.) inside the inner box, mirrored horizontally using `scale(-1, 1)` transform if mirrored.
  5. Plot the **micro-event** coordinates `(claim_u, claim_psi)` to `(real_u, real_psi)` inside the inner box. The plot coordinates are scaled by `0.25` and the morality coordinate (u) is negated if mirrored:
     * `u_plot = (-claim_u if is_mirrored else claim_u) * 0.25`
     * `psi_plot = claim_psi * 0.25`
  6. Draw dashed connection projection lines from the outer macro points to the corresponding inner box corners in the same quadrant.

---

## Verification Plan

### Automated Tests
1. Create a verification script `scratch/test_context_graph.py` that calls the updated `draw_graph` using the exact UFC / White House event parameters:
   * **Macro**: Stated `(1.0, 1.0)`, Actual `(-1.0, -1.0)` ("White House promotional event")
   * **Micro**: Stated `(0.0, 0.0)`, Actual `(-0.5, 0.5)`
2. Run the script and output the graph to `scratch/test_context_graph.png`.
3. Check that the inner box is correctly rotated 180 degrees, points are scaled, and dashed projection lines connect the outer points to the inner corners.

---

## Graph Visual Specification

This section is the source of truth for what a correctly rendered Psochic Hegemony graph must look like. Use it to validate any generated graph.

---

### Outer Grid

| Element | Spec |
|---|---|
| Background | `#111111` (near-black) — figure and axes |
| Grid lines | Dotted gray, `alpha=0.3`, low weight |
| X axis (Morality υ) | **Reversed** — positive (+2.0) is on the LEFT, negative (-2.0) on the RIGHT |
| Y axis (Will ψ) | Standard — positive (+2.0) is TOP, negative (-2.0) is BOTTOM |
| Axis labels | X: `"Morality (υ)"`, Y: `"Will (ψ)"`, white |

**X tick labels (left → right):**
`Everyone (+2.0)` · `Others (+1.0)` · `Other (+0.5)` · `No One (0.0)` · `My Group (-0.5)` · `Me (-1.0)` · `Only Me (-2.0)`

**Y tick labels (top → bottom):**
`Active-Active (+2.0)` · `Passive-Active (+1.0)` · `Neutral (0.0)` · `Passive-Passive (-1.0)` · `Active-Passive (-2.0)`

---

### Zone Boxes

| Zone | Shape | Style |
|---|---|---|
| Zone 1 (Inner Horizon) | Rectangle from `(+1.0, -1.0)` to `(-1.0, +1.0)` | Dashed white border, no fill |
| Zone 2 (Outer Horizon) | Rectangle from `(+2.0, -2.0)` to `(-2.0, +2.0)` | Solid white border, no fill |

---

### Zone 1 Corner Labels (the four quadrant names)

Placed just inside the Zone 1 corners. **These never move.**

| Position | Label |
|---|---|
| Top-Left (u=+1, ψ=+1) | `The Greater Good (Flow)` |
| Top-Right (u=-1, ψ=+1) | `The Greatest Lie (Greed)` |
| Bottom-Left (u=+1, ψ=-1) | `The Lesser Good (Peace)` |
| Bottom-Right (u=-1, ψ=-1) | `The Greater Evil (Void)` |

### Zone 2 Corner Labels (strategic extremes)

Placed just inside the Zone 2 corners. **These never move.**

| Position | Label |
|---|---|
| Top-Left (u≈+2, ψ≈+2) | `JUSTICE` |
| Top-Right (u≈-2, ψ≈+2) | `TYRANNY` |
| Bottom-Left (u≈+2, ψ≈-2) | `STAGNATION` |
| Bottom-Right (u≈-2, ψ≈-2) | `CHAOS` |

---

### Single-Level Graph (no macro context)

| Element | Spec |
|---|---|
| Stated Claim point | Yellow hollow circle (`o`), `markersize=10` |
| Actual Reality point | Red star (`*`), `markersize=15` |
| Trajectory arrow | Dashed white, curved arc from Stated → Actual |
| Title | `"{title}\nProjected Eventuality: {path_name}\nStated: ({u:+.1f}, {ψ:+.1f}) | Actual: ({u:+.1f}, {ψ:+.1f})"` |
| Legend | Bottom-centre, 2 columns |

---

### Dual-Level Graph (macro context present)

Only renders when `macro_event` is non-empty AND macro coords differ from micro coords.

#### Macro layer (outer grid)

| Element | Spec |
|---|---|
| Macro Stated | Yellow hollow circle (`o`), `markersize=10` |
| Macro Actual | Red star (`*`), `markersize=15` |
| Macro trajectory | Dashed white curved arc, Macro Stated → Macro Actual |

#### Inner box

| Element | Spec |
|---|---|
| Position | Centred at `(0,0)`, spans `[-0.5, +0.5]` on both axes |
| Fill | `#161616` (slightly lighter than background) |
| Border | Solid white, `linewidth=1.5` |
| Internal axes | Thin gray lines at `x=0` and `y=0` inside the box |

#### Inner box corner labels (P- labels)

Placed at the corners of the inner box. **Position never changes** — they are fixed to the box corners regardless of inversion state.

| Corner | Label | ha | va |
|---|---|---|---|
| Top-Left `(+0.51, +0.51)` | `P-LE` | right | bottom |
| Top-Right `(-0.51, +0.51)` | `P-GG` | left | bottom |
| Bottom-Left `(+0.51, -0.51)` | `P-GE` | right | top |
| Bottom-Right `(-0.51, -0.51)` | `P-LG` | left | top |

#### Inversion

`is_inverted = (macro_real_u < 0) AND (micro_real_u > 0)`

A good micro actual inside a bad macro frame. The bad macro perceives the prosocial act as a threat — the inner frame flips horizontally to show this distortion.

When `is_inverted = True`:
- Micro points are plotted with **negated u**: `u_plot = -micro_u * 0.5`
- Inner corner JUSTICE/TYRANNY/etc tags swap sides (left↔right)

When `is_inverted = False`:
- Micro points plotted normally: `u_plot = micro_u * 0.5`
- Inner corner tags in standard orientation

#### Micro layer (inside inner box)

| Element | Spec |
|---|---|
| Micro Stated | Yellow hollow circle (`o`), `markersize=6` |
| Micro Actual | Red star (`*`), `markersize=9` |
| Micro trajectory | Dashed white curved arc, Micro Stated → Micro Actual |
| Scale | All micro coordinates multiplied by `0.5` before plotting |

#### Title (dual-level)

```
{scenario title}
Frame Type: {frame_desc} | Projected Eventuality: {path_name}
Micro Stated ({u:+.1f}, {ψ:+.1f}): {micro_claim_desc}
Micro Actual ({u:+.1f}, {ψ:+.1f}): {micro_real_desc}
Macro Stated ({u:+.1f}, {ψ:+.1f}): {macro_claim_desc}
Macro Actual ({u:+.1f}, {ψ:+.1f}): {macro_real_desc}
```

**Frame type strings:**

| Macro actual | Micro actual | Frame desc |
|---|---|---|
| ≥ 0 | ≥ 0 | `Standard Hegemony: Good Event in Good Macro Frame` |
| ≥ 0 | < 0 | `Standard Hegemony: Bad Event in Good Macro Frame` |
| < 0 | ≥ 0 | `Inverted Hegemony: Good Event in Bad Macro Frame` |
| < 0 | < 0 | `Inverted Hegemony: Bad Event in Bad Macro Frame` |

#### Legend

Bottom-centre, 4 columns: `Macro Stated` · `Macro Actual` · `Micro Stated` · `Micro Actual`

---

### Watermark

`"Psychic Hegemony Graph"` — italic, dark gray `#444444`, bottom-centre of figure.

---

### Scenario Validity Rule

> **The macro is the cause-effect-possible-lyrical space of the micro.**
>
> The macro defines what causes the micro event, what effects it can produce, what outcomes are possible, and what meaning it carries. Remove the macro — if the micro still makes sense as its own independent story, the pairing is invalid. They are two separate trajectories, not a nested context.

---

## Perceptual Inversion State Table

Working document. Mark each state `YES / NO / ?` in the Invert column.

**Variables:**
- `+` = positive morality (u > 0, good/altruistic)
- `-` = negative morality (u < 0, bad/selfish)
- `~` = preference (u ≈ 0, neutral)

**Question per state:** Is this serving the bad frame? / Does the inner frame need to flip to show perceptual distortion?

**Confirmed anchors:**
- Honest states (stated = actual at both levels) = NO inversion
- Bad frame only exists when Macro Actual = `-`

```
MACRO trajectory    MICRO trajectory    State label                          Invert?
Stated → Actual     Stated → Actual
──────────────────────────────────────────────────────────────────────────────────────
  +  →  +            +  →  +           Honest Good / Honest Good              NO
  +  →  +            +  →  -           Honest Good / Deception                ?
  +  →  +            ~  →  +           Honest Good / Latent Good              ?
  +  →  +            ~  →  -           Honest Good / Latent Bad               ?
  +  →  +            -  →  +           Honest Good / Redemption               ?
  +  →  +            -  →  -           Honest Good / Honest Bad               NO
──────────────────────────────────────────────────────────────────────────────────────
  +  →  ~            +  →  +           Deflation / Honest Good                ?
  +  →  ~            +  →  -           Deflation / Deception                  ?
  +  →  ~            ~  →  +           Deflation / Latent Good                ?
  +  →  ~            ~  →  -           Deflation / Latent Bad                 ?
  +  →  ~            -  →  +           Deflation / Redemption                 ?
  +  →  ~            -  →  -           Deflation / Honest Bad                 ?
──────────────────────────────────────────────────────────────────────────────────────
  +  →  -            +  →  +           Macro Deception / Honest Good          YES (N5)
  +  →  -            +  →  -           Macro Deception / Micro Deception      ?
  +  →  -            ~  →  +           Macro Deception / Latent Good          ?
  +  →  -            ~  →  -           Macro Deception / Latent Bad           ?
  +  →  -            -  →  +           Macro Deception / Subversion           ?
  +  →  -            -  →  -           Macro Deception / Honest Bad           NO (N3)
──────────────────────────────────────────────────────────────────────────────────────
  ~  →  +            +  →  +           Latent Good / Honest Good              ?
  ~  →  +            +  →  -           Latent Good / Deception                ?
  ~  →  +            ~  →  +           Latent Good / Latent Good              ?
  ~  →  +            ~  →  -           Latent Good / Latent Bad               ?
  ~  →  +            -  →  +           Latent Good / Redemption               ?
  ~  →  +            -  →  -           Latent Good / Honest Bad               ?
──────────────────────────────────────────────────────────────────────────────────────
  ~  →  ~            +  →  +           Stasis / Honest Good                   NO
  ~  →  ~            +  →  -           Stasis / Deception                     ?
  ~  →  ~            ~  →  +           Stasis / Latent Good                   NO
  ~  →  ~            ~  →  -           Stasis / Latent Bad                    NO
  ~  →  ~            -  →  +           Stasis / Redemption                    ?
  ~  →  ~            -  →  -           Stasis / Honest Bad                    NO
──────────────────────────────────────────────────────────────────────────────────────
  ~  →  -            +  →  +           Latent Bad / Honest Good               ?
  ~  →  -            +  →  -           Latent Bad / Deception                 ?
  ~  →  -            ~  →  +           Latent Bad / Latent Good               ?
  ~  →  -            ~  →  -           Latent Bad / Latent Bad                ?
  ~  →  -            -  →  +           Latent Bad / Subversion                ?
  ~  →  -            -  →  -           Latent Bad / Honest Bad                NO
──────────────────────────────────────────────────────────────────────────────────────
  -  →  +            +  →  +           Macro Redemption / Honest Good         ?
  -  →  +            +  →  -           Macro Redemption / Deception           ?
  -  →  +            ~  →  +           Macro Redemption / Latent Good         ?
  -  →  +            ~  →  -           Macro Redemption / Latent Bad          ?
  -  →  +            -  →  +           Macro Redemption / Redemption          ?
  -  →  +            -  →  -           Macro Redemption / Honest Bad          ?
──────────────────────────────────────────────────────────────────────────────────────
  -  →  ~            +  →  +           Partial Redemption / Honest Good       ?
  -  →  ~            +  →  -           Partial Redemption / Deception         ?
  -  →  ~            ~  →  +           Partial Redemption / Latent Good       ?
  -  →  ~            ~  →  -           Partial Redemption / Latent Bad        ?
  -  →  ~            -  →  +           Partial Redemption / Redemption        ?
  -  →  ~            -  →  -           Partial Redemption / Honest Bad        ?
──────────────────────────────────────────────────────────────────────────────────────
  -  →  -            +  →  +           Corrupt Stable / Honest Good           YES (N1)
  -  →  -            +  →  -           Corrupt Stable / Deception             ? (N2)
  -  →  -            ~  →  +           Corrupt Stable / Latent Good           YES (Gaethje)
  -  →  -            ~  →  -           Corrupt Stable / Latent Bad            ?
  -  →  -            -  →  +           Corrupt Stable / Subversion            ? (guard/medicine)
  -  →  -            -  →  -           Corrupt Stable / Honest Bad            NO (N3, N16)
──────────────────────────────────────────────────────────────────────────────────────
```

