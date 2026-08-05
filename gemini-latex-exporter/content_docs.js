console.log("[Gemini LaTeX Exporter] Docs content script loaded!");

// Check if this Google Doc was opened by the Gemini LaTeX Exporter
chrome.storage.local.get('pendingPaste').then((data) => {
  if (data.pendingPaste) {
    // Clear state immediately to prevent duplicate runs
    chrome.storage.local.remove('pendingPaste');
    
    // Wait for the document UI to load before displaying the helper
    const checkInterval = setInterval(() => {
      const docsEditor = document.getElementById('docs-editor') || 
                         document.querySelector('.docs-texteventtarget-iframe') ||
                         document.getElementById('docs-editor-container');
      if (docsEditor) {
        clearInterval(checkInterval);
        showPasteBanner();
        tryFocusEditor();
      }
    }, 200);
    
    // Safety timeout after 10 seconds to stop polling if Docs fails to load
    setTimeout(() => {
      clearInterval(checkInterval);
    }, 10000);
  }
});

function tryFocusEditor() {
  // Attempt to focus the editor frame to make pasting immediate
  const iframe = document.querySelector('iframe.docs-texteventtarget-iframe');
  if (iframe) {
    iframe.focus();
    if (iframe.contentWindow) {
      iframe.contentWindow.focus();
    }
  } else {
    const activeEl = document.activeElement;
    if (activeEl) activeEl.focus();
  }
}

function showPasteBanner() {
  // Ensure we don't display duplicate banners
  if (document.querySelector('.gemini-tex-banner')) return;

  const banner = document.createElement('div');
  banner.className = 'gemini-tex-banner';
  banner.innerHTML = `
    <div class="gemini-tex-banner-content">
      <span class="gemini-tex-banner-icon">📋</span>
      <span class="gemini-tex-banner-text">
        <strong>LaTeX Document Ready!</strong> Focus the document and press <strong>Ctrl+V</strong> (or <strong>Cmd+V</strong>) to paste.
      </span>
      <button class="gemini-tex-banner-close" aria-label="Close message">&times;</button>
    </div>
  `;
  
  document.body.appendChild(banner);
  
  // Transition in after appending to trigger CSS transition
  setTimeout(() => {
    banner.classList.add('gemini-tex-banner-show');
  }, 50);

  // Close button click handler
  banner.querySelector('.gemini-tex-banner-close').addEventListener('click', () => {
    dismissBanner();
  });
  
  // Auto-dismiss on paste key combination
  const handleKeyDown = (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'v') {
      setTimeout(dismissBanner, 1000); // Wait a second for paste rendering
      window.removeEventListener('keydown', handleKeyDown);
    }
  };
  window.addEventListener('keydown', handleKeyDown);
  
  // Auto-dismiss after 15 seconds if untouched
  setTimeout(dismissBanner, 15000);
}

function dismissBanner() {
  const banner = document.querySelector('.gemini-tex-banner');
  if (banner) {
    banner.classList.remove('gemini-tex-banner-show');
    banner.classList.add('gemini-tex-banner-hide');
    banner.addEventListener('transitionend', () => {
      banner.remove();
    }, { once: true });
  }
}
