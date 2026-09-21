with open('exam_v5.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx6 = text.find('06번 상세 해설')
idx7 = text.find('07번 상세 해설')
print("=== 06번 해설 원문 ===")
print(text[idx6-30:idx7-10])

idx14 = text.find('14번 상세 해설')
idx15 = text.find('15번 상세 해설')
print("=== 14번 해설 원문 ===")
print(text[idx14-30:idx15-10])
