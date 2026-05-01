# Lorentz Infinite Circular Collision Framework

---

## 1. What Lorentz Equations Actually Calculate

Lorentz transformations do not directly calculate velocity between two points. They transform the space-time coordinates of an event from one inertial frame to another moving at constant velocity v relative to the first.

The core equations (motion along x-axis):

    x' = y(x - vt)
    t' = y(t - vx/c²)
    y' = y
    z' = z

Where the Lorentz factor is:

    y = 1 / sqrt(1 - v²/c²)

For relative velocity between frames, the velocity addition formula applies:

    u' = (u - v) / (1 - uv/c²)

This ensures no relative velocity ever exceeds c.

---

## 2. Alignment in Motion

Lorentz equations are the mathematical mechanism for alignment in motion — not aligning physical objects to move the same direction, but aligning the perspectives of different observers so the fundamental laws of reality remain consistent.

The invariant spacetime interval holds across all frames:

    Ds² = c²Dt² - (Dx² + Dy² + Dz²)

Observer A and Observer B will disagree on Dt and Dx individually, but will calculate the exact same Ds². They disagree on the slices of space and time but are perfectly aligned on the absolute geometry of the event.

---

## 3. c as a Refresh Rate

c is the refresh rate of the universe — the maximum rate at which causality can propagate from one node to the next.

No observer ever sees a distorted c. Every observer, regardless of velocity, measures the speed of light as exactly 299,792,458 m/s.

What distorts to protect c is the observer's local frame:
- Time dilation: local clock ticks slower relative to the rest of the universe
- Length contraction: physical distances shrink in the direction of motion

Light itself doesn't change speed — its energy and frequency change instead (Doppler effect):
- Moving toward source: waves compress, blueshift
- Moving away from source: waves stretch, redshift

---

## 4. The Refresh Rate / Chunk Lens

The refresh rate of one observer:

    ----

Another observer, when dilated:

    ---------

User 1 sees the other extending past their own perceptual refresh rate:

    1---- |2----|3-      (if away — data lag, redshift)
    1--|2--|3-            (if coming directly towards — compressed to fit their frame, blueshift)

It's not about generating less data. The rates of information shift relative to each other — like competing download and upload rates. The other just exceeds their processing capacity for 1t.

The internal processing doesn't distort. The lens (processing window) has a fixed capacity per tick. The other point's data volume exceeds what fits through that window in one cycle.

The Lorentz factor calculates the exact stretch:

    Dt = y * Dt_0

