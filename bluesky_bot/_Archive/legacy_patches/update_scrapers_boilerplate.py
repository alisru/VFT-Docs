import os
import re

hc_path = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\harvest_candidates.py"
one_shot_path = r"e:\Vector Field Theory\VFT Docs\bluesky_bot\google_ai_studio_one_shot.py"

BOILERPLATE_LIST = """BOILERPLATE_PATTERNS = [
    r'this material may not be published',
    r'broadcast,\s*rewritten,\s*or redistributed',
    r'quotes displayed in real-time or delayed',
    r'market data provided by',
    r'you\'ve successfully subscribed',
    r'subscribe to read',
    r'please subscribe to continue',
    r'enjoy unlimited website access',
    r'exclusive content for subscribers',
    r'log in to your account',
    r'all rights reserved\.\s*©',
    r'please enable javascript',
    r'cookies are required',
    r'access denied',
]
"""

# 1. Update harvest_candidates.py
with open(hc_path, "r", encoding="utf-8") as f:
    hc_content = f.read()

if "BOILERPLATE_PATTERNS =" not in hc_content:
    hc_content = BOILERPLATE_LIST + "\n" + hc_content

# Update ArticleContentExtractor.handle_endtag
old_hc_endtag = """    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p = False
            para_text = "".join(self.current_para).strip()
            if para_text:
                self.paragraphs.append(para_text)
            self.current_para = []"""

new_hc_endtag = """    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p = False
            para_text = "".join(self.current_para).strip()
            if para_text:
                p_lower = para_text.lower()
                if not any(re.search(bp, p_lower) for bp in BOILERPLATE_PATTERNS):
                    self.paragraphs.append(para_text)
            self.current_para = []"""

if old_hc_endtag in hc_content:
    hc_content = hc_content.replace(old_hc_endtag, new_hc_endtag)
    print("Patched handle_endtag in harvest_candidates.py")
else:
    print("old_hc_endtag not found")

# Update AD_TEXT_PATTERNS in harvest_candidates.py
old_ad_pat = """AD_TEXT_PATTERNS = [
    r'\\b#ad\\b', r'\\b#sponsored\\b', r'\\b#partner\\b', r'\\b#affiliate\\b',
    r'\\bsponsored post\\b', r'\\bpromoted post\\b', r'\\bpaid partnership\\b',
    r'\\bpaid post\\b', r'\\bpartner content\\b', r'\\baffiliate link\\b',
    r'\\buse code[:\\s]', r'\\bpromo code[:\\s]', r'\\bdiscount code[:\\s]',
    r'\\border now\\b', r'\\bbuy now\\b', r'\\bexclusive discount\\b',
    r'\\bsponsored content\\b', r'\\bpaid advertisement\\b', r'\\badvertisement feature\\b',
    r'\\bsubscribe to read\\b', r'\\benjoy unlimited website access\\b',
    r'\\bexclusive content for subscribers\\b', r'\\bplease subscribe to continue reading\\b'
]"""

new_ad_pat = """AD_TEXT_PATTERNS = [
    r'\\b#ad\\b', r'\\b#sponsored\\b', r'\\b#partner\\b', r'\\b#affiliate\\b',
    r'\\bsponsored post\\b', r'\\bpromoted post\\b', r'\\bpaid partnership\\b',
    r'\\bpaid post\\b', r'\\bpartner content\\b', r'\\baffiliate link\\b',
    r'\\buse code[:\\s]', r'\\bpromo code[:\\s]', r'\\bdiscount code[:\\s]',
    r'\\border now\\b', r'\\bbuy now\\b', r'\\bexclusive discount\\b',
    r'\\bsponsored content\\b', r'\\bpaid advertisement\\b', r'\\badvertisement feature\\b',
    r'\\bsubscribe to read\\b', r'\\benjoy unlimited website access\\b',
    r'\\bexclusive content for subscribers\\b', r'\\bplease subscribe to continue reading\\b',
    r'this material may not be published', r'broadcast,\\s*rewritten,\\s*or redistributed',
    r'quotes displayed in real-time or delayed', r'market data provided by',
    r'all rights reserved\\.\\s*©'
]"""

if old_ad_pat in hc_content:
    hc_content = hc_content.replace(old_ad_pat, new_ad_pat)
    print("Patched AD_TEXT_PATTERNS in harvest_candidates.py")
else:
    print("old_ad_pat not found")

with open(hc_path, "w", encoding="utf-8") as f:
    f.write(hc_content)

# 2. Update google_ai_studio_one_shot.py
with open(one_shot_path, "r", encoding="utf-8") as f:
    one_content = f.read()

if "BOILERPLATE_PATTERNS =" not in one_content:
    one_content = BOILERPLATE_LIST + "\n" + one_content

old_one_endtag = """    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p = False
            para_text = "".join(self.current_para).strip()
            if para_text:
                self.paragraphs.append(para_text)
            self.current_para = []"""

new_one_endtag = """    def handle_endtag(self, tag):
        if tag == 'p':
            self.in_p = False
            para_text = "".join(self.current_para).strip()
            if para_text:
                p_lower = para_text.lower()
                if not any(re.search(bp, p_lower) for bp in BOILERPLATE_PATTERNS):
                    self.paragraphs.append(para_text)
            self.current_para = []"""

if old_one_endtag in one_content:
    one_content = one_content.replace(old_one_endtag, new_one_endtag)
    print("Patched handle_endtag in google_ai_studio_one_shot.py")
else:
    print("old_one_endtag not found")

# Update scrape_article_text validation
old_scrape = """        parser = ParagraphExtractor()
        parser.feed(response.text)
        return "\\n\\n".join(parser.paragraphs)"""

new_scrape = """        parser = ParagraphExtractor()
        parser.feed(response.text)
        clean_body = "\\n\\n".join(parser.paragraphs).strip()
        if len(clean_body) < 250:
            return "Error: Article body too short or blocked by paywall/boilerplate"
        return clean_body"""

if old_scrape in one_content:
    one_content = one_content.replace(old_scrape, new_scrape)
    print("Patched scrape_article_text in google_ai_studio_one_shot.py")
else:
    print("old_scrape not found")

with open(one_shot_path, "w", encoding="utf-8") as f:
    f.write(one_content)

print("Scrapers successfully updated with auto-flagger and boilerplate filtering.")
