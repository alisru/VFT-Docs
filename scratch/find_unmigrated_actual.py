import os

io_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\io"
files = [f for f in os.listdir(io_dir) if f.endswith('.md')]

theology_keywords = ['theology', 'spirituality', 'god', 'jesus', 'bible', 'biblical', 'faith', 'religion', 'christ', 'church', 'satan', 'communion', 'ekklesia', 'jonah', 'decalogue', 'parable', 'scripture', 'prophet']
philosophy_keywords = ['philosophy', 'philosophical', 'logic', 'meaning', 'axiom', 'concept', 'truth', 'epistemology', 'deception', 'consciousness', 'belie', 'thought', 'dissonance', 'lorentz', 'polytrope', 'nihilism', 'ontology', 'metaphysics']

theology_files = []
philosophy_files = []
others = []

for f in sorted(files):
    filepath = os.path.join(io_dir, f)
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read(4000).lower()
    
    text = (f + " " + content).lower()
    
    is_theo = any(k in text for k in theology_keywords)
    is_phil = any(k in text for k in philosophy_keywords)
    
    # Precise rules for some specific files
    if 'theology' in text or 'theological' in text or 'ekklesia' in text or 'christological' in text or 'mariage' in text or 'marriage' in text:
        is_theo = True
    
    if is_theo:
        theology_files.append(f)
    elif is_phil:
        philosophy_files.append(f)
    else:
        others.append(f)

print(f"Total MD files in io: {len(files)}")
print(f"Theology ({len(theology_files)}):")
for f in theology_files:
    print(f"  - {f}")

print(f"\nPhilosophy ({len(philosophy_files)}):")
for f in philosophy_files:
    print(f"  - {f}")

print(f"\nOthers ({len(others)}):")
for f in others:
    print(f"  - {f}")
