import json
import os

def main():
    json_path = "fetch_wikipedia_20260708.json"
    wiki_path = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive\wiki.txt"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    results = data.get('results', [])
    if results:
        res = results[0]
        url = res.get('url')
        title = res.get('title', 'Unknown Title')
        excerpts = res.get('excerpts', [])
        content = "\n".join(excerpts)
        
        output_content = f"SOURCE: [^wiki]\n"
        output_content += f"TITLE: {title}\n"
        output_content += f"PRIMARY URL: {url}\n\n"
        output_content += "---CONTENT---\n\n"
        output_content += content
        
        with open(wiki_path, 'w', encoding='utf-8') as out_f:
            out_f.write(output_content)
        print("Updated wiki.txt with actual Wikipedia article content.")

if __name__ == "__main__":
    main()
