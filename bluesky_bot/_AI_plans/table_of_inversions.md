# Psochic Hegemony: Table of Inversions

This document acts as the reference research file for detecting and verifying **perceptual inversions** when micro-events are nested inside macro-contexts.

---

## 1. The Programmatic Detection Rule

A perceptual inversion occurs when a positive/constructive micro-action is co-opted, threatened, or distorted by a negative/selfish containing macro-context. 

In terms of the Cartesian grid coordinates:
*   **Macro Actual is Bad**: $m\_real\_u < 0$
*   **Micro Actual is Good**: $real\_u > 0$

```python
is_inverted = (m_real_u < 0) and (real_u > 0)
```

If this condition is met, the inner micro-coordinate box in the graph is rotated by 180 degrees (mirroring the perception of the axes). If the condition is not met, the graph remains upright (normal).

---

## 2. Inversion Reference Table

This table maps every combination of macro and micro trajectories to determine if a perceptual inversion is triggered for the micro-event.

| MACRO Trajectory (Stated $\to$ Actual) | MICRO Trajectory (Stated $\to$ Actual) | State Label / Explanation | Invert? | Case Reference |
| :--- | :--- | :--- | :---: | :--- |
| **`+` $\to$ `+` (Honest Good)** | `+` $\to$ `+` | Honest Good / Honest Good | **NO** | |
| | `+` $\to$ `-` | Honest Good / Deception | **NO** | |
| | `~` $\to$ `+` | Honest Good / Latent Good | **NO** | |
| | `~` $\to$ `-` | Honest Good / Latent Bad | **NO** | |
| | `-` $\to$ `+` | Honest Good / Redemption | **NO** | |
| | `-` $\to$ `-` | Honest Good / Honest Bad | **NO** | |
| **`+` $\to$ `~` (Deflation)** | Any Micro | Deflation / Any | **NO** | |
| **`+` $\to$ `-` (Macro Deception)** | `+` $\to$ `+` | Macro Deception / Honest Good | **YES** | Case N5 (Sustainability Whistleblower) |
| | `+` $\to$ `-` | Macro Deception / Micro Deception | **NO** | |
| | `~` $\to$ `+` | Macro Deception / Latent Good | **YES** | |
| | `~` $\to$ `-` | Macro Deception / Latent Bad | **NO** | |
| | `-` $\to$ `+` | Macro Deception / Subversion | **YES** | |
| | `-` $\to$ `-` | Macro Deception / Honest Bad | **NO** | Case N3 (Clinic Takeover / Bribe Guard) |
| **`~` $\to$ `+` (Latent Good)** | Any Micro | Latent Good / Any | **NO** | |
| **`~` $\to$ `~` (Stasis)** | Any Micro | Stasis / Any | **NO** | |
| **`~` $\to$ `-` (Latent Bad)** | `+` $\to$ `+` | Latent Bad / Honest Good | **YES** | |
| | `+` $\to$ `-` | Latent Bad / Deception | **NO** | |
| | `~` $\to$ `+` | Latent Bad / Latent Good | **YES** | |
| | `~` $\to$ `-` | Latent Bad / Latent Bad | **NO** | |
| | `-` $\to$ `+` | Latent Bad / Subversion | **YES** | |
| | `-` $\to$ `-` | Latent Bad / Honest Bad | **NO** | |
| **`-` $\to$ `+` (Macro Redemption)** | Any Micro | Macro Redemption / Any | **NO** | |
| **`-` $\to$ `~` (Partial Redemption)**| Any Micro | Partial Redemption / Any | **NO** | |
| **`-` $\to$ `-` (Corrupt Stable)** | `+` $\to$ `+` | Corrupt Stable / Honest Good | **YES** | Case N1 (Layoffs / Dedicated Team Leader) |
| | `+` $\to$ `-` | Corrupt Stable / Deception | **NO** | Case N2 (Welfare Theft / Theft Charity) |
| | `~` $\to$ `+` | Corrupt Stable / Latent Good | **YES** | Case Gaethje |
| | `~` $\to$ `-` | Corrupt Stable / Latent Bad | **NO** | |
| | `-` $\to$ `+` | Corrupt Stable / Subversion | **YES** | Case N12 (Abusive Prison / Reading Lessons)|
| | `-` $\to$ `-` | Corrupt Stable / Honest Bad | **NO** | Case N3, N16 (Developer / Price-Gouging) |

---

## 3. Case-by-Case Analysis

### Case N1: Corrupt Stable / Honest Good $\to$ YES
*   **Macro Context**: Corporate Merger collapses ($m\_real\_u = -1.0$).
*   **Micro Event**: Team leader works overtime to deliver the project anyway ($real\_u = 1.0$).
*   **Dynamic**: The micro-action is positive, but it is trapped in a dying system. The system co-opts or ignores the effort.

### Case N2: Corrupt Stable / Deception $\to$ NO
*   **Macro Context**: Welfare safety net collapsed/embezzled ($m\_real\_u = -1.0$).
*   **Micro Event**: Local charity steals donations ($real\_u = -1.0$).
*   **Dynamic**: The micro-action is actual negative/bad, which matches the macro environment. Both are corrupt; no inversion occurs.

### Case N3: Macro Deception / Honest Bad $\to$ NO
*   **Macro Context**: Private operator takes over clinic to strip assets ($m\_real\_u = -1.0$).
*   **Micro Event**: Security guard demands bribes and locks medicine cabinet ($real\_u = -1.0$).
*   **Dynamic**: A corrupt micro-actor operating in a corrupt macro-frame. Coherent bad behavior; no inversion.

### Case N5: Macro Deception / Honest Good $\to$ YES
*   **Macro Context**: Factory green program dumps toxic waste ($m\_real\_u = -1.0$).
*   **Micro Event**: Sustainability officer documents violations and goes public ($real\_u = 1.0$).
*   **Dynamic**: A positive whistleblowing action inside a deceptive macro-corporate frame. The corporation perceives the good act as an active threat.

### Case N12: Corrupt Stable / Subversion $\to$ YES
*   **Macro Context**: Prison rehabilitation program descends into violence ($m\_real\_u = -1.0$).
*   **Micro Event**: Community volunteer enters to teach reading lessons ($real\_u = 1.0$).
*   **Dynamic**: A positive educational subversion of a corrupt stable system. The prison system/abusive guards perceive the good act as a threat.
