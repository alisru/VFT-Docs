import sys
import os
import re
import urllib.parse
import subprocess
import shutil
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

def repair_math(content: str) -> str:
    pattern = r'\[!\[.*?\]\(.*?\)\]\(https://www\.codecogs\.com/eqnedit\.php\?latex=([^)#]+).*?\)'
    
    def replace_latex(match):
        encoded = match.group(1)
        try:
            decoded = urllib.parse.unquote(encoded)
            return f" $$ {decoded} $$ "
        except Exception:
            return match.group(0)
            
    return re.sub(pattern, replace_latex, content)

def process_directory(src_dir: Path, dest_dir: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    docx_files = list(src_dir.glob("*.docx"))
    print(f"Processing {len(docx_files)} docx files from {src_dir} to {dest_dir}...")
    
    for docx in docx_files:
        md_name = docx.stem + ".md"
        dest_md = dest_dir / md_name
        
        print(f"Converting: {docx.name} -> {md_name}")
        cmd = [
            "pandoc",
            "-f", "docx",
            "-t", "markdown+hard_line_breaks-smart",
            "--wrap=none",
            "-o", str(dest_md),
            str(docx)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            print(f"Error converting {docx.name}: {res.stderr}")
        else:
            try:
                content = dest_md.read_text(encoding="utf-8")
                fixed = repair_math(content)
                if fixed != content:
                    dest_md.write_text(fixed, encoding="utf-8")
                    print(f"  Fixed math in {md_name}")
            except Exception as e:
                print(f"  Error reading/writing {md_name}: {e}")

    md_files = list(src_dir.glob("*.md"))
    print(f"Copying {len(md_files)} existing md files from {src_dir} to {dest_dir}...")
    for md in md_files:
        dest_md = dest_dir / md.name
        shutil.copy2(md, dest_md)
        print(f"Copied {md.name}")

if __name__ == "__main__":
    base_src = Path(r"E:\Vector Field Theory\VFT Docs\io")
    base_dest = Path(r"E:\Vector Field Theory\VFT Docs\_VFT MD\io")
    
    # Process IRM
    process_directory(base_src / "irm", base_dest / "irm")
    
    # Process Value Physics
    process_directory(base_src / "value physics", base_dest / "value physics")
    
    print("Done processing all folders.")
