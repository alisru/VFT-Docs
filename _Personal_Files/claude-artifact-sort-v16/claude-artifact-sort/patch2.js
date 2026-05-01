const fs = require('fs');

let text = fs.readFileSync('content.js', 'utf8');

const OLD_BLOCK = `    // Load first-seen timestamps for display
    storageGet('cas_first_seen').then(seen => {
      storageGet('cas_summaries').then(summaries => {
        for (const [source, groupItems] of Object.entries(groups)) {
          if (groupItems.length === 0) continue;
          const meta = sourceMeta[source];

          const header = document.createElement('div');
          header.className = 'cas-group-header';
          header.innerHTML = \\\`<span style="color:\\\${meta.color}">\\\${meta.icon} \\\${meta.label}</span><span class="cas-group-count">\\\${groupItems.length}</span>\\\`;
          list.appendChild(header);

          groupItems.forEach((item, i) => {
            const { data } = item;
            const row = document.createElement('div');
            row.className = 'cas-row';
            row.style.flexDirection = 'column';
            row.style.alignItems = 'flex-start';
            row.style.position = 'relative';

            const badge = data.type
              ? \\\`<span class="cas-badge cas-type-\\\${data.type.toLowerCase()}">\\\${data.type}</span>\\\`
              : '<span class="cas-badge cas-type-unknown">?</span>';
            const ts = seen[data.name] || '';
            const summary = summaries[data.name] || '';

            // ◈ NAVIGATION UI
            row.innerHTML = \\\`
            <div style="display:flex;align-items:center;gap:5px;width:100%">
              <span class="cas-index">\\\${i + 1}</span>

              \\\${badge}
              <span class="cas-name" title="Double-click to open • Single-click to find\\n\\\${data.name || ''}" style="flex:1; cursor:pointer;">\\\${(data.name || 'unknown').slice(0, 24)}</span>
              \\\${ts ? \\\`<span class="cas-meta">\\\${ts}</span>\\\` : ''}
              <button class="cas-jump-btn" title="Jump to point in chat" style="background:none;border:none;color:#fff;cursor:pointer;font-size:12px;padding:0 4px;margin-left:auto;transition:color 0.2s;text-shadow:0 0 2px rgba(255,255,255,0.3)">⟢</button>
            </div>
            \\\${summary ? \\\`<div style="font-size:9px;color:#666;padding:2px 0 0 20px;line-height:1.3">\\\${summary}</div>\\\` : ''}
          \\\`;

            // Single click: highlights and scrolls
            row.addEventListener('click', (e) => {
              if (e.target.closest('.cas-jump-btn')) return;
              highlightNode(item.node, item.isSidebar ? 'sidebar' : 'chat');
            });

            // Double click: Opens the artifact in the sidebar
            row.addEventListener('dblclick', (e) => {
              if (e.target.closest('.cas-jump-btn')) return;
              if (item.node) item.node.click();
            });

            // Clicking the Jump button specifically scrolls to chat flow
            row.querySelector('.cas-jump-btn').addEventListener('click', (e) => {
              e.stopPropagation();
              jumpToArtifact(data.name);
            });

            list.appendChild(row);
          });
        }
      });
    });`;

