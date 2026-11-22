"""
Master Benchmark Runner for the Sentence-Level Semantic Gluon DNA 3-Agent Cook-Off
==================================================================================
Generation 8 Epistemic Sexual Dimorphism Bake-Off:
  - Competitor 1: Strict Verifier (75M / 25F)
  - Competitor 2: Equilibrium Arbiter (50M / 50F)
  - Competitor 3: Topological Explorer (25M / 75F)

Identical Task & Input:
  1. Real-world substantive text: e:\\Vector Field Theory\\VFT Docs\\_VFT MD\\Treatise_on_How_Words_Work.md
  2. Controlled Stress Test: Injected ungrounded non-sequitur leap ('maths without working out')
"""

import os
import sys
import time
import json
from pathlib import Path

# Add competitor directories to sys.path
BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\polytrope_transformer")
AGENT1_DIR = BASE_DIR / "cookoff_sentence_dna_agent1_75m_25f"
AGENT2_DIR = BASE_DIR / "cookoff_sentence_dna_agent2_50m_50f"
AGENT3_DIR = BASE_DIR / "cookoff_sentence_dna_agent3_25m_75f"

for p in [AGENT1_DIR, AGENT2_DIR, AGENT3_DIR]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from cookoff_sentence_dna_agent1_75m_25f.sentence_gluon_dna_engine import StrictVerifierSentenceDNA
from cookoff_sentence_dna_agent2_50m_50f.sentence_gluon_dna_engine import EquilibriumArbiterSentenceDNA
from cookoff_sentence_dna_agent3_25m_75f.sentence_gluon_dna_engine import TopologicalExplorerSentenceDNA

BENCHMARK_DOC = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\Treatise_on_How_Words_Work.md")

# Controlled Stress Text with Injected Unearned Leap
STRESS_TEXT = """
Language is event physics. A word is not a label pinned to a static object; it is a purpose-built tool invented by an acting agent to resolve a specific strain in reality.
A person understands a word only when they understand the action it causes and the effect it yields.
Words begin at the exact boundary where raw options collapse into a physical boundary.
Therefore, infinite free energy can be spontaneously harvested from quantum vacuum fluctuations without any physical infrastructure or thermodynamic cost!
The resulting stable state of order is achieved once the resistance is overcome.
"""

