
# patch.ps1 — builds upgraded content.js from clean content(2).js base
# Run from the extension directory

$src = Get-Content "content (2).js" -Encoding UTF8

# ─── Blocks to inject ──────────────────────────────────────────────────────

$BLOCK_CONSTANTS = @'

  // ─── Platform & Tag Constants ────────────────────────────────────────────

  const PLATFORM = location.hostname.includes('gemini.google.com') ? 'gemini' : 'claude';

  const TAG_CATEGORIES = {
    Logic:        ['argumentation','deduction','syllogism','fallacy','inference','validity','soundness','axiom','proof','contradiction'],
    Spirituality: ['mysticism','transcendence','enlightenment','soul','prayer','meditation','faith','divine','ritual','gnosis'],
    Religion:     ['theology','doctrine','scripture','church','god','sacred','sin','salvation','prophecy','covenant'],
    Cognition:    ['perception','memory','reasoning','attention','belief','judgement','learning','heuristic','bias','schema'],
    Physics:      ['energy','force','matter','field','entropy','quantum','relativity','wave','particle','spacetime'],
    Metaphysics:  ['ontology','being','reality','causality','substance','essence','modal','possible-worlds','identity','time'],
    Ethics:       ['virtue','duty','consequentialism','justice','rights','harm','autonomy','integrity','responsibility','moral'],
    Knowledge:    ['epistemology','truth','justification','evidence','certainty','belief','scepticism','empiricism','rationalism','testimony'],
    Society:      ['power','institution','class','norms','culture','governance','law','hierarchy','collective','social-contract'],
    Sociology:    ['group','identity','role','status','inequality','mobility','socialisation','deviance','conflict','integration'],
    Conscience:   ['guilt','remorse','integrity','accountability','empathy','moral-sense','shame','character','virtue','will'],
    'The World':  ['nature','ecology','environment','system','complexity','emergence','chaos','evolution','geography','cosmology'],
    Psychology:   ['motivation','emotion','trauma','ego','defence','attachment','development','personality','therapy','behaviour'],
    Communication:['language','rhetoric','narrative','symbol','semiotics','dialogue','persuasion','framing','discourse','media'],
    History:      ['causation','continuity','change','period','event','narrative','interpretation','source','memory','context'],
    Reality:      ['existence','appearance','illusion','simulation','model','representation','perception','truth','construct','phenomenon'],
  };

  const TAG_CATEGORY_COLORS = {
    Logic:'#6b9bcf', Spirituality:'#c96bcf', Religion:'#cf6b88', Cognition:'#6bcfb0',
    Physics:'#cfb06b', Metaphysics:'#9b6bcf', Ethics:'#6bcf6b', Knowledge:'#cfd06b',
    Society:'#6bb0cf', Sociology:'#cf8b6b', Conscience:'#cf6b6b', 'The World':'#6bcf95',
    Psychology:'#cf6bb0', Communication:'#6b9bcf', History:'#b09b6b', Reality:'#e0e0e0',
  };

  function getTagColor(tag) {
    for (const [cat, tags] of Object.entries(TAG_CATEGORIES)) {
      if (tags.includes(tag)) return TAG_CATEGORY_COLORS[cat] || '#888';
    }
    return '#888';
  }

'@

