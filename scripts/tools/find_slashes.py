import re

with open('exam_v6.html', 'r', encoding='utf-8') as f:
    html = f.read()

passages = re.findall(r'<div class="passage-box">(.*?)</div>', html, re.DOTALL)
print(f"Total passage boxes: {len(passages)}")
for i, p in enumerate(passages):
    if ' / ' in p or '/' in p:
        print(f"=== Passage {i+1} ===")
        print(p.strip())
        print("="*40)
