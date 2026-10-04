with open('exam_v6.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

boxes = re.findall(r'<div class="passage-box">.*?</div>', html, re.DOTALL)
for i, b in enumerate(boxes):
    lines = b.split('\n')
    has_slash = any(' / ' in l for l in lines)
    print(f"Box {i+1} has ' / ': {has_slash}")
    if has_slash:
        for l in lines:
            if ' / ' in l:
                print("  ", l.strip())

with open('2026_중1_국어_중간고사_실전모의고사_15제_v6.md', 'r', encoding='utf-8') as f:
    md = f.read()

md_passages = re.findall(r'```text\n(.*?)```', md, re.DOTALL)
print(f"Total md codeblocks: {len(md_passages)}")
for i, p in enumerate(md_passages):
    if ' / ' in p:
        print(f"MD block {i+1} has ' / '")
        for l in p.split('\n'):
            if ' / ' in l:
                print("  ", l)
