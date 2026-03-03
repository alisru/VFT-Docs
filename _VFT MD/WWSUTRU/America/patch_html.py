import os
import re

print("Starting robust site patching...")

# 1. Update Map Navbar Sticky & Hyperlinks
map_builder_path = "build_trump_map.py"
with open(map_builder_path, 'r', encoding='utf-8') as f:
    map_code = f.read()

# Fix sticky navbar
map_code = map_code.replace('<nav class="bg-gray-900 border-b border-gray-800">', '<nav class="bg-gray-900 border-b border-gray-800 sticky top-0 z-50">')

# Add click event listener to canvas for hyperlinks
click_js = """
        // Handle clicks for linking to Plane pages
        canvas.addEventListener('click', (e) => {
            if (hoveredEntries.length > 0) {
                const entry = hoveredEntries[0];
                const vectorId = entry.id;
                
                // Determine plane from vector string e.g., "1.1.1" -> plane 1
                const planeNumStr = vectorId.split('.')[0];
                
                // Map plane number to HTML filename
                const planeFiles = {
                    "1": "Plane_1_Identity.html",
                    "2": "Plane_2_Definition.html",
                    "3": "Plane_3_Land.html",
                    "4": "Plane_4_Drive.html",
                    "5": "Plane_5_Method.html",
                    "6": "Plane_6_Foundation.html",
                    "7": "Plane_7_Result.html"
                };
                
                const targetFile = planeFiles[planeNumStr];
                if (targetFile) {
                    window.location.href = targetFile;
                }
            }
        });
        
        let isDragging = false;
"""
if "canvas.addEventListener('click'" not in map_code:
    map_code = map_code.replace("let isDragging = false;", click_js)

# Add pointer cursor on hover
hover_cursor_js = """
                if (hoveredEntries.length > 0) {
                    document.body.style.cursor = 'pointer';
                    tooltip.style.display = 'block';
"""
map_code = map_code.replace("""
                if (hoveredEntries.length > 0) {
                    tooltip.style.display = 'block';""", hover_cursor_js)

with open(map_builder_path, 'w', encoding='utf-8') as f:
    f.write(map_code)
print("build_trump_map.py patched.")


# 2. Update Generator Site Responsive Tables
gen_path = "generate_trump_site.py"
with open(gen_path, 'r', encoding='utf-8') as f:
    gen_code = f.read()

