# Document Templates by Layer: Slot Definitions

Four typed templates for canonical document generation. Each template is a structured catch-net thrown at a cluster of retrieved fragments. The AI fills the slots from fragment content only. Empty slots are gaps, not failures: an empty slot is a signal that the cluster did not contain that information, which is itself useful data about what needs to be written.

The templates are ordered from most constrained to least. Axiom is the tightest because the content it holds is the most stable. Program is the loosest because applied analysis varies by subject.

---

## Template 1: Axiom

An axiom document holds one irreducible claim that nothing else in the corpus derives from. It takes no inputs from other documents and returns a truth value or a defined quantity when applied to a situation. If the document needs to reference another document to make its claim coherent, the claim is not an axiom, it is a concept.

Axiom documents are the most stable things in the corpus. They should change the least. If an axiom document is being revised frequently, it was mislabelled.

---

**[AXIOM TITLE]**
A short noun phrase naming the irreducible principle. Not a sentence. Not a question. The name is the stable identifier.

**Cluster:** [cluster label from vector DB]
**Coordinate:** (υ, ψ) [attractor projection of the cluster centroid]
**Zone:** [nearest zone anchor]
**Layer:** Axiom
**Depends on:** None
**Required by:** [list of concept documents that import this axiom — filled after the corpus is mapped]

---

**Statement**
One sentence only. The axiom in its most compressed form. If it cannot be stated in one sentence, it is not an axiom. The reconstruction prompt fills this from the definition-layer fragments. If no single fragment yields a one-sentence statement, the tightest definition fragment is used and compressed.

**Precision terms**
Every load-bearing word in the Statement that could be misread gets one line of definition here. Not prose paragraphs, one line per term. The goal is to close every gap that would let the Statement mean something it does not mean.

Format:
[term]: [definition in one clause]

**Boundary**
What this axiom does not cover. Stated as one or two sentences maximum. This slot prevents the axiom from being over-applied to situations it was not designed for. If the fragments do not contain explicit boundary conditions, this slot is filled by inferring the complement: what would need to be true for this axiom not to apply.

**Application form**
The operational version of the statement: given an input X, the axiom returns Y. This is not an example. It is the function signature. It states what you feed in and what you get out, without specifying a particular case.

Format:
Input: [what is fed to the axiom]
Operation: [what the axiom does to it]
Output: [what is returned]

**Cross-references**
Links to concept documents that use this axiom as a foundation. This slot is empty at creation and filled progressively as the corpus is mapped.

---

## Template 2: Concept

A concept document holds one framework, tool, or analytical structure built from one or more axioms. It has attributes (what it contains) and methods (what it can do). It is the object layer of the semantic programming architecture.

Concept documents change occasionally as the framework matures. When a concept document changes, every program document that instantiates it may be affected. That cascade is correct behaviour, not a problem.

---

**[CONCEPT TITLE]**
A short noun phrase naming the framework or tool.

**Cluster:** [cluster label]
**Coordinate:** (υ, ψ)
**Zone:** [nearest zone anchor]
**Layer:** Concept
**Depends on:** [list of axiom documents this concept is built from]
**Required by:** [list of program documents that instantiate this concept]

---

**Function**
One to three sentences stating what this concept does and why it exists. Not what it is made of, what it does. This slot answers the question: if you had this concept available, what could you do that you could not do without it.

**Construction**
How the concept is built from its axioms. This section names each axiom dependency explicitly and states how they combine to produce the concept. If the concept has attributes (named internal components), they are listed here with one-line definitions. If the concept has sub-concepts inside it, they are named and cross-referenced, not re-explained.

Format:
Built from: [axiom 1], [axiom 2], ...

Attributes:
[attribute name]: [one-line definition]
[attribute name]: [one-line definition]

**Methods**
What operations this concept can perform. Each method takes inputs, runs a defined procedure, and returns an output. Methods are where the functional layer (axioms) gets wrapped into the object layer (concept). A method that internally calls an axiom states that call explicitly.

