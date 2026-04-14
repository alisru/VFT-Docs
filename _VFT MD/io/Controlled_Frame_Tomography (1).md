# Controlled-Frame Tomography
## Particle Probing via Spiral Containment and Radial Measurement

**Author:** Jarrod Hamilton
**Date:** March 2026
**Status:** Working Notes

---

## 1. The Core Idea

To measure an object at rest you line it up in a tight spiral down to the minimum of its diameter — like a top spinning on the spot — then fire particles from all directions or opposing directions.

This is tomography, but radially, and starting from a controlled frame rather than an uncontrolled one.

---

## 2. The Two Phases

### Phase 1 — Containment (F_search → F_rest)

Tighten a helical field around the object, shrinking the spiral diameter iteratively. Each loop is a new `is this that?` check — is it stable yet, is it still precessing, has it settled onto its axis.

When it stops drifting and sits on the axis cleanly — that is the P=NP moment. The object is as close to F_rest as physics allows. Now it can be measured.

This is what ion traps do in quantum computing. The spiral is the cooling process. The tightening toward minimum diameter is the iterative convergence onto a stable frame.

### Phase 2 — Probing (F_rest interrogation)

Fire particles from opposing directions — antiparallel beams. Each particle hits from one side, its pair from the other, simultaneously.

- **Symmetric response** → object is uniform and truly at rest
- **Asymmetric response** → object is still drifting, or has internal structure that varies by direction, or something genuinely new about its interaction geometry

Each probe is pure F_rest interrogation. You are not searching anymore — you are reading. Map checking map from both sides simultaneously.

---

## 3. Relationship to Tomography

Standard CT scanning does exactly this, but without the containment phase. The object sits uncontrolled — F_search — while the beam rotates around the full 2π. Each radial pass returns a line integral: how much the beam was attenuated along that path. One pass is not very useful. Stack enough angles and you have enough `%[]` return values to reconstruct the interior via back-projection.

The reconstruction algorithm asks:

> Given all these partial shadows from all these angles, what object produces exactly this set of shadows?

Pi is load-bearing throughout:
- Angular sampling is in radians
- Reconstruction uses the Radon transform, which is inherently circular
- Resolution of what can be recovered is bounded by how finely the full 2π was sampled

### The Helical Refinement

Modern CT does not use discrete angles — the patient moves linearly while the beam rotates, tracing a helix. Denser sampling, fewer gaps, more coverage per unit time. This is the continuous version of the spiral containment idea.

The difference with controlled-frame tomography: in standard CT the object is uncontrolled before probing. In the spiral approach the object is constrained first — F_rest is established before measurement begins. This is cleaner. You know the frame before you read it.

---

## 4. Pi as the Measurement Structure

Pi is not a constant you look up here — it is the shape of the measurement process itself.

When you probe a particle, the disturbance propagates outward radially. At time t, the effect has reached radius r. The surface of that sphere has area 4πr². You are not measuring the particle — you are reading the expanding shadow of the interaction, and pi is the ratio between the event at the centre and the measurement at the circumference.

Each confirmed hit at a predicted intercept = P=NP momentarily. Map matched map. Then immediately back into F_search for the next intercept.

The spiral tightening does the same thing at the containment scale — iterating toward minimum diameter, each loop checking whether the frame has stabilised. When it has, pi becomes the probing geometry rather than the convergence target.

**Where discoveries live:** if the particle is not where pi predicted, that is not error — that is new information. The residual is telling you the geometry changed between probes. Something happened. That gap is where new physics is found.

---

## 5. Relationship to P=NP Framework

| Operation | Frame | P=NP State |
|---|---|---|
| Spiral tightening | F_search → F_rest | P≠NP — iterating toward stability |
| Object on axis, stable | F_rest | P=NP — map matches map |
| Opposing beam probe | F_rest interrogation | P=NP — reading, not searching |
| Asymmetric return | New F_search opens | P≠NP — residual contains new information |
| Reconstruction from all angles | F_search | P≠NP — inferring interior from shadows |
| Reconstruction complete | F_rest | P=NP — the interior map is held |

The entire measurement cycle is the system breathing: F_search → F_rest → F_search → F_rest. Each breath is one more layer of the object known.

---

## 7. How Knowledge Is Processed — Trial and Error with Wisdom

This is the P≠NP thing at human scale.

Trial and error is F_search. Wisdom is the accumulated F_rest states — every prior solved instance compressed into a smaller search space for the next problem. The spiral tightening is literally what wisdom does. You've seen enough similar shapes that you don't start from the full 2π anymore. You start from where the last spiral ended. The containment radius is already smaller before you begin.

