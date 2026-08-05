import re

# Read the HTML file
file_path = "Generate Lorem Ipsum Text - Google Gemini.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

print("File loaded. Searching for button elements...")

# Find all buttons and print their tags/attributes
# We can use regex to find <button ... aria-label="..." or containing text
buttons = re.findall(r'<button[^>]*>', html)
print(f"Total buttons found: {len(buttons)}")

print("\n--- Share/Export Related Buttons ---")
for btn in buttons:
    if any(x in btn.lower() for x in ["share", "export", "menu", "copy", "trigger"]):
        print(btn)

print("\n--- Message Footer Containers ---")
# Let's search for classes like 'buttons-container' or 'actions-container'
divs = re.findall(r'<div[^>]*class="[^"]*buttons-container[^"]*"[^>]*>', html)
for div in divs:
    print(div)

divs_actions = re.findall(r'<div[^>]*class="[^"]*actions-container[^"]*"[^>]*>', html)
for div in divs_actions:
    print(div)
