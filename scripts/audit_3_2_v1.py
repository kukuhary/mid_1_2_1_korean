import re
import os

def audit_3_2_v1():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(base_dir) == 'scripts':
        base_dir = os.path.dirname(base_dir)
    md_path = os.path.join(base_dir, '출제', '2026_중1_국어_중간고사_실전모의고사_15제_3-2_v1.md')
    with open(md_path, 'r', encoding='utf-8') as f:
        md = f.read()

    print("================================================================")
    print("      3-2_v1 품사의 종류와 특성 출제 오류 정밀 감사 (Audit)      ")
    print("================================================================")

    # 1. 정답 총괄표 vs 상세 해설 일치성 검사
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

    # 2. 실전 문제지(1부) 내 금지 표기 노출 검사
    print("\n[2] 실전 문제지(1부) 내 금지 표기 노출 검사:")
    parts = md.split('## [1부] 실전 문제지')
    if len(parts) > 1:
        part1_md = parts[1].split('## [2부]')[0]
    else:
        part1_md = ""
    
    p1_diff_tags = re.findall(r'\[(상|중|하)\]', part1_md)
    print(f"  - 실전 문제지 본문 내 난이도([상/중/하]) 태그 수: {len(p1_diff_tags)}건 -> {'PASS (완전 비노출)' if len(p1_diff_tags) == 0 else f'FAIL ({p1_diff_tags})'}")

    points_in_all = re.findall(r'\[\d+점\]', md)
    print(f"  - 문제지 및 해설지 내 배점([X점]) 표기 수: {len(points_in_all)}건 -> {'PASS (배점 표기 일절 배제)' if len(points_in_all) == 0 else f'FAIL ({points_in_all})'}")

    # 3. 금지된 기계적 발문 검사
    print("\n[3] 기계적 발문 검사:")
    forbidden_phrases = ['교과서에서 제시된', '교과서에 제시된', '교과서에 실린', '교과서에서 다룬', '교과서에서 강조하는']
    found_forbidden = []
    for phrase in forbidden_phrases:
        if phrase in part1_md:
            found_forbidden.append(phrase)
    print(f"  - 기계적 발문(\"교과서에서 제시된\" 등) 검출 수: {len(found_forbidden)}건 -> {'PASS (0건)' if len(found_forbidden) == 0 else f'FAIL ({found_forbidden})'}")

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

    # 5. 오답 풀이 및 출제 이유 전수 검사
    print("\n[5] 해설집 구성 요소(오답 풀이, 출제 이유) 전수 점검:")
    reasons = re.findall(r'-\s*\*\*\[문제를 낸 이유\]\*\*', md)
    wrong_notes = re.findall(r'-\s*\*\*오답 풀이\*\*', md)
    print(f"  - [문제를 낸 이유] 수록 수: {len(reasons)}/15문항 -> {'PASS' if len(reasons) == 15 else 'FAIL'}")
    print(f"  - [오답 풀이] 수록 수: {len(wrong_notes)}/15문항 -> {'PASS' if len(wrong_notes) == 15 else 'FAIL'}")

    print("\n================================================================")
    print("                 3-2_v1 마크다운 감사 종료                       ")
    print("================================================================")

if __name__ == '__main__':
    audit_3_2_v1()
