// Background service worker for Chat Context Sync
// Relays chat payloads to local server, completely immune to page Content-Security-Policy (CSP)

const SERVER_URL = 'http://127.0.0.1:8765/api/ingest/chat';

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'SYNC_CHAT') {
    fetch(SERVER_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request.payload)
    })
      .then(async (response) => {
        if (!response.ok) {
          const errText = await response.text();
          throw new Error(`Server returned ${response.status}: ${errText}`);
        }
        return response.json();
      })
      .then((data) => {
        sendResponse({ success: true, data: data });
      })
      .catch((err) => {
        console.warn('[Chat Context Sync] Failed to send to local server:', err);
        sendResponse({ success: false, error: err.message });
      });

    return true; // Keep channel open for async response
  }
});
