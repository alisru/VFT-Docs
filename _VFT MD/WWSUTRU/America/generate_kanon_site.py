import re
import os
import glob
from pathlib import Path

# --- Configuration ---
SOURCE_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America"
OUTPUT_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\America\site"
PLANES = [
    {"num": 1, "id_label": "Who", "name": "Identity", "file": "American_Kanon_Plane_1_Identity.md", "color": "red"},
    {"num": 2, "id_label": "What", "name": "Definition", "file": "American_Kanon_Plane_2_Definition.md", "color": "amber"},
    {"num": 3, "id_label": "Where", "name": "Land", "file": "American_Kanon_Plane_3_Land.md", "color": "blue"},
    {"num": 4, "id_label": "Why", "name": "Drive", "file": "American_Kanon_Plane_4_Drive.md", "color": "green"},
    {"num": 5, "id_label": "How", "name": "Method", "file": "American_Kanon_Plane_5_Method.md", "color": "indigo"},
    {"num": 6, "id_label": "Cause", "name": "Foundation", "file": "American_Kanon_Plane_6_Cause.md", "color": "purple", "totality_name": "Cause"},
    {"num": 7, "id_label": "Effect", "name": "Result", "file": "American_Kanon_Plane_7_Effect.md", "color": "gray", "totality_name": "Effect"},
]

SENSE_COLORS = {
    "q1": {"bg": "bg-red-900", "text": "text-red-200", "badge": "bg-red-800", "icon": "text-red-600", "border": "border-red-200", "light_bg": "bg-red-50"},
    "q2": {"bg": "bg-blue-900", "text": "text-blue-200", "badge": "bg-blue-800", "icon": "text-blue-600", "border": "border-blue-200", "light_bg": "bg-blue-50"},
    "q3": {"bg": "bg-amber-600", "text": "text-amber-100", "badge": "bg-amber-500", "icon": "text-amber-600", "border": "border-amber-200", "light_bg": "bg-amber-50"},
    "q4": {"bg": "bg-green-700", "text": "text-green-100", "badge": "bg-green-600", "icon": "text-green-600", "border": "border-green-200", "light_bg": "bg-green-50"},
    "q5": {"bg": "bg-indigo-700", "text": "text-indigo-200", "badge": "bg-indigo-600", "icon": "text-indigo-600", "border": "border-indigo-200", "light_bg": "bg-indigo-50"},
    "q6": {"bg": "bg-purple-800", "text": "text-purple-200", "badge": "bg-purple-700", "icon": "text-purple-600", "border": "border-purple-200", "light_bg": "bg-purple-50"},
    "q7": {"bg": "bg-gray-800", "text": "text-gray-400", "badge": "bg-gray-700", "icon": "text-gray-600", "border": "border-gray-200", "light_bg": "bg-gray-50"},
}

# --- Parsing Logic ---

