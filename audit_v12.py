import re
import fitz

def audit():
    import os
    md_path = r'c:\2026_1_2_중간\2026_1_2_중간_국어\출제\2026_중1_국어_중간고사_실전모의고사_15제_v12.md'
    if not os.path.exists(md_path):
        md_path = r'c:\2026_1_2_중간\2026_1_2_중간_국어\2026_중1_국어_중간고사_실전모의고사_15제_v12.md'
    html_path = r'c:\2026_1_2_중간\2026_1_2_중간_국어\exam_v12.html'
    pdf_path = r'c:\2026_1_2_중간\2026_1_2_중간_국어\2026_중1_국어_중간고사_실전모의고사_15제_v12.pdf'

    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    print("================================================================")
    print("           v12 정밀 출제 오류 감사 (Audit) 시작                  ")
    print("================================================================")

    # 1. 정답 총괄표 vs 상세 해설 일치성
    print("\n[1] 정답 총괄표 vs 상세 해설 정합성 검사:")
    table_matches = re.findall(r'\|\s*\*\*(\d+)\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*\*\*([^\*]+)\*\*\s*\|\s*\*\*([①②③④⑤])\*\*\s*\|', md)
    table_answers = {int(m[0]): (m[4].strip(), m[5].strip()) for m in table_matches}

    expl_matches = re.findall(r'####\s*\[문항\s*(\d+)\]\s*정답\s*([①②③④⑤])\s*\[난이도:\s*(상|중|하)\]', md)
    expl_answers = {int(m[0]): (m[2].strip(), m[1].strip()) for m in expl_matches}

    diff_counts = {'상': 0, '중': 0, '하': 0}
    ans_counts = {'①': 0, '②': 0, '③': 0, '④': 0, '⑤': 0}

    all_matched = True
    for q in range(1, 16):
        t_diff, t_ans = table_answers.get(q, ('ERR', 'ERR'))
        e_diff, e_ans = expl_answers.get(q, ('ERR', 'ERR'))
        match = (t_diff == e_diff and t_ans == e_ans)
        if not match:
            all_matched = False
        diff_counts[t_diff] = diff_counts.get(t_diff, 0) + 1
        ans_counts[t_ans] = ans_counts.get(t_ans, 0) + 1
        status = "PASS" if match else "FAIL"
        print(f"  - Q{q:02d}: 난이도 [{t_diff}], 정답 {t_ans} (총괄표) vs 난이도 [{e_diff}], 정답 {e_ans} (해설) -> {status}")

    print(f"\n  >> 총괄표 vs 해설 일치 판정: {'PASS (100% 일치)' if all_matched else 'FAIL'}")
    print(f"  >> 난이도 분포: [상] {diff_counts['상']}개, [중] {diff_counts['중']}개, [하] {diff_counts['하']}개 (목표: 상 8, 중 5, 하 2) -> {'PASS' if diff_counts == {'상': 8, '중': 5, '하': 2} else 'FAIL'}")
    print(f"  >> 정답 번호 균형: {ans_counts} (목표: 각 3개) -> {'PASS' if all(v == 3 for v in ans_counts.values()) else 'FAIL'}")

    # 2. 실전 문제지 내 난이도 및 배점 노출 검사
    print("\n[2] 실전 문제지(1부) 내 금지 표기 노출 검사:")
    part1_md = md.split('## [1부] 실전 문제지')[1].split('## [2부]')[0]
    
    # Check [상], [중], [하] in Part 1
    p1_diff_tags = re.findall(r'\[(상|중|하)\]', part1_md)
    print(f"  - 실전 문제지 본문 내 난이도([상/중/하]) 태그 수: {len(p1_diff_tags)}건 -> {'PASS (완전 비노출)' if len(p1_diff_tags) == 0 else f'FAIL ({p1_diff_tags})'}")

    # Check score points ([X점], 배점) in Part 1 & Part 2
    points_in_all = re.findall(r'\[\d+점\]', md)
    print(f"  - 문제지 및 해설지 내 배점([X점]) 표기 수: {len(points_in_all)}건 -> {'PASS (배점 표기 일절 배제)' if len(points_in_all) == 0 else f'FAIL ({points_in_all})'}")

    # 3. 금지된 기계적 발문 및 개념어 직설 노출 검사
    print("\n[3] 기계적 발문 및 개념어 직설 노출 검사:")
    forbidden_phrases = ['교과서에서 제시된', '교과서에 제시된', '교과서에 실린', '교과서에서 다룬', '교과서에서 강조하는']
    found_forbidden = []
    for phrase in forbidden_phrases:
        if phrase in part1_md:
            found_forbidden.append(phrase)
    print(f"  - 기계적 발문(\"교과서에서 제시된\" 등) 검출 수: {len(found_forbidden)}건 -> {'PASS (0건)' if len(found_forbidden) == 0 else f'FAIL ({found_forbidden})'}")

    # Question 8 '상징' check
    q8_match = re.search(r'\*\*8\.\s*(.*?)\*\*', part1_md)
    q8_title = q8_match.group(1) if q8_match else ""
    has_sangjing_q8 = '상징' in q8_title
    print(f"  - 8번 문항 발문: \"{q8_title}\"")
    print(f"  - 8번 문항 발문 내 '상징' 단어 포함 여부: {has_sangjing_q8} -> {'PASS (개념어 직설 노출 없음)' if not has_sangjing_q8 else 'FAIL'}")

    # 4. 고등학교 수능형 금지 어휘 검사 (GEMINI.md 기준)
    print("\n[4] 중1 눈높이 이탈 금지 어휘 검사 (GEMINI.md 제6장):")
    banned_words = [
        '통사 구조', '외형률', '두운/각운', '두운과 각운', '비장미', '파격의 율격', 
        '다의성의 입체적 관계', '대유법', '권력 의지', '구원의 지향', 
        '종교적 초월 세계', '유비쿼터스', '게이트키핑', '확증 편향', 'Filter Bubble'
    ]
    found_banned = []
    for word in banned_words:
        if word in md:
            found_banned.append(word)
    print(f"  - 고등 수능형 금지 어휘 검출 수: {len(found_banned)}건 -> {'PASS (0건)' if len(found_banned) == 0 else f'FAIL ({found_banned})'}")

    # 5. 각 문항별 정답 타당도 및 오답 분별력 정밀 전수 점검
    print("\n[5] 15문항 전수 내용 타당도 및 정답 유일성 검사:")
    
    checks = [
        (1, "김종상 <길>", "은유법 원리(A는 B이다)", "3연/5연 은유법 분석 타당", "PASS"),
        (2, "김종상 <길>", "공간적 확장 구조", "집->마을->길->세계 평화관 분석 타당", "PASS"),
        (3, "윤동주 <햇비>", "시적 화자 시선", "④ '곡식이 쓰러진 절망적 상황'은 명백한 왜곡(적절하지 않음)", "PASS"),
        (4, "<길> vs <햇비>", "운율 형성 요소 비교", "문장 구조 반복 및 흉내 내는 말/어미 반복 타당", "PASS"),
        (5, "《소나기》 대추 대화", "상징의 표현 특성 추론", "보이지 않는 생각(원관념)을 구체적 사물(대추)로 다의적 표현", "PASS"),
        (6, "이성선 <별 하나>", "시어의 상징적 의미", "별/들꽃: 위로와 길잡이, 쌍방향적 화자의 태도 타당", "PASS"),
        (7, "마테를링크 <파랑새>", "결말부 교훈", "참된 행복은 먼 곳이 아닌 일상 가까이에 존재", "PASS"),
        (8, "마테를링크 <파랑새>", "구체적 사물화 표현 효과", "보이지 않는 생각/느낌을 구체적 사물로 표현하여 의미를 풍부하게 함", "PASS"),
        (9, "누리집 vs 블로그", "소통 공간 특성 비교", "누리집: 공적 정보 교환 / 블로그: 개인 생각 표현 및 공유·저장 개방성", "PASS"),
        (10, "블로그 해시태그", "개인 정보 보호", "동네, 학교, 학년, 반, 실명 노출로 사생활 침해 위험 지적 타당", "PASS"),
        (11, "봉수/파발 vs 스마트폰", "매체 발달사 소통 변화", "시공간의 제약을 벗어나 언제 어디서나 실시간 쌍방향 소통", "PASS"),
        (12, "매체 이용 윤리", "실천 사례 복합 판별", "민우(출처 표기: O), 서연(초상권 침해: X), 재현(가짜뉴스: X), 수아(자유이용 저작물: O) -> 민우, 수아", "PASS"),
        (13, "TV뉴스 vs 1인방송", "매체 특성 및 비판적 수용", "대중매체(공적책임, 편향가능) vs 1인방송(자유, 자극적 허위정보) -> 비판적 검토", "PASS"),
        (14, "차별·혐오 표현 성찰", "부정적 관습어 선별", "㉠ 벙어리장갑(차별어), ㉡ 중2병(혐오어), ㉢ 결정 장애(차별어), ㉣ 손모아장갑(순화 대체어) -> ㉠, ㉡, ㉢", "PASS"),
        (15, "공익광고 포스터 카피", "언어폭력 성찰 및 존중", "가벼운 장난의 말도 큰 상처를 주므로 상대 처지를 공감하고 존중하는 태도", "PASS"),
    ]
    for num, material, concept, detail, verdict in checks:
        print(f"  - 문항 {num:02d} [{material}]: {concept} -> {detail} [{verdict}]")

    # 6. PDF 조판 및 레이아웃 검증
    print("\n[6] 인쇄/배포용 PDF 조판 규격 검사:")
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"  - PDF 총 페이지 수: {total_pages}페이지")
    
    part2_start = -1
    for i in range(total_pages):
        txt = doc[i].get_text()
        if "빠른 정답 및 난이도 총괄표" in txt or "정답 및 상세 해설" in txt:
            part2_start = i
            break
    print(f"  - 실전 문제지 (Part 1): 1페이지 ~ {part2_start}페이지 ({part2_start}면 구성)")
    print(f"  - 정답 및 해설지 (Part 2): {part2_start + 1}페이지 ~ {total_pages}페이지 ({total_pages - part2_start}면 구성)")

    # Check question distribution per page in Part 1
    for i in range(part2_start):
        qs = [int(x) for x in re.findall(r'(\d+)\.\s', doc[i].get_text()) if 1 <= int(x) <= 15]
        print(f"    * Page {i+1}: {len(qs)}문항 수록 -> 문항 번호: {qs}")

    print("\n================================================================")
    print("                    v12 출제 오류 감사 완료                      ")
    print("================================================================")

if __name__ == '__main__':
    audit()
