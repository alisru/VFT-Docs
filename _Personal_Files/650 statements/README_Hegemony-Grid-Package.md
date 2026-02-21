# v4 Psochic Hegemony Grid - Complete Package
## 650 Political Spectrum Statements - Standalone HTML

---

## 📦 PACKAGE CONTENTS

```
v4_Hegemony-Grid_Package/
├── README.md (this file)
├── launch-hegemony-grid.bat (Windows launcher)
├── launch-hegemony-grid.sh (Mac/Linux launcher)
├── v4_Hegemony-Grid_650-Statements_COMPLETE.html (standalone grid - ALL 650 statements)
└── MASTER_INDEX_File_Versions_and_Lineage.md (version tracking)
```

---

## 🚀 QUICK START

### Windows:
1. Double-click `launch-hegemony-grid.bat`
2. Grid opens in your default browser
3. No installation, no build, no dependencies

### Mac/Linux:
1. Open terminal in this folder
2. Run: `./launch-hegemony-grid.sh`
3. Grid opens in your default browser

### Manual Launch:
Just open `v4_Hegemony-Grid_650-Statements_COMPLETE.html` in any web browser

---

## ✨ FEATURES

### Complete Dataset
- **650 total statements** across full political spectrum
- **100 Far-Right** - Nationalist, authoritarian, ethnocentric
- **100 Right-Wing** - Conservative, pro-market, traditional
- **100 Centrist** - Pragmatic, evidence-based, hedging
- **100 Left** - Progressive, social justice, regulation
- **100 Far-Left** - Revolutionary, anti-capitalist, anarchist
- **150 General** - Original moral statements

### Interactive Features
- **Ideology Filtering** - Show/hide any political category
- **Clickable Cells** - View all statements in each position
- **8 Heatmap Views** - Density, words, qualifications, complexity, hedging%, action%, passivity, certainty
- **Live Statistics** - Updates based on active filters
- **CSV Export** - Download filtered data for analysis
- **No Installation Required** - Pure HTML + React via CDN

---

## 🎯 HOW TO USE

### 1. Launch the Grid
Use the launcher script or open the HTML file directly

### 2. Filter by Ideology
Click ideology buttons to show/hide categories:
- **Far-Right** (red) - Nationalist statements
- **Right** (light red) - Conservative statements  
- **Centrist** (purple) - Pragmatic statements
- **Left** (blue) - Progressive statements
- **Far-Left** (dark blue) - Revolutionary statements
- **General** (gray) - Non-political statements

### 3. Explore the Topology
Click any cell in the 7×7 grid to see statements at that position

### 4. Switch Heatmaps
View different metrics:
- **Density** - How many statements
- **Qualifications** - "but/maybe/perhaps" count
- **Action %** - Percentage of action verbs
- **Complexity** - Combined metric

### 5. Export Data
Click "Export CSV" to download filtered subset for statistical analysis

---

## 📊 WHAT TO EXPLORE

### Test the Centrist Hypothesis
1. Filter to **only Centrist**
2. Check **Qualifications** heatmap
3. Prediction: Centrists should show highest hedging (2-3× other groups)
4. Check density - Do they cluster in intermediates?

### Test the Horseshoe Theory
1. Filter to **Far-Right + Far-Left only**
2. Check topology - Do they cluster similarly?
3. Check **Action %** - Are both high?
4. Check **Qualifications** - Are both low (certainty)?

### Test the Left Skew
1. Filter to **Left + Far-Left**
2. Check if they dominate GG corner (+1, +1)
3. Is altruistic action left-clustered?

### Test Extremism-Action Correlation
1. Compare **Far-Right + Far-Left** (extremes)
2. vs **Centrist** (middle)
3. Check **Action %** heatmap
4. Do extremes show more activity?

### Test Corner Attraction
1. Show all categories
2. Check **Density** heatmap
3. Do corners (+1,+1), (-1,+1), (+1,-1), (-1,-1) have highest density?
4. Is center (0,0) empty?

---

## 🔬 TECHNICAL DETAILS

### Technology Stack
- **HTML5** - Single standalone file
- **React 18** - Loaded via CDN (unpkg.com)
- **Tailwind CSS** - Loaded via CDN
- **Babel Standalone** - JSX transformation in browser
- **No Build Required** - Works immediately

### Browser Compatibility
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Internet Explorer: ❌ Not supported (use modern browser)

### File Size
- HTML file: ~200-300 KB (includes all 650 statements)
- No external dependencies after CDN load
- Works offline after first load (CDN cached)

### Data Structure
Each statement includes:
- `id` - Unique identifier (1-650)
- `text` - The statement content
- `ideology` - Political category
- `upsilon` (υ) - Morality axis (-1 to +1)
- `psi` (ψ) - Will axis (-1 to +1)
- `words` - Word count
- `qualifications` - "but/maybe/perhaps" count
- `hedges` - "really/actually/basically" count
- `actionVerbs` - "will/do/make/create" count
- `passiveMarkers` - "hope/wish/should" count
- `certaintyMarkers` - "will/must/definitely" count
- `hedgingRatio` - (quals + hedges) / words
- `actionRatio` - actions / words
- `passivityRatio` - passive / words
- `complexityScore` - words × (1 + quals + hedges×0.5)