const NEW_BLOCK = `    // Load multiple metadata sources for display
    Promise.all([
      storageGet('cas_first_seen'),
      storageGet('cas_summaries'),
      storageGet('cas_tags'),
      storageGet('cas_versions'),
      storageGet('cas_downloads')
    ]).then(([seen, summaries, tagsMap, versionsMap, dlsMap]) => {
      for (const [source, groupItems] of Object.entries(groups)) {
        if (groupItems.length === 0) continue;
        const meta = sourceMeta[source] || { label: 'Local', color: '#ccc', icon: '♢' };

        const header = document.createElement('div');
        header.className = 'cas-group-header';
        header.innerHTML = \\\`<span style="color:\\\${meta.color}">\\\${meta.icon} \\\${meta.label}</span><span class="cas-group-count">\\\${groupItems.length}</span>\\\`;
        list.appendChild(header);

        groupItems.forEach((item, i) => {
          const { data } = item;
          const row = document.createElement('div');
          row.className = 'cas-row';
          row.style.flexDirection = 'column';
          row.style.alignItems = 'flex-start';
          row.style.position = 'relative';

          const badge = data.type
            ? \\\`<span class="cas-badge cas-type-\\\${data.type.toLowerCase()}">\\\${data.type}</span>\\\`
            : '<span class="cas-badge cas-type-unknown">?</span>';
          const ts = seen[data.name] || '';
          const summary = summaries[data.name] || '';
          
          const vData = versionsMap[data.name];
          const versionBadge = vData && vData.version > 1 
            ? \\\`<span title="Updated \\\${vData.lastUpdated}" style="background:#2a2e36;color:#c8cdd6;border-radius:3px;padding:1px 4px;font-size:7px;margin-left:4px;border:1px solid #444;">v\\\${vData.version}</span>\\\` 
            : '';
            
          const dlData = dlsMap[data.name];
          const dlBadge = dlData && dlData.count > 0 
            ? \\\`<span title="Downloaded \\\${dlData.count} times. Last version dl: v\\\${dlData.lastVersion}" style="background:#1e2a22;color:#6bcf6b;border-radius:3px;padding:1px 4px;font-size:7px;margin-left:4px;border:1px solid #285030;">⭳ \\\${dlData.count}</span>\\\` 
            : '';

          const tags = tagsMap[data.name] || [];
          const labelsHtml = tags.length > 0 ? \\\`<div style="display:flex;gap:3px;flex-wrap:wrap;padding:3px 0 0 20px;">\\\` + tags.map(t => \\\`<span style="border-radius:3px;padding:1px 4px;font-size:7px;background:\\\${getTagColor(t)}30;color:\\\${getTagColor(t)};border:1px solid \\\${getTagColor(t)}40;">\\\${t}</span>\\\`).join('') + \\\`</div>\\\` : '';

          // ── NAVIGATION UI
          row.innerHTML = \\\`
          <div style="display:flex;align-items:center;gap:5px;width:100%">
            <span class="cas-index">\\\${i + 1}</span>
            \\\${badge}
            \\\${versionBadge}
            \\\${dlBadge}
            <span class="cas-name" title="Double-click to open • Single-click to find\\n\\\${data.name || ''}" style="flex:1; cursor:pointer;">\\\${(data.name || 'unknown').slice(0, 24)}</span>
            \\\${ts ? \\\`<span class="cas-meta">\\\${ts.split(' ')[0]}</span>\\\` : ''}
            <button class="cas-jump-btn" title="Jump to point in chat" style="background:none;border:none;color:#fff;cursor:pointer;font-size:12px;padding:0 4px;margin-left:auto;transition:color 0.2s;text-shadow:0 0 2px rgba(255,255,255,0.3)">↱</button>
          </div>
          \\\${labelsHtml}
          \\\${summary ? \\\`<div style="font-size:9px;color:#666;padding:3px 0 0 20px;line-height:1.3">\\\${summary}</div>\\\` : ''}
        \\\`;

          // Single click: highlights and scrolls
          row.addEventListener('click', (e) => {
            if (e.target.closest('.cas-jump-btn')) return;
            highlightNode(item.node, item.isSidebar ? 'sidebar' : 'chat');
          });

          // Double click: Opens the artifact in the sidebar
          row.addEventListener('dblclick', (e) => {
            if (e.target.closest('.cas-jump-btn')) return;
            if (item.node) item.node.click();
          });

          // Clicking the Jump button specifically scrolls to chat flow
          row.querySelector('.cas-jump-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            jumpToArtifact(data.name);
          });

          list.appendChild(row);
        });
      }
    });`;

text = text.replace(OLD_BLOCK, NEW_BLOCK);

fs.writeFileSync('content.js', text, 'utf8');
console.log('Update finished via JS direct replace');