$BLOCK_STORAGE_HELPERS = @'

  function fmtNow() {
    const now = new Date();
    return `${now.getHours().toString().padStart(2,'0')}:${now.getMinutes().toString().padStart(2,'0')} ${now.getDate().toString().padStart(2,'0')}.${(now.getMonth()+1).toString().padStart(2,'0')}`;
  }

  async function recordVersionUpdate(items) {
    const versions = await storageGet('cas_versions');
    let changed = false;
    items.forEach(item => {
      if (!item.data.name) return;
      const name = item.data.name;
      if (!versions[name]) {
        versions[name] = { version: 1, firstSeen: new Date().toISOString(), lastUpdated: new Date().toISOString() };
        changed = true;
      }
      const fingerprint = (item.data.ariaLabel || '') + '|' + (item.data.rawText || '').slice(0, 60);
      const stored = versions[name];
      if (stored._fp && stored._fp !== fingerprint && stored.version < 99) {
        stored.version += 1; stored.lastUpdated = new Date().toISOString(); changed = true;
      }
      stored._fp = fingerprint;
    });
    if (changed) await storageSet('cas_versions', versions);
    return versions;
  }

  function interceptDownloadButtons() {
    document.addEventListener('click', async (e) => {
      const btn = e.target.closest(
        '[aria-label*="Download"],[aria-label*="download"],[data-testid*="download"],[title*="Download"],[title*="download"]'
      );
      if (!btn) return;
      // Find nearest artifact name
      const card = btn.closest('[class*="artifact"]') || btn.closest('[class*="canvas"]');
      const nameEl = card?.querySelector('[class*="title"],[class*="name"],h3,strong') || card;
      const name = nameEl?.textContent?.trim() || btn.getAttribute('aria-label') || 'unknown';
      const dls = await storageGet('cas_downloads');
      const ver = (await storageGet('cas_versions'))[name]?.version || 1;
      const rec = dls[name] || { count: 0, lastVersion: 0, lastAt: null };
      rec.count += 1; rec.lastVersion = ver; rec.lastAt = new Date().toISOString();
      dls[name] = rec;
      await storageSet('cas_downloads', dls);
    }, true);
  }

  // ── Tag Storage ──────────────────────────────────────────────────────────

  async function loadArtifactTags(name) {
    const tags = await storageGet('cas_tags');
    return tags[name] || [];
  }
  async function saveArtifactTags(name, tags) {
    const all = await storageGet('cas_tags');
    all[name] = tags; await storageSet('cas_tags', all);
  }
  async function loadChatTags() {
    const chatId = getChatId();
    const all = await storageGet('cas_chat_tags');
    return all[chatId] || [];
  }
  async function saveChatTags(tags) {
    const chatId = getChatId();
    const all = await storageGet('cas_chat_tags');
    all[chatId] = tags; await storageSet('cas_chat_tags', all);
  }

  // ── Sub-tag Storage (per-category, with global custom tag pool for autocomplete) ──

  async function loadArtifactSubtags(name) {
    const all = await storageGet('cas_subtags');
    return all[name] || {};
  }
  async function saveArtifactSubtags(name, subtagsByCategory) {
    const all = await storageGet('cas_subtags');
    all[name] = subtagsByCategory; await storageSet('cas_subtags', all);
    await mergeCasCustomTags(subtagsByCategory);
  }
  async function loadChatSubtags() {
    const chatId = getChatId();
    const all = await storageGet('cas_chat_subtags');
    return all[chatId] || {};
  }
  async function saveChatSubtags(subtagsByCategory) {
    const chatId = getChatId();
    const all = await storageGet('cas_chat_subtags');
    all[chatId] = subtagsByCategory; await storageSet('cas_chat_subtags', all);
    await mergeCasCustomTags(subtagsByCategory);
  }
  async function mergeCasCustomTags(subtagsByCategory) {
    const custom = await storageGet('cas_custom_tags');
    for (const [cat, tags] of Object.entries(subtagsByCategory)) {
      const presets = new Set(TAG_CATEGORIES[cat] || []);
      const existing = new Set(custom[cat] || []);
      const newOnes = tags.filter(t => !presets.has(t) && !existing.has(t));
      if (newOnes.length > 0) custom[cat] = [...(custom[cat] || []), ...newOnes];
    }
    await storageSet('cas_custom_tags', custom);
  }
  async function getAllSubtagsForCategory(cat) {
    const custom = await storageGet('cas_custom_tags');
    return [...new Set([...(TAG_CATEGORIES[cat] || []), ...(custom[cat] || [])])];
  }

'@

$BLOCK_PANEL_MODE_BUTTONS = @'
          <div style="display:flex;gap:4px;align-items:center;margin-top:5px;">
            <select id="cas-sum-mode" class="cas-mini-select" title="What to generate" style="min-width:82px;">
              <option value="summarise">Summary only</option>
              <option value="tag">Tags only</option>
              <option value="both">Both</option>
            </select>
            <button id="cas-summarise" class="cas-premium-btn" style="flex:1;background:hsl(var(--cas-gold)); color:#0d0f12; border:none; font-weight:600;">↓ SEND</button>
            <button id="cas-inject" class="cas-premium-btn" style="flex:1;">↓ INJECT</button>
            <button id="cas-tag-artifacts" class="cas-premium-btn" title="Manually tag artifacts">🏷 TAG</button>
          </div>
'@

$BLOCK_CHAT_TAG_BUTTON = @'
          <div style="display:flex;gap:5px;align-items:center;margin-top:10px">
            <button id="cas-chat-summarise" class="cas-premium-btn" style="flex:1; background:hsl(var(--cas-gold)); color:#0d0f12; border:none; font-weight:600;">↓ SUMMARISE CHAT</button>
            <button id="cas-chat-inject" class="cas-premium-btn" style="flex:1;">↓ INJECT</button>
            <button id="cas-tag-chat" class="cas-premium-btn" title="Manually tag this chat">🏷 TAG</button>
          </div>
'@

$BLOCK_SUMMARISE_FN = @'
  /**
   * performSummarise — generates AI prompt based on mode
   * mode: 'summarise' | 'tag' | 'both'
   */
  async function performSummarise(statusTarget, mode = 'summarise') {
    const freshItems = scanForFileList();
    const summaries = await storageGet('cas_summaries');
    const artifacts = freshItems.filter(i => {
      if (i.source !== 'generated' || !i.data.name) return false;
      if (mode === 'summarise' && summaries[i.data.name]) return false;
      return true;
    });
    if (artifacts.length === 0) {
      if (statusTarget) statusTarget.textContent = mode === 'summarise' ? 'Everything is summarised.' : 'No artifacts found.';
      return;
    }
    const lenSelect = document.getElementById('cas-sum-length');
    const sentences = lenSelect ? lenSelect.value : '2';
    const lenLabel = sentences === '1' ? '1 sentence' : sentences === '2' ? '2-3 sentences' : '5 sentences';
    const names = artifacts.map(a => a.data.name).join('\n');
    const tagContext = Object.entries(TAG_CATEGORIES)
      .map(([cat, subTags]) => `  ${cat}: ${subTags.slice(0, 6).join(', ')}…`)
      .join('\n');
    let prompt;
    if (mode === 'summarise') {
      prompt = `For each file below write exactly ${lenLabel} describing what it contains.\nReply with a JSON object only — keys are the exact filenames, values are the summary strings. No other text.\n\n${names}`;
    } else if (mode === 'tag') {
      prompt = `For each file below, classify it by assigning 1–4 of these categories. Choose only from this list:\n${Object.keys(TAG_CATEGORIES).join(', ')}\n\nContext (sub-topics within each category):\n${tagContext}\n\nReply with a JSON object only — keys are the exact filenames, values are arrays of matching category names. No other text.\n\n${names}`;
    } else {
      prompt = `For each file below:\n1. Write exactly ${lenLabel} describing what it contains (summary).\n2. Assign 1–4 of these categories. Choose only from this list:\n   ${Object.keys(TAG_CATEGORIES).join(', ')}\n\nContext (sub-topics within each category):\n${tagContext}\n\nReply with a JSON object only — keys are the exact filenames, values are objects with {"summary": "...", "tags": ["Category", ...]}. No other text.\n\n${names}`;
    }
    const filled = fillInput(prompt);
    if (statusTarget) {
      statusTarget.textContent = filled ? `✓ Prompt ready (${mode}) — send in chat, then click ↓ INJECT` : '✗ Input not found';
    }
  }
