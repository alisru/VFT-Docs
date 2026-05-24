import os
import re
import argparse

def get_summarized_files(summaries_path):
    summarized = set()
    if not os.path.exists(summaries_path):
        return summarized

    # Matches ### [Filename.md] (Date)
    pattern = re.compile(r'^### \[(.*?)\]')

    with open(summaries_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.match(line)
            if match:
                summarized.add(match.group(1))
    return summarized

def discover_files(target_dir, summarized):
    unsummarized = []
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.md'):
                if file not in summarized:
                    full_path = os.path.join(root, file)
                    # Convert to relative path for the handover
                    rel_path = os.path.relpath(full_path, start='.')
                    # Convert to Windows style as per VFT rules
                    win_path = rel_path.replace('/', '\\')
                    unsummarized.append((file, win_path))
    return unsummarized

def generate_handover(unsummarized, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Discovered Unsummarized Files\n\n")
        f.write(f"Total found: {len(unsummarized)}\n\n")
        f.write("## Unsummarized File Queue\n\n")
        for file, path in unsummarized:
            f.write(f"- [ ] {file} (Path: {path})\n")

def main():
    parser = argparse.ArgumentParser(description='Discover unsummarized VFT files.')
    parser.add_argument('directory', help='Directory to scan')
    parser.add_argument('--summaries', default='file_summaries.md', help='Path to master summaries file')
    parser.add_argument('--output', default='discovered_handover.md', help='Output handover file')

    args = parser.parse_args()

    summarized = get_summarized_files(args.summaries)
    unsummarized = discover_files(args.directory, summarized)

    if unsummarized:
        generate_handover(unsummarized, args.output)
        print(f"Discovered {len(unsummarized)} unsummarized files. Generated {args.output}")
    else:
        print("No unsummarized files found in the target directory.")

if __name__ == "__main__":
    main()
