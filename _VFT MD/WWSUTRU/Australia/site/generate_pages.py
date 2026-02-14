"""
Australian Kanon Full HTML Generator v2
Converts Australian Kanon markdown files to COMPLETE HTML pages with all 49 vectors per plane.
Uses the user-corrected Plane 1 template format.
"""

import re
import os
import html

INPUT_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia"
OUTPUT_DIR = r"e:\Vector Field Theory\VFT Docs\_VFT MD\WWSUTRU\Australia\site"

# Map special characters to HTML entities if needed, but UTF-8 should handle it
# Ensure we handle ± correctly

PLANES = [
    {"num": 1, "name": "Identity", "label": "Who", "plane_label": "Who"},
    {"num": 2, "name": "Definition", "label": "What", "plane_label": "What"},
    {"num": 3, "name": "Land", "label": "Where", "plane_label": "Where"},
    {"num": 4, "name": "Drive", "label": "Why", "plane_label": "Why"},
    {"num": 5, "name": "Method", "label": "How", "plane_label": "How"},
    {"num": 6, "name": "Foundation", "label": "Cause", "plane_label": "Cause"},
    {"num": 7, "name": "Result", "label": "Effect", "plane_label": "Effect"},
]

SENSE_COLORS = ["yellow", "amber", "green", "teal", "blue", "indigo", "purple"]
SENSE_LABELS = [
    ("Who", "Authenticity/Soul"),
    ("What", "Roles/Titles"),
    ("Where", "Origins/Location"),
    ("Why", "Motivations/Drive"),
    ("How", "Methods/Character"),
    ("Cause", "Roots/History"),
    ("Effect", "Legacy/Impact"),
]


def escape_html(text):
    """Escape HTML special characters."""
    return html.escape(text) if text else ""

def format_md(text):
    """Convert basic markdown to HTML."""
    if not text: return ""
    text = html.escape(text) # Escape mostly everything first
    # Bold first
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italics second
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    return text

def parse_vectors_from_markdown(content):
    """Parse all vectors from markdown content."""
    vectors = []
    
    # Find all vector entries - they start with **(Code.Code.Code) Name**;
    # Then have a quote, source, and paragraphs
    pattern = r'\*\*\(([A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+)\)\s+([^*]+)\*\*;\s*"([^"]+)"'
    
    for match in re.finditer(pattern, content):
        code = match.group(1).strip()
        name_raw = match.group(2).strip()
        quote = match.group(3).strip()

        # Check for First Nations identifier
        is_fn = "[First Nations Perspective]" in name_raw
        name = name_raw.replace("[First Nations Perspective]", "").strip()
        
        # Find the block following this vector
        start_pos = match.end()
        next_vector = re.search(r'\*\*\([A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+\)', content[start_pos:])
        end_pos = start_pos + next_vector.start() if next_vector else len(content)
        block = content[start_pos:end_pos]
        
        # Truncate block at Narrative or Separator to prevent inclusion in the vector
        narrative_match = re.search(r'\n>\s*\*\*The Narrative of', block)
        if narrative_match:
            block = block[:narrative_match.start()]
            
        separator_match = re.search(r'\n---', block)
        if separator_match:
            block = block[:separator_match.start()]
            
        header_match = re.search(r'\n##', block)
        if header_match:
            block = block[:header_match.start()]
        
        # Extract source - distinct line starting with - or —
        source = ""
        source_line_match = re.search(r'[-—]\s*(.+?)(?=\n|$)', block[:500])
        
        if source_line_match:
            raw_source = source_line_match.group(1).strip()
            # Apply formatting (convert ** to <b>, * to <i>)
            source = format_md(raw_source)
        else:
            if "First Nations Perspective" in block[:150]:
                 source = "First Nations Perspective"
        
        if not source and "First Nations Perspective" in block[:150]:
             source = "First Nations Perspective"
        
        # Extract context - look for indented paragraphs
        # First indented paragraph (4 spaces or tab at start of line)
        context_match = re.search(r'\n\s{4}(.+?)(?=\n\s{4}This establishes|\n\s*\n|\Z)', block, re.DOTALL)
        context = context_match.group(1).strip() if context_match else ""
        
        # Extract role (paragraph starting with "This establishes")
        role_match = re.search(r'This establishes[^\*]*\*\*([^*]+)\*\*', block)
        role_name = role_match.group(1).strip() if role_match else ("Perspective" if is_fn else name)
        
        # Get full role text
        role_text_match = re.search(r'(This establishes[^.]+\*\*[^*]+\*\*(?:\.|[^.]*\.)\s*)([^>]*?)(?=\n\s*\n|\n\s*>|\Z)', block, re.DOTALL)
        if role_text_match:
            role_text = role_text_match.group(0).strip()
            role_text = re.sub(r'\s+', ' ', role_text)
        else:
            role_text = ""
        
        vectors.append({
            'code': code,
            'name': name,
            'is_fn': is_fn,
            'quote': quote,
            'source': source,
            'context': context.replace('\n', ' ').strip()[:1000],  # Limit context length
            'role_name': role_name,
            'role_text': role_text,
        })
    
    return vectors


