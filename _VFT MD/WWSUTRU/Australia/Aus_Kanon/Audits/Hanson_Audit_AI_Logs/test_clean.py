import re

def clean_text(text):
    # Print the target area before cleaning
    idx = text.lower().find("all i ask of people")
    if idx != -1:
        print(f"Target raw: '{text[idx-50:idx+200]}'")
        
    text = re.sub(r'\d+:\d+\d*\s+minutes?,\s+\d+\s+seconds?', ' ', text)
    text = re.sub(r'seconds([a-zA-Z])', r' \1', text)
    
    # Also handle standard youtube timestamp pattern X:XX
    text = re.sub(r'\b\d+:\d+\b', ' ', text)
    
    text = text.replace("--", " ").replace("—", " ").replace("–", " ").replace("-", " ")
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    
    cleaned = " ".join(text.split())
    
    idx_clean = cleaned.find("all i ask of people")
    if idx_clean != -1:
        print(f"Cleaned snippet: '{cleaned[idx_clean-20:idx_clean+200]}'")
    else:
        print("Not found in cleaned!")
        
    return cleaned

def main():
    filepath = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive\enoughrope04.txt"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    clean_text(content)

if __name__ == "__main__":
    main()
