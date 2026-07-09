import json
import os

def main():
    json_path = "fetch_remaining_sources_20260708.json"
    archive_dir = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive"
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    mapping = {
        "senate18prot": "protect-our-australian-way-of-life-senate-speech",
        "onenation_toothfairy": "end-indigenous-claims",
        "netimes26": "hansons-press-club-speech-the-crib-notes",
        "sbsnpc": "hanson-one-nation-press-club-speech",
        "sbspenalty17": "hanson-calls-off-senate-voting-strike",
        "sbsmigration": "bad-people-from-bad-countries-taylor-doubles-down-on-migration-crackdown",
        "sbsdastyari": "smart-arse-hanson-refuses-to-condemn-racial-attack-on-pipsqueak-dastyari",
        "onenation_netzero": "net-zero-destroying-australia",
        "oa_abcbattle": "2017-09-13.65.1"
    }
    
    results = data.get('results', [])
    for res in results:
        url = res.get('url')
        matched_key = None
        for key, marker in mapping.items():
            if marker in url:
                matched_key = key
                break
                
        if matched_key:
            title = res.get('title', 'Unknown Title')
            publish_date = res.get('publish_date', 'Unknown Date')
            excerpts = res.get('excerpts', [])
            content = "\n".join(excerpts)
            
            output_content = f"SOURCE: [^{matched_key}]\n"
            output_content += f"TITLE: {title}\n"
            output_content += f"PUBLISHED: {publish_date}\n"
            output_content += f"PRIMARY URL: {url}\n\n"
            output_content += "---CONTENT---\n\n"
            output_content += content
            
            output_path = os.path.join(archive_dir, f"{matched_key}.txt")
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(output_content)
            print(f"Created/Updated: {matched_key}.txt")

if __name__ == "__main__":
    main()