Format per method:
[Method name]
Input: [what is fed in]
Calls: [which axioms are invoked internally]
Procedure: [what steps are run, stated concisely]
Output: [what is returned]

**Boundary**
What this concept does not cover. What would cause it to return an invalid result. What it should not be applied to. This slot prevents concept over-extension, the error of applying a framework to a domain it was not designed for.

**Known failure modes**
Situations where the concept produces a misleading output if applied naively. These come from program-layer experience: cases where the concept was applied and gave a result that looked valid but was wrong. This slot is empty at creation and filled as program documents accumulate.

**Cross-references**
Axioms this concept depends on (already listed above but linked here for navigation).
Sibling concepts at the same layer that interact with this one.
Idiom documents that describe how this concept composes with others.
Program documents that demonstrate this concept applied.

---

## Template 3: Idiom

An idiom document holds a named, recurring pattern for composing two or more concepts. It is the design pattern layer. An idiom does not define new concepts and does not contain new axioms. It names a way of wiring existing things together that has proven useful enough to be worth recording as a reusable pattern.

An idiom document exists because the same composition kept appearing in multiple program documents. When you find yourself writing the same cross-concept wiring for the third time, extract it as an idiom and reference it.

---

**[IDIOM TITLE]**
A short name for the pattern. Should be evocative enough to be memorable. The Fake Maximiser is an idiom name. The Helixis Bait-Cover-Intent structure is an idiom name.

**Cluster:** [the boundary cluster where two concept clusters meet]
**Coordinate:** (υ, ψ) [the midpoint between the two concept coordinates]
**Layer:** Idiom
**Composes:** [concept A] + [concept B] (+ [concept C] if applicable)

---

**The pattern**
A two to four sentence description of what this composition does that neither concept can do alone. This slot answers: why does this pairing exist as a named thing rather than just being implicit in the program that uses it.

**When to apply**
The conditions under which this idiom is the right tool. Stated as recognisable triggers: if you encounter situation X, this idiom applies. Two to four trigger conditions maximum. If there are more, the idiom is too broad and should be split.

**When not to apply**
The conditions that look like triggers but are not. The failure mode of over-applying this idiom. This slot is the most important part of an idiom document because idioms are pattern-matched by analogy, which means they get applied to superficially similar situations that are actually different.

**Wiring specification**
The exact composition: which method of concept A feeds into which attribute or method of concept B, and in what order. This is the implementation spec. A program document that uses this idiom follows this wiring exactly and does not need to re-derive it.

Format:
Step 1: [call method X of concept A with input Y]
Step 2: [feed output of step 1 into attribute Z of concept B]
Step 3: [call method W of concept B]
Output: [what the composed pair returns]

**Worked example**
One concrete case where this idiom was applied correctly. Names the specific program document it came from. Shows the inputs, the wiring steps, and the output. This is the only place in the template hierarchy where a specific case is required rather than optional.

**Cross-references**
The two or more concept documents this idiom bridges.
Program documents that use this idiom (filled progressively).

---

## Template 4: Program

A program document holds one applied analysis. It instantiates concepts, calls axioms, and produces a result. It is the highest layer and the most numerous type of document. Most of the 1,300 files in the corpus are program documents, many of which restate the same concepts and axioms in passing before getting to their actual subject.

Program documents are the most disposable type. Their value is in the result they produce and the demonstration they provide. When the axioms and concepts they depend on change, program documents may need to be re-run, not revised. A program document that needs significant prose revision when an axiom changes has failed to separate its instantiation from its source material.

---

**[PROGRAM TITLE]**
A short phrase naming the subject of analysis. Should include the subject and the question being asked. "Albanese Government: υψ Coordinate Audit Q2 2026" is a program title. "Some thoughts on Albanese" is not.

**Cluster:** [the concept cluster this analysis primarily draws from]
**Coordinate:** (υ, ψ) [the result coordinate of this specific analysis, not the cluster centroid]
**Zone:** [nearest zone anchor for the result]
**Layer:** Program
**Instantiates:** [list of concept documents used in this analysis]
**Calls:** [list of axiom documents called directly]
**Uses idioms:** [list of idiom documents applied]

