console.log("[Gemini LaTeX Exporter] Content script loaded on: " + window.location.href);

let lastClickedShareButton = null;

// Track the last clicked share/export or conversation actions button
document.addEventListener('mousedown', (event) => {
  const btn = event.target.closest('button, [role="button"]');
  if (btn) {
    const ariaLabel = (btn.getAttribute('aria-label') || '').toLowerCase();
    const btnText = (btn.textContent || '').toLowerCase();
    const hasShareIcon = btn.querySelector('mat-icon, svg, .material-symbols') && 
                         (btn.innerHTML.includes('share') || btn.innerHTML.includes('export'));
    
    const isShareOrExport = ariaLabel.includes('share') || ariaLabel.includes('export') || 
                            btnText.includes('share') || btnText.includes('export') || hasShareIcon;
                            
    const isConversationMenu = ariaLabel.includes('conversation');
    
    if (isShareOrExport || isConversationMenu) {
      lastClickedShareButton = btn;
    } else {
      lastClickedShareButton = null;
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
  if (!lastClickedShareButton) return;
  
  const triggerLabel = (lastClickedShareButton.getAttribute('aria-label') || '').toLowerCase();
  
  if (triggerLabel.includes('conversation')) {
    // Inject "Download Chat as MD" into the conversation actions menu
    const candidates = Array.from(rootNode.querySelectorAll('[role="menuitem"], button, a, li, .mat-mdc-menu-item, [role="button"]'));
    if (rootNode.matches && rootNode.matches('[role="menuitem"], button, a, li, .mat-mdc-menu-item, [role="button"]')) {
      candidates.push(rootNode);
    }
    
    const itemToClone = candidates.find(el => {
      const txt = el.textContent.toLowerCase();
      return txt.includes('delete') || txt.includes('rename') || txt.includes('pin') || el.getAttribute('role') === 'menuitem';
    }) || candidates[0];
    
    if (itemToClone && !itemToClone.parentNode.querySelector('.gemini-chat-md-exporter-btn')) {
      const text = itemToClone.textContent.trim();
      let searchLabel = text;
      if (text.includes('Delete')) searchLabel = 'Delete';
      else if (text.includes('Rename')) searchLabel = 'Rename';
      else if (text.includes('Pin')) searchLabel = 'Pin';
      
      const chatMdBtn = createButtonHelper(itemToClone, searchLabel, 'Download Chat as MD', 'gemini-chat-md-exporter-btn', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        const backdrop = document.querySelector('.cdk-overlay-backdrop');
        if (backdrop) backdrop.click();
        await handleChatExport();
      });
      
      itemToClone.parentNode.appendChild(chatMdBtn);
    }
    return;
  }
  
  // Query all potential share menu item wrappers
  const candidates = Array.from(rootNode.querySelectorAll('[role="menuitem"], button, a, li, .mat-mdc-menu-item, [role="button"]'));
  if (rootNode.matches && rootNode.matches('[role="menuitem"], button, a, li, .mat-mdc-menu-item, [role="button"]')) {
    candidates.push(rootNode);
  }
  
  for (const item of candidates) {
    const text = (item.textContent || '').trim();
    const normalizedText = text.replace(/\s+/g, ' ');
    if (normalizedText.includes('Export to Docs') && !normalizedText.includes('TeX')) {
      if (!item.parentNode.querySelector('.gemini-tex-exporter-btn')) {
        createTexExportBtns(item);
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

function createButtonHelper(templateItem, searchLabel, textLabel, className, onClick) {
  const btn = templateItem.cloneNode(true);
  btn.classList.add(className);
  
  const textNode = findTextNodeWithValue(btn, searchLabel);
  if (textNode) {
    textNode.nodeValue = textNode.nodeValue.replace(searchLabel, textLabel);
  } else {
    // Fallback search in elements
    const elements = Array.from(btn.querySelectorAll('*'));
    let replaced = false;
    for (const el of [btn, ...elements]) {
      if (el.children.length === 0 && el.textContent.trim().includes(searchLabel)) {
        el.textContent = el.textContent.replace(searchLabel, textLabel);
        replaced = true;
        break;
      }
    }
    if (!replaced) {
      btn.textContent = textLabel;
    }
  }
  
  btn.addEventListener('click', onClick);
  return btn;
}

function createTexExportBtns(exportItem) {
  // Create Export to Docs (TeX) button
  const texBtn = createButtonHelper(exportItem, 'Export to Docs', 'Export to Docs (TeX)', 'gemini-tex-exporter-btn', async (e) => {
    e.preventDefault();
    e.stopPropagation();
    const backdrop = document.querySelector('.cdk-overlay-backdrop');
    if (backdrop) backdrop.click();
    await handleTeXExport();
  });

  // Create Download as MD (TeX) button
  const mdBtn = createButtonHelper(exportItem, 'Export to Docs', 'Download as MD (TeX)', 'gemini-tex-md-btn', async (e) => {
    e.preventDefault();
    e.stopPropagation();
    const backdrop = document.querySelector('.cdk-overlay-backdrop');
    if (backdrop) backdrop.click();
    await handleMdExport();
  });

  // Insert both right below the original Export to Docs button
  exportItem.parentNode.insertBefore(mdBtn, exportItem.nextSibling);
  exportItem.parentNode.insertBefore(texBtn, exportItem.nextSibling);
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
//   1. data-math/data-tex/data-latex on element or any ancestor wrapper
//   2. .math-src  : only populated while the node has focus, so usually empty
//   3. annotation / alttext : the MathML paths
function extractTeX(el) {
  if (!el) return null;

  // 1. Search data attributes on the element and its ancestors (up to root/body)
  let current = el;
  while (current && current.nodeType === Node.ELEMENT_NODE) {
    const dataMath = current.getAttribute('data-math');
    if (dataMath && dataMath.trim()) return dataMath.trim();

    const dataTex = current.getAttribute('data-tex') || current.getAttribute('data-latex') || current.getAttribute('data-latex-source');
    if (dataTex && dataTex.trim()) return dataTex.trim();

    // Check title if it looks like LaTeX code
    const title = current.getAttribute('title');
    if (title && title.trim() && (title.includes('\\') || title.includes('_') || title.includes('^'))) {
      return title.trim();
    }

    current = current.parentNode;
  }

  // 2. Search children for text source elements
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
  if (!root) return;

  // 0. Canvas/Transcript custom math nodes. These wrap the KaTeX spans, so they must be handled
  //    before the legacy passes below or we would strip their contents first.
  root.querySelectorAll('math-block, math-inline').forEach(node => {
    if (!node.parentNode) return;
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
    if (!display.parentNode) return;
    const tex = extractTeX(display);
    if (tex) {
      display.parentNode.replaceChild(makeBlockTeX(tex), display);
    }
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

async function handleMdExport() {
  const fromCanvas = findCanvasContent();
  const msgContent = fromCanvas || findAssociatedMessageContent(lastClickedShareButton);

  if (!msgContent) {
    showToast("Could not locate response content.", "error");
    return;
  }
  console.log(`[Gemini LaTeX Exporter] MD Source: ${fromCanvas ? 'canvas' : 'chat message'}`);

  showToast("Converting to Markdown...", "info");

  try {
    const markdown = htmlToMarkdown(msgContent);

    // Document Title
    const title = findCanvasTitle() || `Gemini Export - ${new Date().toLocaleDateString()}`;
    const filename = `${title.toLowerCase().replace(/[^a-z0-9]+/g, '-')}.md`;

    // Trigger download
    const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();

    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 150);

    dismissToast();
    showToast("Markdown downloaded!", "success");
  } catch (err) {
    console.error("Markdown export failed:", err);
    dismissToast();
    showToast("Export failed: " + err.message, "error");
  }
}

function htmlToMarkdown(element) {
  const clone = element.cloneNode(true);
  replaceKaTeX(clone);
  
  // Clean up code block headers and add attributes for pre-formatting
  const codeHeaders = clone.querySelectorAll('.code-block-header');
  codeHeaders.forEach(header => {
    const langSpan = header.querySelector('span');
    const langText = langSpan ? langSpan.textContent.trim() : '';
    const pre = header.nextElementSibling;
    if (pre && pre.tagName === 'PRE') {
      pre.setAttribute('data-language', langText);
    }
    header.remove();
  });

  function processNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      return node.nodeValue;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) {
      return '';
    }

    let childrenVal = '';
    node.childNodes.forEach(child => {
      childrenVal += processNode(child);
    });

    const tagName = node.tagName;
    switch (tagName) {
      case 'H1':
        return `\n\n# ${childrenVal.trim()}\n\n`;
      case 'H2':
        return `\n\n## ${childrenVal.trim()}\n\n`;
      case 'H3':
        return `\n\n### ${childrenVal.trim()}\n\n`;
      case 'H4':
        return `\n\n#### ${childrenVal.trim()}\n\n`;
      case 'P':
        return `\n\n${childrenVal.trim()}\n\n`;
      case 'STRONG':
      case 'B':
        return `**${childrenVal.trim()}**`;
      case 'EM':
      case 'I':
        return `*${childrenVal.trim()}*`;
      case 'CODE':
        if (node.parentNode && node.parentNode.tagName === 'PRE') {
          return childrenVal;
        }
        return `\`${childrenVal.trim()}\``;
      case 'PRE':
        const lang = node.getAttribute('data-language') || '';
        // Remove code block action buttons inside pre
        const copyBtns = node.querySelectorAll('button, .copy-code-button');
        copyBtns.forEach(b => b.remove());
        const codeText = node.textContent.trim();
        return `\n\n\`\`\`${lang}\n${codeText}\n\`\`\`\n\n`;
      case 'UL':
        return `\n${childrenVal}\n`;
      case 'OL':
        return `\n${childrenVal}\n`;
      case 'LI':
        const parent = node.parentNode ? node.parentNode.tagName : '';
        if (parent === 'OL') {
          const siblings = Array.from(node.parentNode.children);
          const idx = siblings.indexOf(node) + 1;
          return `${idx}. ${childrenVal.trim()}\n`;
        }
        return `* ${childrenVal.trim()}\n`;
      case 'BR':
        return '\n';
      case 'A':
        const href = node.getAttribute('href') || '';
        return `[${childrenVal.trim()}](${href})`;
      case 'TABLE':
        return `\n\n${renderTableToMarkdown(node)}\n\n`;
      default:
        // Use window.getComputedStyle to detect block divs/spans
        const display = window.getComputedStyle(node).display;
        if (display === 'block') {
          return `\n${childrenVal}\n`;
        }
        return childrenVal;
    }
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

      if (rowIndex === 0 && row.querySelector('th')) {
        let separator = '|';
        cells.forEach(() => {
          separator += ' --- |';
        });
        md += separator + '\n';
      }
    });
    return md;
  }

  let markdown = processNode(clone);
  
  // Clean up duplicate whitespaces and lines
  markdown = markdown
    .replace(/\n{3,}/g, '\n\n')
    .trim();
    
  return markdown;
}

async function handleChatExport() {
  showToast("Compiling chat transcript...", "info");
  
  try {
    const containers = Array.from(document.querySelectorAll('.conversation-container'));
    if (containers.length === 0) {
      showToast("No chat transcript found.", "error");
      return;
    }
    
    let markdown = `# Gemini Chat Export - ${new Date().toLocaleDateString()}\n\n`;
    
    containers.forEach((container, index) => {
      // Extract user query
      const queryEl = container.querySelector('.query-text');
      if (queryEl) {
        let queryText = queryEl.textContent.replace(/\s+/g, ' ').trim();
        // Remove Screen Reader label
        if (queryText.startsWith('You said')) {
          queryText = queryText.substring('You said'.length).trim();
        }
        markdown += `### User:\n${queryText}\n\n`;
      }
      
      // Extract Gemini response
      const msgContent = container.querySelector('message-content');
      if (msgContent) {
        const responseMd = htmlToMarkdown(msgContent);
        markdown += `### Gemini:\n${responseMd}\n\n`;
      }
      
      if (index < containers.length - 1) {
        markdown += `---\n\n`;
      }
    });
    
    // Document Title
    const firstQuery = containers[0].querySelector('.query-text');
    let title = "gemini-chat-export";
    if (firstQuery) {
      let firstQueryText = firstQuery.textContent.replace(/\s+/g, ' ').trim();
      if (firstQueryText.startsWith('You said')) {
        firstQueryText = firstQueryText.substring('You said'.length).trim();
      }
      title = firstQueryText.toLowerCase().replace(/[^a-z0-9]+/g, '-').substring(0, 30);
    }
    
    const filename = `${title}-chat.md`;
    const blob = new Blob([markdown], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 150);
    
    dismissToast();
    showToast("Chat downloaded!", "success");
  } catch (err) {
    console.error("Chat export failed:", err);
    dismissToast();
    showToast("Export failed: " + err.message, "error");
  }
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