def parse_markdown_file(filepath):
    """
    Parses a Plane markdown file into a structured dictionary.
    Returns: { 
        'meta_quote': str, 
        'total_narrative': str,
        'senses': { 'q1': {items: [], narrative: str}, ... }
    }
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by Sense Headers (### Sense q1...)
    sense_blocks = re.split(r'### Sense (q\d):', content)
    
    parsed_data = {
        "meta_quote": "",
        "total_narrative": "",
        "senses": {}
    }
    
    # 1. Parse Preamble (Meta Quote)
    preamble = sense_blocks[0]
    # Look for blockquotes in preamble
    # Regex: Capture lines starting with >
    meta_matches = re.findall(r'^> (.*)', preamble, re.MULTILINE)
    parsed_data["meta_quote"] = "\n".join(meta_matches).strip()

    if len(sense_blocks) < 2:
        print(f"Warning: No senses found in {filepath}")
        return parsed_data

    # Iterate Blocks
    for i in range(1, len(sense_blocks), 2):
        sense_key = sense_blocks[i]
        raw_content = sense_blocks[i+1]
        
        # Extract Sense Title
        lines = raw_content.split('\n')
        sense_title = lines[0].strip()
        
        # Rest of content
        sense_body = "\n".join(lines[1:])
        
        # Extract Narrative (at the end usually, starting with > **The Narrative)
        # We split by the Narrative Header to separate items from narrative
        narrative_text = ""
        narrative_match = re.search(r'(> \*\*The Narrative.*?)(?=\n###|\Z)', sense_body, re.DOTALL)
        if narrative_match:
             narrative_block = narrative_match.group(1)
             # Clean up the > chars
             narrative_lines = [line.replace('> ', '', 1) for line in narrative_block.split('\n') if line.strip().startswith('>')]
             narrative_text = "\n".join(narrative_lines)
             # Remove narrative from body for item parsing
             sense_body = sense_body.replace(narrative_block, "")
        
        # Parse items
        # New Pattern: (Label) Value; "Quote" - Author. Source
        items = []
        # Regex: 
        # \(([\w.]+)\)    -> (Who.Who.Who) -> Group 1 (ID/Label)
        # \s*             -> space
        # (.*?);          -> Value (Lazy match until ;) -> Group 2 (Value)
        # \s*"            -> space "
        # (.*?)"          -> Quote -> Group 3
        # \s*-\s*         ->  - 
        # (.*?)           -> Author -> Group 4
        # (\n|$)          -> Line end
        # ([\s\S]*?)      -> Description Body -> Group 6
        # (?=\n\(|$)      -> Lookahead for next item starting with ( or EOF
        
        item_matches = re.finditer(r'\(([\w.]+)\)\s*(.*?);\s*"(.*?)"\s*-\s*(.*?)(\n|$)([\s\S]*?)(?=\n\(|$)', sense_body)
        
        for match in item_matches:
            num = match.group(1)   # Who.Who.Who
            label = match.group(1) # Who.Who.Who
            val_name = match.group(2).strip() # Self-Evidence
            quote = match.group(3)
            source_line = match.group(4).strip()
            raw_desc = match.group(6).strip()
            
            clean_desc = "\n".join([line.strip() for line in raw_desc.split('\n')])
            paras = [p.strip() for p in re.split(r'\n{2,}', clean_desc) if p.strip()]
            
            context = paras[0] if len(paras) > 0 else "No context found."
            meaning = paras[1] if len(paras) > 1 else ""
            if len(paras) > 2: meaning = "\n\n".join(paras[1:])
            
            items.append({
                "id": num,
                "label": label,
                "val": val_name,
                "quote": quote,
                "source": source_line,
                "ctx": context,
                "meaning": meaning
            })
            
        parsed_data["senses"][sense_key] = {
            "title": sense_title,
            "items": items,
            "narrative": narrative_text
        }

    # Extract Total Narrative (Looking for the summary block at the very end of file)
    summary_match = re.search(r'(?:### \*\*Summary.*?\n)?((?:> .*\n?)+)\s*\Z', content)
    if summary_match:
        raw_summary = summary_match.group(1)
        parsed_data["total_narrative"] = re.sub(r'^> ', '', raw_summary, flags=re.MULTILINE).strip()

    return parsed_data

# --- HTML Generation ---

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
                        <span class="text-xl font-bold text-white tracking-widest">WWSUTRU</span>
                    </div>
                    <div class="hidden md:block">
                        <div class="ml-10 flex items-baseline space-x-2">
                             <a href="index.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700">Home</a>
                            {nav_links}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    """

