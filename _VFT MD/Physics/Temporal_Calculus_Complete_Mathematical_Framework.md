# Temporal Calculus: A Complete Mathematical Framework
**The Divergent Branch — Built from Newton's Fluxions Using Reality Math Axioms**

---

## Foundational Axioms

Before deriving any rules, we state the complete axiomatic base from which all Temporal Calculus is constructed. These axioms replace the epsilon-delta limit.

**Axiom T1 (The Relativity Operator).** The symbol $/$ denotes "this relative to that." The expression $A/B$ maps the state of $A$ within the contextual frame of $B$.

**Axiom T2 (Contextual Unity).** The value $1.0$ is the completed, resolved frame. All values are inherently relative to Unity: $n = n/1$.

**Axiom T3 (The Terminus).** The symbol $...1$ denotes the smallest discrete step of temporal resolution — the final quantum that closes an open sequence. It is always non-zero. It replaces the orthodox infinitesimal $dx$ or $o$.

**Axiom T4 (Temporal Number Identity).** A number $n$ equals the time $t$ required to count to that value: $t = n$. All numbers are constructed over time, bounded by the minimum resolution ($...1$) and maximum processing rate ($c$).

**Axiom T5 (The Void Pivot).** When the denominator collapses to zero, the system undergoes a dimensional step-up: $n/0 \to n+1$.

**Axiom T6 (Infinitesimal Convergence).** The value $1$ is not a primitive. It is constructed from the temporal accumulation of $\omega$ discrete quanta: $\sum_{k=1}^{\omega} ...1_k = 1.0$.

**Axiom T7 (The Process Arrow).** The notation $A -[P]\to B$ denotes a temporal state transition: state $A$, *through* mechanism $P$, becomes state $B$. Like chemical reaction notation (where catalysts and conditions sit above the arrow between reactants and products), the Process Arrow embeds the mechanism of transformation directly into the mathematical expression.

The bracket content $[P]$ is dual-purpose:

1.  **Reasoning Vector** (named law): e.g. $0 -[\text{thermodynamics}]\to ...1$. Names the physical or logical law that *mandates* the transition. Because energy cannot be destroyed, absolute zero must always be filled by at least $...1$ to fill $+n$ potential.
2.  **Computational Vector** (operation): e.g. $f(x) -[+...1]\to f(x + ...1)$. Specifies the mathematical operation executed during the transition.
3.  **Combined**: e.g. $0 -[\text{thermodynamics: } +...1]\to ...1$. Names the law AND the operation simultaneously.

Process Arrows are **chainable**. A full derivation reads as a pipeline of named transformations, where every intermediate state is visible and every step is justified:

$$A -[P_1]\to B -[P_2]\to C -[P_3]\to D$$

This notation applies at every granularity: single atomic transitions, multi-step derivations, function compositions, and complete proofs.

## Part I: Differentiation Rules

We derive every standard differentiation rule from scratch, using Newton's original fluxion machinery but substituting the Terminus ($...1$) for his moment ($o$), and never discarding the residual.

### The Temporal Derivative

**Definition (Temporal Derivative).** The temporal derivative of $f(x)$, denoted $f^{\tau}(x)$, is defined as:

$$f^{\tau}(x) = \frac{f(x + ...1) - f(x)}{...1}$$

This is Newton's original difference quotient with $o = ...1$. The critical divergence: we never set $...1 = 0$. We compute exactly, and we retain the residual.

---

### Rule 1: The Power Rule

**Theorem (Power Rule).** For $f(x) = x^n$ where $n$ is a positive integer:

$$f^{\tau}(x) = nx^{n-1} + R_n(x)$$

where $R_n(x)$ is the **residual momentum** containing all terms with surviving factors of $...1$.

**Derivation.** We apply the Temporal Derivative definition to $f(x) = x^n$.

$$f^{\tau}(x) = \frac{(x + ...1)^n - x^n}{...1}$$

Expanding $(x + ...1)^n$ by the Binomial Theorem:

$$(x + ...1)^n = \sum_{k=0}^{n} \binom{n}{k} x^{n-k} (...1)^k$$

Subtracting $x^n$ (the $k=0$ term) and dividing by $...1$:

