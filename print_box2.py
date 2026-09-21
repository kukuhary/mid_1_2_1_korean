with open('exam_v6.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('햇비')
print(html[idx-100:idx+500])