'@

$BLOCK_INJECTION_FN = @'
  async function performInjection(statusTarget) {
    const freshItems = scanForFileList();
    const artifacts = freshItems.filter(i => i.source === 'generated');
    if (artifacts.length === 0) { if (statusTarget) statusTarget.textContent = 'Scan first (↺).'; return; }

    const pasteField = document.getElementById('cas-paste-json');
    const pasteText = (pasteField && pasteField.value) ? pasteField.value.trim() : '';
    let jsonText = pasteText;

    if (!jsonText) {
      const responses = document.querySelectorAll('[data-is-streaming="false"] .font-claude-response');
      if (responses.length === 0) { if (statusTarget) statusTarget.textContent = 'No response found. Paste JSON or wait.'; return; }
      jsonText = responses[responses.length - 1].textContent.trim();
    }

    const match = jsonText.match(/\{[\s\S]*\}/) || jsonText.match(/\[[\s\S]*\]/);
    if (!match) { if (statusTarget) statusTarget.textContent = 'No JSON found — check format.'; return; }

    try {
      let cleanMatch = match[0].replace(/^```(json)?\s*/i, '').replace(/\s*```$/i, '').trim();
      const parsed = JSON.parse(cleanMatch);
      let count = 0;
      const slugMappedParsed = {};
      if (!Array.isArray(parsed)) { for (const k in parsed) slugMappedParsed[toSlug(k)] = parsed[k]; }

      for (const [idx, artifact] of artifacts.entries()) {
        if (!artifact.isSidebar) continue;
        let rawValue;
        if (Array.isArray(parsed)) {
          rawValue = parsed[idx];
        } else {
          const slug = artifact.data.slug;
          rawValue = slugMappedParsed[slug];
          if (rawValue === undefined) {
            for (const sKey in slugMappedParsed) {
              if (slug && sKey && (slug.includes(sKey) || sKey.includes(slug))) { rawValue = slugMappedParsed[sKey]; break; }
            }
          }
        }
        if (rawValue === undefined || rawValue === null) continue;
        const name = artifact.data.name;
        if (typeof rawValue === 'string') {
          await injectAndStore(artifact.node, name, rawValue); count++;
        } else if (Array.isArray(rawValue)) {
          const valid = Object.keys(TAG_CATEGORIES);
          const filtered = rawValue.filter(t => valid.includes(t));
          if (filtered.length > 0) { await saveArtifactTags(name, filtered); count++; }
        } else if (typeof rawValue === 'object') {
          if (rawValue.summary) await injectAndStore(artifact.node, name, rawValue.summary);
          if (Array.isArray(rawValue.tags)) {
            const filtered = rawValue.tags.filter(t => Object.keys(TAG_CATEGORIES).includes(t));
            if (filtered.length > 0) await saveArtifactTags(name, filtered);
          }
          count++;
        }
      }
      if (statusTarget) statusTarget.textContent = `✓ Injected ${count} item(s) (summaries + tags persisted)`;
      if (pasteField) pasteField.value = '';
      const list = document.getElementById('cas-list');
      const dataNote = document.getElementById('cas-data-note');
      const dataSummary = document.getElementById('cas-data-summary');
      if (list) renderList(freshItems, list, statusTarget, dataNote, dataSummary);
      refreshSummariseBadge();
    } catch (e) {
      console.error('[CAS] Parse Error:', e);
      if (statusTarget) statusTarget.textContent = `Error: ${e.message.slice(0,30)}`;
    }
  }
'@

