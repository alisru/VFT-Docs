# Semantic Programming: An Architecture for Concept-Oriented Documentation

A standards document for organising a knowledge corpus as if it were a software system. Every OOP best practice is mapped to a semantic equivalent, so that ideas, axioms, idioms, and frameworks behave like functions, classes, namespaces, and programs — reusable, deduplicated, and composable.

## 0. The core premise

A knowledge base is a codebase. The 1,300-file problem is a refactoring problem: a large body of working logic with massive duplication, no clear module boundaries, and the same idea reimplemented inline in a hundred places. The fix is the same fix a senior engineer applies to legacy code. Extract the repeated logic into named, single-source units. Reference them everywhere instead of restating them. Let composition do the work that copy-paste was doing.

The unit of meaning is the **byte**: the smallest indivisible piece of semantic content that cannot be split without losing its meaning. Everything above it is built by composition.

## 1. The type hierarchy (what maps to what)

The mapping is close to one-to-one with object-oriented programming, with a functional layer underneath it, exactly as real software is built.

**Byte** maps to a single irreducible semantic primitive. The smallest meaningful token in your system. Not a word necessarily, but the smallest unit of meaning that has a stable definition. Example: a single coordinate value on the υ axis. It has a type and a value and nothing else.

**Function** maps to an axiom or a pure operation. Stateless, takes inputs, returns an output, never mutates itself, callable from anywhere. The υ scoring rule is a function: feed it an action, it returns a coordinate. The axiom does not change based on what you pass it.

**Variable** maps to a defined term whose value is fixed within a context but can differ across contexts. A named placeholder.

**Class** maps to a concept or framework. It bundles related state (definitions, parameters) with the methods that operate on that state. The Convergence Test is a class. The Qqci tensor is a class. It has attributes and it has callable behaviour.

**Method** maps to an operation a concept can perform on itself or its inputs. A class wraps a function and binds it to the class's own context. The Convergence Test's "score this actor" is a method that internally calls the υ and ψ axiom functions but packages them with the test's own state and rules.

**Instance / Object** maps to a specific applied case. "Albanese evaluated at (υ -1.2, ψ +0.4)" is an instance of the Convergence Test class. The class is the template, the instance is one run of it carrying its own data.

**Interface / Abstract type** maps to a primitive or a contract that several concepts must satisfy. It defines what something must do without saying how. "Any moral coordinate must return a value between +2 and -2" is an interface. Both υ and ψ implement it.

**Inheritance** maps to specialisation. One concept extends another, inheriting its structure and adding to it. VFT / Questoscrapy is the parent; the current Qqci system inherits from it and overrides parts.

**Composition** maps to a concept that contains other concepts as parts. The 42-Structure is composed of seven planes and three axes; it holds them, it is not a subtype of them. Composition is preferred over inheritance here for the same reason it is in code: it avoids brittle hierarchies.

**Idiom** maps to a design pattern. A named, recurring way of wiring concepts together that has proven useful. Not a concept itself but a repeatable assembly. The Fake Maximiser is an idiom: a standard way of composing the coordinate system with an actor's stated position to expose a gap.

**Namespace / Module** maps to a domain folder. A named collection of related concepts that prevents naming collisions and groups things that change together. The moral-coordinate namespace holds υ, ψ, the zone anchors, and the inversion warning. Biblical-philology is a separate namespace.

**Package / Library** maps to a whole framework released as a unit. The Psochic Hegemony system is a package: many namespaces shipped together with a coherent public interface.

**Program / Script** maps to an applied output. A document that instantiates classes, calls functions, and produces a result. Every analysis you have written is a program: the housing model, the Albanese spread, a Convergence run. These sit at the top and consume everything below.

**Import / Dependency** maps to an explicit reference. A program or concept declaring "I depend on concept X." This is the single most important rule of the whole system and gets its own section.

## 2. The three layers

Real software is layered, and so is this. Top depends on bottom, never the reverse.

**Functional layer (bottom).** Axioms, primitives, pure logical operations. Stateless. No incoming dependencies on anything above. These are the most stable things in the system and should change the least. If an axiom changes often, it is not an axiom.

**Object layer (middle).** Concepts, frameworks, analytical tools. Stateful. Built from the functional layer. These carry parameters and have methods. They change occasionally as the framework matures.

**Program layer (top).** Applied analyses and outputs. Built by instantiating the object layer and calling the functional layer. These are the most numerous and the most disposable. Most of your 1,300 files live here, and most of the duplication is here.

The idioms sit at the seams between layers: named patterns for wiring a function into a method, or composing two classes into a program.

## 3. The dependency rule (the one that matters most)

Dependencies point one direction only: from specific to general, from application to axiom. A program imports a concept. A concept imports an axiom. An axiom imports nothing.

If you ever find a dependency pointing the wrong way, where an axiom needs to know about a program that uses it, you have a design error. The axiom is not really an axiom, or the program is doing something that belongs lower in the stack.

