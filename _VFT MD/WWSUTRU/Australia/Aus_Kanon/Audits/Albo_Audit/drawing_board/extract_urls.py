import re

files = ['hansard19defend.txt', 'hansard20future.txt', 'hansard22climate.txt', 'hansard25ack.txt', 'hansard25penalty.txt']
for fn in files:
    with open(f'raw_fetches/{fn}', 'r', encoding='utf-8', errors='replace') as f:
        content = f.read(5000)
    print(f'=== {fn} ===')
    urls = re.findall(r'https?://\S+', content)
    for u in urls[:8]:
        print(' ', u)
    print()
