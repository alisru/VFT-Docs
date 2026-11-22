const fs = require('fs');

const v2 = fs.readFileSync('E:/Vector Field Theory/VFT Docs/fetch_view_icons_preview_20261106.txt', 'utf8');
const v3 = fs.readFileSync('E:/Vector Field Theory/VFT Docs/v3_backup.html', 'utf8');
const v4 = fs.readFileSync('E:/Vector Field Theory/peek_explorer/view_icons_preview.html', 'utf8');

// We want to combine all cards from v2, v3, and v4 into one master file.
// In v3, Section 4 has C1-C5, R1-R5, W1-W5, B1-B5.
// In v3, Section 5 has:
//   Grouping (Replaces 📑), Copy Path, Eject Room, Expand Chevron,
//   New, Cut, Copy, Paste, Rename, Delete, Sort, Preview Pane, Split Tab, Terminal, Scripts, Theme.
// In v2, Section 1 has the locked hollow 4 layout icons.
// In v2, Section 3 has Small (4 Icon Squares) and Small (Folder Stream).
// In v2, Section 4 has Tiles A, Tiles B, Tiles C.
// In v4, we have:
//   S1-S5 (Small icons), Co1-Co5 (Content view), T1-T5 (Tiles),
//   C-G1 to C-G5, R-G1 to R-G5, W-G1 to W-G5, B-G1 to B-G5 (Grounded layouts),
//   G1-G5 (Grouping), CP1-CP5 (Copy path), EJ1-EJ5 (Eject),
//   SO1-SO5 (Sort), PR1-PR5 (Preview pane),
//   Medium, Large, Extra Large, Details, List.

console.log('Building master merged file...');
