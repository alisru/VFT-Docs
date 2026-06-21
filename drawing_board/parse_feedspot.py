import re
from urllib.parse import unquote
from bs4 import BeautifulSoup

filepath = r"C:\Users\hungh\.gemini\antigravity\brain\97fd7b60-d4b8-41d0-8f03-65e750998f03\.system_generated\steps\811\content.md"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

# Find all headings
headings = soup.find_all(class_='feed_heading')
print(f"Found {len(headings)} feed headings.")

parsed_feeds = []
for h3 in headings:
    # Next sibling
    p = h3.find_next_sibling('p', class_='trow')
    if not p:
        continue
    
    # Title
    title_a = h3.find('a', class_='tlink')
    title = title_a.text.strip() if title_a else h3.text.strip()
    
    # RSS URL from data-site
    rss_encoded = p.get('data-site', '')
    rss = unquote(rss_encoded) if rss_encoded else None
    
    # If rss is empty or not direct, try to look for the first link with class "ext"
    if not rss or not (rss.startswith('http') and ('rss' in rss.lower() or 'xml' in rss.lower() or 'feed' in rss.lower())):
        # Try to find link inside p
        ext_links = p.find_all('a', class_='ext')
        for a in ext_links:
            href = a.get('href', '')
            if href and ('rss' in href.lower() or 'xml' in href.lower() or 'feed' in href.lower()):
                rss = href
                break
                
    # Facebook Followers
    fb_el = p.find(class_='fs-facebook')
    fb = None
    if fb_el:
        val_el = fb_el.find(class_='eng_v')
        if val_el:
            fb = val_el.text.strip()
            
    # Twitter Followers
    tw_el = p.find(class_='fs-twitter')
    tw = None
    if tw_el:
        val_el = tw_el.find(class_='eng_v')
        if val_el:
            tw = val_el.text.strip()
            
    # Site
    site = None
    ext_links = p.find_all('a', class_='ext')
    for a in ext_links:
        href = a.get('href', '')
        if href and not ('rss' in href.lower() or 'xml' in href.lower() or 'feed' in href.lower()):
            site = href
            break
            
    parsed_feeds.append({
        'title': title,
        'rss': rss,
        'site': site,
        'fb': fb,
        'tw': tw
    })

print(f"Parsed {len(parsed_feeds)} feeds in total.")

print("\n--- FEEDS WITH FACEBOOK FOLLOWERS ---")
feeds_with_fb = [f for f in parsed_feeds if f['fb']]
for idx, f in enumerate(feeds_with_fb, 1):
    print(f"{idx}. {f['title']} (FB: {f['fb']}, TW: {f['tw']}) -> RSS: {f['rss']}")
