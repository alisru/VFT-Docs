// Content script for Gemini web
(() => {
  let lastSentHash = '';
  let debounceTimer = null;
  let statusBadge = null;

  function createUI() {
    if (document.getElementById('chat-context-widget')) return;

    const widget = document.createElement('div');
    widget.id = 'chat-context-widget';
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
    `;

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

    const syncBtn = document.createElement('button');
    syncBtn.id = 'chat-context-sync-btn';
    syncBtn.textContent = 'Sync Now';
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
        // Extract text, excluding copy/edit buttons if present
        const textContainer = el.querySelector('.query-text, .response-content, message-content') || el;
        const text = textContainer.innerText.trim();
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
        // Collect in DOM order
        const all = document.querySelectorAll('.query-text, [data-test-id="user-query-content"], message-content, .response-content, .model-response-text');
        all.forEach((el) => {
          const isUser = el.matches('.query-text, [data-test-id="user-query-content"]');
          const text = el.innerText.trim();
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
          const text = el.innerText.trim();
          if (text && text.length > 5) {
            msgs.push({
              role: i % 2 === 0 ? 'user' : 'assistant',
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

    return {
      source: 'gemini',
      title: title || 'Gemini Chat',
      url: url,
      messages: msgs
    };
  }

  function performSync(isManual = false) {
    const chat = extractChat();
    if (!chat) {
      if (isManual) setStatus('error', 'No chat open');
      return;
    }

    const currentHash = chat.url + ':' + chat.messages.length + ':' + chat.messages[chat.messages.length - 1].text.slice(-40);
    if (!isManual && currentHash === lastSentHash) return;

    setStatus('syncing', 'Syncing...');

    chrome.runtime.sendMessage({ action: 'SYNC_CHAT', payload: chat }, (response) => {
      if (chrome.runtime.lastError || !response || !response.success) {
        const errMsg = response?.error || chrome.runtime.lastError?.message || 'Server offline';
        setStatus('error', 'Server offline');
        console.warn('[Chat Context Sync]', errMsg);
      } else {
        lastSentHash = currentHash;
        setStatus('synced', `Synced (${chat.messages.length})`);
      }
    });
  }

  // Observe chat DOM updates
  const observer = new MutationObserver(() => {
    createUI();
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      performSync(false);
    }, 2500);
  });

  window.addEventListener('load', () => {
    createUI();
    observer.observe(document.body, { childList: true, subtree: true });
  });

  // Initial check
  setTimeout(() => {
    createUI();
    observer.observe(document.body, { childList: true, subtree: true });
  }, 1000);
})();
