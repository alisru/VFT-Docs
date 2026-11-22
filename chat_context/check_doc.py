from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = Path('html base/Converting Documents to Sheet Music - Google Gemini.html')
html = html_path.read_text(encoding='utf-8', errors='ignore')

title_m = re.search(r'<title>(.*?)</title>', html, re.I)
print('Title:', title_m.group(1) if title_m else None)

# Widget
widget_m = re.search(r'id=["\']chat-context-widget["\'][^>]*>(.*?)</div>', html, re.DOTALL)
if widget_m:
    print('Widget text:', repr(re.sub(r'<[^>]+>', ' ', widget_m.group(1))[:100]))

# Extract messages
user_texts = re.findall(r'<user-query[^>]*>(.*?)</user-query>', html, re.DOTALL)
model_texts = re.findall(r'<model-response[^>]*>(.*?)</model-response>', html, re.DOTALL)

print(f"Extracted user queries: {len(user_texts)}, model responses: {len(model_texts)}")

def strip_tags(s):
    return re.sub(r'<[^>]+>', ' ', s).strip()

msgs = []
max_turns = max(len(user_texts), len(model_texts))
for i in range(max_turns):
    if i < len(user_texts):
        u_text = strip_tags(user_texts[i])
        if u_text:
            msgs.append({'role': 'user', 'text': u_text})
    if i < len(model_texts):
        m_text = strip_tags(model_texts[i])
        if m_text:
            msgs.append({'role': 'assistant', 'text': m_text})

print(f"Total structured messages: {len(msgs)}")

print("\n--- Finding Gemini URLs ---")
urls = set(re.findall(r'https://gemini\.google\.com/[^"\'\s<>]+', html))
for u in list(urls)[:10]:
    print(" ", u)

print("\n--- Checking for Canvas in HTML ---")
# Check if there are canvases or code blocks or extended response
# Look for ProseMirror or monaco
print("has ProseMirror:", 'ProseMirror' in html)
print("has extended-response:", 'extended-response' in html)
print("has code-block:", 'code-block' in html or '<pre' in html)

# Look for titles of canvases or text
canvases = re.findall(r'class=["\'][^"\']*canvas[^"\']*["\']', html, re.I)
print("Canvas class elements:", len(canvases))

# Check payload size
print("Total HTML length in MB:", len(html) / (1024 * 1024))



