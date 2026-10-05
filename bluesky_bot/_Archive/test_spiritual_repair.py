import re

cases = [
    """Spirithekanon:
"" Bhagavad Gita 3.8 — PASS (Spiritual Vector)
[Perform your prescribed duty] Delivering efficient and secure tools fulfills constructive responsibility in an evolving digital ecosystem.""",

    """Spirithekanon:
"" Tao Te Ching 16 PASS
Return to the root and you will find peace.""",

    """Spirithekanon:
"" Ecclesiastes 4:9 Two are better than one because they have a good return for their labor. PASS (Spiritual Vector)
True athletic strength lies in mutual support through adversity, not isolated despair.""",

    """Spirithekanon:
"" Proverbs 21:3 PASS
To do righteousness and justice is more acceptable to the Lord than sacrifice."""
]

def repair_spiritual(sp_text):
    # Strip empty quotes at start
    sp_text = re.sub(r'""\s*', '', sp_text)
    
    # If already has non-empty quotes, check if valid
    m = re.search(r'"([^"]+)"', sp_text)
    if m and len(m.group(1).strip()) > 3:
        return sp_text
        
    lines = [l.strip() for l in sp_text.split('\n') if l.strip()]
    if not lines:
        return sp_text
    header = 'Spirithekanon:'
    content_lines = [l for l in lines if not l.startswith('Spirithekanon:')]
    if not content_lines:
        return sp_text

    # Case A: Citation is on line 0, quote text is on line 1
    # Example: "Bhagavad Gita 3.8 — PASS (Spiritual Vector)" / "[Perform your prescribed duty] Delivering..."
    line0 = content_lines[0]
    cite_match = re.search(r'([A-Za-z0-9\s:]+?\b\d+[\.:\d\-]*(?:\s*—\s*\d+[\.:\d\-]*)?)\s*(?:—|-)?\s*(PASS|FAIL|HIT|COND)(?:\s*\([^\)]*\))?', line0)
    
    if cite_match and len(content_lines) > 1:
        cite_str = cite_match.group(0).strip()
        quote_cand = content_lines[1]
        
        # Check if brackets contain the quote: [Perform your prescribed duty] Reflection...
        b_match = re.match(r'^\[(.*?)\]\s*(.*)$', quote_cand)
        if b_match:
            quote_text = b_match.group(1).strip()
            reflection = b_match.group(2).strip()
            rest = f"\n{reflection}" if reflection else ""
            if len(content_lines) > 2:
                rest += "\n" + "\n".join(content_lines[2:])
            return f'{header}\n"{quote_text}" {cite_str}{rest}'
        else:
            # Entire line 1 is the quote
            quote_text = quote_cand
            rest = ""
            if len(content_lines) > 2:
                rest = "\n" + "\n".join(content_lines[2:])
            return f'{header}\n"{quote_text}" {cite_str}{rest}'
            
    # Case B: Citation, Quote, and Verdict are merged on line 0
    # Example: "Ecclesiastes 4:9 Two are better than one because they have a good return for their labor. PASS (Spiritual Vector)"
    b_cite = re.search(r'([A-Za-z0-9\s:]+?\b\d+[\.:\d\-]*)', line0)
    v_match = re.search(r'\b(PASS|FAIL|HIT|COND)(?:\s*\([^\)]*\))?', line0)
    if b_cite and v_match and b_cite.end() < v_match.start():
        cite_part = b_cite.group(1).strip()
        quote_text = line0[b_cite.end():v_match.start()].strip(" —-:\t")
        verdict_part = v_match.group(0).strip()
        rest = ""
        if len(content_lines) > 1:
            rest = "\n" + "\n".join(content_lines[1:])
        return f'{header}\n"{quote_text}" {cite_part} {verdict_part}{rest}'

    return sp_text

for idx, c in enumerate(cases, 1):
    rep = repair_spiritual(c)
    print(f"CASE {idx}:")
    print(rep)
    m = re.search(r'"([^"]+)"', rep)
    print("  Valid match:", bool(m), f"-> quote: '{m.group(1) if m else None}'")
    print("-" * 50)
