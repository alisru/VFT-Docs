const fs = require('fs');
let text = fs.readFileSync('content.js', 'utf8');

// Update findGeminiFilesSidebar
const oldSidebar = `    function findGeminiFilesSidebar() {
      return document.querySelector('[data-panel-id="files"]') || document.querySelector('[aria-label*="Files in this conversation"]') || document.querySelector('[aria-label*="files"]') || document.querySelector('side-panel') || null;
    }`;
const newSidebar = `    function findGeminiFilesSidebar() {
      return document.querySelector('context-sidebar') || document.querySelector('[data-panel-id="files"]') || document.querySelector('[aria-label*="Files in this conversation"]') || document.querySelector('[aria-label*="files"]') || document.querySelector('side-panel') || null;
    }`;
text = text.replace(oldSidebar, newSidebar);

// Update canvasSelectors
const oldSelectors = `const canvasSelectors = ['[data-canvas-id]','[class*="canvas-item"]','[class*="artifact-item"]','[aria-label*="canvas"]','[aria-label*="Canvas"]'];`;
const newSelectors = `const canvasSelectors = ['sidebar-immersive-chip','[data-canvas-id]','[class*="canvas-item"]','[class*="artifact-item"]','[aria-label*="canvas"]','[aria-label*="Canvas"]'];`;
text = text.replace(oldSelectors, newSelectors);

// Update injectGeminiToggleButtons
const oldInject = `    function injectGeminiToggleButtons() {
      if (document.getElementById('gcs-panel-toggle-group')) return;
      const toolbar = document.querySelector('mat-toolbar') || document.querySelector('[class*="toolbar"]') || document.querySelector('header') || document.querySelector('nav');
      if (!toolbar) return;
      const group = document.createElement('div');`;

const newInject = `    function injectGeminiToggleButtons() {
      if (document.getElementById('gcs-panel-toggle-group')) return;
      const toolbar = document.querySelector('.right-section') || document.querySelector('mat-toolbar') || document.querySelector('[class*="toolbar"]') || document.querySelector('header') || document.querySelector('nav');
      if (!toolbar) return;
      const group = document.createElement('div');`;
text = text.replace(oldInject, newInject);

const oldAppend = `      try { toolbar.appendChild(group); } catch(e) {}`;
const newAppend = `      try { 
        if (toolbar.classList.contains('right-section') && toolbar.firstChild) {
          toolbar.insertBefore(group, toolbar.firstChild);
        } else {
          toolbar.appendChild(group); 
        }
      } catch(e) {}`;
text = text.replace(oldAppend, newAppend);

fs.writeFileSync('content.js', text, 'utf8');
console.log('Gemini DOM tracking updated successfully');
