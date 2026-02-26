import os
import re
import json

md_files = [
    "Trump_American_Kanon_Plane_1_Identity.md",
    "Trump_American_Kanon_Plane_2_Definition.md",
    "Trump_American_Kanon_Plane_3_Land.md",
    "Trump_American_Kanon_Plane_4_Drive.md",
    "Trump_American_Kanon_Plane_5_Method.md",
    "Trump_American_Kanon_Plane_6_Cause.md",
    "Trump_American_Kanon_Plane_7_Effect.md"
]

plane_names = {
    1: "Identity (Who)",
    2: "Definition (What)",
    3: "Land (Where)",
    4: "Drive (Why)",
    5: "Method (How)",
    6: "Cause (Origin)",
    7: "Effect (Result)"
}

plane_colors = {
    1: "#38bdf8",
    2: "#818cf8",
    3: "#4ade80",
    4: "#fbbf24",
    5: "#a78bfa",
    6: "#f472b6",
    7: "#9ca3af"
}

kanon_data = {}

for plane_idx, t_filename in enumerate(md_files, 1):
    if not os.path.exists(t_filename):
        print(f"File not found: {t_filename}")
        continue
        
    j_filename = f"American_Kanon_Plane_{plane_idx}_{plane_names[plane_idx].split(' ')[0]}_JUDGEMENT.md"
    if plane_idx == 6:
        j_filename = "American_Kanon_Plane_6_Cause_JUDGEMENT.md" # Fixing Foundation/Cause name mismatch
    
    base_vectors = {}
    if os.path.exists(j_filename):
        with open(j_filename, 'r', encoding='utf-8') as jf:
            for line in jf:
                if line.startswith('|') and '---' not in line and 'Vector' not in line:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 5 and '.' in parts[1]:
                        vector_id = parts[1]
                        entry_name = re.sub(r'\*\*', '', parts[2])
                        try:
                            u_val = float(parts[3].replace('+', ''))
                            p_val = float(parts[4].replace('+', ''))
                            base_vectors[vector_id] = {'name': entry_name, 'u': u_val, 'p': p_val, 'trump_score': 0}
                        except ValueError:
                            pass
    else:
        print(f"Judgement file not found: {j_filename}")

    with open(t_filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for line in content.split('\n'):
        if line.startswith('|') and 'Trump Score' not in line and '---' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 7 and '.' in parts[1]:
                vector_id = parts[1]
                score_str = parts[3]
                if vector_id in base_vectors:
                    score_val = 0
                    if '+1' in score_str: score_val = 1
                    elif '-1' in score_str: score_val = -1
                    base_vectors[vector_id]['trump_score'] = score_val
    
    entries = list(base_vectors.values())
    
    # Trump Averages
    trump_avg_u, trump_avg_p = 0.0, 0.0
    u_match = re.search(r'Average Trump υ.*?:.*?([+-]\d+\.\d+)', content)
    p_match = re.search(r'Average Trump ψ.*?:.*?([+-]\d+\.\d+)', content)
    if u_match: trump_avg_u = float(u_match.group(1))
    if p_match: trump_avg_p = float(p_match.group(1))
    
    if len(entries) > 0:
        avg_u = sum(e['u'] for e in entries) / len(entries)
        avg_p = sum(e['p'] for e in entries) / len(entries)
    else:
        avg_u, avg_p = 0.0, 0.0
    
    kanon_data[plane_idx] = {
        "name": plane_names[plane_idx],
        "color": plane_colors[plane_idx],
        "total": {"u": avg_u, "p": avg_p},
        "trump_total": {"u": trump_avg_u, "p": trump_avg_p},
        "entries": entries
    }

# Overall American Kanon averages
all_entries = [e for plane in kanon_data.values() for e in plane['entries']]
if len(all_entries) > 0:
    total_u = sum(e['u'] for e in all_entries) / len(all_entries)
    total_p = sum(e['p'] for e in all_entries) / len(all_entries)
else:
    total_u = 0.0
    total_p = 0.0

trump_total_u = -0.11
trump_total_p = 0.16

js_kanon_data = json.dumps(kanon_data, indent=4)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Donald Trump — Hegemony Visualization</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        html, body { overflow-x: hidden; max-width: 100vw; }
        body { font-family: 'Inter', sans-serif; background-color: #F8FAFC; color: #1e293b; min-height: 100vh; }
        .map-container { padding: 1rem; max-width: 1200px; margin: 0 auto; }
        @media (min-width: 768px) { .map-container { padding: 2rem; } }
        h1 { text-align: center; font-size: 2rem; margin-bottom: 0.5rem; color: #0f172a; font-family: 'Merriweather', serif; font-weight: 800; }
        @media (min-width: 768px) { h1 { font-size: 3rem; } }
        .subtitle { text-align: center; color: #64748b; font-size: 1.1rem; margin-bottom: 2rem; font-style: italic; font-family: 'Merriweather', serif; }
        .controls { display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 2rem; }
        .plane-btn { padding: 0.6rem 1.2rem; border: 1px solid #e2e8f0; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85rem; transition: all 0.2s; background: #ffffff; color: #475569; box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); }
        .plane-btn:hover { background: #f1f5f9; color: #1e293b; border-color: #cbd5e1; transform: translateY(-1px); }
        .plane-btn.active { background: #1e3a8a; color: white; border-color: #1e3a8a; }
        .canvas-container { display: flex; justify-content: flex-start; margin-bottom: 2rem; width: 100%; overflow-x: auto; overflow-y: hidden; -webkit-overflow-scrolling: touch; padding-bottom: 1rem; }
        @media (min-width: 800px) { .canvas-container { justify-content: center; } }
        canvas { background: #ffffff; border-radius: 12px; box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1); border: 1px solid #e2e8f0; width: 800px; min-width: 800px; height: 800px; touch-action: auto; margin: 0 auto; }
        .legend { display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 2rem; }
        .legend-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.85rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; }
        .legend-dot { width: 14px; height: 14px; border-radius: 50%; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 1rem; max-width: 1200px; margin: 0 auto; }
        .stat-card { background: #ffffff; border-radius: 12px; padding: 1.5rem; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1); }
        .stat-card h3 { font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
        .stat-value { font-size: 1.5rem; font-weight: 800; color: #1e293b; }
        .positive { color: #16a34a; } .negative { color: #dc2626; } .neutral { color: #d97706; }
        .tooltip { position: fixed; background: #ffffff; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 8px; font-size: 0.85rem; max-width: none; pointer-events: none; z-index: 1000; box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 10px 10px -5px rgb(0 0 0 / 0.04); display: none; color: #1e293b; }
        .tooltip-title { font-weight: 800; font-size: 1rem; margin-bottom: 0.4rem; color: #0f172a; }
        .tooltip-coords { color: #64748b; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.2rem;}
        .tooltip-judgment { font-style: italic; color: #475569; }
    </style>
</head>
<body class="antialiased text-gray-800">

    <nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Branding -->
                <div class="flex items-center">
                    <div class="flex-shrink-0 flex items-center gap-4">
                        <span class="text-xl font-bold text-white tracking-widest uppercase">Trump Audit</span>
                        <a href="index.html" class="ml-4 px-3 py-2 rounded-md text-sm font-medium text-gray-300 border border-gray-600 hover:text-white hover:bg-gray-700 transition">Index</a>
                    </div>
                </div>

                <!-- Desktop Menu -->
                <div class="hidden lg:block">
                    <div class="ml-10 flex items-baseline space-x-2">
                        <a href="Archetype_The_American_Anomaly.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition">Archetype</a>
                        <a href="Plane_1_Identity.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors">Who</a>
                        <a href="Plane_2_Definition.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors">What</a>
                        <a href="Plane_3_Land.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors">Where</a>
                        <a href="Plane_4_Drive.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors">Why</a>
                        <a href="Plane_5_Method.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors">How</a>
                        <a href="Plane_6_Foundation.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors">Cause</a>
                        <a href="Plane_7_Result.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors">Effect</a>
                        <a href="Trump_Hegemony_Visualization.html" class="px-3 py-2 rounded-md text-sm font-medium bg-blue-800 text-white transition-colors">Map</a>
                        <a href="About_Trump_Audit.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition">About</a>
                    </div>
                </div>

                <!-- Mobile Menu Button -->
                <div class="-mr-2 flex lg:hidden">
                    <button type="button" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')" class="bg-gray-800 inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" aria-controls="mobile-menu" aria-expanded="false">
                        <span class="sr-only">Open main menu</span>
                        <svg class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div class="hidden lg:hidden" id="mobile-menu">
            <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-700 bg-gray-900">
                <a href="Archetype_The_American_Anomaly.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition block">Archetype</a>
                <a href="Plane_1_Identity.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors block">Who</a>
                <a href="Plane_2_Definition.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors block">What</a>
                <a href="Plane_3_Land.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors block">Where</a>
                <a href="Plane_4_Drive.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors block">Why</a>
                <a href="Plane_5_Method.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors block">How</a>
                <a href="Plane_6_Foundation.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors block">Cause</a>
                <a href="Plane_7_Result.html" class="px-3 py-2 rounded-md text-sm font-medium text-blue-100 hover:bg-blue-800 hover:text-white transition-colors block">Effect</a>
                <a href="Trump_Hegemony_Visualization.html" class="px-3 py-2 rounded-md text-sm font-medium bg-blue-800 text-white transition-colors block">Map</a>
                <a href="About_Trump_Audit.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 transition block">About</a>
            </div>
        </div>
    </nav>

    <div class="map-container">

    <h1>Donald Trump — Hegemony Visualization</h1>
    <p class="subtitle">Moral Vector Analysis of 343 Entries Across 7 Planes of the American Kanon</p>

    <div class="explainer" style="max-width: 800px; margin: 0 auto 2rem auto; background: #ffffff; padding: 1.5rem; border-radius: 16px; border: 1px solid #e2e8f0; text-align: left; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);">
        <h3 style="font-size: 1.1rem; font-weight: 800; color: #0f172a; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 2px solid #f1f5f9; padding-bottom: 0.75rem; font-family: 'Merriweather', serif;">How to Read this Map</h3>
        <p style="font-size: 0.95rem; color: #475569; line-height: 1.7; margin-bottom: 1.5rem;">
            This graph plots every concept in the American Kanon as interpreted by the actions and rhetoric of Donald Trump into a coordinate in the <strong>Moral Field</strong>.
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 lg:gap-6 font-sm text-slate-700 items-start">
            <div class="bg-slate-50 p-4 rounded-lg border border-slate-100">
                <strong class="text-slate-900 block mb-2 text-base">X-Axis: Moral (υ)</strong>
                <span class="text-green-600 font-bold">Left (+1)</span>: Universal Benefit<br>
                <span class="text-red-600 font-bold">Right (-1)</span>: Self Benefit
            </div>
            <div class="bg-slate-50 p-4 rounded-lg border border-slate-100">
                <strong class="text-slate-900 block mb-2 text-base">Y-Axis: Will (ψ)</strong>
                <span class="text-green-600 font-bold">Top (+1)</span>: Proactive/Creative<br>
                <span class="text-red-600 font-bold">Bottom (-1)</span>: Suppressive/Passive
            </div>
        </div>
        <p style="font-size: 0.85rem; color: #64748b; margin-top: 1.5rem; font-style: italic; text-align: center;">
            * Hover over any dot to see the specific Concept and its exact Vector Coordinate generated by Trump's alignment.
        </p>
    </div>

    <div class="controls">
        <button class="plane-btn active" data-plane="all">All Planes</button>
        <button class="plane-btn" data-plane="1">P1: Identity</button>
        <button class="plane-btn" data-plane="2">P2: Definition</button>
        <button class="plane-btn" data-plane="3">P3: Land</button>
        <button class="plane-btn" data-plane="4">P4: Drive</button>
        <button class="plane-btn" data-plane="5">P5: Method</button>
        <button class="plane-btn" data-plane="6">P6: Foundation</button>
        <button class="plane-btn" data-plane="7">P7: Result</button>
    </div>

    <div class="canvas-container">
        <canvas id="hegemonyCanvas" width="800" height="800"></canvas>
    </div>

    <div class="legend">
        <div class="legend-item"><div class="legend-dot" style="background: #22c55e;"></div> Hit (+1) - Embodies Kanon</div>
        <div class="legend-item"><div class="legend-dot" style="background: #ef4444;"></div> Fail (-1) - Violates Kanon</div>
        <div class="legend-item"><div class="legend-dot" style="background: #9ca3af;"></div> Miss (0) - Neutral/Mixed</div>
    </div>

    <div class="stats-grid" id="statsGrid"></div>

    <div class="tooltip" id="tooltip">
        <div class="tooltip-title"></div>
        <div class="tooltip-coords"></div>
        <div class="tooltip-judgment"></div>
    </div>

    <script>
        const kanonData = JS_DATA_PLACEHOLDER;

        const canvas = document.getElementById('hegemonyCanvas');
        const ctx = canvas.getContext('2d');
        const tooltip = document.getElementById('tooltip');
        const width = canvas.width;
        const height = canvas.height;
        const cx = width / 2;
        const cy = height / 2;
        const scale = (width - 120) / 2; 
        let currentPlane = 'all';
        let hoveredEntries = [];

        function toCanvasX(u) { return cx - (u * scale); }  
        function toCanvasY(p) { return cy - (p * scale); }

        function getQuadrantColor(u, p, score, alpha = 1) {
            // Override with hit/miss/fail coloring logic
            if (score === 1) return `rgba(34, 197, 94, ${alpha})`; // Green for Hits
            if (score === -1) return `rgba(239, 68, 68, ${alpha})`; // Red for Fails
            return `rgba(156, 163, 175, ${alpha})`; // Grey for misses/neutral
        }

        function drawGrid() {
            ctx.clearRect(0, 0, width, height);

            ctx.globalAlpha = 0.08;
            ctx.fillStyle = '#4ade80'; ctx.fillRect(0, 0, cx, cy); 
            ctx.fillStyle = '#f87171'; ctx.fillRect(cx, 0, cx, cy); 
            ctx.fillStyle = '#38bdf8'; ctx.fillRect(0, cy, cx, cy); 
            ctx.fillStyle = '#fb923c'; ctx.fillRect(cx, cy, cx, cy); 
            ctx.globalAlpha = 1;

            ctx.strokeStyle = '#475569';
            ctx.lineWidth = 1.5;
            ctx.setLineDash([5, 5]);
            ctx.strokeRect(cx - scale, cy - scale, 2 * scale, 2 * scale);
            ctx.setLineDash([]);

            ctx.strokeStyle = '#94a3b8';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(0, cy); ctx.lineTo(width, cy); 
            ctx.moveTo(cx, 0); ctx.lineTo(cx, height); 
            ctx.stroke();

            ctx.font = '700 12px Inter';
            ctx.fillStyle = '#4ade80'; ctx.textAlign = 'left'; ctx.fillText('GREATER GOOD (PRODUCTIVE)', 20, 30);
            ctx.fillStyle = '#f87171'; ctx.textAlign = 'right'; ctx.fillText('GREATEST LIE (REDUCTIVE)', width - 20, 30);
            ctx.fillStyle = '#38bdf8'; ctx.textAlign = 'left'; ctx.fillText('LESSER GOOD (CONSTRUCTIVE)', 20, height - 20);
            ctx.fillStyle = '#fb923c'; ctx.textAlign = 'right'; ctx.fillText('GREATER EVIL (DESTRUCTIVE)', width - 20, height - 20);

            ctx.font = '600 11px Inter';
            ctx.fillStyle = '#94a3b8';
            ctx.textAlign = 'center';
            ctx.fillText('ψ = +1 (Create)', cx, 15);
            ctx.fillText('ψ = -1 (Suppress)', cx, height - 8);

            ctx.save();
            ctx.translate(15, cy);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText('υ = +1 (Universal)', 0, 0);
            ctx.restore();

            ctx.save();
            ctx.translate(width - 15, cy);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText('υ = -1 (Self)', 0, 0);
            ctx.restore();
        }

        function drawEntries() {
            const planes = currentPlane === 'all' ? Object.keys(kanonData) : [currentPlane];

            // Draw a faint connecting line to the origin for hovered? Optional.

            planes.forEach(planeId => {
                const plane = kanonData[planeId];
                plane.entries.forEach(entry => {
                    const x = toCanvasX(entry.u);
                    const y = toCanvasY(entry.p);
                    let baseRadius = 5;
                    if (entry.trump_score === 1) baseRadius = 10; // 2x size for Hits
                    if (entry.trump_score === -1) baseRadius = 15; // 3x size for Fails
                    
                    const isHovered = hoveredEntries.includes(entry);
                    const radius = isHovered ? baseRadius + 4 : baseRadius;
                    const color = getQuadrantColor(entry.u, entry.p, entry.trump_score);

                    ctx.beginPath();
                    ctx.arc(x, y, radius, 0, Math.PI * 2);
                    ctx.fillStyle = color;
                    
                    if (isHovered) {
                        ctx.shadowColor = 'rgba(0,0,0,0.3)';
                        ctx.shadowBlur = 10;
                    } else {
                        ctx.shadowColor = 'transparent';
                        ctx.shadowBlur = 0;
                    }
                    
                    ctx.fill();

                    if (isHovered) {
                        ctx.strokeStyle = '#1e293b';
                        ctx.lineWidth = 2;
                        ctx.stroke();
                    } else {
                        ctx.strokeStyle = '#ffffff';
                        ctx.lineWidth = 1;
                        ctx.stroke();
                    }
                });

                // Draw Kanon plane centroid
                ctx.shadowColor = 'transparent';
                ctx.beginPath();
                let centX = toCanvasX(plane.total.u);
                let centY = toCanvasY(plane.total.p);
                
                // Add a crosshair behind centroid
                ctx.strokeStyle = plane.color;
                ctx.globalAlpha = 0.3;
                ctx.strokeRect(centX - 10, centY - 10, 20, 20);
                
                ctx.globalAlpha = 0.9;
                ctx.arc(centX, centY, 12, 0, Math.PI * 2);
                ctx.fillStyle = '#1e293b'; // Kanon color
                ctx.fill();
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 2.5;
                ctx.stroke();
                
                ctx.font = '800 11px Inter';
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.fillText(`K${planeId}`, centX, centY + 4);
                
                // Draw Trump plane centroid
                ctx.beginPath();
                centX = toCanvasX(plane.trump_total.u);
                centY = toCanvasY(plane.trump_total.p);
                
                ctx.strokeStyle = plane.color;
                ctx.globalAlpha = 0.3;
                ctx.strokeRect(centX - 10, centY - 10, 20, 20);
                
                ctx.globalAlpha = 0.9;
                ctx.arc(centX, centY, 12, 0, Math.PI * 2);
                ctx.fillStyle = '#f59e0b'; // Trump gold
                ctx.fill();
                ctx.strokeStyle = '#fff';
                ctx.lineWidth = 2.5;
                ctx.stroke();
                
                ctx.font = '800 11px Inter';
                ctx.fillStyle = '#fff';
                ctx.textAlign = 'center';
                ctx.fillText(`T${planeId}`, centX, centY + 4);
                
                ctx.globalAlpha = 1;
            });
        }

        function drawGrandTotal() {
            if (currentPlane !== 'all') return;
            
            // Kanon Overall Centroid
            let x = toCanvasX(TOTAL_U);
            let y = toCanvasY(TOTAL_P);
            
            ctx.shadowColor = 'rgba(0,0,0,0.4)';
            ctx.shadowBlur = 15;
            
            ctx.beginPath();
            ctx.arc(x, y, 18, 0, Math.PI * 2);
            ctx.fillStyle = '#1e293b';
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.font = '800 9px Inter';
            ctx.fillStyle = '#fff';
            ctx.textAlign = 'center';
            ctx.fillText('KANON', x, y + 3.5);
            
            // Trump Overall Centroid
            x = toCanvasX(TRUMP_TOTAL_U);
            y = toCanvasY(TRUMP_TOTAL_P);
            
            ctx.beginPath();
            ctx.arc(x, y, 18, 0, Math.PI * 2);
            ctx.fillStyle = '#f59e0b';
            ctx.fill();
            ctx.strokeStyle = '#fff';
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.font = '800 9px Inter';
            ctx.fillStyle = '#fff';
            ctx.textAlign = 'center';
            ctx.fillText('TRUMP', x, y + 3.5);
            
            ctx.shadowColor = 'transparent';
            ctx.shadowBlur = 0;
        }

        function draw() {
            drawGrid();
            drawEntries();
            drawGrandTotal();
        }

        function updateStats() {
            const statsGrid = document.getElementById('statsGrid');
            const planes = currentPlane === 'all' ? Object.keys(kanonData) : [currentPlane];
            let html = '';

            if (currentPlane === 'all') {
                html += `
                    <div class="stat-card" style="border-left: 4px solid #0f172a;">
                        <h3>American Kanon Overall Baseline</h3>
                        <div class="stat-value" style="color: #0f172a;">υ = TOTAL_U_STR, ψ = TOTAL_P_STR</div>
                        <p style="font-size: 0.8rem; color: #64748b; margin-top: 0.75rem; font-weight: 500;">
                            <strong>Data Baseline:</strong> Nodes are clustered along the theoretical absolute vectors of the American Kanon. Color denotes Trump evaluation score.
                        </p>
                    </div>
                    <div class="stat-card" style="border-left: 4px solid #f59e0b;">
                        <h3>Overall Trump Evaluation</h3>
                        <div class="stat-value" style="color: #f59e0b;">υ = TRUMP_U_STR, ψ = TRUMP_P_STR</div>
                        <p style="font-size: 0.8rem; color: #64748b; margin-top: 0.75rem; font-weight: 500;">
                            Derived aggregate position based on Trump's deviations (+1, 0, -1) applied to all 343 base Kanon vectors.
                        </p>
                    </div>
                `;
            }

            planes.forEach(planeId => {
                const plane = kanonData[planeId];
                const quadrantClass = (plane.total.u >= 0 && plane.total.p >= 0) ? 'positive' : 
                                      (plane.total.u < 0 && plane.total.p >= 0) ? 'negative' : 
                                      (plane.total.u >= 0 && plane.total.p < 0) ? 'text-blue-500' : 'text-orange-500';
                
                let quadName = "Greater Good";
                if(plane.total.u < 0 && plane.total.p >= 0) quadName = "Greatest Lie";
                else if(plane.total.u >= 0 && plane.total.p < 0) quadName = "Lesser Good";
                else if(plane.total.u < 0 && plane.total.p < 0) quadName = "The Void";

                html += `
                    <div class="stat-card" style="border-left: 4px solid ${plane.color};">
                        <h3>Plane ${planeId}: ${plane.name}</h3>
                        <div class="stat-value ${quadrantClass}">
                            υ = ${plane.total.u > 0 ? '+' : ''}${plane.total.u.toFixed(2)}, 
                            ψ = ${plane.total.p > 0 ? '+' : ''}${plane.total.p.toFixed(2)}
                        </div>
                        <p style="font-size: 0.8rem; color: #64748b; margin-top: 0.5rem; font-weight: 500;">
                            ${plane.entries.length} Vectors • <strong>${quadName}</strong>
                        </p>
                    </div>
                `;
            });
            statsGrid.innerHTML = html;
        }

        canvas.addEventListener('mousemove', (e) => {
            const rect = canvas.getBoundingClientRect();
            // Scale mouse coordinates due to canvas scaling (if using CSS max-width, though here it's fixed width)
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            const mouseX = (e.clientX - rect.left) * scaleX;
            const mouseY = (e.clientY - rect.top) * scaleY;

            hoveredEntries = [];
            const planes = currentPlane === 'all' ? Object.keys(kanonData) : [currentPlane];

            let closestDist = Infinity;
            let targetU = null;
            let targetP = null;

            for (const planeId of planes) {
                for (const entry of kanonData[planeId].entries) {
                    const x = toCanvasX(entry.u);
                    const y = toCanvasY(entry.p);
                    const dist = Math.sqrt((mouseX - x) ** 2 + (mouseY - y) ** 2);

                    if (dist < 12 && dist < closestDist) {
                        closestDist = dist;
                        targetU = entry.u;
                        targetP = entry.p;
                    }
                }
            }

            if (targetU !== null && targetP !== null) {
                for (const planeId of planes) {
                    for (const entry of kanonData[planeId].entries) {
                        if (entry.u === targetU && entry.p === targetP) {
                            entry._planeId = planeId;
                            hoveredEntries.push(entry);
                        }
                    }
                }
            }
            {
                let kanon_u, kanon_p, trump_u, trump_p;
                if (currentPlane === 'all') {
                    kanon_u = TOTAL_U; kanon_p = TOTAL_P;
                    trump_u = TRUMP_TOTAL_U; trump_p = TRUMP_TOTAL_P;
                } else {
                    kanon_u = kanonData[currentPlane].total.u; kanon_p = kanonData[currentPlane].total.p;
                    trump_u = kanonData[currentPlane].trump_total.u; trump_p = kanonData[currentPlane].trump_total.p;
                }
                
                let kx = toCanvasX(kanon_u);
                let ky = toCanvasY(kanon_p);
                if (Math.sqrt((mouseX - kx) ** 2 + (mouseY - ky) ** 2) < 18) {
                    hoveredEntries.push({
                        name: currentPlane === 'all' ? 'Overall Kanon Average' : `Plane ${currentPlane} Kanon Average`,
                        u: kanon_u, p: kanon_p,
                        is_centroid: true, centroid_type: 'KANON', color: '#1e293b'
                    });
                }
                
                let tx = toCanvasX(trump_u);
                let ty = toCanvasY(trump_p);
                if (Math.sqrt((mouseX - tx) ** 2 + (mouseY - ty) ** 2) < 18) {
                    hoveredEntries.push({
                        name: currentPlane === 'all' ? 'Overall Trump Average' : `Plane ${currentPlane} Trump Average`,
                        u: trump_u, p: trump_p,
                        is_centroid: true, centroid_type: 'TRUMP', color: '#f59e0b'
                    });
                }
            }

            if (hoveredEntries.length > 0) {
                document.body.style.cursor = 'pointer';
                tooltip.style.display = 'block';
                
                let baseU = hoveredEntries[0].u;
                let baseP = hoveredEntries[0].p;
                
                let html = '';
                if (hoveredEntries.length > 1) {
                    html += `<div class="tooltip-coords" style="margin-bottom: 12px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px;">Coordinate Stack: <strong style="color:#0f172a;">υ: ${baseU > 0 ? '+' : ''}${baseU.toFixed(2)}, ψ: ${baseP > 0 ? '+' : ''}${baseP.toFixed(2)}</strong><br><span style="font-size:0.75rem; color:#64748b;">${hoveredEntries.length} overlapping items</span></div>`;
                } else {
                    html += `<div class="tooltip-coords" style="margin-bottom: 8px; color: #64748b; font-size: 0.8rem; font-weight: 600;">υ: ${baseU > 0 ? '+' : ''}${baseU.toFixed(2)}  |  ψ: ${baseP > 0 ? '+' : ''}${baseP.toFixed(2)}</div>`;
                }
                
                const maxRows = Math.min(7, hoveredEntries.length);
                html += `<div style="display: grid; grid-auto-flow: column; grid-template-rows: repeat(${maxRows}, auto); grid-auto-columns: max-content; gap: 0 1.5rem;">`;
                
                hoveredEntries.forEach(entry => {
                    if (entry.is_centroid) {
                        html += `
                            <div style="border-left: 3px solid ${entry.color}; padding-left: 10px; margin-bottom: 12px; min-width: 220px;">
                                <div class="tooltip-title" style="margin-bottom: 2px;">${entry.name}</div>
                                <div class="tooltip-judgment" style="font-size: 0.8rem;">Average aggregate coordinate</div>
                                <strong style="color:${entry.color}; font-size: 0.8rem; display:block; margin-top:2px;">Type: ${entry.centroid_type}</strong>
                            </div>
                        `;
                    } else {
                        let scoreText = 'Miss (0)';
                        let colorStr = '#64748b'; // grey
                        if (entry.trump_score === 1) { scoreText = 'Hit (+1)'; colorStr = '#16a34a'; } // green
                        if (entry.trump_score === -1) { scoreText = 'Fail (-1)'; colorStr = '#dc2626'; } // red
                        
                        html += `
                            <div style="border-left: 3px solid ${kanonData[entry._planeId].color}; padding-left: 10px; margin-bottom: 12px; min-width: 220px;">
                                <div class="tooltip-title" style="margin-bottom: 2px;">${entry.name}</div>
                                <div class="tooltip-judgment" style="font-size: 0.8rem;">Plane ${entry._planeId}: ${kanonData[entry._planeId].name}</div>
                                <strong style="color:${colorStr}; font-size: 0.8rem; display:block; margin-top:2px;">Trump Score: ${scoreText}</strong>
                            </div>
                        `;
                    }
                });
                
                html += `</div>`;
                tooltip.innerHTML = html;
                
                const tooltipRect = tooltip.getBoundingClientRect();
                const viewportWidth = window.innerWidth;
                const viewportHeight = window.innerHeight;
                
                let tLeft = e.clientX + 20;
                let tTop = e.clientY + 20;
                
                if (tLeft + tooltipRect.width > viewportWidth - 20) {
                    tLeft = e.clientX - tooltipRect.width - 20;
                }
                
                if (tTop + tooltipRect.height > viewportHeight - 20) {
                    tTop = viewportHeight - tooltipRect.height - 20;
                }
                
                tLeft = Math.max(10, tLeft);
                tTop = Math.max(10, tTop);
                
                tooltip.style.left = tLeft + 'px';
                tooltip.style.top = tTop + 'px';
            } else {
                document.body.style.cursor = 'default';
                tooltip.style.display = 'none';
            }
            draw();
        });
        
        // Ensure explicit taps on mobile correctly trigger the tooltip without swiping natively
        canvas.addEventListener('touchstart', (e) => {
            if (e.touches.length > 0) {
                const touchEvent = new MouseEvent('mousemove', {
                    clientX: e.touches[0].clientX,
                    clientY: e.touches[0].clientY
                });
                canvas.dispatchEvent(touchEvent);
            }
        }, { passive: true });

        canvas.addEventListener('mouseleave', () => {
            hoveredEntries = [];
            tooltip.style.display = 'none';
            document.body.style.cursor = 'default';
            draw();
        });

        document.querySelectorAll('.plane-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.plane-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentPlane = btn.dataset.plane;
                draw();
                updateStats();
            });
        });

        draw();
        updateStats();

    </script>
    </div>
</body>
</html>"""

html_out = html_template.replace("JS_DATA_PLACEHOLDER", js_kanon_data)
html_out = html_out.replace("TOTAL_U_STR", f"{total_u:+.2f}").replace("TOTAL_P_STR", f"{total_p:+.2f}")
html_out = html_out.replace("TRUMP_U_STR", f"{trump_total_u:+.2f}").replace("TRUMP_P_STR", f"{trump_total_p:+.2f}")
html_out = html_out.replace("TRUMP_TOTAL_U", str(trump_total_u)).replace("TRUMP_TOTAL_P", str(trump_total_p))
html_out = html_out.replace("TOTAL_U", str(total_u)).replace("TOTAL_P", str(total_p))

with open("trump_site/Trump_Hegemony_Visualization.html", "w", encoding='utf-8') as f:
    f.write(html_out)

print("Generated trump_site/Trump_Hegemony_Visualization.html !!")
