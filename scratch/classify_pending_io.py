import csv

csv_path = r"E:\Vector Field Theory\VFT Docs\_AI files and chat logs\vft_io_database.csv"

with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

io_rows = [row for row in rows if row.get('Path', '').startswith('io\\')]

theology_keywords = ['theology', 'spirituality', 'god', 'jesus', 'bible', 'biblical', 'faith', 'religion', 'christ', 'church', 'satan', 'communion', 'ekklesia', 'jonah']
philosophy_keywords = ['philosophy', 'philosophical', 'logic', 'meaning', 'axiom', 'concept', 'truth', 'epistemology', 'deception', 'consciousness', 'belie', 'thought', 'dissonance', 'lorentz']

theology_files = []
philosophy_files = []
other_files = []

for row in io_rows:
    filename = row['Filename']
    plane = row.get('PlaneCategory', '').lower()
    node = row.get('NodeCategory', '').lower()
    tags = row.get('DetailedTags', '').lower()
    
    text = (filename + " " + plane + " " + node + " " + tags).lower()
    
    is_theo = any(k in text for k in theology_keywords)
    is_phil = any(k in text for k in philosophy_keywords)
    
    if is_theo:
        theology_files.append(row)
    elif is_phil:
        philosophy_files.append(row)
    else:
        # Fallback to checking the summary or context
        summary = row.get('SummaryAE-C', '').lower()
        if any(k in summary for k in theology_keywords):
            theology_files.append(row)
        elif any(k in summary for k in philosophy_keywords):
            philosophy_files.append(row)
        else:
            other_files.append(row)

print(f"Theology files found: {len(theology_files)}")
for r in theology_files:
    print(f"  - {r['Filename']} -> Theology & Spirituality")

print(f"\nPhilosophy files found: {len(philosophy_files)}")
for r in philosophy_files:
    print(f"  - {r['Filename']} -> Philosophy")

print(f"\nOther files: {len(other_files)}")
for r in other_files[:20]:
    print(f"  - {r['Filename']}")
