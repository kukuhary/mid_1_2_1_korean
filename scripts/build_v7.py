import os
import subprocess
import fitz

def build_v7():
    # 1. Create v7 Markdown
    with open('2026_중1_국어_중간고사_실전모의고사_15제_v6.md', 'r', encoding='utf-8') as f:
        md = f.read()

    md_v7 = md.replace(
        '# [2026학년도 중간고사 대비] 중학 국어 실전 모의 평가 15제 (v6: 출제오류 전면교정 & 가독성 강화형)\n\n- **버전**: v6.0 (교과서 원문 정합성 및 개념 오류 전면 교정 완료 버전)',
        '# [2026학년도 중간고사 대비] 중학 국어 실전 모의 평가 15제 (v7: 지문 행구분 실제 줄바꿈 완비형)\n\n- **버전**: v7.0 (지문 내 슬래시(/) 제거 및 시 원문 실제 줄바꿈 완비 버전)'
    )
    with open('2026_중1_국어_중간고사_실전모의고사_15제_v7.md', 'w', encoding='utf-8') as f:
        f.write(md_v7)
    print("2026_중1_국어_중간고사_실전모의고사_15제_v7.md created successfully.")

    # 2. Create v7 HTML
    with open('exam_v6.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Update headers to v7
    html = html.replace(
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 (v6 전면교정형)</title>',
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 (v7 지문 줄바꿈 완비형)</title>'
    )
    html = html.replace(
        '<div class="header-title">2026학년도 중간고사 대비 국어 실전 모의고사 [v6: 전면교정형]</div>',
        '<div class="header-title">2026학년도 중간고사 대비 국어 실전 모의고사 [v7: 지문 줄바꿈 완비형]</div>'
    )
    html = html.replace(
        '<div class="header-title">정답 및 상세 해설 [v6: 전면교정형] (문제를 낸 이유 수록)</div>',
        '<div class="header-title">정답 및 상세 해설 [v7: 지문 줄바꿈 완비형] (문제를 낸 이유 수록)</div>'
    )

    # Replace slashes in 햇비 passage with actual line breaks
    old_haetbi_html = """    [1연]<br>
    아씨처럼 나린다 / 보슬보슬 햇비<br>
    맞아 주자 다 같이 / 옥수숫대처럼 크게<br>
    닷 자 엿 자 자라게 / 해님이 웃는다 / 나 보고 웃는다.<br><br>
    [2연]<br>
    하늘 다리 놓였다 / 알롱알롱 무지개<br>
    노래하자 즐겁게 / 동무들아 이리 오나<br>
    다 같이 춤을 추자 / 해님이 웃는다 / 즐거워 웃는다."""

    new_haetbi_html = """    [1연]<br>
    아씨처럼 나린다<br>
    보슬보슬 햇비<br>
    맞아 주자 다 같이<br>
    옥수숫대처럼 크게<br>
    닷 자 엿 자 자라게<br>
    해님이 웃는다<br>
    나 보고 웃는다.<br><br>
    [2연]<br>
    하늘 다리 놓였다<br>
    알롱알롱 무지개<br>
    노래하자 즐겁게<br>
    동무들아 이리 오나<br>
    다 같이 춤을 추자<br>
    해님이 웃는다<br>
    즐거워 웃는다."""

    assert old_haetbi_html in html, "old_haetbi_html not found in exam_v6.html"
    html = html.replace(old_haetbi_html, new_haetbi_html)

    with open('exam_v7.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("exam_v7.html created successfully. Length:", len(html))

    # 3. Generate v7 PDF
    pdf_v7_path = os.path.abspath('2026_중1_국어_중간고사_실전모의고사_15제_v7.pdf')
    html_v7_abs = os.path.abspath('exam_v7.html')

    browser_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    if not os.path.exists(browser_path):
        browser_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    print(f"Generating PDF with: {browser_path}")
    cmd = [
        browser_path,
        '--headless',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        f'--print-to-pdf={pdf_v7_path}',
        html_v7_abs
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_v7_path) and os.path.getsize(pdf_v7_path) > 1000:
        print(f"PDF v7 generated successfully! Size: {os.path.getsize(pdf_v7_path)} bytes")
        doc = fitz.open(pdf_v7_path)
        print(f"Total Pages in v7 PDF: {len(doc)}")
        for i in range(len(doc)):
            text = doc[i].get_text()
            print(f"  Page {i+1}: length {len(text)} chars | Sample: {text.strip()[:50]}...")
    else:
        print(f"Failed to generate PDF. Return code: {res.returncode}")
        print("Stderr:", res.stderr)

if __name__ == '__main__':
    build_v7()
