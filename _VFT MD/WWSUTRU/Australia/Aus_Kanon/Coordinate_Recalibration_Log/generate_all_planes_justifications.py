import json
import re
from pathlib import Path

MASTER_JSON = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Australia_Kanon.json")
OUTPUT_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Coordinate_Recalibration_Log")

def get_scope_anchor(v):
    if v >= 1.5:
        return f"{{Everyone}} (+2.0υ anchor: Universal Systemic Justice, biosphere continuity, truth across all beings)"
    elif v >= 0.7:
        return f"Other Beings (+1.0υ anchor: The Good Truth, collective altruism beyond immediate clan)"
    elif v >= 0.2:
        return f"Other Being (+0.3υ to +0.5υ anchor: Targeted altruism, quiet personal endurance for immediate family/peer)"
    elif v == 0.0:
        return f"No-one (0.0υ anchor: Neutral stasis / physical constant / zero moral agency)"
    elif v >= -0.5:
        return f"Only My Group (-0.3υ to -0.5υ anchor: Tribal boundary, in-group preference, sovereign nation-state, suburban insularity)"
    elif v >= -1.2:
        return f"Only Me (-1.0υ anchor: The Bad Preference, private accumulation, ego-interest at expense of others)"
    else:
        return f"No-One Else (-2.0υ anchor: Total parasitic extraction, active erasure, systemic deception)"

def get_will_anchor(psi):
    if psi >= 1.5:
        return f"Productive Justice (+2.0ψ anchor: Systemic, compounding creation of generative order)"
    elif psi >= 0.4:
        return f"Proactive Will (+1.0ψ anchor: Building, asserting, rebelling, active intervention)"
    elif psi == 0.0:
        return f"Neutral Stasis (0.0ψ anchor: Invariant equilibrium, observation)"
    elif psi >= -0.9:
        return f"Suppressive / Passive Will (-1.0ψ anchor: Withholding action, stoic suffering, cutting down excellence, bureaucratic drag, fatalistic complacency)"
    else:
        return f"Destructive Entropy (-2.0ψ anchor: Active dismantling, violence, chaos, systemic collapse)"

def get_trajectory_analysis(v, psi, name, meaning):
    if v > 0 and psi > 0:
        if v >= 1.0:
            return (
                "**The Scale of Truth and Progress — Path to the Bliss Zone (compounding systemic potential):**\n"
                f"The structural mechanism of {name} operates at a systemic, universal horizon. "
                "Because its benefit extends to all humans or the broader ecological/moral order without requiring an excluded outgroup, "
                "its potential increases over time, aligning directly with The Way toward the (2,2) Bliss Zone."
            )
        else:
            return (
                "**The Way / Scale of Truth and Progress (increasing potential over time):**\n"
                f"The internal logic of {name} dissolves arbitrary status barriers, mocks pretension, or provides proactive horizontal mutual aid. "
                "Because it does not rely on zero-sum exploitation or outgroup suppression, its generative potential "
                "compounds across generations, naturally scaling from the individual to *Other Beings*."
            )
    elif v > 0 and psi <= 0:
        return (
            "**The Lesser Good Boundary / Constructive Stasis (stable but low-energy potential):**\n"
            f"The ideal of {name} provides vital social ballast, stoic endurance, or protective restraint, but its reliance on passive acceptance, "
            "suffering, or administrative drag restricts its volitional velocity. Its potential remains stable within the human horizon "
            "but cannot break through into systemic transformation without an injection of proactive will (+ψ)."
        )
    elif v < 0 and psi > 0:
        return (
            "**The Scale of Lies and Regression / Reductive Quadrant (Path to Nowhere — Greed/Conflict):**\n"
            f"While {name} mobilizes formidable proactive energy (+ψ), its beneficiary horizon is hard-coded to *Only My Group* or *Only Me* (-υ). "
            "In dynamic field physics, high kinetic will attached to an in-group boundary creates an entropic debt paid by excluded outgroups. "
            "Over time, this trajectory generates systemic friction and descends into the Greed Zone, unable to achieve structural peace."
        )
    elif v < 0 and psi <= 0:
        return (
            "**The Scale of Stagnation and Decay / Regressive Quadrant (Path to Nowhere — Rot/Depression):**\n"
            f"By combining an in-group or self-interested focus (-υ) with passive avoidance, fatalistic neglect, or suppressive cutting (-ψ), {name} "
            "acts as an entropic sink. Over time, it erodes collective ambition, enforces mediocrity, and allows structural fragility to compound, "
            "locking the social field into the Bored, Depression, or Destructive Zones."
        )
    else:
        return (
            "**Neutral Invariant Boundary (Physical/Environmental Constraint):**\n"
            f"{name} describes a non-negotiable physical, geological, or climatic reality. It possesses kinetic magnitude or friction "
            "but zero moral agency. Its potential over time serves as the unyielding physical arena upon which human conscious vectors must act."
        )

