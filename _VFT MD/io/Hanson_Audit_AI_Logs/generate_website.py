import json
import re
from pathlib import Path

# Paths (resolved relative to this script's location: .../io/Hanson_Audit_AI_Logs/generate_website.py
# so this runs correctly both on the user's Windows machine and in a Linux sandbox mount of the same folder)
IO_DIR = Path(__file__).resolve().parent.parent  # generate_website.py lives in io/Hanson_Audit_AI_Logs/
HANSON_DIR = IO_DIR / "Hanson_Audit"  # audit source docs/JSON live here
JSON_FILE = HANSON_DIR / "Hegemonic Audit_ Pauline Hanson.json"
WEB_DIR = IO_DIR / "Hanson_Audit_Website"
WEB_DIR.mkdir(parents=True, exist_ok=True)
ABOUT_MD_FILE = HANSON_DIR / "About_The_Kanon_Audit.md"

# Canonical mapping
PLANES_MAP = [
    (1, "Identity", "Who"),
    (2, "Definition", "What"),
    (3, "Land", "Where"),
    (4, "Drive", "Why"),
    (5, "Method", "How"),
    (6, "Foundation", "Cause"),
    (7, "Result", "Effect")
]

# Navigation template using Plane Labels (Identity, Definition, Land, etc.)
def get_nav(current_page):
    planes_nav = ""
    for num, label, interrogative in PLANES_MAP:
        filename = f"Plane_{num}_{label}.html"
        active_class = "bg-amber-600 text-white shadow-md" if current_page == filename else "text-gray-300 hover:text-white hover:bg-gray-800"
        planes_nav += f'<a href="{filename}" class="px-3 py-2 rounded-lg text-sm font-semibold transition-all {active_class}">{num}. {label}</a>\n'
    
    home_active = "bg-gray-800 text-white" if current_page == "index.html" else "text-gray-300 hover:text-white hover:bg-gray-800"
    about_active = "bg-amber-600 text-white shadow-md" if current_page == "About.html" else "text-gray-300 hover:text-white hover:bg-gray-800"
    about_link = f'<a href="About.html" class="px-3 py-2 rounded-lg text-sm font-semibold transition-all {about_active}">About</a>\n'

    return f"""
    <nav class="bg-gray-950 border-b border-gray-800 sticky top-0 z-50 shadow-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center">
                    <a href="index.html" class="text-xl font-black text-white tracking-widest flex items-center gap-2">
                        <span class="text-amber-500">★</span> HANSON AUDIT
                    </a>
                </div>
                <div class="hidden lg:flex items-center space-x-2">
                    <a href="index.html" class="px-3 py-2 rounded-lg text-sm font-semibold transition-all {home_active}">Dashboard</a>
                    {planes_nav}
                    {about_link}
                </div>
                <!-- Mobile menu button -->
                <div class="lg:hidden flex items-center">
                    <button type="button" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')" class="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-800 focus:outline-none">
                        <svg class="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>
        <div class="hidden lg:hidden bg-gray-950 border-t border-gray-800 px-2 pt-2 pb-3 space-y-1" id="mobile-menu">
            <a href="index.html" class="block px-3 py-2 rounded-lg text-base font-medium {home_active}">Dashboard</a>
            {planes_nav}
            {about_link}
        </div>
    </nav>
    """

def get_quadrant(v, psi):
    if v >= 0 and psi >= 0:
        return "Greater Good / Grace", "emerald"
    elif v >= 0 and psi < 0:
        return "Lesser Good / Stability", "blue"
    elif v < 0 and psi >= 0:
        return "Greatest Lie", "amber"
    else:
        return "Greater Evil / Collapse", "red"

def format_coord(val):
    s = f"{val:+.1f}" if val != 0 else "0.0"
    return s

CITATIONS_MAP = {
    "wiki": {"label": "Wikipedia", "url": "https://en.wikipedia.org/wiki/Pauline_Hanson"},
    "ms96": {"label": "Maiden Speech (10 Sep 1996)", "url": "https://www.aph.gov.au/Parliamentary_Business/Hansard"},
    "onenation": {"label": "One Nation Policy Platform", "url": "https://www.onenation.org.au/policies"},
    "netimes26": {"label": "National Economic Times NPC Address Coverage (June 2026)", "url": "https://www.nationaleconomictimes.com.au"},
    "tvfy": {"label": "They Vote For You (Voting Record)", "url": "https://theyvoteforyou.org.au"},
    "roymorgan26": {"label": "Roy Morgan Research Poll (Jan/Feb 2026)", "url": "https://www.roymorgan.com"},
    "hawker26": {"label": "Sky News Interview / Hawker Poll (Feb 2026)", "url": "https://www.skynews.com.au"},
    "demosau26": {"label": "DemosAU Primary Poll (Jan 2026)", "url": "https://demosau.com.au"},
    "npc26": {"label": "National Press Club Speech (June 2026)", "url": "https://www.npc.org.au"},
}

DYN_CITATIONS = {}

