console.log("[Gemini LaTeX Exporter] Content script loaded on: " + window.location.href);

let lastClickedShareButton = null;

// Track the last clicked share/export button to identify the associated message later
document.addEventListener('mousedown', (event) => {
  const btn = event.target.closest('button, [role="button"]');
  if (btn) {
    const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
    const btnText = (btn.textContent || '').toLowerCase();
    const hasShareIcon = btn.querySelector('mat-icon, svg, .material-symbols') && 
                         (btn.innerHTML.includes('share') || btn.innerHTML.includes('export'));
    
    if (ariaLabel.includes('share') || ariaLabel.includes('export') || 
        btnText.includes('share') || btnText.includes('export') || hasShareIcon) {
      lastClickedShareButton = btn;
    }
  }
}, true);

// Watch for the popup menu to be appended to the body
const observer = new MutationObserver((mutations) => {
  for (const mutation of mutations) {
    for (const addedNode of mutation.addedNodes) {
      if (addedNode.nodeType === Node.ELEMENT_NODE) {
        checkForShareMenu(addedNode);
      }
    }
  }
});

observer.observe(document.body, { childList: true, subtree: true });

function checkForShareMenu(rootNode) {
  if (!rootNode || !rootNode.querySelectorAll) return;
  
  // Query all potential menu item wrappers
  const candidates = Array.from(rootNode.querySelectorAll('[role="menuitem"], button, a, li, .mat-mdc-menu-item, [role="button"]'));
  
  // Check the rootNode itself if it matches the role
  if (rootNode.matches && rootNode.matches('[role="menuitem"], button, a, li, .mat-mdc-menu-item, [role="button"]')) {
    candidates.push(rootNode);
  }
  
  for (const item of candidates) {
    const text = (item.textContent || '').trim();
    // Check if the item contains the exact words with loose spacing
    const normalizedText = text.replace(/\s+/g, ' ');
    if (normalizedText.includes('Export to Docs') && !normalizedText.includes('TeX')) {
      if (!item.parentNode.querySelector('.gemini-tex-exporter-btn')) {
        createTexExportBtn(item);
        break;
      }
    }
  }
}

function findTextNodeWithValue(root, value) {
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null, false);
  let node;
  while (node = walker.nextNode()) {
    if (node.nodeValue.includes(value)) {
      return node;
    }
  }
  return null;
}

function createTexExportBtn(exportItem) {
  const texItem = exportItem.cloneNode(true);
  texItem.classList.add('gemini-tex-exporter-btn');
  
  // Replace text in the cloned element
  const textNode = findTextNodeWithValue(texItem, 'Export to Docs');
  if (textNode) {
    textNode.textContent = 'Export to Docs (TeX)';
  } else {
    // Fallback search for text container
    const elements = Array.from(texItem.querySelectorAll('*'));
    let replaced = false;
    for (const el of [texItem, ...elements]) {
      if (el.children.length === 0 && el.textContent.trim().includes('Export to Docs')) {
        el.textContent = 'Export to Docs (TeX)';
        replaced = true;
        break;
      }
    }
    if (!replaced) {
      texItem.textContent = 'Export to Docs (TeX)';
    }
  }
  
  // Custom action on click
  texItem.addEventListener('click', async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    // Close the Google popup menu by clicking backdrop
    const backdrop = document.querySelector('.cdk-overlay-backdrop');
    if (backdrop) backdrop.click();
    
    await handleTeXExport();
  });
  
  // Insert the TeX option right below the original Export to Docs option
  exportItem.parentNode.insertBefore(texItem, exportItem.nextSibling);
}

// The open canvas, if there is one. Gemini renders it in a panel that is
// completely separate from the chat transcript:
//   immersive-panel > extended-response-panel > immersive-editor
//     > #extended-response-markdown-content > .ProseMirror
// Reading from here is what keeps Gemini's chat preamble ("I cannot directly
// create a canvas document for you, but...") out of the exported doc — that
// sentence lives in the chat message, never in the canvas.
function findCanvasContent() {
  const panel = document.querySelector('immersive-panel');
  if (!panel || panel.offsetParent === null) return null;

  return panel.querySelector('#extended-response-markdown-content .ProseMirror')
      || panel.querySelector('#extended-response-markdown-content')
      || panel.querySelector('.ProseMirror[aria-label="Canvas editor"]');
}

// Canvas titles itself in the panel toolbar; much better than a date stamp.
function findCanvasTitle() {
  const panel = document.querySelector('immersive-panel');
  if (!panel) return null;
  const heading = panel.querySelector('toolbar h2.title-text, .toolbar h2');
  const title = heading && heading.textContent.trim();
  return title || null;
}

function findAssociatedMessageContent(button) {
  if (!button) return null;

  // Walk up to find the common wrapper, then look for message-content
  let parent = button.parentElement;
  while (parent && parent !== document.body) {
    const msgContent = parent.querySelector('message-content');
    if (msgContent) {
      return msgContent;
    }
    parent = parent.parentElement;
  }
  
  // Fallback: Return the last message-content on the page
  const allMessages = document.querySelectorAll('message-content');
  if (allMessages.length > 0) {
    return allMessages[allMessages.length - 1];
  }
  return null;
}