def generate_all_planes():
    data = json.load(open(MASTER_JSON, encoding="utf-8"))
    
    total_generated = 0
    master_lines = []
    master_lines.append("# Master Ledger: Complete 354-Node Hegemonic Coordinate Justifications")
    master_lines.append("**Canonical Database:** Australian National Kanon (343 Vectors + 11 Shadow Perspectives)")
    master_lines.append("**Evaluation Instrument:** The Psochic Hegemony v2.7 (Dynamic Tensor Potential Field)")
    master_lines.append("**Methodology:** Group Scale Beneficiary Anchors, Volitional Force Triples, and Potential Trajectories Over Time\n")
    master_lines.append("---\n")
    
    for plane_idx, plane in enumerate(data["planes"]):
        p_num = plane["id"]
        p_name = plane["name"]
        p_vec = plane["vector"]
        filename = f"Plane_{p_num}_{p_name}_Full_Node_Justifications.md"
        
        plane_lines = []
        plane_lines.append(f"# Plane {p_num}: {p_name} ({p_vec}) — Complete Hegemonic Node Justifications")
        plane_lines.append(f"**Canonical Database:** Australian National Kanon (343 Vectors)")
        plane_lines.append(f"**Evaluation Instrument:** The Psochic Hegemony v2.7 (Dynamic Tensor Potential Field)")
        plane_lines.append(f"**Scope:** All concepts in Plane {p_num} ({p_name})\n")
        plane_lines.append("---\n")
        
        count = 0
        for s in plane["senses"]:
            s_id = s["id"]
            s_vec = s["vector"]
            s_desc = s["description"]
            plane_lines.append(f"## Sense {s_id}: The {s_vec} of {p_name} ({s_desc})\n")
            
            for item in s["items"]:
                addr = item["id"].strip("()")
                for c in item["concepts"]:
                    count += 1
                    total_generated += 1
                    name = c["name"]
                    quotes = c.get("quotes", [{}])
                    q = quotes[0] if quotes else {}
                    q_text = q.get("text", "No quote recorded.")
                    q_auth = q.get("author", "Traditional")
                    q_src = q.get("source", "")
                    q_yr = q.get("year", "")
                    
                    context = c.get("context_analysis", "")
                    meaning = c.get("meaning_analysis", "")
                    
                    j = c.get("judgement", {})
                    v = j.get("moral_vector", 0.0)
                    psi = j.get("will_vector", 0.0)
                    zone = j.get("archetype_name", "Unassigned")
                    existing_notes = j.get("notes", "")
                    
                    v_str = f"+{v}" if v > 0 else (f"{v}" if v < 0 else "0.0")
                    psi_str = f"+{psi}" if psi > 0 else (f"{psi}" if psi < 0 else "0.0")
                    
                    block = []
                    block.append(f"### Node {count}: `({addr})` **{name}**")
                    block.append(f"> \"{q_text}\"  ")
                    block.append(f"> — **{q_auth}**, *{q_src}* {q_yr}\n")
                    block.append(f"**Hegemonic Coordinates:** $(\\upsilon = {v_str}, \\psi = {psi_str})$ | **Archetype Zone:** **{zone}**\n")
                    
                    # 1. Scope
                    scope_anchor = get_scope_anchor(v)
                    block.append(f"#### 1. Beneficiary Scope Justification (Axis $\\upsilon = {v_str}$)")
                    block.append(f"- **Group Scale Position:** {scope_anchor}")
                    block.append(f"- **Structural Boundary Analysis:**  \n{context}\n")
                    
                    # 2. Will
                    will_anchor = get_will_anchor(psi)
                    block.append(f"#### 2. Volitional Intent Justification (Axis $\\psi = {psi_str}$)")
                    block.append(f"- **Energetic Direction:** {will_anchor}")
                    block.append(f"- **Action Analysis:**  \n{meaning}\n")
                    
                    # 3. Trajectory
                    traj = get_trajectory_analysis(v, psi, name, meaning)
                    block.append(f"#### 3. Potential Over Time & Trajectory")
                    block.append(f"{traj}\n")
                    
                    # 4. Synthesized Verdict
                    block.append(f"#### 4. Canonical Synthesis & Rationale")
                    block.append(f"> **Verdict:** `{existing_notes}`\n")
                    block.append("---\n")
                    
                    plane_lines.extend(block)
                    master_lines.extend(block)
        
        out_path = OUTPUT_DIR / filename
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n".join(plane_lines))
        print(f"Generated {filename} ({count} nodes).")
        
    master_path = OUTPUT_DIR / "COMPLETE_354_NODE_HEGEMONIC_JUSTIFICATIONS.md"
    with open(master_path, "w", encoding="utf-8") as f:
        f.write("\n".join(master_lines))
    print(f"\nGenerated MASTER LEDGER: {master_path.name} with {total_generated} node justifications.")

if __name__ == "__main__":
    generate_all_planes()