def generate_html_page(plane_info, data):
    """Generates the full HTML page for a Plane."""
    
    # Total Narrative (Moved to Top)
    total_html = ""
    if data["total_narrative"]:
        total_html = f"""
        <div class="max-w-4xl mx-auto -mt-10 mb-16 relative z-10 px-4">
            <div class="bg-white rounded-2xl p-8 md:p-12 shadow-xl ring-1 ring-gray-900/5 relative overflow-hidden">
                 <div class="absolute top-0 right-0 w-64 h-64 bg-{plane_info['color']}-50 rounded-full mix-blend-multiply filter blur-3xl opacity-70 -mr-32 -mt-32"></div>
                 <div class="absolute bottom-0 left-0 w-64 h-64 bg-gray-50 rounded-full mix-blend-multiply filter blur-3xl opacity-70 -ml-32 -mb-32"></div>
                 <div class="relative">
                    <h2 class="text-2xl font-bold mb-6 font-serif tracking-tight text-gray-900">The Totality of American {plane_info.get('totality_name', plane_info['name'])}</h2>
                    <div class="prose prose-lg max-w-none text-gray-600 leading-relaxed">
                        {data['total_narrative'].replace('**', '<strong>').replace('\n', '<br>')}
                    </div>
                 </div>
            </div>
        </div>
        """

    sense_sections = ""
    
    for q_key in ["q1", "q2", "q3", "q4", "q5", "q6", "q7"]:
        if q_key not in data["senses"]:
            continue
            
        sense_data = data["senses"][q_key]
        items = sense_data["items"]
        colors = SENSE_COLORS[q_key]
        narrative = sense_data["narrative"]
        
        # Build Table Rows
        table_rows = ""
        for item in items:
            analysis_html = f'<div class="space-y-2 mt-3"><p class="text-gray-700 leading-relaxed">{item["ctx"]}</p>'
            if item['meaning']:
                analysis_html += f'<p class="text-gray-900 font-medium bg-gray-50 p-3 rounded-lg border border-gray-100 shadow-sm">{item["meaning"]}</p>'
            analysis_html += '</div>'

            table_rows += f"""
            <tr class="hover:bg-gray-50/50 transition-colors align-top border-b border-gray-100 last:border-0">
                <td class="px-6 py-6 font-mono text-gray-400 text-xs font-bold w-16 align-top pt-7">{item['id']}</td>
                <td class="px-6 py-6 w-1/4 align-top">
                    <div class="font-bold text-gray-900 text-lg leading-tight mb-1">{item['val']}</div>
                    <div class="text-xs text-blue-600 font-mono bg-blue-50 inline-block px-1.5 py-0.5 rounded">{item['label']}</div>
                </td>
                <td class="px-6 py-6 align-top">
                    <div class="mb-4">
                        <div class="text-lg italic text-gray-800 font-serif leading-relaxed">
                            "{item['quote']}"
                        </div>
                        <div class="mt-2 flex items-center">
                            <div class="h-px bg-gray-200 w-8 mr-3"></div>
                            <span class="text-xs text-gray-500 font-semibold uppercase tracking-wide">{item['source']}</span>
                        </div>
                    </div>
                    {analysis_html}
                </td>
            </tr>
            """
        
        # Narrative Card
        narrative_html = ""
        if narrative:
            # Fix: Use <strong> for bold terms to keep them inline, not block
            formatted_narrative = narrative.replace('**', '') 
            # We want to bold the terms that were wrapped in **, but specific logic depends on input.
            # Actually, the previous logic was replacing ** with a span. 
            # If the input is "**Term**", split simple replacement is risky.
            # Let's use regex for safer bolding if possible, or just standard markdown parsing.
            # Simple approach: Re-implement bolding without 'block'
            
            # The input text has **Term**. We want <strong>Term</strong>.
            # The previous code did: narrative.replace('**', '<span>...').
            # We will use re.sub for cleaner replacement.
            formatted_narrative = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-gray-900 font-bold">\1</strong>', narrative)
            
            # Extract the title if it exists (The part before the first newline or :)
            # The narrative usually starts with "The Narrative of X (The Y of Z):"
            # We can style that distinctively if we want, or just let it flow.
            
            narrative_html = f"""
            <div class="bg-gradient-to-br from-white to-{colors['light_bg'].replace('bg-', '')} border-x border-b border-gray-200 p-8 relative overflow-hidden group">
                <div class="absolute top-0 right-0 w-32 h-32 {colors['bg']} opacity-[0.03] rounded-bl-full -mr-8 -mt-8 transition-opacity group-hover:opacity-[0.08]"></div>
                <div class="relative z-10">
                     <div class="prose prose-lg max-w-none text-gray-700 leading-relaxed font-serif">
                        {formatted_narrative.replace('\n', '<br>')}
                     </div>
                </div>
            </div>
            """

        # Build Section
        section_html = f"""
        <!-- Sense {q_key} -->
        <div class="mb-24">
            <div class="{colors['bg']} text-white p-6 rounded-t-2xl flex justify-between items-center sticky top-16 z-40 shadow-xl ring-1 ring-black/10">
                <div>
                    <h3 class="text-2xl font-bold tracking-tight font-serif">{sense_data['title']}</h3>
                    <div class="flex items-center mt-2 space-x-3 opacity-90">
                        <span class="{colors['text']} text-xs uppercase tracking-widest font-bold">Sense {q_key}</span>
                        <span class="w-1 h-1 bg-white rounded-full opacity-50"></span>
                        <span class="text-xs font-mono opacity-80">{len(items)} Vectors</span>
                    </div>
                </div>
            </div>
            
            <div class="bg-white rounded-b-2xl shadow-sm border border-gray-200 overflow-hidden">
                <!-- Narrative Section at Top -->
                {narrative_html}
                
                <table class="min-w-full text-left border-t border-gray-100">
                    <tbody class="divide-y divide-gray-100">
                        {table_rows}
                    </tbody>
                </table>
            </div>
        </div>
        """
        sense_sections += section_html

    # Meta Quote
    meta_html = ""
    if data["meta_quote"]:
        # Simple parsing for author separation if present
        parts = data['meta_quote'].split('\n')
        quote_text = parts[0].replace('*', '').replace('"', '').strip()
        author_text = parts[1].replace('—', '').replace('*', '').strip() if len(parts) > 1 else ""
        
        meta_html = f"""
        <div class="max-w-3xl mx-auto text-center py-10">
            <blockquote class="text-2xl md:text-3xl font-serif italic text-gray-700 leading-normal mb-4">
                "{quote_text}"
            </blockquote>
            <cite class="text-sm font-bold text-gray-500 uppercase tracking-widest not-italic">
                — {author_text}
            </cite>
        </div>
        """
    
    # Full Page HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plane {plane_info['num']}: Values of American {plane_info['name']}</title>
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
                 <h1 class="text-5xl md:text-6xl font-extrabold text-gray-900 tracking-tight mb-4">Values of American {plane_info['name']}</h1>
                 <p class="text-xl text-gray-500 font-light max-w-2xl mx-auto">Analysis of the 49 Vectors of {plane_info['name']}</p>
            </div>
            {meta_html}
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