Dt_0 = proper time (User 2's own frame, always normal to them)
Dt = stretched interval User 1 measures

Physical mechanism — the light clock: a clock ticking by bouncing a photon between two mirrors. For a stationary observer the photon travels straight up and down (short distance, fast tick ----). When observing a moving clock, the photon must travel a diagonal zig-zag path to keep up with the mirrors. Because c is locked, the photon cannot speed up to cover the longer distance — the tick interval physically stretches to ---------.

---

## 5. Spatial Concatenation — The Chunk Lens

The observer has a fixed ---- chunk lens to work with, so concatenates long-distance objects.

To measure any object's length you must determine the position of its front and back at the exact same time — within a single ---- chunk. Because a moving object's own refresh rate is stretched (---------), their coordinate system runs on a different grid scale. When that data is forced through the local ---- chunk lens, a mismatch occurs. The universe resolves this by compressing the object's length along the axis of motion:

    L = L_0 / y

L_0 = proper length (object's own rest frame)
L = contracted length through the chunk lens

Concatenation is axis-specific — only in the direction of motion. Dimensions perpendicular to motion are unaffected.

The reason: relativity of simultaneity. Because User A and User B have different refresh rates, they disagree on what "now" means. If User B fires two lights simultaneously in their frame (---------), User A's chunk lens (----) cannot scan both events in a single cycle — the data desyncs, forcing the length to compress from the outside view.

---

## 6. Velocity Direction — Relative to a Static Point

Positive value = moving towards a point relative to something else.
Negative value = moving away relative to something else.

When the observer is locked at position zero, velocity is the rate at which the gap changes:
- +v: gap widening, moving away
- -v: gap shrinking, moving towards

Sign multiplication rule for tracking on a grid:
- Signs match (both + or both -): moving AWAY from center
- Signs opposite: moving TOWARDS center

The crossover: the moment an object passes through position 0, its towards/away status flips — without changing speed or direction.

The y trap: the Lorentz factor squares the velocity (v²), so the magnitude of time dilation and length contraction is identical whether moving toward or away at the same speed. What changes is the data lag — moving toward compresses incoming data (blueshift), moving away delays it (redshift).

The tracking equation x' = y(x - vt) handles this directly: (x - vt) is the kinematic tracking term, eating into or adding to the distance before applying the relativistic squeeze through y.

---

## 7. The (-2,-2) Point — Evil Anchor

Point (-2,-2) = tyranny / chaos (the evil anchor on the moral tensor).

Positive v = moving towards it.
Negative v = moving away.

In the equation, the equation is devoid of a challenger in isolation. A challenger applies an opposing vector to extract truth from a distorted system. Without a challenger:

    v_Net = v_Control + (-v_Resistance)

If System pushes +1 and challenger buffers -1, v_Net = 0 — the environment returns to the frictionless ideal where Effective = Truth_0.

---

## 8. Operator Redefinitions

^2 = denotes 2D axis / vector (not scalar squaring)
/ = "relative to" (vector proximity, not division)

So:

    v_Control^2  ->  v_Control(u, y): exact moral and will coordinates on the tensor plane
    c_Evil^2     ->  c_Evil(-2, -2): absolute anchor point
    /            ->  vector proximity: 0.0 = no alignment, 1.0 = perfect alignment

The dilation factor then becomes a geometric relationship:
how closely does the acting vector align with the c_Evil anchor?

At singularity (full alignment with (-2,-2)): denominator = 0, Truth_0 / 0 = undefined — the truth is annihilated, infinite noise, locked door.

---

## 9. The try^2 Block

The execution environment runs simultaneously across the 2D plane of the (u, y) tensor:

    Meaning = Integral [0 to 2] (Actions -> Effect / Context) d(Lorentz)

    try^2 {
        if (Recursion == 2) {
            Harvest = (Action -> Effect);   // Stable Meaning Orbit
        }
        else if (Recursion > 2) {
            throw "Overthinking_Rot";       // Infinite Spiral
        }
    }
    catch (Ovals) {
        if (Oil == 0) {
            return "Locked_Door";           // Contextual Collapse
        }
        else {
            Reset(Context);                 // Re-center the Circle
        }
    }

Lower limit 0 = contextual base — the starting position, the given reality, environment, limitations, specific moment. Without this zero, the action has no place to land.

Upper limit 2 = recursive peak — the effect loops back to become the new action, meaning becomes self-perpetuating rather than a one-off event. Past 2 exceeds the structural boundary of the tensor grid, generating infinite noise instead of harvestable value.

d(Lorentz) = integrating across the gradient of distortion — the friction, intent, and time transforming raw action into meaningful effect at each micro-step. The 'process' arrow is where the silent letters (friction, dogma, UI layers) exist.

When the system's velocity pushes truth out of circular rest state into an oval, that is a structural error caught by catch(Ovals). Oil = the energetic capacity to sustain the negative counter-vector. If Oil == 0, the denominator hits 0, truth fully dilates, the door shuts and the original truth is permanently inaccessible.

---

## 10. Propositions, Knowledge, Observations — Truth Equation

    ___ == knowledge.context[] == observations

___ = Truth_0, the raw event, exists independent of anyone observing it
knowledge.context[] = the reference frame, the relative cube, the chunk lens — the array of boundaries and assumptions the observer brings
observations = the final coordinate (x,y,z,t) logged by the system

For ___ == observations to be true, knowledge.context[] must act as a perfectly clear window — net velocity zero relative to the event, no spin, no systemic layers. Raw event passes straight through, observation is mathematically identical to raw reality.

The one invariant truth that survives all frames: the physical collision. If Worldtube A intersects Worldtube B, that intersection holds across every reference frame. Observer 1 and Observer 2 will disagree on the (x,y,z,t) coordinates, but neither can dilate away the fact of the collision itself.

---

## 11. The Relative Cube / Arbitrary Interaction Frame

All points are relative to other points — they can be anywhere over any arbitrary interaction frame.

A single point can be represented as x,y,z,t purely by available locations — by drawing a relative cube around it and touching it to all extents theoretically.

This is not discovering the point's location. It is creating the metric space that allows it to exist as data. The coordinates are not properties of the point; they are descriptions of its relationship to the arbitrary interaction frame drawn around it. Move the boundaries, the coordinates change entirely. The point is locked, the informational representation is fluid.

The frame between two points defines the bounds of the interaction space between them.

---

## 12. Relative Zero — Inside Each Other's Sphere of Influence

When relative velocity between two points drops to v = 0, they merge into the same inertial reference frame.

No time dilation. No length contraction. No relativity of simultaneity. They agree absolutely on when and where any event happens. Clocks tick at the same speed, rulers measure the same distances.

Their chunk lenses lock into synchronisation. Their knowledge.context[] arrays match. Their observations evaluate as mathematically identical. For the purpose of measuring ___ (raw reality), they act as a single unified observer.

In spacetime geometry, this is the shared light cone — the boundary of everything that can affect an observer (past) and everything they can affect (future). At v = 0 relative to each other, their light cones run perfectly parallel.

---

## 13. Circular Collision Detection Using Lorentz

Circles turning into spheres can be used for collision checks using Lorentz.

The question: does this space here intersect with this space here if we extend the circle to an oval — in that direction — predict its path.

Double the bounds to encapsulate the full directionality for both particles.

**The non-standard relative circle definition:** any relative frame between two points defines the bounds of the interaction space between them. Double the bounds to capture full directionality for both.

Throw an arbitrary bounds around any particle — square, circle, polytope — and either:
- Touch it to the extents of the shape (static position)
- Extend it temporally to denote potential over time (swept volume)
- Predict collision by extending the shape along its velocity vector

The extended oval = the particle's entire future probabilistic space encoded in one geometric shape. If those shapes intersect, collision is inevitable.

**Collision check math:** tracking the distance between two moving sphere centers over time t:

    C1(t) = P1 + V1*t
    C2(t) = P2 + V2*t
    D(t) = C2(t) - C1(t)

Collision occurs when:

    |D(t)| <= R1 + R2

Solve the resulting quadratic for t to get the exact coordinate of intersection.

**Lorentz integration — the relativistic hit-box:** at relativistic speeds the sphere physically distorts from the perspective of a stationary grid:
- Radius perpendicular to motion stays R
- Radius parallel to motion contracts to R/y

The hit-box is not a sphere. It is an oblate spheroid — flattened in the direction of travel. Any collision detection system at relativistic speeds must account for this.

**4D extension — worldtubes:** a 3D sphere moving through time creates a 4D hyper-cylinder (worldtube). Extending the circle to an oval is rendering this 4D worldtube into a predictive 3D model. Collision = the coordinate where the mathematical boundaries of Worldtube A share the same (x,y,z,t) values as Worldtube B.