def parse_footnotes(text):
    if not text:
        return ""
    def replace_citation(match):
        key = match.group(1)
        # Use dynamic citation URL if available in JSON, otherwise fallback to domain map
        if key in DYN_CITATIONS:
            url = DYN_CITATIONS[key]
            label = f"Source: {key}"
        else:
            info = CITATIONS_MAP.get(key, {"label": f"Source: {key}", "url": "#"})
            url = info["url"]
            label = info["label"]
        return f'<a href="{url}" target="_blank" class="inline-flex items-center justify-center px-1.5 py-0.2 ml-0.5 rounded text-[9px] font-mono font-bold bg-amber-500/10 hover:bg-amber-500/20 text-amber-500 border border-amber-500/20 transition-all hover:scale-105" title="{label}">{key}</a>'
    return re.sub(r'\[\^([a-zA-Z0-9_\-]+)\]', replace_citation, text)

def parse_markdown(text):
    if not text:
        return ""
    text = parse_footnotes(text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white font-semibold">\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em class="italic text-gray-300">\1</em>', text)
    return text

def parse_quote_markdown(text):
    if not text:
        return ""
    def replace_citation(match):
        key = match.group(1)
        if key in DYN_CITATIONS:
            url = DYN_CITATIONS[key]
            label = f"Source: {key}"
        else:
            info = CITATIONS_MAP.get(key, {"label": f"Source: {key}", "url": "#"})
            url = info["url"]
            label = info["label"]
        return f'<sup class="text-amber-500 hover:text-amber-400 font-mono text-[10px] ml-0.5"><a href="{url}" target="_blank" title="{label}">^</a></sup>'
    text = re.sub(r'\[\^([a-zA-Z0-9_\-]+)\]', replace_citation, text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white font-semibold">\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em class="italic text-gray-300">\1</em>', text)
    return text

def clean_field_prefixes(text, is_desc=False):
    if not text:
        return ""
    text_clean = text.strip()
    if is_desc:
        # Strip both Brief and Description legacy prefixes recursively or via regex
        text_clean = re.sub(r'^(\*\*Brief:\*\*|\*\*Description:\*\*|Brief:|Description:)\s*', '', text_clean)
        text_clean = re.sub(r'^(\*\*Brief:\*\*|\*\*Description:\*\*|Brief:|Description:)\s*', '', text_clean)
    else:
        # Strip Justification or Actuality prefixes
        text_clean = re.sub(r'^(\*\*Justification:\*\*|Justification:|\*\*Actuality:\*\*|Actuality:)\s*', '', text_clean)
    return text_clean.strip()

def generate_index_page(data):
    total_hits = 0
    total_fails = 0
    total_v_sum = 0
    total_psi_sum = 0
    total_vectors = 0
    plane_cards_html = ""
    
    interrogative_map = {num: (label, inter) for num, label, inter in PLANES_MAP}
    
    for plane in data["planes"]:
        p_num = plane["plane_num"]
        p_name = plane["plane_name"]
        vectors = plane["vectors"]
        
        _, p_interrogative = interrogative_map[p_num]
        
        p_hits = sum(1 for v in vectors if v["verdict"] == "HIT")
        p_fails = sum(1 for v in vectors if v["verdict"] == "FAIL")
        total_hits += p_hits
        total_fails += p_fails
        total_v_sum += sum(v["coordinates"]["v"] * (1 if v["verdict"] == "HIT" else -1) for v in vectors)
        total_psi_sum += sum(v["coordinates"]["psi"] * (1 if v["verdict"] == "HIT" else -1) for v in vectors)
        total_vectors += len(vectors)
        
        p_net = p_hits - p_fails
        p_pct = (p_net / len(vectors)) * 100

        avg_v = sum(v["coordinates"]["v"] * (1 if v["verdict"] == "HIT" else -1) for v in vectors) / len(vectors)
        avg_psi = sum(v["coordinates"]["psi"] * (1 if v["verdict"] == "HIT" else -1) for v in vectors) / len(vectors)

        quad_name, color = get_quadrant(avg_v, avg_psi)

        border_hover = {
            "emerald": "hover:border-emerald-500/30",
            "blue": "hover:border-blue-500/30",
            "amber": "hover:border-amber-500/30",
            "red": "hover:border-red-500/30"
        }[color]
        
        badge_style = f"bg-{color}-100 text-{color}-800 border-{color}-200"
        
        plane_cards_html += f"""
        <a href="Plane_{p_num}_{p_name}.html" class="group relative flex flex-col bg-gray-900 border border-gray-800 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden {border_hover} h-full transform hover:-translate-y-1">
            <div class="absolute inset-0 bg-gradient-to-br from-gray-800/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <div class="p-6 flex-1 relative z-10 flex flex-col">
                <div class="flex items-center justify-between mb-4">
                    <span class="inline-flex items-center justify-center h-10 w-10 rounded-xl bg-gray-800 text-amber-500 text-lg font-black border border-gray-700 group-hover:scale-110 transition-transform">
                        {p_num}
                    </span>
                    <div class="flex items-center gap-2">
                        <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-gray-850 text-gray-400 border border-gray-800 uppercase tracking-widest">
                            {p_interrogative}
                        </span>
                        <span class="px-2.5 py-0.5 rounded-full text-xs font-bold {badge_style} uppercase tracking-widest border">
                            {quad_name}
                        </span>
                    </div>
                </div>
                <h3 class="text-2xl font-bold text-white mb-2 group-hover:text-amber-500 transition-colors">
                    Plane {p_num}: {p_name}
                </h3>
                <div class="h-0.5 w-10 bg-amber-500 rounded-full mb-4 group-hover:w-20 transition-all duration-300"></div>
                
                <div class="grid grid-cols-2 gap-2 mb-4 text-xs font-mono">
                    <div class="bg-gray-950/50 p-2 rounded-lg border border-gray-800">
                        <span class="text-gray-500 block">ALIGNMENT</span>
                        <span class="text-white font-bold text-sm">{p_pct:.1f}%</span>
                    </div>
                    <div class="bg-gray-950/50 p-2 rounded-lg border border-gray-800">
                        <span class="text-gray-500 block">NET SCORE</span>
                        <span class="text-white font-bold text-sm">{p_net:+d} ({p_hits}H / {p_fails}F)</span>
                    </div>
                    <div class="bg-gray-950/50 p-2 rounded-lg border border-gray-800 col-span-2 flex justify-between items-center px-3">
                        <span class="text-gray-500">AVERAGE COORDS</span>
                        <span class="text-amber-500 font-bold text-xs">υ: {avg_v:+.2f}, ψ: {avg_psi:+.2f}</span>
                    </div>
                </div>
            </div>
            <div class="bg-gray-950 px-6 py-3.5 border-t border-gray-800 flex items-center justify-between group-hover:bg-gray-900 transition-colors relative z-10">
                <span class="text-gray-400 group-hover:text-white font-medium text-xs tracking-wider uppercase">Explore {p_name}</span>
                <svg class="w-4 h-4 text-amber-500 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path d="M17 8l4 4m0 0l-4 4m4-4H3" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
                </svg>
            </div>
        </a>
        """

    net_score = total_hits - total_fails
    alignment_percentage = (net_score / total_vectors) * 100 if total_vectors else 0
    overall_avg_v = total_v_sum / total_vectors if total_vectors else 0
    overall_avg_psi = total_psi_sum / total_vectors if total_vectors else 0
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pauline Hanson Hegemonic Audit Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: #030712;
        }}
        .font-mono {{
            font-family: 'JetBrains+Mono', monospace;
        }}
    </style>
