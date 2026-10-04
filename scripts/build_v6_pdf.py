import os
import subprocess
import fitz

def build_v6():
    with open('exam_v5.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update title and headers
    html = html.replace(
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 (v5 가독성 강화형)</title>',
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 (v6 전면교정형)</title>'
    )
    html = html.replace(
        '<div class="header-title">2026학년도 중간고사 대비 국어 실전 모의고사 [v5: 가독성 강화형]</div>',
        '<div class="header-title">2026학년도 중간고사 대비 국어 실전 모의고사 [v6: 전면교정형]</div>'
    )
    html = html.replace(
        '<div class="header-title">정답 및 상세 해설 [v5: 가독성 강화형] (문제를 낸 이유 수록)</div>',
        '<div class="header-title">정답 및 상세 해설 [v6: 전면교정형] (문제를 낸 이유 수록)</div>'
    )

    # 2. Update Q03 choice 5
    old_q3_5 = "<div class=\"choice-item\">⑤ '보슬보슬', '알롱알롱'과 같은 음성 상징어를 사용하여 시적 장면에 감각적 생동감을 부여하였다.</div>"
    new_q3_5 = "<div class=\"choice-item\">⑤ '보슬보슬', '알롱알롱'과 같이 말의 소리와 느낌을 살린 감각적 시어를 활용하여 생동감을 부여하였다.</div>"
    assert old_q3_5 in html, "old_q3_5 not found"
    html = html.replace(old_q3_5, new_q3_5)

    # 3. Update Lee Seong-seon poem in passage-box
    old_poem_html = """  <!-- 지문 3 (06) -->
  <div class="passage-box">
    <div class="passage-header">※ 다음 시를 읽고 물음에 답하시오. (06)</div>
    <div style="text-align:center; font-weight:bold; margin-bottom:2px;">사랑하는 별 하나</div>
    <div style="text-align:right; font-size:7.5pt; margin-bottom:4px;">이성선</div>
    나도 별과 같은 사람은 / 하늘에 가지고 싶다.<br>
    어둠 속에서 무너지려는 / 마음을 비춰 주는 / 풍뎅이 눈물 같은 별 하나<br><br>
    나도 별과 같은 사람은 / 들판에 가지고 싶다.<br>
    새벽길에 풀잎 끝에 / 눈물짓듯 웃어 주는 / 풀잎 이슬 같은 별 하나<br><br>
    나도 별과 같은 사람은 / 이 세상에 가지고 싶다.<br>
    내가 부르면 / 어디서나 소리 없이 / 다가와 안아 주는 꽃 하나<br><br>
    나도 별과 같은 사람은 / 가슴속에 가지고 싶다.<br>
    내가 어둠 속을 헤맬 때 / 가만히 내 작은 손을 잡고 / 길을 비춰 주는 별 하나
  </div>"""

    new_poem_html = """  <!-- 지문 3 (06) -->
  <div class="passage-box">
    <div class="passage-header">※ 다음 시를 읽고 물음에 답하시오. (06)</div>
    <div style="text-align:center; font-weight:bold; margin-bottom:2px;">사랑하는 별 하나</div>
    <div style="text-align:right; font-size:7.5pt; margin-bottom:4px;">이성선</div>
    [1연]<br>
    나도 별과 같은 사람이<br>
    될 수 있을까.<br>
    외로워 쳐다보면<br>
    눈 마주쳐 마음 비춰 주는<br>
    그런 사람이 될 수 있을까.<br><br>
    [2연]<br>
    나도 꽃이 될 수 있을까.<br>
    세상일이 괴로워 쓸쓸히 밖으로 나서는 날에<br>
    가슴에 화안히 안기어<br>
    눈물짓듯 웃어 주는<br>
    하얀 들꽃이 될 수 있을까.<br><br>
    [3연]<br>
    가슴에 사랑하는 별 하나를 갖고 싶다.<br>
    외로울 때 부르면 다가오는<br>
    별 하나를 갖고 싶다.<br>
    마음 어두운 밤 깊을수록<br>
    우러러 쳐다보면<br>
    반짝이는 그 맑은 눈빛으로 나를 씻어<br>
    길을 비추어 주는<br>
    그런 사람 하나 갖고 싶다.
  </div>"""

    assert old_poem_html in html, "old_poem_html not found"
    html = html.replace(old_poem_html, new_poem_html)

    # 4. Update Q14 item ㄹ in view-box
    old_q14_r = '㉣ 시각 장애인을 배려하고 차별 없는 언어를 쓰기 위해 <u>손모아장갑</u>이라는 대체어를 사용하였다.'
    new_q14_r = '㉣ 청각·언어 장애인을 배려하고 차별 없는 언어를 쓰기 위해 <u>손모아장갑</u>이라는 대체어를 사용하였다.'
    assert old_q14_r in html, "old_q14_r not found"
    html = html.replace(old_q14_r, new_q14_r)

    # 5. Update Q06 explanation in card
    old_expl_6 = "'마음을 비춰 주고 안아 주는 존재', 즉 위로와 희망이 되어 주는 순수하고 진실한 대상을 상징함을 정확히 파악하도록 출제하였다."
    new_expl_6 = "'눈 마주쳐 마음 비춰 주고 안아 주는 존재', 즉 고난 속에서 위로와 희망이 되어 주는 순수하고 진실한 대상을 상징함을 정확히 파악하도록 출제하였다."
    if old_expl_6 in html:
        html = html.replace(old_expl_6, new_expl_6)

    # 6. Update Q14 explanation in card
    old_expl_14 = "㉠ 벙어리장갑(장애인 비하)"
    new_expl_14 = "㉠ 벙어리장갑(청각·언어 장애인 비하)"
    if old_expl_14 in html:
        html = html.replace(old_expl_14, new_expl_14)

    with open('exam_v6.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("exam_v6.html successfully written! Total characters:", len(html))

    # Verification checks
    assert '될 수 있을까' in html, "Poem check failed"
    assert '청각·언어 장애인' in html, "Q14 check failed"
    assert '15번' in html or '15.' in html, "Q15 check failed"
    assert '정답 및 상세 해설' in html, "Commentary check failed"

    pdf_v6_path = os.path.abspath('2026_중1_국어_중간고사_실전모의고사_15제_v6.pdf')
    html_v6_abs = os.path.abspath('exam_v6.html')

    browser_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    if not os.path.exists(browser_path):
        browser_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    print(f"Generating PDF with: {browser_path}")
    cmd = [
        browser_path,
        '--headless',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        f'--print-to-pdf={pdf_v6_path}',
        html_v6_abs
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_v6_path) and os.path.getsize(pdf_v6_path) > 1000:
        print(f"PDF v6 generated successfully! Size: {os.path.getsize(pdf_v6_path)} bytes")
        doc = fitz.open(pdf_v6_path)
        print(f"Total Pages in v6 PDF: {len(doc)}")
        for i in range(len(doc)):
            text = doc[i].get_text()
            print(f"  Page {i+1}: length {len(text)} chars | Sample: {text.strip()[:60]}...")
    else:
        print(f"Failed to generate PDF. Return code: {res.returncode}")
        print("Stderr:", res.stderr)

if __name__ == '__main__':
    build_v6()
