// ==UserScript==
// @name         Gemini Web to Chat Context Auto-Sync
// @namespace    https://local.chatcontext/
// @version      1.0
// @description  Automatically syncs Gemini web chats to your local Chat Context offline database
// @match        https://gemini.google.com/*
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// ==/UserScript==

(function() {
    'use strict';

    const SERVER_URL = 'http://127.0.0.1:8765/api/ingest/chat';
    let lastSentHash = '';
    let debounceTimer = null;

    function extractChat() {
        const url = window.location.href;
        // Skip root page if no conversation active
        if (!url.includes('/app/') && !url.includes('/share/')) return null;

        // Try getting title
        let title = document.title.replace(' - Gemini', '').trim();
        const titleEl = document.querySelector('h1, [data-test-id="conversation-title"]');
        if (titleEl && titleEl.textContent.trim()) {
            title = titleEl.textContent.trim();
        }

        // Query message turns
        const msgs = [];
        // User queries
        const queryEls = document.querySelectorAll('.user-query, [data-test-id="user-query"], user-query-item');
        // Responses
        const responseEls = document.querySelectorAll('.model-response, [data-test-id="model-response"], model-response');

        // If specific selectors match
        if (queryEls.length > 0) {
            const allTurns = document.querySelectorAll('.user-query, .model-response, user-query-item, model-response');
            allTurns.forEach(el => {
                const isUser = el.matches('.user-query, user-query-item, [data-test-id="user-query"]');
                const text = el.innerText.trim();
                if (text) {
                    msgs.push({
                        role: isUser ? 'user' : 'assistant',
                        text: text
                    });
                }
            });
        } else {
            // Fallback: search main chat scroller
            const textContainers = document.querySelectorAll('message-content, .message-content, [role="region"]');
            textContainers.forEach((el, i) => {
                const text = el.innerText.trim();
                if (text && text.length > 5) {
                    msgs.push({
                        role: i % 2 === 0 ? 'user' : 'assistant',
                        text: text
                    });
                }
            });
        }

        if (msgs.length === 0) return null;

        return {
            source: 'gemini',
            title: title || 'Gemini Chat',
            url: url,
            messages: msgs
        };
    }

    function sendToLocal(chat) {
        if (!chat || chat.messages.length === 0) return;
        const currentHash = chat.url + ':' + chat.messages.length + ':' + chat.messages[chat.messages.length - 1].text.slice(-50);
        if (currentHash === lastSentHash) return;

        const payload = JSON.stringify(chat);

        const sendReq = (typeof GM_xmlhttpRequest !== 'undefined') ? GM_xmlhttpRequest : null;
        if (sendReq) {
            sendReq({
                method: 'POST',
                url: SERVER_URL,
                headers: { 'Content-Type': 'application/json' },
                data: payload,
                onload: function(r) {
                    if (r.status === 200) {
                        lastSentHash = currentHash;
                        showBadge('Synced to Chat Context');
                    }
                }
            });
        } else {
            fetch(SERVER_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: payload
            }).then(r => {
                if (r.ok) {
                    lastSentHash = currentHash;
                    showBadge('Synced to Chat Context');
                }
            }).catch(() => {});
        }
    }

    function showBadge(text) {
        let badge = document.getElementById('chat-context-badge');
        if (!badge) {
            badge = document.createElement('div');
            badge.id = 'chat-context-badge';
            badge.style.cssText = 'position:fixed;bottom:16px;right:16px;background:#1e3a5f;color:#93c5fd;padding:6px 12px;border-radius:6px;font-size:12px;font-family:sans-serif;z-index:99999;box-shadow:0 2px 8px rgba(0,0,0,0.3);transition:opacity 0.4s;pointer-events:none;';
            document.body.appendChild(badge);
        }
        badge.textContent = text;
        badge.style.opacity = '1';
        setTimeout(() => { if (badge) badge.style.opacity = '0'; }, 3000);
    }

    // Auto-sync observer: triggers when DOM stops mutating for 2.5s
    const observer = new MutationObserver(() => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            const chat = extractChat();
            if (chat) sendToLocal(chat);
        }, 2500);
    });

    observer.observe(document.body, { childList: true, subtree: true });

    // Also add manual sync button in top corner
    const btn = document.createElement('button');
    btn.textContent = '💾 Sync to Context';
    btn.style.cssText = 'position:fixed;bottom:16px;left:16px;background:#1b1e24;border:1px solid #2c313a;color:#d8dce3;padding:6px 12px;border-radius:6px;font-size:12px;cursor:pointer;z-index:99999;';
    btn.onclick = () => {
        const chat = extractChat();
        if (chat) {
            sendToLocal(chat);
        } else {
            showBadge('No chat detected to sync');
        }
    };
    document.body.appendChild(btn);
})();
