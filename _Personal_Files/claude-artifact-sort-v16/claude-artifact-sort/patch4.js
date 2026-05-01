const fs = require('fs');

let code = fs.readFileSync('content.js', 'utf8');

function injectAfter(marker, payload) {
    if (code.includes(payload.substring(0, 50))) return; // Already injected
    const idx = code.indexOf(marker);
    if (idx === -1) throw new Error("Marker not found: " + marker);
    code = code.substring(0, idx + marker.length) + '\n' + payload + code.substring(idx + marker.length);
}

function replaceBlock(startMarker, endMarker, payload) {
    const sIdx = code.indexOf(startMarker);
    const eIdx = code.indexOf(endMarker, sIdx);
    if (sIdx === -1 || eIdx === -1) throw new Error("Block markers not found: " + startMarker);
    code = code.substring(0, sIdx) + payload + code.substring(eIdx + endMarker.length);
}

// FEATURE 1 & 4 (Partial): PLATFORM & TAG_CATEGORIES
injectAfter(
    "// ─── Constants ────────────────────────────────────────────────────────────",
    `
  const PLATFORM = window.location.hostname.includes('gemini.google.com') ? 'gemini' : 'claude';
  const TAG_CATEGORIES = {
    'Logic & Math': ['Mathematics','Computation','Algorithms','Programming','Systems'],
    'Physics': ['Mechanics','Quantum','Relativity','Thermodynamics','Fields'],
    'Philosophy': ['Metaphysics','Epistemology','Ethics','Aesthetics','Logic_Phil'],
    'Theology': ['Doctrine','Spirituality','Ritual','Sacred','Divine'],
    'Art & Design': ['Visual','Music','Literature','Performance','Design'],
    'History': ['Ancient','Medieval','Modern','Contemporary','Archaeology'],
    'Science': ['Biology','Chemistry','Astronomy','Geology','Ecology'],
    'Engineering': ['Civil','Mechanical','Electrical','Software','Aerospace'],
    'Medicine': ['Anatomy','Pathology','Genetics','Pharmacology','Surgery'],
    'Psychology': ['Cognitive','Behavioral','Clinical','Developmental','Social'],
    'Sociology': ['Culture','Class','Demographics','Institutions','Norms'],
    'Economics': ['Micro','Macro','Finance','Trade','Labor'],
    'Politics': ['Governance','Law','Policy','International','Theory'],
    'Linguistics': ['Syntax','Semantics','Phonology','Pragmatics','Evolution'],
    'Education': ['Pedagogy','Curriculum','Assessment','Policy_Ed','Technology'],
    'Business': ['Management','Marketing','Strategy','Operations','Entrepreneurship']
  };
  function getTagColor(tag) {
    let hash = 0;
    for (let i = 0; i < tag.length; i++) { hash = tag.charCodeAt(i) + ((hash << 5) - hash); }
    return "hsl(" + (Math.abs(hash) % 360) + ", 65%, 60%)";
  }
`
);

// FEATURE 2: VERSION TRACKING & FEATURE 3: DOWNLOAD TRACKING
injectAfter(
    "function recordFirstSeen(items) {",
    `
  function recordVersionUpdate(items) {
    const knownFilter = items.filter(i => i.data && i.data.name);
    if (knownFilter.length === 0) return;
    
    storageGet('cas_versions').then(versions => {
      let changed = false;
      knownFilter.forEach(item => {
        const { name } = item.data;
        const currentHash = item.data.rawText + '-' + item.origIndex; 
        if (!versions[name]) {
          versions[name] = { version: 1, firstSeen: fmtNow(), lastUpdated: fmtNow(), lastHash: currentHash };
          changed = true;
        } else if (versions[name].lastHash !== currentHash) {
          versions[name].version += 1;
          versions[name].lastUpdated = fmtNow();
          versions[name].lastHash = currentHash;
          changed = true;
        }
      });
      if (changed) chrome.storage.local.set({ cas_versions: versions });
    });
  }

  function interceptDownloadButtons() {
    const btns = document.querySelectorAll('[aria-label*="download"], [data-testid*="download"]');
    btns.forEach(btn => {
      if (btn.dataset.casIntercept) return;
      btn.dataset.casIntercept = "1";
      btn.addEventListener('click', async () => {
        const artifactName = document.querySelector('[class*="font-semibold"], h3, .leading-tight')?.textContent?.trim() || 'unknown';
        const dls = await storageGet('cas_downloads');
        const versions = await storageGet('cas_versions');
        const currentV = versions[artifactName] ? versions[artifactName].version : 1;
        
        if (!dls[artifactName]) dls[artifactName] = { count: 0, lastVersion: 0 };
        dls[artifactName].count += 1;
        dls[artifactName].lastVersion = currentV;
        dls[artifactName].lastAt = fmtNow();
        await new Promise(r => chrome.storage.local.set({ cas_downloads: dls }, r));
        
        const status = document.getElementById('cas-status');
        if (status) status.textContent = \`Downloaded: \${artifactName} (v\${currentV})\`;
      });
    });
  }
`
);

