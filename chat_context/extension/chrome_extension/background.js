// Background service worker for Chat Context Sync & Context Drawer
// Relays chat payloads and queries to local server, completely immune to page Content-Security-Policy (CSP)

const BASE_URL = 'http://127.0.0.1:8765';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'SYNC_CHAT') {
    fetch(`${BASE_URL}/api/ingest/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request.payload)
    })
      .then(async (response) => {
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Server returned ${response.status}: ${errText}`);
        }
        return response.json();
      })
      .then((data) => sendResponse({ success: true, data }))
      .catch((err) => {
        console.warn('[Chat Context Sync] Failed to send to local server:', err);
        sendResponse({ success: false, error: err.message });
      });
    return true;
  }

  if (request.action === 'SEARCH_CHATS') {
    const k = request.k || 15;
    fetch(`${BASE_URL}/api/search?q=${encodeURIComponent(request.query || '')}&k=${k}`)
      .then(async (r) => {
        if (!r.ok) throw new Error(`Search error ${r.status}`);
        return r.json();
      })
      .then((data) => sendResponse({ success: true, data }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true;
  }

  if (request.action === 'GET_RELATED') {
    fetch(`${BASE_URL}/api/related_live`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request.payload || {})
    })
      .then(async (r) => {
        if (!r.ok) throw new Error(`Related error ${r.status}`);
        return r.json();
      })
      .then((data) => sendResponse({ success: true, data }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true;
  }

  if (request.action === 'GET_PACK') {
    fetch(`${BASE_URL}/api/pack`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request.payload || {})
    })
      .then(async (r) => {
        if (!r.ok) throw new Error(`Pack error ${r.status}`);
        return r.text();
      })
      .then((text) => sendResponse({ success: true, text }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true;
  }

  if (request.action === 'GET_RECENT_CANVASES') {
    const k = request.k || 30;
    fetch(`${BASE_URL}/api/canvases/recent?k=${k}`)
      .then(async (r) => {
        if (!r.ok) throw new Error(`Canvases error ${r.status}`);
        return r.json();
      })
      .then((data) => sendResponse({ success: true, data }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true;
  }

  if (request.action === 'GET_STATUS') {
    fetch(`${BASE_URL}/api/status`)
      .then(async (r) => {
        if (!r.ok) throw new Error(`Status error ${r.status}`);
        return r.json();
      })
      .then((data) => sendResponse({ success: true, data }))
      .catch((err) => sendResponse({ success: false, error: err.message }));
    return true;
  }
});
