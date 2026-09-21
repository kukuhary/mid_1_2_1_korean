import os
import re
import subprocess
import fitz

def build():
    with open('exam.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Define enhanced CSS for v5 with larger font, wider line spacing and question margins
    v5_style = """<style>
  @page {
    size: A4;
    margin: 13mm 10mm 13mm 10mm;
    @bottom-center {
      content: "- " counter(page) " -";
      font-size: 8.5pt;
      font-family: 'Malgun Gothic', '맑은 고딕', sans-serif;
      color: #333;
    }
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    font-family: 'Malgun Gothic', '맑은 고딕', 'Batang', '바탕', sans-serif;
    color: #000;
    line-height: 1.75;
    font-size: 10pt;
    margin: 0;
    padding: 0;
    background: #fff;
  }

  /* 1단 전폭 영역 */
  .full-width {
    width: 100%;
    margin-bottom: 12px;
  }

  /* 시험지 상단 헤더 박스 (흑백) */
  .header-box {
    border: 2px solid #000;
    padding: 10px 14px;
    margin-bottom: 14px;
    text-align: center;
    background-color: #fff;
  }
  .header-title {
    font-size: 16pt;
    font-weight: bold;
    margin: 0 0 6px 0;
    letter-spacing: -0.5px;
  }
  .header-info-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 6px;
    font-size: 9pt;
  }
  .header-info-table td {
    border: 1px solid #444;
    padding: 5px 8px;
    text-align: center;
    background-color: #f7f7f7;
  }
  .header-info-table td.label {
    font-weight: bold;
    background-color: #eaeaea;
    width: 14%;
  }

  /* 섹션 구분 바 (흑백) */
  .section-bar {
    font-size: 11pt;
    font-weight: bold;
    border-top: 1.5px solid #000;
    border-bottom: 1px solid #000;
    padding: 6px 8px;
    margin: 12px 0 10px 0;
    background-color: #f0f0f0;
    display: flex;
    justify-content: space-between;
  }

  /* 2단 레이아웃 컬럼 설정 */
  .two-column-layout {
    column-count: 2;
    column-gap: 8mm;
    column-rule: 0.8px solid #777;
    text-align: justify;
  }

  /* 지문 박스 (흑백) */
  .passage-box {
    border: 1.2px solid #333;
    background-color: #fafafa;
    padding: 10px 12px;
    margin: 0 0 16px 0;
    font-size: 9.5pt;
    line-height: 1.75;
    break-inside: avoid;
    -webkit-column-break-inside: avoid;
  }
  .passage-header {
    font-weight: bold;
    font-size: 10pt;
    text-align: center;
    margin-bottom: 6px;
    border-bottom: 1px dashed #666;
    padding-bottom: 4px;
  }

  /* 개별 문제 박스 */
  .question {
    margin-bottom: 26px;
    break-inside: avoid;
    -webkit-column-break-inside: avoid;
  }
  .q-title {
    font-weight: bold;
    font-size: 10.2pt;
    margin-bottom: 6px;
    line-height: 1.6;
  }
  .q-points {
    font-size: 9pt;
    font-weight: normal;
    color: #333;
  }

  /* 선택지 스타일 */
  .choices {
    margin-left: 2px;
    margin-top: 5px;
  }
  .choice-item {
    margin-bottom: 5px;
    font-size: 9.5pt;
    text-indent: -1.3em;
    padding-left: 1.3em;
    line-height: 1.65;
  }

  /* 보기/조건 박스 (흑백) */
  .view-box {
    border: 1px solid #555;
    background-color: #f5f5f5;
    padding: 8px 10px;
    margin: 6px 0 10px 0;
    font-size: 9pt;
    line-height: 1.65;
    break-inside: avoid;
    -webkit-column-break-inside: avoid;
  }
  .view-title {
    font-weight: bold;
    text-align: center;
    margin-bottom: 4px;
    font-size: 9.5pt;
  }

  /* 페이지 넘김 */
  .page-break {
    page-break-before: always;
    break-before: page;
  }

  /* 정답표 (흑백) */
  table.ans-table {
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 16px 0;
    font-size: 9pt;
  }
  table.ans-table th, table.ans-table td {
    border: 1px solid #333;
    padding: 5px 6px;
    text-align: center;
  }
  table.ans-table th {
    background-color: #e5e5e5;
    font-weight: bold;
  }

  /* 상세 해설 아이템 (흑백) */
  .expl-card {
    border: 1px solid #777;
    background-color: #fff;
    padding: 9px 11px;
    margin-bottom: 16px;
    break-inside: avoid;
    -webkit-column-break-inside: avoid;
    font-size: 9pt;
    line-height: 1.65;
  }
  .expl-card-header {
    font-weight: bold;
    font-size: 9.8pt;
    border-bottom: 1px solid #999;
    padding-bottom: 4px;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
  }
  .tag {
    display: inline-block;
    border: 1px solid #222;
    background: #f0f0f0;
    color: #000;
    padding: 1px 5px;
    font-size: 8.5pt;
    font-weight: bold;
    margin-right: 4px;
    border-radius: 2px;
  }
  .expl-row {
    margin-bottom: 5px;
  }
</style>"""

    # Replace <style>...</style>
    html_v5 = re.sub(r'<style>.*?</style>', v5_style, html, flags=re.DOTALL)

    # Replace title and header labels to indicate v5
    html_v5 = html_v5.replace(
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제</title>',
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 (v5 가독성 강화형)</title>'
    )
    html_v5 = html_v5.replace(
        '<div class="header-title">2026학년도 1학기/2학기 중간고사 대비 국어 실전 모의고사</div>',
        '<div class="header-title">2026학년도 중간고사 대비 국어 실전 모의고사 [v5: 가독성 강화형]</div>'
    )
    html_v5 = html_v5.replace(
        '<div class="header-title">정답 및 상세 해설 (문제를 낸 이유 수록)</div>',
        '<div class="header-title">정답 및 상세 해설 [v5: 가독성 강화형] (문제를 낸 이유 수록)</div>'
    )

    with open('exam_v5.html', 'w', encoding='utf-8') as f:
        f.write(html_v5)
    print("exam_v5.html created successfully.")

    pdf_v5_path = os.path.abspath('2026_중1_국어_중간고사_실전모의고사_15제_v5.pdf')
    html_v5_abs = os.path.abspath('exam_v5.html')

    browser_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    if not os.path.exists(browser_path):
        browser_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    print(f"Generating PDF with: {browser_path}")
    cmd = [
        browser_path,
        '--headless',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        f'--print-to-pdf={pdf_v5_path}',
        html_v5_abs
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if os.path.exists(pdf_v5_path) and os.path.getsize(pdf_v5_path) > 1000:
        print(f"PDF generated successfully: {pdf_v5_path} (Size: {os.path.getsize(pdf_v5_path)} bytes)")
        doc = fitz.open(pdf_v5_path)
        print(f"Total Pages: {len(doc)}")
        for i in range(len(doc)):
            text = doc[i].get_text()
            print(f"  Page {i+1}: length {len(text)} chars | Sample: {text.strip()[:60]}...")
    else:
        print(f"Failed to generate PDF. Return code: {res.returncode}")
        print("Stderr:", res.stderr)

if __name__ == '__main__':
    build()