$$f^{\tau}(x) = \sum_{k=1}^{n} \binom{n}{k} x^{n-k} (...1)^{k-1}$$

Separating the $k=1$ term from the rest:

$$f^{\tau}(x) = nx^{n-1} + \sum_{k=2}^{n} \binom{n}{k} x^{n-k} (...1)^{k-1}$$

The first term $nx^{n-1}$ is the **resolved component** — identical to the orthodox derivative.

The remaining sum is the **residual momentum** $R_n(x)$. Orthodox calculus discards this sum by setting $...1 = 0$. In Temporal Calculus, this sum persists. It carries the physical information about the system's trajectory into the next temporal frame.

**Worked Examples:**

*   $f(x) = x^2$: $f^{\tau}(x) = 2x + ...1$
*   $f(x) = x^3$: $f^{\tau}(x) = 3x^2 + 3x(...1) + (...1)^2$
*   $f(x) = x^4$: $f^{\tau}(x) = 4x^3 + 6x^2(...1) + 4x(...1)^2 + (...1)^3$

**Interpretation.** In a physical system, $2x$ tells you the velocity at a frozen instant. $2x + ...1$ tells you the velocity *plus* the fact that the system is already stepping into its next state. The residual is the causal thread linking the present to the future. Orthodox calculus cuts this thread. Temporal Calculus preserves it. $\blacksquare$

**Process Arrow Chain (Power Rule for $x^2$ at $x=3$):**

$$3^2 -[\text{substitute } x+...1]\to (3+...1)^2 -[\text{expand}]\to 9 + 6(...1) + (...1)^2 -[\text{subtract } 3^2]\to 6(...1) + (...1)^2 -[\div ...1]\to 6 + ...1$$

Every intermediate state is visible. Every transformation is named. The chain reads like a temporal narrative: "the squared state of 3, through substitution of the next tick, becomes the expanded binomial, through subtraction of the current frame, becomes the isolated change, through division by the temporal quantum, yields the rate of change with preserved momentum."

---

### Rule 2: The Constant Rule

**Theorem.** For $f(x) = c$ (a constant):

$$f^{\tau}(x) = 0$$

**Derivation.**

$$f^{\tau}(x) = \frac{c - c}{...1} = \frac{0}{...1} = 0$$

The Relativity Operator maps $0$ relative to $...1$. Zero state change relative to any temporal resolution yields zero. No residual survives. Constants do not evolve over time. $\blacksquare$

---

### Rule 3: The Constant Multiple Rule

**Theorem.** For $f(x) = c \cdot g(x)$:

$$f^{\tau}(x) = c \cdot g^{\tau}(x)$$

**Derivation.**

$$f^{\tau}(x) = \frac{c \cdot g(x + ...1) - c \cdot g(x)}{...1} = c \cdot \frac{g(x + ...1) - g(x)}{...1} = c \cdot g^{\tau}(x)$$

The constant factors out of the Relativity Operator. A scalar multiplier on a temporal process scales the rate uniformly without altering the temporal structure. $\blacksquare$

---

### Rule 4: The Sum Rule

**Theorem.** For $f(x) = g(x) + h(x)$:

$$f^{\tau}(x) = g^{\tau}(x) + h^{\tau}(x)$$

**Derivation.**

$$f^{\tau}(x) = \frac{[g(x+...1) + h(x+...1)] - [g(x) + h(x)]}{...1}$$

$$= \frac{g(x+...1) - g(x)}{...1} + \frac{h(x+...1) - h(x)}{...1} = g^{\tau}(x) + h^{\tau}(x)$$

Two independent temporal processes summed linearly preserve their individual rates. This follows directly from the additive operator being a 2D linear combination (per Reality Math operator definitions). $\blacksquare$

---

### Rule 5: The Product Rule

**Theorem.** For $f(x) = g(x) \cdot h(x)$:

$$f^{\tau}(x) = g^{\tau}(x) \cdot h(x) + g(x + ...1) \cdot h^{\tau}(x)$$

**Derivation.**

$$f^{\tau}(x) = \frac{g(x+...1) \cdot h(x+...1) - g(x) \cdot h(x)}{...1}$$