---

**Subject**
One sentence naming exactly what is being analysed. No background, no context, no history. Just the subject.

**Question**
The specific question this program is designed to answer. Not a general question about the subject. The precise analytical question that the instantiated concepts will resolve.

**Setup**
The minimum context required for the analysis to be interpretable by someone who knows the framework but does not know the subject. This slot is the only place where background information belongs. It should be as short as possible. If the subject is already well-known within the corpus (a recurring actor or case), this slot may be empty and replaced with a cross-reference to the subject's own program documents.

**Analysis**
The main body. This section follows the structure of the primary concept being instantiated. If the Convergence Test is the primary concept, the analysis follows the Convergence Test method specification exactly. If the υψ coordinate scoring is the primary concept, the analysis follows that method. The analysis does not invent its own structure. It runs the method.

For each concept instantiated:
[Concept name]
Input fed in: [what was supplied]
Method called: [which method]
Intermediate result: [what the method returned before composition with other concepts]

**Result**
The output of the analysis. Stated as a coordinate, a verdict, a score, or whatever the primary concept's output format specifies. One section only. No hedging, no qualifications inside the result statement. Qualifications belong in the Boundary section below.

Format:
Coordinate: (υ, ψ)
Zone: [nearest anchor]
Verdict: [plain language statement of what the coordinate means for this subject]

**Boundary**
What this analysis does not cover. Time bounds if applicable. Data limitations. Assumptions made in the setup that, if false, would change the result. This slot is where honest uncertainty lives. It does not weaken the result. It defines the conditions under which the result holds.

**Cross-references**
Other program documents on the same subject (longitudinal comparison).
Program documents on related subjects (comparative analysis).
The concept and axiom documents this program drew from.

---

## How templates interact with the reconstruction prompt

The reconstruction prompt receives sorted fragments and a document type tag. The document type tag selects which template to use. The template slots become the section headers of the reconstruction pass. The AI fills each slot from the fragments that belong in it, based on the linguistic type tags assigned by spaCy.

Mapping of spaCy types to template slots:

definition fragments fill: Statement (axiom), Construction (concept), The pattern (idiom), Subject/Question (program)
assertion fragments fill: Precision terms (axiom), Function (concept), Wiring specification (idiom), Analysis (program)
conditional fragments fill: Boundary and Application form (axiom), Methods and Boundary (concept), When to apply / When not to apply (idiom), Boundary (program)
example fragments fill: nothing in axiom, Known failure modes (concept), Worked example (idiom), Setup and Analysis body (program)

Any fragment that does not map cleanly to a slot is a bridge sentence candidate. It likely belongs to a different cluster and should be extracted as a cross-reference rather than forced into the current document.

---

## The percolation mechanic: how documents surface automatically

After every reconstruction pass, the pipeline runs a coverage scan across the full vector space. For each cluster it computes:

Internal variance: how spread out the fragments are within the cluster.
Canonical coverage: whether a canonical document exists near the cluster centroid.
Fragment density: how many fragments are in the cluster.

The next document to generate is always the cluster with the highest fragment density and no canonical document near its centroid. That cluster represents the largest body of content in the corpus that has not yet been collapsed into a canonical form. It is the largest unmapped topic.

This is the percolation mechanic. Documents do not get generated in any order a human chooses. They surface in order of how much unorganised content exists on each topic. The corpus organises itself by weight. The heaviest unmapped clusters resolve first, and as they resolve, their fragments stop being noise in adjacent clusters, which allows those adjacent clusters to resolve more cleanly in subsequent passes.

The end state is a corpus where every cluster has a canonical document, every canonical document fills a template, and the templates form a navigable hierarchy from axiom through program. The 1,300 files do not disappear. They become the sourced evidence base for the canonical layer above them, correctly typed and cross-referenced rather than flat and redundant.
