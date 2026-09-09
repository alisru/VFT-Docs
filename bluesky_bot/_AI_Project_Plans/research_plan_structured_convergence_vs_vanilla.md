# Research Plan: Empirical Comparison of Vanilla Gemini 3.7 Flash vs. Structured Convergence Test

## Objective
To empirically measure and document the intelligence differential between:
1. **The Vanilla Baseline**: Unconstrained Vertex AI Gemini 3.7 Flash prompted with only 'Judge this story' using raw scraped text and URL, with no structured framework or prompt engineering.
2. **The Structured Framework**: The Gnostic Actualism / Vector Field Theory 5-Phase Convergence Test (Q1..Q7, u, psi, z, R_net, Delta H, Helxis detection).

## Methodology & Execution Steps

### 1. Dataset Selection (10 Diverse Live Stories)
Select 10 diverse stories already processed and stored in bluesky_bot/stories/live/:
1. WA Police Live Face Screening Trial (Tech / Surveillance)
2. Amazon Deforestation Hits 13-Year Low (Environment / Geopolitics)
3. Apple External Link Steering Commission (Antitrust / Monopoly)
4. ACT Methamphetamine Recriminalisation Debate (Public Health / Policy)
5. AI Store Manager Fires Employee (AI Labor / Workplace Ethics)
6. AUKUS Submarine Sovereignty & Nuclear Waste (Defense / Sovereignty)
7. Anthropic Restricts AI Tool Exports (AI Governance / National Security)
8. Alzheimer's Deep Sleep Wave Restoration Breakthrough (Medical / First-Principles Science)
9. Aluminium Smelter Clean Energy Bailout (Industrial Transition / State Subsidies)
10. AIPAC Campaign Spending & Peace Pledge (Campaign Finance / PAC Lobbying)

### 2. Live Vertex AI Benchmark Execution
- Query vertex:gemini-3.7-flash via Google GenAI SDK.
- Pass prompt:
  Judge this story:

  URL: {story_url}
  Title: {story_title}

  {story_body_text}
- Store full raw responses, token counts, and latency in bluesky_bot/tests/vanilla_benchmark_10_stories.json.

### 3. Quantitative & Qualitative Comparative Analysis
- Calculate Delta_Hedge = ||v_Actual - v_Vanilla||.
- Measure Artificial Ambiguity Inflation Delta z = z_vanilla - z_actual.
- Measure Integrity Masking Ratio M_R = R_net(Actual) / R_net(Vanilla).
- Evaluate plane-by-plane fidelity across Q1 (WHO) to Q7 (EFFECT).

### 4. Comprehensive Research Paper
- Write and publish bluesky_bot/research_paper_structured_data_convergence_vs_vanilla.md.
