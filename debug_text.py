with open('exam_v5.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx6 = text.find('06번')
idx7 = text.find('07번', idx6)

with open('debug_out.txt', 'w', encoding='utf-8') as out:
    out.write("=== 06 ===\n" + text[idx6-40:idx7-10] + "\n")
    idx14 = text.find('14번', idx7)
    idx15 = text.find('15번', idx14)
    out.write("=== 14 ===\n" + text[idx14-40:idx15-10] + "\n")

print("debug_out.txt written")
