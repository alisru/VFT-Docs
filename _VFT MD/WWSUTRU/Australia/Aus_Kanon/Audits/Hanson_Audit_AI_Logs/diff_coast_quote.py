import re

def clean_text(text):
    text = text.replace("--", " ").replace("—", " ").replace("–", " ").replace("-", " ")
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return " ".join(text.split())

def main():
    md_quote = "Any foreign ownership is regrettable, but why are we allowing the Chinese government, an oppressive communist regime, to own our land and assets? Why are we allowing our ports, utilities, services, agricultural land and housing to be sold?"
    
    with open(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive\ms16.txt", "r", encoding="utf-8") as f:
        src_text = f.read()
        
    c_md = clean_text(md_quote)
    c_src = clean_text(src_text)
    
    print(f"MD Cleaned:  {c_md}")
    print(f"SRC Cleaned: {c_src[c_src.find('any foreign ownership'):c_src.find('any foreign ownership')+400]}")
    
    if c_md in c_src:
        print("MATCH FOUND!")
    else:
        print("NO MATCH!")
        # Find where they diverge
        words_md = c_md.split()
        words_src = c_src.split()
        start_idx = c_src.find("any foreign ownership")
        if start_idx != -1:
            words_src_sub = c_src[start_idx:].split()
            for i, (w_md, w_src) in enumerate(zip(words_md, words_src_sub)):
                if w_md != w_src:
                    print(f"Divergence at word {i}: MD has '{w_md}', SRC has '{w_src}'")
                    break

if __name__ == "__main__":
    main()
