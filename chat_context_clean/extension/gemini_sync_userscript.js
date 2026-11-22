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
            if (title && title.trim() && (title.includes('\\') || title.includes('_') || title.includes('^'))) return title.trim();
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
        root.querySelectorAll('math-block, math-inline').forEach(node => {
            if (!node.parentNode) return;
            const tex = extractTeX(node);
            if (!tex) return;
            const isBlock = node.tagName.toLowerCase() === 'math-block' || !!node.querySelector('.katex-display');
            node.parentNode.replaceChild(document.createTextNode(isBlock ? `\n\n$$\n${tex}\n$$\n\n` : ` $${tex}$ `), node);
        });
        root.querySelectorAll('.katex-display').forEach(display => {
            if (!display.parentNode) return;
            const tex = extractTeX(display);
            if (tex) display.parentNode.replaceChild(document.createTextNode(`\n\n$$\n${tex}\n$$\n\n`), display);
        });
        root.querySelectorAll('.katex').forEach(inline => {
            if (!inline.parentNode) return;
            const tex = extractTeX(inline);
            if (tex) inline.parentNode.replaceChild(document.createTextNode(` $${tex}$ `), inline);
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
                cells.forEach(() => { separator += ' --- |'; });
                md += separator + '\n';
            }
        });
        return md;
    }

    function htmlToMarkdown(element) {
        if (!element) return '';
        const clone = element.cloneNode(true);
        replaceKaTeX(clone);

        const codeHeaders = clone.querySelectorAll('.code-block-header');
        codeHeaders.forEach(header => {
            const langSpan = header.querySelector('span');
            const langText = langSpan ? langSpan.textContent.trim() : '';
            const pre = header.nextElementSibling;
            if (pre && pre.tagName === 'PRE') pre.setAttribute('data-language', langText);
            header.remove();
        });

        function processNode(node) {
            if (node.nodeType === Node.TEXT_NODE) return node.nodeValue || '';
            if (node.nodeType !== Node.ELEMENT_NODE) return '';

            let childrenVal = '';
            node.childNodes.forEach(child => { childrenVal += processNode(child); });

            const tag = node.tagName.toUpperCase();
            switch (tag) {
                case 'H1': return `\n\n# ${childrenVal.trim()}\n\n`;
                case 'H2': return `\n\n## ${childrenVal.trim()}\n\n`;
                case 'H3': return `\n\n### ${childrenVal.trim()}\n\n`;
                case 'H4': return `\n\n#### ${childrenVal.trim()}\n\n`;
                case 'H5': return `\n\n##### ${childrenVal.trim()}\n\n`;
                case 'H6': return `\n\n###### ${childrenVal.trim()}\n\n`;
                case 'P':
                    if (node.parentNode && node.parentNode.tagName === 'LI') return childrenVal.trim();
                    return `\n\n${childrenVal.trim()}\n\n`;
                case 'STRONG':
                case 'B': return `**${childrenVal.trim()}**`;
                case 'EM':
                case 'I': return `*${childrenVal.trim()}*`;
                case 'DEL':
                case 'S':
                case 'STRIKE': return `~~${childrenVal.trim()}~~`;
                case 'CODE':
                    if (node.parentNode && node.parentNode.tagName === 'PRE') return childrenVal;
                    return `\`${childrenVal.trim()}\``;
                case 'PRE':
                    const lang = node.getAttribute('data-language') || '';
                    node.querySelectorAll('button, .copy-code-button').forEach(b => b.remove());
                    return `\n\n\`\`\`${lang}\n${node.textContent.trim()}\n\`\`\`\n\n`;
                case 'BLOCKQUOTE':
                    const lines = childrenVal.trim().split('\n');
                    return '\n\n' + lines.map(l => `> ${l}`).join('\n') + '\n\n';
                case 'UL':
                case 'OL': return `\n${childrenVal}\n`;
                case 'LI':
                    const parentTag = node.parentNode ? node.parentNode.tagName : '';
                    if (parentTag === 'OL') {
                        const siblings = Array.from(node.parentNode.children);
                        const idx = siblings.indexOf(node) + 1;
                        return `${idx}. ${childrenVal.trim()}\n`;
                    }
                    return `- ${childrenVal.trim()}\n`;
                case 'TABLE': return `\n\n${renderTableToMarkdown(node)}\n\n`;
                case 'HR': return '\n\n---\n\n';
                case 'BR': return '\n';
                case 'A': return `[${childrenVal.trim()}](${node.getAttribute('href') || ''})`;
                default: return childrenVal;
            }
        }
        return processNode(clone).replace(/\n{3,}/g, '\n\n').trim();
    }

    function extractCanvases() {
        const canvases = [];
        try {
            const canvasContainers = document.querySelectorAll(
                'immersive-entry-chip, immersive-editor, inline-preview, ' +
                'immersive-panel, [data-test-id*="immersive"], [data-test-id*="canvas"], ' +
                '.immersive-container, .canvas-container, [aria-label*="Canvas" i], aside[class*="immersive"]'
            );
            canvasContainers.forEach((panel, idx) => {
                if (panel.id === 'chat-context-widget' || panel.closest?.('#chat-context-widget')) return;

                if (panel.parentElement && panel.parentElement.closest('immersive-entry-chip, immersive-panel, .canvas-container')) {
                    return;
                }

                let title = '';
                const titleInput = panel.querySelector(
                    '.title, .title-wrapper .title, .title-container .title, ' +
                    'input[aria-label*="title" i], input[placeholder*="title" i], ' +
                    '[data-test-id="canvas-title"], .canvas-title, .immersive-title'
                );
                if (titleInput) title = titleInput.value || titleInput.textContent || '';
                if (!title) {
                    const heading = panel.querySelector('header h1, header h2, header [role="heading"], h1, h2, h3');
                    if (heading) title = heading.textContent.trim();
                }

                let content = '';
                let type = 'markdown';

                const monacoLines = panel.querySelectorAll('.view-lines .view-line');
                if (monacoLines.length > 0) {
                    content = Array.from(monacoLines).map(l => l.innerText).join('\n');
                    type = 'code';
                }

                if (!content) {
                    const cmLines = panel.querySelectorAll('.cm-content .cm-line');
                    if (cmLines.length > 0) {
                        content = Array.from(cmLines).map(l => l.innerText).join('\n');
                        type = 'code';
                    }
                }

                if (!content) {
                    const editable = panel.querySelector('#extended-response-markdown-content .ProseMirror')
                                  || panel.querySelector('#extended-response-markdown-content')
                                  || panel.querySelector('.ProseMirror[aria-label*="Canvas" i]')
                                  || panel.querySelector('.ProseMirror, .tiptap, [contenteditable="true"]');
                    if (editable) {
                        content = htmlToMarkdown(editable);
                        type = 'markdown';
                        if (!title || title.startsWith('Canvas ')) {
                            const firstHeading = editable.querySelector('h1, h2');
                            if (firstHeading && firstHeading.textContent.trim()) {
                                title = firstHeading.textContent.trim();
                            }
                        }
                    }
                }

                if (!content) {
                    const docContainer = panel.querySelector('.doc-preview, .document-content, .canvas-content, .editor-content');
                    if (docContainer) {
                        content = htmlToMarkdown(docContainer);
                        type = 'markdown';
                    }
                }

                title = title.replace(/\s*(Contents\s*Share\s*&\s*Export\s*Create|Contents|Share\s*&\s*Export|Share|Export|Download|Close|Create)\s*$/i, '').replace(/\s+/g, ' ').trim() || `Canvas ${idx + 1}`;
                content = (content || '').trim();

                if (content && content.length > 10) {
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
        } catch (e) {
            console.warn('[Chat Context] Canvas extraction error:', e);
        }
        return canvases;
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
            'immersive-entry-chip', 'immersive-editor', 'inline-preview',
            '[data-test-id*="immersive"]', '[data-test-id*="canvas"]',
            '.immersive-container', '.canvas-container'
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

        let title = document.title.replace(' - Gemini', '').trim();
        const titleEl = document.querySelector('h1, [data-test-id="conversation-title"]');
        if (titleEl && titleEl.textContent.trim()) {
            title = titleEl.textContent.trim();
        }

        const msgs = [];
        const queryEls = document.querySelectorAll('.user-query, [data-test-id="user-query"], user-query-item');
        if (queryEls.length > 0) {
            const allTurns = document.querySelectorAll('.user-query, .model-response, user-query-item, model-response');
            allTurns.forEach(el => {
                const isUser = el.matches('.user-query, user-query-item, [data-test-id="user-query"]');
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
            const textContainers = document.querySelectorAll('message-content, .message-content, [role="region"]');
            textContainers.forEach((el, i) => {
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

        if (msgs.length === 0) return null;

        const canvases = extractCanvases();

        return {
            source: 'gemini',
            title: title || 'Gemini Chat',
            url: url,
            messages: msgs,
            canvases: canvases
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
