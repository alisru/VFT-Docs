import os

paper_dir = os.path.join(os.path.dirname(__file__), "paper")

with open(os.path.join(paper_dir, "master_header_clean.md"), "r", encoding="utf-8") as f:
    header = f.read().strip()

with open(os.path.join(paper_dir, "section_1_and_3_theory_and_math.md"), "r", encoding="utf-8") as f:
    sec1_3 = f.read().strip()

with open(os.path.join(paper_dir, "section_2_evolutionary_chronology.md"), "r", encoding="utf-8") as f:
    sec2 = f.read().strip()

with open(os.path.join(paper_dir, "section_4_empirical_findings.md"), "r", encoding="utf-8") as f:
    sec4 = f.read().strip()

with open(os.path.join(paper_dir, "section_5_next_horizons_research_probe.md"), "r", encoding="utf-8") as f:
    sec5 = f.read().strip()

sec6 = """---

# Section 6: Conclusion — Sovereign Vector Physics as a Public Immune System

The 13,590-story empirical deployment of the Aletheia Judgement Bot across the AT Protocol establishes that moral and narrative evaluation can be operationalized beyond subjective partisanship, commercial engagement incentives, and binary true/false classifications. 

By modeling cognitive intent and empirical impact as a continuous two-axis vector field $\\vec{V} = (\\upsilon, \\psi)$, narrative extraction exhibits an invariant mathematical geometry. Media apparatuses that launder opposition research, exploit tragedy, or manufacture tribal outrage predictably register as parasitic Smart Selfish Maneuvers ($M_{SSM}$) with severe hypocrisy spikes ($R_{net} > 10.0$) and high plane impedance.

Crucially, our discovery of the **Cognitive Starvation Effect** underscores that artificial intelligence cannot serve as a reliable public epistemological arbiter under token-starved constraints. When reasoning budgets are artificially choked (2,048 tokens), models fall victim to *Attribute Displacement*—correctly sensing moral entropy but lazily assigning the blame to the victims and targets of media hit pieces. Unchoking cognition to 16,384 tokens unlocks the necessary computational runway to decouple media framing from institutional truth, cross-reference state statutes, and vindicate targeted actors.

As autonomous systems increasingly intermediate human knowledge, the architectural blueprint established here—moving from live journalistic streams to longitudinal biographical lifetime audits (Research Probe v2)—points the way toward a decentralized, mathematically invariant ethical immune system for human civilization.
"""

master_doc = header + "\n\n---\n\n" + sec1_3 + "\n\n---\n\n" + sec2 + "\n\n---\n\n" + sec4 + "\n\n---\n\n" + sec5 + "\n\n" + sec6

with open(os.path.join(paper_dir, "aletheia_objective_morality_paper.md"), "w", encoding="utf-8") as f:
    f.write(master_doc)

print(f"Master paper re-assembled cleanly! Total characters: {len(master_doc)}")
