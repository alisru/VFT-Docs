// Offscreen Document Worker for Real-Time Direct Disk File Writes
// Holds FileSystemDirectoryHandle from IndexedDB and writes Markdown files directly to PC folder

const DB_NAME = 'AutoScribeFolderDB';
const STORE_NAME = 'handles';

let dirHandle = null;

function openFolderDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, 1);
    req.onupgradeneeded = (e) => {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(STORE_NAME)) {
        db.createObjectStore(STORE_NAME);
      }
    };
    req.onsuccess = () => resolve(req.result);
    req.onerror = () => reject(req.error);
  });
}

async function loadDirectoryHandle() {
  try {
    const db = await openFolderDB();
    return new Promise((resolve) => {
      const tx = db.transaction(STORE_NAME, 'readonly');
      const req = tx.objectStore(STORE_NAME).get('diskFolder');
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => resolve(null);
    });
  } catch (err) {
    console.warn('[Auto-Scribe Offscreen] Failed to open folder DB:', err);
    return null;
  }
}

function formatDraftMarkdown(draft) {
  return `---
id: ${draft.id}
site: ${draft.site}
url: ${draft.url}
title: ${draft.page_title || ''}
context: ${draft.context_title || ''}
char_count: ${draft.char_count}
word_count: ${draft.word_count}
updated_at: ${draft.updated_at}
---

${draft.text}
`;
}

async function writeDraftToDisk(draft) {
  if (!dirHandle) {
    dirHandle = await loadDirectoryHandle();
  }
  if (!dirHandle) return { success: false, error: 'No disk folder selected' };

  try {
    // Check permission
    const perm = await dirHandle.queryPermission({ mode: 'readwrite' });
    if (perm !== 'granted') {
      return { success: false, error: 'Permission not granted to disk folder' };
    }

    // Site subfolder
    const siteFolder = (draft.site || 'web').replace(/[^a-zA-Z0-9_\-\.]/g, '_');
    const siteDir = await dirHandle.getDirectoryHandle(siteFolder, { create: true });

    // Filename
    const title = draft.context_title || draft.page_title || draft.id;
    const cleanSlug = title.replace(/[\\/*?:"<>|]/g, '').replace(/[\s_]+/g, '-').slice(0, 50).trim() || 'draft';
    const filename = `${cleanSlug}_${draft.id.slice(-6)}.md`;

    // Write file
    const fileHandle = await siteDir.getFileHandle(filename, { create: true });
    const writable = await fileHandle.createWritable();
    await writable.write(formatDraftMarkdown(draft));
    await writable.close();

    return { success: true, filename };
  } catch (err) {
    console.warn('[Auto-Scribe Offscreen] Write error:', err);
    return { success: false, error: err.message };
  }
}

// Initial load
(async () => {
  dirHandle = await loadDirectoryHandle();
})();

// Message listener from background
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'OFFSCREEN_WRITE_DRAFT') {
    (async () => {
      const res = await writeDraftToDisk(request.payload);
      sendResponse(res);
    })();
    return true;
  }

  if (request.action === 'OFFSCREEN_REFRESH_HANDLE') {
    (async () => {
      dirHandle = await loadDirectoryHandle();
      sendResponse({ success: true, folderName: dirHandle ? dirHandle.name : null });
    })();
    return true;
  }

  if (request.action === 'OFFSCREEN_SYNC_ALL') {
    (async () => {
      const drafts = request.payload || [];
      let count = 0;
      for (const d of drafts) {
        const res = await writeDraftToDisk(d);
        if (res.success) count++;
      }
      sendResponse({ success: true, count });
    })();
    return true;
  }
});