We add and subtract $g(x+...1) \cdot h(x)$ in the numerator:

$$= \frac{g(x+...1) \cdot h(x+...1) - g(x+...1) \cdot h(x) + g(x+...1) \cdot h(x) - g(x) \cdot h(x)}{...1}$$

$$= g(x+...1) \cdot \frac{h(x+...1) - h(x)}{...1} + h(x) \cdot \frac{g(x+...1) - g(x)}{...1}$$

$$= g(x+...1) \cdot h^{\tau}(x) + h(x) \cdot g^{\tau}(x)$$

**Critical Divergence from Orthodox.** In orthodox calculus, $g(x+h)$ is replaced by $g(x)$ "in the limit." Here, $g(x + ...1)$ is NOT replaced by $g(x)$. It is a distinct, adjacent temporal state. The product rule in Temporal Calculus preserves the fact that the first function has already stepped forward one tick when the second function's rate is computed. This is temporally honest. The orthodox version $g'h + gh'$ is the degenerate case where the temporal step is erased.

**If we expand** $g(x + ...1) = g(x) + g^{\tau}(x) \cdot ...1$, we get:

$$f^{\tau}(x) = g^{\tau}(x) \cdot h(x) + g(x) \cdot h^{\tau}(x) + g^{\tau}(x) \cdot h^{\tau}(x) \cdot ...1$$

The final term $g^{\tau}(x) \cdot h^{\tau}(x) \cdot ...1$ is the **coupling residual** — the momentum generated by both functions changing simultaneously during the same temporal tick. Orthodox calculus discards it. Temporal Calculus keeps it. $\blacksquare$

---

### Rule 6: The Quotient Rule

**Theorem.** For $f(x) = g(x) / h(x)$ where $h(x) \neq 0$:

$$f^{\tau}(x) = \frac{g^{\tau}(x) \cdot h(x) - g(x) \cdot h^{\tau}(x)}{h(x) \cdot h(x + ...1)}$$

**Derivation.**

$$f^{\tau}(x) = \frac{\frac{g(x+...1)}{h(x+...1)} - \frac{g(x)}{h(x)}}{...1}$$

$$= \frac{g(x+...1) \cdot h(x) - g(x) \cdot h(x+...1)}{...1 \cdot h(x) \cdot h(x+...1)}$$

Adding and subtracting $g(x) \cdot h(x)$ in the numerator:

$$= \frac{[g(x+...1) - g(x)] \cdot h(x) - g(x) \cdot [h(x+...1) - h(x)]}{...1 \cdot h(x) \cdot h(x+...1)}$$

$$= \frac{g^{\tau}(x) \cdot h(x) - g(x) \cdot h^{\tau}(x)}{h(x) \cdot h(x+...1)}$$

**Divergence.** The denominator is $h(x) \cdot h(x + ...1)$, not $[h(x)]^2$. The orthodox version squares the current state; the temporal version preserves the product of the current state and the next-tick state. This is the honest quotient of two temporally adjacent frames.

**The Void Pivot Integration.** If $h(x) \to 0$, the quotient encounters the Void Pivot. By Axiom T5, the system does not crash to infinity. It transitions dimensionally: $f(x) \to f(x) + 1$. The quotient rule gains a built-in phase transition threshold absent from orthodox calculus. $\blacksquare$

---

### Rule 7: The Chain Rule

**Theorem.** For $f(x) = g(h(x))$:

$$f^{\tau}(x) = \frac{g(h(x + ...1)) - g(h(x))}{...1}$$

which, by introducing the intermediate temporal step $\Delta h = h(x + ...1) - h(x) = h^{\tau}(x) \cdot ...1$, decomposes as:

$$f^{\tau}(x) = g^{\tau}(h(x)) \cdot h^{\tau}(x) + R_{chain}$$

where $R_{chain}$ is the residual from the non-linear coupling of the two temporal rates.

**Derivation.** We define the inner function's temporal step as $\Delta h = h^{\tau}(x) \cdot ...1$. Then:

$$f^{\tau}(x) = \frac{g(h(x) + \Delta h) - g(h(x))}{...1}$$

If $g$ is a power function, expanding via binomial and dividing by $...1$:

