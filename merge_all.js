const fs = require('fs');

const v3 = fs.readFileSync('E:/Vector Field Theory/VFT Docs/v3_backup.html', 'utf8');
const v4 = fs.readFileSync('E:/Vector Field Theory/peek_explorer/view_icons_preview.html', 'utf8');

// Find insertion point in v3 (just before the closing script)
const scriptPos = v3.lastIndexOf('  <script>');
if (scriptPos === -1) {
  console.error('script tag not found in v3');
  process.exit(1);
}

const v3Base = v3.substring(0, scriptPos);
const v3Tail = v3.substring(scriptPos);

// In v4, extract the newly added sections:
// sec-small (S1-S5 from user sketch)
// sec-content (Co1-Co5 from user sketch)
// sec-layout-col (C-G1 to C-G5)
// sec-layout-row (R-G1 to R-G5)
// sec-layout-wrap (W-G1 to W-G5)
// sec-layout-room (B-G1 to B-G5)
// sec-headers (G1-G5, CP1-CP5, EJ1-EJ5)
// sec-toolbar (SO1-SO5, PR1-PR5)

const newSecsStart = v4.indexOf('<nav class="nav-pills">');
const newSecsEnd = v4.lastIndexOf('  <script>');

const newContent = (newSecsStart !== -1 && newSecsEnd !== -1)
  ? '\n  <!-- ========================================== -->\n  <!-- NEW ITERATIONS & USER SKETCH CANDIDATES -->\n  <!-- ========================================== -->\n' + v4.substring(newSecsStart, newSecsEnd)
  : '';

const masterHtml = v3Base + newContent + '\n' + v3Tail;

fs.writeFileSync('E:/Vector Field Theory/peek_explorer/view_icons_preview.html', masterHtml, 'utf8');
console.log('Successfully written master view_icons_preview.html! Total length:', masterHtml.length);
