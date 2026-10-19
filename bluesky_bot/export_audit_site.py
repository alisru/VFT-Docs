"""export_audit_site.py — One-click static site exporter for Aletheia Audit Control Panel.

Bundles the complete 13,590+ story audit dataset, interactive vector trajectory charts,
and Hegemony database into a zero-dependency static folder (dist_audit_site/)
ready for instant hosting on GitHub Pages, Cloudflare Pages, Netlify, Vercel, or any static server.

Features:
- Pure Programmatic Assets: All trajectory graphs and infographic cards are generated
  directly in client HTML5 Canvas using the EXACT 1:1 ported process of generate_graph.py
  and image_card_generator.py (aletheia_canvas_renderer.js) — NO external PNGs required.
- Single Unified Dataset: All audits load directly from stories_registry.js — NO individual
  JSON files (sources/*.json) needed.
- Pristine Local Workspace: control_panel.html in the workspace is NEVER modified.
"""
import os
import sys
import shutil
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
dist_dir = os.path.join(script_dir, "dist_audit_site")
os.makedirs(dist_dir, exist_ok=True)

print("=" * 60)
print("ALETHEIA ZERO-DEPENDENCY STATIC SITE EXPORT")
print("=" * 60)

# 1. Bundle hegemony_db.js
parent_dir = os.path.dirname(script_dir)
hegemony_src = os.path.join(parent_dir, "hegemony_db.js")
if os.path.exists(hegemony_src):
    shutil.copy2(hegemony_src, os.path.join(dist_dir, "hegemony_db.js"))
    print(f"[OK] Bundled: hegemony_db.js (49-point matrix database)")
else:
    print(f"[WARN] Missing hegemony_db.js at {hegemony_src}")

# 2. Bundle stories_registry.js
stories_src = os.path.join(script_dir, "stories_registry.js")
if os.path.exists(stories_src):
    shutil.copy2(stories_src, os.path.join(dist_dir, "stories_registry.js"))
    size_mb = os.path.getsize(stories_src) / (1024 * 1024)
    print(f"[OK] Bundled: stories_registry.js ({size_mb:.1f} MB unified audit dataset)")
else:
    print(f"[WARN] Missing stories_registry.js at {stories_src}")

# 3. Bundle aletheia_canvas_renderer.js
renderer_src = os.path.join(script_dir, "aletheia_canvas_renderer.js")
if os.path.exists(renderer_src):
    shutil.copy2(renderer_src, os.path.join(dist_dir, "aletheia_canvas_renderer.js"))
    print(f"[OK] Bundled: aletheia_canvas_renderer.js (Exact 1:1 Canvas Engine)")
else:
    print(f"[WARN] Missing aletheia_canvas_renderer.js at {renderer_src}")

