def main():
    filepath = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive\enoughrope04.txt"
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    for i in range(25, 38):
        if i < len(lines):
            print(f"Line {i}: '{lines[i].strip()}'")

if __name__ == "__main__":
    main()
