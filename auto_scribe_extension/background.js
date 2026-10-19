// Background service worker for Auto-Scribe Standalone Extension
// 100% Pure Extension: Solid, zero-overhead storage in chrome.storage.local

const DEFAULT_SETTINGS = {
  minChars: 50,
  debounceMs: 1500,
  enabled: true,
  showIndicator: true,
  ignoredDomains: ['accounts.google.com', 'login.microsoftonline.com']
};

async function getSettings() {
  const data = await chrome.storage.local.get(['scribe_settings']);
  return { ...DEFAULT_SETTINGS, ...(data.scribe_settings || {}) };
}

async function getDraftsDict() {
  const data = await chrome.storage.local.get(['scribe_drafts']);
  return data.scribe_drafts || {};
}

async function saveDraftsDict(drafts) {
  await chrome.storage.local.set({ scribe_drafts: drafts });
  updateBadge(drafts);
}

function updateBadge(drafts) {
  const list = typeof drafts === 'object' && drafts !== null ? Object.values(drafts) : [];
  const unpostedCount = list.filter(d => d && d.status !== 'posted').length;
  if (unpostedCount > 0) {
    chrome.action.setBadgeText({ text: unpostedCount > 99 ? '99+' : String(unpostedCount) });
    chrome.action.setBadgeBackgroundColor({ color: '#2563eb' });
  } else {
    chrome.action.setBadgeText({ text: '' });
  }
}

function getCanonicalUrl(rawUrl) {
  if (!rawUrl) return '';
  try {
    const u = new URL(rawUrl);
    return (u.origin + u.pathname).replace(/\/$/, '');
  } catch (e) {
    return (rawUrl || '').split('#')[0].split('?')[0].replace(/\/$/, '');
  }
}

function deduplicateDraftsDict(draftsDict) {
  const list = Object.values(draftsDict || {});
  const seen = new Map();
  let removedCount = 0;

  // Sort newest updated first so we keep the freshest timestamp
  list.sort((a, b) => new Date(b.updated_at || 0) - new Date(a.updated_at || 0));

  for (const d of list) {
    if (!d || !d.text) continue;
    const normText = d.text.trim();
    if (!normText) continue;

    const site = (d.site || '').toLowerCase();
    const cUrl = getCanonicalUrl(d.url);
    const sig = `${site}|${cUrl}|${normText}`;

    if (!seen.has(sig)) {
      seen.set(sig, d);
    } else {
      const primary = seen.get(sig);
      if (d.status === 'posted' && primary.status !== 'posted') {
        primary.status = 'posted';
        primary.posted_at = d.posted_at || primary.posted_at || new Date().toISOString();
      }
      removedCount++;
    }
  }

  const cleanDict = {};
  seen.forEach(d => {
    cleanDict[d.id] = d;
  });

  return { cleanDict, removedCount };
}

// Storage sync listener for badge
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === 'local' && changes.scribe_drafts) {
    updateBadge(changes.scribe_drafts.newValue || {});
  }
});

// Startup: auto-clean duplicates and update badge
(async () => {
  const drafts = await getDraftsDict();
  const { cleanDict, removedCount } = deduplicateDraftsDict(drafts);
  if (removedCount > 0) {
    console.log(`[Auto-Scribe] Startup cleanup: merged ${removedCount} duplicate drafts.`);
    await saveDraftsDict(cleanDict);
  } else {
    updateBadge(cleanDict);
  }
})();