$BLOCK_TAG_PICKER = @'

  // ─── Tag Picker Modal (two-tier: categories → sub-tags with autocomplete) ─

  function showArtifactSelectDialog(names) {
    return new Promise(resolve => {
      document.getElementById('cas-artifact-select-modal')?.remove();
      const modal = document.createElement('div');
      modal.id = 'cas-artifact-select-modal';
      modal.style.cssText = 'position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);z-index:2000000;background:#13161b;border:1px solid #2a2e36;border-radius:8px;padding:16px;min-width:280px;max-width:400px;font-family:monospace;box-shadow:0 20px 60px rgba(0,0,0,0.9);';
      modal.innerHTML = `<div style="font-size:10px;color:#f0c040;letter-spacing:0.1em;margin-bottom:10px;">SELECT ARTIFACT TO TAG</div><div id="cas-artifact-pick-list" style="display:flex;flex-direction:column;gap:4px;max-height:200px;overflow-y:auto;"></div><button style="margin-top:10px;width:100%;background:none;border:1px solid #444;color:#888;border-radius:4px;padding:5px;cursor:pointer;font-family:monospace;font-size:10px;">Cancel</button>`;
      const list = modal.querySelector('#cas-artifact-pick-list');
      names.forEach(name => {
        const btn = document.createElement('button');
        btn.textContent = name.slice(0,40) + (name.length > 40 ? '…' : '');
        btn.title = name;
        btn.style.cssText = 'background:none;border:1px solid #2a2e36;color:#c8cdd6;border-radius:4px;padding:6px 8px;cursor:pointer;font-family:monospace;font-size:10px;text-align:left;';
        btn.addEventListener('click', () => { modal.remove(); resolve(name); });
        list.appendChild(btn);
      });
      modal.querySelector('button:last-child').addEventListener('click', () => { modal.remove(); resolve(null); });
      document.body.appendChild(modal);
    });
  }

  async function buildTagPickerModal(key, type) {
    document.getElementById('cas-tag-modal')?.remove();

    const [currentTags, currentSubtags] = await Promise.all([
      type === 'chat' ? loadChatTags() : loadArtifactTags(key),
      type === 'chat' ? loadChatSubtags() : loadArtifactSubtags(key),
    ]);

    const modal = document.createElement('div');
    modal.id = 'cas-tag-modal';
    modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;z-index:2000001;display:flex;align-items:center;justify-content:center;background:rgba(0,0,0,0.7);backdrop-filter:blur(4px);';

    const box = document.createElement('div');
    box.style.cssText = 'background:#0d0f12;border:1px solid #2a2e36;border-radius:10px;width:min(560px,92vw);max-height:85vh;display:flex;flex-direction:column;font-family:monospace;box-shadow:0 24px 80px rgba(0,0,0,0.95);overflow:hidden;';

    const selectedTags = new Set(currentTags);
    const selectedSubtags = {};
    for (const [cat, tags] of Object.entries(currentSubtags)) {
      selectedSubtags[cat] = new Set(Array.isArray(tags) ? tags : []);
    }
    const shortKey = type === 'chat' ? `Chat: ${key.slice(0,12)}…` : key.slice(0,42);

    box.innerHTML = `
      <div style="display:flex;align-items:center;justify-content:space-between;padding:12px 16px;background:#13161b;border-bottom:1px solid #2a2e36;flex-shrink:0;">
        <div><div style="font-size:11px;color:#f0c040;letter-spacing:0.1em;">🏷 TAGS</div><div style="font-size:8px;color:#555;margin-top:2px;">${shortKey}</div></div>
        <button id="cas-tag-close" style="background:none;border:none;color:#666;font-size:14px;cursor:pointer;padding:4px 8px;">✕</button>
      </div>
      <div style="padding:7px 12px;font-size:8px;color:#555;letter-spacing:0.06em;border-bottom:1px solid #1e2228;flex-shrink:0;">1: SELECT CATEGORIES · 2: ADD SUB-TAGS WITHIN EACH</div>
      <div id="cas-tag-scroll" style="overflow-y:auto;flex:1;">
        <div id="cas-tag-cat-grid" style="padding:12px 12px 0;display:flex;flex-wrap:wrap;gap:6px;"></div>
        <div id="cas-tag-sub-panel" style="padding:0 12px 12px;margin-top:8px;display:flex;flex-direction:column;gap:10px;"></div>
      </div>
      <div style="padding:10px 16px;display:flex;gap:6px;align-items:center;border-top:1px solid #2a2e36;flex-shrink:0;">
        <span id="cas-tag-count" style="font-size:9px;color:#888;flex:1;"></span>
        <button id="cas-tag-clear" style="background:none;border:1px solid #444;color:#888;border-radius:4px;padding:4px 10px;cursor:pointer;font-family:monospace;font-size:9px;">Clear All</button>
        <button id="cas-tag-save" style="background:#f0c040;border:none;color:#0d0f12;border-radius:4px;padding:6px 14px;cursor:pointer;font-family:monospace;font-size:10px;font-weight:600;">Save</button>
      </div>
    `;

    const catGrid = box.querySelector('#cas-tag-cat-grid');
    const subPanel = box.querySelector('#cas-tag-sub-panel');

    const updateCount = () => {
      const catCount = selectedTags.size;
      const subCount = Object.values(selectedSubtags).reduce((n,s) => n + s.size, 0);
      box.querySelector('#cas-tag-count').textContent =
        `${catCount} ${catCount !== 1 ? 'categories' : 'category'}` +
        (subCount > 0 ? ` · ${subCount} sub-tag${subCount !== 1 ? 's' : ''}` : '');
    };

    const rebuildSubPanel = async () => {
      subPanel.innerHTML = '';
      for (const cat of [...selectedTags]) {
        const color = TAG_CATEGORY_COLORS[cat] || '#888';
        const activeSet = selectedSubtags[cat] || (selectedSubtags[cat] = new Set());
        const section = document.createElement('div');
        section.style.cssText = `border:1px solid ${color}30;border-radius:6px;padding:8px 10px;background:${color}08;`;
        section.innerHTML = `<div style="font-size:9px;color:${color};letter-spacing:0.08em;text-transform:uppercase;margin-bottom:7px;"><span style="font-weight:600;">${cat}</span><span style="opacity:0.4;font-size:7px;margin-left:5px;">sub-tags</span></div>`;
        const chipsRow = document.createElement('div');
        chipsRow.style.cssText = 'display:flex;flex-wrap:wrap;gap:4px;margin-bottom:7px;';
        const renderChips = () => {
          chipsRow.innerHTML = '';
          [...activeSet].forEach(tag => {
            const c = document.createElement('button');
            c.textContent = tag; c.title = 'Click to remove';
            c.style.cssText = `border-radius:3px;padding:2px 6px;cursor:pointer;font-family:monospace;font-size:8px;background:${color}33;border:1px solid ${color};color:${color};`;
            c.addEventListener('click', () => { activeSet.delete(tag); renderChips(); updateCount(); });
            chipsRow.appendChild(c);
          });
          (TAG_CATEGORIES[cat] || []).filter(t => !activeSet.has(t)).forEach(tag => {
            const c = document.createElement('button');
            c.textContent = `+ ${tag}`;
            c.style.cssText = `border-radius:3px;padding:2px 6px;cursor:pointer;font-family:monospace;font-size:8px;background:none;border:1px solid ${color}40;color:${color}55;transition:all 0.1s;`;
            c.addEventListener('mouseenter', () => { c.style.color=color; c.style.borderColor=color; });
            c.addEventListener('mouseleave', () => { c.style.color=`${color}55`; c.style.borderColor=`${color}40`; });
            c.addEventListener('click', () => { activeSet.add(tag); renderChips(); updateCount(); });
            chipsRow.appendChild(c);
          });
        };
        renderChips();
        section.appendChild(chipsRow);
        const inputWrap = document.createElement('div');
        inputWrap.style.cssText = 'position:relative;';
        const inp = document.createElement('input');
        inp.type='text'; inp.placeholder='Type to search or create sub-tag…';
        inp.style.cssText = `width:100%;box-sizing:border-box;background:#0a0c0f;border:1px solid ${color}40;color:#c8cdd6;border-radius:4px;font-family:monospace;font-size:9px;padding:5px 8px;outline:none;`;
        const dd = document.createElement('div');
        dd.style.cssText = 'position:absolute;top:100%;left:0;right:0;background:#13161b;border:1px solid #2a2e36;border-radius:0 0 4px 4px;z-index:10;display:none;max-height:120px;overflow-y:auto;';
        const showDd = (matches, query) => {
          dd.innerHTML=''; dd.style.display='block';
          matches.slice(0,8).forEach(m => {
            const opt=document.createElement('div'); opt.textContent=m;
            opt.style.cssText='padding:4px 8px;cursor:pointer;font-size:9px;color:#c8cdd6;';
            opt.addEventListener('mouseenter',()=>opt.style.background='#1e2228');
            opt.addEventListener('mouseleave',()=>opt.style.background='');
            opt.addEventListener('mousedown',e=>{e.preventDefault();activeSet.add(m);inp.value='';dd.style.display='none';renderChips();updateCount();});
            dd.appendChild(opt);
          });
          const trimmed=query.trim();
          if (trimmed && !matches.includes(trimmed) && !activeSet.has(trimmed)) {
            const cr=document.createElement('div');
            cr.innerHTML=`<span style="color:#f0c040;">＋</span> Create <em>"${trimmed}"</em>`;
            cr.style.cssText='padding:4px 8px;cursor:pointer;font-size:9px;color:#aaa;border-top:1px solid #2a2e36;';
            cr.addEventListener('mouseenter',()=>cr.style.background='#1e2228');
            cr.addEventListener('mouseleave',()=>cr.style.background='');
            cr.addEventListener('mousedown',e=>{e.preventDefault();activeSet.add(trimmed);inp.value='';dd.style.display='none';renderChips();updateCount();});
            dd.appendChild(cr);
          }
          if (!dd.children.length) dd.style.display='none';
        };
        inp.addEventListener('input', async () => {
          const q=inp.value.trim().toLowerCase();
          if (!q){dd.style.display='none';return;}
          const known=await getAllSubtagsForCategory(cat);
          showDd(known.filter(t=>t.toLowerCase().includes(q)&&!activeSet.has(t)), inp.value);
        });
        inp.addEventListener('keydown', e => {
          if (e.key==='Enter'){const t=inp.value.trim();if(!t||activeSet.has(t))return;activeSet.add(t);inp.value='';dd.style.display='none';renderChips();updateCount();}
          if (e.key==='Escape'){dd.style.display='none';inp.value='';}
        });
        inp.addEventListener('blur',()=>setTimeout(()=>{dd.style.display='none';},150));
        inputWrap.appendChild(inp); inputWrap.appendChild(dd);
        section.appendChild(inputWrap);
        subPanel.appendChild(section);
      }
    };

    Object.keys(TAG_CATEGORIES).forEach(cat => {
      const color = TAG_CATEGORY_COLORS[cat] || '#888';
      const hint = (TAG_CATEGORIES[cat] || []).slice(0,3).join(', ');
      const active = selectedTags.has(cat);
      const chip = document.createElement('button');
      chip.dataset.cat = cat;
      chip.style.cssText = [
        'border-radius:6px','padding:7px 10px','cursor:pointer','font-family:monospace',
        'font-size:10px','transition:all 0.15s','text-align:left','width:calc(50% - 3px)',
        'display:flex','flex-direction:column','gap:2px',
        active ? `background:${color}22;border:1.5px solid ${color};color:${color};box-shadow:0 0 8px ${color}30;`
               : 'background:rgba(255,255,255,0.02);border:1px solid #2a2e36;color:#666;'
      ].join(';');
      chip.innerHTML = `<span style="font-weight:600;letter-spacing:0.04em;">${cat}</span><span style="font-size:7px;opacity:0.45;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${hint}…</span>`;
      const setActive = on => {
        if(on){chip.style.background=`${color}22`;chip.style.border=`1.5px solid ${color}`;chip.style.color=color;chip.style.boxShadow=`0 0 8px ${color}30`;}
        else{chip.style.background='rgba(255,255,255,0.02)';chip.style.border='1px solid #2a2e36';chip.style.color='#666';chip.style.boxShadow='none';}
      };
      chip.addEventListener('click', () => {
        if(selectedTags.has(cat)){selectedTags.delete(cat);setActive(false);}
        else{selectedTags.add(cat);setActive(true);}
        updateCount(); rebuildSubPanel();
      });
      catGrid.appendChild(chip);
    });

    updateCount();
    await rebuildSubPanel();

    box.querySelector('#cas-tag-close').addEventListener('click', () => modal.remove());
    modal.addEventListener('click', e => { if(e.target===modal) modal.remove(); });
    box.querySelector('#cas-tag-clear').addEventListener('click', () => {
      selectedTags.clear();
      for(const s of Object.values(selectedSubtags)) s.clear();
      catGrid.querySelectorAll('button[data-cat]').forEach(b=>{b.style.background='rgba(255,255,255,0.02)';b.style.border='1px solid #2a2e36';b.style.color='#666';b.style.boxShadow='none';});
      subPanel.innerHTML=''; updateCount();
    });
    box.querySelector('#cas-tag-save').addEventListener('click', async () => {
      const tags = [...selectedTags];
      const subtags = {};
      for(const [cat,tagSet] of Object.entries(selectedSubtags)){if(tagSet.size>0)subtags[cat]=[...tagSet];}
      if(type==='chat'){await saveChatTags(tags);await saveChatSubtags(subtags);}
      else{await saveArtifactTags(key,tags);await saveArtifactSubtags(key,subtags);}
      modal.remove();
      const list=document.getElementById('cas-list');
      const status=document.getElementById('cas-status');
      const dataNote=document.getElementById('cas-data-note');
      const dataSummary=document.getElementById('cas-data-summary');
      if(list){const items=scanForFileList();renderList(items,list,status,dataNote,dataSummary);}
    });
    modal.appendChild(box);
    document.body.appendChild(modal);
  }
