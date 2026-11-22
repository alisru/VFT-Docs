import os
import re

cp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "control_panel.html")

with open(cp_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Early switchTab in <head>
target1 = "let warnCount = 0;"
replacement1 = """let warnCount = 0;

      // Early Tab Switcher (available immediately during resource loading)
      window.switchTab = function(evt, tabId) {
        const tabcontents = document.getElementsByClassName("tab-content");
        for (let i = 0; i < tabcontents.length; i++) {
          tabcontents[i].classList.remove("active");
        }
        const tablinks = document.getElementsByClassName("tab-button");
        for (let i = 0; i < tablinks.length; i++) {
          tablinks[i].classList.remove("active");
        }
        const target = document.getElementById(tabId);
        if (target) target.classList.add("active");
        if (evt && evt.currentTarget) evt.currentTarget.classList.add("active");
        if (tabId === 'map-tab' && typeof renderMap === 'function') {
          renderMap();
        }
      };"""

if target1 in html and "Early Tab Switcher" not in html:
    html = html.replace(target1, replacement1, 1)
    print("[OK] Patched early switchTab in <head>")
else:
    print("[SKIP/ALREADY] early switchTab")

# 2. Patch fetchSourceText
start_marker = "// ── Source Text Tab"
end_marker = "function renderAuditTab() {"

shard_source_js = """// ── Source Text Tab (16-Shard Partitioned Web Engine) ────────────────────
    window._SOURCE_SHARDS = window._SOURCE_SHARDS || {};

    function getShardKey(storyId) {
      const clean = String(storyId || '').replace(/^factcheck_/, '').trim();
      let hash = 0;
      for (let i = 0; i < clean.length; i++) {
        hash = ((hash << 5) - hash) + clean.charCodeAt(i);
        hash |= 0;
      }
      return (Math.abs(hash) % 16).toString(16);
    }

    async function fetchSourceText() {
      const container = document.getElementById('sourceContent');
      if (!activeStory) {
        container.innerHTML = `<div style="color:var(--text-muted);padding:40px;text-align:center;">No story selected.</div>`;
        return;
      }

      const url = activeStory.link || activeStory.target_url || '';
      const subject = activeStory.subject || activeStory.id || 'Untitled';
      const storyId = activeStory.id || '';
      const cleanSlug = storyId.replace(/^factcheck_/, '');

      container.innerHTML = `
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid var(--panel-border);">
          <div>
            <div style="font-size:1.1rem;font-weight:700;color:var(--text-primary);">${subject}</div>
            ${url ? `<a href="${url}" target="_blank" style="font-size:0.8rem;color:var(--bsky-blue);word-break:break-all;">${url}</a>` : ''}
          </div>
        </div>
        <div id="sourceTextBody" style="color:var(--text-muted);font-size:0.88rem;">
          ⏳ Loading scraped source text...
        </div>`;

      let articleText = null;

      // 1. Check fast 16-shard partition
      const shardKey = getShardKey(cleanSlug);
      try {
        if (!window._SOURCE_SHARDS[shardKey]) {
          const sResp = await fetch(`sources/shard_${shardKey}.json`);
          if (sResp.ok) {
            window._SOURCE_SHARDS[shardKey] = await sResp.json();
          }
        }
        if (window._SOURCE_SHARDS[shardKey]) {
          articleText = window._SOURCE_SHARDS[shardKey][cleanSlug] || window._SOURCE_SHARDS[shardKey][storyId] || null;
        }
      } catch (e) {
        console.warn('Shard fetch error:', e);
      }

      // 2. Fallback to individual static JSON if present
      if (!articleText) {
        const staticCandidates = [
          `sources/${storyId}.json`,
          `sources/factcheck_${cleanSlug}.json`,
          `sources/${cleanSlug}.json`
        ];
        for (const sp of staticCandidates) {
          try {
            const sResp = await fetch(sp);
            if (sResp.ok) {
              const d = await sResp.json();
              if (d && (d.text || d.body)) {
                articleText = d.text || d.body;
                break;
              }
            }
          } catch(e) {}
        }
      }

      // 3. Fallback to local source server if on localhost
      if (!articleText && url && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')) {
        try {
          const resp = await fetch(`http://localhost:8765/source?url=${encodeURIComponent(url)}`);
          if (resp.ok) {
            const lData = await resp.json();
            if (lData && lData.text) articleText = lData.text;
          }
        } catch(e) {}
      }

      // Render text or fallback card
      if (articleText && articleText.trim()) {
        const paragraphs = articleText.split('\\n\\n').filter(p => p.trim());
        const renderedParas = paragraphs.map(p =>
          `<p style="margin:0 0 14px;line-height:1.75;color:var(--text-primary);">${p.replace(/</g,'&lt;').replace(/>/g,'&gt;')}</p>`
        ).join('');

        document.getElementById('sourceTextBody').innerHTML = paragraphs.length
          ? renderedParas
          : `<em style="color:#f87171;">No paragraph text was captured for this article.</em>`;
      } else {
        // Graceful Static Web Fallback for Vercel / Hosted Environments
        document.getElementById('sourceTextBody').innerHTML = `
          <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 16px; margin-bottom: 16px;">
            <div style="font-size: 0.9rem; font-weight: 600; color: var(--text-primary); margin-bottom: 6px;">📰 Primary Source Article</div>
            <div style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 12px;">This investigation was conducted on the ground-truth reporting from:</div>
            ${url ? `<a href="${url}" target="_blank" rel="noopener noreferrer" style="display: inline-flex; align-items: center; gap: 6px; background: var(--bsky-blue); color: #fff; text-decoration: none; padding: 8px 14px; border-radius: 6px; font-size: 0.85rem; font-weight: 600;">
              🌐 Open Original Article ↗
            </a>` : '<em>No URL link recorded.</em>'}
          </div>
          <div style="font-size:0.8rem;color:var(--text-muted);line-height: 1.6;">
            <strong>Aletheia Knowledge Base:</strong> The full text of this article was parsed and evaluated during the 5-phase Gnostic Actualism convergence test.
          </div>`;
      }
    }

    """

s_idx = html.find(start_marker)
e_idx = html.find(end_marker)
if s_idx != -1 and e_idx != -1:
    html = html[:s_idx] + shard_source_js + html[e_idx:]
    print("[OK] Replaced fetchSourceText with 16-shard partition")
else:
    print(f"[FAIL] Could not find markers: {s_idx}, {e_idx}")

with open(cp_path, "w", encoding="utf-8") as f:
    f.write(html)
print("[SUCCESS] control_panel.html patched and saved.")
