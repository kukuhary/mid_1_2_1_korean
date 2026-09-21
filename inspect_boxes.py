with open('exam_v6.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = 0
while True:
    p_start = html.find('<div class="passage-box">', idx)
    if p_start == -1:
        break
    p_end = html.find('</div>', p_start)
    # find outer div close
    # note: passage-box may contain inner divs!
    # Let's find by looking for the next question or section
    next_q = html.find('<!-- 문항', p_start)
    if next_q == -1:
        next_q = html.find('<div class="question">', p_start)
    box_content = html[p_start:next_q]
    print("BOX:")
    print(box_content)
    print("-" * 50)
    idx = next_q
