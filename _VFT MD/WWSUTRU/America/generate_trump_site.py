import re
import os

SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"
OUTPUT_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America\trump_site"
PLANES = [
    {"num": 1, "id_label": "Who", "name": "Identity", "file": "Trump_American_Kanon_Plane_1_Identity.md", "color": "red"},
    {"num": 2, "id_label": "What", "name": "Definition", "file": "Trump_American_Kanon_Plane_2_Definition.md", "color": "amber"},
    {"num": 3, "id_label": "Where", "name": "Land", "file": "Trump_American_Kanon_Plane_3_Land.md", "color": "blue"},
    {"num": 4, "id_label": "Why", "name": "Drive", "file": "Trump_American_Kanon_Plane_4_Drive.md", "color": "green"},
    {"num": 5, "id_label": "How", "name": "Method", "file": "Trump_American_Kanon_Plane_5_Method.md", "color": "indigo"},
    {"num": 6, "id_label": "Cause", "name": "Foundation", "file": "Trump_American_Kanon_Plane_6_Cause.md", "color": "purple", "totality_name": "Cause"},
    {"num": 7, "id_label": "Effect", "name": "Result", "file": "Trump_American_Kanon_Plane_7_Effect.md", "color": "gray", "totality_name": "Effect"},
]

SENSE_COLORS = {
    "1": {"bg": "bg-red-900", "text": "text-red-200", "badge": "bg-red-800", "icon": "text-red-600", "border": "border-red-200", "light_bg": "bg-red-50"},
    "2": {"bg": "bg-blue-900", "text": "text-blue-200", "badge": "bg-blue-800", "icon": "text-blue-600", "border": "border-blue-200", "light_bg": "bg-blue-50"},
    "3": {"bg": "bg-amber-600", "text": "text-amber-100", "badge": "bg-amber-500", "icon": "text-amber-600", "border": "border-amber-200", "light_bg": "bg-amber-50"},
    "4": {"bg": "bg-green-700", "text": "text-green-100", "badge": "bg-green-600", "icon": "text-green-600", "border": "border-green-200", "light_bg": "bg-green-50"},
    "5": {"bg": "bg-indigo-700", "text": "text-indigo-200", "badge": "bg-indigo-600", "icon": "text-indigo-600", "border": "border-indigo-200", "light_bg": "bg-indigo-50"},
    "6": {"bg": "bg-purple-800", "text": "text-purple-200", "badge": "bg-purple-700", "icon": "text-purple-600", "border": "border-purple-200", "light_bg": "bg-purple-50"},
    "7": {"bg": "bg-gray-800", "text": "text-gray-400", "badge": "bg-gray-700", "icon": "text-gray-600", "border": "border-gray-200", "light_bg": "bg-gray-50"},
}

