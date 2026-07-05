import json

with open('e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hegemonic Audit_ Pauline Hanson.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

p5_vectors = data['planes'][4]['vectors']
with open('e:/Vector Field Theory/VFT Docs/_VFT MD/io/Hanson_Audit_AI_Logs/plane_5_details.txt', 'w', encoding='utf-8') as out:
    for idx, v in enumerate(p5_vectors):
        out.write(f"--- VECTOR {idx+1} ---\n")
        out.write(f"Address: {v.get('address')}\n")
        out.write(f"Name: {v.get('name')}\n")
        out.write(f"Verdict: {v.get('verdict')}\n")
        out.write(f"Quote: {v.get('quote')}\n")
        out.write(f"Description: {v.get('description')}\n")
        out.write(f"Stated Name: {v.get('meta', {}).get('stated_name')}\n")
        out.write("\n")
