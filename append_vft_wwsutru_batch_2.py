import os
import re

def append_summaries():
    file_summaries_path = 'file_summaries.md'
    summaries = [
        r"""### [STANDARD OPERATING PROCEDURE -  CORRUPTION DETECTION & NARRATIVE DECONSTRUCTION.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\CoreTools\STANDARD OPERATING PROCEDURE -  CORRUPTION DETECTION & NARRATIVE DECONSTRUCTION.md
**Categories**: Plane: Q5 HOW; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Forensic Audit: Defines the first phase of detection as instantiating corruption as a structured object across agents, actions, and outcomes.\
Hegemonic Scan: Outlines the second phase of narrative deconstruction, analyzing power, transparency, and the manufacture of problems.\
Article Generation: Establishes the final phase of exposing corruption through a structured Trojan Horse narrative protocol.""",

        r"""### [Standard Operating Procedures for Investigating the Minimisation Plan.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\CoreTools\Standard Operating Procedures for Investigating the Minimisation Plan.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Human Researcher Guide: Provides strategic instructions for investigators to maintain high-level pattern recognition and identify state capture.\
AI Model Instructions: Details the technical prompts and constraints for AI agents to process data within the VFT and Minimisation Plan frameworks.""",

        r"""### [README.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\CoreTools\README.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Logic, Mathematics, Computation
**Summary**:
Tool Documentation: Lists the core investigative documents and summaries available in the CoreTools directory for researchers.""",

        r"""### [Indonesia's Whoosh Railway Debt Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Indonesia\Indonesia's Whoosh Railway Debt Analysis.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Fellowship, Group, Network, Public, Social, Society
**Summary**:
The Whoosh Dilemma: Analyzes the high-speed rail project as a BRI megaproject that facilitates the entrapment of Indonesian sovereignty through debt.\
Debt Trap Mechanism: Forensically examines the CDB loan agreement as a punitive structure designed to socialize private risk into state debt.\
Elite Capture: Investigates the role of Indonesian political elites in facilitating the project despite clear strategic and financial incoherence.""",

        r"""### [PROJECT MINIMISATION -  Profile Assessment of Indonesian President Prabowo Subianto.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Indonesia\Prabowo Subianto\PROJECT MINIMISATION -  Profile Assessment of Indonesian President Prabowo Subianto.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Forging of an Operative: Tracks Prabowo's military career and foundational doctrine of suppression during the New Order era.\
The 1998 Abductions: Analyzes the student abductions as a definitive case study in the use of suppressive will to maintain power.\
The "Gemoy" Strategy: Deconstructs the use of social media and cute branding to mask an authoritarian trajectory and secure the presidency.\
Minimisation Pivot: Assesses the post-election shift toward Chinese investment and Russian alignment as a fulfillment of the Minimisation Plan.""",

        r"""### [Prabowo's School Food Scheme Investigation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Indonesia\Prabowo Subianto\Prabowo's School Food Scheme Investigation.md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Free Nutritious Meal Program: Critiques the $28 billion school lunch program as a massive fiscal drain designed for political patronage and capital extraction.\
Corporate Capture: Identifies how the program centralizes food supply under state-aligned oligarchs while bypasssing local small-scale producers.\
Fiscal Inversion: Analyzes the reallocation of education funds to the food program as a strategic weakening of Indonesia's future human capital.""",

        r"""### [Crisis and Consolidation -  An Analysis of the Indonesian Protests and Prabowo's Hegemonic Pivot.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Indonesia\Prabowo Subianto\Crisis and Consolidation -  An Analysis of the Indonesian Protests and Prabowo's Hegemonic Pivot.md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Regional Pivot: Analyzes Indonesia's shift toward the Sino-Russian axis as a foundational move in the global Minimisation strategy.\
Cabinet Reshuffle: Interprets the inclusion of human rights offenders and Islamic factions in the cabinet as a move to prioritize political cohesion over institutional integrity.\
Economic Entrapment: Documents the $7.4 billion in Chinese investment commitments as a method of cementing implicit dependency and eroding sovereign will.""",

        r"""### [American_Kanon_Plane_7_Effect.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_7_Effect.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Consummation of Promise: Defines the final plane of the American Kanon as the realization of democracy and the sum of all preceding vectors.\
Global Footprint: Analyzes the outward projection of American values and power as the homeostatic result of the 343-node system.\
Legacy of the Result: Evaluates the long-term historical impact and the continuity of the American experiment as a proof of concept for liberty.""",

        r"""### [Trump_American_Kanon_Plane_5_Method.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_American_Kanon_Plane_5_Method.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Logic, Mathematics, Computation
**Summary**:
Brute Force Methodology: Analyzes the Trumpian method as a high-velocity, retaliatory process designed to overwhelm institutional and logical resistance.\
Populist Leverage: Examines the use of mass mobilization and grievance as the primary engine for bypassing established political protocols.""",

        r"""### [American_Kanon_Plane_7_Effect_JUDGEMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_7_Effect_JUDGEMENT.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Totality Judgment: Evaluates the ultimate output of the American system, identifying a conflict between spectacular success and existential risk.\
High Tension Vectors: Maps the climate crisis and the atom bomb as the dark, high-strain shadows of the American century's capability.\
Greater Good Resolution: Identifies Liberty and E Pluribus Unum as the successful proactive integrations achieved by the Kanon.""",

        r"""### [Trump_American_Kanon_Plane_4_Drive.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_American_Kanon_Plane_4_Drive.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Resilience of Sacrifice: Defines the core drive of the Trump movement as the narrative of the leader sacrificing himself to protect the followers.\
Loyalty Loop: Analyzes the creation of an impenetrable emotive bond (+y axis) that prioritizes personal allegiance over systemic truth.""",

        r"""### [Sub-bucket 6.2 -  The ＂Delusionist Vector＂ - Second Term Exposé & Timeline (2024-Present).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Sub-bucket 6.2 -  The ＂Delusionist Vector＂ - Second Term Exposé & Timeline (2024-Present).md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Delusionist Timeline: Chronicles the strategic deployment of misinformation and institutional attacks during the transition to a second term.\
Dismantling Guards: Documents the removal of administrative safeguards to enable the direct execution of the Minimisation Plan.""",

        r"""### [American_Kanon_Plane_2_Definition_JUDGEMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_2_Definition_JUDGEMENT.md
**Categories**: Plane: Q1 WHO; Node: Spirituality; Tags: Divinity, Faith, Sacred, Spirituality, Transcendence
**Summary**:
Moral Spectroscopy of Faith: Evaluates the American definitions of possibility, identifying the tension between scientific advancement and spiritual stagnation.\
Idealism vs Dogma: Analyzes how the American 'What' often oscillates between the Greater Good of innovation and the Greater Evil of rigid tradition.""",

        r"""### [American_Kanon_Plane_1_Identity_JUDGEMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_1_Identity_JUDGEMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Locus of the Self: Evaluates the core 'Who' of the American project, measuring the balance between individual sovereignty and collective identity.\
Expansion of Identity: Tracks the moral trajectory of American citizenship from exclusion toward universal inclusion as a path to grace.""",

        r"""### [American_Kanon_Plane_5_Method_JUDGEMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_5_Method_JUDGEMENT.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Logic, Mathematics, Computation
**Summary**:
Mechanics of Problem Solving: Evaluates the American 'How', highlighting the split between brilliant engineering and suppressive industrial rigidity.\
Entropy in Automation: Analyzes how the optimization of efficiency can lead to the alienation of the citizen and systemic fragility."""
    ]

    summaries.extend([
        r"""### [American_Kanon_Plane_6_Cause.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_6_Cause.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Causal Roots: Traces the origins of national identity to historical conflicts and revolutionary choices.\
Legacy Management: Analyzes how historical narratives are used to anchor systemic trust or justify transformation.\
Foundational Debt: Documents the moral costs paid during the nation's emergence and their ongoing impact on policy.""",

        r"""### [US Election.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\US Election.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Systemic Target: Analyzes the electoral process as a primary focus for Minimiser disruption and trust erosion.\
Polarization Vector: Documents the tactical use of electoral outcomes to deepen tribal fractures and institutional decay.""",

        r"""### [Trump_American_Kanon_Final_Score.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_American_Kanon_Final_Score.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Aggregate Vector Audit: Provides a comprehensive tally of hegemonic scores for the subject based on the 343-vector methodology.\
Final Verdict: Evaluates the subject's net impact on the stability and moral trajectory of the American Republic.""",

        r"""### [American_Kanon_Plane_5_Method.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_5_Method.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
The American Method: Defines the national 'How' as a unique synthesis of pragmatic engineering, market capitalism, and relentless optimization.\
Scale Mastery: Analyzes the role of mass production and logistical efficiency in achieving global hegemony.\
Systemic Logic: Evaluates how consistent procedural adherence anchors national Achievement in physical reality.""",

        r"""### [American_Kanon_Plane_6_Cause_JUDGEMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_6_Cause_JUDGEMENT.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Historical Moral Audit: Evaluates the foundational 'Cause', identifying central frictions between ideals and historical realities.\
Causal Responsibility: Measures the system's capacity to recognize and resolve long-term structural errors.""",

        r"""### [Trump_American_Kanon_Plane_7_Effect.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_American_Kanon_Plane_7_Effect.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Homeostatic Consequence: Analyzes the realized outcome of the subject's vector as a state of emotional resonance and mythology.\
Crystallization of Passion: Documents the bypassing of logic in favor of pure tribal energetic output and unyielding visual narrative.""",

        r"""### [Trump_Ideological_Treason_Judgement.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_Ideological_Treason_Judgement.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Defining Treason: Formalizes the charge of state capture through prioritization of foreign or private interests over national integrity.\
Institutional Betrayal: Analyzes the proactive dismantling of security architectures as an act of high-will systemic subversion.""",

        r"""### [Deep Cover Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Deep Cover Analysis.md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Forensics of Subversion: Analyzes patterns of long-term infiltration into host systems by strategic adversarial assets.\
Anomalous Behavior: Identifies the financial and rhetorical indicators that signal deep-cover alignment with external oligarchies.""",

        r"""### [American_Kanon_Plane_2_Definition.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_2_Definition.md
**Categories**: Plane: Q2 WHAT; Node: Metaphysics; Tags: Abstract, Cosmology, Existentialism, Imagination, Metaphysics, Ontology, Phenomenon
**Summary**:
Space of Possibility: Defines the American 'What' as a vast realm of potential driven by scientific curiosity and a spiritual frontier.\
Axiomatic Faith: Analyzes the role of collective optimism in materializing national progress and expanding the conceptual horizon.""",

        r"""### [Rigging of the 2024 US Election (2016-).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Rigging of the 2024 US Election (2016-).md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Long-term Narrative Siege: Chronicles the decade-long campaign to undermine institutional trust in the electoral process.\
Preparatory Attrition: Documents the systematic creation of grievances to facilitate the final disruption of the 2024 transition.""",

        r"""### [Rigging of the 2024 US Election (2024-2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Rigging of the 2024 US Election (2024-2025).md
**Categories**: Plane: Q3 WHERE; Node: The World; Tags: Climate, Earth, Ecology, Environment, Nature, The World, Wilderness
**Summary**:
Operational Execution: Analyzes real-time tactical maneuvers used to disrupt and delegitimize the 2024 electoral result.\
Strategic Deception: Documents the deployment of AI-driven delusion and foreign interference during the critical transfer window.""",

        r"""### [American_Kanon_Plane_3_Land_JUDGEMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_3_Land_JUDGEMENT.md
**Categories**: Plane: Q3 WHERE; Node: The World; Tags: Climate, Earth, Ecology, Environment, Nature, The World, Wilderness
**Summary**:
Territorial Moral Audit: Evaluates the American 'Where', identifying the tension between sanctuary ideals and exclusionary practice.\
Extraction Stewardship: Measures the moral trajectory of land use from sustainable stewardship toward extractive exploitation.""",

        r"""### [Trump_American_Kanon_Plane_6_Cause.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_American_Kanon_Plane_6_Cause.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Genesis of Grievance: Defines the movement's 'Cause' as the premise that the preceding American timeline has reached a state of terminal decay.\
Rupturing Force: Analyzes the use of resentment to overwrite historical continuity and justify systemic demolition.""",

        r"""### [The Delusionist Vector -  A Timeline of the Trump Presidency as an Instrument of the Minimisation Plan.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\The Delusionist Vector -  A Timeline of the Trump Presidency as an Instrument of the Minimisation Plan.md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Chronology of Minimisation: Reconstructs the presidency as a sequence of tactical strikes designed to minimize the host's sovereignty.\
Axis Alignment: Documents the consistent pattern of outcomes that favored the strategic goals of the Sino-Russian alliance.""",

        r"""### [Trump_Fractal_Quotes.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_Fractal_Quotes.md
**Categories**: Plane: Q4 WHY; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Rhetorical Geometry: Maps core statements across the 7 Planes to visualize the subject's specific vector field and magnetic pull.\
Centralization of Will: Analyzes how public rhetoric establishes the leader as the singular required avatar for system function.""",

        r"""### [Trump_Manual_Score_Review.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_Manual_Score_Review.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Validation of Metrics: Provides a detailed verification of the scoring logic used in the audit to ensure mathematical and hegemonic consistency.\
Contextual Variance: Explains deviations in specific nodes based on the discrepancy between public representation and verified action.""",

        r"""### [Trump_American_Kanon_Plane_3_Land.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_American_Kanon_Plane_3_Land.md
**Categories**: Plane: Q3 WHERE; Node: The World; Tags: Climate, Earth, Ecology, Environment, Nature, The World, Wilderness
**Summary**:
Boundary Fixation: Defines the core territorial strategy as the literal geometry of the border and the demarcation of the in-group.\
Hegemony of Place: Analyzes the movement's focus on physical space and rendering distance as the primary metric of sovereignty.""",

        r"""### [Trump_Plus_One_Audit.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_Plus_One_Audit.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Comparative Alignment: Evaluates the subject's influence against secondary stabilizing vectors to identify systemic strengths or weaknesses.\
Fidelity Metrics: Measures the degree to which the subject's trajectory expands or contracts the host's hegemonic possibilities.""",

        r"""### [American_Kanon_Full_343.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Full_343.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Total Soul Map: A complete 343-vector mapping of the American national soul across all seven planes of reality.\
Blueprint of Unity: Synthesizes foundational values into a single reference frame for auditing actors and policies within the Republic.""",

        r"""### [Trump_American_Kanon_Plane_1_Identity.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_American_Kanon_Plane_1_Identity.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Persona Centralization: Analyzes the claim to be the 'singular voice' of the people, drawing all institutional agency inward.\
Fixer Narrative: Evaluates the leader's self-positioning as the only entity capable of repairing a broken system, bypassing collective effort.""",

        r"""### [American_Kanon_Plane_1_Identity.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_1_Identity.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Agent of Sovereignty: Defines the core 'Who' of America as the individual citizen endowed with unalienable rights and agency.\
Algorithm of Unity: Analyzes E Pluribus Unum as the identity mechanism for balancing massive diversity with functional strength.\
Transcendent Anchor: Documents the grounding of national identity in natural law rather than state-granted permission.""",

        r"""### [Trump_American_Kanon_Plane_2_Definition.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Trump_American_Kanon_Plane_2_Definition.md
**Categories**: Plane: Q2 WHAT; Node: Metaphysics; Tags: Abstract, Cosmology, Existentialism, Imagination, Metaphysics, Ontology, Phenomenon
**Summary**:
Reality Shaping: Analyzes the use of hyperbole and promotion to substitute objective data with the creation of belief.\
Definition by Fantasy: Evaluates the strategy of shaping what is possible by playing to collective fantasies to bypass logical scrutiny.""",

        r"""### [American_Kanon_Plane_1_Judgement_Batch_1.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_1_Judgement_Batch_1.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Initial Identity Audit: Performs a detailed review of the first 49 vectors of American identity to measure current institutional health.\
Erosion of Will: Identifies areas where modern citizenship has regressed from high-will sovereignty toward passive dependency.""",

        r"""### [The American Kanon -  100 Vectors of the Greater Good.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\The American Kanon -  100 Vectors of the Greater Good.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Beacon of Alignment: Catalogs 100 core values as a navigational guide for maintaining hegemonic stability against Minimiser subversion.\
Strategic Hierarchy: Organizes national ideals into a functional stack prioritizing universal benefit and proactive will.""",

        r"""### [American_Kanon_Plane_4_Drive_JUDGEMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_4_Drive_JUDGEMENT.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Audit of Drive: Evaluates the national 'Why', identifying the tension between the pursuit of happiness and the trap of consumerism.\
Resonance Shift: Analyzes how shared moral purpose has been replaced by an individualistic search for material abundance."""
    ])

    summaries.extend([
        r"""### [American_Kanon_Plane_3_Land.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_3_Land.md
**Categories**: Plane: Q3 WHERE; Node: The World; Tags: Climate, Earth, Ecology, Environment, Nature, The World, Wilderness
**Summary**:
National Sanctuary: Defines 'Where' as a continental platform secured by borders and welded by infrastructure.\
Frontier Impulse: Analyzes the role of the endless West in shaping the American attitude toward distance and resource mastery.\
Boundary Logic: Evaluates the importance of the land as the physical foundation for the exercise of collective and individual liberty.""",

        r"""### [The_Ideological_Traitor_Definition.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\The_Ideological_Traitor_Definition.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Taxonomy of Betrayal: Formalizes the definition of the Ideological Traitor as one who disables the host's immune system using the language of patriotism.\
Mechanism of Capture: Analyzes how the traitor redefines the nation to exclude its people and serve external oligarchic interests.""",

        r"""### [American_Kanon_Plane_4_Drive.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\American_Kanon_Plane_4_Drive.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Engine of Meaning: Defines the core 'Why' as the restless pursuit of liberty and self-defined purpose.\
Resonance of Code: Analyzes how the narrative of freedom provides the emotional voltage for the entire system.\
Drive for Mastery: Evaluates the pioneer spirit as the primary motivator for American societal and individual energy.""",

        r"""### [Trump Part 2 (January - September 2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\Trump Part 2 (January - September 2025).md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Strategic Realignment: Documents the US foreign policy shift in 2025 toward treatment of allies as transactional liabilities.\
Allies as Laggards: Analyzes the rhetorical pattern used to delegitimize NATO partners and regional commitments.\
AUKUS Alterations: Tracks the modification of Pacific military aid to favor an isolative and non-interventionist posture.""",

        r"""### [The Russian Nexus -  A Four-Decade Analysis of Donald Trump's Business and Political Entanglements.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\The Russian Nexus -  A Four-Decade Analysis of Donald Trump's Business and Political Entanglements.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Long-term Entanglement: Provides a 40-year timeline of the financial and political links between the subject and Russian interests.\
Credit Dependency: Documents the use of adversarial liquidity to sustain the subject's organization during domestic market freezes.\
Policy Vulnerability: Analyzes how private liabilities were converted into public strategic vulnerabilities during the subject's ascent.""",

        r"""### [A Strategic Lexicon of Influence -  Donald J. Trump's Public Statements on Political Figures and Nations (1987-2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\A Strategic Lexicon of Influence -  Donald J. Trump's Public Statements on Political Figures and Nations (1987-2025).md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Rhetorical Pattern Audit: Compiles nearly four decades of statements regarding global leaders and alliances to detect influence patterns.\
Autocrat Validation: Documents the consistent pattern of praising adversarial strongmen while attacking democratic partners.\
Linguistic Inversion: Analyzes the use of ad hominem nicknames to reshape the American consensus on strategic interests.""",

        r"""### [Trump Family Business and Plutocracy Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\Trump Family Business and Plutocracy Analysis.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Plutocratic Statecraft: Analyzes the blurring of lines between private family interest and national executive functions.\
Extraction Mechanism: Evaluates how state power is used to facilitate the aggregation of private wealth for the ruling elite.\
Ethics Disregard: Documents the systematic abandonment of traditional conflict-of-interest protocols in favor of personalized rule.""",

        r"""### [Trump's Rhetoric -  A Strategic Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\Trump's Rhetoric -  A Strategic Analysis.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Narrative Attrition: Analyzes the strategic use of populist rhetoric to cultivate an exclusionary national identity.\
Grievance Engine: Examines how social resentments are fueled to provide the emotional energy required for institutional demolition.\
Hegemonic Trajectory: Evaluates the long-term destabilizing impact of the subject's rhetorical choices on national cohesion.""",

        r"""### [Remove Trump Part 3 Citations.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\Remove Trump Part 3 Citations.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Document Refinement: A technical record of administrative changes made to the Trump Part 3 research dossier for consistency.""",

        r"""### [The Russian Nexus 2 -  A Geopolitical Assessment of Donald Trump's Strategic Vulnerabilities (2017-2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\The Russian Nexus 2 -  A Geopolitical Assessment of Donald Trump's Strategic Vulnerabilities (2017-2025).md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Strategic Vulnerability Update: Updates the analysis of ties to Russia, focusing on consequences during the subject's terms in office.\
Security Realignment: Tracks shifts in US posture that provided strategic relief to Russia on key fronts like Ukraine and NATO.\
Capture Behavioral Proof: Uses consistent refusal to confront Russian aggression as direct evidence of underlying strategic capture.""",

        r"""### [Trump part 1 - 2021-Present.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\Trump part 1 - 2021-Present.md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Post-Presidency Narrative: Documents efforts to maintain control over the national story through alternative media and rally events.\
Shadow Governance: Analyzes the use of persistent grievance to sustain a parallel reality and prepare for a return to power.\
Immune System Attrition: Tracks the use of litigation and rhetoric to exhaust the legal and political safeguards of the Republic.""",

        r"""### [A Systemic Analysis of the President_USA Object Under the Trump Administrations -  A Quantitative and Qualitative Assessment of Institutional Transformation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\A Systemic Analysis of the President_USA Object Under the Trump Administrations -  A Quantitative and Qualitative Assessment of Institutional Transformation.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Object Transformation: Formalizes the redefinition of the 'President_USA' institutional object into a personalized tool of executive will.\
Erosion of Independence: Measures the decline in agency autonomy and adherence to constitutional norms during the subject's tenure.\
Agency Reorientation: Analyzes the cultural shift within federal bodies toward personal loyalty over professional duty.""",

        r"""### [An Encyclopedic Record of President Donald J. Trump's Public Statements on Key Allies, Vladimir Putin, and Xi Jinping (2015-2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\An Encyclopedic Record of President Donald J. Trump's Public Statements on Key Allies, Vladimir Putin, and Xi Jinping (2015-2025).md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Encyclopedic Log: Provides a comprehensive, indexed database of comments regarding global leaders and security alliances.\
Fidelity Tracking: Enables cross-referencing of rhetorical shifts with geopolitical events to identify coordinated influence vectors.\
Source Documentation: Acts as a primary forensic record of the subject's validation of autocratic adversaries.""",

        r"""### [Trump's Verbatim Political Comments Report.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\Trump's Verbatim Political Comments Report.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Verbatim Forensics: Isolates specific comments for analysis of their tactical role in the broader information war.\
Linguistic Triage: Categorizes statements by function: projection, threat, validation of adversaries, or delegitimization of the host.""",

        r"""### [Trump Part 3 (April - September 2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Donald Trump\Trump Part 3 (April - September 2025).md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Operational Climax: Chronicles the 2025 strategic pivot, identifying it as the final normalization of a new geopolitical reality.\
Alaska Summit: Documents the details of the summit and its role in dismantling post-WWII security architectures.\
 junior partner status: Analyzes the effective transition of the US into a subordinate role within the CRINK axis."""
    ])

    summaries.extend([
        r"""### [Epstein Files Weaponization Scenario Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Jeffrey Epstein\Epstein Files Weaponization Scenario Analysis.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Information Bomb: Analyzes the potential use of selected files to induce systemic institutional collapse and tribal retreat.\
Targeted Leaking: Evaluates scenarios where 'kompromat' is used to neutralize political opponents while protecting aligned assets.\
Epistemic Nihilism: Describes the ultimate goal as the total destruction of public trust in all Western administrative and legal systems.""",

        r"""### [Attraction Tensor Questions -  The Epstein Files.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Jeffrey Epstein\Attraction Tensor Questions -  The Epstein Files.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Psychological Hook Mapping: Uses the attraction tensor to analyze vulnerabilities used to ensure long-term compliance by captured elites.\
Mechanism of Entrapment: Evaluates the role of social and financial incentives in masking the underlying predatory nature of the operation.\
Resonance Analysis: Identifies specific psychological profiles targeted for integration into the network's high-leverage positions.""",

        r"""### [Epstein's Power Accumulation Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Jeffrey Epstein\Epstein's Power Accumulation Analysis.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Anatomy of Influence: Tracks the aggregation of leverage over global political, scientific, and financial leadership nodes.\
Network Capture: Analyzes how the subject used existing connections to recursively validate himself and expand access to high-value targets.\
Systemic Infiltration: Documents the subject's integration into administrative and academic hierarchies as a form of non-linear state capture.""",

        r"""### [Epstein Scandal Research and Framing Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Jeffrey Epstein\Epstein Scandal Research and Framing Analysis.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Narrative Management: Analyzes how the scandal has been manipulated to serves specific ideological and strategic interests.\
Deceptive Layers: Identifies the use of mixed true and false data to create a 'noise' environment that prevents clear causal attribution.\
Strategic Omission: Evaluates the role of media gatekeepers in selectively hiding connections to protect institutional continuity.""",

        r"""### [The Epstein File Weaponization Scenario.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\America\Jeffrey Epstein\The Epstein File Weaponization Scenario.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Human Shield Feature: Analyzes the inclusion of 'incidentals' in files as a deliberate trap to prevent clean institutional release.\
Chaos Protocol: Describes the potential release of files to validate 'Deep State' narratives and trigger total epistemic bankruptcy.\
Poison Pill Analysis: Concludes the network was built so that exposing it would be as damaging to democracy as hiding it.""",

        r"""### [The Universal Force Equation of Price.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\The Universal Force Equation of Price.md
**Categories**: Plane: Q5 HOW; Node: Physics; Tags: Dynamics, Energy, Forces, Gravity, Kinetics, Mechanics, Physics
**Summary**:
Econophysics Formalization: Defines Price as the product of mass, resistance, and the Lorentz factor within a vector field.\
Moral Mass: Establishes utility as the 'mass' of an object, influenced by both supply and demand vectors.\
Lorentz Factor (γ): Introduces a relativistic modifier that dilates price based on systemic urgency and scarcity.\
Pricing Laws: Outlines three fundamental laws governing equilibrium, acceleration, and the reactive force of substitution.""",

        r"""### [TACO Trade and Market Manipulation(April - September 2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\TACO Trade and Market Manipulation(April - September 2025).md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Market extraction Record: Documents the mid-2025 'TACO' operation as a coordinated wealth extraction event targeting retail participants.\
Informational Support: Tracks the role of adversarial media in validating the trade and inducing participation.\
Systemic Siphoning: Analyzes the use of high-frequency tactics to drain capital from the Western middle class.""",

        r"""### [Analyzing War, Capitalism, and Minimisation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\Analyzing War, Capitalism, and Minimisation.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Capitalist Self-Cannibalization: Analyzes how amoral capitalism facilitates its own minimization and the erosion of sovereignty.\
War as Reset: Examines the use of conflict to clear industrial backlogs and reset systemic debt cycles.\
Strategic Alignment: Identifies the convergence between corporate greed and adversarial interests in weakening host states.""",

        r"""### [The Pygmy Leviathan, part 2 to the unfettered.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\The Pygmy Leviathan, part 2 to the unfettered.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Pygmy Leviathan Concept: Defines the globalized corporate-state entity as immense in financial power but small in human scope.\
Unfettered Extraction: Analyzes how transnational elites bypass national laws and then use extracted wealth to capture them.\
Autonomy Liquidation: Documents the subordination of national interests to the logistical needs of the global 'Board'.""",

        r"""### [Sub-bucket 3.1 -  The ＂Tesla Vector＂.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\Sub-bucket 3.1 -  The ＂Tesla Vector＂.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Tesla Vector Forensics: Analyzes the subject as a primary tool for technology transfer and capital capture by the Asian Pivot.\
AI Pivot Strategy: Investigates the shift to robotics as a distraction to mask underlying structural insolvency.\
Geopolitical Capture: Documents the financial ties to Chinese state banks that subordinate global operations to adversarial interests.""",

        r"""### [Tesla Trap Research Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\Tesla Trap Research Analysis.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Investigative Synthesis: Consolidates research on debt structure, accounting anomalies, and insider selling patterns.\
The Trap Mechanism: Identifies the 'Pump, Dump, and Trigger' cycle used to aggregate and extract middle-class capital.\
Regulatory Failure: Evaluates the role of Western oversight in allowing a captured entity to achieve systemic significance.""",

        r"""### [The Universal Force Equation of Price v2.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\The Universal Force Equation of Price v2.md
**Categories**: Plane: Q5 HOW; Node: Physics; Tags: Dynamics, Energy, Forces, Gravity, Kinetics, Mechanics, Physics
**Summary**:
Vector Parity Refinement: Updates the price equation to include the alignment between utility and hegemonic coordinate.\
Systemic Drag Coefficient: Introduces a modifier representing the social and moral cost of an economic exchange.\
Breakpoint Prediction: Demonstrates the model's ability to forecast market collapses caused by cumulative moral strain.""",

        r"""### [Investigating Tesla's Chinese Financial Ties.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\Investigating Tesla's Chinese Financial Ties.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Dependency Audit: Forensically examines loan agreements between the subject's subsidiaries and Chinese state banks.\
Restrictive Covenants: Identifies clauses that subordinate global operational will to Chinese strategic requirements.\
Causal Chain of Capture: Tracks the entity's transition from Silicon Valley pioneer to instrument of the Minimisation Plan.""",

        r"""### [The Vampire Economy -  News Article.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\The Vampire Economy -  News Article.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Extractive Realism: Reframes the global economy as a system that drains value from the periphery to sustain a dead center.\
Narrative of Decay: Analyzes the role of media in normalizing asset inflation and declining standards for the majority.\
Systemic Parasitism: Describes the economy's primary goal as the aggregation of survival-rights by a minority elite.""",

        r"""### [BRICS Trade Blockade Economic Impact.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\BRICS Trade Blockade Economic Impact.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Impact Simulation: Models the consequences of a coordinated trade blockade on Western industrial and consumer capacity.\
Chokepoint Vulnerability: Identifies specific sectors where Western dependency on the BRICS axis is near 100%.\
Asymmetric Disruption: Analyzes how the blockade achieves maximum damage for the host with minimal kinetic cost."""
    ])

    summaries.extend([
        r"""### [China's Trade Deals and Economic Control.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\China's Trade Deals and Economic Control.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Bilateral Leverage: Analyzes the use of trade agreements to establish long-term economic control over sovereign nations.\
Infrastructure Capture: Documents the consistent pattern of acquiring majority stakes in foreign strategic assets like ports and mines.\
Debt-for-Alignment: Evaluates the practice of using unpayable loans to force political and strategic realignment with the Asian Pivot.""",

        r"""### [A VFT-Based Socio-Economic Model.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\A VFT-Based Socio-Economic Model.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Low-Strain Governance: Proposes a global model built on VFT principles to achieve systemic equilibrium and minimize social friction.\
{χ} Moral Ledger: Introduces a 16-dimensional metric that replaces raw wealth with a measure of moral and functional contribution.\
Economic Merger: Suggests the integration of economies managed by a central board to dissolve conflict and optimize resource use.""",

        r"""### [Tesla's Structural Risk Assessment.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\Tesla's Structural Risk Assessment.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Insolvency Forensics: Documents the decoupling of market valuation from underlying industrial and financial reality.\
Extraction Patterns: Identifies synchronized insider selling during periods of unfulfilled technological promises.\
Instrument of Aggregation: Characterizes the entity as a financial tool designed for the extraction of middle-class capital by captured elites.""",

        r"""### [The Physics of Price -  Vector Parity & The Hierarchy Problem.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\The Physics of Price -  Vector Parity & The Hierarchy Problem.md
**Categories**: Plane: Q5 HOW; Node: Physics; Tags: Dynamics, Energy, Forces, Gravity, Kinetics, Mechanics, Physics
**Summary**:
Field Theory of Value: Redefines Value as a vector moving through the Psochic Hegemony, with Price as the measure of work required.\
Hierarchy Problem: Analyzes the 10^42 difference in strength between local wants and global needs that distorts market pricing.\
Parity Axiom: Establishes that systemic stability requires alignment between the physical mass of an object and its hegemonic value.""",

        r"""### [Politics Analysis -  The Socioeconomic Siege.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\Politics Analysis -  The Socioeconomic Siege.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Socioeconomic Siege: Defines modern warfare as a continuous state of economic hostility designed to erode sovereignty from within.\
Meta-Gaming Capitalism: Analyzes the weaponization of free markets to acquire majority control over Western supply chains.\
Trust Bankruptcy: Describes the use of 'believable lies' to destroy the Trust Currency required for effective national governance.\
The Golden Cage: Explains the normalization of dependency used to prevent rebellion and secure final institutional merger.""",

        r"""### [Australian Tax Policy and Housing Crisis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Australian Tax Policy and Housing Crisis.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Tax Policy Forensics: Analyzes negative gearing and capital gains exemptions as primary drivers of the Australian housing crisis.\
Asset Concentration: Documents how current tax settings facilitate the transfer of wealth from workers to a narrow class of property speculators.\
Systemic Incoherence: Evaluates the discrepancy between the stated goal of home ownership and the structural outcomes of existing tax law.""",

        r"""### [i've updated the policy, give me a 1-pager.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\i've updated the policy, give me a 1-pager.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
NEN One-Page Summary: Provides a concise overview of the National Energy Network policy as a nation-building infrastructure upgrade.\
Vision for Sovereignty: Outlines the goal of free, clean, and reliable power for every citizen through a nationalized smart grid.\
Self-Funding Model: Details the funding mechanism via fossil fuel subsidy redirection and the creation of a national infrastructure surplus.""",

        r"""### [The Parent-Child Digital Safety Link -  A Simple Explainer.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\The Parent-Child Digital Safety Link -  A Simple Explainer.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
PCDSL Explainer: Presents an alternative to social media bans that empowers parents with technical tools rather than state mandates.\
Privacy-Preserving Design: Contrasts the opt-in system with government ID requirements, highlighting the reduction in privacy risks.\
Safety Failsafes: Details the confidential support functions and automatic termination of supervision at age 16 to protect child autonomy.""",

        r"""### [Policy Deep Dive -  Redefining Council vs. Applicant Responsibilities.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Policy Deep Dive -  Redefining Council vs. Applicant Responsibilities.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Regulatory Simplification: Analyzes a proposal to shift the burden of proof from housing applicants to local councils to accelerate construction.\
Removing Friction: Documents the specific administrative bottlenecks targeted for elimination to lower the cost and time of development.\
Systemic Accountability: Evaluates the shift toward council-led site validation as a method for increasing local government efficiency.""",

        r"""### [Parent-Child Digital Safety Link (PCDSL) .md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Parent-Child Digital Safety Link (PCDSL) .md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Technical Specification: Provides the full structural and operational blueprint for the Parent-Child Digital Safety Link system.\
Audit and Accountability: Outlines how platform responses to safety reports are logged with the eSafety Commissioner for performance tracking.\
Inter-Parent Coordination: Describes the secure chat function allowing parents to resolve bullying issues anonymously through the digital hub.""",

        r"""### [v2 National Energy Network NEN .md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\v2 National Energy Network NEN .md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
NEN v2 Update: Refines the National Energy Network policy with updated costings and a pragmatic 9-year implementation timeline.\
Strategic Buffer: Introduces the NEN Infrastructure Trust Fund to manage surpluses and accelerate sovereign manufacturing capacity.\
Universal Relief: Details the transitional subsidy scheduled for 2030 to deliver cost-of-living relief ahead of full project completion.""",

        r"""### [Policy Deep Dive -  Further Reductions to Applicant Requirements.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Policy Deep Dive -  Further Reductions to Applicant Requirements.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Streamlining Development: Proposes further reductions in housing application complexity by standardizing requirements across jurisdictions.\
Removing Procedural Rot: Identifies legacy regulations that act as 'dead mass' in the construction process, increasing systemic strain.\
Empowering the Builder: Analyzes the move toward a high-trust model for accredited developers to bypass redundant oversight.""",

        r"""### [The Tyrant's Variable -  A PREF Analysis of Abstract Warfare.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\The Tyrant's Variable -  A PREF Analysis of Abstract Warfare.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
PREF Warfare Analysis: Uses the Paradise Reciprocity Economic Framework to analyze how tyrants use abstract variables to justify real-world extraction.\
Universal Breakpoint: Identifies the coordinate where systemic imbalance triggers total collapse of citizen trust and institutional legitimacy.\
Dignity as Defense: Proposes the implementation of PREF as the primary defense against the Minimisation of the host's social cohesion.""",

        r"""### [The Paradise Reciprocity Economic Framework (PREF) new.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\The Paradise Reciprocity Economic Framework (PREF) new.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
PREF Core Specification: Formalizes the economic framework built on reciprocity, dignity, and the elimination of extractive debt.\
Equilibrium Model: Outlines the seven planes of economic interaction, from metaphysical identity to the emotive result of financial security.\
Resolution Pathway: Proposes the transition from a 'Zero-Sum' scarcity mindset to a 'Positive-Sum' reciprocity model for national prosperity.""",

        r"""### [Policy Proposal -  Emergency Housing Acceleration Package (EHAP).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Policy Proposal -  Emergency Housing Acceleration Package (EHAP).md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
EHAP Overview: Proposes a high-velocity legislative package to immediately expand housing supply and reduce market volatility.\
Crisis Intervention: Outlines the use of emergency powers to bypass administrative delays and establish a national housing standard.\
Societal Cohesion: Evaluates the proposal's impact on restoring the social contract by ensuring affordable shelter for all citizens."""
    ])

    summaries.extend([
        r"""### [Immigration Research Report Outline.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Immigration Research Report Outline.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Report Outline: Structures a comprehensive investigation into immigration as a strategic battlefield and manufactured crisis.\
Tactical Signature Analysis: Proposes mapping immigration narratives to Minimiser vectors to detect foreign influence in domestic debate.\
Social Cohesion Metrics: Outlines the use of VFT variables to measure the impact of high-velocity migration on institutional stability.""",

        r"""### [The National Energy Network (NEN) Summary Proposal.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\The National Energy Network (NEN) Summary Proposal.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
NEN Executive Summary: Provides a high-level briefing on the plan to nationalize and decentralize the Australian energy grid.\
Cost-Benefit Analysis: Summarizes the project's ability to eliminate residential power bills while remaining fiscally positive through subsidy redirection.\
Strategic Autonomy: Highlights the role of the NEN in securing national energy independence from global market volatility.""",

        r"""### [Policy Proposal -  The National Energy Network (NEN).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\Policy Proposal -  The National Energy Network (NEN).md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Full NEN Proposal: Details the 9-year roadmap for installing government-owned solar and storage on 10 million Australian homes.\
Industrial Strategy: Outlines the creation of 450,000 jobs and the establishment of a sovereign manufacturing sector for clean tech.\
Financial Model: Documents the project's path to self-funding by 2034 through the sale of grid services and energy exports.""",

        r"""### [Proposal -  The National Energy Network (NEN).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\Proposal -  The National Energy Network (NEN).md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
NEN Policy Draft: A variant of the National Energy Network proposal focusing on the immediate legislative requirements for implementation.\
Governance Structure: Proposes the establishment of the NEN Infrastructure Trust Fund to manage national energy assets and surpluses.\
Implementation Phases: Breaks down the project into discrete phases of pilot testing, mass rollout, and grid integration.""",

        r"""### [The Paradise Reciprocity Economic Framework (PREF)v4 .md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\The Paradise Reciprocity Economic Framework (PREF)v4 .md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
PREF v4 Refinement: Updates the reciprocity economic model with enhanced mechanisms for debt-free value exchange and national dividends.\
Sovereign Equity: Introduces the concept of 'Australia Inc.' where citizens hold equity in national infrastructure and key corporate sectors.\
Systemic Resolution: Analyzes the model's ability to dissolve class conflict by aligning the interests of workers, the state, and corporations.""",

        r"""### [National Energy Network Cost Analysis␊.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\National Energy Network Cost Analysis␊.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Detailed Financial Audit: Provides a line-by-line breakdown of the $70.1 billion capital expenditure required for the NEN project.\
Revenue Projections: Forecasts the income from energy trading and grid stabilization services starting in 2030.\
Fiscal Multiplier: Calculates the project's net positive impact on GDP through job creation and the elimination of household power costs.""",

        r"""### [National Energy Network public.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\National Energy Network public.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Public Briefing: A plain-English version of the NEN policy designed for dissemination to the general population.\
Cost-of-Living Relief: Focuses on the immediate benefit of bill elimination for families and the long-term goal of national prosperity.\
Call to Action: Outlines the steps for citizens to participate in and support the transition to a sovereign decentralized grid.""",

        r"""### [📄 Policy Proposal -  Emergency Housing Acceleration Package (EHAP).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\📄 Policy Proposal -  Emergency Housing Acceleration Package (EHAP).md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
EHAP Formal Draft: Presents the complete legislative and operational text of the housing acceleration package.\
Fast-Track Permitting: Details the removal of local council barriers for high-density development and social housing projects.\
Affordability Standard: Establishes a national baseline for housing costs relative to the guaranteed minimum wage.""",

        r"""### [PREF as a Resolution Vector -  A Comparative Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\PREF as a Resolution Vector -  A Comparative Analysis.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Comparative Economic Audit: Evaluates PREF against traditional Capitalism, Socialism, and Populism to measure hegemonic efficiency.\
Conflict Resolution: Analyzes how the reciprocity model dissolves the 'Scarcity Paradox' and the 'Zero-Sum' trap of modern economics.\
Sovereign Stability: Documents the model's role in anchoring national identity in shared productive value rather than extractive debt.""",

        r"""### [The Paradise Reciprocity Economic Framework (PREF).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\The Paradise Reciprocity Economic Framework (PREF).md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
PREF Foundation: Defines the foundational principles of dignity-based economics and the elimination of poverty as a management issue.\
Circular Value Loop: Outlines the mechanism of national dividends funded by corporate equity swaps and infrastructure surpluses.\
Moral Economy: Evaluates the shift from wealth accumulation as success to hegemonic alignment as the primary metric of national health.""",

        r"""### [National Energy Network (NEN) Policy Proposal (Revised).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\National Energy Network (NEN) Policy Proposal (Revised).md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
NEN Revised Roadmap: Incorporates feedback on grid stability and battery density into the core National Energy Network blueprint.\
Community Node Strategy: Details the role of local transformer-level batteries in creating a resilient and decentralized energy backbone.\
Energy Export Potential: Analyzes Australia's future as a global clean energy superpower through the mass deployment of solar tech.""",

        r"""### [National Energy Network (NEN) Policy Proposal.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\National Energy Network (NEN) Policy Proposal.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Core NEN Blueprint: Provides the primary technical and economic justification for the mass rollout of rooftop solar as a public utility.\
Fossil Fuel Redirection: Details the fiscal mechanism for ending coal and gas subsidies to fund the transition to renewable sovereignty.\
Job Creation Engine: Forecasts the long-term workforce requirements for maintaining and managing the national smart grid.""",

        r"""### [PREF; The ROI of Dignity -  Benefit-Cost Analysis (BCR) of Universal Basic Income.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Policy\Versions\PREF; The ROI of Dignity -  Benefit-Cost Analysis (BCR) of Universal Basic Income.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
UBI BCR Analysis: Forensically calculates the positive return on investment for implementing a guaranteed national dividend in Australia.\
Fiscal Multiplier: Documents how moving 'dead money' from corporate earnings to the local economy increases the velocity of money.\
Cost of Poverty Savings: Estimates billions in savings across health, justice, and bureaucracy by eliminating the symptoms of poverty.\
Economic Verdict: Concludes that ending poverty is a net profitable strategy for the nation, with an estimated BCR of 1.6 : 1.0.""",

        r"""### [A Unified Philosophy of 21st Century Conflict.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\A Unified Philosophy of 21st Century Conflict.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Integrated Warfare Philosophy: Formalizes the shift from purely kinetic conflict to a unified model of economic and informational attrition.\
Rhizomatic War: Analyzes the use of proxy forces and non-linear subversion to achieve systemic effects on conventional adversaries.\
Minimisation Strategy: Identifies the core goal of modern conflict as the minimization of the opponent's sovereign capacity for reaction.""",

        r"""### [The Reverse Open Nuclear Umbrella card.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\The Reverse Open Nuclear Umbrella card.md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Nuclear Coercion Analysis: Deconstructs the Russian strategic doctrine of using nuclear threats to shield conventional aggression in Ukraine.\
Inversion of Deterrence: Analyzes how the 'umbrella' is used not to prevent war, but to create a protected space for regional expansion.\
Global Precedent: Evaluates the consequences of this strategy on the international security order and the proliferation of regional conflict."""
    ])

    summaries.extend([
        r"""### [A Unified Philosophy of 21st Century Conflict v2.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\A Unified Philosophy of 21st Century Conflict v2.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Warfare v2 Refinement: Updates the integrated conflict model to include the role of AI-driven delusion and rapid state capture.\
Entropy as Weapon: Analyzes the deliberate injection of chaos into the host's decision-making loops to induce strategic paralysis.\
Systemic Victory: Defines the goal of modern war not as territorial conquest, but as the total administrative integration of the host into the aggressor's field.""",

        r"""### [The Minimisation Plan -  An Assessment of Donald Trump's Rhetoric as Strategic Information Warfare.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\The Minimisation Plan -  An Assessment of Donald Trump's Rhetoric as Strategic Information Warfare.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Rhetoric as Warfare: Evaluates the subject's public statements as precise tactical instruments within the Minimisation Plan.\
Dismantling Truth: Analyzes the use of 'believable lies' to bankrupt the Trust Currency required for democratic governance.\
Coordination with CRINK: Documents the alignment between the subject's narrative pivots and the strategic needs of foreign adversarial powers.""",

        r"""### [Taiwan Bait Hypothesis Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\Taiwan Bait Hypothesis Analysis.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Strategic Exhaustion: Analyzes the hypothesis that the Taiwan conflict is being used as 'bait' to overextend and exhaust Western military and financial capacity.\
PDI Escalation: Documents the quantifiable increase in joint military activities as a campaign to create sustained strategic pressure.\
Indo-Pacific Trap: Evaluates the role of the conflict in diverting attention from the underlying socioeconomic siege of Western institutions.""",

        r"""### [The AUKUS Gambit -  Australia's Five Strategic Choices in a Multipolar World.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\The AUKUS Gambit -  Australia's Five Strategic Choices in a Multipolar World.md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Geopolitical Calculus: Outlines the five primary strategic paths for Australia in response to the rise of the Sino-Russian axis.\
AUKUS Evaluation: Analyzes the security pact as both a vital shield and a potential vector for strategic entrapment.\
Sovereign Autonomy: Evaluates the trade-offs between deep alliance integration and the maintenance of independent national agency.""",

        r"""### [The Evolution of Warfare.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\The Evolution of Warfare.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Generational Warfare: Traces the transition from 1st-generation kinetic battles to 5th-generation socioeconomic and informational sieges.\
Technological Thresholds: Analyzes how nuclear weapons and the internet have forced the evolution of conflict into the non-linear domain.\
Causal Trajectory: Evaluates the long-term trend toward the total weaponization of every aspect of human and institutional interaction.""",

        r"""### [Sub-bucket 4.2 -  The ＂Taiwan Bait＂ (Calibrated Military Pressure, PDI).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\Sub-bucket 4.2 -  The ＂Taiwan Bait＂ (Calibrated Military Pressure, PDI).md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Calibrated Pressure: Documents the use of military drills and incursions to maintain a state of high tension and strategic anxiety around Taiwan.\
Pacific Attrition: Analyzes the goal of the operation as the gradual exhaustion of the US Pacific presence through continuous minor alerts.\
Tactical Signature: Identifies the patterns of coordination between Chinese and Russian naval activities in the region.""",

        r"""### [The Evolution of Conflict.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\The Evolution of Conflict.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Historical Convergence: Analyzes how multiple conflict vectors (economic, cognitive, institutional) are converging in the 21st century.\
Phase Transition: Describes the current era as a move from a world of stable state actors to a fluid, rhizomatic battlefield.\
Evolutionary Verdict: Concludes that the survival of nations depends on their ability to recognize and respond to non-kinetic aggression.""",

        r"""### [AUKUS Gambit Minimisation Plan Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\AUKUS Gambit Minimisation Plan Analysis.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
AUKUS as Target: Analyzes the security pact through the lens of the Minimisation Plan, identifying it as a primary target for subversion.\
Divide and Conquer: Documents the efforts to create diplomatic friction between AUKUS partners and their regional neighbors.\
Strategic Entrapment: Evaluates whether the costs of the pact (financial and sovereign) serve to minimize Australia's long-term capability.""",

        r"""### [The Mechanics of Collapse -  A Vector-Based Probability Function for Civil War.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\The Mechanics of Collapse -  A Vector-Based Probability Function for Civil War.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Collapse Function: Formalizes a mathematical model to predict the probability of internal state collapse based on hegemonic variables.\
Threshold Indicators: Identifies the specific ratios of trust bankruptcy and social strain that trigger discontinuous civil unrest.\
Vector Dynamics: Analyzes how the acceleration of tribalism and the erosion of shared facts lead to inevitable systemic failure.""",

        r"""### [Strategic Exhaustion -  An Analysis of the Taiwan Bait Hypothesis within the Framework of the Minimisation Plan.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\Strategic Exhaustion -  An Analysis of the Taiwan Bait Hypothesis within the Framework of the Minimisation Plan.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Taiwan Bait Forensics: Provides a detailed analysis of the Taiwan conflict as a strategic resource sink for Western powers.\
IMEC Derailment: Explains the link between regional instability and the prevention of Western-aligned economic corridors.\
Outcome Audit: Measures the realized strategic relief provided to the CRINK axis by the sustained tension in the Indo-Pacific.""",

        r"""### [Sub-bucket 1.3 -  Core Objective - Strategic Exhaustion.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\Sub-bucket 1.3 -  Core Objective - Strategic Exhaustion.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Exhaustion Doctrine: Defines the core goal of the Minimisation Plan as the total depletion of the host's will and capacity to resist.\
Multi-Front Attrition: Analyzes the use of simultaneous crises (health, economic, security) to overwhelm the target's cognitive and logistical resources.\
The Long Siege: Describes the shift from quick victory to a generational campaign of institutional and cultural erosion.""",

        r"""### [The Logic of Conflict.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\The Logic of Conflict.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Formalizing Hostility: Redefines conflict as a competition between incompatible logic systems occupying the same vector space.\
Rule-Set Warfare: Analyzes how adversaries use the host's own logical rules (law, democracy) to paralyze and then subvert it.\
Equilibrium Failure: Evaluates the point where the cost of maintaining a peaceful logic system exceeds the system's available energy.""",

        r"""### [Hegemonic Analysis -  The Chronology of Radicalization Why Hitler Genocided Jews.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\KineticMilitaryAttrition\History\Hegemonic Analysis -  The Chronology of Radicalization Why Hitler Genocided Jews.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Anatomy of Radicalization: Analyzes the historical sequence of events and narrative shifts that led to the Holocaust.\
Scapegoating Vector: Examines the use of a perceived 'internal enemy' to unify a high-will, low-morality national movement.\
Lessons for the Present: Identifies the tactical signatures of dehumanization and institutional capture common to modern authoritarian rises.""",

        r"""### [Australian_Kanon_Plane_3_Land.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_3_Land.md
**Categories**: Plane: Q3 WHERE; Node: The World; Tags: Climate, Earth, Ecology, Environment, Nature, The World, Wilderness
**Summary**:
The Island Continent: Defines the Australian 'Where' as a vast, ancient sanctuary isolated by distance and ocean.\
Spirit of Place: Analyzes the role of the harsh, unyielding land in forging the national character of resilience and practicality.\
Logistics of Sovereignty: Evaluates the strategic challenge of securing a massive landmass with a concentrated population on the periphery.""",

        r"""### [Australian_Kanon_Plane_1_Identity_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_1_Identity_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Identity Moral Audit: Evaluates the Australian 'Who', identifying the central friction between the 'Fair Go' ideal and the 'Tall Poppy' syndrome.\
Egalitarian Trajectory: Measures the national movement toward a horizontal social contract and the rejection of inherited authority.\
Convict Stain: Documents the historical role of the founding trauma in shaping the Australian's skeptical relationship with the State."""
    ])

    summaries.extend([
        r"""### [Deep Research on Billionaire Entrapment.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Deep Research on Billionaire Entrapment.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Entrapment Forensics: Analyzes the mechanism by which major Australian billionaires are captured by foreign interests through debt and trade.\
Strategic Leverage: Documents the specific industrial and financial assets used as leverage to influence domestic Australian policy.\
Oligarchic Subversion: Evaluates the role of captured domestic wealth in disabling the nation's strategic autonomy.""",

        r"""### [Analyzing Australia's Minimisation Plan.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Analyzing Australia's Minimisation Plan.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Australian Minimisation: Maps the global Minimisation strategy onto specific Australian institutions and political actors.\
Sovereign Decay: Analyzes the erosion of Australian independent will in favor of a subordinate role in the Asian Pivot.\
Immune System Check: Evaluates the effectiveness of Australia's legal and security safeguards in detecting and resisting capture.""",

        r"""### [Tony Abbott's Minimisation Plan Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Tony Abbott's Minimisation Plan Analysis.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Abbott Audit: Performs a hegemonic assessment of the former Prime Minister's policy legacy and its alignment with Minimiser goals.\
Institutional Inversion: Analyzes specific decisions that weakened long-term national capacity while projecting a narrative of strength.\
Foundational Shift: Documents the acceleration of extractive economic models during the subject's tenure.""",

        r"""### [Analyzing FOI Resistance as Authoritarian Tell.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Analyzing FOI Resistance as Authoritarian Tell.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Opacity Metrics: Formalizes the resistance to Freedom of Information requests as a primary indicator of institutional corruption.\
Narrative Shielding: Analyzes how administrative delays are used to hide 'tragic' or 'hypocritical' gaps in government policy.\
Democratic Erosion: Evaluates the long-term impact of systemic secrecy on public trust and systemic accountability.""",

        r"""### [Australian_Kanon_Plane_6_Foundation_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_6_Foundation_JUDGMENT.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Foundational Audit: Evaluates the historical 'Cause' of Australia, focusing on the tension between the convict origin and the democratic ideal.\
Sacrifice and Service: Measures the national value assigned to ANZAC-style sacrifice as a stabilizing causal force.\
Structural Hypocrisy: Documents the failure to fully integrate indigenous history into the foundational national narrative.""",

        r"""### [Victorian Premier Dossier -  Minimisation Plan.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Victorian Premier Dossier -  Minimisation Plan.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
State-level Capture: Analyzes the Victorian Premiership through the lens of the Minimisation Plan and the Belt and Road Initiative.\
Fiscal Extraction: Documents the use of mega-projects to facilitate capital flight and establish unpayable state-level debt.\
Administrative Subversion: Evaluates the modification of state-level protocols to favor foreign commercial and strategic interests.""",

        r"""### [Australian_Kanon_FINAL_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_FINAL_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Consolidated Audit Verdict: Provides the aggregate hegemonic score for the Australian project based on the complete 343-vector audit.\
National Equilibrium: Measures the current state of the Australian social contract relative to the foundational 'Fair Go' ideal.\
Strategic Recommendation: Identifies the primary vectors for national recovery and the restoration of sovereign integrity.""",

        r"""### [Australian_Kanon_Plane_4_Drive_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_4_Drive_JUDGMENT.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Drive Moral Audit: Evaluates the Australian 'Why', identifying the tension between the 'Battler' spirit and the 'Consumer' retreat.\
Resonance of Place: Analyzes how the national meaning is anchored in a connection to the land and the rejection of abstract pretension.\
Erosion of Ambition: Measures the shift from national building toward individualized material comfort as a metric of systemic decay.""",

        r"""### [Australian_Kanon_Plane_7_Result.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_7_Result.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Homeostatic Result: Defines the Australian 'Effect' as a stable, high-trust society characterized by informal egalitarianism.\
Globalization Impact: Analyzes how international economic integration has stressed the unique Australian horizontal contract.\
Continuity of Character: Evaluates the persistence of national traits like humor and skepticism as the ultimate systemic stabilizers.""",

        r"""### [Australian_Kanon_Philosophy.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Philosophy.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Underlying Axioms: Formalizes the philosophical foundations of the Australian Kanon, focusing on monism and practical realism.\
Rejection of Class: Analyzes the inherent philosophical refusal of inherited social hierarchies within the Australian system.\
Mateship as Logic: Evaluates the concept of mateship not as a sentiment, but as a functional protocol for distributed systemic trust.""",

        r"""### [Australia's Role in Minimisation Plan.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australia's Role in Minimisation Plan.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Strategic Node Analysis: Defines Australia's role in the global strategy as a primary provider of resources and a relay for Pacific influence.\
Relay Subversion: Analyzes how Australian political capture is used to project adversarial influence into the Five Eyes and AUKUS networks.\
Logistical Dependency: Documents the weaponization of Australia's trade imbalance to ensure its compliance with the Asian Pivot.""",

        r"""### [Project Delusion -  A Causal Analysis of the Minimisation Plan's Influence on Australia (2001-Present) - A Consolidated Report.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Project Delusion -  A Causal Analysis of the Minimisation Plan's Influence on Australia (2001-Present) - A Consolidated Report.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Two-Decade Narrative: Chronicles the systematic infiltration and subversion of Australian political reality since 2001.\
Causal Chain of Decay: Documents the sequence of policy 'accidents' and 'incompetencies' that have facilitated the national retreat.\
Consolidated Forensics: Synthesizes case studies of political capture into a single unified theory of Australian minimization.""",

        r"""### [Australian_Kanon_Plane_4_Drive.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_4_Drive.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
National Driver: Defines the Australian 'Why' as the drive for personal independence within a supportive horizontal community.\
Battler Mythology: Analyzes the role of the self-reliant underdog in providing the emotional energy for national endurance.\
Resonance of Fair Go: Evaluates how the demand for equity acts as the primary corrective feedback loop in the system.""",

        r"""### [Australian Minimisation Plan Research Synthesis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian Minimisation Plan Research Synthesis.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Research Compendium: Consolidates various investigative streams regarding the Minimisation Plan's execution within the Australian theatre.\
Tactical Pattern Identification: Isolates recurring signatures of adversarial influence in Australian media, policy, and corporate behavior.\
Counter-Strategy Roadmap: Proposes a framework for restoring national sovereignty through transparency and hegemonic alignment.""",

        r"""### [An Analysis of Political Capture in the Australian Theatre -  A Timelined Account of the Minimisation Plan (1990-Present).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\An Analysis of Political Capture in the Australian Theatre -  A Timelined Account of the Minimisation Plan (1990-Present).md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Generational Subversion: Provides a comprehensive timeline of state capture in Australia starting from the post-Cold War era.\
Financial Infiltration: Tracks the acquisition of key infrastructure and political influence through corporate lobbying and donations.\
Long-term Trajectory: Evaluates the shift from a sovereign middle-power to a captured resource colony for the Sino-Russian axis."""
    ])

    summaries.extend([
        r"""### [Project Delusion -  The Minimisation Plan's Australian Vectors.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Project Delusion -  The Minimisation Plan's Australian Vectors.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Aletheia Vector Mapping: Analyzes specific narrative vectors used to inject delusion into the Australian public discourse.\
Media Capture: Documents the role of major media networks in amplifying Minimiser-produced lies and distractions.\
Cognitive Exhaustion: Evaluates the use of constant social conflict to tire the national immune system and enable subversion.""",

        r"""### [Woolworths Chinese Ties Investigation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Woolworths Chinese Ties Investigation.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Supply Chain Capture: Investigates the financial and logistical ties between a major Australian retailer and Chinese interests.\
Strategic Entrapment: Documents how retail dependence on foreign-linked supply chains creates a vector for domestic political influence.\
Corporate Accountability: Evaluates the discrepancy between public nationalistic branding and underlying globalized ownership.""",

        r"""### [Internet Ban Data Harvesting Investigation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Internet Ban Data Harvesting Investigation.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Digital Harvesting Forensics: Analyzes the proposed Australian social media ban as a pretext for massive state-level data harvesting.\
Surveillance Vector: Documents how mandatory ID verification creates a centralized database of citizen digital identities vulnerable to capture.\
Privacy Liquidation: Evaluates the systemic shift toward total digital visibility and the erosion of individual privacy as a hegemonic risk.""",

        r"""### [Australian_Kanon_Plane_2_Definition_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_2_Definition_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Possibility Space Audit: Evaluates the Australian 'What', identifying the tension between practical innovation and cultural cringe.\
Scientific Realism: Measures national fidelity to objective reality and the empirical method as a stabilizing factor.\
Axiomatic Stagnation: Documents the failure to update the national definition of 'What is Possible' in the face of 21st-century challenges.""",

        r"""### [Australian_Kanon_Plane_5_Method.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_5_Method.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
The Workingman's Method: Defines the Australian 'How' as a unique synthesis of pragmatic improvisation and strong labor protections.\
Infrastructure of Equity: Analyzes the role of public utilities and the social safety net in achieving national stability.\
Procedural Pragmatism: Evaluates how the focus on 'Getting the Job Done' anchors the national identity in tangible results.""",

        r"""### [Australian_Kanon_Plane_5_Method_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_5_Method_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Method Moral Audit: Evaluates the Australian 'How', identifying the tension between industrial efficiency and social welfare.\
Entropy of Bureaucracy: Measures the shift from pragmatic service toward administrative self-preservation as a metric of decay.\
Systemic Integrity Check: Documents the capacity of Australian methods to deliver on the promise of the Fair Go.""",

        r"""### [Strategic Assessment of the Australian Information Environment -  Corporate Entrapment and Vectors of the Minimisation Plan.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategic Assessment of the Australian Information Environment -  Corporate Entrapment and Vectors of the Minimisation Plan.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Information Environment Audit: Provides a strategic assessment of the actors and narratives dominating the Australian media landscape.\
Corporate Capture Vectors: Identifies the use of advertising and lobbying to neutralize critical reporting on strategic vulnerabilities.\
Minimiser Influence Channels: Documents the specific platforms and personas used to disseminate foreign-aligned propaganda.""",

        r"""### [Australian_Kanon_Plane_3_Land_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_3_Land_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Territorial Audit: Evaluates the Australian 'Where', identifying the tension between environmental protection and resource exploitation.\
Sovereignty of Soil: Measures the national value assigned to land ownership and the integrity of the border as a protective shield.\
Structural Extraction: Documents the moral costs paid for a wealth model based primarily on digging things out of the ground.""",

        r"""### [Australian_Kanon_Plane_6_Foundation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_6_Foundation.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
National Bedrock: Defines the Australian 'Cause' as a unique synthesis of indigenous heritage, convict trauma, and democratic hope.\
Sacrifice and Survival: Analyzes the role of the ANZAC legend in providing the causal narrative for national unity.\
Causal Trajectory: Evaluates the long-term movement from a British outpost to a self-defined independent republic.""",

        r"""### [Australian_Kanon_Plane_2_Definition.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_2_Definition.md
**Categories**: Plane: Q2 WHAT; Node: Metaphysics; Tags: Abstract, Cosmology, Existentialism, Imagination, Metaphysics, Ontology, Phenomenon
**Summary**:
National Possibility: Defines the Australian 'What' as a pragmatic space of potential centered on social mobility and objective fact.\
Realism over Ideology: Analyzes the role of skepticism in preventing the rise of extreme political dogmas within the system.\
Substantive Identity: Evaluates the grounding of the national definition in the material achievement of the population rather than abstract symbols.""",

        r"""### [No More Bullshit Democracy Model.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\No More Bullshit Democracy Model.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Direct Democracy Proposal: Outlines a model for radical transparency and citizen participation to bypass captured institutional intermediaries.\
Removing the Buffer: Proposes the elimination of political donations and the implementation of immediate citizen feedback loops.\
Systemic Accountability: Evaluates the proposal's potential to restore hegemonic alignment between the state and the people.""",

        r"""### [Friendlyjordies Firebombing Investigation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Friendlyjordies Firebombing Investigation.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Political Violence Forensics: Investigates the firebombing of an Australian journalist as a tactical signature of organized state/corporate capture.\
Suppression of Dissent: Documents the use of extra-legal violence to silence criticism of high-level corruption and influence peddling.\
Institutional Failure: Evaluates the role of law enforcement and the judiciary in failing to provide a protective shield for independent investigative reporting.""",

        r"""### [Australian_Kanon_Plane_7_Result_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_7_Result_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Homeostatic Audit: Evaluates the Australian 'Effect', identifying the central friction between social cohesion and individualistic retreat.\
National Resilience: Measures the system's capacity to absorb external shocks while maintaining its internal egalitarian equilibrium.\
Verdict on Continuity: Concludes the assessment of whether the Australian experiment remains a viable and sovereign project."""
    ])

    summaries.extend([
        r"""### [Australian_Kanon_Plane_1_Identity.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Australian_Kanon_Plane_1_Identity.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
The Australian 'Who': Defines the primary agent as the egalitarian citizen committed to the 'Fair Go' and mutual aid.\
Identity Mapping: Analyzes the national soul as a synthesis of individual independence and horizontal community obligation.\
Rejecting Authority: Documents the historical refusal of rigid class structures and the embrace of a merit-based social contract.""",

        r"""### [Australian_Kanon_Plane_3_Land.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_3_Land.md
**Categories**: Plane: Q3 WHERE; Node: The World; Tags: Climate, Earth, Ecology, Environment, Nature, The World, Wilderness
**Summary**:
Island Sanctuary: Defines the physical territory as an ancient landmass requiring unique methods of stewardship and defense.\
Perimeter Defense: Analyzes the strategic importance of maritime security in maintaining Australian sovereign autonomy.\
Resource Base: Evaluates the land as the primary source of national wealth and the locus of the 'Spirit of Place'.""",

        r"""### [Australian_Kanon_Plane_1_Identity_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_1_Identity_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Identity Audit (Aus Kanon): Evaluates the alignment of the national 'Who' with the 343 vectors of the Australian ideal.\
Social Cohesion Check: Measures the current strength of the horizontal contract and the impact of increasing wealth inequality.\
Trait Persistence: Tracks the survival of egalitarian values in the face of globalized class re-emergence.""",

        r"""### [AustralianKanon1-3.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\AustralianKanon1-3.md
**Categories**: Plane: Q1 to Q3; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
National Soul Audit (Part 1): Consolidates the audit results for the first three planes of the Australian Kanon (Identity, Definition, Land).\
Triangulation of Being: Analyzes the intersection of the national agent, its possibility space, and its physical territory.\
Baseline Stability: Establishes the foundational hegemonic coordinates for the Australian state at the start of the 21st century.""",

        r"""### [Australian_Kanon_Plane_6_Foundation_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_6_Foundation_JUDGMENT.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Historical Foundation Audit: Evaluates the national 'Cause', identifying the central frictions between origin myths and verified action.\
Continuity Validation: Measures the system's capacity to maintain its core democratic logic across generational transitions.\
Sacrifice Metric: Documents the value assigned to national service as a primary stabilizer of institutional trust.""",

        r"""### [Australian_Kanon_Plane_4_Drive_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_4_Drive_JUDGMENT.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Audit of Drive (Aus Kanon): Evaluates the national 'Why', identifying the tension between collective ambition and individualistic apathy.\
Resonance Mapping: Analyzes how national purpose is anchored in the shared experience of the Australian environment.\
Decay Indicators: Measures the shift from national building toward reactive consumption as a sign of hegemonic contraction.""",

        r"""### [Australian_Kanon_Plane_7_Result.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_7_Result.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Realized National Outcome: Defines the Australian 'Effect' as a stable society characterized by high trust and minimal class friction.\
Heuristic for Success: Analyzes how informal social protocols like 'Mateship' deliver real-world stability with low administrative cost.\
Global Positioning: Evaluates Australia's homeostatic result within the context of the international security and economic field.""",

        r"""### [AustralianKanon.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\AustralianKanon.md
**Categories**: Plane: Q1 to Q7; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Consolidated Australian Kanon: Provides the master registry of the 343 vectors defining the Australian national soul.\
Unified Reference Frame: Synthesizes the planes, senses, and uses into a single diagnostic engine for auditing national integrity.\
Strategic Beacon: Acts as the absolute standard for identifying and correcting Minimiser-produced distortions in the Australian OS.""",

        r"""### [Australian_Kanon_Plane_4_Drive.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_4_Drive.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Engine of Australian Meaning: Defines the core motivation as the pursuit of independence within a cooperative horizontal field.\
Myth of the Battler: Analyzes the role of self-reliance and the rejection of pretense in driving national energy.\
Trajectory of Purpose: Evaluates the historical movement from colonial dependency toward absolute sovereign self-determination.""",

        r"""### [AustralianKanon6-7.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\AustralianKanon6-7.md
**Categories**: Plane: Q6 to Q7; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
National Soul Audit (Part 2): Consolidates the audit results for the final two planes of the Australian Kanon (Cause, Effect).\
Legacy and Realization: Analyzes the intersection of historical origin and contemporary outcome to measure national fidelity.\
Equilibrium Verdict: Provides the final hegemonic assessment of the Australian system's stability and future potential.""",

        r"""### [Australian_Kanon_Plane_2_Definition_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_2_Definition_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Definition Audit (Aus Kanon): Evaluates the alignment of the national possibility space with the 343 vectors of the ideal.\
Skepticism Metric: Measures the national capacity to resist ideological delusion through the application of practical realism.\
Fidelity to Fact: Documents the role of objective truth in maintaining the integrity of the Australian democratic process.""",

        r"""### [Australian_Kanon_Plane_5_Method.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_5_Method.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Practical Methodology: Defines the Australian 'How' as a synthesis of industrial pragmatism and social equity protocols.\
Systemic Delivery: Analyzes the role of national infrastructure and public services in manifesting the egalitarian ideal.\
Logic of the Job: Evaluates the focus on outcome-based problem solving as a stabilizer for national institutional trust.""",

        r"""### [Australian_Kanon_Plane_5_Method_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_5_Method_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Method Audit (Aus Kanon): Evaluates the operational efficiency and moral integrity of Australian institutional methods.\
Bureaucratic Strain: Measures the impact of administrative centralization on the delivery of the national promise of equity.\
Integrity of Service: Documents the capacity of state methods to serve the collective good without succumbing to elite capture.""",

        r"""### [Australian_Kanon_Plane_3_Land_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_3_Land_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Territorial Audit (Aus Kanon): Evaluates the stewardship of the Australian landmass and the security of its borders.\
Sovereign Integrity: Measures the national value assigned to territorial independence and the protection of natural assets.\
Extraction Friction: Documents the tension between national environmental goals and the realities of an export-based economy.""",

        r"""### [AustralianKanon4-5.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\AustralianKanon4-5.md
**Categories**: Plane: Q4 to Q5; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
National Soul Audit (Part 2): Consolidates audit results for the Drive and Method planes of the Australian Kanon.\
Resonance and Process: Analyzes the intersection of national meaning and operational execution to detect systemic misalignment.\
Operational Fidelity: Establishes the hegemonic coordinates for the current functionality of the Australian state."""
    ])

    summaries.extend([
        r"""### [Australian_Kanon_Plane_6_Foundation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_6_Foundation.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Causal Roots of Australia: Defines the foundation as a synthesis of ancient land, colonial trauma, and democratic growth.\
Narrative of Emergence: Analyzes the ANZAC legend as the primary causal stabilizer for national unity and identity.\
Generational Continuity: Evaluates the persistence of foundational egalitarian values across the national timeline.""",

        r"""### [Australian_Kanon_Plane_2_Definition.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_2_Definition.md
**Categories**: Plane: Q2 WHAT; Node: Metaphysics; Tags: Abstract, Cosmology, Existentialism, Imagination, Metaphysics, Ontology, Phenomenon
**Summary**:
National Potential: Defines the American 'What' as a pragmatic space of potential centered on social mobility and objective fact.\
Substantive Skepticism: Analyzes the role of practical realism in preventing the rise of extreme political dogmas.\
Definition by Achieving: Evaluates the grounding of national identity in the material achievements of the population.""",

        r"""### [Australian_Kanon_Plane_7_Result_JUDGMENT.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_7_Result_JUDGMENT.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Outcome Moral Audit: Evaluates the Australian 'Effect', identifying the friction between social cohesion and individualistic retreat.\
National Resilience Metric: Measures the system's capacity to maintain its egalitarian equilibrium under global economic stress.\
Integrity of Continuity: Documents whether the homeostatic result of the Australian system remains sovereign and aligned with its origins.""",

        r"""### [Australian_Kanon_Plane_1_Identity.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Aus Kanon\Australian_Kanon_Plane_1_Identity.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Identity Definition: Defines the Australian agent as the egalitarian 'Battler' committed to the Fair Go and mateship.\
Sovereignty of the Self: Analyzes the refusal of rigid social hierarchies as the core identity mechanism of the nation.\
Community obligation: Documents the historical anchoring of identity in mutual aid and shared survival in a harsh environment.""",

        r"""### [An Analysis of Sussan Ley.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Sussan Ley\An Analysis of Sussan Ley.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Figure Audit: Performs a hegemonic assessment of Sussan Ley's political career and policy alignment.\
Vector Discrepancy: Analyzes specific instances where stated 'Maximiser' intentions diverged from verified 'Minimiser' outcomes.\
Strategic Allegiance: Evaluates the subject's role in facilitating extractive economic models within the Australian landscape.""",

        r"""### [Project Chimera -  An Investigation into the Minimisation Strategy of Peter Dutton (2001-2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Peter Dutton\Project Chimera -  An Investigation into the Minimisation Strategy of Peter Dutton (2001-2025).md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Long-term Figure Analysis: Chronicles Peter Dutton's political rise as a study in the strategic minimization of host sovereignty.\
Authoritarian Trajectory: Documents the consistent use of security and border policy to centralize executive power and bypass oversight.\
Causal Signature: Identifies the patterns of institutional attrition and narrative control associated with the subject's career.""",

        r"""### [Peter Dutton Investigation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Peter Dutton\Peter Dutton Investigation.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Forensic Dossier: Consolidates investigative data on the subject's policy impact and political allegiances.\
Minimisation Alignment: Evaluates the subject's consistency with the Minimisation Plan's goals of institutional capture and social polarization.\
Verification of Tactic: Uses public statements and legislative actions to verify the subject's status as a high-will adversarial actor.""",

        r"""### [Murdoch Empire Post-2019 Review.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Rupert Murdoch\Murdoch Empire Post-2019 Review.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Media Empire Audit: Analyzes the post-2019 strategy of the Murdoch media apparatus in Australia and globally.\
Narrative Monopolization: Documents the use of media concentration to suppress competing 'Maximiser' viewpoints and amplify division.\
Systemic Influence: Evaluates the empire's role as a primary logistical relay for the Minimisation Plan's informational warfare.""",

        r"""### [An Analytical Review of Rupert Murdoch -  The Architecture of a Global Ideological Apparatus.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Rupert Murdoch\An Analytical Review of Rupert Murdoch -  The Architecture of a Global Ideological Apparatus.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Architectural Forensics: Deconstructs the global media empire as a unified instrument of ideological and political capture.\
Protocol of Influence: Analyzes the specific mechanical rules used to shape public reality and ensure the survival of the 'Board's' interests.\
Autonomy Liquidator: Documents the role of the subject in liquidating national sovereign will to serve transnational oligarchic agendas.""",

        r"""### [The_Stoic_Guardian.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Archetype\The_Stoic_Guardian.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Archetype Definition: Formalizes 'The Stoic Guardian' as a high-will, high-morality persona within the Australian hegemonic field.\
Resonance with Land: Analyzes how the archetype integrates the harshness of the environment with a commitment to egalitarian justice.\
Stabilizing Function: Evaluates the role of the guardian in maintaining systemic integrity during periods of high adversarial pressure.""",

        r"""### [Sub-bucket 6.1 -  Profiles of Australian Billionaires (Rinehart, Forrest, Palmer, Stokes).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Billionaires\Sub-bucket 6.1 -  Profiles of Australian Billionaires (Rinehart, Forrest, Palmer, Stokes).md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Oligarchic Audit: Performs hegemonic assessments of four major Australian billionaires to detect capture or alignment patterns.\
Extraction vs Investment: Measures the balance between national value creation and the offshore siphoning of national wealth.\
Influence Mapping: Documents the use of private wealth to shape Australian media and political agendas in favor of Minimiser goals.""",

        r"""### [Verified Intelligence -  Pauline Hanson's Rhetoric (Dec 15–24, 2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Pauline Hanson\Verified Intelligence -  Pauline Hanson's Rhetoric (Dec 15–24, 2025).md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Rhetorical Forensics: Analyzes a specific window of public statements by the subject for tactical alignment with the Minimisation Plan.\
Polarization Vector: Documents the use of inflammatory narratives to deepen social fractures and divert attention from economic capture.\
Validation Check: Measures the degree to which the subject's rhetoric validates foreign-aligned interests while claiming nationalistic intent.""",

        r"""### [Project Dossier -  A Min／Max Analysis of the Mostyn Governorship.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Sam Mostyn\Project Dossier -  A Min／Max Analysis of the Mostyn Governorship.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Institutional Audit: Performs a hegemonic assessment of the Mostyn governorship, identifying its trajectory as a Maximiser or Minimiser agent.\
Policy Cohesion: Analyzes specific administrative decisions for their impact on Australian institutional independence and trust.\
Systemic Alignment: Documents whether the leadership office functions as a shield for sovereign integrity or a gateway for capture.""",

        r"""### [The Australian Political Matrix -  A Psochic Analysis of Power, Influence, and Inertia.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\The Australian Political Matrix -  A Psochic Analysis of Power, Influence, and Inertia.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Political Field Analysis: Maps the primary Australian political actors and institutions onto the hegemonic coordinate grid.\
Inertia vs. Velocity: Analyzes the resistance of established bureaucracies to systemic reform and the speed of adversarial subversion.\
Conflict Vectors: Identifies the primary friction points between the national egalitarian ideal and the reality of corporate/state capture.""",

        r"""### [Hegemonic Analysis -  The Double Dissolution (DD) Plot.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\Hegemonic Analysis -  The Double Dissolution (DD) Plot.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Tactical Audit: Analyzes the use of constitutional 'Double Dissolution' triggers as a strategic instrument for institutional disruption.\
Manufactured Crisis: Documents the creation of legislative stalemates designed to force premature elections and exhaust public patience.\
Subversion Mechanism: Evaluates how the DD plot is used to disable government function and enable a high-will hostile takeover."""
    ])

    summaries.extend([
        r"""### [Australia's War Economic Loss Assessment.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\Australia's War Economic Loss Assessment.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Economic Impact Simulation: Models the potential losses for the Australian economy in the event of a regional kinetic or trade war.\
Logistical Vulnerability: Identifies critical dependencies in energy, fuel, and manufactured goods that would lead to rapid systemic failure.\
Sovereign Risk Check: Evaluates the cost of existing 'Just-In-Time' supply chain models relative to the need for national resilience.""",

        r"""### [Projected Timeline -  The ＂Double Dissolution＂ Rhetoric & Indicators.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\Projected Timeline -  The ＂Double Dissolution＂ Rhetoric & Indicators.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Strategic Forecasting: Documents the rhetorical indicators and policy decisions signaling a move toward a manufactured Double Dissolution election.\
Timeline of Disruption: Maps the sequence of anticipated legislative conflicts designed to exhaust the Australian political system.\
Indicator Audit: Provides a checklist of tactical signatures associated with the use of constitutional crises as subversion tools.""",

        r"""### [The Politicisation of Immigration in Australia (1990-Present) -  A Strategic Assessment of Minimiser Narratives and Actors.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\The Politicisation of Immigration in Australia (1990-Present) -  A Strategic Assessment of Minimiser Narratives and Actors.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Immigration Narrative Audit: Analyzes the use of migration as a primary vector for deepening social division and enabling state capture.\
Tactical Scapegoating: Documents the role of specific media and political actors in framing immigration as an existential threat to national identity.\
Diversionary Conflict: Evaluates how inflammatory migration debate is used to divert public attention from underlying industrial and financial erosion.""",

        r"""### [The Corporate Duopoly of Coles and Woolworths -  Market Power, Strategic Minimisation, and Regulatory Constraint.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\The Corporate Duopoly of Coles and Woolworths -  Market Power, Strategic Minimisation, and Regulatory Constraint.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Duopoly Forensics: Analyzes the market dominance of major Australian retailers as a primary vector for consumer entrapment and wealth extraction.\
Strategic Minimisation: Documents the role of retail concentration in suppressing domestic competition and facilitating foreign influence in the supply chain.\
Regulatory Capture: Evaluates the failure of oversight bodies to prevent the liquidation of small-scale producers and the erosion of national food security.""",

        r"""### [Strategic Assessment -  The 'Fortress Australia' Contingency.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\Strategic Assessment -  The 'Fortress Australia' Contingency.md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Sovereign Shield Analysis: Evaluates the strategic 'Fortress Australia' model as a potential response to global systemic collapse.\
Resilience Checklist: Outlines the requirements for achieving self-sufficiency in energy, nutrition, and industrial defense.\
Autonomy vs. Isolation: Analyzes the trade-offs between deep global integration and the creation of a protected national sanctuary.""",

        r"""### [Australia's Strategic Choices Report.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\Australia's Strategic Choices Report.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Grand Strategy Audit: Consolidates the strategic options for Australia within the current multipolar conflict field.\
Alignment Vectors: Maps the consequences of aligning with the CRINK axis, the US/AUKUS shield, or pursuing a policy of armed neutrality.\
Systemic Recommendation: Identifies the need for a 'Maximiser' strategy centered on sovereign capability and high-trust alliances.""",

        r"""### [The Unfettered Leviathan -  An Inquiry into the Dangers of Global Capitalism and the Imperative for Democratic Oversight.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\The Unfettered Leviathan -  An Inquiry into the Dangers of Global Capitalism and the Imperative for Democratic Oversight.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Leviathan Critique: Formalizes the danger of globalized capitalism when it operates beyond the reach of national democratic oversight.\
Liquidation of the State: Analyzes how transnational capital siphons national wealth and then uses it to dismantle host legal protections.\
Restoring Oversight: Proposes a framework for re-anchoring global entities to national moral and volitional standards to prevent systemic rot.""",

        r"""### [The Structural Encapturement of the Australian Consumer -  A Forensic Analysis of the Corporate Duopoly, Sovereign Supply Chain Risks, and the Mechanics of Market Entrapment.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Strategy & Analysis\The Structural Encapturement of the Australian Consumer -  A Forensic Analysis of the Corporate Duopoly, Sovereign Supply Chain Risks, and the Mechanics of Market Entrapment.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Consumer Encapturement: Provides a deep forensic analysis of the market mechanisms used to trap Australian consumers in a low-choice environment.\
Supply Chain Vulnerability: Documents the strategic risks associated with retail dependency on a small number of geopolitically sensitive providers.\
Market Entrapment Mechanics: Identifies the use of loyalty programs and data harvesting to normalize consumer passivity and enable extraction.""",

        r"""### [Manufacturing Dissent -  A Timeline of the Coordinated Suppression of the Australian Greens.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\Manufacturing Dissent -  A Timeline of the Coordinated Suppression of the Australian Greens.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Timeline of Suppression: Chronicles the coordinated efforts by corporate and major party interests to delegitimize the Australian Greens.\
Manufacturing Outrage: Documents the use of media distortions and tactical distractions to suppress 'Maximiser' environmental policy.\
Strategic Marginalization: Analyzes the goal of the operation as the removal of a primary institutional obstacle to extractive industrial expansion.""",

        r"""### [Greens Maximiser／Minimiser Detection Test.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\Greens Maximiser／Minimiser Detection Test.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Hegemonic Litmus Test: Applies the VFT framework to current Greens policy and leadership to detect underlying Minimiser influence.\
Distinguishing Vectors: Provides a methodology for separating genuine environmental advocacy from foreign-aligned 'Zero-Growth' subversion.\
Internal Integrity Check: Evaluates the subject's consistency with the principles of universal benefit and sovereign transparency.""",

        r"""### [The Supra-Political Donor Convergence.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\The Supra-Political Donor Convergence.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Donor Convergence Forensics: Analyzes the pattern of major corporate donors funding both major parties to ensure a fixed policy outcome.\
Supra-Political Control: Documents the mechanism by which private wealth creates a permanent administrative floor above the electoral process.\
Liquidation of Choice: Evaluates the impact of donor convergence on the public's perception of democratic agency and institutional trust.""",

        r"""### [Australian Greens under attack analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\Australian Greens under attack analysis.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Attack Vector Audit: Analyzes specific rhetorical and media strikes against the Greens for tactical alignment with extractive industrial interests.\
Narrative Inversion: Documents the framing of environmental responsibility as an elite luxury or a foreign-aligned threat to the working class.\
Systemic Resistance: Evaluates the role of the Greens as a target for Minimiser operations designed to protect the status quo of asset extraction.""",

        r"""### [The Actualist Gematria -  A ＂Gap Alphabet＂ Lexicon.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\The Actualist Gematria -  A ＂Gap Alphabet＂ Lexicon.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Actualist Lexicon: Defines the 'Gap Alphabet' used in VFT to decode the underlying machine code of language and intent.\
Semantic Encryption: Analyzes the use of specific letter-to-plane mappings to uncover the functional specifications of public names and slogans.\
Heuristic for Truth: Provides a linguistic auditing tool for identifying deceptive framing and detecting the 'Hum' in administrative speech.""",

        r"""### [A Strategic Directory of Elected Representatives of the Australian Greens -  Federal, State, and Local Tiers.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\A Strategic Directory of Elected Representatives of the Australian Greens -  Federal, State, and Local Tiers.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Greens Directory: Provides a comprehensive list of elected representatives as a resource for mapping the party's influence networks.\
Strategic Contact Points: Identifies key decision-makers within the party for engagement on 'Maximiser' environmental and social policy.\
Network Analysis: Acts as a foundational database for tracking the party's institutional resilience against adversarial subversion.""",

        r"""### ['Advance Australia Fair'.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\'Advance Australia Fair'.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Anthem Moral Audit: Analyzes the Australian national anthem through the VFT framework to extract its foundational hegemonic claims.\
Universal Opportunity: Evaluates the phrase 'Advance Australia Fair' as an absolute mandate for egalitarian progress and the Fair Go.\
Resonance Check: Measures the alignment between the anthem's high-will lyrical intent and the current reality of national policy."""
    ])

    summaries.extend([
        r"""### [Political Donor Network Analysis-Advance Australia-ONP-Katter-Majors.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\Political Donor Network Analysis-Advance Australia-ONP-Katter-Majors.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Donor Network Audit: Forensically maps the financial connections between major donors and the spectrum of Australian political parties.\
Strategic Funding Flow: Documents the use of diverse funding channels to support both populist and major party actors simultaneously.\
Influence Consolidation: Evaluates how the donor network creates a structural blockade against systemic reform and 'Maximiser' policy.""",

        r"""### [Hegemonic Analysis -  Core Tenets of Australian Political Parties.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\Hegemonic Analysis -  Core Tenets of Australian Political Parties.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Party Platform Audit: Performs a hegemonic assessment of the core tenets of the ALP, LNP, ONP, and Greens.\
Ideological Trajectory: Maps each party's stated ideals against their historical actions to identify tragic or hypocritical gaps.\
Systemic Alignment: Evaluates which political actors remain capable of serving as shields for national sovereign integrity.""",

        r"""### [ALP Right Faction Dossier Research.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\ALP Right Faction Dossier Research.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Factional Forensics: Investigates the ALP Right faction as a primary target for corporate and foreign influence within the Labor party.\
Capture Indicators: Documents specific policy decisions and personnel links that signal an underlying alignment with extractive interests.\
Minimiser Vectors: Evaluates the role of the faction in suppressing 'Maximiser' industrial and social reform to maintain donor approval.""",

        r"""### [Actualism; The Lyrical Plane of Meaning alphabet of meaning.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\Actualism; The Lyrical Plane of Meaning alphabet of meaning.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Alphabet of Meaning: Formalizes the VFT machine code for language, providing functional definitions for each alphabetical character.\
Lyrical Plane Logic: Analyzes how the physical shape and frequency of letters encode metaphysical and moral instructions.\
Forensic Linguistics: Provides a toolkit for decoding the underlying intent of political slogans and corporate branding.""",

        r"""### [Sub-bucket 5.6 -  Suppression of the Australian Greens - A Chronological Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\Sub-bucket 5.6 -  Suppression of the Australian Greens - A Chronological Analysis.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Chronology of Suppression: Reconstructs the multi-decade campaign by extractive interests to marginalize the Greens in Australian politics.\
Tactical Evolution: Tracks the shift from simple policy disagreement to sophisticated character assassination and institutional isolation.\
Causal Signature: Identifies the patterns of media coordination and funding flows used to execute the suppression strategy.""",

        r"""### [AFL Related Donations／Receipts (Sorted & Totalled).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Donors & Influence\AFL Related Donations／Receipts (Sorted & Totalled).md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Cultural Capital Audit: Forensically totals the financial contributions between the AFL and political entities.\
Soft Power Leverage: Documents the use of sporting institutions as relays for political messaging and elite network building.\
Transactional Ritual: Evaluates the role of corporate box attendance and sponsorship in facilitating off-the-record wealth and influence transfers.""",

        r"""### [Analyzing Political Collusion and Strategy.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Security & Legal\Analyzing Political Collusion and Strategy.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Collusion Forensics: Analyzes the strategic interaction between supposedly opposing political parties to preserve extractive systemic rules.\
Rules of the Game: Documents the unwritten protocols used by political elites to neutralize 'Maximiser' challenges to their dominance.\
Restoring Integrity: Proposes a legal and hegemonic framework for detecting and criminalizing intra-systemic collusion.""",

        r"""### [Analyzing Australia's Neo-Nazi Response.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Security & Legal\Analyzing Australia's Neo-Nazi Response.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Response Paradox Audit: Analyzes the disproportionate state response to small-scale extremism as a pretext for broader surveillance.\
Manufactured Threat: Documents the role of media amplification in creating an environment of fear that justifies the removal of civil liberties.\
Surveillance Vector: Evaluates how the 'Neo-Nazi' narrative is used as a tactical shield for the implementation of the Minimisation Plan's control goals.""",

        r"""### [Hegemonic Analysis -  Voting Record Subject -  Terrorism and Other Legislation Amendment .md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Security & Legal\Hegemonic Analysis -  Voting Record Subject -  Terrorism and Other Legislation Amendment .md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Legislative Audit: Performs a hegemonic assessment of specific security legislation and the accompanying parliamentary voting records.\
Liquidation of Liberty: Analyzes how 'anti-terror' clauses are used to remove judicial oversight and establish administrative dominance.\
Voting Trajectory: Maps the consistency of political actors in supporting or resisting the expansion of the suppressive state-will.""",

        r"""### [The Universal Fear Template -  Improper Implementation and Inevitable Use.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Security & Legal\The Universal Fear Template -  Improper Implementation and Inevitable Use.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Fear Engine Forensics: Formalizes the 'Universal Fear Template' used by adversarial actors to induce systemic social and cognitive paralysis.\
Misuse of Metrics: Analyzes how legitimate concerns are weaponized into unresolvable 'Doom' narratives to exhaust public agency.\
Invevitable Result: Describes the trajectory toward authoritarian stability once the population has been sufficiently primed by the template.""",

        r"""### [The Path to Redemption -  A VFT Deprogramming Methodology.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Security & Legal\The Path to Redemption -  A VFT Deprogramming Methodology.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Deprogramming Protocol: Outlines a systematic methodology for restoring cognitive autonomy to individuals captured by Minimiser delusions.\
Restoring Ratios: Provides technical tools for re-balancing an individual's worldview scope and reactivating their hegemonic judgment.\
Pathway to Clarity: Describes the sequence of semantic and historical corrections required to break the 'Hum' of ideological capture.""",

        r"""### [Government Security Response Strategy -  Post-Bondi ＂Crisis Governance＂.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Security & Legal\Government Security Response Strategy -  Post-Bondi ＂Crisis Governance＂.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Crisis Governance Audit: Analyzes the Australian government's response to the Bondi events as a move toward a permanent 'Emergency' state.\
Surveillance Acceleration: Documents the rapid deployment of digital tracking and facial recognition tools under the cover of public safety.\
Institutional Inversion: Evaluates the shift from proactive security toward reactive suppression of civilian movement and digital agency.""",

        r"""### [Hegemonic Analysis -  The Bondi 7x7 Fractal Interrogative.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Security & Legal\Hegemonic Analysis -  The Bondi 7x7 Fractal Interrogative.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Forensic Event Audit: Applies the 7x7x7 fractal matrix to the Bondi events to detect anomalies and identify underlying influence vectors.\
Vector Conflict: Analyzes the discrepancy between official narratives and the observed physical and lyrical data of the event.\
Deception Forensics: Provides a detailed tally of hypocrisy gaps in the administrative response to the crisis.""",

        r"""### [A VFT Analysis of Hypnosis -  The Art of the Attraction Tensor.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Security & Legal\A VFT Analysis of Hypnosis -  The Art of the Attraction Tensor.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Hypnosis Forensics: Formalizes the mechanics of social and individual hypnosis through the lens of the attraction tensor.\
Bypassing Reason: Analyzes the use of frequency and narrative repetition to induce high-will, low-morality states in a target population.\
Deprogramming Shield: Proposes the use of VFT axioms as a primary defense against the tactical use of psychological capture.""",

        r"""### [Hegemonic Assessment Report -  The Bondi Event (Dec 2025).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Security & Legal\Hegemonic Assessment Report -  The Bondi Event (Dec 2025).md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Event Audit Verdict: Provides the final hegemonic assessment of the Bondi event and its systemic consequences for Australian society.\
Tactical Hit Check: Identifies the event as a significant tactical victory for Minimiser actors seeking to expand state-level control.\
Restoring Sovereignty: Evaluates the primary paths for reclaiming national agency and institutional trust following the crisis."""
    ])

    summaries.extend([
        r"""### [Analyzing Albanese's Social Media Ban.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Anthony Albanese\Analyzing Albanese's Social Media Ban.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Ban Policy Audit: Performs a hegemonic assessment of the Prime Minister's proposed ban on social media for minors.\
Pretext for Control: Analyzes how the 'Protect the Children' narrative is used as a cover forImplementing mandatory digital ID systems.\
Sovereign Risk: Evaluates the consequences of centralizing the digital life of the population under tech-giant and state supervision.""",

        r"""### [Platform vs. Practice -  An Audit of the Albanese Labor Government's Fidelity to its Stated Agenda (2021-Present).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Anthony Albanese\Platform vs. Practice -  An Audit of the Albanese Labor Government's Fidelity to its Stated Agenda (2021-Present).md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Fidelity Audit: Measures the discrepancy between the Labor government's 'Maximiser' campaign promises and its 'Minimiser' policy outcomes.\
Tragic Gap Analysis: Identifies specific areas where external geopolitical pressure or donor influence forced a retreat from reform.\
Institutional Stasis: Documents the pattern of strategic inaction on housing, energy, and digital rights as a metric of state capture.""",

        r"""### [Albanese Leadership and Policy Analysis part 2.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Anthony Albanese\Albanese Leadership and Policy Analysis part 2.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Leadership Audit (Part 2): Continues the assessment of the Prime Minister's trajectory, focusing on the second half of his tenure.\
Geopolitical Shift: Analyzes the government's alignment with the Asian Pivot and the impact on Australian security autonomy.\
Verdict on Will: Evaluates whether the subject possesses the proactive will required to serves as a shield for the national interest.""",

        r"""### [Albanese Leadership and Policy Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Anthony Albanese\Albanese Leadership and Policy Analysis.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Core Leadership Audit: Provides the foundational hegemonic assessment of the Prime Minister's leadership style and policy goals.\
Alignment of Intent: Maps the subject's stated values against the 343 vectors of the Australian Kanon.\
Signature of Capture: Documents early indicators of institutional reorientation toward donor and foreign-aligned priorities.""",

        r"""### [Strategic Deconstruction of Prime Minister Albanese's United Nations General Assembly Address.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Anthony Albanese\Strategic Deconstruction of Prime Minister Albanese's United Nations General Assembly Address.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Speech Forensics: Deconstructs the subject's UN address to uncover the underlying geopolitical and moral signals being sent to the 'Board'.\
Credentialing the Proxy: Analyzes the use of 'Globalist' jargon to validate the subject's status as a compliant middle manager for transnational interests.\
Erasure of Sovereignty: Documents the tactical omission of specific Australian national interests in favor of vague internationalist cooperation.""",

        r"""### [Australian Political Email List Compilation.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Media & Communications\Australian Political Email List Compilation.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Direct Contact Database: Provides a consolidated list of verified email addresses for Australian federal and state representatives.\
Removing Gatekeepers: Documents the naming conventions and administrative barriers used by the state to shield itself from public inquiry.\
Operational Resource: Acts as the primary tool for large-scale digital advocacy and hegemonic auditing by the citizenry.""",

        r"""### [Australian Media Entrapment Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Media & Communications\Australian Media Entrapment Analysis.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Media Entrapment Forensics: Analyzes how Australian media networks are captured by corporate and foreign interests through ownership and funding.\
Narrative Shielding: Documents the systematic suppression of 'Maximiser' stories that threaten the status quo of extractive industrial power.\
Cognitive Enclosure: Evaluates the role of media in creating a 'Closed-Loop' reality for the population that excludes sovereign alternatives.""",

        r"""### [Investigating Internet Ban Control Scheme.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Media & Communications\Investigating Internet Ban Control Scheme.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Digital Siege Forensics: Investigates the proposed Australian internet regulations as a primary instrument of the Minimisation Plan.\
Liquidation of Anonymity: Documents how mandatory ID verification for digital services destroys the citizen's capacity for independent inquiry.\
Centralized Control: Analyzes the goal of the scheme as the establishment of a state-controlled 'Information Chokepoint' to manage the national reality.""",

        r"""### [Collated Australian Political Email List .md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Media & Communications\Collated Australian Political Email List .md
**Categories**: Plane: Q3 WHERE; Node: Society; Tags: Community, Fellowship, Group, Network, Public, Social, Society
**Summary**:
Contact Directory: Consolidates verified email addresses for all members of the House of Representatives and the Senate.\
Jurisdictional Mapping: Provides state-level contact lists for NSW, VIC, QLD, and WA parliaments to facilitate targeted advocacy.\
Transparency Tool: Designed to empower citizens to bypass bureaucratic buffers and communicate directly with their elected servants.""",

        r"""### [Chinese Media Reactions To Australian Actions.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Media & Communications\Chinese Media Reactions To Australian Actions.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Adversarial Media Monitoring: Analyzes the official and state-aligned Chinese media responses to Australian policy and security decisions.\
Signaling Verification: Documents the use of specific rhetorical themes to signal approval or displeasure to captured Australian elites.\
Validation of Impact: Measures the effectiveness of Australian 'Maximiser' actions by tracking the intensity of adversarial media backlash.""",

        r"""### [Five Eyes Internet Control Research.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Media & Communications\Five Eyes Internet Control Research.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Intelligence Network Audit: Investigates the role of the Five Eyes network in developing and deploying global information control tools.\
Protocol Synchronization: Documents the coordinated move across Western nations toward mandatory digital ID and restricted internet access.\
Minimiser Convergence: Evaluates how legitimate security coordination is co-opted to achieve the Minimisation Plan's goal of domestic suppression.""",

        r"""### [A Comprehensive Directory of the Australian News Media Landscape -  Corporate, Regional, and Community Contacts.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Media & Communications\A Comprehensive Directory of the Australian News Media Landscape -  Corporate, Regional, and Community Contacts.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Media Directory: Provides a detailed list of contact points for every major, regional, and independent media outlet in Australia.\
Strategic Engagement: Identifies the primary channels for bypassing corporate gatekeepers and reaching local communities with 'Maximiser' narratives.\
Network Analysis: Acts as a foundational resource for auditing the responsiveness and independence of the Australian fourth estate.""",

        r"""### [Australian Political Email List Expansion.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Media & Communications\Australian Political Email List Expansion.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Database Maintenance: Documents the addition of local government and administrative board contact points to the master political email list.\
Expanding Reach: Analyzes the role of local-level decision-makers in either facilitating or resisting Minimiser subversion of national policy.\
Integrity Check: Acts as a resource for citizen-led audits of the entire administrative hierarchy of the Australian state.""",

        r"""### [Verifying Australian Political Emails.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Media & Communications\Verifying Australian Political Emails.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Database Verification: Records the technical process used to certify the accuracy of the contact data in the Australian political email list.\
Ensuring Signal: Documents the removal of dead or redirected addresses to ensure that citizen inquiries reach their intended human targets.\
Audit History: Provides a timestamped record of database updates to maintain the reliability of the citizen advocacy tool.""",

        r"""### [Peta Credlin -  Political Operative Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Peta Credlin\Peta Credlin -  Political Operative Analysis.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Operative Audit: Performs a hegemonic assessment of the subject's role as a media figure and former political staffer.\
Narrative Engineering: Analyzes the subject's use of inflammatory and divisive rhetoric to maintain donor-aligned 'Minimiser' policy focus.\
Influence Relay: Evaluates the subject's role in coordinating media attacks against 'Maximiser' reform within the Australian center-right."""
    ])

    summaries.extend([
        r"""### [Dan Andrews part 1.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Dan Andrews\Dan Andrews part 1.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Victorian Leadership Audit: Performs an initial hegemonic assessment of Dan Andrews' tenure as Premier of Victoria.\
Sovereign Pivot: Analyzes the decision to sign the Belt and Road Initiative (BRI) agreement as a foundational move toward state-level capture.\
Centralization of Will: Documents the use of emergency powers to expand executive authority and bypass institutional oversight.""",

        r"""### [Dan Andrews -  Network Analysis and Influence Vectors.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Dan Andrews\Dan Andrews -  Network Analysis and Influence Vectors.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Influence Network Audit: Forensically maps the financial and political links between the subject and specific foreign/corporate interests.\
Logistical Relay: Documents the role of the subject in facilitating the acquisition of key Victorian infrastructure by adversarial entities.\
Strategic Entrapment: Evaluates the use of unpayable state-level debt for mega-projects as a method of cementing long-term capture.""",

        r"""### [Victorian Premier Dossier Update.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Dan Andrews\Victorian Premier Dossier Update.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Dossier Maintenance: Updates the hegemonic assessment of the Victorian Premiership following a change in leadership.\
Continuity of Vector: Documents the persistence of 'Minimiser' policy goals under the new administration, signaling institutional capture.\
Administrative Cleanup: Analyzes the removal of specific checks and balances designed to shield the state from strategic subversion.""",

        r"""### [Dan Andrews part 2 Chinese Reaction.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Dan Andrews\Dan Andrews part 2 Chinese Reaction.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Adversarial Validation: Analyzes the official Chinese media response to the subject's policy decisions and eventual exit from politics.\
Signaling Forensics: Documents the use of specific praise and support by adversarial actors to validate their compliant domestic proxies.\
Impact Audit: Measures the subject's effectiveness as an instrument of the Minimisation Plan by tracking the intensity of foreign approval.""",

        r"""### [Anatomy of a Fall -  Demolition, Incompetence, and the Unmaking of Australia's Resource Tax.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\Anatomy of a Fall -  Demolition, Incompetence, and the Unmaking of Australia's Resource Tax.md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Policy Demolition Forensics: Analyzes the destruction of the Resource Super Profits Tax (RSPT) as a primary tactical victory for Minimiser actors.\
Manufactured Incompetence: Documents the role of corporate-funded media in framing sovereign wealth preservation as administrative failure.\
Liquidation of Future: Evaluates the long-term cost to the Australian people of losing sovereign control over the nation's natural wealth.""",

        r"""### [A Strategic Workforce Analysis for Australia's Energy Transition.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\A Strategic Workforce Analysis for Australia's Energy Transition.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Workforce Audit: Provides a detailed assessment of the skills and personnel required to execute the National Energy Network transition.\
Industrial Gap Analysis: Identifies specific shortages in sovereign manufacturing and technical expertise that threaten the project's success.\
Strategic Recommendation: Outlines the educational and training requirements for building a resilient national clean energy workforce.""",

        r"""### [Policy Deep Dive -  The National Construction Network (NCN).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\Policy Deep Dive -  The National Construction Network (NCN).md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
NCN Proposal: Outlines a plan to nationalize and standardize the construction of critical residential and industrial infrastructure.\
Removing Middlemen: Documents the use of state-level logistics to bypass captured private contractors and lower development costs.\
Systemic Efficiency: Evaluates the proposal's impact on national housing supply and industrial sovereign capability.""",

        r"""### [Reconnecting the Central West -  A Feasibility Study and Return on Investment Analysis for the Dubbo-Coonabarabran-Baradine Rail Corridor.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\Reconnecting the Central West -  A Feasibility Study and Return on Investment Analysis for the Dubbo-Coonabarabran-Baradine Rail Corridor.md
**Categories**: Plane: Q7 EFFECT; Node: Society; Tags: Community, Group, Network, Public, Social, Society
**Summary**:
Rail Feasibility Audit: Forensically calculates the positive ROI for restoring critical regional rail infrastructure in New South Wales.\
Logistical Resilience: Documents how regional rail connectivity reduces dependency on fossil-fuel-intensive road transport and stabilizes the inland economy.\
Restoring Local Identity: Evaluates the role of shared infrastructure in revitalizing regional communities and resisting the drain of the cities.""",

        r"""### [Gas vs Solar Australia Costs␊.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\Gas vs Solar Australia Costs␊.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Comparative Cost Audit: Provides a data-driven comparison between domestic gas power and distributed rooftop solar within the Australian market.\
Economic Verdict: Documents the massive financial advantage of national electrification over the continued extraction of fossil fuel resources.\
Subsidized Extraction: Analyzes the hidden costs of state support for the gas industry relative to the self-funding potential of the NEN.""",

        r"""### [Australian Environmental Policy Deep Dive.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\Australian Environmental Policy Deep Dive.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Environmental Audit: Performs a hegemonic assessment of Australia's current environmental protection laws and their outcomes.\
Regulatory Capture: Documents the consistent pattern of prioritizing extractive industrial profit over the preservation of the national biosphere.\
Trajectory for Recovery: Proposes a framework for re-aligning environmental policy with the VFT principles of universal benefit and long-term stability.""",

        r"""### [Hegemonic Analysis -  The Suburban Rail Loop (SRL) Pause Policy.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\Hegemonic Analysis -  The Suburban Rail Loop (SRL) Pause Policy.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
SRL Pause Audit: Performs a hegemonic assessment of the policy to pause or cancel segments of the Victorian Suburban Rail Loop.\
Fiscal Responsibility: Analyzes the decision as a potential move toward restoring state-level solvency and reducing unpayable debt.\
Strategic Reset: Evaluates the impact of the rail pause on national infrastructure integrity and the role of foreign commercial capture.""",

        r"""### [A Strategic Workforce Analysis for Australia's Energy Transition (2026-2034).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\A Strategic Workforce Analysis for Australia's Energy Transition (2026-2034).md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Long-term Workforce Roadmap: Updates the personnel requirements for the NEN transition, focusing on the critical 2026-2034 implementation window.\
Sovereign Capability: Documents the move toward domestic manufacturing and technical training as a primary defense against supply chain subversion.\
Economic Multiplier: Forecasts the positive impact of national clean energy jobs on local communities and the overall GDP.""",

        r"""### [A Case Study in Post-Democratic Governance -  The Political Economy of the Tasmanian Stadium Mandate.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\A Case Study in Post-Democratic Governance -  The Political Economy of the Tasmanian Stadium Mandate.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Mandate Forensics: Analyzes the Tasmanian stadium project as a definitive case study in elite-led, post-democratic governance.\
Liquidation of Consent: Documents how the state bypassed public consensus and existing fiscal safeguards to serve private commercial interests.\
Signature of Capture: Identifies the use of 'prestige' projects to facilitate the transfer of public funds into unmonitored private networks.""",

        r"""### [From Sovereign Capability to Global Exporter -  A Strategic Roadmap for Australia's National Sodium-Ion Battery Manufacturing Initiative (2026-2040).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\From Sovereign Capability to Global Exporter -  A Strategic Roadmap for Australia's National Sodium-Ion Battery Manufacturing Initiative (2026-2040).md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Battery Initiative Roadmap: Outlines a strategic plan to establish Australia as a global leader in sodium-ion battery production.\
Resource Mastery: Analyzes how utilizing domestic raw materials for finished high-tech products reverses the extractive 'Resource Colony' model.\
Global Market Pivot: Documents the potential for Australia to supply clean energy storage tech to international partners, securing global influence.""",

        r"""### [From Sovereign Capability to Global Exporter -  An Aggressive Industrial Roadmap for Australia's NEN Manufacturing Initiative.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\From Sovereign Capability to Global Exporter -  An Aggressive Industrial Roadmap for Australia's NEN Manufacturing Initiative.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Aggressive Industrialization: Proposes a high-velocity framework for building a sovereign manufacturing sector to support the NEN.\
Strategic Counter-Pivot: Documents the use of domestic production to break the dependency on foreign-aligned supply chains for critical energy tech.\
Economic Sovereignty: Evaluates the role of finished-goods export in restoring Australia's trade balance and national independent will."""
    ])

    summaries.extend([
        r"""### [Dubbo-Baradine ROI Detailed Analysis␊.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Australia\Infrastructure & Energy\Dubbo-Baradine ROI Detailed Analysis␊.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Forensic ROI Audit: Provides a detailed line-by-line financial analysis for the restoration of the Dubbo-Baradine regional rail line.\
Systemic Value Calculation: Documents how regional rail connectivity reduces long-term road maintenance costs and state-level emissions.\
Economic Stimulus: Forecasts the positive return to the state through increased agricultural efficiency and regional town revitalization.""",

        r"""### [The Minimisation Plan -  A Psochic Hegemony Analysis of the Sino-Russian Rhizomatic War Against the West.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\The Minimisation Plan -  A Psochic Hegemony Analysis of the Sino-Russian Rhizomatic War Against the West.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Grand Strategy Forensics: Provides a high-level assessment of the global campaign to minimize Western sovereignty and institutional will.\
Rhizomatic War Mechanics: Analyzes the use of non-linear subversion, proxy conflict, and economic entrapment to disable state function.\
Hegemonic Result: Documents the trajectory toward total administrative integration of host nations into the adversarial field.""",

        r"""### [The Dragon's Shadow Network -  An Analysis of China's Role in the Indirect Geopolitical Nexus Between Israel and Hamas.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\China Nexus\The Dragon's Shadow Network -  An Analysis of China's Role in the Indirect Geopolitical Nexus Between Israel and Hamas.md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Nexus Analysis: Forensically examines China's role in coordinating and supporting regional conflicts to exhaust Western resources.\
Strategic Alignment: Documents how the Middle Eastern quagmire serves the goals of the Asian Pivot by diverting US military and financial will.\
Influence Relay Audit: Identifies the specific logistical and diplomatic channels used to sustain the shadow network of adversarial proxies.""",

        r"""### [China's Response To Neo-Nazism Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\China Nexus\China's Response To Neo-Nazism Analysis.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Narrative Inversion audit: Analyzes the adversarial use of Western extremism reports to validate their own authoritarian stability model.\
Propaganda Vector: Documents the framing of democratic freedoms as inherently leading to social chaos and the rise of dangerous ideologies.\
Strategic Discrediting: Evaluates the goal of the operation as the total erosion of Western global moral authority in the non-aligned world.""",

        r"""### [Tesla in 2025 -  Analyzing the AI Pivot and the Indispensable China Nexus.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\China Nexus\Tesla in 2025 -  Analyzing the AI Pivot and the Indispensable China Nexus.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
Tesla China Nexus Audit: Analyzes the entity's 2025 strategy through the lens of its dependency on Chinese industrial and financial will.\
AI Transition Forensics: Investigates the pivot to robotics as a method for fulfilling Chinese strategic tech-transfer requirements.\
Geopolitical Capture: Documents the consistent alignment between the entity's leadership and the interests of the Sino-Russian axis.""",

        r"""### [Sino-Russian Alliance Psyops and Conspiracy Theories.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\China Nexus\Sino-Russian Alliance Psyops and Conspiracy Theories.md
**Categories**: Plane: Q2 WHAT; Node: Communication; Tags: Connection, Language, Linguistics, Media, Rhetoric, Semantics, Symbology
**Summary**:
Psyop Forensics: Deconstructs the coordinated dissemination of conspiracy theories designed to bankrupt the Reserve Currency of Trust.\
Alignment of Narratives: Documents the tactical synchronization between Russian and Chinese information operations in the Western field.\
Systemic Exhaustion: Evaluates the role of epistemic nihilism in disabling the host's capacity to recognize and respond to strategic subversion.""",

        r"""### [China Atrocities Research Request.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\China Nexus\China Atrocities Research Request.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Investigative Directive: Outlines the requirement for detailed forensic documentation of adversarial state-level human rights abuses.\
Historical Accountability: Proposes the use of VFT metrics to analyze the systemic consequences of centralized suppressive will.\
Counter-Narrative Engine: Designed to provide the evidentiary base required to reclaim moral authority from captured institutional gatekeepers.""",

        r"""### [review all the documents against ＂China-Russia Mi....md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\China Nexus\review all the documents against ＂China-Russia Mi....md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Cross-Document Audit: Summarizes the findings of an exhaustive review of the repository against the 'China-Russia Minimisation' framework.\
Pattern Validation: Documents the consistent recurrence of Minimiser tactical signatures across disparate folders and research streams.\
Systemic Verdict: Concludes that the evidence assembled in the knowledgebase points toward a coordinated and terminal strategic siege.""",

        r"""### [Sub-bucket 5.1 -  Foundational Vulnerabilities (Howard Era, Tampa, ＂Children Overboard＂).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\TacticalBuckets\Sub-bucket 5.1 -  Foundational Vulnerabilities (Howard Era, Tampa, ＂Children Overboard＂).md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Foundational Erosion Audit: Analyzes the late 20th-century Australian policy decisions that created systemic vulnerabilities for future capture.\
Weaponized Trauma: Documents the role of the 'Tampa' and 'Children Overboard' events in establishing a high-will, exclusionary national vector.\
Causal Legacy: Evaluates how these historical fractures have been exploited by Minimiser actors to justify institutional reorientation.""",

        r"""### [Sub-bucket 4.1 -  The ＂Ukraine Gambit＂ (Russia as ＂Battering Ram＂, Demographic Reset).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\TacticalBuckets\Sub-bucket 4.1 -  The ＂Ukraine Gambit＂ (Russia as ＂Battering Ram＂, Demographic Reset).md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Ukraine Strategic Audit: Analyzes the war in Ukraine as a primary instrument for the strategic exhaustion of Western industrial and moral capacity.\
Russia as Battering Ram: Documents the use of kinetic conflict to break existing international rules and enable a broader state-capture model.\
Demographic Reset Vector: Evaluates the role of mass displacement in straining European institutional stability and institutional cohesion.""",

        r"""### [Sub-bucket 3.2 -  The ＂Debt Weapon＂ (Gradual Bleed of US Treasuries).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\TacticalBuckets\Sub-bucket 3.2 -  The ＂Debt Weapon＂ (Gradual Bleed of US Treasuries).md
**Categories**: Plane: Q5 HOW; Node: Physics; Tags: Dynamics, Energy, Forces, Gravity, Kinetics, Mechanics, Physics
**Summary**:
Debt Weapon Forensics: Analyzes the use of Western sovereign debt as a primary instrument of strategic financial attrition.\
Gradual Bleed Mechanism: Documents the coordinated selling and redirection of US Treasury holdings by the CRINK axis.\
Systemic Fragility: Evaluates the point where the cost of debt service disables the host's capacity for defense and social investment.""",

        r"""### [Sub-bucket 1.1 -  Philosophical Foundations .md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\TacticalBuckets\Sub-bucket 1.1 -  Philosophical Foundations .md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Doctrine Audit: Formalizes the philosophical underpinnings of the global Minimisation Plan, focusing on anti-hegemonic rhizomatic war.\
Erasure of Logos: Analyzes the role of postmodern deconstruction in disabling the Western capacity for fact-based judgment.\
Foundational Strategy: Outlines the move from 1945 rules-based order toward a 21st-century model of high-will, low-morality statecraft.""",

        r"""### [Sub-bucket 2.3 -  The COVID-19 Simulacrum (Lab Leak Hypothesis).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\TacticalBuckets\Sub-bucket 2.3 -  The COVID-19 Simulacrum (Lab Leak Hypothesis).md
**Categories**: Plane: Q3 WHERE; Node: Sociology; Tags: Anthropology, Culture, Demographics, Human-Ecology, Interpersonal, Norms, Sociology
**Summary**:
Simulacrum Forensics: Analyzes the COVID-19 pandemic as a strategic catalyst for institutional trust bankruptcy and social polarization.\
Lab Leak Vector: Documents the tactical use of conflicting narratives to disable the host's capacity for coherent public health response.\
Outcome Audit: Measures the realized strategic damage to Western economic and cognitive stability following the pandemic response.""",

        r"""### [Sub-bucket 5.4 -  The AUKUS Gambit & Strategic Exhaustion.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\TacticalBuckets\Sub-bucket 5.4 -  The AUKUS Gambit & Strategic Exhaustion.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
AUKUS Strategic Audit: Updates the analysis of the security pact as a target for strategic overextension and sovereign minimization.\
IMEC Derailment link: Explains how Pacific-focused military commitments prevent the consolidation of Western-aligned economic corridors.\
Exhaustion Vector: Documents the role of high-cost military integration in depleting the host's available energy for domestic resilience.""",

        r"""### [minimisation phase summary.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\Versions\minimisation phase summary.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Strategic Phase Audit: Provides a high-level summary of the progression from infiltration toward the final liquidation of host sovereignty.\
Operational Indicators: Outlines the specific tactical signatures associated with each phase of the global Minimisation strategy.\
Verdict on Progress: Evaluates the current state of Western institutional capture relative to the Asian Pivot's end-goals."""
    ])

    summaries.extend([
        r"""### [China-Russia Minimisation Plan Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\Versions\China-Russia Minimisation Plan Analysis.md
**Categories**: Plane: Q1 WHO; Node: Conscience; Tags: Accountability, Conviction, Equity, Internal Judgment, Jurisprudance, Justice, Law
**Summary**:
CRINK Alliance Audit: Forensically examines the coordination between Beijing and Moscow to execute a terminal siege of Western systems.\
Strategic Incoherence: Documents how adversarial operations exploit the inherent contradictions in Western liberal democracy.\
Endgame Forecast: Identifies the trajectory toward a post-Western international order governed by the principles of the Asian Pivot.""",

        r"""### [Consolidating Minimisation Plan Analysis.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\Versions\Consolidating Minimisation Plan Analysis.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Consolidated Strategic Audit: Synthesizes various investigative streams into a single definitive account of the Minimisation Plan.\
Pattern Recognition: Documents the recurring tactical signatures of subversion in economic, informational, and institutional domains.\
Framework Validation: Uses global case studies to reinforce the predictive power of the VFT and Minimisation analytical models.""",

        r"""### [Deconstructing Minimisation Plan Theories.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\Versions\Deconstructing Minimisation Plan Theories.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Strategic Deconstruction: Performs a critical analysis of the various theories and reports assembled under the Minimisation Plan umbrella.\
Fidelity Check: Measures the internal consistency and evidentiary grounding of each investigative stream.\
Operational Triage: Prioritizes conflict vectors based on their immediate threat to national sovereign integrity.""",

        r"""### [The Minimisation Plan -  A Strategic Briefing.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\Versions\The Minimisation Plan -  A Strategic Briefing.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
High-level Executive Briefing: Provides a concise overview of the Asian Pivot's campaign of socioeconomic and informational attrition.\
Resource Sink Strategy: Analyzes the use of manufactured crises to deplete Western military, financial, and moral capacity.\
Subversion Roadmap: Outlines the phases of institutional capture and the role of domestic proxies in enabling the national unravelling.""",

        r"""### [Minimisation Plan Theory Report.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\Versions\Minimisation Plan Theory Report.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Theoretical Foundation Audit: Formally defines the 'Minimisation Plan' as an algorithmic approach to regional and global dominance.\
Rhizomatic Logistics: Analyzes the use of non-state actors and corporate entities as primary logistical relays for subversion.\
Systemic Result: Documents the trajectory toward total administrative integration of target nations into the adversarial field.""",

        r"""### [Minimisation Plan Data Analysis and Research.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\Versions\Minimisation Plan Data Analysis and Research.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Data-driven Strategic Audit: Provides a quantitative assessment of the Minimisation Plan's execution using market and media data.\
Pattern Identification: Documents the correlation between adversarial signaling and real-world domestic policy shifts in the West.\
Evidentiary Base: Acts as a foundational resource for verifying the tactical signatures of state capture and influence operations.""",

        r"""### [The Minimisation Plan -  A Comprehensive Analysis of the Russia-China-Iran-DPRK-Syria Alliance Web and its Multi-Front Strategy (1948-Present).md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\Versions\The Minimisation Plan -  A Comprehensive Analysis of the Russia-China-Iran-DPRK-Syria Alliance Web and its Multi-Front Strategy (1948-Present).md
**Categories**: Plane: Q6 CAUSE; Node: History; Tags: Archives, Chronology, Context, History, Past, Record, Timeline
**Summary**:
Generational Alliance Audit: Provides a long-term historical analysis of the coordination within the 'CRINK' axis.\
Multi-Front Strategy: Documents the use of simultaneous conflicts across Europe, the Middle East, and Asia to exhaust Western resources.\
Causal Trajectory: Evaluates the shift from ideological competition toward a unified model of non-linear institutional demolition.""",

        r"""### [Minimisation Plan Analysis and Integration.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\GrandStrategy\Versions\Minimisation Plan Analysis and Integration.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Analytical Integration Audit: Summarizes the findings of the exhaustive cross-folder review of the Minimisation Plan research.\
Tactical Signature Record: Consolidates the identified patterns of subversion in economic, informational, and security domains.\
Systemic Recommendation: Identifies the primary vectors for reclaiming institutional trust and national sovereignty.""",

        r"""### [The_7x7x7_Collapse_Matrix.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Collapse\Taxonomy\The_7x7x7_Collapse_Matrix.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Collapse Taxonomy: Formalizes the 7x7x7 matrix for predicting and analyzing state failure across all planes of existence.\
Indicator Mapping: Documents the specific hegemonic variables and threshold values that signal an imminent systemic snap point.\
Forensic Utility: Provides a diagnostic tool for researchers to identify underlying collapse vectors in supposedly stable institutions.""",

        r"""### [The_Meaning_Aligned_Collapse_Matrix.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Collapse\Taxonomy\The_Meaning_Aligned_Collapse_Matrix.md
**Categories**: Plane: Q4 WHY; Node: Ethics; Tags: Code, Deontology, Ethics, Integrity, Morality, Philosophy, Virtue
**Summary**:
Lyrical Collapse Audit: Analyzes the role of narrative and meaning erosion in facilitating systemic institutional failure.\
Loss of Purpose: Documents how the destruction of shared national myths and values disables the collective will to survive.\
Resonance Breakdown: Evaluates the impact of narrative dissonance on the long-term stability of the social contract.""",

        r"""### [The_Interrogative_Collapse_Matrix.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Collapse\Taxonomy\The_Interrogative_Collapse_Matrix.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Inquiry-based Failure Model: Maps the stages of state failure across the seven recursive meta-questions of the VFT framework.\
Epistemic Erasure: Analyzes the role of fact-based inquiry suppression in blinding the host to its own terminal decay.\
Diagnostic Protocol: Outlines a method for researchers to use the interrogative stack to probe for hidden collapse signatures.""",

        r"""### [Collapse_Matrix_7x7x7_Part2.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Collapse\Taxonomy\Collapse_Matrix_7x7x7_Part2.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Failure Matrix (Part 2): Continues the formalization of collapse indicators, focusing on the method and foundation planes.\
Administrative Decay: Documents the shift from results-oriented government toward procedural stagnation and self-preservation.\
Systemic Fragility: Measures the impact of increasing bureaucratic complexity on the system's capacity to absorb external stress.""",

        r"""### [Collapse_Matrix_7x7x7_Part3.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Collapse\Taxonomy\Collapse_Matrix_7x7x7_Part3.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Failure Matrix (Part 3): Completes the formalization of the 7x7x7 collapse model, focusing on the result and passion planes.\
Tribal Realization: Analyzes the final stage of failure where collective identity dissolves into hostile, unresolvable tribal conflicts.\
Homeostatic Ruin: Describes the end-state where the system maintains stability only through total authoritarian suppression or collapse.""",

        r"""### [Collapse_Matrix_7x7x7_Part1.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\Collapse\Taxonomy\Collapse_Matrix_7x7x7_Part1.md
**Categories**: Plane: Q5 HOW; Node: Logic; Tags: Algorithms, Calculus, Computation, Geometry, Logic, Mathematics, Statistics
**Summary**:
Failure Matrix (Part 1): Initiates the formalization of the 7x7x7 collapse matrix, covering the identity, definition, and land planes.\
Sovereign Erosion: Documents the early-stage indicators of state capture and the loss of independent national agency.\
Territorial Instability: Analyzes the role of resource mismanagement and border erosion in seeding foundational failure."""
    ])

    summaries.extend([
        r"""### [NEN Financial Accelerants.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\NEN Financial Accelerants.md
**Categories**: Plane: Q5 HOW; Node: Knowledge; Tags: Data, Information, Instruction, Knowledge, Learning, Pedagogy, Prudence
**Summary**:
Monetising Climate Action: Outlines the strategy for leveraging emissions reduction through the Australian Carbon Credit Unit (ACCU) market.\
Production Rebate for Renewable Technology: Proposes a tax instrument (New PRRT) to de-risk investment in domestic advanced manufacturing.\
Corporate Partnership Model: Establishes a framework for direct partnership between the NEN and strategic industrial suppliers.""",

        r"""### [tesla vector.md] (2026-05-24)
**Path**: _VFT MD\WWSUTRU\EconomicWarfare\tesla vector.md
**Categories**: Plane: Q1 WHO; Node: Psychology; Tags: Behavior, Mind, Subconscious, Understanding
**Summary**:
The Tesla Vector: Reframes Tesla as a cultivated asset of China, patiently seeded to become a future economic weapon.\
Surgical Capitalism: Describes the mechanism of state-sponsored valuation inflation designed to engineer systemic Western vulnerability.\
The Driverless Deception: Identifies the failure of Level 5 autonomy as the primary catalyst for shattering Elon Musk's narrative infallibility."""
    ])
