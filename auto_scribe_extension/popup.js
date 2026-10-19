document.addEventListener('DOMContentLoaded', async () => {
  const statDrafts = document.getElementById('stat-drafts');
  const statPosted = document.getElementById('stat-posted');
  const toggleEnabled = document.getElementById('toggle-enabled');
  const recentList = document.getElementById('recent-list');
  const btnDashboard = document.getElementById('btn-dashboard');
  const statusBadge = document.getElementById('status-badge');

  // Open Dashboard handler
  btnDashboard.onclick = () => {
    chrome.tabs.create({ url: chrome.runtime.getURL('dashboard.html') });
    window.close();
  };

  // Load Settings
  chrome.runtime.sendMessage({ action: 'GET_SETTINGS' }, (res) => {
    if (chrome.runtime.lastError || !res || !res.settings) return;
    toggleEnabled.checked = res.settings.enabled !== false;
    updateStatusBadge(toggleEnabled.checked);
  });

  // Toggle handler
  toggleEnabled.onchange = () => {
    const isEnabled = toggleEnabled.checked;
    updateStatusBadge(isEnabled);
    chrome.runtime.sendMessage({
      action: 'SAVE_SETTINGS',
      settings: { enabled: isEnabled }
    });
  };

  function updateStatusBadge(active) {
    if (active) {
      statusBadge.textContent = 'Active';
      statusBadge.style.color = '#22c55e';
      statusBadge.style.background = 'rgba(34, 197, 94, 0.15)';
    } else {
      statusBadge.textContent = 'Paused';
      statusBadge.style.color = '#f59e0b';
      statusBadge.style.background = 'rgba(245, 158, 11, 0.15)';
    }
  }

  function loadDrafts() {
    chrome.runtime.sendMessage({ action: 'GET_DRAFTS' }, (res) => {
      if (chrome.runtime.lastError || !res || !res.drafts) {
        recentList.innerHTML = '<div style="color:#64748b;font-size:12px;text-align:center;padding:12px;">No drafts found.</div>';
        return;
      }

      const drafts = res.drafts || [];
      const unposted = drafts.filter(d => d && d.status !== 'posted');
      const posted = drafts.filter(d => d && d.status === 'posted');

      if (statDrafts) statDrafts.textContent = unposted.length;
      if (statPosted) statPosted.textContent = posted.length;

      if (unposted.length === 0) {
        recentList.innerHTML = `
          <div style="color:#22c55e;font-size:12px;text-align:center;padding:16px 8px;line-height:1.5;">
            ✓ No unposted drafts<br>
            <span style="color:#64748b;font-size:11px;">All drafts have been posted or cleared.</span>
          </div>`;
        return;
      }

      recentList.innerHTML = '';
      unposted.slice(0, 4).forEach(d => {
        const item = document.createElement('div');
        item.className = 'recent-item';

        const title = d.context_title || d.page_title || 'Untitled Draft';
        const preview = d.text ? d.text.slice(0, 80) + (d.text.length > 80 ? '...' : '') : '';
        const siteTag = d.site || 'web';

        item.innerHTML = `
          <div class="recent-top">
            <span class="recent-title" title="${escapeHtml(title)}">${escapeHtml(title)}</span>
            <span style="color:#38bdf8;font-size:10px;font-weight:600;">${escapeHtml(siteTag)}</span>
          </div>
          <div class="recent-preview">${escapeHtml(preview)}</div>
        `;

        item.style.cursor = 'pointer';
        item.onclick = () => {
          navigator.clipboard.writeText(d.text).then(() => {
            const oldTitle = item.querySelector('.recent-title').textContent;
            item.querySelector('.recent-title').textContent = 'Copied to Clipboard! ✓';
            item.querySelector('.recent-title').style.color = '#4ade80';
            setTimeout(() => {
              item.querySelector('.recent-title').textContent = oldTitle;
              item.querySelector('.recent-title').style.color = '';
            }, 1500);
          });
        };

        recentList.appendChild(item);
      });
    });
  }

  // Initial load
  loadDrafts();

  // Real-time storage listener
  chrome.storage.onChanged.addListener((changes, areaName) => {
    if (areaName === 'local' && changes.scribe_drafts) {
      loadDrafts();
    }
  });

  function escapeHtml(str) {
    return (str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
});
