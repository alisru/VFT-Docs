// Content script for Gemini web
(() => {
  let lastSentHash = '';
  let debounceTimer = null;
  let statusBadge = null;
  let isChatCensored = false;

  // --- Context Drawer & Prompt Injection System ---
  let drawerEl = null;
  let currentTab = 'related'; // 'related' | 'search' | 'canvases' | 'topics'
  let searchDebounceTimer = null;
  let currentResults = [];
  let drawerTopicSort = localStorage.getItem('chat_ctx_drawer_topic_sort') || 'recent';
  let drawerSearchSort = localStorage.getItem('chat_ctx_drawer_search_sort') || 'relevance';
  let drawerSearchMode = localStorage.getItem('chat_ctx_drawer_search_mode') || 'hybrid';
  let drawerSearchGroup = localStorage.getItem('chat_ctx_drawer_search_group') || 'chat';
  let drawerSearchTopicId = null;
  let drawerSearchTopicName = '';
  let drawerSearchMustContain = '';
  let drawerTreeData = null;

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
      .ctx-sort-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 6px 16px;
        background: #141822;
        border-bottom: 1px solid #1e2432;
        font-size: 11px;
      }
      .ctx-sort-btn {
        background: none;
        border: none;
        color: #64748b;
        padding: 2px 7px;
        border-radius: 4px;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.15s;
      }
      .ctx-sort-btn:hover {
        color: #e2e8f0;
        background: #1e2535;
      }
      .ctx-sort-btn.active {
        background: #0284c7;
        color: #fff;
        font-weight: 600;
      }
      .ctx-topic-group {
        border: 1px solid #232a38;
        border-radius: 8px;
        background: #161a23;
        overflow: hidden;
        margin-bottom: 8px;
      }
      .ctx-topic-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 8px 12px;
        background: #191f2b;
        cursor: pointer;
        gap: 6px;
      }
      .ctx-topic-header:hover {
        background: #1f2736;
      }
      .ctx-topic-title {
        font-size: 12px;
        font-weight: 600;
        color: #38bdf8;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        flex: 1;
      }
      .ctx-topic-body {
        display: flex;
        flex-direction: column;
        gap: 4px;
        padding: 6px 8px;
        background: #11141a;
      }
      .ctx-topic-chat-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 4px 6px;
        border-radius: 4px;
        font-size: 12px;
        background: #151820;
        cursor: pointer;
        gap: 6px;
      }
      .ctx-topic-chat-row:hover {
        background: #1e2330;
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
      .ctx-badge-date {
        background: #1e293b;
        color: #94a3b8;
        border: 1px solid #334155;
      }
      .ctx-badge-topic {
        background: #1e1b4b;
        color: #a5b4fc;
        border: 1px solid #3730a3;
        cursor: pointer;
        max-width: 140px;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .ctx-badge-topic:hover {
        background: #312e81;
        color: #c7d2fe;
      }
      .ctx-badge-source {
        background: #1f2937;
        color: #9ca3af;
        border: 1px solid #374151;
        text-transform: uppercase;
        font-size: 9px;
      }
      .ctx-badge-chunks {
        background: #142938;
        color: #7dd3fc;
        border: 1px solid #0284c7;
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
        <div style="display:flex;align-items:center;gap:6px;">
          <a href="http://127.0.0.1:8767" target="_blank" title="Open Full Dashboard & Export Suite" style="color:#94a3b8;font-size:11px;text-decoration:none;padding:3px 8px;border-radius:4px;border:1px solid #283040;transition:all 0.15s;" onmouseover="this.style.color='#38bdf8';this.style.borderColor='#38bdf8'" onmouseout="this.style.color='#94a3b8';this.style.borderColor='#283040'">Dashboard ↗</a>
          <button class="ctx-drawer-close" id="ctx-drawer-close-btn" title="Close Drawer (Esc)">✕</button>
        </div>
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
        <button class="ctx-tab-btn" id="ctx-tab-topics" data-tab="topics">🗂️ Topics</button>
      </div>

      <div class="ctx-sort-bar" id="ctx-topics-sort-bar" style="display:none;">
        <span style="font-size:11px;color:#64748b;">Sort topics:</span>
        <div style="display:flex;gap:4px;">
          <button class="ctx-sort-btn active" data-sort="recent" title="Topics with newest caught chats first">Recent</button>
          <button class="ctx-sort-btn" data-sort="name" title="Alphabetical A-Z">Name</button>
          <button class="ctx-sort-btn" data-sort="count" title="Topics with most chats first">Count</button>
        </div>
      </div>

      <div class="ctx-sort-bar" id="ctx-search-sort-bar" style="display:none;flex-direction:column;gap:6px;padding:8px 16px;background:#141822;border-bottom:1px solid #1e2432;">
        <div style="display:flex;justify-content:space-between;align-items:center;width:100%;">
          <div style="display:flex;align-items:center;gap:4px;">
            <span style="font-size:10px;color:#64748b;">Mode:</span>
            <button class="ctx-sort-btn active" data-search-mode="hybrid" title="Semantic + Keyword Hybrid">⚡ Hybrid</button>
            <button class="ctx-sort-btn" data-search-mode="semantic" title="Pure Dense Vector">🎯 Semantic</button>
            <button class="ctx-sort-btn" data-search-mode="exact" title="Exact Terms FTS5">🔍 Exact</button>
          </div>
          <div style="display:flex;align-items:center;gap:4px;">
            <span style="font-size:10px;color:#64748b;">View:</span>
            <button class="ctx-sort-btn active" data-search-group="chat" title="1 card per conversation">💬 Chat</button>
            <button class="ctx-sort-btn" data-search-group="chunk" title="All chunk passages">📄 Chunks</button>
          </div>
        </div>
        <div style="display:flex;justify-content:space-between;align-items:center;width:100%;">
          <div style="display:flex;align-items:center;gap:4px;">
            <span style="font-size:10px;color:#64748b;">Sort:</span>
            <button class="ctx-sort-btn active" data-search-sort="relevance" title="Highest match score first">🎯 Relevance</button>
            <button class="ctx-sort-btn" data-search-sort="recent" title="Newest caught first">🕒 Recent</button>
          </div>
          <div id="ctx-search-topic-filter-tag" style="display:none;align-items:center;gap:4px;font-size:10px;background:#1e1b4b;color:#a5b4fc;border:1px solid #3730a3;padding:1px 6px;border-radius:4px;cursor:pointer;" title="Click to clear topic filter">
            <span id="ctx-search-topic-filter-name">Topic</span>
            <span>✕</span>
          </div>
        </div>
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

    // Topic sort buttons
    drawerEl.querySelectorAll('#ctx-topics-sort-bar .ctx-sort-btn').forEach(btn => {
      btn.onclick = () => {
        drawerTopicSort = btn.dataset.sort;
        localStorage.setItem('chat_ctx_drawer_topic_sort', drawerTopicSort);
        drawerEl.querySelectorAll('#ctx-topics-sort-bar .ctx-sort-btn').forEach(b => {
          b.classList.toggle('active', b.dataset.sort === drawerTopicSort);
        });
        if (drawerTreeData) {
          renderTopicsTree(drawerTreeData);
        }
      };
    });

    // Search control buttons (Mode, Group, Sort)
    drawerEl.querySelectorAll('#ctx-search-sort-bar .ctx-sort-btn').forEach(btn => {
      btn.onclick = () => {
        if (btn.dataset.searchMode) {
          drawerSearchMode = btn.dataset.searchMode;
          localStorage.setItem('chat_ctx_drawer_search_mode', drawerSearchMode);
        } else if (btn.dataset.searchGroup) {
          drawerSearchGroup = btn.dataset.searchGroup;
          localStorage.setItem('chat_ctx_drawer_search_group', drawerSearchGroup);
        } else if (btn.dataset.searchSort) {
          drawerSearchSort = btn.dataset.searchSort;
          localStorage.setItem('chat_ctx_drawer_search_sort', drawerSearchSort);
        }
        updateSearchControlUI();
        const q = document.getElementById('ctx-search-input')?.value.trim();
        if (q) executeSearch(q);
      };
    });

    // Topic filter tag clear button
    const topicTagEl = document.getElementById('ctx-search-topic-filter-tag');
    if (topicTagEl) {
      topicTagEl.onclick = () => {
        drawerSearchTopicId = null;
        drawerSearchTopicName = '';
        topicTagEl.style.display = 'none';
        const q = document.getElementById('ctx-search-input')?.value.trim();
        if (q) executeSearch(q);
      };
    }

    // Bulk buttons
    document.getElementById('ctx-bulk-insert-btn').onclick = (e) => executeBulkPack('insert', e.currentTarget);
    document.getElementById('ctx-bulk-copy-btn').onclick = (e) => executeBulkPack('copy', e.currentTarget);
  }

  function updateSearchControlUI() {
    const bar = document.getElementById('ctx-search-sort-bar');
    if (!bar) return;
    bar.querySelectorAll('[data-search-mode]').forEach(b => {
      b.classList.toggle('active', b.dataset.searchMode === drawerSearchMode);
    });
    bar.querySelectorAll('[data-search-group]').forEach(b => {
      b.classList.toggle('active', b.dataset.searchGroup === drawerSearchGroup);
    });
    bar.querySelectorAll('[data-search-sort]').forEach(b => {
      b.classList.toggle('active', b.dataset.searchSort === drawerSearchSort);
    });
    const topicTagEl = document.getElementById('ctx-search-topic-filter-tag');
    const topicNameEl = document.getElementById('ctx-search-topic-filter-name');
    if (topicTagEl && topicNameEl) {
      if (drawerSearchTopicId && drawerSearchTopicName) {
        topicTagEl.style.display = 'flex';
        topicNameEl.textContent = `🏷️ ${drawerSearchTopicName.slice(0, 20)}`;
      } else {
        topicTagEl.style.display = 'none';
      }
    }
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
    const topicSortBar = document.getElementById('ctx-topics-sort-bar');
    if (topicSortBar) topicSortBar.style.display = (tab === 'topics') ? 'flex' : 'none';
    const searchSortBar = document.getElementById('ctx-search-sort-bar');
    if (searchSortBar) {
      searchSortBar.style.display = (tab === 'search') ? 'flex' : 'none';
      updateSearchControlUI();
    }
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
    } else if (currentTab === 'topics') {
      loadTopics();
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

    chrome.runtime.sendMessage({
      action: 'SEARCH_CHATS',
      query,
      sort: drawerSearchSort,
      mode: drawerSearchMode,
      group_by: drawerSearchGroup,
      topic_id: drawerSearchTopicId,
      must_contain: drawerSearchMustContain,
      k: 30
    }, (response) => {
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

  function loadTopics() {
    const sortBar = document.getElementById('ctx-topics-sort-bar');
    if (sortBar) {
      sortBar.style.display = 'flex';
      sortBar.querySelectorAll('.ctx-sort-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.sort === drawerTopicSort);
      });
    }
    const bulkBar = document.getElementById('ctx-bulk-bar');
    if (bulkBar) bulkBar.style.display = 'none';

    showLoading('Loading semantic topics...');
    chrome.runtime.sendMessage({ action: 'GET_TOPICS_TREE' }, (response) => {
      if (chrome.runtime.lastError || !response || !response.success) {
        showEmptyState('Unable to load topics (server offline)');
        return;
      }
      drawerTreeData = response.data;
      renderTopicsTree(drawerTreeData);
    });
  }

  function renderTopicsTree(tree) {
    const content = document.getElementById('ctx-drawer-content');
    if (!content) return;
    if (!tree || !tree.topics || tree.topics.length === 0) {
      showEmptyState('No semantic topics clustered yet');
      return;
    }

    content.innerHTML = '';

    let sortedTopics = [...tree.topics];
    if (drawerTopicSort === 'recent') {
      sortedTopics.sort((a, b) => (b.updated || '').localeCompare(a.updated || ''));
    } else if (drawerTopicSort === 'name') {
      sortedTopics.sort((a, b) => (a.name || '').localeCompare(b.name || ''));
    } else if (drawerTopicSort === 'count') {
      sortedTopics.sort((a, b) => (b.count || b.chats.length) - (a.count || a.chats.length));
    }

    const renderGroup = (t, isUnsorted = false) => {
      const group = document.createElement('div');
      group.className = 'ctx-topic-group';

      const header = document.createElement('div');
      header.className = 'ctx-topic-header';

      const titleWrap = document.createElement('div');
      titleWrap.className = 'ctx-topic-title';
      titleWrap.textContent = `${t.name} (${t.chats.length})`;
      titleWrap.title = t.name;

      const metaWrap = document.createElement('div');
      metaWrap.style.cssText = 'display:flex;align-items:center;gap:6px;flex-shrink:0;';

      if (t.updated) {
        const dateEl = document.createElement('span');
        dateEl.style.cssText = 'font-size:10px;color:#64748b;font-weight:normal;';
        dateEl.textContent = t.updated.slice(5, 10);
        dateEl.title = `Last caught: ${t.updated}`;
        metaWrap.appendChild(dateEl);
      }

      if (!isUnsorted) {
        const packBtn = document.createElement('button');
        packBtn.className = 'ctx-card-btn';
        packBtn.style.cssText = 'padding:2px 6px;font-size:10px;';
        packBtn.textContent = '📥 Pack';
        packBtn.title = 'Insert entire topic context pack into prompt';
        packBtn.onclick = (e) => {
          e.stopPropagation();
          executeTopicPack(t.id, packBtn);
        };
        metaWrap.appendChild(packBtn);
      }

      header.appendChild(titleWrap);
      header.appendChild(metaWrap);

      const body = document.createElement('div');
      body.className = 'ctx-topic-body';
      body.style.display = 'none';

      t.chats.forEach(c => {
        const row = document.createElement('div');
        row.className = 'ctx-topic-chat-row';

        const rowTitle = document.createElement('span');
        rowTitle.style.cssText = 'overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1;color:#f1f5f9;';
        rowTitle.textContent = (c.n_canvases > 0 ? '🎨 ' : '') + (c.title || c.id);
        rowTitle.title = c.title || c.id;

        const rowDate = document.createElement('span');
        rowDate.style.cssText = 'font-size:10px;color:#64748b;margin:0 4px;flex-shrink:0;';
        rowDate.textContent = (c.updated || '').slice(5, 10);

        const rowBtn = document.createElement('button');
        rowBtn.className = 'ctx-card-btn insert';
        rowBtn.style.cssText = 'padding:1px 5px;font-size:10px;';
        rowBtn.textContent = 'Insert';
        rowBtn.onclick = (e) => {
          e.stopPropagation();
          insertChatIntoPrompt(c);
          rowBtn.textContent = '✓';
          setTimeout(() => { rowBtn.textContent = 'Insert'; }, 1500);
        };

        row.appendChild(rowTitle);
        row.appendChild(rowDate);
        row.appendChild(rowBtn);
        body.appendChild(row);
      });

      header.onclick = () => {
        const isHidden = body.style.display === 'none';
        body.style.display = isHidden ? 'flex' : 'none';
      };

      group.appendChild(header);
      group.appendChild(body);
      return group;
    };

    const unsortedObj = tree.unsorted && tree.unsorted.length ? {
      id: null,
      name: 'Unsorted',
      chats: tree.unsorted,
      count: tree.unsorted.length,
      updated: tree.unsorted_updated || tree.unsorted[0]?.updated || ''
    } : null;

    if (drawerTopicSort === 'recent' && unsortedObj) {
      let placed = false;
      sortedTopics.forEach(t => {
        if (!placed && (unsortedObj.updated || '') >= (t.updated || '')) {
          content.appendChild(renderGroup(unsortedObj, true));
          placed = true;
        }
        content.appendChild(renderGroup(t));
      });
      if (!placed) {
        content.appendChild(renderGroup(unsortedObj, true));
      }
    } else {
      sortedTopics.forEach(t => content.appendChild(renderGroup(t)));
      if (unsortedObj) {
        content.appendChild(renderGroup(unsortedObj, true));
      }
    }
  }

  function executeTopicPack(topicId, btnEl) {
    const orig = btnEl ? btnEl.textContent : '';
    if (btnEl) btnEl.textContent = '...';
    chrome.runtime.sendMessage({ action: 'GET_PACK', payload: { topic_id: topicId } }, (response) => {
      if (response && response.success && response.text) {
        insertIntoGeminiPrompt(response.text, 'Topic Context');
        if (btnEl) btnEl.textContent = '✓ Inserted';
      } else {
        if (btnEl) btnEl.textContent = 'Error';
      }
      setTimeout(() => { if (btnEl) btnEl.textContent = orig; }, 1500);
    });
  }

  function insertChatIntoPrompt(chat) {
    chrome.runtime.sendMessage({ action: 'GET_PACK', payload: { chat_ids: [chat.id] } }, (response) => {
      if (response && response.success && response.text) {
        insertIntoGeminiPrompt(response.text, chat.title || 'Chat Context');
      }
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
      const dateBadge = item.updated ? `<span class="ctx-card-badge ctx-badge-date" title="Caught: ${escapeHtml(item.updated)}">🕒 ${escapeHtml(item.updated.slice(0, 10))}</span>` : '';
      const sourceBadge = item.source ? `<span class="ctx-card-badge ctx-badge-source">${escapeHtml(item.source)}</span>` : '';
      const topicBadge = item.topic_name ? `<span class="ctx-card-badge ctx-badge-topic" title="Filter by topic: ${escapeHtml(item.topic_name)}" data-topic-id="${item.topic_id}" data-topic-name="${escapeHtml(item.topic_name)}">🏷️ ${escapeHtml(item.topic_name.slice(0, 25))}</span>` : '';
      const chunksBadge = (item.matching_chunks && item.matching_chunks > 1) ? `<span class="ctx-card-badge ctx-badge-chunks">📄 ${item.matching_chunks}</span>` : '';

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
          <div style="display:flex;gap:4px;align-items:center;flex-wrap:wrap;justify-content:flex-end;">
            ${topicBadge}
            ${chunksBadge}
            ${sourceBadge}
            ${dateBadge}
            ${score ? `<span class="ctx-card-badge ctx-badge-score">${score}</span>` : ''}
            ${typeBadge ? `<span class="ctx-card-badge ctx-badge-canvas">${typeBadge}</span>` : ''}
          </div>
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

      // Topic badge click to filter
      const topicEl = card.querySelector('.ctx-badge-topic');
      if (topicEl) {
        topicEl.onclick = (e) => {
          e.stopPropagation();
          drawerSearchTopicId = topicEl.dataset.topicId ? parseInt(topicEl.dataset.topicId) : null;
          drawerSearchTopicName = topicEl.dataset.topicName || '';
          updateSearchControlUI();
          if (currentQuery) executeSearch(currentQuery);
        };
      }

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
        window.open(`http://127.0.0.1:8767/?chat=${encodeURIComponent(cid)}`, '_blank');
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

    const exportBtn = document.createElement('button');
    exportBtn.id = 'chat-context-export-btn';
    exportBtn.textContent = 'Export';
    exportBtn.title = 'Download current chat as Markdown (.md)';
    exportBtn.style.cssText = `
      background: #1e2733;
      border: 1px solid #3b4252;
      color: #94a3b8;
      border-radius: 12px;
      padding: 2px 8px;
      font-size: 11px;
      cursor: pointer;
      font-weight: 500;
      transition: color 0.15s, border-color 0.15s;
    `;
    exportBtn.onmouseenter = () => { exportBtn.style.color = '#38bdf8'; exportBtn.style.borderColor = '#38bdf8'; };
    exportBtn.onmouseleave = () => { exportBtn.style.color = '#94a3b8'; exportBtn.style.borderColor = '#3b4252'; };
    exportBtn.onclick = (e) => {
      e.stopPropagation();
      let chat;
      try { chat = extractChat(); } catch (err) {}
      if (chat && chat.id) {
        window.open(`http://127.0.0.1:8767/api/export/chat/${chat.id}?format=markdown`, '_blank');
      } else {
        window.open('http://127.0.0.1:8767/api/export/all?format=zip', '_blank');
      }
    };

    const censorBtn = document.createElement('button');
    censorBtn.id = 'chat-context-censor-btn';
    censorBtn.textContent = '⛔';
    censorBtn.title = 'Censor conversation: remove all saved copies and prevent future saving';
    censorBtn.style.cssText = `
      background: #1e2733;
      border: 1px solid #3b4252;
      color: #ef4444;
      border-radius: 12px;
      padding: 2px 7px;
      font-size: 11px;
      cursor: pointer;
      font-weight: 500;
      transition: all 0.15s;
    `;
    censorBtn.onmouseenter = () => { censorBtn.style.borderColor = '#ef4444'; censorBtn.style.background = '#2d1a20'; };
    censorBtn.onmouseleave = () => {
      censorBtn.style.borderColor = isChatCensored ? '#ef4444' : '#3b4252';
      censorBtn.style.background = isChatCensored ? '#2d1a20' : '#1e2733';
    };
    censorBtn.onclick = (e) => {
      e.stopPropagation();
      let chat;
      try { chat = extractChat(); } catch (err) {}
      const targetUrl = chat?.url || window.location.href;
      const targetId = chat?.id || '';
      if (!confirm('Censor this chat?\n\nThis will remove all saved messages, chunks, and canvases from local storage, and stop future syncs for this conversation.')) {
        return;
      }
      setStatus('syncing', 'Censoring...');
      chrome.runtime.sendMessage({ action: 'CENSOR_CHAT', payload: { chat_id: targetId, url: targetUrl } }, (resp) => {
        if (resp && resp.success) {
          isChatCensored = true;
          censorBtn.style.background = '#450a0a';
          censorBtn.style.borderColor = '#ef4444';
          censorBtn.title = 'Chat is censored (not saved)';
          syncBtn.disabled = true;
          syncBtn.style.opacity = '0.4';
          syncBtn.title = 'Sync disabled: chat is censored';
          setStatus('error', '⛔ Censored');
        } else {
          alert('Failed to censor chat: ' + (resp?.error || 'Unknown error'));
          setStatus('error', 'Censor failed');
        }
      });
    };

    widget.appendChild(indicator);
    widget.appendChild(text);
    widget.appendChild(searchIcon);
    widget.appendChild(syncBtn);
    widget.appendChild(censorBtn);
    widget.appendChild(exportBtn);
    document.body.appendChild(widget);

    // Check if current chat is already censored
    chrome.runtime.sendMessage({ action: 'CHECK_CENSORED', url: window.location.href }, (resp) => {
      if (resp && resp.censored) {
        isChatCensored = true;
        censorBtn.style.background = '#450a0a';
        censorBtn.style.borderColor = '#ef4444';
        censorBtn.title = 'Chat is censored (not saved)';
        syncBtn.disabled = true;
        syncBtn.style.opacity = '0.4';
        syncBtn.title = 'Sync disabled: chat is censored';
        setStatus('error', '⛔ Censored');
      }
    });
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

  function normalizeGeminiUrl(rawUrl) {
    if (!rawUrl) return '';
    try {
      const u = new URL(rawUrl);
      let cleanPath = u.pathname.replace(/\/+$/, '');
      cleanPath = cleanPath.replace(/^\/u\/\d+(\/.*)?$/, '$1') || cleanPath;
      return `${u.origin}${cleanPath}`;
    } catch (e) {
      return rawUrl.split('?')[0].split('#')[0].replace(/\/+$/, '');
    }
  }

  function extractClaudeChat() {
    const rawUrl = window.location.href;
    const m = rawUrl.match(/\/chat\/([a-zA-Z0-9_-]+)/);
    const convoId = m ? m[1] : '';
    const chatId = convoId ? `claude-${convoId}` : undefined;
    const url = convoId ? `https://claude.ai/chat/${convoId}` : rawUrl.split('?')[0];

    let title = document.title.replace(/\s*-\s*Claude.*$/i, '').trim();
    if (!title || title.toLowerCase() === 'claude') {
      const h1 = document.querySelector('h1, [data-testid="chat-header"]');
      if (h1 && h1.textContent.trim()) {
        title = h1.textContent.trim();
      }
    }

    const msgs = [];
    const rows = document.querySelectorAll('[data-testid="transcript-row"]');
    if (rows.length > 0) {
      rows.forEach(r => {
        const asst = r.querySelector('[data-testid="assistant-message"]') || r.querySelector('.font-claude-message');
        const user = r.querySelector('[data-testid="user-message"]') || r.querySelector('.cds-user-message-body') || r.querySelector('.font-user-message');
        if (asst) {
          let text = asst.innerText.trim();
          text = text.replace(/^Claude\s+responded:\s*/i, '').trim();
          if (text) msgs.push({ role: 'assistant', text });
        } else if (user) {
          let text = user.innerText.trim();
          text = text.replace(/^You\s+said:\s*/i, '').trim();
          text = text.replace(/just now.*$/is, '').trim();
          if (text) msgs.push({ role: 'user', text });
        } else if (r.querySelector('[data-testid="user-message-edit"]')) {
          let text = r.innerText.trim();
          text = text.replace(/^You\s+said:\s*/i, '').trim();
          text = text.replace(/just now.*$/is, '').trim();
          if (text) msgs.push({ role: 'user', text });
        }
      });
    } else {
      // Fallback
      const turns = document.querySelectorAll('[data-testid="assistant-message"], .font-claude-message, [data-testid="user-message"], .cds-user-message-body, .font-user-message');
      turns.forEach(el => {
        const isUser = el.matches('[data-testid="user-message"], .cds-user-message-body, .font-user-message');
        let text = el.innerText.trim();
        if (!isUser) text = text.replace(/^Claude\s+responded:\s*/i, '').trim();
        else text = text.replace(/^You\s+said:\s*/i, '').trim();
        if (text) msgs.push({ role: isUser ? 'user' : 'assistant', text });
      });
    }

    if (msgs.length === 0) return null;

    if (!title || title.toLowerCase() === 'claude') {
      const firstUser = msgs.find(m => m.role === 'user');
      title = (firstUser ? firstUser.text : msgs[0].text).slice(0, 60).replace(/\n/g, ' ').trim();
    }

    return {
      id: chatId,
      source: 'claude',
      title: title || 'Claude Chat',
      url: url,
      messages: msgs,
      canvases: []
    };
  }

  function extractChatGPTChat() {
    const rawUrl = window.location.href;
    const m = rawUrl.match(/\/(?:c|share)\/([a-zA-Z0-9_-]+)/);
    const convoId = m ? m[1] : '';
    const chatId = convoId ? `chatgpt-${convoId}` : undefined;
    const url = convoId ? `https://chatgpt.com/c/${convoId}` : rawUrl.split('?')[0];

    let title = document.title.replace(/\s*-\s*ChatGPT.*$/i, '').trim();
    if (!title || title.toLowerCase() === 'chatgpt') {
      const activeNav = document.querySelector('nav a[class*="bg-token"], h1');
      if (activeNav && activeNav.textContent.trim()) {
        title = activeNav.textContent.trim();
      }
    }

    const msgs = [];
    const units = document.querySelectorAll('[data-chatgpt-search-unit-key]');
    if (units.length > 0) {
      units.forEach(u => {
        const key = u.getAttribute('data-chatgpt-search-unit-key') || '';
        const isUser = key.includes(':user');
        let text = u.innerText.trim();
        if (!isUser) {
          text = text.replace(/^ChatGPT\s+said:\s*/i, '').trim();
        }
        if (text) msgs.push({ role: isUser ? 'user' : 'assistant', text });
      });
    } else {
      // Fallback
      const turns = document.querySelectorAll('[data-message-author-role], article, [data-user-message-bubble="true"]');
      turns.forEach(t => {
        const roleAttr = t.getAttribute('data-message-author-role');
        const isUser = roleAttr === 'user' || t.matches('[data-user-message-bubble="true"]') || (t.className && t.className.includes('user-message'));
        let text = t.innerText.trim();
        if (!isUser) {
          text = text.replace(/^ChatGPT\s+said:\s*/i, '').trim();
        }
        if (text && text.length > 1) {
          msgs.push({ role: isUser ? 'user' : 'assistant', text });
        }
      });
    }

    if (msgs.length === 0) return null;

    if (!title || title.toLowerCase() === 'chatgpt') {
      const firstUser = msgs.find(m => m.role === 'user');
      title = (firstUser ? firstUser.text : msgs[0].text).slice(0, 60).replace(/\n/g, ' ').trim();
    }

    return {
      id: chatId,
      source: 'chatgpt',
      title: title || 'ChatGPT Chat',
      url: url,
      messages: msgs,
      canvases: []
    };
  }

  function extractGeminiChat() {
    const rawUrl = window.location.href;
    if (!rawUrl.includes('/app/') && !rawUrl.includes('/share/') && !rawUrl.includes('/gem/') && !rawUrl.includes('/task') && !rawUrl.includes('/prompt')) return null;
    const url = normalizeGeminiUrl(rawUrl);
    const m = url.match(/\/(?:app|share|task|tasks|prompt|gem\/[^/]+)\/([a-zA-Z0-9_-]+)/);
    const convoId = m ? m[1] : '';
    const chatId = convoId ? `gemini-${convoId}` : undefined;

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
      } else if (msgs[0]) {
        title = msgs[0].text.slice(0, 60).replace(/\n/g, ' ').trim();
      }
    }

    const canvases = extractCanvases();

    return {
      id: chatId,
      source: 'gemini',
      title: title || 'Gemini Chat',
      url: url,
      messages: msgs,
      canvases: canvases
    };
  }

  function extractChat() {
    const host = window.location.hostname;
    if (host.includes('claude.ai')) {
      return extractClaudeChat();
    } else if (host.includes('chatgpt.com') || host.includes('openai.com')) {
      return extractChatGPTChat();
    } else {
      return extractGeminiChat();
    }
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

        content = (content || '').trim();

        // Clean toolbar residue from raw DOM title
        title = title.replace(/\s*(Contents\s*Share\s*&\s*Export\s*Create|Contents|Share\s*&\s*Export|Share|Export|Download|Close|Create)\s*$/i, '').replace(/\s+/g, ' ').trim();

        const isGenericTitle = !title || /^(canvas|artifact|card)\s*\d+$/i.test(title) || /^(untitled|canvas|document)$/i.test(title);

        // Content-first title extraction: Check frontmatter, top # Heading, or HTML title
        let contentTitle = '';
        const fmMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
        if (fmMatch) {
          const tMatch = fmMatch[1].match(/^title:\s*["']?(.*?)["']?$/m);
          if (tMatch && tMatch[1].trim()) {
            contentTitle = tMatch[1].trim();
          }
        }

        if (!contentTitle) {
          const bodyText = fmMatch ? content.slice(fmMatch[0].length) : content;
          const h1Match = bodyText.match(/^#\s+(.+)$/m);
          if (h1Match && h1Match[1].trim()) {
            contentTitle = h1Match[1].trim().replace(/^(?:H1|Title|Document)\s*:\s*/i, '').replace(/[*_`]/g, '').trim();
          }
        }

        if (!contentTitle && type === 'code') {
          const htmlMatch = content.match(/<title>(.*?)<\/title>/i);
          if (htmlMatch && htmlMatch[1].trim()) {
            contentTitle = htmlMatch[1].trim();
          }
        }

        // Prioritize content title if DOM title is generic or if content heading is longer/more descriptive
        if (contentTitle && (isGenericTitle || contentTitle.length > title.length)) {
          title = contentTitle;
        } else if (!title) {
          title = `Canvas ${idx + 1}`;
        }

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
    if (isChatCensored) {
      if (isManual) setStatus('error', '⛔ Censored');
      return;
    }
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

    const payloadWithFlags = { ...chat, is_manual: isManual };
    chrome.runtime.sendMessage({ action: 'SYNC_CHAT', payload: payloadWithFlags }, (response) => {
      if (chrome.runtime.lastError || !response || !response.success) {
        const errMsg = response?.error || chrome.runtime.lastError?.message || 'Server error';
        if (errMsg.includes('context invalidated') || errMsg.includes('Extension context')) {
          setStatus('error', 'Reload tab');
        } else if (errMsg.includes('Failed to fetch') || errMsg.includes('NetworkError')) {
          setStatus('error', 'Server offline');
        } else if (errMsg.includes('500')) {
          setStatus('error', 'Server error (500)');
        } else {
          setStatus('error', 'Sync error');
        }
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
      isChatCensored = false;
      chrome.runtime.sendMessage({ action: 'CHECK_CENSORED', url: window.location.href }, (resp) => {
        isChatCensored = !!resp?.censored;
        const censorBtn = document.getElementById('chat-context-censor-btn');
        const syncBtn = document.getElementById('chat-context-sync-btn');
        if (censorBtn && syncBtn) {
          if (isChatCensored) {
            censorBtn.style.background = '#450a0a';
            censorBtn.style.borderColor = '#ef4444';
            syncBtn.disabled = true;
            syncBtn.style.opacity = '0.4';
            setStatus('error', '⛔ Censored');
          } else {
            censorBtn.style.background = '#1e2733';
            censorBtn.style.borderColor = '#3b4252';
            syncBtn.disabled = false;
            syncBtn.style.opacity = '1';
          }
        }
      });
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