# 3. Copy and sanitize control_panel.html -> dist_audit_site/index.html
cp_src = os.path.join(script_dir, "control_panel.html")
if os.path.exists(cp_src):
    with open(cp_src, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 3.1 Strip out private chat button
    html_sanitized = re.sub(
        r'<button[^>]*window\.open\([\'\"]aletheia_chat\.html[\'\"][^>]*>[\s\S]*?</button>',
        '',
        html_content
    )

    # 3.2 Strip out Controller & Composer tab button
    html_sanitized = re.sub(
        r'<button[^>]*switchTab\(event,\s*[\'\"]composer-tab[\'\"]\)[^>]*>[\s\S]*?</button>',
        '',
        html_sanitized
    )

    # 3.3 Strip out Controller & Composer tab viewport content
    html_sanitized = re.sub(
        r'<!-- Tab 3: Composer & CLI Controller -->[\s\S]*?</div>\s*</div>\s*(?=<!-- Lightbox)',
        '',
        html_sanitized
    )

    # 3.4 Fix relative path for hegemony_db.js in standalone bundle
    html_sanitized = html_sanitized.replace('src="../hegemony_db.js"', 'src="hegemony_db.js"')

    # 3.5 Include exact canvas renderer script right before main script
    html_sanitized = html_sanitized.replace(
        '<script src="stories_registry.js"></script>',
        '<script src="stories_registry.js"></script>\n  <script src="aletheia_canvas_renderer.js"></script>'
    )

    # 3.6 Guard renderController against null DOM references (prevents TypeError on line 2275)
    html_sanitized = html_sanitized.replace(
        "function renderController() {",
        "function renderController() {\n      if (!document.getElementById('terminalCmd')) return;"
    )

    # 3.7 Replace Post 0 embed image tags with exact programmatic canvas cards in dist_audit_site
    old_embed_code = """        if (index === 0) {
          let embedImages = [];
          if (activeStory.graph_img) {
            embedImages.push(activeStory.graph_img);
          }
          if (isFiveWord) {
            embedImages.push(`graph_png/${activeStory.id}_info_card_five_word.png`);
          } else if (isCompactSingle || isCompactThread) {
            embedImages.push(`graph_png/${activeStory.id}_info_card_verdict.png`);
            embedImages.push(`graph_png/${activeStory.id}_info_card_analysis.png`);
          }
          
          if (embedImages.length > 0) {
            embedTag = `<div style="display: grid; grid-template-columns: repeat(${Math.min(embedImages.length, 2)}, 1fr); gap: 0.5rem; margin-top: 0.75rem;">`;
            embedImages.forEach(img => {
              embedTag += `<img class="post-embed-image" src="${img}" alt="Embed Media" style="margin: 0; aspect-ratio: 16/10; object-fit: cover;" onerror="this.style.display='none';" onclick="openLightbox('${img}')">`;
            });
            embedTag += `</div>`;
          }
        }"""

    new_embed_code = """        if (index === 0) {
          embedTag = `
            <div id="embedCanvasContainer" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 0.75rem; margin-top: 0.75rem;">
              <div class="embed-tile" onclick="openLightboxCanvas('graph')" style="cursor: pointer; background: #111111; border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; overflow: hidden;">
                <div style="padding: 4px 8px; font-size: 0.68rem; font-weight: 700; color: #94a3b8; background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.06); display: flex; justify-content: space-between;">
                  <span>📈 TRAJECTORY GRAPH</span><span style="color: var(--bsky-blue)">Magnify ↗</span>
                </div>
                <canvas id="postCanvas_graph" style="width: 100%; aspect-ratio: 1/1; display: block;"></canvas>
              </div>
              ${activeStory.five_word ? `
                <div class="embed-tile" onclick="openLightboxCanvas('five_word')" style="cursor: pointer; background: #0B0F19; border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; overflow: hidden;">
                  <div style="padding: 4px 8px; font-size: 0.68rem; font-weight: 700; color: #F59E0B; background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.06); display: flex; justify-content: space-between;">
                    <span>⚡ 5-WORD CARD</span><span style="color: var(--bsky-blue)">Magnify ↗</span>
                  </div>
                  <canvas id="postCanvas_five_word" style="width: 100%; aspect-ratio: 1100/860; display: block;"></canvas>
                </div>
              ` : `
                <div class="embed-tile" onclick="openLightboxCanvas('verdict')" style="cursor: pointer; background: #0B0F19; border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; overflow: hidden;">
                  <div style="padding: 4px 8px; font-size: 0.68rem; font-weight: 700; color: #38BDF8; background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.06); display: flex; justify-content: space-between;">
                    <span>⚖️ VERDICT CARD</span><span style="color: var(--bsky-blue)">Magnify ↗</span>
                  </div>
                  <canvas id="postCanvas_verdict" style="width: 100%; display: block;"></canvas>
                </div>
                <div class="embed-tile" onclick="openLightboxCanvas('analysis')" style="cursor: pointer; background: #0B0F19; border: 1px solid rgba(255,255,255,0.12); border-radius: 8px; overflow: hidden;">
                  <div style="padding: 4px 8px; font-size: 0.68rem; font-weight: 700; color: #C084FC; background: rgba(255,255,255,0.03); border-bottom: 1px solid rgba(255,255,255,0.06); display: flex; justify-content: space-between;">
                    <span>🔬 ANALYSIS CARD</span><span style="color: var(--bsky-blue)">Magnify ↗</span>
                  </div>
                  <canvas id="postCanvas_analysis" style="width: 100%; display: block;"></canvas>
                </div>
              `}
            </div>
          `;
          setTimeout(() => {
            if (window.AletheiaCanvas && activeStory) {
              const cg = document.getElementById('postCanvas_graph');
              if (cg) AletheiaCanvas.drawGraphCanvas(activeStory, cg);
              const cv = document.getElementById('postCanvas_verdict');
              if (cv) AletheiaCanvas.drawVerdictCardCanvas(activeStory, cv);
              const ca = document.getElementById('postCanvas_analysis');
              if (ca) AletheiaCanvas.drawAnalysisCardCanvas(activeStory, ca);
              const cf = document.getElementById('postCanvas_five_word');
              if (cf) AletheiaCanvas.drawFiveWordCardCanvas(activeStory, cf);
            }
          }, 0);
        }"""

    if old_embed_code in html_sanitized:
        html_sanitized = html_sanitized.replace(old_embed_code, new_embed_code)
    else:
        # Regex replacement if whitespace differences exist
        html_sanitized = re.sub(
            r'if \(index === 0\) \{[\s\S]*?embedTag = `<div style="display: grid; grid-template-columns: repeat\(\$\{Math\.min\(embedImages\.length, 2\)\}, 1fr\)[\s\S]*?</div>`;\s*\}\s*\}',
            new_embed_code.replace('\\', '\\\\'),
            html_sanitized
        )

    # 3.8 Replace Generated Assets panel in sidebar with programmatic asset buttons
    old_assets_pattern = r'const assets = \[\s*\{ label: \'Trajectory Graph\', path: `graph_png/\$\{activeStory\.id\}_graph\.png` \}[\s\S]*?const assetsHTML = `[\s\S]*?`;'
    new_assets_code = """const assetsHTML = `
        <div style="margin-top: 1.25rem; border-top: 1px solid var(--panel-border); padding-top: 1rem;">
          <div style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.75rem;">Programmatic Assets</div>
          <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(105px, 1fr)); gap: 0.5rem;">
            <div onclick="openLightboxCanvas('graph')" style="cursor: pointer; background: rgba(255,255,255,0.03); border: 1px solid var(--panel-border); border-radius: 6px; padding: 0.6rem 0.5rem; text-align: center;">
              <div style="font-size: 1.2rem; margin-bottom: 0.25rem;">📈</div>
              <div style="font-size: 0.72rem; font-weight: 600; color: var(--text-primary);">Trajectory Graph</div>
              <div style="font-size: 0.62rem; color: var(--bsky-blue); margin-top: 2px;">Inspect ↗</div>
            </div>
            ${activeStory.five_word ? `
              <div onclick="openLightboxCanvas('five_word')" style="cursor: pointer; background: rgba(255,255,255,0.03); border: 1px solid var(--panel-border); border-radius: 6px; padding: 0.6rem 0.5rem; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.25rem;">⚡</div>
                <div style="font-size: 0.72rem; font-weight: 600; color: var(--text-primary);">5-Word Card</div>
                <div style="font-size: 0.62rem; color: var(--bsky-blue); margin-top: 2px;">Inspect ↗</div>
              </div>
            ` : `
              <div onclick="openLightboxCanvas('verdict')" style="cursor: pointer; background: rgba(255,255,255,0.03); border: 1px solid var(--panel-border); border-radius: 6px; padding: 0.6rem 0.5rem; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.25rem;">⚖️</div>
                <div style="font-size: 0.72rem; font-weight: 600; color: var(--text-primary);">Verdict Card</div>
                <div style="font-size: 0.62rem; color: var(--bsky-blue); margin-top: 2px;">Inspect ↗</div>
              </div>
              <div onclick="openLightboxCanvas('analysis')" style="cursor: pointer; background: rgba(255,255,255,0.03); border: 1px solid var(--panel-border); border-radius: 6px; padding: 0.6rem 0.5rem; text-align: center;">
                <div style="font-size: 1.2rem; margin-bottom: 0.25rem;">🔬</div>
                <div style="font-size: 0.72rem; font-weight: 600; color: var(--text-primary);">Analysis Card</div>
                <div style="font-size: 0.62rem; color: var(--bsky-blue); margin-top: 2px;">Inspect ↗</div>
              </div>
            `}
          </div>
        </div>
      `;"""
    html_sanitized = re.sub(old_assets_pattern, new_assets_code.replace('\\', '\\\\'), html_sanitized)

    # 3.9 Add openLightboxCanvas handler to JavaScript
    lightbox_canvas_code = """
    function openLightboxCanvas(type) {
      if (!window.AletheiaCanvas || !activeStory) return;
      const lightbox = document.getElementById('lightbox');
      const lightboxImg = document.getElementById('lightboxImg');
      let lbCanvas = document.getElementById('lightboxCanvas');
      if (!lbCanvas) {
        lbCanvas = document.createElement('canvas');
        lbCanvas.id = 'lightboxCanvas';
        lbCanvas.style.cssText = 'max-width: 90%; max-height: 85vh; border-radius: 12px; box-shadow: 0 20px 50px rgba(0,0,0,0.7); border: 1px solid rgba(255,255,255,0.15);';
        lightbox.appendChild(lbCanvas);
      }
      if (lightboxImg) lightboxImg.style.display = 'none';
      lbCanvas.style.display = 'block';

      if (type === 'graph') {
        AletheiaCanvas.drawGraphCanvas(activeStory, lbCanvas);
      } else if (type === 'verdict') {
        AletheiaCanvas.drawVerdictCardCanvas(activeStory, lbCanvas);
      } else if (type === 'analysis') {
        AletheiaCanvas.drawAnalysisCardCanvas(activeStory, lbCanvas);
      } else if (type === 'five_word') {
        AletheiaCanvas.drawFiveWordCardCanvas(activeStory, lbCanvas);
      }
      lightbox.classList.add('active');
    }

    const origCloseLightbox = window.closeLightbox;
    window.closeLightbox = function() {
      const lbCanvas = document.getElementById('lightboxCanvas');
      if (lbCanvas) lbCanvas.style.display = 'none';
      const lightbox = document.getElementById('lightbox');
      if (lightbox) lightbox.classList.remove('active');
    };
    """
    html_sanitized = html_sanitized.replace(
        "function closeLightbox() {",
        lightbox_canvas_code + "\n    function closeLightbox_orig() {"
    )

    # 3.10 Upgrade loadSourceArticle to not depend on individual static JSON files
    source_replacement = """if (!url && !story.scraped_text && !story.article_text && !story.text) {
        document.getElementById('sourceTextBody').innerHTML = '<em>No URL or article text stored for this story.</em>';
        return;
      }
      const directText = story.scraped_text || story.article_text || story.text || '';
      if (directText) {
        const paragraphs = directText.split('\\n\\n').filter(p => p.trim());
        const renderedParas = paragraphs.map(p =>
          `<p style="margin:0 0 14px;line-height:1.75;color:var(--text-primary);">${p.replace(/</g,'&lt;').replace(/>/g,'&gt;')}</p>`
        ).join('');
        document.getElementById('sourceTextBody').innerHTML = renderedParas;
        return;
      }
      let data = null;"""
    html_sanitized = re.sub(
        r'if \(!url\) \{\s*document\.getElementById\(\'sourceTextBody\'\)\.innerHTML = \'<em>No URL stored for this story\.</em>\';\s*return;\s*\}[\s\S]*?let data = null;',
        lambda m: source_replacement,
        html_sanitized
    )

    with open(os.path.join(dist_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_sanitized)
    print(f"[OK] Bundled & Sanitized: dist_audit_site/index.html (Programmatic Canvas Engine configured)")

# Remove any obsolete files from dist_audit_site
obsolete_files = ["chat.html", "alethekanon.png", "policy_ledger.json"]
for obs in obsolete_files:
    obs_path = os.path.join(dist_dir, obs)
    if os.path.exists(obs_path):
        try:
            os.remove(obs_path)
            print(f"[CLEAN] Removed obsolete file: {obs}")
        except Exception:
            pass

print("\n" + "=" * 60)
print(f"EXPORT COMPLETE: ZERO PNGs & ZERO INDIVIDUAL JSONs NEEDED")
print(f"Output Directory: {dist_dir}")
print("Core Files:")
print("  - index.html (Programmatic Canvas Trajectory Graphs & Info Cards)")
print("  - aletheia_canvas_renderer.js (Exact 1:1 Canvas Engine Port)")
print("  - stories_registry.js (Consolidated Multi-Story Audit Database)")
print("  - hegemony_db.js (49-Point Matrix)")
print("=" * 60)
print("Deploy instantly to:")
print("  1. GitHub Pages (push dist_audit_site/ contents to gh-pages branch)")
print("  2. Cloudflare Pages / Netlify / Vercel (set publish directory to 'bluesky_bot/dist_audit_site')")
print("  3. Drag and drop dist_audit_site/ to any static hosting service")
