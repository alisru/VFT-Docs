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

function replaceKaTeX(root) {
  // 1. Replace display math blocks first (block equations)
  const displays = root.querySelectorAll('.katex-display');
  displays.forEach(display => {
    const annotation = display.querySelector('annotation[encoding="application/x-tex"]');
    if (annotation) {
      const tex = annotation.textContent.trim();
      const textNode = document.createTextNode(`\n$$\n${tex}\n$$\n`);
      display.parentNode.replaceChild(textNode, display);
    } else {
      const math = display.querySelector('math');
      if (math && math.getAttribute('alttext')) {
        const tex = math.getAttribute('alttext').trim();
        const textNode = document.createTextNode(`\n$$\n${tex}\n$$\n`);
        display.parentNode.replaceChild(textNode, display);
      }
    }
  });

  // 2. Replace inline math elements
  const inlines = root.querySelectorAll('.katex');
  inlines.forEach(inline => {
    if (!inline.parentNode) return; // Already removed by a display block replacement
    
    const annotation = inline.querySelector('annotation[encoding="application/x-tex"]');
    if (annotation) {
      const tex = annotation.textContent.trim();
      const textNode = document.createTextNode(` $${tex}$ `);
      inline.parentNode.replaceChild(textNode, inline);
    } else {
      const math = inline.querySelector('math');
      if (math && math.getAttribute('alttext')) {
        const tex = math.getAttribute('alttext').trim();
        const textNode = document.createTextNode(` $${tex}$ `);
        inline.parentNode.replaceChild(textNode, inline);
      }
    }
  });
}

async function handleTeXExport() {
  const msgContent = findAssociatedMessageContent(lastClickedShareButton);
  if (!msgContent) {
    showToast("Could not locate response content.", "error");
    return;
  }
  
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
  
  // Generate a friendly document title using current date
  const dateStr = new Date().toLocaleDateString();
  const docTitle = `Gemini LaTeX Export - ${dateStr}`;
  
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