parts = gen_code.split('            table_rows += f"""')
if len(parts) > 1:
    before_table = parts[0]
    
    parts_after = parts[1].split('            """\n        \n        section_html')
    if len(parts_after) > 1:
        after_table = '            """\n        \n        section_html' + parts_after[1]
        
        responsive_table_html = '''            table_rows += f"""
            <tr class="hover:bg-gray-50/20 transition-colors align-top border-t border-gray-100 flex flex-col md:table-row">
                <td class="px-4 md:px-6 py-3 md:py-4 font-mono text-gray-400 text-xs font-bold w-full md:w-16 align-middle bg-gray-50 md:bg-transparent flex justify-between md:table-cell border-b md:border-b-0 border-gray-100">
                    <span class="md:hidden text-gray-500 uppercase tracking-widest text-[10px]">Vector ID</span>
                    <span>{item['id']}</span>
                </td>
                <td class="px-4 md:px-6 py-4 w-full md:w-1/3 align-middle flex flex-col md:table-cell">
                    <div class="font-bold text-gray-900 text-lg md:text-xl leading-tight mb-2 md:mb-0">{item['val']}</div>
                </td>
                <td class="px-4 md:px-6 py-4 w-full md:w-1/4 align-middle flex flex-col md:table-cell">
                    <div class="flex md:block items-center justify-between md:justify-start gap-4 mb-3 md:mb-0">
                        <div class="font-bold text-center text-xl p-2 rounded-lg border w-24 md:w-auto {score_class} shadow-sm order-2 md:order-none">{item['score']}</div>
                        <div class="text-xs font-bold text-left md:text-center tracking-wider {score_class.replace('bg-', 'text-').replace('-100', '-700')} order-1 md:order-none w-1/2 md:w-auto md:mb-2">{score_label}</div>
                    </div>
                    <div class="grid grid-cols-2 gap-2 text-xs font-mono bg-gray-50 p-2 rounded border border-gray-200 mt-2">
                        <div class="text-right text-gray-500 pr-2 border-r border-gray-300">Ideal (υ, ψ):<br><span class="font-bold text-gray-700">{base_coords}</span></div>
                        <div class="text-left text-gray-500 pl-2">Trump (υ, ψ):<br><span class="font-bold text-gray-700">{item['v']}, {item['p']}</span></div>
                    </div>
                </td>
                <td class="px-4 md:px-6 py-4 w-full md:w-1/4 align-middle bg-slate-50 md:border-l border-white flex flex-col items-start md:table-cell border-t md:border-t-0 border-gray-100">
                    <div class="flex md:block justify-between w-full md:w-auto mb-2 md:mb-1 border-b md:border-0 border-gray-200 pb-2 md:pb-0">
                        <div class="text-sm font-mono text-gray-600 leading-tight">υ: {item['v']} <span class="hidden md:inline text-gray-400">relative to</span><span class="md:hidden text-gray-400">vs</span> {base_data.get('v', '1')} = <strong class="text-gray-900">{rel_v:+.1f}</strong></div>
                        <div class="text-sm font-mono text-gray-600 leading-tight">ψ: {item['p']} <span class="hidden md:inline text-gray-400">relative to</span><span class="md:hidden text-gray-400">vs</span> {base_data.get('p', '1')} = <strong class="text-gray-900">{rel_p:+.1f}</strong></div>
                    </div>
                    <div class="text-sm font-bold uppercase tracking-wider {v_color} bg-white p-1 px-3 rounded-md border shadow-sm mt-2 md:mt-1 text-center w-full md:inline-block md:w-auto">{verdict}</div>
                </td>
            </tr>
            <tr class="align-top border-b border-gray-200 last:border-0 bg-slate-50 flex flex-col md:table-row">
                <td colspan="4" class="px-4 md:px-6 py-4 md:py-6 w-full">
                    {kanon_quote_html}
                    <div class="text-gray-900 leading-relaxed font-medium md:pl-4 md:border-l-4 border-slate-400 flex flex-col md:block">
                        <span class="font-bold text-gray-800 uppercase tracking-wider text-xs mb-2 md:mb-0 mr-2 text-slate-700 bg-slate-200 md:bg-transparent px-2 py-1 md:p-0 rounded-sm md:rounded-none w-max block md:inline">Trump Justification:</span>
                        <div class="text-[0.95rem] md:text-base">{item['reasoning']}</div>
                    </div>
                </td>
            </tr>
'''
        
        gen_code = before_table + responsive_table_html + after_table
        
        # Now fix the outer table wrapper
        
        # We need to replace: <table class="min-w-full text-left border-t border-gray-100">
        # with: <table class="min-w-full text-left md:border-t md:border-gray-100 block md:table">
        import re
        gen_code = re.sub(
            r'<table class="min-w-full text-left border-t border-gray-100">\s*<thead>\s*<tr class="bg-gray-50">\s*<th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Vector</th>\s*<th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Entry</th>\s*<th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider text-center">Trump Score / Coordinates</th>\s*<th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider border-l border-gray-200">Relative Moral Result \(υ, ψ\)</th>\s*</tr>\s*</thead>\s*<tbody class="divide-y divide-gray-100">',
            r'''<table class="min-w-full text-left md:border-t md:border-gray-100 block md:table">
                    <thead class="hidden md:table-header-group">
                        <tr class="bg-gray-50">
                            <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Vector</th>
                            <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">Entry</th>
                            <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider text-center">Trump Score / Coordinates</th>
                            <th class="px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider border-l border-gray-200">Relative Moral Result (υ, ψ)</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y md:divide-y-0 divide-gray-200 md:divide-gray-100 block md:table-row-group">''',
            gen_code
        )
        
        gen_code = gen_code.replace('<div class="bg-white rounded-b-2xl shadow-sm border border-gray-200 overflow-hidden">', '<div class="bg-white rounded-b-xl md:rounded-b-2xl md:shadow-sm md:border md:border-gray-200 overflow-hidden">')
        gen_code = gen_code.replace('<div class="{colors[\'bg\']} text-white p-6 rounded-t-2xl', '<div class="{colors[\'bg\']} text-white p-4 md:p-6 rounded-t-xl md:rounded-t-2xl')
        gen_code = gen_code.replace('<div class="mb-24">', '<div class="mb-16 md:mb-24 shadow-sm md:shadow-none bg-white rounded-xl md:rounded-none overflow-hidden border border-gray-200 md:border-0">')
        
        with open(gen_path, 'w', encoding='utf-8') as f:
            f.write(gen_code)
        print("generate_trump_site.py patched.")
else:
    print("table rows not found")
