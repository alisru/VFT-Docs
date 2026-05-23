import os

def main():
    root_dir = r"e:\Vector Field Theory\VFT Docs"
    print("Searching for any files with 'batch' in their name...")
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            if "batch" in f.lower():
                print(f"Found: {os.path.join(root, f)}")

if __name__ == "__main__":
    main()
