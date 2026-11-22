const fs = require('fs');
const v2 = fs.readFileSync('E:/Vector Field Theory/VFT Docs/fetch_view_icons_preview_20261106.txt', 'utf8');
const v3 = fs.readFileSync('E:/Vector Field Theory/VFT Docs/v3_backup.html', 'utf8');
const v4 = fs.readFileSync('E:/Vector Field Theory/peek_explorer/view_icons_preview.html', 'utf8');

function getNames(html) {
  const matches = [];
  const lines = html.split('\n');
  for (const line of lines) {
    if (line.includes('class="icon-name"')) {
      const start = line.indexOf('>') + 1;
      const end = line.indexOf('</span>', start);
      if (start > 0 && end > start) {
        matches.push(line.substring(start, end).trim());
      }
    }
  }
  return matches;
}

const n2 = getNames(v2);
const n3 = getNames(v3);
const n4 = getNames(v4);

console.log('V2 count:', n2.length, n2);
console.log('V3 count:', n3.length, n3);
console.log('V4 count:', n4.length, n4);
