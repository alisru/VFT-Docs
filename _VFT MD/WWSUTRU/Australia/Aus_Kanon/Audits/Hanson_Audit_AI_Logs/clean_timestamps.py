import re
import os

def clean_transcript_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove timestamp headers like "3:563 minutes, 56 seconds" or similar patterns
    # e.g., "3:483 minutes, 48 seconds"
    # Regex: match numbers, colons, words like "minutes", "seconds", "hour", etc.
    cleaned = re.sub(r'\d+:\d+\d*\s+minutes?,\s+\d+\s+seconds?', '', content)
    cleaned = re.sub(r'\d+\s+minutes?,\s+\d+\s+seconds?', '', cleaned)
    cleaned = re.sub(r'\d+:\d+\s+seconds?', '', cleaned)
    cleaned = re.sub(r'\d+\s+minutes?', '', cleaned)
    
    # Replace multiple spaces/newlines with single ones
    cleaned = "\n".join([line.strip() for line in cleaned.splitlines() if line.strip()])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f"Cleaned timestamps from {filepath}")

def main():
    filepath = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive\enoughrope04.txt"
    clean_transcript_file(filepath)

if __name__ == "__main__":
    main()
