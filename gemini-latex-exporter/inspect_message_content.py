import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = "Generate Lorem Ipsum Text w-latex - Google Gemini.html"
with open(file_path, "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

message_contents = soup.find_all("message-content")
print(f"Found {len(message_contents)} <message-content> elements.")

for i, mc in enumerate(message_contents):
    print(f"\n--- <message-content> [{i}] ---")
    print(f"Attributes: {mc.attrs}")
    
    # Let's find all descendants and print their tags and attributes
    descendants = mc.find_all(True)
    print(f"Total descendants: {len(descendants)}")
    
    # Group them by tag name
    tag_counts = {}
    for d in descendants:
        tag_counts[d.name] = tag_counts.get(d.name, 0) + 1
    print(f"Tag counts: {tag_counts}")
    
    # Print any elements with data-* attributes
    print("\nElements with data-attributes:")
    data_elements = mc.find_all(lambda tag: tag and any(attr.startswith("data-") for attr in tag.attrs))
    for de in data_elements[:10]:
        # Filter out angular attributes like data-turn-source-index
        attrs = {k: v for k, v in de.attrs.items() if k.startswith("data-") and not k.startswith("data-ng-")}
        if attrs:
            print(f"  <{de.name}> attrs: {attrs} (text snippet: {de.get_text()[:60].strip()})")
            
    # Print any script tags or hidden inputs
    hidden = mc.find_all(["script", "input", "textarea"])
    if hidden:
        print(f"\nHidden elements: {len(hidden)}")
        for h in hidden:
            print(f"  <{h.name}> type={h.get('type')} value={str(h.get('value'))[:100]}")
