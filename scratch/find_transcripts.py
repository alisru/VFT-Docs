import os

def find_files():
    root_dir = "e:/Vector Field Theory/VFT Docs"
    print(f"Searching in {root_dir}...")
    for root, dirs, files in os.walk(root_dir):
        # Exclude .git and .venv
        dirs[:] = [d for d in dirs if d not in ('.git', '.venv', '.vscode')]
        for file in files:
            if "transcript" in file.lower() or "subagent" in file.lower():
                print(os.path.join(root, file))

find_files()
