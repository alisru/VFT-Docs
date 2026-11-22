# Implementation Plan: Actual Language Model Pathway (v3)
**Creation Timestamp:** 2026-10-18T18:40:00+11:00  
**Supersedes:** `plans/PLAN_20261009_v2_Causal_Z_Axis_Revision.md`  
**Status:** Active Implementation Roadmap  
**Project Location:** `polytrope_transformer/`  

---

## 1. Executive Vision: From Embedding Classifier to Generative Language Model
The previous prototype demonstrated that the $(7 \times 6 + n)$ Polytrope accurately classifies coordinates, rotates modal rays, and tracks causal roots vs fruits. 

The user's new diagram establishes the **Generative Dialectic State Machine**: meaning is not static; it is an active, directed sequence of modal transitions that resolves what:
* **`will be`** (The Solution / Generative Future)
* **`can't be`** (The Problem / Physical Impossibility)
* **`may be`** (The Structural Hypothesis / Analogy)
* **`wont be`** (The Rejected / Entropic Fossil)

This document maps the exact technical pathway to turn this architecture into an **actual, generative Language Model (LM)**.

---

## 2. The Dialectic State Machine (Formalizing the 4 Generative Rules)

```
       [SOLUTION]                                       [PROBLEM]
       "will be"                                       "can't be"
           ▲                                               ▲
           │                                               │
       (can be) ◄────────────── [ ACTIVE ] ──────────────► (is not)
           ▲ ╲                                           ╱ ▲
           │   ╲                                       ╱   │
(INCLUSIVE)│     PRODUCTIVE ───────────────> REDUCTIVE     │(EXCLUSIVE)
           │     ▲                             │           │
           │     │            [ IS ]           │           │
           │     │                             ▼           │
           │     CONSTRUCTIVE <───────────── REGRESS       │
           │   ╱                                       ╲   │
           ▼ ╱                                           ╲ ▼
       (is like) ◄────────── [ COUNTERACTIVE ] ──────────► (was like)
           │                                               │
           ▼                                               ▼
        "may be"                                       "wont be"
      [HYPOTHESIS]                                    [REJECTION]
```

### The 4 Definitive Generation Rules:

#### 1. Defining "CAN'T BE" (Problem / Boundary Impossibility):
> *"If you want to define IS as something that **can't be**, you must go through a **reductive** process using what it **was like** and **can be** opposing what it's like until **it's not**."*
* **Process**: Reductive ($-\upsilon, +\psi$, Active Exclusion).
* **Inputs**: Antecedent precedent (`was like`) $+$ Generative potential (`can be`).
* **Opposition**: Opposes structural resemblance (`is like`).
* **Terminal State**: Negation (`it's not`) $\to$ Locks the boundary as **`can't be`**.
* **LM Application**: Formal verification, constraint solving, debunking thermodynamic violations (e.g. proving a perpetual motion machine or infinite debt compound *can't be*).

#### 2. Defining "WILL BE" (Solution / Generative Actualization):
> *"If you want to define IS as something that **will be**, you must go through a **productive** process using what **is not** and **is like** opposing what it was like until **it can be**."*
* **Process**: Productive ($+\upsilon, +\psi$, Active Inclusion).
* **Inputs**: Negative boundary (`is not`) $+$ Structural invariant (`is like`).
* **Opposition**: Opposes historical inertia and debt baggage (`was like`).
* **Terminal State**: Dynamic potential (`can be`) $\to$ Materializes into **`will be`**.
* **LM Application**: Constructive synthesis, strategic planning, engineering design, policy actualization.

#### 3. Defining "WONT BE" (Rejection / Entropic Decay):
> *"If you want to define IS as something that **wont be**, you must go through a **regressive** process using what **it's not** and what **it's like** to oppose what it **can be** until it **was like**."*
* **Process**: Regressive ($-\upsilon, -\psi$, Counteractive Exclusion).
* **Inputs**: Negation (`it's not`) $+$ Analogous comparison (`it's like`).
* **Opposition**: Opposes generative potential (`can be`).
* **Terminal State**: Fossilized trace (`was like`) $\to$ Deprecates path as **`wont be`**.
* **LM Application**: Risk mitigation, sunsetting obsolete systems, identifying stranded assets and dead paradigms.

#### 4. Defining "MAY BE" (Hypothesis / Analogical Exploration):
> *"If you want to define IS as something that **may be**, you must go through a **constructive** process using what it **can be** and **was like** until it **is like**."*
* **Process**: Constructive ($+\upsilon, -\psi$, Counteractive Inclusion).
* **Inputs**: Open potential (`can be`) $+$ Past precedent (`was like`).
* **Terminal State**: Invariant morphism (`is like`) $\to$ Establishes exploratory model as **`may be`**.
* **LM Application**: Scientific theorizing, cross-domain metaphor translation, philosophical discovery.

---

## 3. The 3 Implementation Pathways for an Actual LM

### Pathway A: Native Micro-LM (Trained from Scratch)
* **Scale**: 50M – 125M parameters.
* **Architecture**:
  * Token Embeddings tied to AEC Dictionary Invariant Anchors.
  * 6 to 12 Dialectic Transformer Blocks:
    - 42-Head Polytropic Attention ($(7 \times 6)$ matrix).
    - 4-Quadrant FFN (Productive, Reductive, Regressive, Constructive sub-networks).
  * Polyhedral Generation Head predicting next tokens conditioned on target modal trajectory (`will be`, `can't be`, `may be`, `wont be`).
* **Training Corpus**: AEC Dictionary + VFT Papers + Australian Hansard + Selected Public Domain Philosophy/Science.
* **Pros**: 100% mathematically pure, zero black-box weights, fully interpretable.

### Pathway B: Dialectic Adapter over Open-Weight Base Model (Recommended Fast Path)
* **Scale**: 1B – 3B parameters (e.g. LLaMA-3.2-1B, SmolLM-1.7B, or Gemma-2-2B).
* **Architecture**:
  * Freeze base linguistic layers (grammar, syntax, general vocabulary).
  * Insert **Polytropic Dialectic Routing Layers** into the attention and MLP feed-forwards.
  * Train the routing layers on semantic hexads and dialectic transition rules.
* **Pros**: Instantly fluent English, low compute requirements, can be trained on a single local GPU in hours.

### Pathway C: Polyhedral Guided Beam Search (Zero-Training Inference Engine)
* **Scale**: Any existing LLM (local or API).
* **Architecture**:
  * The $(7 \times 6 + n)$ Polytrope operates as a real-time **Logit Steerer / Decider**.
  * At each generated token or sentence, the 4 dialectic rules filter candidate continuations.
  * Shearing paths are rejected; only paths moving toward the target modal state (`will be`, etc.) are permitted.
* **Pros**: Immediate deployment, zero training compute.

---

## 4. Phase-by-Phase Roadmap to Deliver Pathway A/B

### Phase 1: Dialectic State Machine Engine (`src/dialectic_engine.py`)
- [ ] Formalize the 4 generation transition functions in PyTorch.
- [ ] Build the state transition matrix mapping input state $\to$ operator $\to$ terminal state.
- [ ] Implement transition validation checks.

### Phase 2: Generative Decoder Layer (`src/generative_polytrope.py`)
- [ ] Implement causal masked attention across the 42 cells.
- [ ] Implement the 4-Process FFN blocks (Productive, Reductive, Regressive, Constructive).
- [ ] Add the $(\upsilon, \psi, z, \vec{\theta}_{xyz})$ coordinate head to output tokens.

### Phase 3: Tokenizer & Corpus Assembler (`src/dataset_builder.py`)
- [ ] Ingest the 69 AEC Invariants and 374 aliases.
- [ ] Assemble training pairs paired with their dialectic transition labels.
- [ ] Tokenize with HuggingFace Byte-Pair Encoding (BPE).

### Phase 4: Training & Comparative Benchmarking (`src/train_lm.py`)
- [ ] Train dialectic generation loop.
- [ ] Benchmark generation: Compare standard LLaMA/GPT outputs vs. Polytrope Dialectic outputs on complex reasoning problems.
- [ ] Verify zero-hallucination boundary enforcement.
