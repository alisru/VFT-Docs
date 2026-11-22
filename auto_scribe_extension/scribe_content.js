/**
 * Auto-Scribe Content Script
 * Intercepts text entered into textareas, inputs, and contenteditable editors
 * (Reddit ProseMirror/Shreddit, Facebook Lexical, Twitter/X, forums, etc.)
 * Only persists text exceeding a configurable character threshold (> n chars).
 */

(() => {
  // Prevent double injection
  if (window.__AUTO_SCRIBE_LOADED__) return;
  window.__AUTO_SCRIBE_LOADED__ = true;
  console.log('[Auto-Scribe] Content script active on ' + window.location.hostname);

  // Don't run on local server dashboard to avoid self-recording
  if (window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost') {
    if (window.location.port === '8765') return;
  }

  // Default configuration
  let config = {
    minChars: 30,
    debounceMs: 300,
    enabled: true,
    showIndicator: true,
    ignoredDomains: []
  };

  // Check if current domain is blacklisted
  function getEffectiveHost() {
    try {
      const h = (window.top && window.top.location.hostname) || window.location.hostname;
      return h.replace(/^www\./, '').toLowerCase();
    } catch (e) {
      return window.location.hostname.replace(/^www\./, '').toLowerCase();
    }
  }
  const currentHost = getEffectiveHost();

  // Load settings from background
  try {
    chrome.runtime.sendMessage({ action: 'GET_SETTINGS' }, (res) => {
      if (chrome.runtime.lastError) return;
      if (res && res.settings) {
        config = { ...config, ...res.settings };
      }
    });
  } catch (e) {
    // Background not ready
  }

  // State
  let activeElement = null;
  let lastActiveElement = null;
  let lastActiveDraftId = null;
  let debounceTimer = null;
  let currentWorkingTextMap = new WeakMap();
  let sessionKeyMap = new WeakMap();
  let savedDraftMap = new WeakMap();
  let submittedDrafts = new Set();
  let lastSubmitTime = 0;
  let activeObserver = null;
  let indicatorEl = null;
  let fadeTimeout = null;
  let lastSavedText = '';

  /**
   * Resolve any element or child node to its canonical root editable container
   */
  function getEditableRoot(el) {
    if (!el) return null;
    if (el.nodeType === 3) el = el.parentElement;
    if (!el || !el.tagName) return null;

    const tag = el.tagName.toLowerCase();
    if (tag === 'textarea' || tag === 'input') {
      return el;
    }

    const ce = el.closest('[contenteditable="true"], [role="textbox"], .ProseMirror, .public-DraftEditor-content, [data-lexical-editor="true"], .ql-editor, body.cke_editable');
    if (ce) return ce;
    if (el.isContentEditable || el.contentEditable === 'true') return el;
    if (el.ownerDocument && el.ownerDocument.designMode === 'on') return el.ownerDocument.body;
    return null;
  }

  /**
   * Helper: Check if element is sensitive or password
   */
  function isSensitiveElement(el) {
    const root = getEditableRoot(el);
    if (!root || !root.tagName) return true;
    const tag = root.tagName.toLowerCase();
    if (tag === 'input') {
      const type = (root.getAttribute('type') || 'text').toLowerCase();
      if (['password', 'hidden', 'email', 'number', 'tel', 'date', 'checkbox', 'radio', 'file'].includes(type)) {
        return true;
      }
    }
    const ac = (root.getAttribute('autocomplete') || '').toLowerCase();
    if (ac.includes('password') || ac.includes('cc-') || ac.includes('current-password')) {
      return true;
    }
    const name = (root.getAttribute('name') || root.id || '').toLowerCase();
    if (name.includes('pass') || name.includes('pin') || name.includes('cvv') || name.includes('card')) {
      return true;
    }
    return false;
  }

  /**
   * Helper: Extract clean text from element
   */
  function extractText(el) {
    if (!el) return '';
    const tag = el.tagName ? el.tagName.toLowerCase() : '';

    if (tag === 'textarea' || tag === 'input') {
      const val = (el.value || '').trim();
      const ph = (el.placeholder || '').trim();
      return (ph && val === ph) ? '' : val;
    }

    if (el.isContentEditable || el.getAttribute('contenteditable') === 'true' || el.getAttribute('role') === 'textbox') {
      const clone = el.cloneNode(true);
      // Strip decorations, hidden artifacts, and Lexical/ProseMirror cursor placeholders
      clone.querySelectorAll('[aria-hidden="true"], [data-lexical-cursor="true"], .empty-placeholder, [class*="placeholder" i], [data-placeholder]').forEach(n => {
        if (n.classList && (n.classList.contains('placeholder') || n.className.toString().toLowerCase().includes('placeholder'))) {
          n.remove();
        } else if (n.hasAttribute('aria-hidden') || n.hasAttribute('data-lexical-cursor')) {
          n.remove();
        }
      });
      
      // Preserve line breaks
      clone.querySelectorAll('br').forEach(br => br.replaceWith('\n'));
      clone.querySelectorAll('p, div, li, h1, h2, h3, h4, h5, h6').forEach(b => {
        b.prepend('\n');
      });

      let text = clone.textContent || '';
      text = text.replace(/[\u200B\uFEFF]/g, ''); // strip zero-width characters
      text = text.replace(/\n{3,}/g, '\n\n').trim();

      // Check if text is just the placeholder text
      const placeholder = (el.getAttribute('placeholder') || el.getAttribute('data-placeholder') || el.getAttribute('aria-label') || '').trim();
      if (placeholder && text.toLowerCase() === placeholder.toLowerCase()) {
        return '';
      }

      return text;
    }

    return '';
  }

  /**
   * Context extraction: subreddit, post title, Facebook group, or page title
   */
  function detectContext() {
    const host = currentHost;
    let contextTitle = '';

    // Reddit Context Extraction
    if (host.includes('reddit.com')) {
      // Subreddit from URL
      const subMatch = window.location.pathname.match(/\/r\/([^\/]+)/i);
      const sub = subMatch ? `r/${subMatch[1]}` : '';
      
      // Post title
      const h1 = document.querySelector('h1, shreddit-post [slot="title"], [data-testid="post-title"]');
      const title = h1 ? h1.textContent.trim() : '';
      if (sub && title) {
        contextTitle = `${sub}: ${title}`;
      } else if (sub) {
        contextTitle = sub;
      } else if (title) {
        contextTitle = title;
      }
    }
    // Facebook Context Extraction
    else if (host.includes('facebook.com')) {
      const groupHeader = document.querySelector('h1, span[dir="auto"] strong, [role="main"] h2');
      if (groupHeader && groupHeader.textContent.trim()) {
        contextTitle = `Facebook: ${groupHeader.textContent.trim().slice(0, 80)}`;
      }
    }
    // Twitter / X Context Extraction
    else if (host.includes('x.com') || host.includes('twitter.com')) {
      const tweetTarget = document.querySelector('[data-testid="tweetTextarea_0_label"], [data-testid="tweet"]');
      if (tweetTarget) {
        contextTitle = `X / Twitter: ${document.title.replace(/ \/ X$/, '').trim()}`;
      }
    }

    if (!contextTitle) {
      try {
        contextTitle = (window.top && window.top.document.title) || document.title || window.location.pathname;
      } catch (e) {
        contextTitle = document.title || window.location.pathname;
      }
    }

    // Clean up generic suffixes
    contextTitle = contextTitle
      .replace(/ - Google Chrome$/i, '')
      .replace(/ - Reddit$/i, '')
      .replace(/ \| Facebook$/i, '')
      .trim();

    return contextTitle;
  }

  /**
   * Generate stable draft ID for the active field session
   */
  function getSessionId(el) {
    if (!sessionKeyMap.has(el)) {
      const path = window.location.pathname.replace(/\/$/, '') || 'root';
      const rand = Math.random().toString(36).slice(2, 8);
      const tag = el.tagName ? el.tagName.toLowerCase() : 'div';
      const cleanPath = path.replace(/[^a-zA-Z0-9_\-]/g, '_').slice(0, 30);
      const id = `draft_${currentHost}_${cleanPath}_${rand}`;
      sessionKeyMap.set(el, id);
    }
    return sessionKeyMap.get(el);
  }

  /**
   * Delete draft from background storage when text is removed
   */
  function deleteSavedDraft(id) {
    if (!id) return;
    try {
      chrome.runtime.sendMessage({
        action: 'DELETE_DRAFT',
        id: id
      });
    } catch (e) {}
    lastSavedText = '';
    lastActiveDraftId = null;
    activeEmptyCheck = null;
  }

  /**
   * Mark draft as posted in background
   */
  function markDraftPosted(id, fallbackPayload) {
    if (!id) return;
    try {
      chrome.runtime.sendMessage({
        action: 'MARK_DRAFT_POSTED',
        id: id,
        payload: fallbackPayload || null
      });
      const targetEl = activeElement || lastActiveElement;
      if (targetEl) {
        updateIndicator('saved', targetEl);
      }
    } catch (e) {}
  }

  /**
   * Observe active editor mutations (catches programmatic clearing by website JS)
   */
  function observeElement(el) {
    if (!el || !window.MutationObserver) return;
    if (activeObserver) activeObserver.disconnect();

    activeObserver = new MutationObserver((mutations) => {
      // Ignore mutations caused by our own indicator widget
      const isOurIndicator = mutations.every(m => {
        return Array.from(m.addedNodes).concat(Array.from(m.removedNodes)).every(n => {
          return n.id === '__auto_scribe_field_indicator' || (n.classList && n.classList.contains('__auto_scribe'));
        });
      });
      if (isOurIndicator) return;

      if (activeElement) {
        evaluateTextChange(activeElement);
      }
    });

    activeObserver.observe(el, {
      childList: true,
      subtree: true,
      characterData: true
    });
  }

  function getEffectiveUrl() {
    try {
      return (window.top && window.top.location.href) || window.location.href;
    } catch (e) {
      return window.location.href;
    }
  }

  function getEffectiveTitle() {
    try {
      return (window.top && window.top.document.title) || document.title || '';
    } catch (e) {
      return document.title || '';
    }
  }

  /**
   * Save draft snapshot to storage
   */
  function persistDraft(el, text, statusOverride = null) {
    if (!config.enabled) return;
    if (config.ignoredDomains && config.ignoredDomains.some(d => d && currentHost.includes(d.toLowerCase()))) {
      return;
    }
    if (!text || text.length < config.minChars) return;

    const draftId = getSessionId(el);
    lastActiveElement = el;
    lastActiveDraftId = draftId;

    const contextTitle = detectContext();
    const wordCount = text.split(/\s+/).filter(Boolean).length;
    const nowIso = new Date().toISOString();
    const isPosted = statusOverride === 'posted';

    const payload = {
      id: draftId,
      site: currentHost,
      url: getEffectiveUrl(),
      page_title: getEffectiveTitle(),
      context_title: contextTitle,
      text: text,
      char_count: text.length,
      word_count: wordCount,
      updated_at: nowIso,
      status: isPosted ? 'posted' : 'draft',
      posted_at: isPosted ? nowIso : undefined
    };

    lastSavedText = text;
    savedDraftMap.set(el, text);

    try {
      chrome.runtime.sendMessage({
        action: 'SAVE_DRAFT',
        payload: payload
      }, (res) => {
        if (chrome.runtime.lastError) return;
        if (res && res.id) {
          sessionKeyMap.set(el, res.id);
          lastActiveDraftId = res.id;
        }
        updateIndicator('saved', el);
      });
    } catch (err) {}
  }

  /**
   * Core evaluator: handles text changes, deletions, and post-submissions
   */
  function evaluateTextChange(target) {
    const root = getEditableRoot(target);
    if (!root || isSensitiveElement(root)) return;

    activeElement = root;
    lastActiveElement = root;

    const text = extractText(root);
    const draftId = getSessionId(root);
    const prevSaved = savedDraftMap.get(root) || '';

    if (text.length >= config.minChars) {
      currentWorkingTextMap.set(root, text);
      updateIndicator('saving', root);
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        persistDraft(root, text);
      }, config.debounceMs || 800);
    } else {
      // Text dropped below threshold or was cleared completely
      hideIndicator();
      clearTimeout(debounceTimer);

      const hadText = currentWorkingTextMap.get(root) || prevSaved || '';
      if (hadText && hadText.length >= config.minChars) {
        const isRecentSubmit = (activeEmptyCheck && activeEmptyCheck.did === draftId && !activeEmptyCheck.done) ||
                               submittedDrafts.has(draftId) ||
                               (Date.now() - lastSubmitTime < 2500);

        if (isRecentSubmit) {
          console.log('[Auto-Scribe] ✓ Submission confirmed on text drop:', draftId);
          if (activeEmptyCheck) activeEmptyCheck.done = true;
          const payload = {
            id: draftId,
            site: currentHost,
            url: window.location.href,
            page_title: document.title || '',
            context_title: detectContext(),
            text: hadText,
            char_count: hadText.length,
            word_count: hadText.split(/\s+/).filter(Boolean).length,
            updated_at: new Date().toISOString(),
            status: 'posted',
            posted_at: new Date().toISOString()
          };
          chrome.runtime.sendMessage({ action: 'SAVE_DRAFT', payload: payload });
          chrome.runtime.sendMessage({ action: 'MARK_DRAFT_POSTED', id: draftId, payload: payload });
          submittedDrafts.add(draftId);
        } else {
          console.log('[Auto-Scribe] ✗ Manual text deletion without submit. Deleting draft:', draftId);
          deleteSavedDraft(draftId);
        }
        currentWorkingTextMap.delete(root);
        savedDraftMap.delete(root);
        sessionKeyMap.delete(root); // Refresh session ID for any subsequent post in this box
      }
    }
  }

  /**
   * Helper: Check if element is inside a Canvas, document editor, or code workspace
   * (In canvases, Enter creates newlines/paragraphs, not post submissions)
   */
  function isCanvasOrDocEditor(el) {
    if (!el) return false;
    const tag = (el.tagName || '').toLowerCase();
    if (tag === 'textarea' || tag === 'input') return false;
    if (el.getAttribute && el.getAttribute('role') === 'textbox') return false;
    if (el.closest && el.closest('rich-textarea, #prompt-textarea, [data-testid*="prompt"], [data-testid*="chat-input"], .text-input-field')) {
      return false;
    }

    const target = el.closest ? el : el.parentElement;
    if (!target) return false;
    return !!target.closest(
      '[data-testid*="canvas-editor" i], [id*="canvas-editor" i], [class*="canvas-editor" i], ' +
      '.monaco-editor, .cm-editor, .CodeMirror, [data-testid*="code-editor"]'
    );
  }

  let activeEmptyCheck = null;
  let lastSubmitArmTime = 0;

  /**
   * Arms a check to observe if the active text box empties or unmounts after an Enter key or submit button click
   */
  function triggerPotentialSubmit(source, sourceTarget = null) {
    const now = Date.now();
    lastSubmitTime = now;

    const target = sourceTarget || activeElement || lastActiveElement;
    if (!target) return;

    // Never trigger submit clearance checks on a canvas/document editor!
    if (isCanvasOrDocEditor(target)) return;

    // Strictly check CURRENT text in the box or working text in memory
    const currentText = extractText(target) || currentWorkingTextMap.get(target) || '';
    if (!currentText || currentText.length < config.minChars) {
      return;
    }

    const did = getSessionId(target);
    if (!did) return;

    lastSubmitArmTime = now;

    // ATOMIC PRE-DISPATCH: Instantly save as 'posted' into background storage right now!
    // If the page redirects or clears immediately, the post is already 100% saved and marked posted.
    clearTimeout(debounceTimer);
    persistDraft(target, currentText, 'posted');
    submittedDrafts.add(did);

    activeEmptyCheck = {
      target: target,
      did: did,
      text: currentText,
      context: detectContext(),
      done: false
    };

    console.log(`[Auto-Scribe] 🎯 Instant POST buffered & dispatched for draft: ${did} (${currentText.length} chars from ${source}).`);

    const delays = [60, 150, 350, 700, 1200, 2000, 3500];
    delays.forEach(delay => {
      setTimeout(() => {
        if (!activeEmptyCheck || activeEmptyCheck.done || activeEmptyCheck.did !== did) return;

        const isUnmounted = !activeEmptyCheck.target || !document.contains(activeEmptyCheck.target);
        let remText = '';
        if (!isUnmounted) {
          remText = extractText(activeEmptyCheck.target);
        }

        const isCleared = isUnmounted || !remText || (remText.length < config.minChars && remText !== activeEmptyCheck.text);

        if (isCleared) {
          activeEmptyCheck.done = true;
          currentWorkingTextMap.delete(activeEmptyCheck.target);
          savedDraftMap.delete(activeEmptyCheck.target);
          sessionKeyMap.delete(activeEmptyCheck.target);

          if (!isUnmounted) {
            updateIndicator('saved', activeEmptyCheck.target);
          } else {
            hideIndicator();
          }
        }
      }, delay);
    });
  }

  /**
   * Helper: Check if click is on an actual submit/post/comment button
   */
  function isSubmitClick(e) {
    const path = e.composedPath ? e.composedPath() : [e.target];
    for (const node of path) {
      if (!node || node.nodeType !== 1) continue;

      const tag = node.tagName.toLowerCase();
      const role = (node.getAttribute('role') || '').toLowerCase();
      const type = (node.getAttribute('type') || '').toLowerCase();
      const slot = (node.getAttribute('slot') || '').toLowerCase();
      const testId = (node.getAttribute('data-testid') || '').toLowerCase();
      const aria = (node.getAttribute('aria-label') || '').toLowerCase();
      const title = (node.getAttribute('title') || '').toLowerCase();
      const className = (node.className || '').toString().toLowerCase();
      const text = (node.innerText || node.textContent || node.value || '').trim().toLowerCase();

      // Submit indicators
      if (slot === 'submit-button' || testId.includes('submit') || testId.includes('comment') || testId.includes('post')) {
        return true;
      }
      const submitRegex = /comment|post|reply|send|publish|tweet|submit|share|arrow_upward|save/i;
      if (submitRegex.test(aria) || submitRegex.test(title)) {
        return true;
      }
      const isButton = tag === 'button' || role === 'button' || type === 'submit';
      if (isButton) {
        if (/^(comment|post|reply|send|publish|submit|tweet|share|save)$/i.test(text)) {
          return true;
        }
        if (submitRegex.test(className) || node.id.includes('submit') || (node.name && node.name.includes('submit'))) {
          return true;
        }
        if (node.querySelector('svg, [data-icon*="send"], [class*="send"], [class*="submit"], [class*="post"]')) {
          return true;
        }
      }
    }
    return false;
  }

  /**
   * Flush on blur or visibility change
   */
  function handleFlush() {
    clearTimeout(debounceTimer);
    const target = activeElement || lastActiveElement;
    if (target) {
      const text = extractText(target);
      const prevSaved = savedDraftMap.get(target);
      if (text && text.length >= config.minChars && text !== prevSaved) {
        persistDraft(target, text);
      }
    }
  }

  // Event Listeners
  document.addEventListener('input', (e) => {
    const root = getEditableRoot(e.target);
    if (root && !isSensitiveElement(root)) {
      observeElement(root);
      evaluateTextChange(root);
    }
  }, true);

  document.addEventListener('keyup', (e) => {
    const root = getEditableRoot(e.target);
    if (root && !isSensitiveElement(root)) {
      evaluateTextChange(root);
    }
  }, true);

  document.addEventListener('compositionend', (e) => {
    const root = getEditableRoot(e.target);
    if (root && !isSensitiveElement(root)) {
      evaluateTextChange(root);
    }
  }, true);

  document.addEventListener('focusin', (e) => {
    const root = getEditableRoot(e.target);
    if (root && !isSensitiveElement(root)) {
      activeElement = root;
      lastActiveElement = root;
      observeElement(root);
    }
  }, true);

  // Single document-level submit listeners in capture phase
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      if (e.shiftKey) return; // Shift+Enter is newline
      if (isCanvasOrDocEditor(e.target)) return; // Canvas / document editors use Enter for newlines
      triggerPotentialSubmit('Enter-keydown', e.target);
    }
  }, true);

  document.addEventListener('click', (e) => {
    if (isSubmitClick(e)) {
      triggerPotentialSubmit('submit-button-click');
    }
  }, true);

  document.addEventListener('submit', (e) => {
    triggerPotentialSubmit('form-submit', e.target);
  }, true);

  document.addEventListener('blur', handleFlush, true);
  window.addEventListener('beforeunload', handleFlush);
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') handleFlush();
  });

  // -----------------------------------------------------------------
  // WYSIWYG Iframe Bridge (CKEditor, TinyMCE, Drupal wysiwyg-processed)
  // -----------------------------------------------------------------
  const bridgedDocs = new WeakSet();

  function attachToFrameDocument(frameDoc) {
    if (!frameDoc || bridgedDocs.has(frameDoc)) return;
    try {
      bridgedDocs.add(frameDoc);

      frameDoc.addEventListener('input', (e) => {
        const root = getEditableRoot(e.target) || frameDoc.body;
        if (root && !isSensitiveElement(root)) {
          observeElement(root);
          evaluateTextChange(root);
        }
      }, true);

      frameDoc.addEventListener('keyup', (e) => {
        const root = getEditableRoot(e.target) || frameDoc.body;
        if (root && !isSensitiveElement(root)) {
          evaluateTextChange(root);
        }
      }, true);

      frameDoc.addEventListener('focusin', (e) => {
        const root = getEditableRoot(e.target) || frameDoc.body;
        if (root && !isSensitiveElement(root)) {
          activeElement = root;
          lastActiveElement = root;
          observeElement(root);
        }
      }, true);

      frameDoc.addEventListener('blur', () => {
        handleFlush();
      }, true);
    } catch (err) {}
  }

  function scanAndBridgeWysiwygIframes() {
    const iframes = document.querySelectorAll('iframe.cke_wysiwyg_frame, iframe[class*="wysiwyg"], iframe[title*="Rich Text"], .cke_contents iframe');
    iframes.forEach(iframe => {
      try {
        const doc = iframe.contentDocument || (iframe.contentWindow && iframe.contentWindow.document);
        if (doc && (doc.readyState === 'complete' || doc.readyState === 'interactive' || doc.body)) {
          attachToFrameDocument(doc);
        } else {
          iframe.addEventListener('load', () => {
            try {
              const loadedDoc = iframe.contentDocument || (iframe.contentWindow && iframe.contentWindow.document);
              if (loadedDoc) attachToFrameDocument(loadedDoc);
            } catch (e) {}
          }, { once: true });
        }
      } catch (err) {}
    });
  }

  // Scan on start and watch for dynamically loaded editors
  scanAndBridgeWysiwygIframes();
  const wysiwygObserver = new MutationObserver(() => {
    scanAndBridgeWysiwygIframes();
  });
  wysiwygObserver.observe(document.documentElement || document.body, { childList: true, subtree: true });

  // -----------------------------------------------------------------
  // In-Input Status Indicator (Bottom-Left of active text entry box)
  // Simple icon: Circle when saving, Tick when saved
  // -----------------------------------------------------------------

  function ensureStyles() {
    if (document.getElementById('__auto_scribe_styles')) return;
    const style = document.createElement('style');
    style.id = '__auto_scribe_styles';
    style.textContent = `
      @keyframes scribe-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `;
    (document.head || document.documentElement).appendChild(style);
  }

  function ensureIndicator() {
    if (indicatorEl && document.contains(indicatorEl)) return indicatorEl;
    ensureStyles();

    const el = document.createElement('div');
    el.id = '__auto_scribe_field_indicator';
    el.title = 'Auto-Scribe';
    el.style.cssText = `
      position: fixed;
      z-index: 2147483647;
      display: none;
      align-items: center;
      justify-content: center;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: rgba(15, 23, 42, 0.88);
      border: 1px solid rgba(255, 255, 255, 0.18);
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.35);
      pointer-events: none;
      transition: opacity 0.3s ease;
      opacity: 0;
      user-select: none;
    `;
    (document.body || document.documentElement).appendChild(el);
    indicatorEl = el;
    return el;
  }

  const CIRCLE_SVG = `
    <svg width="11" height="11" viewBox="0 0 16 16" fill="none" style="display:block;">
      <circle cx="8" cy="8" r="5" stroke="#60a5fa" stroke-width="2.2" stroke-linecap="round" stroke-dasharray="24" stroke-dashoffset="6" style="animation: scribe-spin 0.85s linear infinite; transform-origin: center center;" />
    </svg>
  `;

  const TICK_SVG = `
    <svg width="11" height="11" viewBox="0 0 16 16" fill="none" style="display:block;">
      <path d="M3.5 8.5L6.5 11.5L12.5 4.5" stroke="#22c55e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  `;

  function positionIndicator(target) {
    if (!target) {
      hideIndicator();
      return;
    }
    // If target is inside an iframe document or is an iframe document body, position relative to the iframe in top window
    let elToMeasure = target;
    if (target.ownerDocument && target.ownerDocument !== document) {
      const parentIframe = Array.from(document.querySelectorAll('iframe')).find(f => {
        try {
          return f.contentDocument === target.ownerDocument;
        } catch (e) { return false; }
      });
      if (parentIframe) {
        elToMeasure = parentIframe;
      } else {
        hideIndicator();
        return;
      }
    }

    if (!document.contains(elToMeasure)) {
      hideIndicator();
      return;
    }
    const rect = elToMeasure.getBoundingClientRect();
    if (rect.width === 0 || rect.height === 0 || rect.bottom <= 0 || rect.top >= window.innerHeight) {
      hideIndicator();
      return;
    }

    const el = ensureIndicator();
    const size = 16;
    const paddingRight = 10;
    const paddingBottom = 6;

    let left = rect.right - size - paddingRight;
    let top;

    if (rect.height < 36) {
      top = rect.top + (rect.height - size) / 2;
    } else {
      top = rect.bottom - size - paddingBottom;
    }

    el.style.left = `${Math.round(left)}px`;
    el.style.top = `${Math.round(top)}px`;
  }

  function updateIndicator(state, target) {
    // Never show indicator inside sub-frames/iframes to prevent DOM reflow loops with WYSIWYG engines
    if (window !== window.top) {
      return;
    }
    if (!config.enabled || config.showIndicator === false) {
      hideIndicator();
      return;
    }

    const el = ensureIndicator();
    clearTimeout(fadeTimeout);

    positionIndicator(target || activeElement);

    if (state === 'saving') {
      el.innerHTML = CIRCLE_SVG;
      el.title = 'Auto-Scribe: Scribing...';
      el.style.display = 'flex';
      el.style.opacity = '1';
    } else if (state === 'saved') {
      el.innerHTML = TICK_SVG;
      el.title = 'Auto-Scribe: Saved ✓';
      el.style.display = 'flex';
      el.style.opacity = '1';

      // Softly fade out after 3.5 seconds of inactivity
      fadeTimeout = setTimeout(() => {
        if (indicatorEl) indicatorEl.style.opacity = '0';
      }, 3500);
    }
  }

  function hideIndicator() {
    clearTimeout(fadeTimeout);
    if (indicatorEl) {
      indicatorEl.style.display = 'none';
      indicatorEl.style.opacity = '0';
    }
  }

  // Smoothly track element position on scroll and resize
  window.addEventListener('scroll', () => {
    if (activeElement && indicatorEl && indicatorEl.style.display === 'flex') {
      positionIndicator(activeElement);
    }
  }, { passive: true, capture: true });

  window.addEventListener('resize', () => {
    if (activeElement && indicatorEl && indicatorEl.style.display === 'flex') {
      positionIndicator(activeElement);
    }
  }, { passive: true });
})();