def parse_sense_narratives(content):
    """Extract sense narratives from markdown."""
    narratives = {}
    
    # Pattern for sense narratives
    pattern = r'>\s*\*\*The Narrative of ([^(]+)\(The (\w+) of[^)]+\):\*\*\s*>\s*(.+?)(?=\n\n---|\n\n##|\Z)'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        sense_name = match.group(1).strip()
        sense_label = match.group(2).strip()
        narrative = match.group(3).strip()
        
        # Clean up narrative - remove > prefixes
        narrative = re.sub(r'>\s*', ' ', narrative)
        narrative = re.sub(r'\s+', ' ', narrative).strip()
        
        # Convert **text** to <strong>
        narrative = re.sub(r'\*\*([^*]+)\*\*', r'<strong class="text-gray-900 font-bold">\1</strong>', narrative)
        
        narratives[sense_label] = narrative
    
    return narratives


def parse_totality(content):
    """Extract the totality narrative."""
    # Find the last "The Totality" blockquote
    pattern = r'>\s*\*\*The Totality of[^*]+\*\*\s*(.+?)(?=\n\n|\Z)'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    if matches:
        totality = matches[-1].group(0)
        # Clean up
        totality = re.sub(r'^>\s*', '', totality, flags=re.MULTILINE)
        totality = re.sub(r'\s+', ' ', totality).strip()
        # Convert **text** to <strong>
        totality = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', totality)
        return totality
    
    return ""


def parse_header_quote(content):
    """Extract the header quote."""
    pattern = r'>\s*\*"([^"]+)"\*\s*>\s*—\s*\*\*([^*]+)\*\*,?\s*\*([^*]+)\*(?:,?\s*(\d{4}))?'
    match = re.search(pattern, content)
    
    if match:
        return {
            'text': match.group(1).strip(),
            'author': match.group(2).strip(),
            'work': match.group(3).strip(),
            'year': match.group(4).strip() if match.group(4) else ""
        }
    
    return {'text': '', 'author': '', 'work': '', 'year': ''}


