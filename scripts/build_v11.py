import os
import re
import subprocess
import fitz

def build_v11():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(base_dir) == 'scripts':

        base_dir = os.path.dirname(base_dir)

    # ----------------------------------------------------
    # 1. Create v11 Markdown
    # ----------------------------------------------------
    v10_md_path = os.path.join(base_dir, '2026_중1_국어_중간고사_실전모의고사_15제_v10.md')
    with open(v10_md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    # Update version header
    md = md.replace(
        '# [2026학년도 중간고사 대비] 중학 국어 실전 모의 평가 15제 (v10: 중1 눈높이 표준 완성형)',
        '# [2026학년도 중간고사 대비] 중학 국어 실전 모의 평가 15제 (v11: 실전 문제지 난이도 비노출 완성형)'
    )
    md = md.replace(
        '- **버전**: v10.0 (중학교 1학년 눈높이 적정 난이도 [상 8 / 중 5 / 하 2] & 배점 배제 표준형)',
        '- **버전**: v11.0 (실전 문제지 난이도 표기 일절 배제 & 해설지 난이도 보존 완성형)'
    )

    # In [1부] 실전 문제지: remove "[난이도: 상]", "[난이도: 중]", "[난이도: 하]" from headers
    # e.g., "#### [문항 1] 비유 표현의 원리와 유형 (선택형 / [난이도: 중])" -> "#### [문항 1] 비유 표현의 원리와 유형 (선택형)"
    # But ONLY in [1부] (before [2부])
    parts = md.split('## [2부] 정답 및 상세 해설집')
    part1 = parts[0]
    part2 = '## [2부] 정답 및 상세 해설집' + parts[1]

    # Clean part 1
    part1 = re.sub(r' \(선택형 / \[난이도: [^\]]+\]\)', r' (선택형)', part1)

    md_v11 = part1 + part2

    v11_md_path = os.path.join(base_dir, '2026_중1_국어_중간고사_실전모의고사_15제_v11.md')
    with open(v11_md_path, 'w', encoding='utf-8') as f:
        f.write(md_v11)
    print(f"[1] Saved v11 Markdown: {v11_md_path} ({os.path.getsize(v11_md_path)} bytes)")

    # ----------------------------------------------------
    # 2. Create v11 HTML
    # ----------------------------------------------------
    v10_html_path = os.path.join(base_dir, '출제', 'exam_v10.html')
    with open(v10_html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Update titles
    html = html.replace(
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 (v10 중1 눈높이 표준형)</title>',
        '<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 (v11 실전 시험지형)</title>'
    )
    html = html.replace(
        '<div class="header-title">2026학년도 중간고사 대비 국어 실전 평가원형 모의고사 [v10]</div>',
        '<div class="header-title">2026학년도 중간고사 대비 국어 실전 평가원형 모의고사 [v11]</div>'
    )
    html = html.replace(
        '<div class="header-title">정답 및 상세 해설 [v10: 중1 눈높이 표준형] (문제를 낸 이유 수록)</div>',
        '<div class="header-title">정답 및 상세 해설 [v11: 중1 표준형] (문제를 낸 이유 수록)</div>'
    )

    # In [1부] header table: replace difficulty info with exam taker info (수험번호, 성명)
    old_header_diff = """    <tr>
      <td class="label">난이도 배분</td>
      <td colspan="5"><b>[상] 8문항 (53.3%) | [중] 5문항 (33.3%) | [하] 2문항 (13.3%) 고정 안배</b></td>
    </tr>"""
    new_header_diff = """    <tr>
      <td class="label">제한 시간</td>
      <td>45분</td>
      <td class="label">수험 번호</td>
      <td></td>
      <td class="label">성 명</td>
      <td></td>
    </tr>"""
    if old_header_diff in html:
        html = html.replace(old_header_diff, new_header_diff)
    else:
        # Fallback regex
        html = re.sub(
            r'<tr>\s*<td class="label">난이도 배분</td>\s*<td colspan="5">.*?</td>\s*</tr>',
            new_header_diff,
            html,
            flags=re.DOTALL
        )

    # In [1부] questions: remove diff tags: e.g. <span class="diff-tag">[상]</span>, <span class="diff-tag">[중]</span>, <span class="diff-tag">[하]</span>
    # Split by [2부] to ensure we only remove from [1부]
    html_parts = html.split('<!-- ================= [2부] 정답 및 상세 해설집 ================= -->')
    html_p1 = html_parts[0]
    html_p2 = '<!-- ================= [2부] 정답 및 상세 해설집 ================= -->' + html_parts[1]

    # Remove diff tags in html_p1
    html_p1 = re.sub(r'<span class="diff-tag">\[[^\]]+\]</span>', '', html_p1)

    html_v11 = html_p1 + html_p2

    v11_html_path = os.path.join(base_dir, '출제', 'exam_v11.html')
    with open(v11_html_path, 'w', encoding='utf-8') as f:
        f.write(html_v11)
    print(f"[2] Saved v11 HTML: {v11_html_path} ({os.path.getsize(v11_html_path)} bytes)")

    # ----------------------------------------------------
    # 3. Generate v11 PDF
    # ----------------------------------------------------
    v11_pdf_path = os.path.join(base_dir, '2026_중1_국어_중간고사_실전모의고사_15제_v11.pdf')
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

    cmd = [
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--no-pdf-header-footer',
        f'--print-to-pdf={v11_pdf_path}',
        v11_html_path
    ]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(v11_pdf_path) and os.path.getsize(v11_pdf_path) > 1000:
        print(f"[3] PDF Generated: {v11_pdf_path} ({os.path.getsize(v11_pdf_path)} bytes)")
    else:
        print(f"[FAIL] Return code: {res.returncode}")
        return

    # Verify with PyMuPDF
    doc = fitz.open(v11_pdf_path)
    print(f"[4] Total Pages in v11 PDF: {len(doc)}")

    # Check pages 1~5 (Part 1: Questions) for any difficulty tags
    p1_text = "\\n".join([doc[i].get_text() for i in range(5)])
    has_diff_in_p1 = bool(re.search(r'\[(상|중|하)\]', p1_text))
    print(f"Check Part 1 (Questions, Pages 1~5) -> Has [상/중/하]: {has_diff_in_p1}")

    # Check pages 6~10 (Part 2: Commentary) for difficulty tags
    p2_text = "\\n".join([doc[i].get_text() for i in range(5, len(doc))])
    has_diff_in_p2 = bool(re.search(r'\[(상|중|하)\]', p2_text))
    print(f"Check Part 2 (Commentary, Pages 6~10) -> Has [상/중/하]: {has_diff_in_p2}")

if __name__ == '__main__':
    build_v11()
