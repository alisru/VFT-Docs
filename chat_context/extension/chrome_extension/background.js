// Background service worker for Chat Context Sync & Context Drawer
// Auto-discovers active local server port (scans 8767..8775, fallback 8765)

const CANDIDATE_PORTS = [8767, 8768, 8769, 8770, 8771, 8772, 8765, 8766];
let activeBaseUrl = 'http://127.0.0.1:8767';

async function checkPort(port) {
  try {
    const ctrl = new AbortController();
    const timer = setTimeout(() => ctrl.abort(), 1500);
    const res = await fetch('http://127.0.0.1:' + port + '/api/status', { signal: ctrl.signal });
    clearTimeout(timer);
    if (res.ok) {
      const data = await res.json();
      if (data && ('rev' in data || 'state' in data)) return true;
    }
  } catch (e) {}
  return false;
}

async function getBaseUrl(forceRefresh = false) {
  if (!forceRefresh && activeBaseUrl) {
    const currentPort = parseInt(new URL(activeBaseUrl).port, 10);
    if (await checkPort(currentPort)) return activeBaseUrl;
  }
  for (const port of CANDIDATE_PORTS) {
    if (await checkPort(port)) {
      activeBaseUrl = 'http://127.0.0.1:' + port;
      console.log('[Chat Context Sync] Connected to active port:', activeBaseUrl);
      return activeBaseUrl;
    }
  }
  return activeBaseUrl;
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'GET_BASE_URL') {
    getBaseUrl().then(url => sendResponse({ success: true, url }));
    return true;
  }

  if (request.action === 'SYNC_CHAT') {
    getBaseUrl().then(baseUrl => {
      fetch(baseUrl + '/api/ingest/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request.payload)
      })
        .then(async (response) => {
          if (!response.ok) {
            const errText = await response.text();
            throw new Error('Server returned ' + response.status + ': ' + errText);
          }
          return response.json();
        })
        .then((data) => sendResponse({ success: true, data }))
        .catch(async (err) => {
          const newUrl = await getBaseUrl(true);
          console.warn('[Chat Context Sync] Send failed, retrying on', newUrl, err);
          sendResponse({ success: false, error: err.message });
        });
    });
    return true;
  }

  if (request.action === 'CENSOR_CHAT') {
    getBaseUrl().then(baseUrl => {
      fetch(baseUrl + '/api/chat/censor', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request.payload || {})
      })
        .then(async (response) => {
          if (!response.ok) {
            const errText = await response.text();
            throw new Error('Server returned ' + response.status + ': ' + errText);
          }
          return response.json();
        })
        .then((data) => sendResponse({ success: true, data }))
        .catch((err) => {
          console.warn('[Chat Context] Censor failed:', err);
          sendResponse({ success: false, error: err.message });
        });
    });
    return true;
  }

  if (request.action === 'CHECK_CENSORED') {
    const url = encodeURIComponent(request.url || '');
    const chatId = encodeURIComponent(request.chat_id || '');
    getBaseUrl().then(baseUrl => {
      fetch(baseUrl + '/api/chat/is-censored?url=' + url + '&chat_id=' + chatId)
        .then(async (r) => {
          if (!r.ok) return { censored: false };
          return r.json();
        })
        .then((data) => sendResponse({ success: true, censored: !!data.censored }))
        .catch(() => sendResponse({ success: false, censored: false }));
    });
    return true;
  }

  if (request.action === 'SEARCH_CHATS') {
    const k = request.k || 25;
    const sort = request.sort || 'relevance';
    const mode = request.mode || 'hybrid';
    const group_by = request.group_by || 'chat';
    const must_contain = encodeURIComponent(request.must_contain || '');
    const min_score = request.min_score || 0;
    const topic_id = request.topic_id ? ('&topic_id=' + request.topic_id) : '';
    const source = request.source ? ('&source=' + encodeURIComponent(request.source)) : '';
    getBaseUrl().then(baseUrl => {
      const url = baseUrl + '/api/search?q=' + encodeURIComponent(request.query || '') + '&k=' + k + '&sort=' + sort + '&mode=' + mode + '&group_by=' + group_by + '&must_contain=' + must_contain + '&min_score=' + min_score + topic_id + source;
      fetch(url)
        .then(async (r) => {
          if (!r.ok) throw new Error('Search error ' + r.status);
          return r.json();
        })
        .then((data) => sendResponse({ success: true, data }))
        .catch((err) => sendResponse({ success: false, error: err.message }));
    });
    return true;
  }

  if (request.action === 'GET_RELATED') {
    getBaseUrl().then(baseUrl => {
      fetch(baseUrl + '/api/related_live', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request.payload || {})
      })
        .then(async (r) => {
          if (!r.ok) throw new Error('Related error ' + r.status);
          return r.json();
        })
        .then((data) => sendResponse({ success: true, data }))
        .catch((err) => sendResponse({ success: false, error: err.message }));
    });
    return true;
  }

  if (request.action === 'GET_PACK') {
    getBaseUrl().then(baseUrl => {
      fetch(baseUrl + '/api/pack', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request.payload || {})
      })
        .then(async (r) => {
          if (!r.ok) throw new Error('Pack error ' + r.status);
          return r.text();
        })
        .then((text) => sendResponse({ success: true, text }))
        .catch((err) => sendResponse({ success: false, error: err.message }));
    });
    return true;
  }

  if (request.action === 'GET_RECENT_CANVASES') {
    const k = request.k || 30;
    getBaseUrl().then(baseUrl => {
      fetch(baseUrl + '/api/canvases/recent?k=' + k)
        .then(async (r) => {
          if (!r.ok) throw new Error('Canvases error ' + r.status);
          return r.json();
        })
        .then((data) => sendResponse({ success: true, data }))
        .catch((err) => sendResponse({ success: false, error: err.message }));
    });
    return true;
  }

  if (request.action === 'GET_STATUS') {
    getBaseUrl().then(baseUrl => {
      fetch(baseUrl + '/api/status')
        .then(async (r) => {
          if (!r.ok) throw new Error('Status error ' + r.status);
          return r.json();
        })
        .then((data) => sendResponse({ success: true, data }))
        .catch((err) => sendResponse({ success: false, error: err.message }));
    });
    return true;
  }

  if (request.action === 'GET_TOPICS_TREE') {
    getBaseUrl().then(baseUrl => {
      fetch(baseUrl + '/api/topics_tree')
        .then(async (r) => {
          if (!r.ok) throw new Error('Topics tree error ' + r.status);
          return r.json();
        })
        .then((data) => sendResponse({ success: true, data }))
        .catch((err) => sendResponse({ success: false, error: err.message }));
    });
    return true;
  }
});
