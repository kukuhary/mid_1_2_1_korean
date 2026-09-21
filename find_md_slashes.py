with open('2026_중1_국어_중간고사_실전모의고사_15제_v6.md', 'r', encoding='utf-8') as f:
    md = f.read()

lines = md.split('\n')
for i, l in enumerate(lines):
    if ' / ' in l:
        print(f"Line {i+1}: {l}")
