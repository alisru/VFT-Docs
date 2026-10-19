import json
import re
from pathlib import Path

MASTER_JSON = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Australia_Kanon.json")
OUTPUT_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Coordinate_Recalibration_Log")

def get_scope_anchor(v):
    if v >= 1.5:
        return "{Everyone} (+2.0υ anchor: Universal Systemic Justice, biosphere continuity, all beings)"
    elif v >= 0.7:
        return "Other Beings (+1.0υ anchor: The Good Truth, collective altruism beyond immediate clan)"
    elif v >= 0.2:
        return "Other Being (+0.3υ to +0.5υ anchor: Targeted altruism, quiet personal endurance for immediate family/peer)"
    elif v == 0.0:
        return "No-one (0.0υ anchor: Confusion Zone / Stasis / Neutral physical/environmental constant)"
    elif v >= -0.5:
        return "Only My Group (-0.3υ to -0.5υ anchor: Tribal boundary, in-group preference, sovereign nation-state, suburban insularity)"
    elif v >= -1.2:
        return "Only Me (-1.0υ anchor: The Bad Preference, private accumulation, ego-interest at expense of others)"
    else:
        return "No-One Else (-2.0υ anchor: Total parasitic extraction, active erasure, systemic deception)"

def get_will_anchor(psi):
    if psi >= 1.5:
        return "Productive Justice (+2.0ψ anchor: Systemic, compounding creation of generative order)"
    elif psi >= 0.5:
        return "Proactive Will (+1.0ψ anchor: Building, asserting, rebelling, active intervention)"
    elif psi == 0.0:
        return "Neutral Stasis (0.0ψ anchor: Invariant equilibrium, observation)"
    elif psi >= -0.9:
        return "Suppressive / Passive Will (-1.0ψ anchor: Withholding action, stoic suffering, cutting down excellence, bureaucratic drag, fatalistic complacency)"
    else:
        return "Destructive Entropy (-2.0ψ anchor: Active dismantling, violence, chaos, systemic collapse)"

def get_trajectory_analysis(v, psi, name, meaning):
    if v >= 0.7 and psi >= 0.4:
        return (
            "**The Way / Scale of Truth and Progress (increasing potential over time):**\n"
            f"The internal logic of {name} dissolves arbitrary status barriers and expands social cohesion. "
            "Because it does not require an excluded outgroup or zero-sum exploitation to function, its generative potential "
            "compounds across generations, naturally scaling from the individual to *Other Beings* and pointing toward the (2,2) Bliss Zone."
        )
    elif v > 0 and psi < 0:
        return (
            "**The Lesser Good Boundary / Constructive Stasis (stable but low-energy potential):**\n"
            f"The ideal of {name} provides vital social ballast or individual resilience, but its reliance on passive acceptance, "
            "stoicism, or institutional drag restricts its volitional velocity. Its potential remains stable within the human horizon "
            "but cannot break through into systemic transformation without an injection of proactive will (+ψ)."
        )
    elif v < 0 and psi > 0:
        return (
            "**The Scale of Lies and Regression / Reductive Quadrant (Path to Nowhere - Greed/Conflict):**\n"
            f"While {name} mobilizes formidable proactive energy (+ψ), its beneficiary horizon is hard-coded to *Only My Group* or *Only Me* (-υ). "
            "In dynamic field physics, high kinetic will attached to an in-group boundary creates an entropic debt paid by excluded outgroups. "
            "Over time, this trajectory generates systemic friction and descends into the Greed Zone, unable to achieve structural peace."
        )
    elif v < 0 and psi < 0:
        return (
            "**The Scale of Stagnation and Decay / Regressive Quadrant (Path to Nowhere - Rot/Depression):**\n"
            f"By combining an in-group or self-interested focus (-υ) with passive avoidance or suppressive cutting (-ψ), {name} "
            "acts as an entropic sink. Over time, it erodes collective ambition, enforces mediocrity, and allows structural fragility to compound, "
            "locking the social field into the Bored, Depression, or Destructive Zones."
        )
    else:
        return (
            "**Neutral Invariant Boundary (Physical/Environmental Constraint):**\n"
            f"{name} describes a non-negotiable physical, geological, or climatic reality. It possesses kinetic magnitude or friction "
            "but zero moral agency. Its potential over time serves as the unyielding physical arena upon which human conscious vectors must act."
        )

def generate_plane_document(plane_idx, filename):
    data = json.load(open(MASTER_JSON, encoding="utf-8"))
    plane = data["planes"][plane_idx]
    p_num = plane["id"]
    p_name = plane["name"]
    p_vec = plane["vector"]
    
    lines = []
    lines.append(f"# Plane {p_num}: {p_name} ({p_vec}) — Complete Hegemonic Node Justifications")
    lines.append(f"**Canonical Database:** Australian National Kanon (343 Vectors)")
    lines.append(f"**Evaluation Instrument:** The Psochic Hegemony v2.7 (Dynamic Tensor Potential Field)")
    lines.append(f"**Scope:** All concepts in Plane {p_num}\n")
    lines.append("---\n")
    
    count = 0
    for s in plane["senses"]:
        s_id = s["id"]
        s_vec = s["vector"]
        s_desc = s["description"]
        lines.append(f"## Sense {s_id}: The {s_vec} of {p_name} ({s_desc})\n")
        
        for item in s["items"]:
            addr = item["id"].strip("()")
            for c in item["concepts"]:
                count += 1
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
                
                lines.append(f"### Node {count}: `({addr})` **{name}**")
                lines.append(f"> \"{q_text}\"  ")
                lines.append(f"> — **{q_auth}**, *{q_src}* {q_yr}\n")
                
                lines.append(f"**Hegemonic Coordinates:** $(\\upsilon = {v_str}, \\psi = {psi_str})$ | **Archetype Zone:** **{zone}**\n")
                
                # 1. Scope
                scope_anchor = get_scope_anchor(v)
                lines.append(f"#### 1. Beneficiary Scope Justification (Axis $\\upsilon = {v_str}$)")
                lines.append(f"- **Group Scale Position:** {scope_anchor}")
                lines.append(f"- **Structural Boundary Analysis:**  \n{context}\n")
                
                # 2. Will
                will_anchor = get_will_anchor(psi)
                lines.append(f"#### 2. Volitional Intent Justification (Axis $\\psi = {psi_str}$)")
                lines.append(f"- **Energetic Direction:** {will_anchor}")
                lines.append(f"- **Action Analysis:**  \n{meaning}\n")
                
                # 3. Trajectory
                traj = get_trajectory_analysis(v, psi, name, meaning)
                lines.append(f"#### 3. Potential Over Time & Trajectory")
                lines.append(f"{traj}\n")
                
                # 4. Synthesized Verdict
                lines.append(f"#### 4. Canonical Synthesis & Rationale")
                lines.append(f"> **Verdict:** `{existing_notes}`\n")
                lines.append("---\n")
                
    out_path = OUTPUT_DIR / filename
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Generated {out_path.name} with {count} node justifications.")

if __name__ == "__main__":
    generate_plane_document(0, "Plane_1_Identity_Full_Node_Justifications.md")
