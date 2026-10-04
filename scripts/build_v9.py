import os
import re
import subprocess
import fitz

def build_v9():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(base_dir) == 'scripts':

        base_dir = os.path.dirname(base_dir)

    # ----------------------------------------------------
    # 1. Create v9 Markdown
    # ----------------------------------------------------
    v8_md_path = os.path.join(base_dir, '2026_중1_국어_중간고사_실전모의고사_15제_v8.md')
    with open(v8_md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    # Update version header
    md = md.replace(
        '# [2026학년도 중간고사 대비] 중학 국어 실전 모의 평가 15제 (v8: 상 8 / 중 5 / 하 2 고난도 개편형)',
        '# [2026학년도 중간고사 대비] 중학 국어 실전 모의 평가 15제 (v9: 배점 배제 및 난이도 고정형)'
    )
    md = md.replace(
        '- **버전**: v8.0 (난이도 고정 표준: [상] 8문항 / [중] 5문항 / [하] 2문항 전면 신규 출제형)',
        '- **버전**: v9.0 (배점 표기 일절 배제 & 난이도 [상 8 / 중 5 / 하 2] 중심 표준 완성형)'
    )
    md = md.replace(
        '- **문항 구성**: 총 15문항 (전 문항 5지 선다형 객관식) / 100점 만점\n- **배점 체계**: 6점 문항 5개 (30점) + 7점 문항 10개 (70점) = 총 100점\n',
        '- **문항 구성**: 총 15문항 (전 문항 5지 선다형 객관식)\n- **배점 체계**: 배점 표기 일절 배제 (GEMINI.md 표준 준수)\n'
    )

    # Remove points from question headers: e.g., "(선택형 / 7점 / [난이도: 상])" -> "(선택형 / [난이도: 상])"
    md = re.sub(r'\(선택형 / \d+점 / \[난이도: ([^\]]+)\]\)', r'(선택형 / [난이도: \1])', md)

    # Update summary table: change header and rows
    md = md.replace('### [정답 및 배점 총괄표]', '### [정답 및 난이도 총괄표]')
    md = md.replace(
        '| 문항 | 출제 단원 | 교과서 수록 제재 및 핵심 개념 | 문제 유형 | 난이도 | 배점 | 정답 |',
        '| 문항 | 출제 단원 | 교과서 수록 제재 및 핵심 개념 | 문제 유형 | 난이도 | 정답 |'
    )
    md = md.replace(
        '| :---: | :---: | :--- | :---: | :---: | :---: | :---: |',
        '| :---: | :---: | :--- | :---: | :---: | :---: |'
    )
    # Remove point column from rows: e.g. "| **상** | 7점 | **①** |" -> "| **상** | **①** |"
    md = re.sub(r'\| (\*\*[상중하]\*\*) \| \d+점 \| (\*\*[①②③④⑤]\*\*) \|', r'| \1 | \2 |', md)

    # Update commentary headers: remove point references e.g., "배점: 7점"
    # e.g., "#### [문항 1] 정답 ① [난이도: 상]" remains clean as is!

    v9_md_path = os.path.join(base_dir, '2026_중1_국어_중간고사_실전모의고사_15제_v9.md')
    with open(v9_md_path, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"[1] Saved v9 Markdown: {v9_md_path} ({os.path.getsize(v9_md_path)} bytes)")

    # ----------------------------------------------------
    # 2. Create v9 HTML
    # ----------------------------------------------------
    v8_html_path = os.path.join(base_dir, '출제', 'exam_v8.html')
    with open(v8_html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update titles and headers
    html = html.replace(
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 (v8 고난도 개편형)</title>',
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 (v9 배점 배제형)</title>'
    )
    html = html.replace(
        '<div class="header-title">2026학년도 2학기 중간고사 대비 국어 실전 평가원형 모의고사 [v8]</div>',
        '<div class="header-title">2026학년도 2학기 중간고사 대비 국어 실전 평가원형 모의고사 [v9: 배점 배제형]</div>'
    )
    html = html.replace(
        '<td class="label">문항 수 / 배점</td>',
        '<td class="label">문항 구성</td>'
    )
    html = html.replace(
        '<td>전 문항 객관식 15제 / 100점 만점</td>',
        '<td>전 문항 객관식 15제 (배점 없음)</td>'
    )
    html = html.replace(
        '<div class="header-title">정답 및 상세 해설 [v8: 고난도 개편형] (문제를 낸 이유 수록)</div>',
        '<div class="header-title">정답 및 상세 해설 [v9: 배점 배제형] (문제를 낸 이유 수록)</div>'
    )
    html = html.replace(
        '<span>[제 2 부] 빠른 정답 및 배점 총괄표</span>',
        '<span>[제 2 부] 빠른 정답 및 난이도 총괄표</span>'
    )
    html = html.replace(
        '<span>100점 만점 / 전 문항 객관식 5지선다</span>',
        '<span>전 문항 객관식 5지선다</span>'
    )

    # Remove question points from q-title: e.g. <span class="q-points">[7점]</span>
    html = re.sub(r'<span class="q-points">\[\d+점\]</span>', '', html)

    # Remove points from table header and cells in HTML
    html = html.replace(
        '<th style="width: 8%;">배점</th>\\n      <th style="width: 8%;">정답</th>',
        '<th style="width: 10%;">정답</th>'
    )
    html = re.sub(r'<td>\d+점</td><td><b>([①②③④⑤])</b></td>', r'<td><b>\1</b></td>', html)

    # Remove tag for points in explanation cards: e.g. <span class="tag">7점</span>
    html = re.sub(r'<span class="tag">\d+점</span>', '', html)

    v9_html_path = os.path.join(base_dir, '출제', 'exam_v9.html')
    with open(v9_html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[2] Saved v9 HTML: {v9_html_path} ({os.path.getsize(v9_html_path)} bytes)")

    # ----------------------------------------------------
    # 3. Generate v9 PDF
    # ----------------------------------------------------
    v9_pdf_path = os.path.join(base_dir, '2026_중1_국어_중간고사_실전모의고사_15제_v9.pdf')
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    cmd = [
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--no-pdf-header-footer',
        f'--print-to-pdf={v9_pdf_path}',
        v9_html_path
    ]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(v9_pdf_path) and os.path.getsize(v9_pdf_path) > 1000:
        print(f"[3] PDF Generated: {v9_pdf_path} ({os.path.getsize(v9_pdf_path)} bytes)")
    else:
        print(f"[FAIL] Return code: {res.returncode}")
        return

    # Verify with PyMuPDF
    doc = fitz.open(v9_pdf_path)
    print(f"[4] Total Pages in v9 PDF: {len(doc)}")
    all_text = "\\n".join([page.get_text() for page in doc])

    # Check that points are completely removed
    has_points = bool(re.search(r'\[\d+점\]', all_text))
    has_100_points = '100점' in all_text
    print(f"Points check in PDF -> has '[X점]': {has_points}, has '100점': {has_100_points}")
    print(f"Difficulty check in PDF -> [상]: {'[상]' in all_text}, [중]: {'[중]' in all_text}, [하]: {'[하]' in all_text}")

if __name__ == '__main__':
    build_v9()