def parse_markdown_file(filepath):
    """Parses base Kanon files to extract context and meaning for each vector."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    sense_blocks = re.split(r'## \d\.\d.*? \(.*?\)\n', content)
    sense_titles = re.findall(r'## \d\.(\d).*? \((.*?)\)\n', content) # extracts sense num, and label

    parsed_data = {
        "preamble": "",
        "senses": {},
        "averages_html": "",
        "totality_html": ""
    }
    
    parsed_data["preamble"] = sense_blocks[0].strip()

    if len(sense_blocks) < 2:
        return parsed_data

    for i, (sense_num, sense_label) in enumerate(sense_titles):
        raw_content = sense_blocks[i+1]
        
        # split out the score and following sections
        item_block_match = re.search(r'(\| Vector \|.*?)\n\n\*\*Score:(.*?)\*\*', raw_content, re.DOTALL)
        if not item_block_match:
            # Maybe there are no averages / totality at the end of this block
            item_block = raw_content
            sense_score = ""
        else:
            item_block = item_block_match.group(1)
            sense_score = item_block_match.group(2).strip()

        items = []
        for line in item_block.split('\n'):
            if '|' in line and not '---|' in line and not 'Vector | Entry' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 7 and re.match(r'^[A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+$', parts[1]):
                    vec_id = parts[1]
                    val = parts[2].strip()
                    val = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', val)
                    val = re.sub(r'\*(.*?)\*', r'<em>\1</em>', val)
                    
                    reasoning = parts[6].strip()
                    reasoning = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', reasoning)
                    reasoning = re.sub(r'\*(.*?)\*', r'<em>\1</em>', reasoning)
                    
                    items.append({
                        "id": vec_id,
                        "val": val,
                        "score": parts[3],
                        "v": parts[4],
                        "p": parts[5],
                        "reasoning": reasoning
                    })
        
        parsed_data["senses"][str(sense_num)] = {
            "title": f"The {sense_label}",
            "items": items,
            "score": sense_score
        }

    # Extract averages and totality
    averages_match = re.search(r'## Plane Average Moral Scores(.*?)(?=\n---)', content, re.DOTALL)
    if averages_match:
        avg_html = averages_match.group(1).strip()
        avg_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', avg_html)
        avg_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', avg_html)
        parsed_data["averages_html"] = avg_html.replace('\n', '<br>')

    totality_match = re.search(r'### Plane \d Totality:(.*)', content, re.DOTALL)
    if totality_match:
        tot_html = totality_match.group(1).strip()
        # Basic markdown to HTML conversion for totality
        tot_html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', tot_html)
        tot_html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', tot_html)
        tot_html = tot_html.replace('\n\n', '</p><p>').replace('\n', '<br>')
        parsed_data["totality_html"] = f"<p>{tot_html}</p>"

    return parsed_data

def generate_navbar(current_plane_num):
    nav_links = ""
    for p in PLANES:
        active_class = "bg-blue-800 text-white" if p['num'] == current_plane_num else "text-blue-100 hover:bg-blue-800 hover:text-white"
        nav_links += f'<a href="Plane_{p["num"]}_{p["name"]}.html" class="px-3 py-2 rounded-md text-sm font-medium {active_class} transition-colors">{p["id_label"]}</a>\n'

    return f"""
    <nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <span class="text-xl font-bold text-white tracking-widest">TRUMP AUDIT</span>
                    </div>
                    <div class="hidden md:block">
                        <div class="ml-10 flex items-baseline space-x-2">
                             <a href="index.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700">Final Score</a>
                            {nav_links}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    """

def get_score_color(score):
    if '+1' in score: return 'bg-green-100 text-green-800 border-green-200'
    if '-1' in score: return 'bg-red-100 text-red-800 border-red-200'
    return 'bg-gray-100 text-gray-800 border-gray-200'

def generate_html_page(plane_info, data):
    total_html = ""
    if data["totality_html"]:
        total_html = f"""
        <div class="max-w-4xl mx-auto -mt-10 mb-16 relative z-10 px-4">
            <div class="bg-white rounded-2xl p-8 md:p-12 shadow-xl ring-1 ring-gray-900/5 relative overflow-hidden">
                 <div class="relative">
                    <h2 class="text-2xl font-bold mb-6 font-serif tracking-tight text-gray-900">Plane Totality Analysis</h2>
                    <div class="prose prose-lg max-w-none text-gray-600 leading-relaxed">
                        {data["totality_html"]}
                    </div>
                    
                    <h3 class="text-xl font-bold mt-8 mb-4 font-serif text-gray-900">Plane Averages</h3>
                    <div class="bg-gray-50 p-4 rounded-lg font-mono text-sm">
                        {data["averages_html"]}
                    </div>
                 </div>
            </div>
        </div>
        """

    sense_sections = ""
    for sense_num, sense_data in data["senses"].items():
        items = sense_data["items"]
        colors = SENSE_COLORS[sense_num]
        
        table_rows = ""
        for item in items:
            score_class = get_score_color(item["score"])
            table_rows += f"""
            <tr class="hover:bg-gray-50/20 transition-colors align-top border-t border-gray-100">
                <td class="px-6 py-4 font-mono text-gray-400 text-xs font-bold w-16 align-middle">{item['id']}</td>
                <td class="px-6 py-4 w-1/3 align-middle">
                    <div class="font-bold text-gray-900 text-lg leading-tight">{item['val']}</div>
                </td>
                <td class="px-6 py-4 w-1/6 align-middle">
                    <div class="font-bold text-center text-xl p-2 rounded-lg border {score_class}">{item['score']}</div>
                </td>
                <td class="px-6 py-4 w-1/6 align-middle">
                    <div class="text-sm"><span class="font-bold text-gray-700">υ:</span> {item['v']}</div>
                    <div class="text-sm"><span class="font-bold text-gray-700">ψ:</span> {item['p']}</div>
                </td>
            </tr>
            <tr class="align-top border-b border-gray-200 last:border-0 bg-slate-50">
                <td colspan="4" class="px-6 py-4">
                    <div class="text-gray-900 leading-relaxed font-medium pl-4 border-l-4 border-slate-400">
                        <span class="font-bold text-gray-800 uppercase tracking-wider text-xs mr-2 text-slate-700">Trump Justification:</span>
                        {item['reasoning']}
                    </div>
                </td>
            </tr>
            """
        
        section_html = f"""
        <div class="mb-24">
            <div class="{colors['bg']} text-white p-6 rounded-t-2xl flex justify-between items-center sticky top-16 z-40 shadow-xl ring-1 ring-black/10">
                <div>
                    <h3 class="text-2xl font-bold tracking-tight font-serif">{sense_data['title']}</h3>
                    <div class="flex items-center mt-2 space-x-3 opacity-90">
                        <span class="{colors['text']} text-sm font-bold tracking-widest">Score: {sense_data['score']}</span>
                    </div>
                </div>
            </div>
            <div class="bg-white rounded-b-2xl shadow-sm border border-gray-200 overflow-hidden">
                <table class="min-w-full text-left border-t border-gray-100">
                    <thead>
                        <tr class="bg-gray-50">
                            <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Vector</th>
                            <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Entry</th>
                            <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider text-center">Trump Score</th>
                            <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Morals (υ, ψ)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                        {table_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """
        sense_sections += section_html

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trump Audit - Plane {plane_info['num']}: {plane_info['name']}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');
        body {{ font-family: 'Inter', sans-serif; background-color: #F8FAFC; }}
        .font-serif {{ font-family: 'Merriweather', serif; }}
    </style>
</head>
<body class="antialiased text-gray-800">

    {generate_navbar(plane_info['num'])}

    <!-- Header -->
    <header class="bg-white border-b border-gray-200 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-b from-{plane_info['color']}-50 to-white/0 pointer-events-none"></div>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative">
            <div class="text-center mb-12">
                 <div class="inline-flex h-20 w-auto px-6 bg-{plane_info['color']}-600 rounded-2xl items-center justify-center text-white text-3xl font-bold shadow-xl mb-6 ring-4 ring-{plane_info['color']}-50">
                    {plane_info['id_label']}
                 </div>
                 <h1 class="text-5xl md:text-6xl font-extrabold text-gray-900 tracking-tight mb-4">Donald Trump vs. {plane_info['name']}</h1>
                 <p class="text-xl text-gray-500 font-light max-w-2xl mx-auto">Evaluating Trump across the 49 Vectors of American {plane_info['name']}</p>
            </div>
        </div>
    </header>

    {total_html}

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {sense_sections}
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 border-t border-gray-800 text-white py-12 mt-12">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p class="text-gray-500 text-sm">generated by the psochic hegemony</p>
        </div>
    </footer>

</body>
</html>
    """
    return html

def parse_final_score(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    html_content = content
    
    # Extract tables bulletproof
    lines = content.split('\n')
    tables = []
    current_table = []
    for line in lines:
        if line.strip().startswith('|') and line.strip().endswith('|'):
            current_table.append(line)
        else:
            if current_table:
                tables.append('\n'.join(current_table))
                current_table = []
    if current_table:
        tables.append('\n'.join(current_table))
        
    for table_text in tables:
        rows = [r.strip() for r in table_text.split('\n') if r.strip()]
        if len(rows) < 3: continue # Not a valid markdown table
        
        table_html = '<div class="overflow-x-auto my-8"><table class="min-w-full bg-white shadow-sm rounded-lg overflow-hidden border border-gray-200"><thead><tr class="bg-gray-800 text-white">'
        headers = [h.strip() for h in rows[0].strip('|').split('|')]
        for h in headers: table_html += f'<th class="py-3 px-4 font-semibold text-sm text-center">{h.replace("**", "")}</th>'
        table_html += '</tr></thead><tbody class="divide-y divide-gray-200">'
        
        for row in rows[2:]:
            cells = [c.strip() for c in row.strip('|').split('|')]
            table_html += '<tr class="hover:bg-gray-50 align-top">'
            for c in cells: table_html += f'<td class="py-3 px-4 text-sm text-gray-700 text-center">{c}</td>'
            table_html += '</tr>'
        table_html += '</tbody></table></div>'
        
        html_content = html_content.replace(table_text, table_html)

    html_content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html_content)
    html_content = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html_content)
    html_content = re.sub(r'### (.*?)\n', r'<h3 class="text-xl font-bold mt-8 mb-4 font-serif text-gray-900">\1</h3>', html_content)
    html_content = re.sub(r'## (.*?)\n', r'<h2 class="text-2xl font-bold mt-6 mb-4 text-gray-900">\1</h2>', html_content)
    html_content = re.sub(r'# (.*?)\n', r'<h1 class="text-3xl font-extrabold mb-8 text-gray-900">\1</h1>', html_content)
    
    # Paragraphing
    # Split paragraphs by double newline, avoiding wrapping tags like div
    paragraphs = html_content.split('\n\n')
    formatted_paras = []
    for p in paragraphs:
        if p.strip() and not p.strip().startswith('<'):
            formatted_paras.append(f'<p class="mb-4">{p.strip()}</p>')
        else:
            formatted_paras.append(p.strip())
            
    html_content = '\n'.join(formatted_paras)
    
    return html_content