def generate_index_page():
    # Build Cards HTML
    cards_html = ""
    for p in PLANES:
         # Descriptions based on the user's index.html content
         description = ""
         if p['num'] == 1: description = "The Agent and their character; the metaphysical definition of the self."
         elif p['num'] == 2: description = "The concepts and roles regarding the State and Society." # Definition (New Plane 2)
         elif p['num'] == 3: description = "The physical and spatial environment; the geography of the nation." # Land (New Plane 3)
         elif p['num'] == 4: description = "The motivations and will that propel the nation forward."
         elif p['num'] == 5: description = "The operational logic and techniques used to achieve the Drive."
         elif p['num'] == 6: description = "The Service/Historical Origins and Ancestors."
         elif p['num'] == 7: description = "The legacy, impact, and final status of the American experiment."
         
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
                    <p class="text-gray-600 font-medium text-sm flex-1 leading-relaxed">
                        {description}
                    </p>
                </div>

                <div
                    class="bg-{p['color']}-50 px-8 py-4 border-t border-{p['color']}-100 flex items-center justify-between group-hover:bg-{p['color']}-100/50 transition-colors relative z-10">
                    <span class="text-{p['color']}-700 font-medium text-sm">Explore {p['id_label']}</span>
                    <svg class="w-5 h-5 text-{p['color']}-500 transform group-hover:translate-x-1 transition-transform"
                        fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                </div>
            </a>
         """

    # Build Full HTML
    # Note: Added US Flag SVG background behind title
    html = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The American Kanon</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Merriweather:ital,wght@0,300;0,400;0,700;1,300;1,400&display=swap');

        body {{
            font-family: 'Inter', sans-serif;
            background-color: #F8FAFC;
        }}

        .font-serif {{
            font-family: 'Merriweather', serif;
        }}
    </style>
</head>

<body class="antialiased text-gray-800">

    <!-- Hero -->
    <div class="relative bg-gray-900 overflow-hidden">
        <!-- American Flag Background -->
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20">
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 7410 3900" class="w-full h-full" preserveAspectRatio="xMidYMid slice">
                <path d="M0,0h7410v3900H0" fill="#b31942"/>
                <path d="M0,450H7410m0,600H0m0,600H7410m0,600H0m0,600H7410m0,600H0" stroke="#FFF" stroke-width="300"/>
                <path d="M0,0h2964v2100H0" fill="#0a3161"/>
                <g fill="#FFF">
                <g id="s18">
                <g id="s9">
                <g id="s5">
                <g id="s4">
                <path id="s" d="M247,90 317.534230,307.082039 132.873218,172.917961H361.126782L176.465770,307.082039z"/>
                <use xlink:href="#s" y="420"/>
                <use xlink:href="#s" y="840"/>
                <use xlink:href="#s" y="1260"/>
                </g>
                <use xlink:href="#s" y="1680"/>
                </g>
                <use xlink:href="#s4" x="247" y="210"/>
                </g>
                <use xlink:href="#s9" x="494"/>
                </g>
                <use xlink:href="#s18" x="988"/>
                <use xlink:href="#s9" x="1976"/>
                <use xlink:href="#s5" x="2470"/>
                </g>
            </svg>
        </div>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32 relative z-10 text-center">
            <h1
                class="text-6xl md:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-200 via-white to-red-200 mb-6 tracking-tight relative">
                AMERICAN KANON
            </h1>
            <p class="text-2xl md:text-3xl text-gray-400 font-light max-w-4xl mx-auto leading-relaxed mb-8">
                The 343 Vectors of the National Soul
            </p>
            <div class="h-1 w-32 bg-blue-500 mx-auto rounded-full"></div>
        </div>
    </div>

    <!-- Matrix Explainer -->
    <div class="bg-white border-b border-gray-200">
        <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">

            <h2 class="text-4xl font-bold text-gray-900 mb-8 font-serif">Defining the Ideological American</h2>

            <div class="prose prose-xl mx-auto text-gray-600 leading-relaxed mb-12">
                <p class="font-medium text-gray-800">
                    An examination of the ideological American over history, to define what "American" means
                    irrespective of political or economic ideology, purely based on the intention of its founders and
                    its motivating members through history.
                </p>
                <p>
                    This is not a political platform but a metaphysical map. The American Kanon utilizes the
                    <strong>Vector Field Theory (VFT)</strong> to generate a <strong>343-Point Matrix</strong> (7 Planes
                    × 7 Senses × 7 Vectors) that captures the total holographic complexity of the nation. It ignores the
                    transient noise of current events to focus on the <strong>Motivating Members</strong>—the
                    architects, poets, and citizens who have actively shaped the trajectory of the country. By aligning
                    with their original intent, we reveal the structural 'Standard' of the American experiment.
                </p>
            </div>

            <div class="flex flex-wrap justify-center gap-4">
                <span
                    class="px-4 py-2 bg-gray-100 rounded-full text-sm font-bold text-gray-600 uppercase tracking-widest">7
                    Planes</span>
                <span
                    class="px-4 py-2 bg-gray-100 rounded-full text-sm font-bold text-gray-600 uppercase tracking-widest">49
                    Senses</span>
                <span
                    class="px-4 py-2 bg-gray-100 rounded-full text-sm font-bold text-gray-600 uppercase tracking-widest">343
                    Vectors</span>
            </div>

        </div>
    </div>

    <!-- Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {cards_html}
        </div>
    </div>

    <footer class="bg-white border-t border-gray-100 py-12 mt-12">
        <div class="text-center text-gray-400 text-sm">
            <p>&copy; 2024 The Psochic Hegemony. All rights reserved.</p>
        </div>
    </footer>
</body>

</html>
    """
    return html

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("Starting American Kanon Website Generation...")
    
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
    index_html = generate_index_page()
    with open(os.path.join(OUTPUT_DIR, "index.html"), 'w', encoding='utf-8') as f:
        f.write(index_html)
        
    print("Done!")