// Message router
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'OPEN_DASHBOARD') {
    chrome.tabs.create({ url: chrome.runtime.getURL('dashboard.html') });
    sendResponse({ ok: true });
    return true;
  }

  if (request.action === 'DEDUPLICATE_DRAFTS') {
    (async () => {
      const drafts = await getDraftsDict();
      const { cleanDict, removedCount } = deduplicateDraftsDict(drafts);
      if (removedCount > 0) {
        await saveDraftsDict(cleanDict);
      }
      sendResponse({ success: true, removedCount });
    })();
    return true;
  }

  if (request.action === 'SAVE_DRAFT') {
    (async () => {
      const payload = request.payload;
      if (!payload || !payload.id || !payload.text) {
        sendResponse({ success: false, error: 'Invalid draft payload' });
        return;
      }

      const drafts = await getDraftsDict();
      const normText = payload.text.trim();
      const cUrl = getCanonicalUrl(payload.url);
      const site = (payload.site || '').toLowerCase();

      // Check for an existing draft with the exact same text on the same page or site
      let targetId = payload.id;
      let existing = drafts[targetId];

      if (!existing) {
        for (const [did, d] of Object.entries(drafts)) {
          if (!d || !d.text) continue;
          const isSamePage = (cUrl && getCanonicalUrl(d.url) === cUrl) || ((d.site || '').toLowerCase() === site);
          if (isSamePage && d.text.trim() === normText) {
            targetId = did;
            existing = d;
            break;
          }
        }
      }

      // Guard against race condition: don't revert an already posted draft if identical text or posted recently
      if (existing && existing.status === 'posted') {
        const postedTime = existing.posted_at ? new Date(existing.posted_at).getTime() : 0;
        const isRecentPosted = (Date.now() - postedTime < 15000);
        if (existing.text === payload.text || isRecentPosted) {
          sendResponse({ success: true, id: targetId, ignoredRevert: true });
          return;
        }
      }

      drafts[targetId] = {
        status: 'draft',
        ...(existing || {}),
        ...payload,
        id: targetId,
        status: payload.status || (existing && existing.status) || 'draft',
        posted_at: payload.posted_at || (existing && existing.posted_at) || (payload.status === 'posted' ? new Date().toISOString() : undefined),
        created_at: (existing && existing.created_at) || payload.updated_at || new Date().toISOString()
      };
      await saveDraftsDict(drafts);

      sendResponse({ success: true, id: targetId });
    })();
    return true;
  }

  if (request.action === 'GET_DRAFTS') {
    (async () => {
      const draftsDict = await getDraftsDict();
      const drafts = Object.values(draftsDict).sort((a, b) => {
        return new Date(b.updated_at || 0) - new Date(a.updated_at || 0);
      });
      sendResponse({ success: true, drafts: drafts });
    })();
    return true;
  }

  if (request.action === 'DELETE_DRAFT') {
    (async () => {
      const did = request.id;
      const drafts = await getDraftsDict();
      if (drafts[did]) {
        delete drafts[did];
        await saveDraftsDict(drafts);
      }
      sendResponse({ success: true });
    })();
    return true;
  }

  if (request.action === 'SET_DRAFT_STATUS' || request.action === 'MARK_DRAFT_POSTED') {
    (async () => {
      const did = request.id;
      const status = request.status || 'posted';
      if (!did) {
        sendResponse({ success: false, error: 'No draft ID' });
        return;
      }
      const drafts = await getDraftsDict();
      if (drafts[did]) {
        drafts[did].status = status;
        if (status === 'posted') {
          drafts[did].posted_at = new Date().toISOString();
        } else {
          delete drafts[did].posted_at;
        }
        await saveDraftsDict(drafts);
      } else if (request.payload) {
        drafts[did] = {
          ...request.payload,
          status: status,
          posted_at: status === 'posted' ? new Date().toISOString() : undefined,
          created_at: request.payload.updated_at || new Date().toISOString()
        };
        await saveDraftsDict(drafts);
      }
      sendResponse({ success: true });
    })();
    return true;
  }

  if (request.action === 'CLEAR_DRAFTS') {
    (async () => {
      await saveDraftsDict({});
      sendResponse({ success: true });
    })();
    return true;
  }

  if (request.action === 'GET_SETTINGS') {
    (async () => {
      const settings = await getSettings();
      sendResponse({ success: true, settings: settings });
    })();
    return true;
  }

  if (request.action === 'SAVE_SETTINGS') {
    (async () => {
      const current = await getSettings();
      const updated = { ...current, ...(request.settings || {}) };
      await chrome.storage.local.set({ scribe_settings: updated });
      sendResponse({ success: true, settings: updated });
    })();
    return true;
  }
});
