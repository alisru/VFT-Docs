# -*- coding: utf-8 -*-
import os, sys, json, re, time
import urllib.request, urllib.parse, xml.etree.ElementTree as ET
from harvest_candidates import scrape_article_content, normalize_url

script_dir = os.path.dirname(os.path.abspath(__file__))
candidates_file = os.path.join(script_dir, "harvested_candidates.json")

if not os.path.exists(candidates_file):
    print(f"Error: {candidates_file} not found.")
    sys.exit(1)

with open(candidates_file, "r", encoding="utf-8") as f:
    candidates = json.load(f)

print(f"Loaded {len(candidates)} candidates from queue. Expanding with multi-source comparison...")

def find_alternative_sources(subject, primary_url, max_extra=2):
    clean_words = re.findall(r'\b[a-zA-Z0-9]{3,}\b', subject)
    query = ' '.join(clean_words[:6])
    encoded_q = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_q}&hl=en-US&gl=US&ceid=US:en"
    
    req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    results = []
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        items = root.findall('.//item')
        
        primary_host = urllib.parse.urlparse(primary_url.lower()).hostname or ""
        if primary_host.startswith("www."):
            primary_host = primary_host[4:]
            
        seen_publishers = {primary_host}
        
        for item in items:
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            source_tag = item.find('source')
            pub = source_tag.text.strip() if source_tag is not None and source_tag.text else ''
            
            if not link or not pub:
                continue
                
            pub_clean = pub.lower().replace("www.", "")
            if pub_clean in seen_publishers:
                continue
                
            seen_publishers.add(pub_clean)
            results.append({'title': title, 'publisher': pub, 'url': link})
            if len(results) >= max_extra:
                break
    except Exception as ex:
        pass
    return results

enriched_count = 0
for idx, c in enumerate(candidates, 1):
    subject = c.get("subject") or c.get("title") or ""
    primary_url = c.get("url") or ""
    primary_text = c.get("text") or ""
    primary_pub = c.get("publisher") or urllib.parse.urlparse(primary_url).hostname or "Primary Source"
    
    if not subject:
        continue
        
    print(f"[{idx}/{len(candidates)}] Searching alternative sources for: {subject[:50]}...")
    alt_sources = find_alternative_sources(subject, primary_url, max_extra=2)
    
    if alt_sources:
        cluster_sources = [{
            "publisher": primary_pub,
            "url": primary_url,
            "snippet": primary_text[:300].strip()
        }]
        
        dossier_lines = [
            f"=== MULTI-SOURCE TOPIC CLUSTER: {subject} ===",
            f"\n[Source 1 -- {primary_pub}] (URL: {primary_url}):\n{primary_text[:1000].strip()}"
        ]
        
        for s_idx, alt in enumerate(alt_sources, 2):
            alt_pub = alt["publisher"]
            alt_url = alt["url"]
            alt_title, alt_desc, alt_body = scrape_article_content(alt_url)
            
            clean_body = alt_body if (alt_body and not alt_body.startswith("Error")) else alt_desc or alt["title"]
            cluster_sources.append({
                "publisher": alt_pub,
                "url": alt_url,
                "snippet": clean_body[:300].strip()
            })
            dossier_lines.append(f"\n[Source {s_idx} -- {alt_pub}] (URL: {alt_url}):\n{clean_body[:1000].strip()}")
            
        c["is_multi_source"] = True
        c["cluster_sources"] = cluster_sources
        c["cross_source_dossier"] = "\n".join(dossier_lines)
        c["text"] = f"Stated Claim / Post Context:\n{subject}\n\n{c['cross_source_dossier']}"
        enriched_count += 1
        print(f"  -> Enriched with {len(alt_sources)} alternative source(s): {[s['publisher'] for s in alt_sources]}")
    else:
        c["is_multi_source"] = False
        c["cluster_sources"] = [{
            "publisher": primary_pub,
            "url": primary_url,
            "snippet": primary_text[:300].strip()
        }]
        print(f"  -> Single source maintained.")

with open(candidates_file, "w", encoding="utf-8") as f:
    json.dump(candidates, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully enriched {enriched_count}/{len(candidates)} candidates into Multi-Source Topic Clusters!")
