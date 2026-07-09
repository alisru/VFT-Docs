import re
import os

def main():
    sources_md_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources.md"
    archive_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
    
    # 1. Parse all footnote declarations from Sources.md
    with open(sources_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Regex to find footnotes e.g. [^ms96]: ...
    declarations = re.findall(r'^\[\^([^\]]+)\]:\s*(.*)', content, re.MULTILINE)
    
    declared_keys = {decl[0]: decl[1] for decl in declarations}
    
    # 2. Get list of files on disk (lowercased, without extensions)
    disk_files = {os.path.splitext(f)[0].lower() for f in os.listdir(archive_dir) if f.endswith('.txt')}
    
    print(f"Total Declared References in Sources.md: {len(declared_keys)}")
    print(f"Total Files currently in Sources_Archive: {len(disk_files)}")
    print("\n--- DECLARED KEY VS DISK FILE STATUS ---")
    
    missing_from_disk = []
    for key, val in declared_keys.items():
        if key.lower() not in disk_files:
            missing_from_disk.append((key, val))
            
    if missing_from_disk:
        print(f"\nThere are {len(missing_from_disk)} references declared in Sources.md that are missing on disk:")
        for key, val in missing_from_disk:
            print(f"- [^{key}]: {val}")
    else:
        print("\nAll declared references in Sources.md exist as files on disk!")

if __name__ == "__main__":
    main()
