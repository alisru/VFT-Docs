import json
import os

def process_results(json_path, name_mapping):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    results = data.get('results', [])
    for res in results:
        url = res.get('url')
        matched_key = None
        for key, u in name_mapping.items():
            if u in url:
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
            
            output_path = os.path.join(r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\Aus_Kanon\Audits\Hanson_Audit\Sources_Archive", f"{matched_key}.txt")
            with open(output_path, 'w', encoding='utf-8') as out_f:
                out_f.write(output_content)
            print(f"Created/Updated: {matched_key}.txt")

def main():
    # Mapping of keys to URL identifiers
    mapping_1 = {
        "oa_dairylastchance": "2019-12-02.7.1",
        "oa_gamblingpartoflife": "2017-03-20.161.2",
        "oa_cronulla": "2026-06-24.31.1"
    }
    
    mapping_2 = {
        "hansard22crown": "2022-09-27.103.2",
        "onenation_aboriginalspend": "hanson-aboriginal-spending-accountability",
        "onenation_nativetitlepetition": "australia-native-title-enough",
        "wtc_afl25": "lies-hanson-urges-aussies-to-ignore-welcome-to-country",
        "onenation_bradfield19": "pauline-hanson-calls-for-construction-of-bradfield-and-ord-schemes-to-drought-proof-inland-australia",
        "onenation_senategrowth25": "one-nation-senate-growth-hanson-milestone"
    }
    
    process_results("fetch_openaustralia_20260708.json", mapping_1)
    process_results("fetch_onenation_openaustralia_20260708.json", mapping_2)

if __name__ == "__main__":
    main()
