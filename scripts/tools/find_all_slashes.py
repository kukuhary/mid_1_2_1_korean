with open('exam_v6.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search all occurrences of ' / ' in html
lines = html.split('\n')
for i, line in enumerate(lines):
    if ' / ' in line:
        print(f"Line {i+1}: {line.strip()}")
