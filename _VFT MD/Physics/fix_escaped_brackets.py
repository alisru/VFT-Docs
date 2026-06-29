import re
import sys

file_path = r'e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\The Geometry of Definition Monograph.md'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
except Exception as e:
    print(f"Error reading: {e}")
    sys.exit(1)

# The user is hitting KaTeX errors because NotebookLM parses \[ and \] as math block delimiters, 
# but the text is using them as escaped literal brackets like \[Q/A\]. 
# We need to un-escape them or properly format them as math.

# 1. Un-escape all \[ and \] and \^ and \* in the file so they are just normal characters, 
# except where they are genuinely part of a math block. But wait, in standard Markdown, 
# \[ is just an escaped [. In NotebookLM, it triggers math. 
# It's safer to just replace \[ and \] with [ and ] globally, because standard brackets 
# don't need escaping unless they are part of a link.
text = text.replace(r'\[', '[')
text = text.replace(r'\]', ']')
# Same for \^ and \* 
text = text.replace(r'\^', '^')
text = text.replace(r'\*', '*')

# 2. Now let's properly wrap the specific math formulas in inline LaTeX so they look good.
# $A[Q/A]^{(6+n)} \cdot [Q/A]^{(6+n)} \cdot [Q/A]^{(6+n)}$
text = text.replace(
    'A[Q/A]^(6+n) * [Q/A]^(6+n) * [Q/A]^(6+n)',
    r'$A[Q/A]^{(6+n)} \cdot [Q/A]^{(6+n)} \cdot [Q/A]^{(6+n)}$'
)

# $Q^{(7×6q)} + n$
text = text.replace('Q^(7×6q) + n', r'$Q^{(7 \times 6q)} + n$')

# $[Q/A]^{(6+n)}[p][f]$
text = text.replace(
    '[Q/A]^(6+n)[p][f]',
    r'$[Q/A]^{(6+n)}[p][f]$'
)

# $[Q/A]^{(6+n)}[when]$
text = text.replace(
    '[Q/A]^(6+n)[when]',
    r'$[Q/A]^{(6+n)}[\text{when}]$'
)

# $[Q/A]^{(6+n)}$
text = text.replace(
    '[Q/A]^(6+n)',
    r'$[Q/A]^{(6+n)}$'
)

# Hash([Q/A]^42) = n
text = text.replace('Hash([Q/A]^42)', r'$\text{Hash}([Q/A]^{42})$')

# Hash([Q/A]^42[when_past])
text = text.replace('Hash([Q/A]^42[when_past])', r'$\text{Hash}([Q/A]^{42}[\text{when}_{\text{past}}])$')
text = text.replace('Hash([Q/A]^42[when_now])', r'$\text{Hash}([Q/A]^{42}[\text{when}_{\text{now}}])$')
text = text.replace('Hash([Q/A]^42[when_next])', r'$\text{Hash}([Q/A]^{42}[\text{when}_{\text{next}}])$')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed escaped brackets causing KaTeX collision')
