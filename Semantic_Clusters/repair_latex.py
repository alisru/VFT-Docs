import os
import re
import urllib.parse
import sys

def repair_content(content):
    # Balanced parenthesis regex matching for the CodeCogs query parameters
    pattern = re.compile(
        r'\[!\[\]\(media/image\d+\.png\)\{[^}]*\}\]\(https://www\.codecogs\.com/eqnedit\.php\?latex=([^)]*(?:\([^)]*\)[^)]*)*)\)'
    )
    
    matches = pattern.findall(content)
    if not matches:
        return content, 0
        
    def replace_match(match):
        encoded_latex = match.group(1)
        decoded = urllib.parse.unquote(encoded_latex)
        
        # Clean up any trailing anchors like #0, #1, etc.
        decoded = re.sub(r'#\d+$', '', decoded)
        
        # Return cleanly formatted inline LaTeX
        return f"${decoded}$"
        
    new_content = pattern.sub(replace_match, content)
    return new_content, len(matches)

def repair_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content, count = repair_content(content)
    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Repaired {count} LaTeX conversion errors in: {os.path.relpath(file_path, '.')}", flush=True)
        return True
    return False

def main():
    if sys.version_info >= (3, 7):
        sys.stdout.reconfigure(encoding='utf-8')
        
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    print("Scanning workspace for markdown files containing CodeCogs LaTeX conversions...", flush=True)
    
    repaired_count = 0
    for root, dirs, files in os.walk(workspace_root):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() not in ['venv', 'env', 'bible', 'node_modules', 'geometry of definitions', 'scratch', 'drawing board']]
        
        for file in files:
            if file.lower().endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    if repair_file(file_path):
                        repaired_count += 1
                except Exception as e:
                    print(f"Error processing {file_path}: {e}", flush=True)
                    
    print(f"Scan complete. Repaired LaTeX in {repaired_count} files.", flush=True)

if __name__ == "__main__":
    main()
