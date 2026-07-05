import json

h = json.load(open('e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json', encoding='utf-8'))
p6 = [p for p in h['planes'] if p['plane_num'] == 6][0]

with open('e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hanson_Audit_AI_Logs/plane_6_temp_dump.json', 'w', encoding='utf-8') as f:
    json.dump(p6['vectors'], f, indent=2, ensure_ascii=False)

print(f"Dumped {len(p6['vectors'])} vectors.")
