with open('exam_v5.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('06번 정답 해설')
if idx == -1:
    idx = text.find('06번')
if idx == -1:
    idx = text.find('문항 06')
print('idx:', idx)
print(text[idx:idx+800])