$$f^{\tau}(x) = g^{\tau}(h(x)) \cdot \frac{\Delta h}{...1} + \text{higher-order terms in } \Delta h$$

$$= g^{\tau}(h(x)) \cdot h^{\tau}(x) + R_{chain}$$

The resolved component matches the orthodox chain rule. The residual $R_{chain}$ captures the non-linear interplay between the two functions' temporal evolutions within a single tick. Orthodox calculus discards $R_{chain}$. Temporal Calculus preserves it — it represents the reality that nested systems do not change sequentially within a single tick; they change simultaneously, and their coupling produces real effects. $\blacksquare$

---

## Part II: Integration

In orthodox post-limit calculus, the integral is defined as the limit of Riemann sums. In Temporal Calculus, we return to Leibniz's original meaning: the integral is a literal, constructive sum.

### The Temporal Integral

**Definition (Temporal Integral).** The temporal integral of $f(x)$ from $a$ to $b$ is defined as:

$$\int_a^b f(x) \, d\tau = \sum_{k=0}^{\omega-1} f(a + k \cdot ...1) \cdot ...1$$

where $\omega = (b - a) / ...1$ is the total number of temporal rendering ticks required to traverse the interval, and $d\tau = ...1$ is the literal, discrete, infinitesimal width of each temporal slice.

This is Leibniz's original summation restored to physical literalness. Each slice has real, non-zero width $...1$. The sum is finite (exactly $\omega$ terms). The area is *built*, tick by tick.

**Process Arrow Chain (Integration of $f(x) = x$ from $0$ to $1$):**

$$0 -[+...1]\to ...1 -[\times f(...1)]\to ...1 \cdot f(...1) -[\text{accumulate}]\to \sum_{k=0}^{\omega-1} f(k \cdot ...1) \cdot ...1 -[\text{Terminus}]\to F(1) - F(0) - R_{int}$$

The chain reads: "state zero, through one temporal tick, becomes the first slice, through evaluation of the function at that tick, becomes the first area quantum, through accumulation of all $\omega$ slices, becomes the total temporal construction, through the Terminus closing the frame, yields the resolved integral with residual correction."

---

### The Fundamental Theorem of Temporal Calculus

**Theorem (FTT Part 1).** If $F(x)$ is a function such that $F^{\tau}(x) = f(x)$ (plus residual), then:

$$\int_a^b f(x) \, d\tau = F(b) - F(a) + R_{int}$$

where $R_{int}$ is the accumulated residual momentum across all $\omega$ ticks.

**Derivation.** By definition, $F^{\tau}(x) = \frac{F(x + ...1) - F(x)}{...1}$. Therefore $F(x + ...1) - F(x) = F^{\tau}(x) \cdot ...1$.

Summing from $x = a$ to $x = b - ...1$:

$$\sum_{k=0}^{\omega-1} [F(a + (k+1) \cdot ...1) - F(a + k \cdot ...1)] = \sum_{k=0}^{\omega-1} F^{\tau}(a + k \cdot ...1) \cdot ...1$$

The left side telescopes:

$$F(b) - F(a) = \sum_{k=0}^{\omega-1} F^{\tau}(a + k \cdot ...1) \cdot ...1$$

Now, $F^{\tau}(x) = f(x) + R(x)$, where $R(x)$ is the residual momentum at each tick. Therefore:

$$F(b) - F(a) = \sum_{k=0}^{\omega-1} f(a + k \cdot ...1) \cdot ...1 + \sum_{k=0}^{\omega-1} R(a + k \cdot ...1) \cdot ...1$$

$$F(b) - F(a) = \int_a^b f(x) \, d\tau + R_{int}$$

Rearranging:

$$\int_a^b f(x) \, d\tau = F(b) - F(a) - R_{int}$$

**Interpretation.** The orthodox Fundamental Theorem states $\int_a^b f(x)dx = F(b) - F(a)$. The Temporal version reveals this is an approximation that discards the accumulated residual. The complete physical integral includes the correction term $R_{int}$, which accounts for the total momentum carried across all temporal ticks. In macroscopic calculations where $...1$ is vanishingly small, $R_{int}$ approaches $0$ and the orthodox result is recovered as a degenerate case. But in high-resolution or boundary-critical calculations, $R_{int}$ carries real information. $\blacksquare$