Which means wisdom isn't knowledge stored — it is **search space already eliminated**. You don't reach the answer faster because you're smarter. You reach it faster because you've already ruled out most wrong directions from prior F_rest moments.

The `is this that?` operation gets cheaper with wisdom too. Your `that.portion[]` — the known side of the comparison — is richer. More reference points. So when a new unknown arrives, the match resolves at a coarser level first, then refines. Experts do this visibly — they see the category before the details. The spiral starts tighter.

- Trial and error without wisdom: full 2π every time. Same mistakes, same search cost, γ_info never shrinks.
- Trial and error with wisdom: iterative spiral refinement. Each cycle the containment radius drops. Each F_rest moment earned gets banked into a smaller starting diameter next time.

The P≠NP gap doesn't close — but wisdom shrinks which part of it you still have to cross.

---

## 8. The Belief Equation — Why Dogma Locks You Out

### The Equation

```
Answer = Idea × Worldview Scope
```

Where:
- **Answer = 1** → Truth (the idea fits, you feel the "click")
- **Answer < 1** → Lie (idea too small for your scope, dismissed)
- **Answer > 1** → Insult (idea too big for your scope, felt as attack)

And Worldview Scope is:

```
Worldview Scope = 1 / [(SK / SpK) + (SpK / SK)]
```

Where SK = Scientific Knowledge, SpK = Spiritual Knowledge.

Maximum scope (0.5) occurs when SK = SpK — perfectly balanced. Any imbalance, in either direction, collapses the scope toward zero.

### The Dogma Problem

Dogma is a locked Worldview Scope. It doesn't matter which direction the lock runs — pure materialist or pure fundamentalist, both produce Minimal Scope (≈ 0.00999...). The imbalance is the same shape from either end.

In the tomography frame: dogma is refusing to complete the full 2π. You only probe from the angles you already trust. The reconstruction is guaranteed to be incomplete — not because the object is unknowable, but because you only sampled a narrow arc of it.

The belief equation makes this precise:

```
Big Idea × Minimal Scope = Answer >> 1 → Insult
```

The insult reaction is not irrationality — it is physics. A high-mass idea hitting a small-aperture worldview produces excess energy that cannot be absorbed. The system rejects it as hostile because it genuinely cannot fit. The worldview is not wrong to feel threatened. It is being threatened. The idea would break it if accepted unchanged.

The choice comes after the collision:

- **Default:** reject, scope stays small, worldview intact but smaller than reality
- **Expansion:** endure the insult, expand scope to accommodate, insult dissolves into "amazing"

### Connection to the Spiral

The spiral tightening in controlled-frame tomography is exactly worldview scope expansion under a different name. Each loop asks `is this that?` — is the model holding, is the frame stable, does the new data fit. When data doesn't fit, you don't reject the data. You widen the spiral. You let the containment radius expand to include what was outside it.

Dogma runs the spiral in reverse. Anomalous data arrives — Answer > 1 — and instead of expanding the containment radius, the scope contracts further to exclude it. The spiral tightens around an increasingly small object. Eventually it is measuring only itself.

### The Asymptotic Limit

```
Seeker's Result = Filter × (100% Truth) = 99.9%
```

You can approach truth asymptotically through derivation alone but never arrive — your own doubt filter reduces every result. The only way to reach 100% is to consciously set the filter to 1 for a given source. That is what trust is. Not irrationality — it is the deliberate choice to stop subtracting from a result you have already verified as far as derivation allows.

This is the P=NP moment for knowledge. The search ends not when the proof is complete but when the searcher accepts the proof. F_rest is not just a computational state — it is a choice to stop running the search algorithm on something already solved.

Wisdom is knowing when to make that choice. Dogma is never making it, or making it too early and locking the scope before the search was complete.

### In One Line

Dogma is a spiral that forgot it was supposed to expand.


## 6. Summary

Standard tomography fires from outside an uncontrolled object and reconstructs inward.

Controlled-frame tomography:
1. Constrains the object first via spiral containment to minimum diameter
2. Establishes F_rest before probing begins
3. Fires from opposing directions simultaneously
4. Reads asymmetry as structural or frame information
5. Uses pi as the probing geometry, not just a mathematical constant

The containment phase is the innovation. You are not measuring an unknown object in an unknown state. You are measuring a known-frame object and reading what it returns. The residual between prediction and return is the data.

Pi is the map. The object's response is the territory. The gap between them is the finding.