def parse_judgment_vectors(plane_num, plane_name):
    """Parse judgment vectors from the shadow _JUDGMENT.md file."""
    judgment_file = os.path.join(INPUT_DIR, f"Australian_Kanon_Plane_{plane_num}_{plane_name}_JUDGMENT.md")
    
    judgments = {}
    
    if not os.path.exists(judgment_file):
        print(f"  Warning: No Judgment file found: {judgment_file}")
        return judgments
        
    with open(judgment_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Regex to parse the table rows
    # | Who.Who.Who | **Mateship** | +0.7 | +0.4 | **Greater Good** — Note |
    pattern = r'\|\s*([A-Za-z]+\.[A-Za-z]+\.[A-Za-z]+)\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*([+\-±]?\d+(?:\.\d+)?)\s*\|\s*([+\-±]?\d+(?:\.\d+)?)\s*\|\s*\*\*([^*]+)\*\*\s*(?:—|-|–)\s*([^|]+)\s*\|'
    
    matches = list(re.finditer(pattern, content))
    print(f"  Found {len(matches)} judgment entries in shadow file.")

    for match in matches:
        code = match.group(1).strip()
        val_u = match.group(3).strip()
        val_p = match.group(4).strip()
        label = match.group(5).strip()
        note = match.group(6).strip()
        
        # Determine badge colors based on label
        bg_color = "bg-slate-100"
        text_color = "text-slate-800"
        border_color = "border-slate-200"
        
        l_lower = label.lower()
        if "greater good" in l_lower:
            bg_color = "bg-emerald-100"
            text_color = "text-emerald-800"
            border_color = "border-emerald-200"
        elif "lesser good" in l_lower:
             bg_color = "bg-emerald-50"
             text_color = "text-emerald-800"
             border_color = "border-emerald-100"
        elif "good" in l_lower:
            bg_color = "bg-emerald-100"
            text_color = "text-emerald-800"
            border_color = "border-emerald-200"
        elif "greatest lie" in l_lower:
            bg_color = "bg-red-100"
            text_color = "text-red-900"
            border_color = "border-red-200"
        elif "tension point" in l_lower:
            bg_color = "bg-orange-100"
            text_color = "text-orange-800"
            border_color = "border-orange-200"
        elif "constraint" in l_lower:
             bg_color = "bg-gray-100"
             text_color = "text-gray-800"
             border_color = "border-gray-200"

        judgments[code] = {
            'val_u': val_u,
            'val_p': val_p,
            'label': label,
            'note': note,
            'style': {
                'bg': bg_color,
                'text': text_color,
                'border': border_color
            }
        }
    
    return judgments


def generate_vector_row_html(vector, color, is_fn=False, judgment=None):
    """Generate HTML for a single vector row (Standard or FN)."""
    code = escape_html(vector['code'])
    name = escape_html(vector['name'])
    quote = format_md(vector['quote'])
    source = vector['source'] # Already formatted
    context = format_md(vector['context'])
    role_name = escape_html(vector['role_name'])
    role_text = format_md(vector['role_text'])

    row_class = "hover:bg-gray-50/50 transition-colors align-top border-b border-gray-100 last:border-0"
    
    judgment_html = ""
    if judgment:
        j = judgment
        # Color for the numbers (Green/Red/Gray based on sign)
        # Simple heuristic: + is emerald, - is red, ± is gray
        u_col = "text-emerald-600" if "+" in j['val_u'] else ("text-red-600" if "-" in j['val_u'] else "text-gray-500")
        p_col = "text-emerald-600" if "+" in j['val_p'] else ("text-red-600" if "-" in j['val_p'] else "text-gray-500")

        judgment_html = f'''
        <div class="mt-2 flex flex-wrap items-center gap-2 judgment-badge">
            <div class="inline-flex items-center space-x-1.5 px-2 py-1 bg-slate-50 border border-slate-200 rounded-md text-xs font-mono">
                <span class="font-semibold text-gray-500" title="Moral Vector (Benefit vs Cost)">υ</span>
                <span class="{u_col} font-bold">{j['val_u']}</span>
                <span class="text-gray-300">|</span>
                <span class="font-semibold text-gray-500" title="Will Vector (Proactive vs Suppressive)">ψ</span>
                <span class="{p_col} font-bold">{j['val_p']}</span>
            </div>
            <span class="inline-block px-2 py-0.5 text-xs font-bold rounded border {j['style']['bg']} {j['style']['text']} {j['style']['border']}">{j['label']}</span>
        </div>
        <div class="mt-1.5 text-xs text-gray-500 italic leading-snug w-full judgment-note">{j['note']}</div>
        '''

    # Distinct styling for FN rows
    if is_fn:
         row_class = "bg-amber-50/30 hover:bg-amber-50/60 transition-colors align-top border-b border-amber-100 last:border-0"
         code_col = "" # Empty code col for FN
         meta_col = f'''
             <div class="font-bold text-gray-900 text-lg leading-tight mb-1">{name}</div>
             <div class="text-xs text-amber-800 font-mono bg-amber-100 inline-block px-1.5 py-0.5 rounded">First Nations Perspective</div>
             {judgment_html}
         '''
    else:
        # Standard Colonial Row
         code_col = f'<div class="font-mono text-gray-400 text-xs font-bold w-16 align-top pt-7">{code}</div>'
         meta_col = f'''
             <div class="font-bold text-gray-900 text-lg leading-tight mb-1">{name}</div>
             <div class="text-xs text-{color}-600 font-mono bg-{color}-50 inline-block px-1.5 py-0.5 rounded">The {role_name}</div>
             {judgment_html}
         '''

    return f'''
                        <tr class="{row_class}">
                            <td class="px-6 py-6 md:w-16 align-top pt-7">{code_col}</td>
                            <td class="px-6 py-6 md:w-1/4 align-top">
                                {meta_col}
                            </td>
                            <td class="px-6 py-6 align-top">
                                <div class="mb-4">
                                    <div class="text-lg italic text-gray-800 font-serif leading-relaxed">"{quote}"</div>
                                    <div class="mt-2 flex items-center">
                                        <div class="h-px bg-gray-200 w-8 mr-3"></div>
                                        <span class="text-xs text-gray-500 font-semibold uppercase tracking-wide">{source}</span>
                                    </div>
                                </div>
                                <div class="space-y-2 mt-3">
                                    <p class="text-gray-700 leading-relaxed">{context}</p>
                                    <p class="text-gray-900 font-medium bg-gray-50 p-3 rounded-lg border border-gray-100 shadow-sm">{role_text}</p>
                                </div>
                            </td>
                        </tr>'''


def generate_sense_section(sense_idx, sense_vectors_group, narrative, plane_label, color):
    """Generate HTML for a complete sense section."""
    sense_label, sense_desc = SENSE_LABELS[sense_idx]
    
    rows_html = []
    
    # Process vectors in pairs
    seen_codes = []
    
    # First, organise vectors by code
    vectors_by_code = {}
    for v in sense_vectors_group:
        if v['code'] not in vectors_by_code:
            vectors_by_code[v['code']] = []
        vectors_by_code[v['code']].append(v)
        
    # Now generate rows keys in original order
    for v in sense_vectors_group:
        if v['code'] in seen_codes:
            continue
        
        seen_codes.append(v['code'])
        group = vectors_by_code[v['code']]
        
        # Find Standard and FN
        standard = next((x for x in group if not x['is_fn']), None)
        fn_vector = next((x for x in group if x['is_fn']), None)
        
        # Look up judgment for this code
        judgment_data = v.get('judgment', None)
        
        # Render Standard First
        if standard:
            rows_html.append(generate_vector_row_html(standard, color, is_fn=False, judgment=judgment_data))
        
        # Render FN Second (Partner Row)
        # Note: We typically apply the same judgment to the vector slot, but FN might differ.
        # For now, we only show judgment on the primary/standard vector as per original design.
        if fn_vector:
            rows_html.append(generate_vector_row_html(fn_vector, color, is_fn=True, judgment=None))
            
    vector_rows = "\n".join(rows_html)
    
    # Format narrative with strong tags
    narrative_html = narrative if narrative else f"The Narrative of the {sense_label} of the {plane_label}..."
    
    return f'''
        <!-- Sense q{sense_idx + 1}: The {sense_label} of the {plane_label} -->
        <div class="mb-24">
            <div class="bg-{color}-900 text-white p-6 rounded-t-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center sticky top-16 z-40 shadow-xl ring-1 ring-black/10 w-full">
                <div class="w-full">
                    <h3 class="text-2xl font-bold tracking-tight font-serif">The {sense_label} of the {plane_label} ({sense_desc})</h3>
                    <div class="flex items-center mt-2 space-x-3 opacity-90">
                        <span class="text-{color}-200 text-xs uppercase tracking-widest font-bold">Sense q{sense_idx + 1}</span>
                        <span class="w-1 h-1 bg-white rounded-full opacity-50"></span>
                        <span class="text-xs font-mono opacity-80">7 Vectors</span>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-b-2xl shadow-sm border border-gray-200">
                <div class="bg-gradient-to-br from-white to-{color}-50 border-x border-b border-gray-200 p-8 relative overflow-hidden group">
                    <div class="absolute top-0 right-0 w-32 h-32 bg-{color}-900 opacity-[0.03] rounded-bl-full -mr-8 -mt-8 transition-opacity group-hover:opacity-[0.08]"></div>
                    <div class="relative z-10">
                        <div class="prose prose-lg max-w-none text-gray-700 leading-relaxed font-serif">
                            <strong class="text-gray-900 font-bold">The Narrative of {sense_desc} (The {sense_label} of the {plane_label}):</strong><br>
                            {narrative_html}
                        </div>
                    </div>
                </div>

                <table class="min-w-full text-left border-t border-gray-100">
                    <tbody class="divide-y divide-gray-100">
{vector_rows}
                    </tbody>
                </table>
            </div>
        </div>
'''


def generate_nav(current_plane):
    """Generate navigation HTML."""
    nav_items = []
    for p in PLANES:
        if p["num"] == current_plane:
            active = "bg-yellow-800 text-white transition-colors"
        else:
            active = "text-yellow-100 hover:bg-yellow-800 hover:text-white transition-colors"
        nav_items.append(f'<a href="Plane_{p["num"]}_{p["name"]}.html" class="px-3 py-2 rounded-md text-sm font-medium {active} block md:inline-block">{p["label"]}</a>')
    
    # Add matrix link to nav items for mobile menu
    mobile_nav_items = [f'<a href="AustralianMatrix.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700 block">Back To Matrix</a>'] + nav_items
    
    return "\n                            ".join(nav_items), "\n                            ".join(mobile_nav_items)


def generate_full_html(plane_info, header_quote, totality, senses_html):
    """Generate the complete HTML page."""
    nav_html, mobile_nav_html = generate_nav(plane_info["num"])
    color = SENSE_COLORS[plane_info["num"] - 1]
    
    quote_source = f'{header_quote["author"]}, {header_quote["work"]}'
    if header_quote["year"]:
        quote_source += f', {header_quote["year"]}'
    
    return f'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plane {plane_info["num"]}: Values of Australian {plane_info["name"]}</title>
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
        @media (max-width: 640px) {{
            /* Force table to not be like tables anymore */
            table, thead, tbody, th, td, tr {{ 
                display: block; 
            }}
            
            /* Hide table headers (but not display: none;, for accessibility) */
            thead tr {{ 
                position: absolute;
                top: -9999px;
                left: -9999px;
            }}
            
            tr {{ border: 1px solid #e2e8f0; border-radius: 0.75rem; margin-bottom: 1.5rem; background: white; box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1); overflow: hidden; }}
            
            td {{ 
                /* Behave  like a "row" */
                border: none;
                position: relative;
                padding-left: 1.25rem !important;
                padding-right: 1.25rem !important;
                padding-top: 0.75rem !important;
                padding-bottom: 0.75rem !important;
            }}
            
            /* Code Column */
            td:nth-of-type(1) {{
                background-color: #f8fafc;
                border-bottom: 1px solid #e2e8f0;
                padding-top: 0.5rem !important;
                padding-bottom: 0.5rem !important;
            }}
            
            /* Concept Column */
            td:nth-of-type(2) {{
                padding-bottom: 0 !important;
            }}
            
            /* Description/Quote Column */
            td:nth-of-type(3) {{
                padding-top: 1rem !important;
            }}
        }}
    </style>
</head>

<body class="antialiased text-gray-800">

    <nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Branding -->
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <span class="text-xl font-bold text-white tracking-widest">
                            <a href="../index.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700">←WWSUTRU</a>
                        </span>
                    </div>
                </div>

                <!-- Desktop Menu -->
                <div class="hidden md:block">
                    <div class="ml-10 flex items-baseline space-x-2">
                        <a href="AustralianMatrix.html" class="px-3 py-2 rounded-md text-sm font-medium text-gray-300 hover:text-white hover:bg-gray-700">Back To Matrix</a>
                        {nav_html}
                    </div>
                </div>

                <!-- Mobile Menu Button -->
                <div class="-mr-2 flex md:hidden">
                    <button type="button" onclick="document.getElementById('mobile-menu').classList.toggle('hidden')" class="bg-gray-800 inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white" aria-controls="mobile-menu" aria-expanded="false">
                        <span class="sr-only">Open main menu</span>
                        <!-- Icon when menu is closed -->
                        <svg class="block h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
                        </svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Menu, show/hide based on menu state. -->
        <div class="hidden md:hidden" id="mobile-menu">
            <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3 border-t border-gray-700">
                {mobile_nav_html}
            </div>
        </div>
    </nav>


    <!-- Header -->
    <header class="bg-white border-b border-gray-200 relative overflow-hidden">
        <div class="absolute inset-0 bg-gradient-to-b from-{color}-50 to-white/0 pointer-events-none"></div>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 relative">
            <div class="text-center mb-12">
                <div class="inline-flex h-20 w-auto px-6 bg-{color}-600 rounded-2xl items-center justify-center text-white text-3xl font-bold shadow-xl mb-6 ring-4 ring-{color}-50">
                    {plane_info["label"]}
                </div>
                <h1 class="text-5xl md:text-6xl font-extrabold text-gray-900 tracking-tight mb-4">Values of Australian {plane_info["name"]}</h1>
                <p class="text-xl text-gray-500 font-light max-w-2xl mx-auto">Analysis of the 49 Vectors of {plane_info["name"]}</p>
            </div>

            <div class="max-w-3xl mx-auto text-center py-10">
                <blockquote class="text-2xl md:text-3xl font-serif italic text-gray-700 leading-normal mb-4">
                    "{escape_html(header_quote["text"])}"
                </blockquote>
                <cite class="text-sm font-bold text-gray-500 uppercase tracking-widest not-italic">
                    — {escape_html(quote_source)}
                </cite>
            </div>
        </div>
    </header>

    <div class="max-w-4xl mx-auto -mt-10 mb-16 relative z-10 px-4">
        <div class="bg-white rounded-2xl p-8 md:p-12 shadow-xl ring-1 ring-gray-900/5 relative overflow-hidden">
            <div class="absolute top-0 right-0 w-64 h-64 bg-{color}-50 rounded-full mix-blend-multiply filter blur-3xl opacity-70 -mr-32 -mt-32"></div>
            <div class="absolute bottom-0 left-0 w-64 h-64 bg-gray-50 rounded-full mix-blend-multiply filter blur-3xl opacity-70 -ml-32 -mb-32"></div>
            <div class="relative">
                <h2 class="text-2xl font-bold mb-6 font-serif tracking-tight text-gray-900">The Totality of Australian {plane_info["name"]}</h2>
                <div class="prose prose-lg max-w-none text-gray-600 leading-relaxed">
                    {totality}
                </div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
{senses_html}
    </main>

    <footer class="bg-white border-t border-gray-100 py-12 mt-12">
        <div class="text-center text-gray-400 text-sm">
            <p>&copy; 2024 The Psochic Hegemony. All rights reserved.</p>
        </div>
    </footer>
</body>

</html>'''


def process_plane(plane):
    """Process a single plane markdown file and generate HTML."""
    input_file = os.path.join(INPUT_DIR, f"Australian_Kanon_Plane_{plane['num']}_{plane['name']}.md")
    output_file = os.path.join(OUTPUT_DIR, f"Plane_{plane['num']}_{plane['name']}.html")
    
    if not os.path.exists(input_file):
        print(f"  MISSING: {input_file}")
        return False
    
    print(f"Processing Plane {plane['num']}: {plane['name']}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse content
    header_quote = parse_header_quote(content)
    totality = parse_totality(content)
    vectors = parse_vectors_from_markdown(content)
    narratives = parse_sense_narratives(content)
    judgments = parse_judgment_vectors(plane['num'], plane['name'])
    
    print(f"  Found {len(vectors)} vectors")
    
    # 1. Bucket by code
    # Preserve order
    unique_codes = []
    vectors_map = {}
    for v in vectors:
        v['judgment'] = judgments.get(v['code'], None) # Inject judgment
        if v['code'] not in unique_codes:
            unique_codes.append(v['code'])
            vectors_map[v['code']] = []
        vectors_map[v['code']].append(v)
        
    print(f"  Found {len(unique_codes)} unique vector codes")
    
    # 2. Iterate by 7 codes at a time for senses
    senses_html = []
    
    for sense_idx in range(7):
        # Determine codes for this sense
        # Assuming strict 7x7 structure and input file is ordered
        start_idx = sense_idx * 7
        end_idx = start_idx + 7
        
        current_codes = unique_codes[start_idx:end_idx]
        
        if not current_codes:
            break
            
        sense_vectors_group = []
        for c in current_codes:
            sense_vectors_group.extend(vectors_map[c])
            
        sense_label = SENSE_LABELS[sense_idx][0]
        narrative = narratives.get(sense_label, "")
        color = SENSE_COLORS[sense_idx]
        
        sense_html = generate_sense_section(
            sense_idx,
            sense_vectors_group,
            narrative,
            plane["label"],
            color
        )
        senses_html.append(sense_html)
        print(f"  Sense q{sense_idx + 1}: {len(current_codes)} unique vectors")
    
    # Generate full HTML
    html_content = generate_full_html(
        plane,
        header_quote,
        totality,
        "\n".join(senses_html)
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"  Created: {output_file}")
    return True


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    success_count = 0
    for plane in PLANES:
        if process_plane(plane):
            success_count += 1
    
    print(f"\n[OK] Generated {success_count}/7 plane pages with full content.")


if __name__ == "__main__":
    main()