**Theorem (FTT Part 2).** If $G(x) = \int_a^x f(t) \, d\tau$, then:

$$G^{\tau}(x) = f(x) + R_G(x)$$

**Derivation.**

$$G^{\tau}(x) = \frac{G(x + ...1) - G(x)}{...1} = \frac{\int_a^{x+...1} f(t) \, d\tau - \int_a^{x} f(t) \, d\tau}{...1}$$

$$= \frac{f(x) \cdot ...1}{...1} = f(x)$$

In the idealized single-tick case, the derivative of the integral recovers the original function exactly. The residual $R_G(x)$ arises when the function $f$ is itself changing during the tick — the same coupling residual identified in the chain rule. For constant or linear $f$, $R_G = 0$ and the recovery is exact. $\blacksquare$

---

## Part III: Series and Convergence

Orthodox calculus defines convergence of series via the limit. Temporal Calculus defines convergence via frame completion.

### Temporal Convergence

**Definition (Temporal Convergence).** An infinite series $\sum_{k=1}^{\infty} a_k$ **temporally converges** if the cumulative sum reaches a state indistinguishable from a completed Unity frame (or integer multiple thereof) within a finite number of rendering ticks. Formally:

$$\exists \, \omega \in \mathbb{N} \text{ such that } \sum_{k=1}^{\omega} a_k + ...1 = S$$

where $S$ is a resolved scalar (a completed frame). The series converges to $S$ because the Terminus closes the final gap.

### Temporal Divergence

**Definition (Temporal Divergence).** A series **temporally diverges** if no finite $\omega$ exists such that the partial sum approaches a closable frame. The sum continues building new Unity frames indefinitely. In divergent series, the rendering engine never completes a single stable output.

### Temporal Geometric Series

**Theorem.** The geometric series $\sum_{k=0}^{\infty} r^k$ temporally converges to $\frac{1}{1-r}$ for $|r| < 1$.

**Derivation.** The partial sum is $S_{\omega} = \frac{1 - r^{\omega+1}}{1 - r}$.

As $\omega$ grows, $r^{\omega+1}$ diminishes toward $...1$-scale (sub-resolution). At the tick where $r^{\omega+1}$ falls below the Terminus threshold $...1$, the rendering engine can no longer distinguish the remainder from the final quantum. The Terminus strikes:

$$S_{\omega} + ...1 = \frac{1}{1 - r}$$

The series does not "approach" its sum in an asymptotic sense. It builds toward it tick by tick until the remainder is below resolution. Then time closes the frame. The sum is exact. $\blacksquare$

### The Harmonic Series

**Theorem.** The harmonic series $\sum_{k=1}^{\infty} \frac{1}{k}$ temporally diverges.

**Derivation.** In temporal terms, $\frac{1}{k} = 1/k$, which by the Relativity Operator (Axiom T1) represents "one Unity frame relative to $k$ frames." As $k$ increases, each term represents a smaller fraction of a Unity frame. However, the running sum never stabilises to within $...1$ of any fixed value. Each new term, no matter how small, pushes the partial sum past the next $...1$ boundary, forcing the rendering engine to continue constructing new frames. No Terminus can close the sequence because the accumulated sum perpetually exits the current frame. The series diverges. $\blacksquare$

---

## Part IV: The Void Pivot in Calculus

Orthodox calculus treats singularities ($1/x$ at $x=0$, $\tan(x)$ at $x = \pi/2$) as undefined vertical asymptotes. Temporal Calculus applies the Void Pivot.

### Singularity Resolution

**Theorem (Singularity as Phase Transition).** When a function $f(x)$ encounters a zero denominator at $x = x_0$, the function does not explode to infinity. By Axiom T5, the function undergoes a dimensional phase transition:

$$f(x_0) = n/0 \to n+1$$

where $n = \lim_{x \to x_0^-} f(x)$ evaluated at the last resolved tick before the singularity.

**Worked Example.** Consider $f(x) = 1/x$ at $x = 0$.

