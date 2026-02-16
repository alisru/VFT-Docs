
import os
import re
from collections import Counter

file_list_path = r"C:\Users\hungh\.gemini\antigravity\brain\e88937b1-8fee-414a-9340-745dcf7f3ed4\current_structure.txt"

def analyze_structure():
    if not os.path.exists(file_list_path):
        print(f"File list not found at {file_list_path}")
        return

    with open(file_list_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[3:] # Skip header

    files = []
    for line in lines:
        path = line.strip()
        # Some paths might have extra whitespace or be formatted as "Path: ..."
        if "FullName" in path or "-----" in path:
            continue
        if path and os.path.isfile(path):
            files.append(path)

    # 1. Detect Duplicates by Filename
    filenames = {}
    duplicates = []
    for f in files:
        name = os.path.basename(f).lower()
        if name in filenames:
            filenames[name].append(f)
            if name not in [d[0] for d in duplicates]:
                duplicates.append((name, filenames[name]))
        else:
            filenames[name] = [f]

    # 2. Extract Keywords for Clustering
    all_words = []
    for f in files:
        name = os.path.basename(f).replace('_', ' ').replace('-', ' ').replace('.', ' ')
        words = re.findall(r'\w+', name.lower())
        # Filter out common/short words
        words = [w for w in words if len(w) > 3 and w not in ['with', 'that', 'this', 'from', 'analysis', 'report', 'plan', 'protocol', 'summary', 'final', 'part', 'version', 'revised', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9', 'v10', 'v11', 'v12', 'v13', 'v14', 'v24', 'v25']]
        all_words.extend(words)

    word_freq = Counter(all_words).most_common(100)

    # 3. Identify Root Files (Clutter)
    vft_root = r"E:\Vector Field Theory\VFT Docs\_VFT MD"
    root_files = [f for f in files if os.path.dirname(f).lower() == vft_root.lower()]

    # 4. Identify Ambiguous Files (Short names or generic names)
    ambiguous = []
    for f in files:
        name = os.path.basename(f)
        if (len(name) < 15 or name.lower() in ['readme.md', 'states.md', 'weave.md', 'check_metadata.py', 'file_list.txt']) and '.agent' not in f and '.vscode' not in f:
            ambiguous.append(f)

    # Output Results
    print("--- DUPLICATE FILENAMES ---")
    for name, locations in duplicates:
        print(f"File: {name}")
        for loc in locations:
            print(f"  - {loc}")

    print("\n--- TOP CONCEPT KEYWORDS ---")
    for word, freq in word_freq:
        print(f"{word}: {freq}")

    print("\n--- ROOT LEVEL CLUTTER ---")
    for f in root_files:
        print(f"  - {f}")

    print("\n--- POTENTIALLY AMBIGUOUS FILES ---")
    for f in ambiguous:
        print(f"  - {f}")

if __name__ == "__main__":
    analyze_structure()