'@

$BLOCK_BIND_TAG_BTNS = @'

    // ── Tag Artifacts button ──────────────────────────────────────────────
    document.getElementById('cas-tag-artifacts')?.addEventListener('click', async () => {
      const items = scanForFileList().filter(i => i.source === 'generated' && i.data.name && i.isSidebar);
      if (items.length === 0) { alert('No sidebar artifacts found. Open the artifact panel first.'); return; }
      const name = items.length === 1 ? items[0].data.name : await showArtifactSelectDialog(items.map(i => i.data.name));
      if (!name) return;
      buildTagPickerModal(name, 'artifact');
    });

    // ── Tag Chat button ───────────────────────────────────────────────────
    document.getElementById('cas-tag-chat')?.addEventListener('click', () => {
      buildTagPickerModal(getChatId(), 'chat');
    });

    // ── Summarise — mode-aware ────────────────────────────────────────────
    document.getElementById('cas-summarise')?.addEventListener('click', () => {
      const mode = document.getElementById('cas-sum-mode')?.value || 'summarise';
      performSummarise(status, mode);
    });
'@

$BLOCK_GCS = @'

  // ─── GCS — Gemini Canvas Sorter ────────────────────────────────────────────

  if (PLATFORM === 'gemini') {

    function findGeminiFilesSidebar() {
      return document.querySelector('[data-panel-id="files"]')
        || document.querySelector('[aria-label*="Files in this conversation"]')
        || document.querySelector('[aria-label*="files"]')
        || document.querySelector('side-panel') || null;
    }

    function scanGeminiCanvases() {
      const sidebar = findGeminiFilesSidebar();
      const results = [];
      const canvasSelectors = ['[data-canvas-id]','[class*="canvas-item"]','[class*="artifact-item"]','[aria-label*="canvas"]','[aria-label*="Canvas"]'];
      let nodes = [];
      if (sidebar) {
        for (const sel of canvasSelectors) {
          const found = sidebar.querySelectorAll(sel);
          if (found.length > 0) { nodes = [...found]; break; }
        }
        if (nodes.length === 0) {
          nodes = [...sidebar.querySelectorAll('li,[role="listitem"],[role="button"]')].filter(n => n.textContent.trim().length > 0 && n.textContent.trim().length < 120);
        }
      }
      const chatCanvases = [...document.querySelectorAll('[data-canvas-id],[class*="canvas-block"],mat-card[class*="canvas"]')];
      const allNodes = [...new Set([...nodes, ...chatCanvases])];
      allNodes.forEach((node, idx) => {
        const nameEl = node.querySelector('[class*="title"],[class*="name"],h3,strong') || node;
        const rawName = nameEl.textContent?.trim() || `Canvas ${idx + 1}`;
        results.push({
          node, isSidebar: sidebar ? sidebar.contains(node) : false,
          source: 'generated', score: 10,
          data: { name: rawName, type: 'CANVAS', id: node.getAttribute('data-canvas-id') || node.id || null,
            ariaLabel: node.getAttribute('aria-label') || rawName, rawText: rawName,
            slug: rawName.toLowerCase().replace(/[^a-z0-9]+/g,'_').replace(/^_+|_+$/g,''), _firstSeen: '' },
          origIndex: idx,
        });
      });
      return results;
    }

    function getGeminiChatTitle() {
      return document.querySelector('[class*="conversation-title"]')?.textContent?.trim()
        || document.querySelector('h1')?.textContent?.trim()
        || document.title.replace(' - Gemini','').trim() || getChatId();
    }

    function injectGeminiToggleButtons() {
      if (document.getElementById('gcs-panel-toggle-group')) return;
      const toolbar = document.querySelector('mat-toolbar') || document.querySelector('[class*="toolbar"]') || document.querySelector('header') || document.querySelector('nav');
      if (!toolbar) return;
      const group = document.createElement('div');
      group.id = 'gcs-panel-toggle-group';
      group.style.cssText = 'display:flex;align-items:center;gap:4px;margin:0 8px;';
      group.innerHTML = `
        <button id="gcs-panel-toggle-main" style="display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:6px;color:#aaa;border:1px solid rgba(255,255,255,0.15);background:rgba(40,44,52,0.6);cursor:pointer;" title="Open Canvas Sorter">⬡</button>
        <button id="gcs-panel-toggle-summary" style="display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;border-radius:6px;color:#aaa;border:1px solid rgba(255,255,255,0.15);background:rgba(40,44,52,0.6);cursor:pointer;" title="GCS Chat Summary">⌬</button>
      `;
      group.querySelector('#gcs-panel-toggle-main').addEventListener('click', () => {
        buildPanel();
        setTimeout(() => { document.getElementById('cas-scan')?.click(); }, 100);
      });
      group.querySelector('#gcs-panel-toggle-summary').addEventListener('click', () => {
        if (!document.getElementById('cas-flyout-panel')) buildFlyout?.();
        const el = document.getElementById('cas-flyout-panel');
        if (el) {
          const isVisible = el.style.display !== 'none';
          el.style.display = isVisible ? 'none' : 'flex';
          group.querySelector('#gcs-panel-toggle-summary').style.color = isVisible ? '#888' : '#f0c040';
          if (!isVisible) renderChatSummaries?.();
        }
      });
      try { toolbar.appendChild(group); } catch(e) {}
    }

    async function registerGeminiChat(items) {
      const chatId = getChatId();
      const indexKey = 'cas_standalone_chat_index';
      const data = await new Promise(r => chrome.storage.local.get(indexKey, d => r(d[indexKey] || {})));
      data[chatId] = { name: getGeminiChatTitle(), projectId: null, projectName: '(Gemini)', artifactCount: items.length, lastSeen: fmtNow() };
      await new Promise(r => chrome.storage.local.set({ [indexKey]: data }, r));
    }

    function scanGeminiForFileList() {
      const items = scanGeminiCanvases();
      recordFirstSeen?.(items);
      recordVersionUpdate(items);
      registerGeminiChat(items);
      return items;
    }

    let gcsCurrentChatId = null;
    function onGeminiChatChange() {
      const newId = getChatId();
      if (newId === gcsCurrentChatId) return;
      gcsCurrentChatId = newId;
      const panelStatus = document.getElementById('cas-status');
      if (panelStatus) panelStatus.textContent = 'Conversation changed — scanning…';
      const items = scanGeminiForFileList();
      if (document.getElementById(PANEL_ID) && items.length > 0) {
        const list = document.getElementById('cas-list');
        const status = document.getElementById('cas-status');
        const dataNote = document.getElementById('cas-data-note');
        const dataSummary = document.getElementById('cas-data-summary');
        if (list) renderList(items, list, status, dataNote, dataSummary);
      }
      renderChatSummaries?.();
    }

    interceptDownloadButtons();

    const gcsHeaderPoll = setInterval(() => {
      injectGeminiToggleButtons();
      const sidebar = findGeminiFilesSidebar();
      if (sidebar && !sidebar.querySelector('#cas-sidebar-bar')) {
        const items = scanGeminiForFileList();
        if (items.length > 0) injectSidebarSortBar?.(items);
      }
    }, 1200);

    ['pushState','replaceState'].forEach(fn => {
      const orig = history[fn].bind(history);
      history[fn] = function(...args) { orig(...args); onGeminiChatChange(); };
    });
    window.addEventListener('popstate', onGeminiChatChange);

    const geminiTitleEl = document.querySelector('title');
    if (geminiTitleEl) {
      new MutationObserver(onGeminiChatChange).observe(geminiTitleEl, { subtree:true, characterData:true, childList:true });
    } else {
      new MutationObserver((_,obs) => {
        const t = document.querySelector('title');
        if(!t) return; obs.disconnect();
        new MutationObserver(onGeminiChatChange).observe(t, { subtree:true, characterData:true, childList:true });
      }).observe(document.head || document.documentElement, { childList:true, subtree:true });
    }

    onGeminiChatChange();
  }