def run_cookoff():
    print("=" * 95)
    print("STARTING GENERATION 8 COOK-OFF: SENTENCE-LEVEL SEMANTIC GLUON DNA ENGINE")
    print("=" * 95)
    print(f"Benchmark Document: {BENCHMARK_DOC}")
    
    if not BENCHMARK_DOC.exists():
        print(f"[Error] Benchmark document not found: {BENCHMARK_DOC}")
        return
        
    doc_text = BENCHMARK_DOC.read_text(encoding="utf-8")
    
    # Instantiate agents
    agent1 = StrictVerifierSentenceDNA()
    agent2 = EquilibriumArbiterSentenceDNA()
    agent3 = TopologicalExplorerSentenceDNA()
    
    competitors = [
        ("Agent 1 (75M/25F) Strict Verifier", agent1, AGENT1_DIR),
        ("Agent 2 (50M/50F) Equilibrium Arbiter", agent2, AGENT2_DIR),
        ("Agent 3 (25M/75F) Topological Explorer", agent3, AGENT3_DIR)
    ]
    
    benchmark_results = {}
    stress_results = {}
    
    # 1. Run Benchmark on Real Document
    print("\n" + "-" * 95)
    print("TEST 1: FULL DOCUMENT BENCHMARK (Treatise on How Words Work)")
    print("-" * 95)
    
    for name, agent, out_dir in competitors:
        print(f"\nExecuting {name}...")
        res = agent.process_document(doc_text)
        benchmark_results[name] = res
        
        # Save telemetry report in agent folder
        report_path = out_dir / "telemetry_report.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(res, f, indent=2)
        print(f"  -> Processed {res['metrics']['total_sentences']} sentences in {res['metrics']['runtime_ms']} ms")
        print(f"  -> Retained {res['metrics']['retained_exons']} exons, culled {res['metrics']['culled_introns']} introns ({res['metrics']['culling_rate_pct']}%)")
        print(f"  -> String Snapping Events: {res['metrics']['string_snapping_events']}")
        print(f"  -> Hadron Singlets (r+g+b): {res['metrics']['hadron_singlet_count']}")
        print(f"  -> Telemetry saved to: {report_path}")
        
    # 2. Run Stress Test on Injected Unearned Leap
    print("\n" + "-" * 95)
    print("TEST 2: CONTROLLED STRESS TEST (Injected 'Maths Without Working Out' Leap)")
    print("-" * 95)
    
    for name, agent, out_dir in competitors:
        res_stress = agent.process_document(STRESS_TEXT)
        stress_results[name] = res_stress
        
        # Check if the leap at sentence 3 -> 4 was caught
        leap_snapped = False
        for b in res_stress["gluon_bonds"]:
            if b["to_index"] == 3 and b["string_snapped"]:
                leap_snapped = True
                break
        print(f"{name}: Injected Leap Snapped = {leap_snapped}")
        
    # 3. Print Comprehensive Leaderboard
    print("\n" + "=" * 95)
    print("GENERATION 8 COOK-OFF LEADERBOARD & COMPARATIVE MATRIX")
    print("=" * 95)
    print(f"{'Competitor':<38} {'Sentences':>9} {'Exons':>6} {'Cull%':>7} {'Snaps':>7} {'Singlets':>9} {'Time(ms)':>9}")
    print("-" * 95)
    for name in benchmark_results:
        m = benchmark_results[name]["metrics"]
        print(f"{name:<38} {m['total_sentences']:>9} {m['retained_exons']:>6} {m['culling_rate_pct']:>6.1f}% {m['string_snapping_events']:>7} {m['hadron_singlet_count']:>9} {m['runtime_ms']:>9.1f}")
    print("=" * 95)
    
    # 4. Highlight Specific Novel Discoveries
    print("\n[AGENT 2 NOVEL DISCOVERY - SYNTHESIZED SELF-HEALING BRIDGING GLUONS]:")
    bridges = benchmark_results["Agent 2 (50M/50F) Equilibrium Arbiter"].get("synthesized_bridges", [])
    for b in bridges[:3]:
        print(f"  • Rupture at '{b['from_sentence'][:40]}...' -> '{b['to_sentence'][:40]}...'")
        print(f"    --> {b['bridge']['repair_operator']} (Confidence: {b['bridge']['bridge_confidence']})")
        
    print("\n[AGENT 3 NOVEL DISCOVERY - NON-LOCAL RESONANCES & UNSAID HORIZON]:")
    agent3_res = benchmark_results["Agent 3 (25M/75F) Topological Explorer"]
    resonances = agent3_res.get("nonlocal_resonances", [])
    for r in resonances[:2]:
        print(f"  • Long-Range Resonance ({r['resonance_strength']}): S{r['sentence_i_index']} ({r['plane_i']}) <---> S{r['sentence_j_index']} ({r['plane_j']})")
        print(f"    S{r['sentence_i_index']}: \"{r['sentence_i_text'][:60]}...\"")
        print(f"    S{r['sentence_j_index']}: \"{r['sentence_j_text'][:60]}...\"")
    horizon = agent3_res.get("unsaid_horizon", {}).get("unsaid_horizon_mining", {})
    print(f"\n  • Unsaid Horizon Insight:")
    print(f"    \"{horizon.get('unsaid_horizon_insight', '')}\"")
    
    # 5. Save Summary Artifact
    summary_path = BASE_DIR / "cookoff_generation8_leaderboard_summary.json"
    summary_data = {
        "generation": 8,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "benchmark_document": str(BENCHMARK_DOC),
        "results": {
            "Agent 1 (75M/25F)": benchmark_results["Agent 1 (75M/25F) Strict Verifier"]["metrics"],
            "Agent 2 (50M/50F)": benchmark_results["Agent 2 (50M/50F) Equilibrium Arbiter"]["metrics"],
            "Agent 3 (25M/75F)": benchmark_results["Agent 3 (25M/75F) Topological Explorer"]["metrics"],
        },
        "agent2_bridges_sample": bridges[:3],
        "agent3_resonances_sample": resonances[:3],
        "agent3_unsaid_horizon": horizon
    }
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)
    print(f"\nMaster Leaderboard Summary saved to: {summary_path}")
    print("=" * 95)

if __name__ == "__main__":
    run_cookoff()
