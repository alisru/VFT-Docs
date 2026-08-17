"""export_audit_site.py — One-click static site exporter for Aletheia Audit Control Panel.

Bundles the complete 8,640+ story audit dataset, interactive charts, and Hegemony database
into a zero-dependency static folder (dist_audit_site/) ready for instant hosting on
GitHub Pages, Cloudflare Pages, Netlify, Vercel, or any static web server.
"""
import os
import sys
import shutil
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
dist_dir = os.path.join(script_dir, "dist_audit_site")
os.makedirs(dist_dir, exist_ok=True)

files_to_copy = [
    ("stories_registry.js", "stories_registry.js"),
    ("alethekanon.png", "alethekanon.png"),
    ("policy_ledger.json", "policy_ledger.json")
]

parent_dir = os.path.dirname(script_dir)
hegemony_src = os.path.join(parent_dir, "hegemony_db.js")
if os.path.exists(hegemony_src):
    shutil.copy2(hegemony_src, os.path.join(dist_dir, "hegemony_db.js"))
    print(f"[OK] Bundled: hegemony_db.js")

# Copy and sanitize control_panel.html -> index.html
cp_src = os.path.join(script_dir, "control_panel.html")
if os.path.exists(cp_src):
    with open(cp_src, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    import re
    # 1. Strip out the private chat button for the public site
    html_sanitized = re.sub(
        r'<button[^>]*window\.open\([\'\"]aletheia_chat\.html[\'\"][^>]*>[\s\S]*?</button>',
        '',
        html_content
    )
    # 2. Strip out the Controller & Composer tab button
    html_sanitized = re.sub(
        r'<button[^>]*switchTab\(event,\s*[\'\"]composer-tab[\'\"]\)[^>]*>[\s\S]*?</button>',
        '',
        html_sanitized
    )
    # 3. Strip out the entire Controller & Composer tab viewport content
    html_sanitized = re.sub(
        r'<!-- Tab 3: Composer & CLI Controller -->[\s\S]*?</div>\s*</div>\s*(?=<!-- Lightbox)',
        '',
        html_sanitized
    )
    
    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_sanitized)
    print(f"[OK] Bundled & Sanitized: control_panel.html -> index.html (stripped private chat & controller tabs)")

for src_name, dst_name in files_to_copy:
    src_path = os.path.join(script_dir, src_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, os.path.join(dist_dir, dst_name))
        print(f"[OK] Bundled: {src_name} -> {dst_name}")
    else:
        print(f"[WARN] Missing source: {src_name}")

# Remove any old chat.html from dist_audit_site if present
old_chat = os.path.join(dist_dir, "chat.html")
if os.path.exists(old_chat):
    os.remove(old_chat)

# Also copy graph images if available
graph_src_dir = os.path.join(script_dir, "graph_png")
graph_dst_dir = os.path.join(dist_dir, "graph_png")
if os.path.exists(graph_src_dir):
    os.makedirs(graph_dst_dir, exist_ok=True)
    count = 0
    for f in os.listdir(graph_src_dir):
        if f.endswith(".png"):
            shutil.copy2(os.path.join(graph_src_dir, f), os.path.join(graph_dst_dir, f))
            count += 1
    print(f"[OK] Bundled: {count} trajectory graph images in graph_png/")

# Bundle static article sources from harvested_stories_log.jsonl
log_file = os.path.join(script_dir, "harvested_stories_log.jsonl")
sources_dst_dir = os.path.join(dist_dir, "sources")
if os.path.exists(log_file):
    os.makedirs(sources_dst_dir, exist_ok=True)
    sources_count = 0
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.strip():
                try:
                    obj = json.loads(line)
                    sid = obj.get("id") or ""
                    url = obj.get("url") or ""
                    text = obj.get("text") or ""
                    if text and (sid or url):
                        payload = {
                            "id": sid,
                            "url": url,
                            "title": obj.get("title", ""),
                            "text": text,
                            "timestamp": obj.get("timestamp", "")
                        }
                        if sid:
                            with open(os.path.join(sources_dst_dir, f"{sid}.json"), "w", encoding="utf-8") as sf:
                                json.dump(payload, sf, ensure_ascii=False)
                            sources_count += 1
                except Exception:
                    pass
    print(f"[OK] Bundled: {sources_count} static source article JSONs in sources/")

print("\n" + "=" * 60)
print(f"ALETHEIA AUDIT STATIC SITE READY")
print(f"Output Directory: {dist_dir}")
print("=" * 60)
print("You can deploy this directory directly to:")
print("1. GitHub Pages (push dist_audit_site/ contents to gh-pages branch)")
print("2. Cloudflare Pages / Netlify / Vercel (set build output directory to 'bluesky_bot/dist_audit_site')")
print("3. Any static web hosting service (drag and drop the dist_audit_site folder)")
