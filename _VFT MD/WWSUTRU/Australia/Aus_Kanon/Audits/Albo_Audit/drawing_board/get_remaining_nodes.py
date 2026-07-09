import json
import sys

json_path = r"e:\Vector Field Theory\VFT Docs\.agents\skills\kanon-audit\references\Plane_2_Definition_compact.json"

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

target_addresses = [
    "What.How.Cause", "What.How.Effect",
    "What.Cause.Who", "What.Cause.What", "What.Cause.Where", "What.Cause.Why", "What.Cause.How", "What.Cause.Cause", "What.Cause.Effect",
    "What.Effect.Who", "What.Effect.What", "What.Effect.Where", "What.Effect.Why", "What.Effect.How", "What.Effect.Cause", "What.Effect.Effect"
]

remaining = [x for x in data if x['address'] in target_addresses]

out_lines = []
for x in remaining:
    out_lines.append(f"Address: {x['address']}")
    out_lines.append(f"Name: {x['name']}")
    out_lines.append(f"Canonical Quote: {x['canonical_quote']}")
    out_lines.append(f"Attribution: {x.get('attribution', '')}")
    out_lines.append(f"Source: {x.get('source', '')}")
    out_lines.append(f"Description: {x.get('description', '')}")
    out_lines.append(f"Establishes: {x.get('establishes', '')}")
    out_lines.append(f"Coordinates: {x.get('coordinates', {})}")
    out_lines.append(f"Zone: {x.get('zone', '')}")
    out_lines.append(f"Judgment Rationale: {x.get('judgment_rationale', '')}")
    out_lines.append("-" * 50)

with open("drawing_board/nodes_output.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(out_lines))

print("Done writing to drawing_board/nodes_output.txt")