---

## 📈 COORDINATE SYSTEM

### υ Axis (Morality) - Who Benefits?
```
+2.0  ┬  Everyone / All beings (Systemic Justice)
+1.0  ┼  Other people (Greater Good) ◄─── GG corner
+0.0  ┼  No one / Neutral
-1.0  ┼  My group only (Lesser Evil) ◄─── LE corner
-2.0  ┴  Only me (Tyranny)
```

### ψ Axis (Will) - What Energy?
```
+2.0  ┬  Actively creating value (Productive Justice)
+1.0  ┼  Proactive - creating, building ◄─── GG, LE (active)
+0.0  ┼  Neutral - no force applied
-1.0  ┼  Passive - allowing, withholding ◄─── LG, GE (passive)
-2.0  ┴  Actively destroying (Chaos)
```

### The Four Corners
- **GG (+1,+1)** - Greater Good - Active altruism
- **LE (-1,+1)** - Lesser Evil - Active self-interest
- **LG (+1,-1)** - Lesser Good - Passive altruism
- **GE (-1,-1)** - Greater Evil - Passive nihilism

---

## 🎓 THEORETICAL BACKGROUND

### Core Concepts
- **Topology** - Statements naturally cluster at attractors (corners)
- **Instability** - Intermediate positions are hard to maintain
- **Hedging** - More qualifications = less stable position
- **Action Gap** - Extreme positions motivate action
- **Horseshoe** - Far-right and far-left show similar dynamics

### Key Predictions
1. **Corners attract** - 45%+ of statements at ±1 positions
2. **Center is empty** - True neutrality is impossible
3. **Centrists hedge most** - 2-3× qualifications vs extremes
4. **Extremes act more** - Higher ψ (action) values
5. **Left skew in GG** - Altruistic action clusters progressive

### Related Documents
- `The_Four_Spirals_Energy_As_Inquiry.md` - Theoretical framework
- `50_Statement_Bucket_Grid_Analysis.md` - Original methodology
- `AI_Measurement_Protocol_Psochic_Hegemony.md` - Replication protocol
- `MASTER_INDEX_File_Versions_and_Lineage.md` - Version control

---

## 💾 EXPORT DATA

### CSV Export
Click "Export CSV" button to download data with columns:
- ID, Ideology, Upsilon, Psi, Text
- Words, Qualifications, Hedges, ActionVerbs, PassiveMarkers, CertaintyMarkers
- HedgingRatio, ActionRatio, PassivityRatio, ComplexityScore

### Statistical Analysis
Import CSV into:
- **Python** (pandas) - For statistical testing
- **R** (tidyverse) - For advanced modeling
- **Excel** - For basic analysis
- **SPSS/Stata** - For academic research

### Suggested Analyses
1. **ANOVA** - Test if qualification density differs by ideology
2. **Correlation** - Test υ vs ideology, ψ vs action
3. **Cluster analysis** - Validate four-corner structure
4. **Regression** - Predict position from text features

---

## 🐛 TROUBLESHOOTING

### Grid doesn't open
- **Windows:** Right-click .bat → "Run as administrator"
- **Mac/Linux:** Make script executable: `chmod +x launch-hegemony-grid.sh`
- **Manual:** Open HTML file directly in browser

### Grid shows but no data
- Check browser console (F12) for errors
- Ensure JavaScript is enabled
- Try a different browser (Chrome/Firefox recommended)

### Export doesn't work
- Check browser allows file downloads
- Try right-click Export button → "Save link as"

### Grid is slow
- Normal with 650 statements
- Try filtering to reduce displayed data
- Close other browser tabs

---

## 📝 VERSION HISTORY

### v4 (Current)
- 650 complete statements
- Ideology filtering
- Full heatmap suite
- CSV export
- Standalone HTML

### v3 (Superseded)
- 150 statements
- Basic filtering
- React component

### v2 (Superseded)
- 50 statements
- No filtering

### v1 (Superseded)
- Empty grid
- Metric tracking only

---

## 🔗 ADDITIONAL RESOURCES

### Documentation Files
- All 650 statements documented in MD files
- Complete measurements included
- Methodology explained
- Replication protocol provided

### Academic Use
- Cite as: "Psochic Hegemony Grid v4 (2026)"
- Dataset available for research
- Methodology peer-reviewable
- Open for replication

---

## 📧 FEEDBACK

This is v4 FINAL - if you find issues:
1. Check MASTER_INDEX for version info
2. Verify you have complete HTML file
3. Test in different browser
4. Check documentation files

---

## ⚖️ LICENSE

Research and educational use permitted.
Please cite if used in academic work.

---

**v4 Psochic Hegemony Grid**  
**650 Political Spectrum Statements**  
**Standalone HTML Package**  
**No Installation • No Dependencies • Just Open and Explore**

---

END OF README
