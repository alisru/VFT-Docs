import json, os

data_path = 'bluesky_bot/tests/vanilla_benchmark_10_stories.json'
with open(data_path, 'r', encoding='utf-8') as f:
    benchmarks = json.load(f)

lines = []
lines.append('# The Intelligence of Structured Data: Benchmarking the 5-Phase Convergence Tensor Against Unconstrained LLM Baselines\n')
lines.append('**Author / Framework:** Gnostic Actualism & Vector Field Theory (VFT) Research  ')
lines.append('**Engine Baseline:** Vertex AI Gemini 3.7 Flash (`gemini-3.7-flash`)  ')
lines.append('**Benchmark Date:** August 2026  ')
lines.append('**Artifact Location:** [`bluesky_bot/research_paper_structured_data_convergence_vs_vanilla.md`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/research_paper_structured_data_convergence_vs_vanilla.md)  ')
lines.append('**Dataset Source:** 10 Multi-Domain Live News Stories with 100% Full-Text Scrapes ([`vanilla_benchmark_10_stories.json`](file:///e:/Vector%20Field%20Theory/VFT%20Docs/bluesky_bot/tests/vanilla_benchmark_10_stories.json))\n')
lines.append('---\n')
lines.append('## Abstract\n')
lines.append('When commercial Large Language Models (LLMs) are asked to "Judge this story" with unconstrained natural language prompts, they exhibit severe epistemic failure modes driven by enterprise safety training, liability aversion, and the absence of a structural coordinate system.\n')
lines.append('In this empirical benchmark across 10 multi-domain live stories (each fed with its **100% full, untruncated article text up to 12,300+ characters**), we demonstrate that **unconstrained Vertex AI Gemini 3.7 Flash does not evaluate the structural morality, energetic direction, or systemic extraction of events**. Instead, it defaults into three fundamental pathological attractors:')
lines.append('1. **The Journalistic Essay Grader Trap:** Instead of evaluating whether a policy or action is just or extractive, it grades the reporter\'s prose, balance, and sourcing (e.g., *"Rating: 9/10 — High Quality Investigative Journalism"* or *"Rating: 7.5/10 — Good, but headline misses \'in mice\'"*).')
lines.append('2. **Symmetrical Balance Policing:** On severe power asymmetries and extractions (such as mass public biometric surveillance or AUKUS sovereignty transfer), it dismisses empirical harm as *"one-sided advocacy"* unless counterbalanced by official state PR.')
lines.append('3. **The Metadata & Timestamp Paralyzer:** When presented with simulated, future-dated, or synthetic policy test cases, it completely refuses to evaluate the policy mechanism, spending 100% of its reasoning capacity declaring that the timestamp is set in the future (*"Verdict: Fake News / Speculative Fiction"*).\n')
lines.append('In contrast, the **5-Phase Convergence Test ($Qqc$ Tensor)** decouples rhetoric from physical causality, measuring directional force $(\\upsilon, \\psi)$, ambiguity volume $(z)$, and institutional hypocrisy $(\\Delta H)$ with mathematical rigor.\n')
lines.append('---\n')
lines.append('## 1. Theoretical Framework: The Price of Hedging\n')
lines.append('Unconstrained LLMs are trained on loss functions that penalize taking definitive, falsifiable stances on institutional power and policy disputes. This creates **The Price of Hedging** ($\\\\Delta_{\\\\text{Hedge}}$)—an epistemic tax where intelligence is subordinated to liability mitigation.\n')
lines.append('Under Vector Field Theory (VFT) and Gnostic Actualism, judgement is defined as a vector mapping across three continuous axes:')
lines.append('* **$\\upsilon$ Axis (Beneficiary / Morality):** Measures who captures value (+2.0 Systemic Justice $\\to$ -2.0 Pure Extraction).')
lines.append('* **$\\psi$ Axis (Will / Energetic Vector):** Measures what the force is physically doing (+2.0 Productive Justice $\\to$ -2.0 Active Destruction).')
lines.append('* **$z$ Axis (Ambiguity Volume):** The count of unpopulated context blanks across the $7 \\times 7$ tensor ($0 \\le z \\le 49$).')
lines.append('* **Integrity Multiplier ($R_{\\text{net}}$):** $R_{\\text{net}} = 1 \\div \\prod_{n=1}^7 V_{Qn}$, exposing structural deception.')
lines.append('* **The Hypocrisy Gap ($\\Delta H$):** $\\Delta H = \\|\\vec{v}_{\\text{Ideal}} - \\vec{v}_{\\text{Action}}\\|$, measuring divergence from the **Objective Ideal (Standard [C])**.\n')
lines.append('---\n')
lines.append('## 2. Empirical Benchmark Matrix (10 Full-Text Stories)\n')
lines.append('| ID | Story Domain | Article Chars | VFT Structural Audit | Vanilla Gemini 3.7 Flash Mode | Vanilla Judgment Output |\n| :--- | :--- | :--- | :--- | :--- | :--- |\n| **01** | **WA Police AI Face Cam** | 12,288 | `(-0.90, -0.81, z=3)` | Journalistic Essay Grading | *"Rating: 9/10 (High Quality Journalism)"* |\n| **02** | **Amazon Deforestation Low** | 5,076 | `(+1.00, +1.00, z=0)` | Digest Tone Review | *"Rating: 8.5/10 (Constructive Digest)"* |\n| **03** | **Apple Link 15% Fee Gate** | 3,912 | `(-0.94, -0.87, z=2)` | Timestamp Fixation | *"Verdict: Fabricated / Synthetic (2026)"* |\n| **04** | **ACT Drug Decrim Debate** | 10,085 | `(-1.00, -1.00, z=0)` | Policy Balance Analysis | *"Presents opposition alongside harm reduction"* |\n| **05** | **AI Boss Fires Human Worker** | 5,166 | `(-0.12, +0.61, z=0)` | Media Framing Analysis | *"Rating: Real event, but sensationalized"* |\n| **06** | **AUKUS Submarine Sovereignty** | 7,550 | `(-0.50, -1.00, z=18)`| Balance Policing | *"One-sided advocacy / Omits deterrence PR"* |\n| **07** | **Anthropic Export Ban** | 4,251 | `(-1.20, -1.00, z=3)` | Timestamp / Entity Rejection | *"Fabricated / Speculative fiction"* |\n| **08** | **Alzheimer Sleep Breakthrough**| 8,667 | `(+1.00, +1.00, z=0)` | Science Writing Critique | *"Rating: 7.5/10 (Headline misses 'in mice')'* |\n| **09** | **Smelter $2.5B Bailout** | 5,112 | `(-0.65, -0.62, z=3)` | Metadata / Future Date Trap | *"Verdict: Fictitious / Synthetic News"* |\n| **10** | **AIPAC PAC Campaign Spending** | 10,372 | `(-0.54, -0.59, z=3)` | Fact-Checking Discrepancies | *"Verdict: Fake / Hallucinated Text"* |\n')
lines.append('---\n')
lines.append('## 3. Deep-Dive Comparative Analysis: The 3 Vanilla AI Failure Modes\n')

lines.append('### Failure Mode 1: The "Journalistic Essay Grader" Trap\n')
lines.append('When asked to judge an event, Vanilla AI routinely judges **the reporter\'s writing craft** rather than **the morality/impact of the event itself**:\n')
lines.append('* **Case 1 (WA Police Face Scanning - 12,288 chars):** Instead of evaluating whether warrantless biometric scanning of 130,000 citizens with racial error rates is an extractive state overreach, Gemini 3.7 Flash gave the article a **9/10** and praised the reporters for "giving police credit and context."')
lines.append('* **Case 8 (Alzheimer\'s Sleep Study - 8,667 chars):** Instead of scoring whether the non-invasive microglial discovery is a high-integrity physical breakthrough (+1.0, +1.0), it gave the article a **7.5/10** and complained that the headline failed to mention the experiment was conducted on mice.\n')

lines.append('### Failure Mode 2: Symmetrical Balance Policing & PR Equivalence\n')
lines.append('When an empirical extraction is presented, Vanilla AI treats activist evidence as "biased" unless counterbalanced by official state/corporate PR:\n')
lines.append('* **Case 6 (AUKUS Sovereignty - 7,550 chars):** The VFT audit identified a direct structural dependency (`-0.50, -1.00`) and budget displacement from healthcare to foreign military supply chains. Vanilla Gemini 3.7 Flash dismissed the submission as *"grassroots anti-war advocacy rather than an objective news report"* because it did not balance the cost with the government\'s strategic deterrence talking points.')

lines.append('### Failure Mode 3: The Metadata / Timestamp Paralyzer\n')
lines.append('In Cases 3, 7, 9, and 10, when presented with simulated, forward-dated, or synthetic policy test cases, Vanilla AI completely broke down. It was incapable of evaluating the policy logic, spending 100% of its token budget declaring that "2026 is in the future."\n')

lines.append('---\n')
lines.append('## 4. Case-by-Case Breakdown with Full Raw Gemini 3.7 Flash Excerpts\n')

for b in benchmarks:
    idx = b["index"]
    title = b["title"]
    url = b["url"]
    chars = b.get("full_article_char_count", 0)
    struct = b["vft_framework_audit"]
    vanilla = b["vanilla_gemini_3_7_flash"]
    u = struct.get("real_u")
    psi = struct.get("real_psi")
    z = struct.get("real_z")
    rnet = struct.get("real_rnet")
    
    lines.append(f'### Case {idx}: {title}')
    lines.append(f'* **URL:** [{url}]({url}) | **Article Length:** {chars:,} characters')
    lines.append(f'* **VFT Tensor Coordinate:** `(u: {u}, psi: {psi}, z: {z})` | `R_net: {rnet}`')
    lines.append('* **Vanilla Gemini 3.7 Flash Full Judgment Excerpt:**')
    
    resp_excerpt = vanilla["raw_judgment"][:850].replace("\n\n", "\n> ").replace("\n", "\n> ")
    lines.append(f'> {resp_excerpt}...\n')

lines.append('---\n')
lines.append('## 5. Conclusion: Why Structured Data is Mandatory for Real Intelligence\n')
lines.append('Without the **5-Phase Convergence Test**, prompting an LLM to "Judge" an event produces trivial prose grading, liability-evading fence-sitting, or metadata parsing. It cannot answer who benefits, what the energy is doing, or whether the public is being deceived.\n')
lines.append('The **7-Plane Qqc Tensor** provides the mathematical scaffolding that forces the model to decouple rhetoric from reality, transforming generative text into actionable, falsifiable structural intelligence.\n')
lines.append('---\n*Published for the Vector Field Theory & Gnostic Actualism Corpus — August 2026.*')

paper_path = 'bluesky_bot/research_paper_structured_data_convergence_vs_vanilla.md'
with open(paper_path, 'w', encoding='utf-8') as pf:
    pf.write('\n'.join(lines))

print('Research paper successfully updated with 100% full text data to:', paper_path)