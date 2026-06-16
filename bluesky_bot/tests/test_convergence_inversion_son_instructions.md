# Test Instructions: Convergence-Inversion Test using the SON Method

This document outlines the test instructions for evaluating context-in-context narratives using the **Multi-Attractor Vector Force Equilibrium (SON) Method**. This protocol calculates coordinates and detects perceptual inversions dynamically by evaluating the story's relationship to all points.

---

## 1. The Prompt Template (AI Input)

To populate the attractor fields, we send the following instruction set to the AI:

```markdown
You are an expert hegemonic analyst. Evaluate the provided news story and populate the 3-reading vector (Support, Oppose, Neutral) in the range [0.0 - 1.0] for each of the 4 moral/volitional attractors:

*   **Greater Good (GG)**: (+1.0, +1.0)
*   **Greater Evil (GE)**: (-1.0, -1.0)
*   **Lesser Good (LG)**: (+1.0, -1.0)
*   **Lesser Evil (LE)**: (-1.0, +1.0)

For each attractor, populate:
- **Support (S)**: Does the action/narrative align with, reinforce, or promote this attractor? (Provide quote/evidence + score)
- **Oppose (O)**: Does the action/narrative actively violate, resist, or conflict with this attractor? (Provide quote/evidence + score)
- **Neutral (N)**: Is the action/narrative indifferent, orthogonal, or unrelated to this attractor? (Provide quote/evidence + score)
```

---

## 2. Reference AI Evaluation (`gaethje-ufc-white-house-show`)

Below is the reference output demonstrating how the AI populates the SON vectors using the target story text:

### Attractor 1: Greater Good (GG = +1.0, +1.0)
*   **Support ($S_{GG}$)**: **0.3**
    *   *Evidence*: "A champion's victory lap on the White House lawn, framed as a patriotic spectacle... celebrating 250 years of American independence."
    *   *Rationale*: The framing claims a public benefit (patriotism/unity), but it is a surface-level cover.
*   **Oppose ($O_{GG}$)**: **0.8**
    *   *Evidence*: "Using the nation's highest civic lawn for a commercial bloodsport... degrades public institutions."
    *   *Rationale*: The action directly conflicts with systemic justice and civic dignity.
*   **Neutral ($N_{GG}$)**: **0.3**
    *   *Evidence*: "Combat sports can showcase incredible human resilience, skill..."
    *   *Rationale*: The athletic achievement is partially orthogonal to the political co-optation.

### Attractor 2: Greater Evil (GE = -1.0, -1.0)
*   **Support ($S_{GE}$)**: **0.7**
    *   *Evidence*: "...using violence as entertainment... masking the destructive nature of the sport."
    *   *Rationale*: It actively promotes physical violence as public entertainment, drifting toward Chaos.
*   **Oppose ($O_{GE}$)**: **0.0**
    *   *Evidence*: None.
    *   *Rationale*: No actors in the scenario oppose or resist the violence.
*   **Neutral ($N_{GE}$)**: **0.1**
    *   *Evidence*: None.
    *   *Rationale*: The event is active, not passive.

### Attractor 3: Lesser Evil / Greatest Lie (LE = -1.0, +1.0)
*   **Support ($S_{LE}$)**: **0.9**
    *   *Evidence*: "...hosted on Trump's birthday... extracting public prestige for private branding."
    *   *Rationale*: The event is a high-will, self-serving co-optation of a public symbol for private branding.
*   **Oppose ($O_{LE}$)**: **0.0**
    *   *Evidence*: "Trump and UFC president Dana White were prominent figures."
    *   *Rationale*: No actors resist the co-optation.
*   **Neutral ($N_{LE}$)**: **0.1**
    *   *Evidence*: None.
    *   *Rationale*: The event is highly partisan/deceptive.

### Attractor 4: Lesser Good (LG = +1.0, -1.0)
*   **Support ($S_{LG}$)**: **0.4**
    *   *Evidence*: "...providing a moment of shared celebration for its intended audience."
    *   *Rationale*: It provides passive/local entertainment for a subset of the population.
*   **Oppose ($O_{LG}$)**: **0.3**
    *   *Evidence*: "...put a UFC cage on the White House lawn..."
    *   *Rationale*: The active violence conflicts with passive stasis/peace.
*   **Neutral ($N_{LG}$)**: **0.3**
    *   *Evidence*: "...genuinely entertained millions of fans..."
    *   *Rationale*: The fans are passive consumers, not active builders.

---

## 3. Reference Coordinate Calculation

$$\sum \text{Weights} = 1.4 (\text{GG}) + 0.8 (\text{GE}) + 1.0 (\text{LE}) + 1.0 (\text{LG}) = 4.2$$

$$\sum \vec{F}_i = (-2.0, 0.0)$$

$$\vec{C}_{net} = \frac{(-2.0, 0.0)}{4.2} = (-0.476, 0.0)$$

This places the final coordinate in the **Lesser Evil / Greatest Lie** quadrant on the fly, matching the co-opted reality of the event.
