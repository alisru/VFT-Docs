const fs = require('fs');
const vm = require('vm');

const html = fs.readFileSync('e:/Vector Field Theory/VFT Docs/semantic_sheet_music_studio.html', 'utf8');

// Extract all JavaScript inside <script> tags
const scriptMatches = html.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi);
let allJs = '';
for (const match of scriptMatches) {
    allJs += match[1] + '\n';
}

console.log(`Extracted ${allJs.length} bytes of JS.`);

// Mock a lightweight DOM environment for compilation test
const mockElements = {
    'source-text': { value: "I heard there was a secret chord\nThat David played and it pleased the Lord\nIt goes like this the fourth the fifth\nThe minor fall and the major lift" },
    'score-title': { value: "Magic 4 Chord Test" },
    'meter-select': { value: '4/4' },
    'granularity-select': { value: 'syllable' },
    'contour-mode-select': { value: 'flow-gravity' },
    'phrasing-mode-select': { value: 'ballad-stretch' },
    'progression-mode-select': { value: 'anthem-4' },
    'syllable-carry-toggle': { checked: true },
    'linebreak-rest-toggle': { checked: true },
    'multistaff-score-toggle': { checked: true },
    'strum-mode-select': { value: 'guitar-strum' },
    'keep-groove-on-rest-toggle': { checked: true },
    'plane-articulation-toggle': { checked: true },
    'tuning-system-select': { value: '440-equal' },
    'voicing-offset-select': { value: 'chord-lock' },
    'backing-drums-toggle': { checked: true },
    'band-conductor-toggle': { checked: true },
    'vol-lead-lbl': { textContent: '' },
    'vol-strum-lbl': { textContent: '' },
    'vol-bass-lbl': { textContent: '' },
    'vol-drums-lbl': { textContent: '' },
    'mute-lead-btn': { classList: { add() {}, remove() {} } },
    'mute-strum-btn': { classList: { add() {}, remove() {} } },
    'mute-bass-btn': { classList: { add() {}, remove() {} } },
    'mute-drums-btn': { classList: { add() {}, remove() {} } },
    'solo-lead-btn': { classList: { add() {}, remove() {} } },
    'solo-strum-btn': { classList: { add() {}, remove() {} } },
    'solo-bass-btn': { classList: { add() {}, remove() {} } },
    'solo-drums-btn': { classList: { add() {}, remove() {} } }
};

const sandbox = {
    console,
    Math,
    Object,
    Array,
    String,
    Number,
    parseInt,
    parseFloat,
    isNaN,
    isFinite,
    Set,
    Map,
    document: {
        getElementById(id) {
            return mockElements[id] || null;
        },
        querySelectorAll() { return []; }
    },
    window: {},
    ABCJS: {
        renderAbc() { return {}; }
    }
};

vm.createContext(sandbox);

try {
    // Run definitions
    vm.runInContext(allJs, sandbox);
    console.log("Successfully evaluated studio script in VM!");

    // Run compileDocument
    vm.runInContext('compileDocument(); window.testTokens = compiledTokens; window.testAbc = currentAbcString;', sandbox);
    console.log("compileDocument executed successfully!");
    console.log("\n--- FULL GENERATED ABC STRING ---");
    console.log(sandbox.window.testAbc);

    // Parse each voice line and verify sum of eighths per measure
    const lines = sandbox.window.testAbc.split('\n');
    let hasMeasureError = false;
    lines.forEach((line, lNum) => {
        if (!line.startsWith('[V:1]')) return;
        const barContent = line.replace(/^\[V:1\]\s*/, '').replace(/\|\]$/, '').trim();
        const bars = barContent.split('|').map(b => b.trim()).filter(b => b.length > 0);
        bars.forEach((bar, bIdx) => {
            // Strip chord labels like "Am (i)" or "Dm"
            const cleanedBar = bar.replace(/"[^"]*"/g, '').trim();
            // Count eighths in cleaned bar
            // Notes look like D1, E2, z2, z8, (D1D1)
            let eighthsInBar = 0;
            const noteRegex = /(?:[A-Ga-g][,']*(?:\/2|\d+)?|z(?:\/2|\d+)?)/g;
            let m;
            while ((m = noteRegex.exec(cleanedBar)) !== null) {
                const token = m[0];
                if (token.endsWith('/2')) {
                    eighthsInBar += 0.5;
                } else {
                    const durMatch = token.match(/\d+/);
                    eighthsInBar += durMatch ? parseInt(durMatch[0], 10) : 1;
                }
            }
            const expectedEighths = 8;
            if (eighthsInBar !== expectedEighths) {
                console.warn(`Line ${lNum} Bar ${bIdx + 1} has ${eighthsInBar} eighths (expected ${expectedEighths}): "${bar}"`);
                hasMeasureError = true;
            } else {
                console.log(`Line ${lNum} Bar ${bIdx + 1}: ${eighthsInBar} eighths [OK]`);
            }
        });
    });
    if (!hasMeasureError) {
        console.log("\n>>> ALL MEASURES HAVE EXACTLY 8 EIGHTHS (PERFECT 4/4 TIME)! <<<");
    }

} catch (err) {
    console.error("Evaluation error:", err);
}
