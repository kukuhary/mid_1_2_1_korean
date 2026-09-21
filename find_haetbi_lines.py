import fitz

doc = fitz.open('2026_중1_국어_중간고사_실전모의고사_15제_v7.pdf')
for i, page in enumerate(doc):
    t = page.get_text('text')
    if '햇비' in t:
        lines = [l.strip() for l in t.split('\n') if l.strip()]
        for j, line in enumerate(lines):
            if '햇비' in line:
                print(f"Page {i+1}, line {j}:")
                for k in range(max(0, j-2), min(len(lines), j+16)):
                    print(f"  {k}: {repr(lines[k])}")
                break
