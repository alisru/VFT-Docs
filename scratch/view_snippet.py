import os
import sys

# Reconfigure stdout to use UTF-8
if sys.version_info >= (3, 7):
    sys.stdout.reconfigure(encoding='utf-8')

io_dir = r"E:\Vector Field Theory\VFT Docs\_VFT MD\io"
files = [
    "BRAINSTORM_FUTURE_MODULES.md",
    "The Law of Empty Mass.md",
    "Critique of Faith-Based Economics Structural Economic Models & The Parallel Polis.md",
    "Historical Analysis of Systemic Critiques.md",
    "Tagging Matrix.md",
    "virtue_compounds_model.md"
]

for f in files:
    filepath = os.path.join(io_dir, f)
    if os.path.exists(filepath):
        print(f"=== {f} ===")
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            print(file.read(800))
        print("="*40 + "\n")
