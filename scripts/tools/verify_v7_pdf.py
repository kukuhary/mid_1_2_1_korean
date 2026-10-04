import fitz

doc = fitz.open('2026_중1_국어_중간고사_실전모의고사_15제_v7.pdf')
print("Total pages:", len(doc))

p2_text = doc[1].get_text('text')
print("=== Page 2 Text around 햇비 ===")
idx = p2_text.find('햇비')
if idx != -1:
    print(p2_text[idx-50:idx+350])
else:
    print("햇비 not found on Page 2, searching all pages:")
    for i, page in enumerate(doc):
        t = page.get_text('text')
        if '햇비' in t:
            print(f"Found on page {i+1}")
            idx = t.find('햇비')
            print(t[idx-50:idx+350])
