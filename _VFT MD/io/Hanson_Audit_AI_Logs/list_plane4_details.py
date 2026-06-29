import json
from pathlib import Path

audit_path = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json")
with open(audit_path, 'r', encoding='utf-8') as f:
    audit_data = json.load(f)

plane_4 = next(p for p in audit_data['planes'] if p['plane_num'] == 4)

out_lines = []
for idx, v in enumerate(plane_4['vectors']):
    out_lines.append(f"#{idx+1} {v['address']} - {v['name']} ({v['verdict']})")
    out_lines.append(f"  Quote: {v['quote']}")
    out_lines.append(f"  Description: {v['description']}")
    out_lines.append(f"  Justification: {v['justification']}")
    out_lines.append("---")

out_path = Path("e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hanson_Audit_AI_Logs/plane_4_temp_details.txt")
with open(out_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(out_lines))

print("Dumped Plane 4 details to plane_4_temp_details.txt")
