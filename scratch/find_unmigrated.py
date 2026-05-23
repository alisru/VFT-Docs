import csv

csv_path = r"E:\Vector Field Theory\VFT Docs\_AI files and chat logs\vft_io_database.csv"

with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for r in rows:
    path = r.get('Path', '')
    if not path.startswith('io\\'):
        continue
    filename = r.get('Filename', '')
    plane = r.get('PlaneCategory', '')
    node = r.get('NodeCategory', '')
    tags = r.get('DetailedTags', '')
    
    # Check if Theology
    is_theo = any(x in (filename + plane + node + tags).lower() for x in ['theology', 'spirituality', 'god', 'jesus', 'bible', 'biblical', 'faith', 'religion', 'christ', 'church', 'satan', 'communion', 'ekklesia', 'jonah'])
    # Check if Philosophy
    is_phil = any(x in (filename + plane + node + tags).lower() for x in ['philosophy', 'philosophical', 'logic', 'meaning', 'axiom', 'concept', 'truth', 'epistemology', 'deception', 'consciousness', 'belie', 'thought', 'dissonance', 'lorentz'])
    
    if is_theo:
        print(f"THEO: {filename} | Path: {path} | Plane: {plane} | Node: {node} | Tags: {tags}")
    elif is_phil:
        print(f"PHIL: {filename} | Path: {path} | Plane: {plane} | Node: {node} | Tags: {tags}")
