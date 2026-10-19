// Auto-Scribe Dashboard Logic
// Supports:
// 1. Built-in Browser Database (chrome.storage.local)
// 2. Direct Disk Folder Sync (File System Access API, zero server)
// 3. On-Demand Export (JSON + Markdown .zip)

(function () {
  // State
  let drafts = [];
  let selectedDraft = null;
  let activeSite = 'all';
  let minLengthFilter = 0;
  let searchQuery = '';
  let sortBy = 'newest';
  let isMonospace = false;
  let diskDirHandle = null;
  let groupBy = 'url';
  let filterStatus = 'all';

  let currentSettings = {
    minChars: 50,
    debounceMs: 1500,
    enabled: true,
    showFloatingWidget: true,
    ignoredDomains: []
  };

  // DOM Elements
  const totalDraftsCount = document.getElementById('total-drafts-count');
  const totalWordsCount = document.getElementById('total-words-count');
  const allSitesCount = document.getElementById('all-sites-count');
  const sitesList = document.getElementById('sites-list');
  const lengthFilters = document.getElementById('length-filters');
  const globalSearch = document.getElementById('global-search');
  const clearSearch = document.getElementById('clear-search');
  const statusSelect = document.getElementById('status-select');
  const groupSelect = document.getElementById('group-select');
  const btnToggleCollapseAll = document.getElementById('btn-toggle-collapse-all');
  const sortSelect = document.getElementById('sort-select');
  const streamActiveSite = document.getElementById('stream-active-site');
  const filteredCountBadge = document.getElementById('filtered-count-badge');
  const draftsStream = document.getElementById('drafts-stream');

  const collapsedGroups = new Set();

  const readerEmpty = document.getElementById('reader-empty');
  const readerContent = document.getElementById('reader-content');
  const readerSiteBadge = document.getElementById('reader-site-badge');
  const readerTitle = document.getElementById('reader-title');
  const readerUrlLink = document.getElementById('reader-url-link');
  const readerStatWords = document.getElementById('reader-stat-words');
  const readerStatChars = document.getElementById('reader-stat-chars');
  const readerStatTime = document.getElementById('reader-stat-time');
  const readerStatUpdated = document.getElementById('reader-stat-updated');
  const readerText = document.getElementById('reader-text');

  const btnCopyDraft = document.getElementById('btn-copy-draft');
  const copyBtnText = document.getElementById('copy-btn-text');
  const btnToggleStatus = document.getElementById('btn-toggle-status');
  const toggleStatusIcon = document.getElementById('toggle-status-icon');
  const toggleStatusText = document.getElementById('toggle-status-text');
  const btnDownloadMd = document.getElementById('btn-download-md');
  const btnToggleFont = document.getElementById('btn-toggle-font');
  const btnDeleteDraft = document.getElementById('btn-delete-draft');
  const btnExportJson = document.getElementById('btn-export-json');
  const btnExportZip = document.getElementById('btn-export-zip');
  const btnCleanDuplicates = document.getElementById('btn-clean-duplicates');

  // Disk Elements
  const diskSyncStatus = document.getElementById('disk-sync-status');
  const diskSyncDot = document.getElementById('disk-sync-dot');
  const diskSyncText = document.getElementById('disk-sync-text');
  const sidebarDiskFolder = document.getElementById('sidebar-disk-folder');
  const btnSidebarPickFolder = document.getElementById('btn-sidebar-pick-folder');
  const btnModalPickFolder = document.getElementById('btn-modal-pick-folder');
  const btnSyncAllDisk = document.getElementById('btn-sync-all-disk');
  const btnDisconnectFolder = document.getElementById('btn-disconnect-folder');
  const modalFolderPath = document.getElementById('modal-folder-path');

  // Settings Elements
  const settingsModal = document.getElementById('settings-modal');
  const btnSettingsToggle = document.getElementById('btn-settings-toggle');
  const btnCloseSettings = document.getElementById('btn-close-settings');
  const btnCancelSettings = document.getElementById('btn-cancel-settings');
  const btnSaveSettings = document.getElementById('btn-save-settings');
  const btnClearAllData = document.getElementById('btn-clear-all-data');

  const settingMinChars = document.getElementById('setting-min-chars');
  const settingDebounceMs = document.getElementById('setting-debounce-ms');
  const settingFloatingWidget = document.getElementById('setting-floating-widget');
  const settingIgnoredDomains = document.getElementById('setting-ignored-domains');

  // -------------------------------------------------------------
  // IndexedDB Helper for Directory Handle Persistence
  // -------------------------------------------------------------
  const DB_NAME = 'AutoScribeFolderDB';
  const STORE_NAME = 'handles';

  function openFolderDB() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(DB_NAME, 1);
      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME);
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }

  async function getStoredDirHandle() {
    try {
      const db = await openFolderDB();
      return new Promise((resolve) => {
        const tx = db.transaction(STORE_NAME, 'readonly');
        const req = tx.objectStore(STORE_NAME).get('diskFolder');
        req.onsuccess = () => resolve(req.result || null);
        req.onerror = () => resolve(null);
      });
    } catch (e) {
      return null;
    }
  }

  async function setStoredDirHandle(handle) {
    try {
      const db = await openFolderDB();
      return new Promise((resolve, reject) => {
        const tx = db.transaction(STORE_NAME, 'readwrite');
        const req = handle
          ? tx.objectStore(STORE_NAME).put(handle, 'diskFolder')
          : tx.objectStore(STORE_NAME).delete('diskFolder');
        req.onsuccess = () => resolve();
        req.onerror = () => reject(req.error);
      });
    } catch (e) {
      console.warn('Failed to store directory handle:', e);
    }
  }

  // -------------------------------------------------------------
  // Direct Disk File System Operations
  // -------------------------------------------------------------
  async function pickDiskFolder() {
    if (!window.showDirectoryPicker) {
      alert('Your browser does not support the File System Access API.');
      return;
    }

    try {
      const handle = await window.showDirectoryPicker({ mode: 'readwrite' });
      diskDirHandle = handle;
      await setStoredDirHandle(handle);
      updateDiskUI(handle.name);
      // Notify background offscreen worker
      chrome.runtime.sendMessage({ action: 'REFRESH_OFFSCREEN_HANDLE' });
      // Auto-sync all existing drafts into the chosen folder
      await syncAllDraftsToDisk();
      alert(`Connected to folder: ${handle.name}\nAll current drafts were synchronized into site subfolders!`);
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('Error selecting folder:', err);
        alert('Could not open folder: ' + err.message);
      }
    }
  }

  async function disconnectDiskFolder() {
    diskDirHandle = null;
    await setStoredDirHandle(null);
    updateDiskUI(null);
    chrome.runtime.sendMessage({ action: 'REFRESH_OFFSCREEN_HANDLE' });
  }

  function updateDiskUI(folderName) {
    if (folderName) {
      diskSyncDot.style.background = '#22c55e';
      diskSyncDot.style.boxShadow = '0 0 6px #22c55e';
      diskSyncText.textContent = `Disk: ${folderName}`;
      sidebarDiskFolder.textContent = folderName;
      sidebarDiskFolder.style.color = '#38bdf8';
      btnSidebarPickFolder.textContent = 'Change Folder...';

      modalFolderPath.textContent = `Current: ${folderName} (Active)`;
      modalFolderPath.style.color = '#4ade80';
      btnSyncAllDisk.style.display = 'inline-flex';
      btnDisconnectFolder.style.display = 'inline-flex';
    } else {
      diskSyncDot.style.background = '#64748b';
      diskSyncDot.style.boxShadow = 'none';
      diskSyncText.textContent = 'Browser Database';
      sidebarDiskFolder.textContent = 'Not selected';
      sidebarDiskFolder.style.color = 'var(--text-dim)';
      btnSidebarPickFolder.textContent = 'Choose Folder...';

      modalFolderPath.textContent = 'Current: None (saving to browser database only)';
      modalFolderPath.style.color = 'var(--text-muted)';
      btnSyncAllDisk.style.display = 'none';
      btnDisconnectFolder.style.display = 'none';
    }
  }

  function formatDraftMarkdown(draft) {
    return `---
id: ${draft.id}
site: ${draft.site}
url: ${draft.url}
title: ${draft.page_title || ''}
context: ${draft.context_title || ''}
char_count: ${draft.char_count}
word_count: ${draft.word_count}
updated_at: ${draft.updated_at}
---

${draft.text}
`;
  }

  async function writeDraftToDisk(draft) {
    if (!diskDirHandle) return;
    try {
      // 1. Verify/request permission
      const perm = await diskDirHandle.queryPermission({ mode: 'readwrite' });
      if (perm !== 'granted') {
        const req = await diskDirHandle.requestPermission({ mode: 'readwrite' });
        if (req !== 'granted') return;
      }

      // 2. Get site subfolder
      const siteFolder = (draft.site || 'web').replace(/[^a-zA-Z0-9_\-\.]/g, '_');
      const siteDir = await diskDirHandle.getDirectoryHandle(siteFolder, { create: true });

      // 3. Clean file name
      const title = draft.context_title || draft.page_title || draft.id;
      const cleanSlug = title.replace(/[\\/*?:"<>|]/g, '').replace(/[\s_]+/g, '-').slice(0, 50).trim() || 'draft';
      const filename = `${cleanSlug}_${draft.id.slice(-6)}.md`;

      // 4. Write file
      const fileHandle = await siteDir.getFileHandle(filename, { create: true });
      const writable = await fileHandle.createWritable();
      await writable.write(formatDraftMarkdown(draft));
      await writable.close();
    } catch (e) {
      console.warn('Failed to write draft to disk folder:', e);
    }
  }

  async function syncAllDraftsToDisk() {
    if (!diskDirHandle || drafts.length === 0) return;
    let count = 0;
    for (const d of drafts) {
      await writeDraftToDisk(d);
      count++;
    }
    return count;
  }

  // -------------------------------------------------------------
  // Data Layer (chrome.storage.local)
  // -------------------------------------------------------------
  function fetchDrafts() {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: 'GET_DRAFTS' }, (res) => {
        if (chrome.runtime.lastError || !res || !res.drafts) {
          resolve([]);
        } else {
          resolve(res.drafts);
        }
      });
    });
  }

  function fetchSettings() {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: 'GET_SETTINGS' }, (res) => {
        if (chrome.runtime.lastError || !res || !res.settings) {
          resolve(currentSettings);
        } else {
          resolve(res.settings);
        }
      });
    });
  }

  function persistSettings(newSettings) {
    currentSettings = { ...currentSettings, ...newSettings };
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: 'SAVE_SETTINGS', settings: currentSettings }, () => resolve());
    });
  }

  function deleteDraftItem(id) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: 'DELETE_DRAFT', id }, () => resolve());
    });
  }

  function setDraftStatus(id, status) {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: 'SET_DRAFT_STATUS', id, status }, () => resolve());
    });
  }

  function clearAllDrafts() {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: 'CLEAR_DRAFTS' }, () => resolve());
    });
  }

  // -------------------------------------------------------------
  // Rendering: Sites Sidebar
  // -------------------------------------------------------------
  function renderSidebar(siteCounts) {
    sitesList.querySelectorAll('.site-nav-btn:not([data-site="all"])').forEach(n => n.remove());

    const sortedSites = Object.keys(siteCounts).sort((a, b) => siteCounts[b] - siteCounts[a]);

    sortedSites.forEach(site => {
      const count = siteCounts[site];
      const btn = document.createElement('button');
      btn.className = `site-nav-btn ${activeSite === site ? 'active' : ''}`;
      btn.dataset.site = site;

      const icon = getSiteIcon(site);
      btn.innerHTML = `
        <span class="site-icon">${icon}</span>
        <span class="site-name">${escapeHtml(site)}</span>
        <span class="site-count">${count}</span>
      `;

      btn.onclick = () => {
        activeSite = site;
        updateActiveNavButtons();
        renderStream();
      };

      sitesList.appendChild(btn);
    });

    allSitesCount.textContent = drafts.length;
  }

  function getSiteIcon(site) {
    const s = (site || '').toLowerCase();
    if (s.includes('reddit')) return '🔴';
    if (s.includes('facebook')) return '🔵';
    if (s.includes('twitter') || s === 'x.com') return '🐦';
    if (s.includes('github')) return '🐙';
    if (s.includes('youtube')) return '▶️';
    if (s.includes('medium') || s.includes('substack')) return '📰';
    if (s.includes('discord')) return '💬';
    return '🌐';
  }

  function updateActiveNavButtons() {
    sitesList.querySelectorAll('.site-nav-btn').forEach(btn => {
      if (btn.dataset.site === activeSite) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    });
    streamActiveSite.textContent = activeSite === 'all' ? 'All Sites' : activeSite;
  }

  // -------------------------------------------------------------
  // Rendering: Drafts Timeline Stream
  // -------------------------------------------------------------
  function getCanonicalUrl(rawUrl) {
    if (!rawUrl) return '';
    try {
      const u = new URL(rawUrl);
      u.hash = '';
      const dropParams = ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'fbclid', 'share_id'];
      dropParams.forEach(p => u.searchParams.delete(p));
      return u.toString();
    } catch (e) {
      return rawUrl.split('#')[0].split('?')[0];
    }
  }

  function createDraftCard(d, isGrouped = false) {
    const card = document.createElement('div');
    card.className = `draft-card ${isGrouped ? 'draft-card-compact' : ''} ${selectedDraft && selectedDraft.id === d.id ? 'active' : ''}`;
    card.dataset.id = d.id;

    const title = d.context_title || d.page_title || 'Untitled Draft';
    const snippet = d.text ? d.text.slice(0, 160) + (d.text.length > 160 ? '...' : '') : '';
    const timeAgo = formatTimeAgo(d.updated_at);
    const siteClass = getSiteClass(d.site);
    const words = d.word_count || d.text.split(/\s+/).filter(Boolean).length;
    const chars = d.char_count || d.text.length;
    const statusText = d.status === 'posted' ? 'Posted' : 'Draft';
    const statusClass = d.status === 'posted' ? 'posted' : 'draft';

    if (isGrouped) {
      card.innerHTML = `
        <div class="card-top">
          <div style="display:flex;align-items:center;gap:6px;min-width:0;">
            <span class="card-status-badge ${statusClass}">${statusText}</span>
            <span class="card-counts" title="${words} words, ${chars.toLocaleString()} characters">(${words}w : ${chars.toLocaleString()}c)</span>
          </div>
          <div style="display:flex;align-items:center;gap:6px;flex-shrink:0;">
            <span class="card-time">${timeAgo}</span>
            <div class="card-quick-actions">
              <button class="card-btn btn-card-status" title="${d.status === 'posted' ? 'Mark as Draft' : 'Mark as Posted'}">${d.status === 'posted' ? '↩' : '✓'}</button>
              <button class="card-btn btn-card-copy" title="Copy to clipboard">📋</button>
              <button class="card-btn btn-card-del" title="Delete draft">🗑️</button>
            </div>
          </div>
        </div>
        <div class="card-snippet">${escapeHtml(snippet)}</div>
      `;
    } else {
      card.innerHTML = `
        <div class="card-top">
          <div style="display:flex;align-items:center;gap:6px;">
            <span class="card-site-tag ${siteClass}">${escapeHtml(d.site || 'web')}</span>
            <span class="card-status-badge ${statusClass}">${statusText}</span>
          </div>
          <span class="card-time">${timeAgo}</span>
        </div>
        <div class="card-title" title="${escapeHtml(title)}">${escapeHtml(title)}</div>
        <div class="card-snippet">${escapeHtml(snippet)}</div>
        <div class="card-footer">
          <span class="card-counts">${words} words · ${chars.toLocaleString()} chars</span>
          <div class="card-quick-actions">
            <button class="card-btn btn-card-status" title="${d.status === 'posted' ? 'Mark as Draft' : 'Mark as Posted'}">${d.status === 'posted' ? '↩' : '✓'}</button>
            <button class="card-btn btn-card-copy" title="Copy to clipboard">📋</button>
            <button class="card-btn btn-card-del" title="Delete draft">🗑️</button>
          </div>
        </div>
      `;
    }

    card.onclick = (e) => {
      if (e.target.closest('.card-quick-actions')) return;
      selectDraft(d);
    };

    card.querySelector('.btn-card-status').onclick = async (e) => {
      e.stopPropagation();
      const newStatus = d.status === 'posted' ? 'draft' : 'posted';
      d.status = newStatus;
      await setDraftStatus(d.id, newStatus);
      if (selectedDraft && selectedDraft.id === d.id) {
        selectedDraft.status = newStatus;
        renderReader();
      }
      renderStream();
    };

    card.querySelector('.btn-card-copy').onclick = (e) => {
      e.stopPropagation();
      navigator.clipboard.writeText(d.text).then(() => {
        const btn = card.querySelector('.btn-card-copy');
        btn.textContent = '✓';
        setTimeout(() => { btn.textContent = '📋'; }, 1200);
      });
    };

    card.querySelector('.btn-card-del').onclick = async (e) => {
      e.stopPropagation();
      if (confirm(`Delete this draft from ${d.site}?`)) {
        await deleteDraftItem(d.id);
        drafts = drafts.filter(item => item.id !== d.id);
        if (selectedDraft && selectedDraft.id === d.id) {
          selectedDraft = null;
          renderReader();
        }
        refreshDashboard();
      }
    };

    return card;
  }

  function updateCollapseAllBtn() {
    if (!btnToggleCollapseAll) return;
    if (groupBy === 'flat') {
      btnToggleCollapseAll.style.display = 'none';
      return;
    }
    btnToggleCollapseAll.style.display = 'inline-flex';
    const groups = draftsStream.querySelectorAll('.url-group');
    if (groups.length === 0) {
      btnToggleCollapseAll.style.display = 'none';
      return;
    }
    const anyExpanded = Array.from(groups).some(g => !g.classList.contains('collapsed'));
    btnToggleCollapseAll.textContent = anyExpanded ? 'Collapse All' : 'Expand All';
  }

  function renderStream() {
    draftsStream.innerHTML = '';

    let filtered = drafts.filter(d => {
      if (filterStatus === 'draft' && d.status === 'posted') return false;
      if (filterStatus === 'posted' && d.status !== 'posted') return false;
      if (activeSite !== 'all' && d.site !== activeSite) return false;
      if (minLengthFilter > 0 && (d.char_count || 0) < minLengthFilter) return false;
      if (searchQuery) {
        const q = searchQuery.toLowerCase();
        const textMatch = (d.text || '').toLowerCase().includes(q);
        const titleMatch = (d.context_title || d.page_title || '').toLowerCase().includes(q);
        const siteMatch = (d.site || '').toLowerCase().includes(q);
        if (!textMatch && !titleMatch && !siteMatch) return false;
      }
      return true;
    });

    filtered.sort((a, b) => {
      if (sortBy === 'newest') return new Date(b.updated_at || 0) - new Date(a.updated_at || 0);
      if (sortBy === 'oldest') return new Date(a.updated_at || 0) - new Date(b.updated_at || 0);
      if (sortBy === 'longest') return (b.word_count || 0) - (a.word_count || 0);
      return 0;
    });

    // Deduplicate in stream view: only keep newest instance of identical text on same site & URL
    const seenSigs = new Set();
    filtered = filtered.filter(d => {
      if (!d || !d.text) return false;
      const sig = `${(d.site || '').toLowerCase()}|${getCanonicalUrl(d.url)}|${d.text.trim()}`;
      if (seenSigs.has(sig)) return false;
      seenSigs.add(sig);
      return true;
    });

    const uniqueUrls = new Set(filtered.map(d => getCanonicalUrl(d.url) || d.site)).size;
    filteredCountBadge.textContent = `${filtered.length} draft${filtered.length === 1 ? '' : 's'} (${uniqueUrls} page${uniqueUrls === 1 ? '' : 's'})`;

    if (filtered.length === 0) {
      draftsStream.innerHTML = `
        <div style="padding: 30px; text-align: center; color: var(--text-dim); font-size: 13px;">
          No drafts match this filter or search.
        </div>
      `;
      updateCollapseAllBtn();
      return;
    }

    if (groupBy === 'flat') {
      filtered.forEach(d => {
        draftsStream.appendChild(createDraftCard(d, false));
      });
      updateCollapseAllBtn();
      return;
    }

    // Determine grouping map
    const groupsMap = new Map();
    if (groupBy === 'site') {
      filtered.forEach(d => {
        const siteKey = (d.site || 'web').toLowerCase();
        if (!groupsMap.has(siteKey)) {
          groupsMap.set(siteKey, {
            key: siteKey,
            title: d.site ? d.site.toUpperCase() : 'WEB',
            site: d.site,
            url: '',
            drafts: []
          });
        }
        groupsMap.get(siteKey).drafts.push(d);
      });
    } else {
      // Group by URL (default)
      filtered.forEach(d => {
        const cUrl = getCanonicalUrl(d.url) || d.site || 'Other';
        if (!groupsMap.has(cUrl)) {
          groupsMap.set(cUrl, {
            key: cUrl,
            url: d.url || cUrl,
            title: d.context_title || d.page_title || d.site,
            site: d.site,
            drafts: []
          });
        }
        groupsMap.get(cUrl).drafts.push(d);
      });
    }

    groupsMap.forEach(group => {
      const wrap = document.createElement('div');
      const isCollapsed = collapsedGroups.has(group.key);
      wrap.className = `url-group ${isCollapsed ? 'collapsed' : ''}`;
      wrap.dataset.key = group.key;

      const header = document.createElement('div');
      header.className = 'url-group-header';

      const siteClass = getSiteClass(group.site);

      header.innerHTML = `
        <div class="url-group-info">
          <span class="group-collapse-icon">▼</span>
          <span class="card-site-tag ${siteClass}">${escapeHtml(group.site || 'web')}</span>
          <span class="url-group-title" title="${escapeHtml(group.title)}">${escapeHtml(group.title)}</span>
          ${group.url && group.url.startsWith('http') ? `<a href="${escapeHtml(group.url)}" target="_blank" class="url-group-link" title="${escapeHtml(group.url)}">🔗 Open Page ↗</a>` : ''}
        </div>
        <span class="url-group-badge">${group.drafts.length} draft${group.drafts.length === 1 ? '' : 's'}</span>
      `;

      header.onclick = (e) => {
        if (e.target.closest('.url-group-link')) return;
        wrap.classList.toggle('collapsed');
        if (wrap.classList.contains('collapsed')) {
          collapsedGroups.add(group.key);
        } else {
          collapsedGroups.delete(group.key);
        }
        updateCollapseAllBtn();
      };

      const cardsWrap = document.createElement('div');
      cardsWrap.className = 'url-group-cards';

      group.drafts.forEach(d => {
        cardsWrap.appendChild(createDraftCard(d, true));
      });

      wrap.appendChild(header);
      wrap.appendChild(cardsWrap);
      draftsStream.appendChild(wrap);
    });

    updateCollapseAllBtn();
  }

  function getSiteClass(site) {
    const s = (site || '').toLowerCase();
    if (s.includes('reddit')) return 'reddit';
    if (s.includes('facebook')) return 'facebook';
    if (s.includes('twitter') || s === 'x.com') return 'twitter';
    return '';
  }

  // -------------------------------------------------------------
  // Rendering: Reader Pane
  // -------------------------------------------------------------
  function selectDraft(draft) {
    selectedDraft = draft;
    draftsStream.querySelectorAll('.draft-card').forEach(c => {
      if (c.dataset.id === draft.id) c.classList.add('active');
      else c.classList.remove('active');
    });
    renderReader();
  }

  function renderReader() {
    if (!selectedDraft) {
      readerEmpty.style.display = 'flex';
      readerContent.style.display = 'none';
      return;
    }

    readerEmpty.style.display = 'none';
    readerContent.style.display = 'flex';

    const d = selectedDraft;
    const title = d.context_title || d.page_title || 'Untitled Draft';
    const words = d.word_count || d.text.split(/\s+/).filter(Boolean).length;
    const chars = d.char_count || d.text.length;
    const readTimeMin = Math.max(1, Math.ceil(words / 200));

    readerSiteBadge.textContent = d.site || 'web';
    readerSiteBadge.className = `reader-site-badge ${getSiteClass(d.site)}`;
    readerTitle.textContent = title;

    if (d.url) {
      readerUrlLink.textContent = d.url;
      readerUrlLink.href = d.url;
      readerUrlLink.style.display = 'inline';
      document.querySelector('.reader-url-row').style.display = 'flex';
    } else {
      document.querySelector('.reader-url-row').style.display = 'none';
    }

    readerStatWords.textContent = `${words.toLocaleString()} words`;
    readerStatChars.textContent = `${chars.toLocaleString()} characters`;
    readerStatTime.textContent = `~${readTimeMin} min read`;
    readerStatUpdated.textContent = `Updated ${formatDate(d.updated_at)}`;

    if (d.status === 'posted') {
      toggleStatusIcon.textContent = '↩';
      toggleStatusText.textContent = 'Mark as Draft';
      btnToggleStatus.title = 'Mark as unposted draft';
    } else {
      toggleStatusIcon.textContent = '✓';
      toggleStatusText.textContent = 'Mark as Posted';
      btnToggleStatus.title = 'Mark as successfully posted';
    }

    readerText.textContent = d.text || '';
    if (isMonospace) {
      readerText.classList.add('monospace');
    } else {
      readerText.classList.remove('monospace');
    }
  }

  // -------------------------------------------------------------
  // Actions
  // -------------------------------------------------------------
  btnToggleStatus.onclick = async () => {
    if (!selectedDraft) return;
    const newStatus = selectedDraft.status === 'posted' ? 'draft' : 'posted';
    selectedDraft.status = newStatus;
    const idx = drafts.findIndex(item => item.id === selectedDraft.id);
    if (idx !== -1) drafts[idx].status = newStatus;
    await setDraftStatus(selectedDraft.id, newStatus);
    renderReader();
    renderStream();
  };

  btnCopyDraft.onclick = () => {
    if (!selectedDraft || !selectedDraft.text) return;
    navigator.clipboard.writeText(selectedDraft.text).then(() => {
      copyBtnText.textContent = 'Copied to Clipboard! ✓';
      btnCopyDraft.classList.add('btn-primary');
      setTimeout(() => {
        copyBtnText.textContent = 'Copy to Clipboard';
      }, 1800);
    });
  };

  btnDownloadMd.onclick = () => {
    if (!selectedDraft) return;
    const d = selectedDraft;
    const title = d.context_title || d.page_title || 'draft';
    const cleanTitle = title.replace(/[^a-zA-Z0-9_\-]/g, '_').slice(0, 40);
    const filename = `${d.site || 'draft'}_${cleanTitle}.md`;

    const mdContent = formatDraftMarkdown(d);
    downloadFile(filename, mdContent, 'text/markdown;charset=utf-8');
  };

  btnToggleFont.onclick = () => {
    isMonospace = !isMonospace;
    btnToggleFont.classList.toggle('btn-primary', isMonospace);
    if (readerText) {
      readerText.classList.toggle('monospace', isMonospace);
    }
  };

  btnDeleteDraft.onclick = async () => {
    if (!selectedDraft) return;
    if (confirm(`Are you sure you want to permanently delete this draft from ${selectedDraft.site}?`)) {
      const id = selectedDraft.id;
      await deleteDraftItem(id);
      drafts = drafts.filter(d => d.id !== id);
      selectedDraft = null;
      renderReader();
      refreshDashboard();
    }
  };

  // -------------------------------------------------------------
  // On-Demand Exports & Deduplication (JSON, Markdown .zip, Clean Duplicates)
  // -------------------------------------------------------------
  if (btnCleanDuplicates) {
    btnCleanDuplicates.onclick = async () => {
      chrome.runtime.sendMessage({ action: 'DEDUPLICATE_DRAFTS' }, async (res) => {
        if (res && res.removedCount > 0) {
          alert(`Cleaned up ${res.removedCount} duplicate draft${res.removedCount === 1 ? '' : 's'}!`);
        } else {
          alert('No duplicates found. All drafts are unique!');
        }
        await refreshDashboard();
      });
    };
  }

  btnExportJson.onclick = () => {
    if (drafts.length === 0) {
      alert('No drafts to export yet.');
      return;
    }
    const jsonStr = JSON.stringify(drafts, null, 2);
    downloadFile(`auto_scribe_archive_${new Date().toISOString().slice(0, 10)}.json`, jsonStr, 'application/json');
  };

  // Native Zero-Dependency Zip Creator
  btnExportZip.onclick = async () => {
    if (drafts.length === 0) {
      alert('No drafts to export yet.');
      return;
    }

    const files = drafts.map(d => {
      const site = (d.site || 'web').replace(/[^a-zA-Z0-9_\-\.]/g, '_');
      const title = (d.context_title || d.page_title || d.id).replace(/[\\/*?:"<>|]/g, '').replace(/[\s_]+/g, '-').slice(0, 40).trim() || 'draft';
      const path = `${site}/${title}_${d.id.slice(-6)}.md`;
      const content = formatDraftMarkdown(d);
      return { path, content };
    });

    const zipBlob = createZipBlob(files);
    downloadBlob(`auto_scribe_markdowns_${new Date().toISOString().slice(0, 10)}.zip`, zipBlob);
  };

  function downloadFile(filename, text, mimeType) {
    const blob = new Blob([text], { type: mimeType });
    downloadBlob(filename, blob);
  }

  function downloadBlob(filename, blob) {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  // Minimal ZIP encoder using standard RFC 1950 specs
  function createZipBlob(files) {
    const encoder = new TextEncoder();
    const fileEntries = [];
    let offset = 0;

    // CRC32 table
    const crcTable = new Uint32Array(256);
    for (let i = 0; i < 256; i++) {
      let c = i;
      for (let j = 0; j < 8; j++) {
        c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      }
      crcTable[i] = c;
    }

    function crc32(bytes) {
      let crc = 0 ^ (-1);
      for (let i = 0; i < bytes.length; i++) {
        crc = (crc >>> 8) ^ crcTable[(crc ^ bytes[i]) & 0xFF];
      }
      return (crc ^ (-1)) >>> 0;
    }

    const chunks = [];

    files.forEach(f => {
      const nameBytes = encoder.encode(f.path);
      const dataBytes = encoder.encode(f.content);
      const crc = crc32(dataBytes);
      const size = dataBytes.length;

      // Local file header (30 bytes + name length)
      const header = new Uint8Array(30 + nameBytes.length);
      const hv = new DataView(header.buffer);
      hv.setUint32(0, 0x04034b50, true); // signature
      hv.setUint16(4, 20, true);         // version needed
      hv.setUint16(6, 0, true);          // flags
      hv.setUint16(8, 0, true);          // compression (0 = store)
      hv.setUint16(10, 0, true);         // time
      hv.setUint16(12, 0, true);         // date
      hv.setUint32(14, crc, true);       // crc32
      hv.setUint32(18, size, true);      // compressed size
      hv.setUint32(22, size, true);      // uncompressed size
      hv.setUint16(26, nameBytes.length, true); // filename length
      hv.setUint16(28, 0, true);         // extra field length
      header.set(nameBytes, 30);

      chunks.push(header);
      chunks.push(dataBytes);

      fileEntries.push({ nameBytes, crc, size, offset });
      offset += header.length + size;
    });

    const cdStartOffset = offset;
    let cdSize = 0;

    // Central directory records
    fileEntries.forEach(entry => {
      const cd = new Uint8Array(46 + entry.nameBytes.length);
      const cdv = new DataView(cd.buffer);
      cdv.setUint32(0, 0x02014b50, true); // cd signature
      cdv.setUint16(4, 20, true);         // version made by
      cdv.setUint16(6, 20, true);         // version needed
      cdv.setUint16(8, 0, true);          // flags
      cdv.setUint16(10, 0, true);         // compression
      cdv.setUint16(12, 0, true);         // time
      cdv.setUint16(14, 0, true);         // date
      cdv.setUint32(16, entry.crc, true); // crc32
      cdv.setUint32(20, entry.size, true);// compressed size
      cdv.setUint32(24, entry.size, true);// uncompressed size
      cdv.setUint16(28, entry.nameBytes.length, true);
      cdv.setUint16(30, 0, true);         // extra len
      cdv.setUint16(32, 0, true);         // comment len
      cdv.setUint16(34, 0, true);         // disk start
      cdv.setUint16(36, 0, true);         // internal attrs
      cdv.setUint32(38, 0, true);         // external attrs
      cdv.setUint32(42, entry.offset, true); // local header offset
      cd.set(entry.nameBytes, 46);

      chunks.push(cd);
      cdSize += cd.length;
    });

    // End of central directory record (22 bytes)
    const eocd = new Uint8Array(22);
    const eocdv = new DataView(eocd.buffer);
    eocdv.setUint32(0, 0x06054b50, true); // eocd signature
    eocdv.setUint16(4, 0, true);          // disk number
    eocdv.setUint16(6, 0, true);          // start disk
    eocdv.setUint16(8, fileEntries.length, true);  // entries on disk
    eocdv.setUint16(10, fileEntries.length, true); // total entries
    eocdv.setUint32(12, cdSize, true);             // cd size
    eocdv.setUint32(16, cdStartOffset, true);      // cd offset
    eocdv.setUint16(20, 0, true);                  // comment len

    chunks.push(eocd);
    return new Blob(chunks, { type: 'application/zip' });
  }

  // -------------------------------------------------------------
  // Filter & Search Handlers
  // -------------------------------------------------------------
  globalSearch.oninput = () => {
    searchQuery = globalSearch.value.trim();
    clearSearch.style.display = searchQuery ? 'block' : 'none';
    renderStream();
  };

  clearSearch.onclick = () => {
    globalSearch.value = '';
    searchQuery = '';
    clearSearch.style.display = 'none';
    renderStream();
  };

  statusSelect.onchange = () => {
    filterStatus = statusSelect.value;
    renderStream();
  };

  groupSelect.onchange = () => {
    groupBy = groupSelect.value;
    renderStream();
  };

  if (btnToggleCollapseAll) {
    btnToggleCollapseAll.onclick = () => {
      const groups = draftsStream.querySelectorAll('.url-group');
      const anyExpanded = Array.from(groups).some(g => !g.classList.contains('collapsed'));

      groups.forEach(wrap => {
        const key = wrap.dataset.key;
        if (anyExpanded) {
          wrap.classList.add('collapsed');
          if (key) collapsedGroups.add(key);
        } else {
          wrap.classList.remove('collapsed');
          if (key) collapsedGroups.delete(key);
        }
      });
      updateCollapseAllBtn();
    };
  }

  sortSelect.onchange = () => {
    sortBy = sortSelect.value;
    renderStream();
  };

  lengthFilters.querySelectorAll('.pill-btn').forEach(btn => {
    btn.onclick = () => {
      lengthFilters.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      minLengthFilter = parseInt(btn.dataset.len, 10) || 0;
      renderStream();
    };
  });

  sitesList.querySelector('[data-site="all"]').onclick = () => {
    activeSite = 'all';
    updateActiveNavButtons();
    renderStream();
  };

  // -------------------------------------------------------------
  // Settings & Folder Pickers
  // -------------------------------------------------------------
  btnSettingsToggle.onclick = () => {
    settingMinChars.value = currentSettings.minChars || 50;
    settingDebounceMs.value = currentSettings.debounceMs || 1500;
    settingFloatingWidget.checked = currentSettings.showIndicator !== false && currentSettings.showFloatingWidget !== false;
    settingIgnoredDomains.value = (currentSettings.ignoredDomains || []).join(', ');
    settingsModal.style.display = 'flex';
  };

  btnCloseSettings.onclick = () => { settingsModal.style.display = 'none'; };
  btnCancelSettings.onclick = () => { settingsModal.style.display = 'none'; };

  document.querySelectorAll('.preset-chip').forEach(chip => {
    chip.onclick = () => {
      settingMinChars.value = chip.dataset.val;
    };
  });

  btnSaveSettings.onclick = async () => {
    const updated = {
      minChars: Math.max(10, parseInt(settingMinChars.value, 10) || 50),
      debounceMs: Math.max(500, parseInt(settingDebounceMs.value, 10) || 1500),
      showIndicator: settingFloatingWidget.checked,
      showFloatingWidget: settingFloatingWidget.checked,
      ignoredDomains: settingIgnoredDomains.value.split(',').map(s => s.trim()).filter(Boolean)
    };

    await persistSettings(updated);
    settingsModal.style.display = 'none';
    alert('Settings saved!');
  };

  btnClearAllData.onclick = async () => {
    if (confirm('DANGER: This will delete ALL drafts stored in local extension memory. Continue?')) {
      await clearAllDrafts();
      drafts = [];
      selectedDraft = null;
      renderReader();
      refreshDashboard();
      settingsModal.style.display = 'none';
    }
  };

  btnSidebarPickFolder.onclick = pickDiskFolder;
  btnModalPickFolder.onclick = pickDiskFolder;
  btnDisconnectFolder.onclick = disconnectDiskFolder;
  btnSyncAllDisk.onclick = async () => {
    const count = await syncAllDraftsToDisk();
    alert(`Synchronized ${count || 0} drafts to your folder!`);
  };

  // -------------------------------------------------------------
  // Helpers
  // -------------------------------------------------------------
  function refreshDashboard() {
    totalDraftsCount.textContent = drafts.length;
    const totalWords = drafts.reduce((sum, d) => sum + (d.word_count || 0), 0);
    totalWordsCount.textContent = totalWords.toLocaleString();

    const siteCounts = {};
    drafts.forEach(d => {
      const site = d.site || 'web';
      siteCounts[site] = (siteCounts[site] || 0) + 1;
    });

    renderSidebar(siteCounts);
    renderStream();
  }

  function formatTimeAgo(isoString) {
    if (!isoString) return '';
    const diff = (Date.now() - new Date(isoString).getTime()) / 1000;
    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
    return `${Math.floor(diff / 86400)}d ago`;
  }

  function formatDate(isoString) {
    if (!isoString) return '';
    try {
      const d = new Date(isoString);
      return d.toLocaleDateString(undefined, {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (e) {
      return isoString;
    }
  }

  function escapeHtml(str) {
    return (str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // -------------------------------------------------------------
  // Initialization
  // -------------------------------------------------------------
  async function init() {
    currentSettings = await fetchSettings();

    // Check stored disk folder handle
    try {
      const storedHandle = await getStoredDirHandle();
      if (storedHandle) {
        diskDirHandle = storedHandle;
        updateDiskUI(storedHandle.name);
      } else {
        updateDiskUI(null);
      }
    } catch (e) {
      updateDiskUI(null);
    }

    drafts = await fetchDrafts();
    refreshDashboard();

    if (drafts.length > 0 && !selectedDraft) {
      selectDraft(drafts[0]);
    }

    // Live sync with storage changes in background
    if (chrome.storage && chrome.storage.onChanged) {
      chrome.storage.onChanged.addListener((changes, areaName) => {
        if (areaName === 'local' && changes.scribe_drafts) {
          (async () => {
            drafts = await fetchDrafts();
            refreshDashboard();
            if (selectedDraft) {
              const updated = drafts.find(d => d.id === selectedDraft.id);
              if (updated) {
                selectedDraft = updated;
                renderReader();
              }
            }
          })();
        }
      });
    }
  }

  init();
})();