</head>
<body class="antialiased text-gray-200">
    
    {get_nav("index.html")}

    <!-- Hero / Header -->
    <header class="bg-gray-950 border-b border-gray-800 relative overflow-hidden py-16">
        <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(245,158,11,0.05),transparent_50%)] pointer-events-none"></div>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative text-center">
            <div class="inline-flex px-4 py-1.5 bg-amber-500/10 border border-amber-500/20 text-amber-500 rounded-full text-xs font-bold uppercase tracking-widest mb-6">
                Forensic Hegemonic Stress Test
            </div>
            <h1 class="text-5xl md:text-7xl font-extrabold text-white tracking-tight mb-4">
                Pauline Hanson Audit
            </h1>
            <p class="text-xl text-gray-400 font-light max-w-3xl mx-auto leading-relaxed">
                Quantitative measurement of constitutional, moral, and historical alignment against the 343-Vector Australian Kanon.
            </p>
        </div>
    </header>

    <!-- Dashboard Main -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        <!-- Bottom Line Summary Card -->
        <div class="bg-gray-900 border border-gray-800 rounded-3xl p-8 shadow-2xl relative overflow-hidden mb-12">
            <div class="absolute top-0 right-0 w-80 h-80 bg-amber-500/5 rounded-full filter blur-3xl opacity-50 -mr-32 -mt-32 pointer-events-none"></div>
            <div class="flex flex-col lg:flex-row gap-8 items-center relative z-10">
                <!-- Large Circular Progress Chart -->
                <div class="relative flex-shrink-0 flex items-center justify-center">
                    <svg class="w-48 h-48 transform -rotate-90">
                        <circle cx="96" cy="96" r="80" stroke="#1f2937" stroke-width="16" fill="transparent" />
                        <circle cx="96" cy="96" r="80" stroke="#f59e0b" stroke-width="16" fill="transparent" 
                                stroke-dasharray="502.6" stroke-dashoffset="{502.6 - (502.6 * alignment_percentage / 100)}" />
                    </svg>
                    <div class="absolute text-center">
                        <span class="text-4xl font-black text-white">{alignment_percentage:.1f}%</span>
                        <span class="text-xs text-gray-500 block uppercase tracking-widest mt-1">Alignment</span>
                    </div>
                </div>
                
                <!-- Metric stats -->
                <div class="flex-1 space-y-4 text-center lg:text-left">
                    <h2 class="text-3xl font-extrabold text-white font-serif tracking-tight">The Bottom Line: Structural Alignment</h2>
                    <p class="text-gray-400 leading-relaxed text-lg max-w-3xl">
                        According to the strict metrics of the Australian Kanon, Pauline Hanson aligns with just over a quarter (<strong class="text-white">{alignment_percentage:.1f}%</strong>) of the nation's core structural, moral, and historical identity, yielding a Net Score of <strong class="text-amber-500">{net_score:+.0f}</strong>.
                    </p>
                    <div class="grid grid-cols-3 gap-4 pt-4 text-center max-w-xl mx-auto lg:mx-0">
                        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
                            <span class="text-gray-500 text-xs block uppercase tracking-wider mb-1">HITS</span>
                            <span class="text-emerald-500 text-2xl font-black">{total_hits}</span>
                        </div>
                        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
                            <span class="text-gray-500 text-xs block uppercase tracking-wider mb-1">FAILS</span>
                            <span class="text-red-500 text-2xl font-black">{total_fails}</span>
                        </div>
                        <div class="bg-gray-950 p-4 rounded-xl border border-gray-800">
                            <span class="text-gray-500 text-xs block uppercase tracking-wider mb-1">MISSES</span>
                            <span class="text-gray-400 text-2xl font-black">0</span>
                        </div>
                    </div>
                    <div class="bg-gray-950 p-4 rounded-xl border border-gray-800 mt-4 max-w-xl mx-auto lg:mx-0">
                        <span class="text-gray-500 text-xs block uppercase tracking-wider mb-1">AVERAGE COORDS (ALL {total_vectors})</span>
                        <span class="text-amber-400 font-mono font-bold">υ: {overall_avg_v:+.2f}, ψ: {overall_avg_psi:+.2f}</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- Quadrant Placement Map -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
            <!-- Coordinate Explanation -->
            <div class="bg-gray-900 border border-gray-800 rounded-3xl p-8 shadow-xl flex flex-col justify-between">
                <div>
                    <h2 class="text-2xl font-extrabold text-white mb-4">Hegemonic Coordinate System</h2>
                    <p class="text-gray-400 leading-relaxed mb-6">
                        Every stance and actuality has been plotted on the Harmonia-Helixis framework against two axes:
                    </p>
                    <div class="space-y-4">
                        <div class="flex items-start gap-4">
                            <div class="h-10 w-10 bg-amber-500/10 border border-amber-500/20 text-amber-500 font-bold rounded-xl flex items-center justify-center font-mono">υ</div>
                            <div>
                                <h3 class="text-white font-bold text-sm">Axis υ (Morality) — Benefit Focus</h3>
                                <p class="text-gray-400 text-xs mt-1">Ranging from +2 (Universal Benefit/Systemic Justice) to -2 (Tyranny/Pure Extraction/Self Benefit).</p>
                            </div>
                        </div>
                        <div class="flex items-start gap-4">
                            <div class="h-10 w-10 bg-amber-500/10 border border-amber-500/20 text-amber-500 font-bold rounded-xl flex items-center justify-center font-mono">ψ</div>
                            <div>
                                <h3 class="text-white font-bold text-sm">Axis ψ (Will) — Will Expression</h3>
                                <p class="text-gray-400 text-xs mt-1">Ranging from +2 (Productive Justice/Creation) to -2 (Chaos/Collapse/Extraction).</p>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="pt-6 border-t border-gray-800/50 mt-6 flex justify-between items-center text-xs text-gray-500">
                    <span>Hanson's Stance: Greatest Lie Anchor</span>
                    <span>Quadrant Placement: (-υ, +ψ)</span>
                </div>
            </div>

            <!-- Quadrants Grid -->
            <div class="bg-gray-900 border border-gray-800 rounded-3xl p-8 shadow-xl relative flex flex-col justify-center">
                <div class="aspect-square w-full max-w-sm mx-auto relative border border-gray-800 p-2 rounded-xl bg-gray-950">
                    <div class="absolute inset-x-2 top-1/2 h-px bg-gray-800"></div> <!-- X Axis -->
                    <div class="absolute inset-y-2 left-1/2 w-px bg-gray-800"></div> <!-- Y Axis -->
                    
                    <div class="absolute top-2 left-1/2 -translate-x-1/2 text-[9px] font-bold text-amber-500 tracking-wider">CREATE (+ψ)</div>
                    <div class="absolute bottom-2 left-1/2 -translate-x-1/2 text-[9px] font-bold text-gray-600 tracking-wider">SUPPRESS (-ψ)</div>
                    <div class="absolute left-2 top-1/2 -translate-y-1/2 text-[9px] font-bold text-amber-500 tracking-wider rotate-90 origin-left">UNIVERSAL (+υ)</div>
                    <div class="absolute right-2 top-1/2 -translate-y-1/2 text-[9px] font-bold text-gray-600 tracking-wider -rotate-90 origin-right">SELF (-υ)</div>
                    
                    <div class="grid grid-cols-2 grid-rows-2 h-full w-full p-4 gap-2 text-center text-xs font-bold">
                        <!-- TL: Greater Good -->
                        <div class="bg-emerald-500/5 rounded-lg border border-emerald-500/10 flex flex-col items-center justify-center p-2 text-emerald-500/40">
                            <span>Greater Good</span>
                            <span class="text-[9px] font-mono opacity-50">+υ, +ψ</span>
                        </div>
                        <!-- TR: Greatest Lie -->
                        <div class="bg-amber-500/10 rounded-lg border border-amber-500/30 flex flex-col items-center justify-center p-2 text-amber-500 ring-2 ring-amber-500/20">
                            <span>Greatest Lie</span>
                            <span class="text-[9px] font-mono opacity-80">-υ, +ψ</span>
                            <span class="text-[8px] bg-amber-500 text-gray-900 rounded px-1 mt-1 font-sans">HANSON</span>
                        </div>
                        <!-- BL: Lesser Good -->
                        <div class="bg-blue-500/5 rounded-lg border border-blue-500/10 flex flex-col items-center justify-center p-2 text-blue-500/40">
                            <span>Lesser Good</span>
                            <span class="text-[9px] font-mono opacity-50">+υ, -ψ</span>
                        </div>
                        <!-- BR: Greater Evil -->
                        <div class="bg-red-500/5 rounded-lg border border-red-500/10 flex flex-col items-center justify-center p-2 text-red-500/40">
                            <span>Greater Evil</span>
                            <span class="text-[9px] font-mono opacity-50">-υ, -ψ</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 7 Planes Grid Section -->
        <h2 class="text-3xl font-extrabold text-white mb-8 border-b border-gray-800 pb-4">Audit Planes</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {plane_cards_html}
        </div>

    </main>

    <footer class="bg-gray-950 border-t border-gray-800 py-12 mt-20 text-center text-gray-500 text-sm">
        <p>© 2026 The Psochic Hegemony. All rights reserved.</p>
    </footer>

