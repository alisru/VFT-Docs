// Content script for Gemini web
(() => {
  let lastSentHash = '';
  let debounceTimer = null;
  let statusBadge = null;

  // --- Context Drawer & Prompt Injection System ---
  let drawerEl = null;
  let currentTab = 'related'; // 'related' | 'search' | 'canvases'
  let searchDebounceTimer = null;
  let currentResults = [];
  let currentQuery = '';

  function injectDrawerStyles() {
    if (document.getElementById('chat-context-drawer-styles')) return;
    const style = document.createElement('style');
    style.id = 'chat-context-drawer-styles';
    style.textContent = `
      #chat-context-drawer {
        position: fixed;
        top: 0;
        right: 0;
        width: 440px;
        max-width: 90vw;
        height: 100vh;
        background: #111419;
        border-left: 1px solid #232936;
        box-shadow: -10px 0 30px rgba(0, 0, 0, 0.65);
        z-index: 10000000;
        display: flex;
        flex-direction: column;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #d1d5db;
        transition: transform 0.26s cubic-bezier(0.16, 1, 0.3, 1);
        transform: translateX(100%);
        box-sizing: border-box;
      }
      #chat-context-drawer.open {
        transform: translateX(0);
      }
      #chat-context-drawer * {
        box-sizing: border-box;
      }
      .ctx-drawer-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 16px;
        border-bottom: 1px solid #232936;
        background: #151922;
      }
      .ctx-drawer-title {
        font-size: 14px;
        font-weight: 600;
        color: #f1f5f9;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .ctx-drawer-close {
        background: none;
        border: none;
        color: #94a3b8;
        font-size: 18px;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 4px;
        line-height: 1;
      }
      .ctx-drawer-close:hover {
        color: #fff;
        background: #232936;
      }
      .ctx-search-box {
        padding: 12px 16px;
        border-bottom: 1px solid #1e2430;
        background: #131720;
      }
      .ctx-search-input-wrap {
        position: relative;
        display: flex;
        align-items: center;
      }
      .ctx-search-input {
        width: 100%;
        background: #1b202c;
        border: 1px solid #2f3747;
        border-radius: 8px;
        padding: 8px 32px 8px 12px;
        color: #f1f5f9;
        font-size: 13px;
        outline: none;
        transition: border-color 0.2s;
      }
      .ctx-search-input:focus {
        border-color: #38bdf8;
      }
      .ctx-search-clear {
        position: absolute;
        right: 8px;
        background: none;
        border: none;
        color: #64748b;
        cursor: pointer;
        font-size: 14px;
        padding: 2px 4px;
        display: none;
      }
      .ctx-search-clear:hover {
        color: #e2e8f0;
      }
      .ctx-tabs {
        display: flex;
        gap: 6px;
        padding: 8px 16px;
        background: #131720;
        border-bottom: 1px solid #1e2430;
      }
      .ctx-tab-btn {
        background: #181d27;
        border: 1px solid #283040;
        color: #94a3b8;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      .ctx-tab-btn:hover {
        background: #212836;
        color: #cbd5e1;
      }
      .ctx-tab-btn.active {
        background: #1e3a5f;
        border-color: #38bdf8;
        color: #7dd3fc;
      }
      .ctx-bulk-bar {
        display: flex;
        gap: 8px;
        padding: 8px 16px;
        background: #161b24;
        border-bottom: 1px solid #222938;
      }
      .ctx-btn-primary {
        background: #0284c7;
        color: #fff;
        border: none;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 600;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 4px;
        transition: background 0.15s;
      }
      .ctx-btn-primary:hover {
        background: #0369a1;
      }
      .ctx-btn-secondary {
        background: #1e2533;
        border: 1px solid #333d52;
        color: #cbd5e1;
        padding: 5px 10px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 500;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 4px;
        transition: background 0.15s;
      }
      .ctx-btn-secondary:hover {
        background: #273142;
      }
      .ctx-drawer-content {
        flex: 1;
        overflow-y: auto;
        padding: 12px 16px;
        display: flex;
        flex-direction: column;
        gap: 10px;
      }
      .ctx-drawer-content::-webkit-scrollbar {
        width: 6px;
      }
      .ctx-drawer-content::-webkit-scrollbar-thumb {
        background: #2b3345;
        border-radius: 3px;
      }
      .ctx-card {
        background: #171b24;
        border: 1px solid #232a38;
        border-radius: 8px;
        padding: 10px 12px;
        display: flex;
        flex-direction: column;
        gap: 6px;
        transition: border-color 0.15s, background 0.15s;
      }
      .ctx-card:hover {
        border-color: #3b465c;
        background: #1c212c;
      }
      .ctx-card-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 8px;
      }
      .ctx-card-title {
        font-size: 13px;
        font-weight: 600;
        color: #f1f5f9;
        line-height: 1.3;
        word-break: break-word;
      }
      .ctx-card-badge {
        font-size: 10px;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        white-space: nowrap;
      }
      .ctx-badge-score {
        background: #064e3b;
        color: #6ee7b7;
        border: 1px solid #059669;
      }
      .ctx-badge-canvas {
        background: #3b1d54;
        color: #d8b4fe;
        border: 1px solid #7e22ce;
      }
      .ctx-card-meta {
        font-size: 11px;
        color: #64748b;
        display: flex;
        gap: 8px;
        align-items: center;
      }
      .ctx-card-snippet {
        font-size: 12px;
        color: #94a3b8;
        line-height: 1.4;
        background: #12151d;
        border: 1px solid #1c2230;
        border-radius: 5px;
        padding: 6px 8px;
        white-space: pre-wrap;
        word-break: break-word;
        max-height: 85px;
        overflow: hidden;
        position: relative;
        cursor: pointer;
      }
      .ctx-card-snippet.expanded {
        max-height: none;
      }
      .ctx-card-actions {
        display: flex;
        gap: 6px;
        margin-top: 4px;
      }
      .ctx-card-btn {
        background: #202736;
        border: 1px solid #303b50;
        color: #cbd5e1;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 11px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      .ctx-card-btn:hover {
        background: #2c364c;
        color: #fff;
      }
      .ctx-card-btn.insert {
        background: #103859;
        border-color: #0284c7;
        color: #bae6fd;
      }
      .ctx-card-btn.insert:hover {
        background: #0369a1;
        color: #fff;
      }
      .ctx-empty-state {
        text-align: center;
        padding: 40px 16px;
        color: #64748b;
        font-size: 13px;
      }
      .ctx-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid #38bdf8;
        border-top-color: transparent;
        border-radius: 50%;
        animation: ctx-spin 0.8s linear infinite;
        margin-bottom: 8px;
      }
      @keyframes ctx-spin {
        to { transform: rotate(360deg); }
      }
    `;
    document.head.appendChild(style);
  }

  function insertIntoGeminiPrompt(text, title) {
    const editor = document.querySelector('rich-textarea .ql-editor') ||
                   document.querySelector('div[contenteditable="true"][role="textbox"]') ||
                   document.querySelector('.ql-editor') ||
                   document.querySelector('textarea[aria-label*="prompt" i]') ||
                   document.querySelector('div[contenteditable="true"]');

    const formatted = `\n\n<context>\n${title ? `[Reference: ${title}]\n` : ''}${text.trim()}\n</context>\n\n`;

    if (!editor) {
      navigator.clipboard.writeText(formatted);
      return 'copied';
    }

    editor.focus();

    let success = false;
    try {
      success = document.execCommand('insertText', false, formatted);
    } catch (e) {
      success = false;
    }

    if (!success) {
      if (editor.tagName.toLowerCase() === 'textarea' || editor.tagName.toLowerCase() === 'input') {
        const start = editor.selectionStart || editor.value.length;
        const end = editor.selectionEnd || editor.value.length;
        editor.value = editor.value.substring(0, start) + formatted + editor.value.substring(end);
        editor.dispatchEvent(new Event('input', { bubbles: true }));
        editor.dispatchEvent(new Event('change', { bubbles: true }));
      } else {
        let p = editor.querySelector('p:last-child');
        if (!p) {
          p = document.createElement('p');
          editor.appendChild(p);
        }
        if (p.textContent === editor.getAttribute('data-placeholder')) {
          p.textContent = '';
        }
        p.textContent += formatted;
        editor.dispatchEvent(new Event('input', { bubbles: true }));
        editor.dispatchEvent(new Event('change', { bubbles: true }));
      }
    }

    editor.scrollTop = editor.scrollHeight;
    return 'inserted';
  }

  function copyTextToClipboard(text, btnEl, successLabel = '✓ Copied') {
    navigator.clipboard.writeText(text).then(() => {
      if (btnEl) {
        const orig = btnEl.textContent;
        btnEl.textContent = successLabel;
        setTimeout(() => { if (btnEl) btnEl.textContent = orig; }, 1500);
      }
    });
  }

  function createDrawer() {
    if (drawerEl) return;
    injectDrawerStyles();

    drawerEl = document.createElement('div');
    drawerEl.id = 'chat-context-drawer';

    drawerEl.innerHTML = `
      <div class="ctx-drawer-header">
        <div class="ctx-drawer-title">
          <span>🔍</span>
          <span>Chat Context & Knowledge</span>
          <span style="font-size:10px;font-weight:normal;color:#64748b;background:#1e2430;padding:2px 6px;border-radius:4px;">Alt+C</span>
        </div>
        <button class="ctx-drawer-close" id="ctx-drawer-close-btn" title="Close Drawer (Esc)">✕</button>
      </div>

      <div class="ctx-search-box">
        <div class="ctx-search-input-wrap">
          <input type="text" class="ctx-search-input" id="ctx-search-input" placeholder="Search past chats, concepts, canvases..." autocomplete="off">
          <button class="ctx-search-clear" id="ctx-search-clear-btn" title="Clear">✕</button>
        </div>
      </div>

      <div class="ctx-tabs">
        <button class="ctx-tab-btn active" id="ctx-tab-related" data-tab="related">📌 Related</button>
        <button class="ctx-tab-btn" id="ctx-tab-search" data-tab="search">🔎 Search</button>
        <button class="ctx-tab-btn" id="ctx-tab-canvases" data-tab="canvases">🎨 Canvases</button>
      </div>

      <div class="ctx-bulk-bar" id="ctx-bulk-bar" style="display:none;">
        <button class="ctx-btn-primary" id="ctx-bulk-insert-btn">📥 Insert Context Pack</button>
        <button class="ctx-btn-secondary" id="ctx-bulk-copy-btn">📋 Copy Pack</button>
      </div>

      <div class="ctx-drawer-content" id="ctx-drawer-content">
        <div class="ctx-empty-state">
          <div class="ctx-spinner"></div>
          <div>Loading related chats...</div>
        </div>
      </div>
    `;

    document.body.appendChild(drawerEl);

    // Event listeners
    document.getElementById('ctx-drawer-close-btn').onclick = () => toggleDrawer(false);

    const searchInput = document.getElementById('ctx-search-input');
    const clearBtn = document.getElementById('ctx-search-clear-btn');

    searchInput.oninput = () => {
      const q = searchInput.value.trim();
      clearBtn.style.display = q ? 'block' : 'none';
      if (q) {
        switchTab('search', false);
      }
      clearTimeout(searchDebounceTimer);
      searchDebounceTimer = setTimeout(() => {
        if (q) {
          executeSearch(q);
        } else if (currentTab === 'search') {
          showEmptyState('Type a query to search offline database');
        }
      }, 250);
    };

    clearBtn.onclick = () => {
      searchInput.value = '';
      clearBtn.style.display = 'none';
      if (currentTab === 'search') {
        showEmptyState('Type a query to search offline database');
      }
      searchInput.focus();
    };

    // Tab buttons
    drawerEl.querySelectorAll('.ctx-tab-btn').forEach(btn => {
      btn.onclick = () => switchTab(btn.dataset.tab);
    });

    // Bulk buttons
    document.getElementById('ctx-bulk-insert-btn').onclick = (e) => executeBulkPack('insert', e.currentTarget);
    document.getElementById('ctx-bulk-copy-btn').onclick = (e) => executeBulkPack('copy', e.currentTarget);
  }

  function toggleDrawer(forceOpen) {
    createDrawer();
    const isOpen = drawerEl.classList.contains('open');
    const shouldOpen = forceOpen !== undefined ? forceOpen : !isOpen;

    if (shouldOpen) {
      drawerEl.classList.add('open');
      drawerEl.style.transform = 'translateX(0)';
      const input = document.getElementById('ctx-search-input');
      if (input && currentTab === 'search') input.focus();
      loadActiveTab();
    } else {
      drawerEl.classList.remove('open');
      drawerEl.style.transform = 'translateX(100%)';
    }
  }

  function switchTab(tab, triggerLoad = true) {
    currentTab = tab;
    drawerEl.querySelectorAll('.ctx-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tab);
    });
    if (triggerLoad) {
      loadActiveTab();
    }
  }

  function showLoading(msg = 'Searching...') {
    const content = document.getElementById('ctx-drawer-content');
    if (!content) return;
    content.innerHTML = `
      <div class="ctx-empty-state">
        <div class="ctx-spinner"></div>
        <div>${msg}</div>
      </div>
    `;
    const bulkBar = document.getElementById('ctx-bulk-bar');
    if (bulkBar) bulkBar.style.display = 'none';
  }

  function showEmptyState(msg = 'No results found') {
    const content = document.getElementById('ctx-drawer-content');
    if (!content) return;
    content.innerHTML = `<div class="ctx-empty-state">${msg}</div>`;
    const bulkBar = document.getElementById('ctx-bulk-bar');
    if (bulkBar) bulkBar.style.display = 'none';
  }

  function loadActiveTab() {
    if (currentTab === 'related') {
      loadRelatedChats();
    } else if (currentTab === 'search') {
      const q = document.getElementById('ctx-search-input')?.value.trim();
      if (q) executeSearch(q);
      else showEmptyState('Type a query to search offline database');
    } else if (currentTab === 'canvases') {
      loadCanvases();
    }
  }

  function loadRelatedChats() {
    showLoading('Finding related conversations...');
    let chat = null;
    try { chat = extractChat(); } catch (e) {}

    const textPayload = chat ? (chat.title + ' ' + (chat.messages || []).slice(-3).map(m => m.text).join(' ')).slice(0, 1000) : '';
    const payload = {
      url: window.location.href,
      text: textPayload
    };

    chrome.runtime.sendMessage({ action: 'GET_RELATED', payload }, (response) => {
      if (chrome.runtime.lastError || !response || !response.success) {
        showEmptyState('Unable to load related chats (server offline)');
        return;
      }
      currentResults = response.data || [];
      renderCards(currentResults, 'related');
    });
  }

  function executeSearch(query) {
    currentQuery = query;
    showLoading(`Searching for "${query}"...`);

    chrome.runtime.sendMessage({ action: 'SEARCH_CHATS', query, k: 15 }, (response) => {
      if (chrome.runtime.lastError || !response || !response.success) {
        showEmptyState('Search error (server offline)');
        return;
      }
      currentResults = response.data || [];
      renderCards(currentResults, 'search');
    });
  }

  function loadCanvases() {
    showLoading('Loading saved canvases...');
    chrome.runtime.sendMessage({ action: 'GET_RECENT_CANVASES', k: 30 }, (response) => {
      if (chrome.runtime.lastError || !response || !response.success) {
        showEmptyState('Unable to load canvases (server offline)');
        return;
      }
      currentResults = response.data || [];
      renderCards(currentResults, 'canvases');
    });
  }

  function renderCards(items, type) {
    const content = document.getElementById('ctx-drawer-content');
    const bulkBar = document.getElementById('ctx-bulk-bar');
    if (!content) return;

    if (!items || items.length === 0) {
      showEmptyState(type === 'canvases' ? 'No canvases found yet' : 'No matching results found');
      return;
    }

    if (bulkBar) bulkBar.style.display = (type === 'related' || type === 'search') ? 'flex' : 'none';

    content.innerHTML = '';
    items.forEach((item, idx) => {
      const card = document.createElement('div');
      card.className = 'ctx-card';

      const title = item.title || item.chat_title || 'Untitled';
      const score = item.score !== undefined ? `${Math.round(item.score * 100)}% match` : null;
      const typeBadge = item.type ? `🎨 ${item.type}` : null;

      let snippet = '';
      if (type === 'related') {
        snippet = item.why?.other || item.why?.this || '';
        if (!snippet && item.updated) snippet = `Last active: ${item.updated.slice(0, 10)}`;
      } else if (type === 'search') {
        snippet = item.text || '';
      } else if (type === 'canvases') {
        snippet = item.preview || '';
      }

      card.innerHTML = `
        <div class="ctx-card-header">
          <div class="ctx-card-title">${escapeHtml(title)}</div>
          ${score ? `<span class="ctx-card-badge ctx-badge-score">${score}</span>` : ''}
          ${typeBadge ? `<span class="ctx-card-badge ctx-badge-canvas">${typeBadge}</span>` : ''}
        </div>
        ${item.why?.shared && item.why.shared.length ? `
          <div class="ctx-card-meta">
            <span>🔗 Shared: ${escapeHtml(item.why.shared.join(', '))}</span>
          </div>` : ''}
        ${snippet ? `
          <div class="ctx-card-snippet" title="Click to expand/collapse">${escapeHtml(snippet)}</div>` : ''}
        <div class="ctx-card-actions">
          <button class="ctx-card-btn insert" data-action="insert">📥 Insert into Prompt</button>
          <button class="ctx-card-btn" data-action="copy">📋 Copy</button>
          <button class="ctx-card-btn" data-action="view">↗ View</button>
        </div>
      `;

      // Toggle expand on snippet click
      const snipEl = card.querySelector('.ctx-card-snippet');
      if (snipEl) {
        snipEl.onclick = () => snipEl.classList.toggle('expanded');
      }

      // Action buttons
      const insertBtn = card.querySelector('[data-action="insert"]');
      insertBtn.onclick = () => {
        const textToInsert = snippet || title;
        const res = insertIntoGeminiPrompt(textToInsert, title);
        const orig = insertBtn.textContent;
        insertBtn.textContent = res === 'inserted' ? '✓ Inserted!' : '✓ Copied!';
        setTimeout(() => { if (insertBtn) insertBtn.textContent = orig; }, 1500);
      };

      const copyBtn = card.querySelector('[data-action="copy"]');
      copyBtn.onclick = () => {
        const textToCopy = `[Reference: ${title}]\n${snippet}`;
        copyTextToClipboard(textToCopy, copyBtn);
      };

      const viewBtn = card.querySelector('[data-action="view"]');
      viewBtn.onclick = () => {
        const cid = item.chat_id || item.id;
        window.open(`http://127.0.0.1:8765/?chat=${encodeURIComponent(cid)}`, '_blank');
      };

      content.appendChild(card);
    });
  }

  function executeBulkPack(action, btnEl) {
    if (!currentResults || currentResults.length === 0) return;
    const chatIds = currentResults.map(r => r.chat_id || r.id).filter(Boolean).slice(0, 5);
    const orig = btnEl.textContent;
    btnEl.textContent = '⏳ Packing...';

    const payload = {
      query: currentQuery || undefined,
      chat_ids: chatIds,
      max_chars: 8000
    };

    chrome.runtime.sendMessage({ action: 'GET_PACK', payload }, (response) => {
      btnEl.textContent = orig;
      if (chrome.runtime.lastError || !response || !response.success || !response.text) {
        alert('Failed to generate context pack from server');
        return;
      }
      const packText = response.text;
      if (action === 'insert') {
        const res = insertIntoGeminiPrompt(packText, 'Context Pack');
        btnEl.textContent = res === 'inserted' ? '✓ Inserted Pack!' : '✓ Copied Pack!';
        setTimeout(() => { if (btnEl) btnEl.textContent = orig; }, 1500);
      } else {
        copyTextToClipboard(packText, btnEl, '✓ Copied Pack!');
      }
    });
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function createUI() {
    if (document.getElementById('chat-context-widget')) return;
    injectDrawerStyles();
    createDrawer();

    const widget = document.createElement('div');
    widget.id = 'chat-context-widget';
    widget.title = 'Click to toggle Context Drawer (Alt + C)';
    widget.style.cssText = `
      position: fixed;
      bottom: 18px;
      right: 20px;
      z-index: 999999;
      display: flex;
      align-items: center;
      gap: 8px;
      background: #14161a;
      border: 1px solid #2c313a;
      border-radius: 20px;
      padding: 4px 12px 4px 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
      font-family: system-ui, -apple-system, sans-serif;
      font-size: 12px;
      color: #d8dce3;
      user-select: none;
      cursor: pointer;
      transition: background 0.15s, border-color 0.15s;
    `;
    widget.onclick = () => toggleDrawer();

    const indicator = document.createElement('span');
    indicator.id = 'chat-context-dot';
    indicator.style.cssText = `
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #8a919e;
      display: inline-block;
    `;

    const text = document.createElement('span');
    text.id = 'chat-context-status';
    text.textContent = 'Context';
    text.style.color = '#8a919e';

    const searchIcon = document.createElement('span');
    searchIcon.textContent = '🔍';
    searchIcon.style.cssText = 'font-size: 11px; opacity: 0.8;';

    const syncBtn = document.createElement('button');
    syncBtn.id = 'chat-context-sync-btn';
    syncBtn.textContent = 'Sync Now';
    syncBtn.title = 'Sync current conversation to local database';
    syncBtn.style.cssText = `
      background: #1e2733;
      border: 1px solid #3b4252;
      color: #6aa9ff;
      border-radius: 12px;
      padding: 2px 8px;
      font-size: 11px;
      cursor: pointer;
      font-weight: 500;
    `;
    syncBtn.onclick = (e) => {
      e.stopPropagation();
      performSync(true);
    };

    widget.appendChild(indicator);
    widget.appendChild(text);
    widget.appendChild(searchIcon);
    widget.appendChild(syncBtn);
    document.body.appendChild(widget);
  }

  function setStatus(state, msg) {
    const dot = document.getElementById('chat-context-dot');
    const text = document.getElementById('chat-context-status');
    if (!dot || !text) return;

    if (state === 'syncing') {
      dot.style.background = '#e5c07b';
      text.style.color = '#e5c07b';
      text.textContent = msg || 'Syncing...';
    } else if (state === 'synced') {
      dot.style.background = '#98c379';
      text.style.color = '#98c379';
      text.textContent = msg || 'Synced';
      setTimeout(() => {
        if (text && text.textContent === msg) {
          text.textContent = 'Context';
          text.style.color = '#8a919e';
          dot.style.background = '#8a919e';
        }
      }, 4000);
    } else if (state === 'error') {
      dot.style.background = '#e06c75';
      text.style.color = '#e06c75';
      text.textContent = msg || 'Offline';
    } else {
      dot.style.background = '#8a919e';
      text.style.color = '#8a919e';
      text.textContent = msg || 'Context';
    }
  }

  // --- High-Fidelity LaTeX & Markdown Preservation Engine ---
  function extractTeX(el) {
    if (!el) return null;

    let current = el;
    while (current && current.nodeType === Node.ELEMENT_NODE) {
      const dataMath = current.getAttribute('data-math');
      if (dataMath && dataMath.trim()) return dataMath.trim();

      const dataTex = current.getAttribute('data-tex') || current.getAttribute('data-latex') || current.getAttribute('data-latex-source');
      if (dataTex && dataTex.trim()) return dataTex.trim();

      const title = current.getAttribute('title');
      if (title && title.trim() && (title.includes('\\') || title.includes('_') || title.includes('^'))) {
        return title.trim();
      }
      current = current.parentNode;
    }

    const src = el.querySelector('.math-src');
    if (src && src.textContent.trim()) return src.textContent.trim();

    const annotation = el.querySelector('annotation[encoding="application/x-tex"], annotation');
    if (annotation && annotation.textContent.trim()) return annotation.textContent.trim();

    const math = el.querySelector('math[alttext]');
    if (math && math.getAttribute('alttext')?.trim()) return math.getAttribute('alttext').trim();

    return null;
  }

  function replaceKaTeX(root) {
    if (!root) return;

    // 0. Custom math tags (<math-block>, <math-inline>)
    root.querySelectorAll('math-block, math-inline').forEach(node => {
      if (!node.parentNode) return;
      const tex = extractTeX(node);
      if (!tex) return;
      const isBlock = node.tagName.toLowerCase() === 'math-block' || !!node.querySelector('.katex-display');
      const replacement = document.createTextNode(isBlock ? `\n\n$$\n${tex}\n$$\n\n` : ` $${tex}$ `);
      node.parentNode.replaceChild(replacement, node);
    });

    // 1. Bare display math (.katex-display)
    root.querySelectorAll('.katex-display').forEach(display => {
      if (!display.parentNode) return;
      const tex = extractTeX(display);
      if (tex) {
        display.parentNode.replaceChild(document.createTextNode(`\n\n$$\n${tex}\n$$\n\n`), display);
      }
    });

    // 2. Bare inline math (.katex)
    root.querySelectorAll('.katex').forEach(inline => {
      if (!inline.parentNode) return;
      const tex = extractTeX(inline);
      if (tex) {
        inline.parentNode.replaceChild(document.createTextNode(` $${tex}$ `), inline);
      }
    });
  }

  function renderTableToMarkdown(tableNode) {
    let md = '';
    const rows = Array.from(tableNode.querySelectorAll('tr'));
    if (rows.length === 0) return '';

    rows.forEach((row, rowIndex) => {
      const cells = Array.from(row.querySelectorAll('th, td'));
      let rowStr = '|';
      cells.forEach(cell => {
        rowStr += ` ${cell.textContent.trim().replace(/\|/g, '\\|')} |`;
      });
      md += rowStr + '\n';

      if (rowIndex === 0) {
        let separator = '|';
        cells.forEach(() => {
          separator += ' --- |';
        });
        md += separator + '\n';
      }
    });
    return md;
  }

  function htmlToMarkdown(element) {
    if (!element) return '';
    const clone = element.cloneNode(true);
    replaceKaTeX(clone);

    // Pre-process code block headers
    const codeHeaders = clone.querySelectorAll('.code-block-header');
    codeHeaders.forEach(header => {
      const langSpan = header.querySelector('span');
      const langText = langSpan ? langSpan.textContent.trim() : '';
      const pre = header.nextElementSibling;
      if (pre && pre.tagName === 'PRE') {
        pre.setAttribute('data-language', langText);
      }
      header.remove();
    });

    function processNode(node) {
      if (node.nodeType === Node.TEXT_NODE) {
        return node.nodeValue || '';
      }
      if (node.nodeType !== Node.ELEMENT_NODE) {
        return '';
      }

      let childrenVal = '';
      node.childNodes.forEach(child => {
        childrenVal += processNode(child);
      });

      const tag = node.tagName.toUpperCase();
      switch (tag) {
        case 'H1': return `\n\n# ${childrenVal.trim()}\n\n`;
        case 'H2': return `\n\n## ${childrenVal.trim()}\n\n`;
        case 'H3': return `\n\n### ${childrenVal.trim()}\n\n`;
        case 'H4': return `\n\n#### ${childrenVal.trim()}\n\n`;
        case 'H5': return `\n\n##### ${childrenVal.trim()}\n\n`;
        case 'H6': return `\n\n###### ${childrenVal.trim()}\n\n`;
        case 'P':
          if (node.parentNode && node.parentNode.tagName === 'LI') {
            return childrenVal.trim();
          }
          return `\n\n${childrenVal.trim()}\n\n`;
        case 'STRONG':
        case 'B':
          return `**${childrenVal.trim()}**`;
        case 'EM':
        case 'I':
          return `*${childrenVal.trim()}*`;
        case 'DEL':
        case 'S':
        case 'STRIKE':
          return `~~${childrenVal.trim()}~~`;
        case 'CODE':
          if (node.parentNode && node.parentNode.tagName === 'PRE') {
            return childrenVal;
          }
          return `\`${childrenVal.trim()}\``;
        case 'PRE':
          const lang = node.getAttribute('data-language') || '';
          node.querySelectorAll('button, .copy-code-button').forEach(b => b.remove());
          const codeText = node.textContent.trim();
          return `\n\n\`\`\`${lang}\n${codeText}\n\`\`\`\n\n`;
        case 'BLOCKQUOTE':
          const bqLines = childrenVal.trim().split('\n');
          return '\n\n' + bqLines.map(l => `> ${l}`).join('\n') + '\n\n';
        case 'UL':
        case 'OL':
          return `\n${childrenVal}\n`;
        case 'LI':
          const parentTag = node.parentNode ? node.parentNode.tagName : '';
          if (parentTag === 'OL') {
            const siblings = Array.from(node.parentNode.children);
            const idx = siblings.indexOf(node) + 1;
            return `${idx}. ${childrenVal.trim()}\n`;
          }
          return `- ${childrenVal.trim()}\n`;
        case 'TABLE':
          return `\n\n${renderTableToMarkdown(node)}\n\n`;
        case 'HR':
          return '\n\n---\n\n';
        case 'BR':
          return '\n';
        case 'A':
          const href = node.getAttribute('href') || '';
          return `[${childrenVal.trim()}](${href})`;
        default:
          return childrenVal;
      }
    }

    let md = processNode(clone);
    return md.replace(/\n{3,}/g, '\n\n').trim();
  }

  function getCanvasTitleFromElement(el) {
    if (!el) return '';
    let title = '';
    const titleInput = el.querySelector(
      'input[aria-label*="title" i], input[placeholder*="title" i], ' +
      '[data-test-id="canvas-title"], .canvas-title, .immersive-title, ' +
      '.extended-response-title, h1.title, h2.title, span.title, ' +
      '.title, .title-wrapper .title, .title-container .title, [class*="title"]'
    );
    if (titleInput) {
      if (titleInput.tagName === 'INPUT' || titleInput.tagName === 'TEXTAREA') {
        title = titleInput.value || '';
      } else {
        const clone = titleInput.cloneNode(true);
        clone.querySelectorAll('button, [role="button"], mat-icon, gem-icon').forEach(b => b.remove());
        title = clone.textContent || '';
      }
    }
    if (!title) {
      const heading = el.querySelector('header h1, header h2, header [role="heading"], h1, h2, h3');
      if (heading) {
        const clone = heading.cloneNode(true);
        clone.querySelectorAll('button, [role="button"], mat-icon, gem-icon').forEach(b => b.remove());
        title = clone.textContent || '';
      }
    }
    return title.replace(/\s*(Contents\s*Share\s*&\s*Export\s*Create|Contents|Share\s*&\s*Export|Share|Export|Download|Close|Create)\s*$/i, '').replace(/\s+/g, ' ').trim();
  }

  function extractChatMessageMarkdown(element) {
    if (!element) return '';
    const clone = element.cloneNode(true);
    const canvasSelectors = [
      'immersive-entry-chip', 'immersive-editor', 'immersive-panel'
    ].join(', ');

    const canvasElements = Array.from(clone.querySelectorAll(canvasSelectors));
    const topCanvases = canvasElements.filter(el => {
      let p = el.parentElement;
      while (p && p !== clone) {
        if (p.matches(canvasSelectors)) return false;
        p = p.parentElement;
      }
      return true;
    });

    topCanvases.forEach(el => {
      const title = getCanvasTitleFromElement(el) || 'Canvas';
      const marker = document.createTextNode(`\n\n[[CANVAS: ${title}]]\n\n`);
      el.replaceWith(marker);
    });

    // Remove any remaining stray canvas fragments
    clone.querySelectorAll(canvasSelectors).forEach(el => el.remove());
    return htmlToMarkdown(clone);
  }

  function extractChat() {
    const url = window.location.href;
    if (!url.includes('/app/') && !url.includes('/share/')) return null;

    let title = document.title.replace(/\s*-\s*Gemini.*$/i, '').trim();
    if (!title || title.toLowerCase() === 'gemini') {
      const titleSelectors = [
        '[data-test-id="conversation-title"]',
        '.conversation-title',
        'h1',
        '.selected .conversation-title',
        '[aria-selected="true"] .title',
        '[aria-current="page"]'
      ];
      for (const sel of titleSelectors) {
        const el = document.querySelector(sel);
        if (el && el.textContent.trim()) {
          title = el.textContent.trim();
          break;
        }
      }
    }

    const msgs = [];
    // Primary Gemini selectors: custom tags <user-query> and <model-response>
    const turnElements = document.querySelectorAll(
      'user-query, model-response, .user-query, .model-response, [data-test-id="user-query"], [data-test-id="model-response"]'
    );

    if (turnElements.length > 0) {
      turnElements.forEach((el) => {
        const isUser = el.matches('user-query, .user-query, [data-test-id="user-query"]') ||
                       el.tagName.toLowerCase() === 'user-query';
        const textContainer = el.querySelector('.query-text, .response-content, message-content') || el;
        const text = isUser ? textContainer.innerText.trim() : extractChatMessageMarkdown(textContainer);
        if (text) {
          msgs.push({
            role: isUser ? 'user' : 'assistant',
            text: text
          });
        }
      });
    } else {
      // Fallback: search by content containers
      const queries = document.querySelectorAll('.query-text, [data-test-id="user-query-content"]');
      const responses = document.querySelectorAll('message-content, .response-content, .model-response-text');
      if (queries.length > 0 || responses.length > 0) {
        const all = document.querySelectorAll('.query-text, [data-test-id="user-query-content"], message-content, .response-content, .model-response-text');
        all.forEach((el) => {
          const isUser = el.matches('.query-text, [data-test-id="user-query-content"]');
          const text = isUser ? el.innerText.trim() : extractChatMessageMarkdown(el);
          if (text && text.length > 2) {
            msgs.push({
              role: isUser ? 'user' : 'assistant',
              text: text
            });
          }
        });
      } else {
        // Last-resort fallback: block regions
        const blocks = document.querySelectorAll('[role="region"], .message-content');
        blocks.forEach((el, i) => {
          const isUser = i % 2 === 0;
          const text = isUser ? el.innerText.trim() : extractChatMessageMarkdown(el);
          if (text && text.length > 5) {
            msgs.push({
              role: isUser ? 'user' : 'assistant',
              text: text
            });
          }
        });
      }
    }

    if (msgs.length === 0) return null;

    if (!title || title.toLowerCase() === 'gemini') {
      const firstUser = msgs.find(m => m.role === 'user');
      if (firstUser) {
        title = firstUser.text.slice(0, 60).replace(/\n/g, ' ').trim();
      }
    }

    const canvases = extractCanvases();

    return {
      source: 'gemini',
      title: title || 'Gemini Chat',
      url: url,
      messages: msgs,
      canvases: canvases
    };
  }

  function extractCanvases() {
    const canvases = [];
    try {
      // Target strictly genuine top-level canvas chips and editor panels:
      const canvasContainers = document.querySelectorAll(
        'immersive-entry-chip, immersive-editor, immersive-panel, aside[class*="immersive"]'
      );

      canvasContainers.forEach((panel, idx) => {
        if (panel.id === 'chat-context-widget' || panel.closest?.('#chat-context-widget') || panel.id === 'chat-context-drawer' || panel.closest?.('#chat-context-drawer')) return;

        // Skip nested inner containers if an outer container is already matching
        if (panel.parentElement && panel.parentElement.closest('immersive-entry-chip, immersive-panel, immersive-editor')) {
          return;
        }

        let title = getCanvasTitleFromElement(panel);

        let content = '';
        let type = 'markdown';

        // Monaco editor
        const monacoLines = panel.querySelectorAll('.view-lines .view-line');
        if (monacoLines.length > 0) {
          content = Array.from(monacoLines).map(l => l.innerText).join('\n');
          type = 'code';
        }

        // CodeMirror 6
        if (!content) {
          const cmLines = panel.querySelectorAll('.cm-content .cm-line');
          if (cmLines.length > 0) {
            content = Array.from(cmLines).map(l => l.innerText).join('\n');
            type = 'code';
          } else {
            const cmContent = panel.querySelector('.cm-content');
            if (cmContent) {
              content = cmContent.innerText;
              type = 'code';
            }
          }
        }

        // ProseMirror or contenteditable
        if (!content) {
          const editable = panel.querySelector('#extended-response-markdown-content .ProseMirror')
                        || panel.querySelector('#extended-response-markdown-content')
                        || panel.querySelector('.ProseMirror[aria-label*="Canvas" i]')
                        || panel.querySelector('.ProseMirror, .tiptap, [contenteditable="true"]');
          if (editable) {
            content = htmlToMarkdown(editable);
            type = 'markdown';
            // If title is missing or default, try getting it from the first heading of the document
            if (!title || title.startsWith('Canvas ')) {
              const firstHeading = editable.querySelector('h1, h2');
              if (firstHeading && firstHeading.textContent.trim()) {
                title = firstHeading.textContent.trim();
              }
            }
          }
        }

        // Document container within immersive chip
        if (!content) {
          const docContainer = panel.querySelector('.doc-preview, .document-content, .canvas-content');
          if (docContainer) {
            content = htmlToMarkdown(docContainer);
            type = 'markdown';
          }
        }

        title = title.replace(/\s*(Contents\s*Share\s*&\s*Export\s*Create|Contents|Share\s*&\s*Export|Share|Export|Download|Close|Create)\s*$/i, '').replace(/\s+/g, ' ').trim() || `Canvas ${idx + 1}`;
        content = (content || '').trim();

        // Enforce genuine document threshold (minimum 250 characters; skip ASCII snippets)
        if (content && content.length >= 250) {
          const normTitle = title.toLowerCase();
          const existing = canvases.find(c => c.title.toLowerCase() === normTitle);
          if (!existing) {
            canvases.push({
              id: `canvas-${idx + 1}`,
              title: title,
              type: type,
              content: content,
              updated: new Date().toISOString()
            });
          } else if (content.length > existing.content.length) {
            existing.content = content;
            existing.type = type;
          }
        }
      });

      // Also search for any inline artifact cards in chat that have expandable/embedded content
      const artifactCards = document.querySelectorAll('artifact-card, [data-test-id="artifact-card"]');
      artifactCards.forEach((card, idx) => {
        const cardTitleEl = card.querySelector('.title, [data-test-id="card-title"], h3, h4');
        let cardTitle = cardTitleEl ? cardTitleEl.textContent.trim() : `Artifact ${idx + 1}`;
        cardTitle = cardTitle.replace(/\s*(Export|Download|Close)\s*$/i, '').replace(/\s+/g, ' ').trim();
        const codeBlock = card.querySelector('pre, code, .content');
        if (codeBlock) {
          const cardContent = codeBlock.innerText.trim();
          if (cardContent && cardContent.length > 10) {
            const normTitle = cardTitle.toLowerCase();
            const existing = canvases.find(c => c.title.toLowerCase() === normTitle);
            if (!existing) {
              canvases.push({
                id: `card-${idx + 1}`,
                title: cardTitle,
                type: 'code',
                content: cardContent,
                updated: new Date().toISOString()
              });
            } else if (cardContent.length > existing.content.length) {
              existing.content = cardContent;
              existing.type = 'code';
            }
          }
        }
      });
    } catch (e) {
      console.warn('[Chat Context] Canvas extraction error:', e);
    }

    return canvases;
  }

  function performSync(isManual = false) {
    let chat;
    try {
      chat = extractChat();
    } catch (err) {
      console.error('[Chat Context] extractChat failed:', err);
      if (isManual) setStatus('error', 'Extract error');
      return;
    }

    if (!chat || !chat.messages || chat.messages.length === 0) {
      if (isManual) setStatus('error', 'No chat open');
      return;
    }

    const lastMsg = chat.messages[chat.messages.length - 1];
    const lastMsgSnippet = lastMsg ? (lastMsg.text || '').slice(-40) : '';
    const canvasHash = (chat.canvases || []).map(c => c.title + ':' + c.content.length).join('|');
    const currentHash = chat.url + ':' + chat.messages.length + ':' + lastMsgSnippet + ':' + canvasHash;
    if (!isManual && currentHash === lastSentHash) return;

    setStatus('syncing', 'Syncing...');

    chrome.runtime.sendMessage({ action: 'SYNC_CHAT', payload: chat }, (response) => {
      if (chrome.runtime.lastError || !response || !response.success) {
        const errMsg = response?.error || chrome.runtime.lastError?.message || 'Server offline';
        setStatus('error', 'Server offline');
        console.warn('[Chat Context Sync]', errMsg);
      } else {
        lastSentHash = currentHash;
        const cvCount = chat.canvases && chat.canvases.length ? `, ${chat.canvases.length} 🎨` : '';
        setStatus('synced', `Synced (${chat.messages.length}${cvCount})`);
      }
    });
  }

  // 1. Observe chat DOM updates (children and character text changes)
  const observer = new MutationObserver((mutations) => {
    let hasExternalMutation = false;
    for (let i = 0; i < mutations.length; i++) {
      const target = mutations[i].target;
      if (!target) continue;
      const el = target.nodeType === 1 ? target : target.parentElement;
      if (!el || (el.id !== 'chat-context-widget' && !el.closest?.('#chat-context-widget') && el.id !== 'chat-context-drawer' && !el.closest?.('#chat-context-drawer'))) {
        hasExternalMutation = true;
        break;
      }
    }
    if (!hasExternalMutation) return;

    createUI();
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      performSync(false);
    }, 2000);
  });

  // 2. SPA URL watcher: polls location.href every 1s to trigger sync when switching chats
  let lastUrl = window.location.href;
  setInterval(() => {
    createUI();
    if (window.location.href !== lastUrl) {
      lastUrl = window.location.href;
      lastSentHash = ''; // Reset hash so the new chat syncs immediately
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => performSync(false), 1200);
    }
  }, 1000);

  // 3. Global keyboard shortcut: Alt+C to toggle drawer, Esc to close
  window.addEventListener('keydown', (e) => {
    if (e.altKey && (e.key === 'c' || e.key === 'C')) {
      e.preventDefault();
      toggleDrawer();
    } else if (e.key === 'Escape' && drawerEl && drawerEl.classList.contains('open')) {
      toggleDrawer(false);
    }
  });

  // 4. Lifecycle initialization
  function init() {
    createUI();
    if (document.body) {
      observer.observe(document.body, { childList: true, subtree: true, characterData: true });
      setTimeout(() => performSync(false), 2000);
    }
  }

  if (document.readyState === 'complete' || document.readyState === 'interactive') {
    init();
  } else {
    window.addEventListener('DOMContentLoaded', init, { once: true });
  }
})();
