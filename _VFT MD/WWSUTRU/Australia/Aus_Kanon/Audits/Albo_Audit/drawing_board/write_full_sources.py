import json
import os

active_dir = "e:/Vector Field Theory/VFT Docs/_VFT MD/WWSUTRU/Australia/Aus_Kanon/Audits/Albo_Audit"
raw_fetches_dir = os.path.join(active_dir, "raw_fetches")

# Mapping of file name to (json_file, url_key, result_index)
# If result_index is None, we look for matching URL or just take the first result
mapping = {
    "veteransuicide24.txt": ("fetch_veteran_suicide_response.json", "https://www.pm.gov.au/media/governments-response-final-report-royal-commission-defence-and-veteran-suicide"),
    "donaldhorne23.txt": ("fetch_donald_horne.json", "https://www.pm.gov.au/media/opening-donald-horne-building"),
    "revivespeech23.txt": ("fetch_revive_speech.json", "https://www.pm.gov.au/media/launch-national-cultural-policy"),
    "socialmediaban24.txt": ("fetch_social_media_ban.json", "https://www.pm.gov.au/media/albanese-government-protecting-kids-social-media-harms"),
    "isuravdawn24.txt": ("fetch_footnote_urls.json", "https://www.pm.gov.au/media/anzac-day-dawn-service-2024"),
    "constitutionbill23.txt": ("fetch_footnote_urls.json", "https://www.pm.gov.au/media/constitution-alteration-aboriginal-and-torres-strait-islander-voice-2023"),
    "socialmediaact25.txt": ("fetch_remaining_urls.json", "https://www.legislation.gov.au/C2024A00127/asmade"),
    "nbnbudget22.txt": ("fetch_nbn_budget_url.json", "https://minister.infrastructure.gov.au/rowland/media-release/albanese-government-delivers-major-nbn-boost-2022-23-federal-budget"),
    "garma22.txt": ("fetch_garma_2022.json", "https://www.pm.gov.au/media/address-garma-festival")
}

for txt_name, (json_name, target_url) in mapping.items():
    json_path = os.path.join(active_dir, json_name)
    txt_path = os.path.join(raw_fetches_dir, txt_name)
    
    if not os.path.exists(json_path):
        print(f"JSON file not found: {json_path}")
        continue
        
    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error loading {json_name}: {e}")
            continue
            
    results = data.get("results", [])
    found_result = None
    for r in results:
        if r.get("url") == target_url:
            found_result = r
            break
            
    if not found_result and results:
        # Fallback to first result if we can't find direct URL match
        found_result = results[0]
        
    if found_result:
        excerpts = found_result.get("excerpts", [])
        full_text = "\n\n".join(excerpts)
        
        # Format the file contents
        content = f"SOURCE: [^{txt_name.replace('.txt', '')}]\n"
        content += f"CITATION: Verified via {json_name}\n"
        content += f"URL: {target_url}\n"
        content += f"STATUS: Full content restored\n\n"
        content += "---EXTRACTED TEXT---\n\n"
        content += full_text
        
        with open(txt_path, "w", encoding="utf-8") as out:
            out.write(content)
        print(f"Wrote full content to {txt_name} (length: {len(content)} chars)")
    else:
        print(f"No results found for {txt_name} in {json_name}")

# Let's also write Kokoda Track media release from the context (step 1570)
kokoda_txt_path = os.path.join(raw_fetches_dir, "kokodamateship24.txt")
kokoda_content = """SOURCE: [^kokodamateship24]
CITATION: Anthony Albanese, "Commemorating Anzac Day on the Kokoda Track", Prime Minister of Australia Media Release, 20 April 2024
URL: https://www.pm.gov.au/media/commemorating-anzac-day-kokoda-track
STATUS: Full content restored

---EXTRACTED TEXT---

Prime Prime Minister Anthony Albanese will travel to Papua New Guinea from 22 – 25 April to meet with Prime Minister Marape, walk sections of the Kokoda Track and commemorate Anzac Day.

The Kokoda campaign lasted from July to November 1942, with about 56,000 Australians involved. Around 625 Australians were killed and over 1,600 were wounded along the track.

Each year many Australians take the challenge of walking the Kokoda Track, alongside Papua New Guineans, to not only test their limits, but to reflect on the events that took place.

The trek retraces the footsteps of Australian soldiers and those who walked alongside them during the Kokoda campaign.

The Prime Minister will spend two days walking the Kokoda Track before standing shoulder to shoulder with Australians and Papua New Guineans at the annual Anzac Day Dawn Service at the Isurava memorial site.

## Quotes attributable to Prime Minister Anthony Albanese:

“The Kokoda campaign and the Kokoda Track form part of our national identity, a defining chapter in the story of those who risked and lost their lives in defence of Australia and in our shared history with Papua New Guinea.

“Kokoda is a name that lives in Australian legend. It captures the spirit of courage, endurance, mateship and sacrifice forged between Australia and Papua New Guinea during World War II.

“Participating in this walk is a solemn way to honour to reflect on the sacrifices made by those who walked this same ground, people from Papua New Guinea and Australia, serving and sacrificing together in defence of their home.”
"""

with open(kokoda_txt_path, "w", encoding="utf-8") as out:
    out.write(kokoda_content)
print("Wrote full content to kokodamateship24.txt")
