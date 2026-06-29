import json

data = json.load(open('plane_6_temp_dump.json', encoding='utf-8'))
with open('plane_6_details.txt', 'w', encoding='utf-8') as f:
    for i, v in enumerate(data):
        f.write(f"=== {i+1} ===\n")
        f.write(f"Address: {v['address']}\n")
        f.write(f"Name: {v['name']}\n")
        f.write(f"Verdict: {v['verdict']}\n")
        f.write(f"Quote: {v['quote']}\n")
        f.write(f"Description: {v['description']}\n")
        f.write(f"Justification: {v['justification']}\n\n")

print("Done writing plane_6_details.txt")
