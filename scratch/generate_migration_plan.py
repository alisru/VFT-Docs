import os

md_io_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\io"
docs_io_dir = r"E:\Vector Field Theory\VFT Docs\io"

md_files = [f for f in os.listdir(md_io_dir) if os.path.isfile(os.path.join(md_io_dir, f))]
docs_files = [f for f in os.listdir(docs_io_dir) if os.path.isfile(os.path.join(docs_io_dir, f))]

theology_words = ['theology', 'spirituality', 'god', 'jesus', 'bible', 'biblical', 'faith', 'religion', 'christ', 'church', 'satan', 'communion', 'ekklesia', 'jonah', 'decalogue', 'parable', 'scripture', 'prophet', 'immortal', 'witness', 'cain', 'babel', 'virtue', 'sin', 'triad', 'marriage', 'ritual', 'mass']
philosophy_words = ['philosophy', 'philosophical', 'logic', 'meaning', 'axiom', 'concept', 'truth', 'epistemology', 'deception', 'consciousness', 'belie', 'thought', 'dissonance', 'lorentz', 'polytrope', 'nihilism', 'ontology', 'metaphysics', 'malice', 'humor', 'chance', 'necessity', 'astrology', 'psochic hegemony', 'psochic_hegemony', 'cognitive', 'semantic', 'tautonic']

theology_moves = []
philosophy_moves = []
ignored_moves = []

def get_category(filename, content=""):
    text = (filename + " " + content).lower()
    
    # Exclude files like process_io_files or scripts
    if filename.endswith('.py') or filename.endswith('.ps1') or filename.endswith('.bat'):
        return None
    
    # Specific exceptions/overrides
    if 'theology' in text or 'ekklesia' in text or 'christological' in text or 'marriage' in text or 'witness' in text or 'burial of the talent' in text or 'jonah' in text or 'hagia_triada' in text or 'decalogue' in text or 'adin' in text or 'adig' in text:
        return 'Theology & Spirituality'
    
    if 'astrology' in text or 'psochic hegemony' in text or 'psochic_hegemony' in text or 'polytrope' in text or 'axiom' in text or 'philosophy' in text or 'meaning' in text or 'lorentz' in text or 'cognitive' in text or 'semantic' in text or 'truth' in text or 'deception' in text:
        return 'Philosophy'
        
    is_theo = any(w in text for w in theology_words)
    is_phil = any(w in text for w in philosophy_words)
    
    if is_theo:
        return 'Theology & Spirituality'
    elif is_phil:
        return 'Philosophy'
    else:
        return None

for f in sorted(md_files):
    # Read snippet
    filepath = os.path.join(md_io_dir, f)
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read(4000)
    except:
        content = ""
        
    cat = get_category(f, content)
    if cat == 'Theology & Spirituality':
        theology_moves.append(f)
    elif cat == 'Philosophy':
        philosophy_moves.append(f)
    else:
        ignored_moves.append(f)

print(f"THEOLOGY MOVES ({len(theology_moves)}):")
for f in theology_moves:
    print(f"  - {f}")

print(f"\nPHILOSOPHY MOVES ({len(philosophy_moves)}):")
for f in philosophy_moves:
    print(f"  - {f}")

print(f"\nIGNORED MOVES ({len(ignored_moves)}):")
for f in ignored_moves:
    print(f"  - {f}")