def generate_index_page(final_score_html):
    cards_html = ""
    for p in PLANES:
         cards_html += f"""
            <a href="Plane_{p['num']}_{p['name']}.html"
                class="group relative flex flex-col bg-white rounded-3xl shadow-sm hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-100 hover:border-{p['color']}-200 h-full transform hover:-translate-y-1">
                <div
                    class="absolute inset-0 bg-gradient-to-br from-{p['color']}-50/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
                </div>

                <div class="p-8 flex-1 relative z-10 flex flex-col">
                    <div class="flex items-center justify-between mb-6">
                        <span
                            class="inline-flex items-center justify-center h-12 w-12 rounded-xl bg-{p['color']}-100 text-{p['color']}-700 text-xl font-bold ring-4 ring-white shadow-sm group-hover:scale-110 transition-transform">
                            {p['num']}
                        </span>
                        <span
                            class="px-3 py-1 rounded-full text-xs font-bold bg-{p['color']}-50 text-{p['color']}-700 uppercase tracking-widest border border-{p['color']}-100 group-hover:bg-{p['color']}-100">
                            {p['id_label']}
                        </span>
                    </div>

                    <h2 class="text-3xl font-extrabold text-gray-900 mb-3 group-hover:text-{p['color']}-700 transition-colors">
                        {p['name']}
                    </h2>
                    <div class="w-12 h-1 bg-{p['color']}-500 rounded-full mb-6 group-hover:w-24 transition-all duration-300">
                    </div>
                </div>

                <div
                    class="bg-{p['color']}-50 px-8 py-4 border-t border-{p['color']}-100 flex items-center justify-between group-hover:bg-{p['color']}-100/50 transition-colors relative z-10">
                    <span class="text-{p['color']}-700 font-medium text-sm">View {p['name']} Scores</span>
                    <svg class="w-5 h-5 text-{p['color']}-500 transform group-hover:translate-x-1 transition-transform"
                        fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                </div>
            </a>
         """

    html = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Donald Trump: American Kanon Evaluation</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');

        body {{ font-family: 'Inter', sans-serif; background-color: #F8FAFC; }}
        .font-serif {{ font-family: 'Merriweather', serif; }}
    </style>
</head>

<body class="antialiased text-gray-800">

    <!-- Hero -->
    <div class="relative overflow-hidden" style="background-color: #0e1235;">
        <!-- Stylized American Flag Elements in Background -->
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20">
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 7410 3900" class="w-full h-full" preserveAspectRatio="xMidYMid slice">
                <path d="M0,0h7410v3900H0" fill="#b31942"/>
                <path d="M0,450H7410m0,600H0m0,600H7410m0,600H0m0,600H7410m0,600H0" stroke="#FFF" stroke-width="300"/>
                <path d="M0,0h2964v2100H0" fill="#0a3161"/>
            </svg>
        </div>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32 relative z-10 text-center">
            <h1
                class="text-6xl md:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-red-200 via-white to-blue-200 mb-6 tracking-tight relative drop-shadow-lg">
                DONALD TRUMP
            </h1>
            <p class="text-3xl md:text-4xl text-gray-200 font-serif italic max-w-4xl mx-auto leading-relaxed mb-6">
                "The American Anomaly"
            </p>
            <p class="text-xl text-gray-400 font-light max-w-2xl mx-auto leading-relaxed mb-8">
                Alethekanon Evaluation against the 343 Vectors of America.
            </p>
            <div class="h-1 w-32 bg-red-600 mx-auto rounded-full"></div>
        </div>
    </div>

    <!-- Matrix Explainer & Links -->
    <div class="bg-white border-b border-gray-200">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center relative">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div class="flex flex-col md:flex-row justify-between items-center">
                    <div class="mb-4 md:mb-0">
                        <a href="../AmericanMatrix.html" class="text-blue-600 hover:text-blue-800 font-medium">← Back To American Kanon Matrix</a>
                    </div>
                    <div class="flex flex-wrap justify-center gap-4 w-full sm:w-auto items-center">
                        <a class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-700 hover:bg-red-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 transition-all"
                            href="Archetype_The_American_Anomaly.html">The Archetype</a>
                        <a class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-800 hover:bg-blue-900 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all"
                            href="Trump_Hegemony_Visualization.html">The Map</a>
                        <a class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all"
                            href="About_Trump_Audit.html">Methodology</a>
                    </div>
                </div>
            </div>
            
            <div class="relative mb-8 flex flex-col items-center justify-center">
                <h2 class="text-4xl font-bold text-gray-900 font-serif mb-6">The Evaluation of the Anomaly</h2>
            </div>
            <div class="prose prose-xl mx-auto text-gray-600 leading-relaxed mb-12">
                <p class="font-medium text-gray-800">
                    This evaluation measures Donald Trump against the established 343 vectors of the American Kanon. It maps his actions, rhetoric, and systemic impact relative to the philosophical substrate of the nation.
                </p>
                <div class="flex flex-wrap justify-center gap-4 mt-8">
                    <span class="px-4 py-2 bg-gray-100 rounded-full text-sm font-bold text-gray-600 uppercase tracking-widest">7 Planes</span>
                    <span class="px-4 py-2 bg-gray-100 rounded-full text-sm font-bold text-gray-600 uppercase tracking-widest">49 Senses</span>
                    <span class="px-4 py-2 bg-gray-100 rounded-full text-sm font-bold text-gray-600 uppercase tracking-widest">343 Vectors</span>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Relative Morality Explainer -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-16 mt-16">
        <div class="bg-white rounded-2xl p-8 md:p-12 shadow-xl border border-gray-200">
            <h2 class="text-3xl font-bold text-gray-900 mb-6 font-serif text-center">Relative Morality: The Coordinate System</h2>
            <div class="flex flex-col lg:flex-row gap-12 items-center">
                <!-- Text Content -->
                <div class="flex-1 space-y-6 text-gray-700 leading-relaxed">
                    <p>
                        The evaluation uses a <strong>Vector Field</strong> defined by two axes, measuring Trump's deviation from or alignment with the ideal American vector (+1, +1):
                    </p>
                    <ul class="space-y-4">
                        <li class="flex items-start">
                            <span class="inline-flex items-center justify-center h-8 w-8 rounded-full bg-emerald-100 text-emerald-600 font-bold text-sm mr-3 mt-0.5">υ</span>
                            <div>
                                <strong class="text-gray-900 block">The Moral Vector (Universal vs Self)</strong>
                                <span class="text-sm">Does the subject's action generate <span class="text-emerald-700 font-semibold">+1 (Universal Benefit)</span> or <span class="text-red-700 font-semibold">-1 (Self Benefit)</span>?</span>
                            </div>
                        </li>
                        <li class="flex items-start">
                            <span class="inline-flex items-center justify-center h-8 w-8 rounded-full bg-emerald-100 text-emerald-600 font-bold text-sm mr-3 mt-0.5">ψ</span>
                            <div>
                                <strong class="text-gray-900 block">The Will Vector (Create vs Suppress)</strong>
                                <span class="text-sm">Is the subject acting to <span class="text-emerald-700 font-semibold">+1 (Proactive/Create)</span> or <span class="text-red-700 font-semibold">-1 (Suppressive/Prevent)</span>?</span>
                            </div>
                        </li>
                    </ul>
                </div>
                <!-- Quadrant Visual -->
                <div class="flex-1 w-full max-w-md aspect-square relative bg-gray-50 rounded-xl border border-gray-200 p-4">
                    <!-- Axes -->
                    <div class="absolute inset-x-4 top-1/2 h-px bg-gray-300"></div> <!-- X Axis -->
                    <div class="absolute inset-y-4 left-1/2 w-px bg-gray-300"></div> <!-- Y Axis -->
                    <!-- Labels -->
                    <div class="absolute top-4 left-1/2 -translate-x-1/2 -bg-white px-2 text-xs font-bold text-emerald-700">CREATE (+ψ)</div>
                    <div class="absolute bottom-4 left-1/2 -translate-x-1/2 -bg-white px-2 text-xs font-bold text-red-700">SUPPRESS (-ψ)</div>
                    <div class="absolute left-4 top-1/2 -translate-y-1/2 -bg-white px-2 text-xs font-bold text-emerald-700">UNIVERSAL (+υ)</div>
                    <div class="absolute right-4 top-1/2 -translate-y-1/2 -bg-white px-2 text-xs font-bold text-red-700">SELF (-υ)</div>
                    <!-- Quadrants -->
                    <div class="grid grid-cols-2 grid-rows-2 h-full w-full pt-6 pb-6 pl-6 pr-6 gap-2">
                        <!-- TL: Greater Good -->
                        <div class="bg-emerald-100/50 rounded-lg flex items-center justify-center text-center p-2 border border-emerald-100">
                            <div>
                                <div class="font-bold text-emerald-900 text-sm">Greater Good</div>
                                <div class="text-[10px] text-emerald-700 font-mono">+υ, +ψ</div>
                            </div>
                        </div>
                        <!-- TR: Greatest Lie -->
                        <div class="bg-amber-100/50 rounded-lg flex items-center justify-center text-center p-2 border border-amber-100">
                            <div>
                                <div class="font-bold text-amber-900 text-sm">Greatest Lie</div>
                                <div class="text-[10px] text-amber-700 font-mono">-υ, +ψ</div>
                            </div>
                        </div>
                        <!-- BL: Lesser Good -->
                        <div class="bg-blue-100/50 rounded-lg flex items-center justify-center text-center p-2 border border-blue-100">
                            <div>
                                <div class="font-bold text-blue-900 text-sm">Lesser Good</div>
                                <div class="text-[10px] text-blue-700 font-mono">+υ, -ψ</div>
                            </div>
                        </div>
                        <!-- BR: Greater Evil -->
                        <div class="bg-red-100/50 rounded-lg flex items-center justify-center text-center p-2 border border-red-100">
                            <div>
                                <div class="font-bold text-red-900 text-sm">The Void</div>
                                <div class="text-[10px] text-red-700 font-mono">-υ, -ψ</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <h3 class="text-3xl font-extrabold text-gray-900 mb-8 text-center font-serif">The 7 Planes of Evaluation</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {cards_html}
        </div>
    </div>
    
    <!-- Final Score Explainer (Moved to Bottom) -->
    <div class="bg-gray-50 border-t border-b border-gray-200 mt-20">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-gray-800 prose prose-lg max-w-none">
            {final_score_html}
        </div>
    </div>

    <footer class="bg-gray-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p class="text-gray-500 text-sm">generated by the psochic hegemony</p>
        </div>
    </footer>
</body>
</html>
    """
    return html

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Starting Trump Evaluation Website Generation...")
    
    for p in PLANES:
        filepath = os.path.join(SOURCE_DIR, p['file'])

        print(f"Parsing {p['name']} from {filepath}...")
        
        if os.path.exists(filepath):
            data = parse_markdown_file(filepath)
            html = generate_html_page(p, data)
            
            out_file = os.path.join(OUTPUT_DIR, f"Plane_{p['num']}_{p['name']}.html")
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"Generated {out_file}")
        else:
            print(f"ERROR: File not found: {filepath}")

    print("Generating Index...")
    final_score_file = os.path.join(SOURCE_DIR, "Trump_American_Kanon_Final_Score.md")
    if os.path.exists(final_score_file):
        final_score_html = parse_final_score(final_score_file)
        index_html = generate_index_page(final_score_html)
        with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
            f.write(index_html)
        print("Generated index.html")
    else:
        print(f"ERROR: Final score file not found: {final_score_file}")
        
    print("Done!")