// FEATURE 4: TAG PICKER MODAL UI (Inserted before buildPanel)
injectAfter(
    "function buildPanel() {",
    `
  async function buildTagPickerModal(targetId, type = 'artifact') {
    if (document.getElementById('cas-tag-modal')) return;

    const allTags = await storageGet(type === 'chat' ? 'cas_chat_tags' : 'cas_tags');
    const subtagsData = await storageGet('cas_subtags');
    const existingTags = allTags[targetId] || [];

    const modal = document.createElement('div');
    modal.id = 'cas-tag-modal';
    modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.7);z-index:100000;display:flex;align-items:center;justify-content:center;font-family:ui-sans-serif,system-ui,sans-serif;backdrop-filter:blur(4px);';

    const box = document.createElement('div');
    box.style.cssText = 'background:#1e222a;border:1px solid #333;border-radius:12px;width:95vw;max-width:800px;max-height:90vh;display:flex;flex-direction:column;box-shadow:0 10px 30px rgba(0,0,0,0.5);';

    const header = document.createElement('div');
    header.style.cssText = 'padding:16px 20px;border-bottom:1px solid #333;display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,0.02);border-radius:12px 12px 0 0;';
    header.innerHTML = \`<h3 style="margin:0;color:#f0c040;font-size:16px;letter-spacing:0.05em;">⬡ TAG: <span style="color:#fff;font-weight:400;margin-left:8px">\${targetId}</span></h3>
    <button id="cas-close-tags" style="background:none;border:none;color:#888;cursor:pointer;font-size:24px;line-height:1;padding:0;">×</button>\`;

    const body = document.createElement('div');
    body.style.cssText = 'padding:20px;overflow-y:auto;flex:1;display:flex;flex-direction:column;gap:20px;';

    // Current Selection Area
    const currentArea = document.createElement('div');
    currentArea.style.cssText = 'background:#13161b;padding:16px;border-radius:8px;border:1px dashed #444;';
    const currentTitle = document.createElement('div');
    currentTitle.style.cssText = 'font-size:11px;color:#888;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;';
    currentTitle.textContent = 'Selected Tags';
    
    const tagTray = document.createElement('div');
    tagTray.style.cssText = 'display:flex;flex-wrap:wrap;gap:8px;min-height:28px;';

    const selectedSet = new Set(existingTags);

    function renderTray() {
      tagTray.innerHTML = '';
      if (selectedSet.size === 0) {
        tagTray.innerHTML = '<span style="color:#555;font-size:13px;font-style:italic">No tags selected</span>';
        return;
      }
      for (const t of selectedSet) {
        const chip = document.createElement('div');
        chip.style.cssText = \`display:inline-flex;align-items:center;gap:6px;background:\${getTagColor(t)}30;color:\${getTagColor(t)};border:1px solid \${getTagColor(t)}50;padding:4px 10px;border-radius:16px;font-size:12px;font-weight:500;\`;
        chip.innerHTML = \`\${t} <span style="cursor:pointer;opacity:0.7;" title="Remove">×</span>\`;
        chip.querySelector('span').addEventListener('click', () => { selectedSet.delete(t); renderTray(); renderGrid(); });
        tagTray.appendChild(chip);
      }
    }

    currentArea.appendChild(currentTitle);
    currentArea.appendChild(tagTray);
    body.appendChild(currentArea);

    // Matrix Grid
    const grid = document.createElement('div');
    grid.style.cssText = 'display:grid;grid-template-columns:repeat(auto-fill, minmax(180px, 1fr));gap:12px;';

    function renderGrid() {
      grid.innerHTML = '';
      for (const [cat, tags] of Object.entries(TAG_CATEGORIES)) {
        const col = document.createElement('div');
        col.style.cssText = 'background:#242933;border-radius:8px;padding:12px;border:1px solid #333;';
        
        const catTitle = document.createElement('div');
        catTitle.style.cssText = 'color:#fff;font-size:13px;font-weight:600;margin-bottom:10px;border-bottom:1px solid #3a404d;padding-bottom:6px;';
        catTitle.textContent = cat;
        col.appendChild(catTitle);

        const list = document.createElement('div');
        list.style.cssText = 'display:flex;flex-direction:column;gap:6px;';
        
        tags.forEach(t => {
          const btn = document.createElement('button');
          const isSel = selectedSet.has(t);
          btn.style.cssText = \`text-align:left;background:\${isSel ? getTagColor(t)+'20' : 'transparent'};color:\${isSel ? getTagColor(t) : '#aaa'};border:1px solid \${isSel ? getTagColor(t) : 'transparent'};padding:4px 8px;border-radius:4px;font-size:12px;cursor:pointer;transition:all 0.15s;\`;
          btn.textContent = t;
          btn.onmouseover = () => { if(!isSel) btn.style.background = '#2a303c'; };
          btn.onmouseout = () => { if(!isSel) btn.style.background = 'transparent'; };
          btn.onclick = () => {
            if (isSel) selectedSet.delete(t); else selectedSet.add(t);
            renderTray(); renderGrid();
          };
          list.appendChild(btn);
        });
        col.appendChild(list);
        grid.appendChild(col);
      }
    }

    body.appendChild(grid);

    const footer = document.createElement('div');
    footer.style.cssText = 'padding:16px 20px;border-top:1px solid #333;display:flex;justify-content:flex-end;gap:12px;background:rgba(255,255,255,0.02);border-radius:0 0 12px 12px;';
    footer.innerHTML = \`<button id="cas-btn-cancel" style="background:transparent;border:1px solid #555;color:#ccc;padding:8px 24px;border-radius:6px;cursor:pointer;font-size:13px;">Cancel</button>
    <button id="cas-btn-save" style="background:#f0c040;border:none;color:#000;padding:8px 32px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600;">Save Tags</button>\`;

    renderTray();
    renderGrid();

    box.appendChild(header);
    box.appendChild(body);
    box.appendChild(footer);
    modal.appendChild(box);

    document.body.appendChild(modal);

    const closeTags = () => modal.remove();
    document.getElementById('cas-close-tags').onclick = closeTags;
    document.getElementById('cas-btn-cancel').onclick = closeTags;
    modal.addEventListener('click', e => { if (e.target === modal) closeTags(); });

    document.getElementById('cas-btn-save').onclick = async () => {
      const arr = Array.from(selectedSet);
      const key = type === 'chat' ? 'cas_chat_tags' : 'cas_tags';
      const d = await storageGet(key);
      d[targetId] = arr;
      await new Promise(r => chrome.storage.local.set({ [key]: d }, r));
      closeTags();
      
      const list = document.getElementById('cas-list');
      if (list && type !== 'chat') {
        const status = document.getElementById('cas-status');
        const dataNote = document.getElementById('cas-data-note');
        const dataSummary = document.getElementById('cas-data-summary');
        renderList(scanForFileList(), list, status, dataNote, dataSummary);
      }
    };
  }
` + "\n"
);

// We save our progress to file
fs.writeFileSync('content.temp.js', code, 'utf8');