This rule is what makes deduplication permanent rather than temporary. As long as dependencies only flow downward, you can change any program without touching the concepts it uses, and change any concept without touching the axioms it rests on. The single source of truth stays single.

A practical test: when you edit a document, ask what else must change as a result. If editing a concept forces you to edit an axiom, the layering is wrong. If editing an axiom forces you to edit fifty programs, that is correct and expected, because they all depend on it. Dependencies cascade downward-to-upward in effect, never upward-to-downward in reference.

## 4. The encapsulation rule

Each unit owns its own definition. A concept document holds everything true about that concept and nothing about any other concept. When a concept needs another concept, it references it by name, it does not restate it.

The violation to hunt for: a document that re-explains the υ axis in passing before getting to its actual point. That re-explanation is duplicated state. It should be deleted and replaced with a reference to the canonical υ document. The moment the υ definition changes, every document that restated it goes stale, but every document that referenced it stays correct automatically.

This is the entire value proposition. Encapsulation plus the dependency rule equals a corpus that updates itself by reference.

## 5. The single-responsibility rule

Each document does one thing. One concept per concept-document. One axiom per axiom-document. One analysis per program-document.

A document that covers three concepts is three documents wearing a trenchcoat. Split it. The clustering pass will surface these, because a single file will show up pulling toward three different cluster centres at once. That tension is the signal to split.

The atomic-note discipline from tools like Obsidian is the same principle arrived at from the other direction: one idea per note, link rather than duplicate. The difference here is that you are deriving atomicity from an existing messy corpus rather than imposing it on new notes as you write them.

## 6. Naming and namespacing

Names must be unique within a namespace and stable over time. A concept's name is its public interface; if you rename it, every reference breaks, exactly like renaming a function in code.

Use the namespace to disambiguate. "Resonance" in the lyrical-plane namespace and "resonance" in some physical namespace are different symbols that happen to share a string. The namespace prefix keeps them apart. When you cite across namespaces, use the qualified name.

Reserve a stable identifier for each canonical unit that never changes even if the human-readable title does. This is the equivalent of a function keeping its address even when you rename the variable that points to it. Your Notion page IDs already do this; the doc system should too.

## 7. Versioning and state

Concepts have state and state changes over time. This is where the OOP mapping is genuinely complete rather than merely analogous: if running the Convergence Test across enough actors shifts what a given score means to you, then the class is mutating, and that mutation is real state.

Handle it the way code handles it. The canonical document is the current state. Git history is the version log. Every revision commits to the same file path so the full lineage is preserved without cluttering the namespace with v1, v2, v3 files. You already settled this convention for the artifact library, and it is exactly right for the concept layer too.

Axioms, by contrast, should be effectively immutable. If an axiom needs versioning because it keeps changing, that is the tell that it was a concept misfiled as an axiom.

## 8. The build pipeline (how to get from 1,300 files to this)

This is the refactor, run once, then maintained.

**Step one, inventory.** Embed every file into a vector and cluster by semantic similarity. This surfaces the natural module boundaries without you imposing them. The clusters become candidate namespaces.

**Step two, deduplicate within clusters.** Inside each cluster, find near-identical content and merge it. Global deduplication across all 1,300 is intractable and meaningless; local deduplication within a cluster of related files is fast and correct.

**Step three, stratify each cluster by layer.** Within a namespace, sort documents into axiom-level, concept-level, and program-level. The axiom and concept documents become canonical nodes. The program documents become leaves that reference them.

**Step four, extract and reference.** Wherever a program restates a concept, cut the restatement and replace it with a reference. This is the step that collapses the corpus. A large fraction of your total volume is almost certainly restated definitions that can become one-line references.

**Step five, wire dependencies.** Make every reference explicit and directional. Now the corpus is a graph with the dependency rule enforced, and it maintains itself.

## 9. Where the analogy stops being literal

Honesty about the seams, because the orthogonality you raised is real.

OOP inheritance assumes a tree: every class has at most one chain of ancestors in single-inheritance languages. Your concepts are not a tree, they are a tensor field. The Q-planes are orthogonal axes, not parent and child. Two axioms can be completely independent while both being foundational.

OOP handles this through composition and interfaces rather than inheritance, which is why the standards above lean on composition as the default and treat inheritance as the rare case. The 42-Structure composes seven planes; it does not inherit from them. This is the same advice every modern OOP guide gives ("prefer composition over inheritance"), and it happens to be exactly what an orthogonal, tensor-shaped knowledge base requires. The analogy holds precisely because OOP best practice already abandoned strict inheritance trees for the same structural reasons your material has.

The one place it is not literal: code executes, documents are read. A program in this system does not run itself; you run it by reading and applying it. So this is OOP as an organising discipline, not as an execution model. The payoff is in the structure and the maintenance properties, not in automation, unless you later wire the functional layer into actual callable tools, at which point parts of it could genuinely execute.