</body>
</html>
"""
    with open(WEB_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Dashboard index.html written successfully!")

def generate_plane_pages(data):
    for plane in data["planes"]:
        p_num = plane["plane_num"]
        p_name = plane["plane_name"]
        vectors = plane["vectors"]
        
        # Collect all active citation keys on this plane
        active_keys = set()
        for v in vectors:
            for text_field in [v.get("description", ""), v.get("justification", ""), v.get("actuality", ""), v.get("quote", "")]:
                for key in re.findall(r'\[\^([a-zA-Z0-9_\-]+)\]', text_field):
                    active_keys.add(key)
        
        sources_html = ""
        if active_keys:
            sources_html += f"""
            <!-- Sources Referenced Section -->
            <div class="mt-20 bg-gray-900 border border-gray-800 rounded-3xl p-8 shadow-xl">
                <h3 class="text-xl font-bold mb-6 font-serif text-white uppercase tracking-wider border-b border-gray-800 pb-3">Sources Referenced in Plane {p_num}</h3>
                <ul class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm font-mono text-gray-400">
            """
            for key in sorted(active_keys):
                url = DYN_CITATIONS.get(key, "#")
                label = CITATIONS_MAP.get(key, {}).get("label", f"Source: {key}")
                sources_html += f"""
                    <li class="flex items-center gap-3">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-500 border border-amber-500/20">{key}</span>
                        <a href="{url}" target="_blank" class="hover:text-amber-500 transition-colors truncate" title="{label}">{url}</a>
                    </li>
                """
            sources_html += """
                </ul>
            </div>
            """
        
        p_hits = sum(1 for v in vectors if v["verdict"] == "HIT")
        p_fails = sum(1 for v in vectors if v["verdict"] == "FAIL")
        p_net = p_hits - p_fails
        p_pct = (p_net / len(vectors)) * 100

        avg_v = sum(v["coordinates"]["v"] * (1 if v["verdict"] == "HIT" else -1) for v in vectors) / len(vectors)
        avg_psi = sum(v["coordinates"]["psi"] * (1 if v["verdict"] == "HIT" else -1) for v in vectors) / len(vectors)

        quad_name, color = get_quadrant(avg_v, avg_psi)
        
        # Get final statement from parsed final_verdict node
        final_verdict_data = plane.get("final_verdict", {})
        final_statement = final_verdict_data.get("statement", "")
        if not final_statement:
            statements = {
                1: "Pauline Hanson operates as a defensive, group-centric leveling agent, stoking structural friction in order to isolate identity within monocultural bounds.",
                2: "Hanson stokes systemic friction across the constitutional rulebook, exploiting the High Court and local jurisdictions to campaign against federal integration.",
                3: "Pauline Hanson operates as a highly regressive extraction advocate, actively denying ecological stewardship and treaty obligations to support corporate development.",
                4: "Hanson stokes existential threat narratives to justify border fortification and protectionist isolationism, targeting the quiet fears of the electorate.",
                5: "Hanson utilizes high-friction populist disruption and Senate leverage to bypass administrative standards, calling for direct democracy mechanisms.",
                6: "Hanson stokes national pride around the 1788 colonial inception, defending traditional monarchist stability and history curricula from revision.",
                7: "Pauline Hanson stokes suburban siege paranoia, stoking fear of cultural change and foreign control to maintain isolationist border defense."
            }
            final_statement = statements.get(p_num, "Pauline Hanson acts as a Structural Regression on this Plane.")
        else:
            final_statement = parse_markdown(final_statement)

        # Generate vectors list html
        vectors_html = ""
        current_aspect = ""
        toc_entries = []
        
        for v in vectors:
            addr_parts = v["address"].split('.')
            aspect = addr_parts[1]
            
            # Add section divider
            if aspect != current_aspect:
                current_aspect = aspect
                titles = {
                    1: {"Who": "1.1 The Who of Identity (Metaphysical)", "What": "1.2 The What of Identity (Possible)", "Where": "1.3 The Where of Identity (Physical)", "Why": "1.4 The Why of Identity (Lyrical)", "How": "1.5 The How of Identity (Logical)", "Cause": "1.6 The Cause of Identity (Historical)", "Effect": "1.7 The Effect of Identity (Emotive)"},
                    2: {"Who": "2.1 The Who of Definition (What.Who)", "What": "2.2 The What of Definition (What.What)", "Where": "2.3 The Where of Definition (What.Where)", "Why": "2.4 The Why of Definition (What.Why)", "How": "2.5 The How of Definition (What.How)", "Cause": "2.6 The Cause of Definition (What.Cause)", "Effect": "2.7 The Effect of Definition (What.Effect)"},
                    3: {"Who": "3.1 The Who of Land (Where.Who)", "What": "3.2 The What of Land (Where.What)", "Where": "3.3 The Where of Land (Where.Where)", "Why": "3.4 The Why of Land (Where.Why)", "How": "3.5 The How of Land (Where.How)", "Cause": "3.6 The Cause of Land (Where.Cause)", "Effect": "3.7 The Effect of Land (Where.Effect)"},
                    4: {"Who": "4.1 The Character of the Drive (Why.Who)", "What": "4.2 The Object of the Drive (Why.What)", "Where": "4.3 The Context of the Drive (Why.Where)", "Why": "4.4 The Motivation of the Drive (Why.Why)", "How": "4.5 The Method of the Drive (Why.How)", "Cause": "4.6 The Cause of the Drive (Why.Cause)", "Effect": "4.7 The Result of the Drive (Why.Effect)"},
                    5: {"Who": "5.1 The Operators (How.Who)", "What": "5.2 The Instruments (How.What)", "Where": "5.3 The Architecture (How.Where)", "Why": "5.4 The Rationale (How.Why)", "How": "5.5 The Mechanics (How.How)", "Cause": "5.6 The Origins (How.Cause)", "Effect": "5.7 The Results (How.Effect)"},
                    6: {"Who": "6.1 The Ancestral Agents (Cause.Who)", "What": "6.2 The Foundational Events (Cause.What)", "Where": "6.3 The Historical Geographies (Cause.Where)", "Why": "6.4 The Historical Motivations (Cause.Why)", "How": "6.5 The Historical Methods (Cause.How)", "Cause": "6.6 The Deep Origins (Cause.Cause)", "Effect": "6.7 The Historical Outcomes (Cause.Effect)"},
                    7: {"Who": "7.1 The Resulting Agents (Effect.Who)", "What": "7.2 The Resulting Institutions (Effect.What)", "Where": "7.3 The Resulting Geographies (Effect.Where)", "Why": "7.4 The Resulting Drives (Effect.Why)", "How": "7.5 The Resulting Methods (Effect.How)", "Cause": "7.6 The Resulting Origins (Effect.Cause)", "Effect": "7.7 The Resulting Outcomes (Effect.Effect)"}
                }
                sub_title = titles.get(p_num, {}).get(aspect, f"Section {aspect}")
                anchor_id = f"sub-{aspect.lower()}"
                toc_entries.append((anchor_id, sub_title))
                vectors_html += f"""
                <div class="col-span-1 lg:col-span-2 mt-12 mb-6" id="{anchor_id}">
                    <h2 class="text-2xl font-black text-amber-500 border-b border-gray-800 pb-3 font-serif">
                        {sub_title}
                    </h2>
                </div>
                """
            
            v_val = v["coordinates"]["v"]
            psi_val = v["coordinates"]["psi"]
            v_str = format_coord(v_val)
            psi_str = format_coord(psi_val)
            
            verdict_badge = "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" if v["verdict"] == "HIT" else "bg-red-500/10 text-red-400 border-red-500/20"
            
            quote_block = ""
            if v["quote"]:
                parsed_quote = parse_quote_markdown(v['quote'])
                quote_block = f"""
                <div class="mb-4 pl-4 border-l-2 border-amber-500/30">
                    <p class="text-sm italic text-gray-300 font-serif">"{parsed_quote}"</p>
                    {f'<span class="text-[10px] text-gray-500 mt-1 block">— {v["context"]}</span>' if v.get("context") else ''}
                </div>
                """
            
            clean_name = v["name"]
            
            desc_text = parse_markdown(clean_field_prefixes(v.get('description', ''), is_desc=True))
            just_text = parse_markdown(clean_field_prefixes(v.get('justification', ''), is_desc=False))
            act_text = parse_markdown(clean_field_prefixes(v.get('actuality', ''), is_desc=False))
            
            vectors_html += f"""
            <div class="bg-gray-900 border border-gray-800 rounded-2xl p-6 shadow-md flex flex-col justify-between hover:border-gray-700 transition-colors">
                <div>
                    <!-- Header -->
                    <div class="flex items-start justify-between mb-4 gap-2">
                        <div>
                            <span class="text-xs font-mono text-gray-500 block mb-1">{v['address']}</span>
                            <h4 class="text-xl font-bold text-white leading-tight">{clean_name}</h4>
                        </div>
                        <div class="flex flex-col items-end gap-1.5 flex-shrink-0">
                            <span class="px-2 py-0.5 text-[10px] font-bold rounded border uppercase tracking-wide {verdict_badge}">
                                {v['verdict']}
                            </span>
                            <div class="inline-flex items-center px-1.5 py-0.5 bg-gray-950 border border-gray-800 rounded-md text-[10px] font-mono">
                                <span class="text-gray-500 mr-1">υ:</span>
                                <span class="text-white font-bold">{v_str}</span>
                                <span class="text-gray-700 mx-1">|</span>
                                <span class="text-gray-500 mr-1">ψ:</span>
                                <span class="text-white font-bold">{psi_str}</span>
                            </div>
                        </div>
                    </div>
                    
                    {quote_block}
                    
                    <div class="space-y-3 text-sm text-gray-400">
                        <p><strong class="text-gray-300 font-medium">Description:</strong> {desc_text}</p>
                        <p><strong class="text-gray-300 font-medium">Justification:</strong> {just_text}</p>
                        <p class="bg-gray-950/40 p-3 rounded-lg border border-gray-800/50 mt-2 text-gray-300"><strong class="text-amber-500 font-medium">Actuality:</strong> {act_text}</p>
                    </div>
                </div>
            </div>
            """
            
        # Write plane file
        filename = f"Plane_{p_num}_{p_name}.html"
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plane {p_num}: {p_name} — Pauline Hanson Hegemonic Audit</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: #030712;
        }}
        .font-mono {{
            font-family: 'JetBrains+Mono', monospace;
        }}
    </style>
</head>
<body class="antialiased text-gray-200">
    
    {get_nav(filename)}

    <!-- Plane Header -->
    <header class="bg-gray-950 border-b border-gray-800 relative overflow-hidden py-16">
        <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(245,158,11,0.03),transparent_50%)] pointer-events-none"></div>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
            <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
                <div>
                    <div class="inline-flex h-12 w-auto px-4 bg-amber-500/10 border border-amber-500/20 text-amber-500 rounded-xl items-center justify-center text-lg font-bold shadow-md mb-4">
                        Plane {p_num}
                    </div>
                    <h1 class="text-4xl md:text-5xl font-extrabold text-white tracking-tight mb-2">
                        {p_name}
                    </h1>
                    <p class="text-gray-400 font-light max-w-2xl text-lg">
                        Detailed stress-test analysis of the {len(vectors)} vectors in the {p_name} dimension.
                    </p>
                </div>
                
                <!-- Scorecard widget -->
                <div class="bg-gray-900 border border-gray-800 rounded-2xl p-4 flex gap-6 text-center text-xs font-mono">
                    <div>
                        <span class="text-gray-500 block mb-0.5">ALIGNMENT</span>
                        <span class="text-white font-bold text-lg">{p_pct:.1f}%</span>
                    </div>
                    <div class="w-px h-8 bg-gray-800 my-auto"></div>
                    <div>
                        <span class="text-gray-500 block mb-0.5">NET SCORE</span>
                        <span class="text-white font-bold text-lg">{p_net:+d}</span>
                    </div>
                    <div class="w-px h-8 bg-gray-800 my-auto"></div>
                    <div>
                        <span class="text-gray-500 block mb-0.5">AVERAGE COORDS</span>
                        <span class="text-amber-500 font-bold text-lg">υ: {avg_v:+.2f}, ψ: {avg_psi:+.2f}</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Section -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        
        <!-- Forensic Verdict Block -->
        <div class="bg-gray-900 border border-gray-800 rounded-3xl p-8 shadow-xl relative overflow-hidden mb-12">
            <div class="absolute top-0 right-0 w-64 h-64 bg-amber-500/5 rounded-full filter blur-3xl opacity-50 -mr-32 -mt-32 pointer-events-none"></div>
            <div class="relative z-10">
                <h3 class="text-xl font-bold mb-4 font-serif text-white uppercase tracking-wider">Final Forensic Verdict: Plane {p_num}</h3>
                <p class="text-gray-300 leading-relaxed text-lg mb-4 italic">
                    "{final_statement}"
                </p>
                <div class="inline-flex items-center gap-2 px-3 py-1 bg-gray-950 border border-gray-800 rounded-xl text-sm">
                    <span class="text-gray-500">Hegemonic Zone:</span>
                    <span class="text-amber-500 font-bold uppercase tracking-wider">{quad_name}</span>
                </div>
            </div>
        </div>

        <!-- TOC + Vectors layout -->
        <div class="flex gap-8 items-start">

            <!-- Sticky TOC Sidebar -->
            <aside class="hidden xl:block w-56 flex-shrink-0 sticky top-20 self-start">
                <div class="bg-gray-900 border border-gray-800 rounded-2xl p-4">
                    <p class="text-xs font-bold uppercase tracking-widest text-amber-500 mb-3">Jump to</p>
                    <nav class="space-y-1">
                        {"".join(f'<a href="#{eid}" class="block text-xs text-gray-400 hover:text-amber-400 transition-colors py-1 border-l-2 border-gray-800 hover:border-amber-500 pl-2 leading-tight">{etitle}</a>' for eid, etitle in toc_entries)}
                    </nav>
                </div>
            </aside>

            <!-- Vectors Grid -->
            <div class="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-8">
                {vectors_html}
            </div>

        </div>

        {sources_html}

    </main>

    <footer class="bg-gray-950 border-t border-gray-800 py-12 mt-20 text-center text-gray-500 text-sm">
        <p>© 2026 The Psochic Hegemony. All rights reserved.</p>
    </footer>

</body>
</html>
"""
        with open(WEB_DIR / filename, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"File {filename} written successfully!")

