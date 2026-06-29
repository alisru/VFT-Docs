import re
import sys

file_path = r'e:\Vector Field Theory\VFT Docs\_VFT MD\Physics\The Geometry of Definition Monograph.md'
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
except Exception as e:
    print(f"Error reading: {e}")
    sys.exit(1)

# 1. Fix single line $$ matrix blocks
def fix_matrix(m):
    inner = m.group(1)
    inner = inner.replace(' \\\\ ', ' \\\\\n')
    return '\n$$\n' + inner + '\n$$\n'

text = re.sub(
    r'\$\$(.*?\\begin\{bmatrix\}.*?\\end\{bmatrix\}.*?)\$\$', 
    fix_matrix, 
    text
)

# 2. Fix the non-math variables
# USE raw strings AND double backslashes for re.sub replacement!
# In re.sub, \t is parsed as tab even in raw strings. To get literal \t, we need \\t.
text = re.sub(r'past\[\{?when_prev\}?\]', r'$\\text{past}[\\text{when}_{\\text{prev}}]$', text)
text = re.sub(r'present\[\{?when_now\}?\]', r'$\\text{present}[\\text{when}_{\\text{now}}]$', text)
text = re.sub(r'future\[\{?when_next(?:Predicted)?\}?\]', r'$\\text{future}[\\text{when}_{\\text{next}}]$', text)

# 3. Fix the who_when, what_when, etc outside of math blocks
for word in ['who', 'what', 'why', 'where', 'how', 'cause', 'effect']:
    text = re.sub(rf'\b{word}_when\b', rf'$\\text{{{word}}}_{{{{\\text{{when}}}}}}$', text)
    text = re.sub(rf'\b{word}_past\b', rf'$\\text{{{word}}}_{{{{\\text{{past}}}}}}$', text)
    text = re.sub(rf'\b{word}_now\b', rf'$\\text{{{word}}}_{{{{\\text{{now}}}}}}$', text)
    text = re.sub(rf'\b{word}_future\b', rf'$\\text{{{word}}}_{{{{\\text{{future}}}}}}$', text)

# 4. Fix n_now, n_past, n_future
text = re.sub(r'\bn_now\b', r'$n_{\\text{now}}$', text)
text = re.sub(r'\bn_past\b', r'$n_{\\text{past}}$', text)
text = re.sub(r'\bn_future\b', r'$n_{\\text{future}}$', text)

# 5. Fix x_when
text = re.sub(r'\bx_when\b', r'$x_{\\text{when}}$', text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print('Fixed LaTeX formatting properly')
