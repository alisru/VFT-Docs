import json
import re
from pathlib import Path

# Paths
BASE_DIR = Path(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon")
COMPACT_DIR = BASE_DIR / "compact JSON"
MASTER_JSON = BASE_DIR / "Australia_Kanon.json"

# Recalibrations table: keyed by (plane_num, address, concept_name) or (address, concept_name)
# Format: (new_v, new_psi, new_zone, new_rationale)
RECALIBRATIONS = {
    # PLANE 1: IDENTITY
    ("Who.Who.Who", "Mateship"): (
        0.8, 0.5, "Greater Good",
        "Universal horizontal solidarity extended to any stranger (+υ) that actively binds (+ψ); defensively ejects exploiters/scabs. The Way (increasing potential)."
    ),
    ("Who.Who.What", "The Larrikin"): (
        0.6, 0.6, "Greater Good",
        "Deflates hubris (+υ) through active mockery (+ψ). Anti-authoritarian circuit breaker preventing vertical hierarchy. The Way."
    ),
    ("Who.Who.Where", "The Battler"): (
        0.4, -0.3, "Lesser Good",
        "Quiet endurance benefiting collective (+υ) through stoic suffering (-ψ). Bounded to Other Being; passive will limits breakthrough."
    ),
    ("Who.Who.Why", "The Anzac"): (
        -0.4, 1.0, "Greatest Lie",
        "Sacrifice for sovereign nation-state (+ψ) bounded to in-group tribal identity (-υ) against an external other. Path to Nowhere (TR)."
    ),
    ("Who.Who.How", "Stringybark and Greenhide"): (
        0.7, 0.7, "Greater Good",
        "Universal problem-solving (+υ) through active improvisation (+ψ). Generative engineering expanding local capacity. The Way."
    ),
    ("Who.Who.Cause", "The Indigenous Custodian"): (
        1.6, 1.2, "Systemic Justice",
        "65,000 years of unbroken ecological and spiritual stewardship (+υ) demanding truth and justice (+ψ). Scale of Truth and Progress toward Bliss Zone."
    ),
    ("Who.Who.Effect", "The Forgotten People"): (
        -0.3, -0.4, "Greater Evil",
        "Suburban middle-class buffer (-υ) stabilizing status quo through passive home-centered retreat (-ψ). Only My Group; Protection Trap."
    ),
    ("Who.What.Who", "The Fair Go"): (
        1.2, 0.8, "Greater Good",
        "Universal baseline axiom (+υ) actively enforced (+ψ). The Rule of 1: no human locked out of dignity. Compounds systemic potential."
    ),
    ("Who.What.What", "Tall Poppy Syndrome"): (
        -0.4, -0.6, "Greater Evil",
        "Envious leveling (-υ) through suppressive cutting (-ψ) to enforce in-group mediocrity. Path to Nowhere (BR)."
    ),
    ("Who.What.Where", "Egalitarianism"): (
        0.9, 0.5, "Greater Good",
        "Universal leveling (+υ) through active rejection of class and inherited deference (+ψ). The Way."
    ),
    ("Who.What.Why", "\"She'll be right\""): (
        -0.3, -0.7, "Greater Evil",
        "Complacent avoidance of duty (-υ) through fatalistic passivity (-ψ). Allows structural rot to compound. Path to Nowhere (BR)."
    ),
    ("Who.Where.Cause", "Terra Nullius"): (
        -1.6, 1.2, "Greatest Lie",
        "The foundational legal fiction (+ψ active erasure) serving colonial land enclosure (-υ). Scale of Lies and Regression (TR)."
    ),
    ("Who.Where.Effect", "The Suburb"): (
        -0.3, -0.4, "Greater Evil",
        "Atomized quarter-acre retreat (-υ) through passive domestic isolation (-ψ). Only My Group; Protection Trap."
    ),
    ("Who.Why.Where", "Populate or Perish"): (
        -0.4, 0.8, "Greatest Lie",
        "Fear-driven demographic expansion (+ψ) predicated on erasure of original population (-υ). Bounded to colonial survival."
    ),
    ("Who.Why.Where", "Anteriority [First Nations Perspective]"): (
        1.6, 0.6, "Systemic Justice",
        "Deep-time truth of 65,000 years (+υ) actively asserted against colonial fiction (+ψ). Scale of Truth and Progress."
    ),
    ("Who.Why.Why", "\"Have a Go, Ya Mug\""): (
        1.2, 1.4, "Greater Good",
        "Universal democratic participation (+υ) through defiant rebellion (+ψ). Eureka spirit: break-out from arbitrary oppression."
    ),
    ("Who.Why.How", "The Cultural Cringe"): (
        -0.5, -0.5, "Greater Evil",
        "Self-harm (-υ) through internalized passive inferiority (-ψ). Path to Nowhere (BR)."
    ),
    ("Who.How.Who", "The Pub Test"): (
        -0.2, -0.5, "Lesser Evil",
        "Anti-intellectual populist filter (-υ) through passive rejection of complexity (-ψ). Bounded to in-group comfort."
    ),
    ("Who.How.What", "Compulsory Voting"): (
        1.4, 1.0, "Greater Good",
        "Universal participation (+υ) through enforced collective civic duty (+ψ). Structural protection of democratic health."
    ),
    ("Who.Cause.How", "White Australia Policy"): (
        -1.5, 1.0, "Greatest Lie",
        "Racial exclusion (-υ) actively legislated (+ψ). Statutory walling off the continent for in-group monopoly."
    ),
    ("Who.Cause.How", "Survival [First Nations Perspective]"): (
        1.4, 1.0, "Greater Good",
        "Unbroken persistence against systemic elimination (+υ) through active resistance (+ψ). The Way."
    ),
    ("Who.Effect.How", "Medicare"): (
        1.4, 1.0, "Greater Good",
        "Universal healthcare (+υ) through state-guaranteed single-payer architecture (+ψ). Compound systemic justice toward Bliss Zone."
    ),

    # PLANE 2: DEFINITION
    ("What.Who.Who", "The Independent Australian Briton"): (
        -0.4, 0.2, "Lesser Evil",
        "Hybrid colonial identity (-υ) maintaining deference to foreign crown hierarchy (+ψ). Bounded to Only My Group."
    ),
    ("What.What.Who", "The Governor-General"): (
        0.2, -0.4, "Lesser Good",
        "Unelected constitutional safety-valve (+υ) exercising passive reserve authority (-ψ). Structural constraint."
    ),
    ("What.Effect.What", "The Lucky Country"): (
        -0.4, -0.6, "Greater Evil",
        "Unearned mineral luck (-υ) breeding second-rate leadership and complacent de-industrialization (-ψ). Path to Nowhere (BR)."
    ),
    ("What.Effect.Cause", "The Great Silence"): (
        -1.4, -0.8, "Greater Evil",
        "Active structural erasure (-υ) through deliberate institutional forgetting of frontier history (-ψ)."
    ),
    ("What.Effect.Effect", "The Nanny State"): (
        -0.4, -0.6, "Greater Evil",
        "Risk-averse paternalism (-υ) suppressing individual and civic initiative (-ψ) under guise of safety."
    ),

    # PLANE 3: LAND
    ("Where.What.Who", "The Squatter"): (
        -1.4, 1.0, "Greatest Lie",
        "Violent enclosure of indigenous land (+ψ) for private dynastic rentier accumulation (-υ). Greed Zone."
    ),
    ("Where.What.What", "The Void"): (
        -1.6, 1.2, "Greatest Lie",
        "Active legal and spatial erasure (+ψ) serving colonizers exclusively (-υ)."
    ),
    ("Where.Where.Who", "The Red Heart"): (
        0.0, -0.5, "Constraint",
        "Geological fact, not moral agency. Sublime arid reality imposing physical boundary."
    ),
    ("Where.Why.Why", "The Flood"): (
        0.0, 0.6, "Constraint",
        "Natural violent ecological reset (+ψ); environmental force, not moral choice."
    ),
    ("Where.Effect.What", "The Sprawl"): (
        -0.5, -0.3, "Greater Evil",
        "Low-density private land consumption (-υ) through atomized dispersion (-ψ). Depletes public resources."
    ),

    # PLANE 4: DRIVE
    ("Why.Who.What", "The Bludger"): (
        -0.8, -0.6, "Greater Evil",
        "Parasitic extraction (-υ) through deliberate refusal to contribute (-ψ)."
    ),
    ("Why.Why.What", "Tall Poppy Syndrome"): (
        -0.4, -0.6, "Greater Evil",
        "Envious leveling (-υ) through suppressive cutting (-ψ) serving group mediocrity."
    ),
    ("Why.Why.Why", "She'll Be Right"): (
        -0.3, -0.7, "Greater Evil",
        "Fatalistic complacency (-υ) acting as a passive brake on systemic reform (-ψ)."
    ),
    ("Why.Why.Where", "Cultural Cringe"): (
        -0.5, -0.5, "Greater Evil",
        "Internalized colonial inferiority (-υ) producing creative deference (-ψ)."
    ),

    # PLANE 5: METHOD
    ("How.How.How", "The Shortcut"): (
        -0.5, 0.2, "Greatest Lie",
        "Pragmatic 'she'll do' fix (+ψ) sacrificing systemic excellence and safety (-υ)."
    ),

    # PLANE 6: FOUNDATION
    ("Cause.Who.What", "The Colonizer"): (
        -1.5, 1.0, "Greatest Lie",
        "Terra Nullius erasure (-υ) through active dispossession and frontier violence (+ψ)."
    ),
    ("Cause.Who.Why", "The Squatter"): (
        -1.4, 1.0, "Greatest Lie",
        "Usurpation of common land (-υ) through active private land-grabbing (+ψ)."
    ),
    ("Cause.What.Cause", "The White Australia Policy"): (
        -1.5, 1.0, "Greatest Lie",
        "Statutory racial engineering (-υ) through active exclusion (+ψ)."
    ),
    ("Cause.Cause.What", "Gondwana"): (
        0.0, 0.0, "Constraint",
        "Geological reality: 45 million years of biological isolation. Physical constant."
    ),

    # PLANE 7: RESULT
    ("Effect.Who.Who", "The Quiet Australian"): (
        -0.4, -0.5, "Greater Evil",
        "Suburban voter (-υ) withdrawing into private tax shields (-ψ) at expense of public equity. Protection Trap."
    ),
    ("Effect.What.Who", "The Home Owner"): (
        -0.6, 0.7, "Greatest Lie",
        "Leveraged asset hoarding (+ψ) disguised as a universal dream (-υ). Intergenerational wealth extraction."
    ),
    ("Effect.Where.What", "The Commodity"): (
        -0.8, 1.1, "Greatest Lie",
        "Hyper-active non-renewable extraction (+ψ) exporting wealth exclusively to multinational interests (-υ)."
    ),
    ("Effect.Effect.How", "She'll Be Right"): (
        -0.3, -0.7, "Greater Evil",
        "National complacency (-υ) allowing infrastructure and social compacts to decay (-ψ)."
    ),
    ("Effect.Effect.Cause", "The Apology"): (
        1.2, 0.8, "Greater Good",
        "Truth-telling and state-level moral restitution (+υ) through formal acknowledgment (+ψ)."
    )
}

def update_compact_files():
    print("--- Updating Compact JSON Files ---")
    for fpath in COMPACT_DIR.glob("Plane_*_compact.json"):
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        modified = False
        for entry in data:
            addr = entry.get("address")
            name = entry.get("name")
            key = (addr, name)
            if key in RECALIBRATIONS:
                v, psi, zone, rationale = RECALIBRATIONS[key]
                entry["coordinates"] = {"v": v, "psi": psi}
                entry["zone"] = zone
                entry["judgment_rationale"] = rationale
                modified = True
                print(f"Updated Compact: {addr} {name} -> ({v}, {psi}) [{zone}]")
        
        if modified:
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Saved: {fpath.name}")

def update_master_json():
    print("\n--- Updating Master Australia_Kanon.json ---")
    with open(MASTER_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    modified_count = 0
    for plane in data.get("planes", []):
        for sense in plane.get("senses", []):
            for item in sense.get("items", []):
                addr = item.get("id", "").strip("()")
                for concept in item.get("concepts", []):
                    name = concept.get("name")
                    key = (addr, name)
                    if key in RECALIBRATIONS:
                        v, psi, zone, rationale = RECALIBRATIONS[key]
                        concept["judgement"] = {
                            "moral_vector": v,
                            "will_vector": psi,
                            "archetype_name": zone,
                            "notes": rationale
                        }
                        modified_count += 1
                        print(f"Updated Master: {addr} {name} -> ({v}, {psi}) [{zone}]")
    
    with open(MASTER_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved Master JSON with {modified_count} updates.")

def update_judgment_markdown():
    print("\n--- Updating Judgment Markdown Files ---")
    for fpath in BASE_DIR.glob("*_JUDGMENT.md"):
        with open(fpath, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            updated_line = line
            # Match table row: | Address | **Name** | v | psi | Judgment |
            m = re.match(r'^\|\s*([\w\.\(\)]+)\s*\|\s*\*\*([^\*]+)\*\*\s*\|\s*([^\s\|]+)\s*\|\s*([^\s\|]+)\s*\|\s*(.*)$', line)
            if m:
                raw_addr, raw_name, old_v, old_psi, rest = m.groups()
                addr = raw_addr.replace("(", "").replace(")", "").strip()
                name = raw_name.strip()
                key = (addr, name)
                if key in RECALIBRATIONS:
                    v, psi, zone, rationale = RECALIBRATIONS[key]
                    v_str = f"+{v}" if v > 0 else (f"{v}" if v < 0 else "0.0")
                    psi_str = f"+{psi}" if psi > 0 else f"{psi}"
                    updated_line = f"| {raw_addr} | **{name}** | {v_str} | {psi_str} | **{zone}** — {rationale} |\n"
                    print(f"Updated MD: {addr} {name} -> {v_str}, {psi_str}")
            new_lines.append(updated_line)
        
        with open(fpath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"Saved: {fpath.name}")

def update_australian_kanon_combined_md():
    kanon_md = BASE_DIR / "AustralianKanon.md"
    if not kanon_md.exists():
        return
    print("\n--- Updating AustralianKanon.md ---")
    with open(kanon_md, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Pattern for table entries:
    #   Who.Who.Who        **Mateship**     +0.7   +0.4   **Greater Good** --- ...
    for (addr, name), (v, psi, zone, rationale) in RECALIBRATIONS.items():
        v_str = f"+{v}" if v > 0 else (f"{v}" if v < 0 else "0.0")
        psi_str = f"+{psi}" if psi > 0 else f"{psi}"
        # Match lines like: \s+Who.Who.Who\s+\*\*Mateship\*\*\s+[+-]?\d+\.?\d*\s+[+-]?\d+\.?\d*
        # We replace the coords and the first sentence of judgment
        pattern = re.compile(
            r'(\s+' + re.escape(addr) + r'\s+\*\*' + re.escape(name) + r'\*\*\s+)([^\s]+)(\s+)([^\s]+)(\s+\*\*)([^\*]+)(\*\* --- )',
            re.MULTILINE
        )
        def repl(m):
            return f"{m.group(1)}{v_str}{m.group(3)}{psi_str}{m.group(5)}{zone}{m.group(7)}"
        content = pattern.sub(repl, content)
    
    with open(kanon_md, "w", encoding="utf-8") as f:
        f.write(content)
    print("Saved: AustralianKanon.md")

if __name__ == "__main__":
    update_compact_files()
    update_master_json()
    update_judgment_markdown()
    update_australian_kanon_combined_md()
    print("\n--- All Kanon Recalibration Updates Complete! ---")