def render_about_markdown(md_text):
    """Minimal Markdown -> styled HTML renderer for the About page.
    Supports: '# ' / '## ' headers, blank-line-separated paragraphs,
    **bold**, *italic*. Deliberately simple -- this is prose, not audit data."""
    def inline(text):
        text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white font-semibold">\1</strong>', text)
        text = re.sub(r'\*(.*?)\*', r'<em class="italic text-gray-300">\1</em>', text)
        return text

    blocks = [b.strip() for b in md_text.strip().split("\n\n") if b.strip()]
    html_parts = []
    for block in blocks:
        if block.startswith("## "):
            html_parts.append(
                f'<h2 class="text-2xl font-extrabold text-white mt-12 mb-4 border-b border-gray-800 pb-3">{inline(block[3:].strip())}</h2>'
            )
        elif block.startswith("# "):
            html_parts.append(
                f'<h1 class="text-4xl font-black text-white mb-6">{inline(block[2:].strip())}</h1>'
            )
        elif re.match(r'^\d+\.\s+\*\*', block):
            # numbered list block (used for "The seven planes")
            items = block.split("\n")
            list_item_re = re.compile(r'^\d+\.\s+')
            lis_parts = []
            for item in items:
                if item.strip():
                    stripped_item = list_item_re.sub("", item.strip())
                    lis_parts.append(f'<li class="mb-2">{inline(stripped_item)}</li>')
            lis = "".join(lis_parts)
            html_parts.append(f'<ol class="list-decimal list-inside text-gray-400 leading-relaxed space-y-1 mb-6 pl-2">{lis}</ol>')
        else:
            html_parts.append(f'<p class="text-gray-400 leading-relaxed text-lg mb-6">{inline(block)}</p>')
    return "\n".join(html_parts)