// Pull the LaTeX source out of a rendered math node.
// Order matters — most reliable source first:
//   1. data-math  : the canvas keeps verbatim LaTeX here on <math-block>/<math-inline>
//   2. .math-src  : only populated while the node has focus, so usually empty
//   3. annotation / alttext : the MathML paths, absent from the canvas because
//      it runs KaTeX in HTML-only output mode (no .katex-mathml is emitted)
function extractTeX(el) {
  const data = el.getAttribute && el.getAttribute('data-math');
  if (data && data.trim()) return data.trim();

  const src = el.querySelector('.math-src');
  if (src && src.textContent.trim()) return src.textContent.trim();

  const annotation = el.querySelector('annotation[encoding="application/x-tex"]');
  if (annotation && annotation.textContent.trim()) return annotation.textContent.trim();

  const math = el.querySelector('math[alttext]');
  if (math && math.getAttribute('alttext').trim()) return math.getAttribute('alttext').trim();

  return null;
}

// Display math becomes its own monospace paragraph. A bare text node would not
// work: the \n we used to emit collapses to a space in HTML, so the equation
// ran into the surrounding prose once Docs imported it.
function makeBlockTeX(tex) {
  const p = document.createElement('p');
  p.style.fontFamily = "'Courier New', monospace";
  p.textContent = `$$${tex}$$`;
  return p;
}

function replaceKaTeX(root) {
  // 0. Canvas math nodes. These wrap the KaTeX spans, so they must be handled
  //    before the legacy passes below or we would strip their contents first.
  root.querySelectorAll('math-block, math-inline').forEach(node => {
    const tex = extractTeX(node);
    if (!tex) return;

    const isBlock = node.tagName.toLowerCase() === 'math-block'
                 || !!node.querySelector('.katex-display');
    const replacement = isBlock
      ? makeBlockTeX(tex)
      : document.createTextNode(` $${tex}$ `);
    node.parentNode.replaceChild(replacement, node);
  });

  // 1. Bare KaTeX display blocks (chat transcript, or any canvas node that
  //    was not wrapped in a math-block).
  root.querySelectorAll('.katex-display').forEach(display => {
    const tex = extractTeX(display);
    if (tex) display.parentNode.replaceChild(makeBlockTeX(tex), display);
  });

  // 2. Bare inline KaTeX.
  let unresolved = 0;
  root.querySelectorAll('.katex').forEach(inline => {
    if (!inline.parentNode) return; // Already removed by a display replacement

    const tex = extractTeX(inline);
    if (tex) {
      inline.parentNode.replaceChild(document.createTextNode(` $${tex}$ `), inline);
    } else {
      // Nothing left to recover the source from; the rendered glyphs will be
      // exported as Unicode. Worth knowing about rather than failing silently.
      unresolved++;
    }
  });

  if (unresolved) {
    console.warn(`[Gemini LaTeX Exporter] ${unresolved} math element(s) had no recoverable LaTeX source; exported as rendered text.`);
  }
}

async function handleTeXExport() {
  // Prefer the canvas: it holds the document itself, with none of the
  // conversational framing Gemini wraps around it in the chat transcript.
  const fromCanvas = findCanvasContent();
  const msgContent = fromCanvas || findAssociatedMessageContent(lastClickedShareButton);

  if (!msgContent) {
    showToast("Could not locate response content.", "error");
    return;
  }
  console.log(`[Gemini LaTeX Exporter] Source: ${fromCanvas ? 'canvas' : 'chat message'}`);

  showToast("Preparing document...", "info");

  // Clone content to leave the UI untouched
  const clone = msgContent.cloneNode(true);
  
  // Process LaTeX elements
  replaceKaTeX(clone);
  
  // Clean up code block copy/action buttons
  const copyButtons = clone.querySelectorAll('pre button, pre .copy-code-button, button, [role="button"]');
  copyButtons.forEach(btn => btn.remove());
  
  // Format code block headers into clean text
  const codeHeaders = clone.querySelectorAll('.code-block-header');
  codeHeaders.forEach(header => {
    const langSpan = header.querySelector('span');
    if (langSpan) {
      const langText = langSpan.textContent.trim();
      const bold = document.createElement('strong');
      bold.style.display = 'block';
      bold.style.marginTop = '1em';
      bold.textContent = `[Code: ${langText}]`;
      header.parentNode.insertBefore(bold, header);
    }
    header.remove();
  });
  
  const htmlContent = clone.innerHTML;

  // Name the doc after the canvas when we can; fall back to a date stamp.
  const docTitle = findCanvasTitle() || `Gemini LaTeX Export - ${new Date().toLocaleDateString()}`;

  showToast("Exporting to Google Docs...", "info");
  
  chrome.runtime.sendMessage({
    action: "createDoc",
    title: docTitle,
    html: htmlContent
  }, (response) => {
    dismissToast();
    if (response && response.success) {
      showToast("Export successful!", "success");
    } else {
      const errMsg = response ? response.error : "Unknown error occurred.";
      showToast("Export failed: " + errMsg, "error");
    }
  });
}

function showToast(message, type = "info") {
  const existing = document.querySelector('.gemini-tex-toast');
  if (existing) existing.remove();
  
  const toast = document.createElement('div');
  toast.className = `gemini-tex-toast gemini-tex-toast-${type}`;
  toast.innerHTML = `
    <div class="gemini-tex-toast-content">
      <span class="gemini-tex-toast-icon">${
        type === 'success' ? '✅' : type === 'error' ? '❌' : '⏳'
      }</span>
      <span class="gemini-tex-toast-text">${message}</span>
    </div>
  `;
  document.body.appendChild(toast);
  
  // Force a reflow to trigger transition
  toast.offsetHeight;
  toast.classList.add('gemini-tex-toast-show');
  
  if (type !== 'info') {
    setTimeout(() => {
      dismissToast();
    }, 4000);
  }
}

function dismissToast() {
  const toast = document.querySelector('.gemini-tex-toast');
  if (toast) {
    toast.classList.remove('gemini-tex-toast-show');
    toast.addEventListener('transitionend', () => {
      toast.remove();
    }, { once: true });
  }
}
