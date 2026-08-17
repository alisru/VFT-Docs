import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = "Generate Lorem Ipsum Text w-latex - Google Gemini.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

math_tags = soup.find_all(["math-block", "math-inline"])
print(f"Total math tags found: {len(math_tags)}")

canvas_math = 0
chat_math = 0

for tag in math_tags:
    # Check if the tag is inside an immersive-panel (Canvas)
    in_canvas = tag.find_parent(class_=re.compile("immersive-panel|canvas")) is not None or tag.find_parent("immersive-panel") is not None
    if in_canvas:
        canvas_math += 1
    else:
        chat_math += 1
        print(f"\n[Chat Math Tag] Tag Name: {tag.name}")
        print(f"Attributes: {tag.attrs}")
        # Print parent elements up to 3 levels
        parents = []
        p = tag.parent
        for _ in range(3):
            if p:
                parents.append(f"{p.name} (class={p.get('class')})")
                p = p.parent
        print(f"Parents: {' -> '.join(parents)}")

print(f"\nSummary:")
print(f"Math tags in Canvas: {canvas_math}")
print(f"Math tags in Chat: {chat_math}")