def generate_about_page():
    if not ABOUT_MD_FILE.exists():
        print(f"About markdown not found at {ABOUT_MD_FILE}, skipping About.html generation.")
        return

    with open(ABOUT_MD_FILE, "r", encoding="utf-8") as f:
        md_text = f.read()

    # First '# ' line becomes the hero title; rest renders as body
    lines = md_text.strip().split("\n\n", 1)
    title_block = lines[0].lstrip("# ").strip() if lines[0].startswith("# ") else "About This Audit"
    body_md = lines[1] if len(lines) > 1 else ""
    body_html = render_about_markdown(body_md)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About — Pauline Hanson Hegemonic Audit</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');
        body {{
            font-family: 'Outfit', sans-serif;
            background-color: #030712;
        }}
        .font-mono {{
            font-family: 'JetBrains+Mono', monospace;
        }}
    </style>
</head>
<body class="antialiased text-gray-200">

    {get_nav("About.html")}

    <!-- Hero / Header -->
    <header class="bg-gray-950 border-b border-gray-800 relative overflow-hidden py-16">
        <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(245,158,11,0.05),transparent_50%)] pointer-events-none"></div>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative text-center">
            <div class="inline-flex px-4 py-1.5 bg-amber-500/10 border border-amber-500/20 text-amber-500 rounded-full text-xs font-bold uppercase tracking-widest mb-6">
                Methodology &amp; Framework
            </div>
            <h1 class="text-5xl md:text-7xl font-extrabold text-white tracking-tight mb-4">
                {title_block}
            </h1>
            <p class="text-xl text-gray-400 font-light max-w-3xl mx-auto leading-relaxed">
                How the Australian Kanon works, how it was built, and how this audit measures a real actor against it.
            </p>
        </div>
    </header>

    <!-- Body -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="bg-gray-900 border border-gray-800 rounded-3xl p-8 md:p-12 shadow-2xl">
            {body_html}
        </div>
    </main>

    <footer class="bg-gray-950 border-t border-gray-800 py-12 mt-20 text-center text-gray-500 text-sm">
        <p>© 2026 The Psochic Hegemony. All rights reserved.</p>
    </footer>

</body>
</html>
"""
    with open(WEB_DIR / "About.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("About.html written successfully!")

def run():
    print("Loading data...")
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    global DYN_CITATIONS
    DYN_CITATIONS = data.get("sources", {})
    
    print("Generating index Dashboard...")
    generate_index_page(data)
    
    print("Generating Plane Pages...")
    generate_plane_pages(data)

    print("Generating About page...")
    generate_about_page()

    print("Website generation complete!")

if __name__ == "__main__":
    run()
