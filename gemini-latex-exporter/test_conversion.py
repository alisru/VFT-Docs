import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

def extract_tex(el):
    # Mimic extractTeX(el)
    data = el.get('data-math')
    if data and data.strip():
        return data.strip()
    
    src = el.find(class_='math-src')
    if src and src.get_text().strip():
        return src.get_text().strip()
        
    annotation = el.find('annotation', encoding='application/x-tex')
    if annotation and annotation.get_text().strip():
        return annotation.get_text().strip()
        
    math_tag = el.find('math', alttext=True)
    if math_tag and math_tag.get('alttext').strip():
        return math_tag.get('alttext').strip()
        
    return None

def replace_katex(root, soup):
    # Mimic replaceKaTeX(root)
    # 0. math-block and math-inline
    math_nodes = root.find_all(['math-block', 'math-inline'])
    for node in math_nodes:
        tex = extract_tex(node)
        if not tex:
            continue
            
        is_block = node.name == 'math-block' or node.find(class_='katex-display') is not None
        
        if is_block:
            replacement = soup.new_tag('p')
            replacement['style'] = "font-family: 'Courier New', monospace"
            replacement.string = f"$${tex}$$"
        else:
            replacement = soup.new_string(f" ${tex}$ ")
            
        node.replace_with(replacement)

    # 1. Bare .katex-display
    displays = root.find_all(class_='katex-display')
    for display in displays:
        tex = extract_tex(display)
        if tex:
            replacement = soup.new_tag('p')
            replacement['style'] = "font-family: 'Courier New', monospace"
            replacement.string = f"$${tex}$$"
            display.replace_with(replacement)

    # 2. Bare .katex
    inlines = root.find_all(class_='katex')
    for inline in inlines:
        tex = extract_tex(inline)
        if tex:
            replacement = soup.new_string(f" ${tex}$ ")
            inline.replace_with(replacement)

def html_to_markdown(element, soup):
    # Mimic htmlToMarkdown(element)
    
    # Pre-process code headers
    code_headers = element.find_all(class_='code-block-header')
    for header in code_headers:
        lang_span = header.find('span')
        lang_text = lang_span.get_text().strip() if lang_span else ''
        pre = header.find_next_sibling('pre')
        if pre:
            pre['data-language'] = lang_text
        header.decompose()

    def process_node(node):
        if node.name is None:  # Text node
            return node.string or ''
            
        # Recursive children value
        children_val = ''
        for child in node.children:
            children_val += process_node(child)
            
        tag_name = node.name.upper()
        if tag_name in ['H1', 'H2', 'H3', 'H4']:
            return f"\n\n{'#' * int(tag_name[1])} {children_val.strip()}\n\n"
        elif tag_name == 'P':
            return f"\n\n{children_val.strip()}\n\n"
        elif tag_name in ['STRONG', 'B']:
            return f"**{children_val.strip()}**"
        elif tag_name in ['EM', 'I']:
            return f"*{children_val.strip()}*"
        elif tag_name == 'CODE':
            if node.parent and node.parent.name == 'pre':
                return children_val
            return f"`{children_val.strip()}`"
        elif tag_name == 'PRE':
            lang = node.get('data-language', '')
            buttons = node.find_all(['button', 'copy-code-button'])
            for b in buttons:
                b.decompose()
            code_text = node.get_text().strip()
            return f"\n\n```{lang}\n{code_text}\n```\n\n"
        elif tag_name in ['UL', 'OL']:
            return f"\n{children_val}\n"
        elif tag_name == 'LI':
            parent_tag = node.parent.name.upper() if node.parent else ''
            if parent_tag == 'OL':
                siblings = list(node.parent.find_all('li', recursive=False))
                idx = siblings.index(node) + 1
                return f"{idx}. {children_val.strip()}\n"
            return f"* {children_val.strip()}\n"
        elif tag_name == 'BR':
            return '\n'
        elif tag_name == 'A':
            href = node.get('href', '')
            return f"[{children_val.strip()}]({href})"
        elif tag_name == 'TABLE':
            return f"\n\n{render_table(node)}\n\n"
        else:
            if tag_name in ['DIV', 'SECTION']:
                return f"\n{children_val}\n"
            return children_val

    def render_table(table):
        md = ''
        rows = table.find_all('tr')
        for rowIndex, row in enumerate(rows):
            cells = row.find_all(['th', 'td'])
            row_str = '|'
            for cell in cells:
                row_str += f" {cell.get_text().strip().replace('|', '\\|')} |"
            md += row_str + '\n'
            
            if rowIndex == 0 and row.find('th'):
                separator = '|'
                for _ in cells:
                    separator += ' --- |'
                md += separator + '\n'
        return md

    markdown = process_node(element)
    markdown = re.sub(r'\n{3,}', '\n\n', markdown)
    return markdown.strip()

# Run the test
file_path = "Generate Lorem Ipsum Text w-latex - Google Gemini.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
pm = soup.find(class_='ProseMirror')

if pm:
    print("Found ProseMirror canvas! Running converter...")
    clone_soup = BeautifulSoup(str(pm), "html.parser")
    pm_clone = clone_soup.find(class_='ProseMirror')
    
    replace_katex(pm_clone, clone_soup)
    md = html_to_markdown(pm_clone, clone_soup)
    
    print("\n--- Converted Markdown ---")
    print(md[:2000])
else:
    print("Could not find ProseMirror canvas in HTML.")