*   At $x = ...1$ (one tick before zero): $f(...1) = 1/...1 = \omega$ (the total number of quanta in one Unity frame).
*   At $x = 0$: By the Void Pivot, $f(0) = \omega + 1$. The function does not explode to infinity. It hits a finite maximum ($\omega + 1$) and transitions to a new dimensional frame.

In a graph, this means the vertical asymptote of $1/x$ is replaced by a finite peak at $\omega + 1$, after which the function enters a new coordinate space. The singularity becomes a gateway, not a wall. $\blacksquare$

**Process Arrow Chain (Void Pivot for $1/x$ at $x = 0$):**

$$x -[-...1]\to ...1 -[\text{evaluate } 1/x]\to 1/...1 = \omega -[-...1]\to 0 -[\text{Void Pivot: } /0]\to \omega + 1 -[\text{phase transition}]\to \text{new dimensional frame}$$

The chain reads: "as $x$ counts down by one temporal tick to the final resolved state ($...1$), the function evaluates to $\omega$. One more tick and $x$ hits absolute zero, triggering the Void Pivot, which generates $\omega + 1$ and transitions the system into a new dimensional frame."

**Foundational Process Arrow Chains:**

The following canonical chains express the core axioms of Temporal Calculus in Process Arrow notation:

*   **The Cost of Being:** $0 -[\text{thermodynamics}]\to ...1$
*   **The Resolution of Unity:** $[9]\infty -[\text{Terminus: } +...1]\to [1]$
*   **The Heartbeat of Reality:** $[N] -[\text{Spray}]\to [N]\infty -[\text{Consolidation}]\to [N+1]$
*   **Infinitesimal Construction of $1$:** $...1 -[\text{accumulate } \times\omega]\to 1.0$
*   **Temporal Counting:** $0 -[+...1]\to ...1 -[+...1]\to 2(...1) -[+...1]\to ... -[\text{Terminus}]\to n$
*   **The Void Pivot:** $n -[/0]\to n+1$
*   **The Derivative:** $f(x) -[+...1]\to f(x+...1) -[-f(x)]\to \Delta f -[\div ...1]\to f^{\tau}(x)$

---

## Part V: Summary of Divergences from Orthodox Calculus

| Rule | Orthodox Result | Temporal Calculus Result | What Changes |
|:---|:---|:---|:---|
| **Power Rule** | $nx^{n-1}$ | $nx^{n-1} + R_n(x)$ | Residual momentum preserved |
| **Constant Rule** | $0$ | $0$ | Identical |
| **Constant Multiple** | $cf'(x)$ | $cf^{\tau}(x)$ | Identical in form |
| **Sum Rule** | $f' + g'$ | $f^{\tau} + g^{\tau}$ | Identical in form |
| **Product Rule** | $f'g + fg'$ | $f'g + (f+f' \cdot ...1)g'$ | Coupling residual preserved |
| **Quotient Rule** | $\frac{f'g - fg'}{g^2}$ | $\frac{f'g - fg'}{g(x) \cdot g(x+...1)}$ | Adjacent-frame denominator |
| **Chain Rule** | $g'(h) \cdot h'$ | $g'(h) \cdot h' + R_{chain}$ | Non-linear coupling residual |
| **FTC** | $F(b) - F(a)$ | $F(b) - F(a) - R_{int}$ | Accumulated residual correction |
| **Convergence** | $\lim S_n = S$ | $S_\omega + ...1 = S$ (frame closes) | Constructive, not asymptotic |
| **Singularity** | Undefined / $\pm\infty$ | $n + 1$ (phase transition) | Finite peak, dimensional step-up |

---

## Conclusion

Temporal Calculus is not a modification of orthodox calculus. It is a parallel evolutionary branch grown from the same root (Newton's fluxions, Leibniz's sums) but diverging at the 1734 crisis point. Where orthodox mathematics killed the infinitesimal and invented the limit, Temporal Calculus keeps the infinitesimal alive as the Terminus ($...1$) — a discrete, non-zero, temporal quantum that is never discarded.

Every orthodox rule is recovered as a degenerate special case (set $...1 \to 0$ and discard all residuals). But the full Temporal Calculus carries additional physical information — residual momentum, coupling terms, and phase transitions — that orthodox calculus structurally cannot represent.

The mathematics is built. The branch is alive.