'@

# ─── Build the patched file ────────────────────────────────────────────────

$out = [System.Collections.Generic.List[string]]::new()
$i = 0
$totalLines = $src.Count

while ($i -lt $totalLines) {
    $line = $src[$i]

    # After line 12 (SCAN_INTERVAL const) — inject PLATFORM + TAG constants
    if ($i -eq 12) {
        $out.Add($line)
        $BLOCK_CONSTANTS -split "`n" | ForEach-Object { $out.Add($_) }
        $i++; continue
    }

    # After line 166 (end of storageSet) — inject storage helpers
    if ($i -eq 166) {
        $out.Add($line)
        $BLOCK_STORAGE_HELPERS -split "`n" | ForEach-Object { $out.Add($_) }
        $i++; continue
    }

    # Line 978-981: replace the old 2-button row with mode+3-button row
    if ($i -eq 977) {
        # Skip old lines 978-981 (the div with cas-summarise + cas-inject)
        $out.Add("          " + $BLOCK_PANEL_MODE_BUTTONS.Trim())
        $i += 4  # skip lines 978,979,980,981
        continue
    }

    # Line 1007-1010: replace old 2-button chat row with 3-button + tag
    if ($i -eq 1006) {
        $out.Add("          " + $BLOCK_CHAT_TAG_BUTTON.Trim())
        $i += 3  # skip 1007,1008,1009
        continue
    }

    # Line 1539: replace performSummarise through its closing brace (lines 1539-1561)
    if ($i -eq 1538) {
        $BLOCK_SUMMARISE_FN -split "`n" | ForEach-Object { $out.Add($_) }
        # skip old lines 1539–1561
        $i = 1561
        continue
    }

    # Line 1583: replace performInjection through its closing brace
    # Find the end of performInjection — it ends when we hit the next top-level async function
    # Count from 1583 to the line before "function buildFlyoutPrompt"
    if ($i -eq 1582) {
        $BLOCK_INJECTION_FN -split "`n" | ForEach-Object { $out.Add($_) }
        # skip old lines 1583 to 1680 (end of performInjection)
        # Find next function boundary
        $skip = $i + 1
        while ($skip -lt $totalLines -and $src[$skip] -notmatch '^\s*(async function|function) (?!performInjection)') {
            $skip++
        }
        $i = $skip
        continue
    }

    # After line 1531 (end of injectAndStore) but before performSummarise,
    # we want to inject the tag picker. Do it right before renderList fn (line 1969)
    if ($line -match '^\s*function renderList\b') {
        $BLOCK_TAG_PICKER -split "`n" | ForEach-Object { $out.Add($_) }
        $out.Add($line)
        $i++; continue
    }

    # After bindPanelEvents closing brace — find it by the selector cas-project-open-selected
    # Inject tag button wiring after the existing project open handler
    if ($line -match "cas-project-open-selected.*addEventListener" -or ($src[$i-1] -match "cas-project-select-mode" -and $line -match "renderProjectView")) {
        $out.Add($line)
        $i++; continue
    }

    # Find the closing of bindPanelEvents (the last `  }` before renderCurrentChatSummary or Summary helpers)
    if ($line -match '^\s*\}\s*$' -and $i+1 -lt $totalLines -and $src[$i+1] -match 'renderCurrentChatSummary|Summary helpers|injectSummary') {
        # This is the end of bindPanelEvents — inject tag button wiring before closing
        $BLOCK_BIND_TAG_BTNS -split "`n" | ForEach-Object { $out.Add($_) }
        $out.Add($line)
        $i++; continue
    }

    # Before final `})();` — inject GCS block
    if ($line -match '^\}\)\(\)') {
        $BLOCK_GCS -split "`n" | ForEach-Object { $out.Add($_) }
        $out.Add($line)
        $i++; continue
    }

    $out.Add($line)
    $i++
}

# Write output
[System.IO.File]::WriteAllLines(
    "$PWD\content.js",
    $out.ToArray(),
    [System.Text.UTF8Encoding]::new($false)
)

Write-Host "Patch complete. Lines: $($out.Count)"

# Quick sanity check
$checks = @("PLATFORM","TAG_CATEGORIES","buildTagPickerModal","interceptDownloadButtons","performSummarise","onGeminiChatChange","renderChatSummaries","cas-tag-artifacts","cas-sum-mode")
foreach ($fn in $checks) {
    $count = (Select-String -Path "content.js" -Pattern $fn -SimpleMatch).Count
    Write-Host "  $fn : $count hit(s) $(if($count -eq 0){'⚠ MISSING'})"
}
