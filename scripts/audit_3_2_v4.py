import os
import re
import sys

def run_audit():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(base_dir) == 'scripts':
        base_dir = os.path.dirname(base_dir)
    md_path = os.path.join(base_dir, '출제', '2026_중1_국어_중간고사_실전모의고사_15제_3-2_v4.md')
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    print('=== 1. 빠른 정답표 파싱 ===')
    table_rows = re.findall(r'\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*([①②③④⑤])\*\*\s*\|\s*\*\*([상중하])\*\*\s*\|\s*([^|]+)\|\s*([^|]+)\|', text)
    print(f'총괄표 행 수: {len(table_rows)}')
    table_dict = {int(r[0]): {'ans': r[1], 'diff': r[2], 'concept': r[3].strip(), 'src': r[4].strip()} for r in table_rows}

    print('\n=== 2. 상세 해설 파싱 ===')
    expl_blocks = re.findall(r'####\s*\[문항\s*(\d+)\]\s*정답\s*([①②③④⑤])\s*\|\s*난이도\s*\[([상중하])\]', text)
    print(f'해설 블록 수: {len(expl_blocks)}')
    expl_dict = {int(e[0]): {'ans': e[1], 'diff': e[2]} for e in expl_blocks}

    print('\n=== 3. 3자 일치 점검 ===')
    ans_counts = {'①': 0, '②': 0, '③': 0, '④': 0, '⑤': 0}
    diff_counts = {'상': 0, '중': 0, '하': 0}
    all_match = True
    for q in range(1, 16):
        t = table_dict.get(q, {})
        e = expl_dict.get(q, {})
        ans_counts[t.get('ans', '')] = ans_counts.get(t.get('ans', ''), 0) + 1
        diff_counts[t.get('diff', '')] = diff_counts.get(t.get('diff', ''), 0) + 1
        m = (t.get('ans') == e.get('ans')) and (t.get('diff') == e.get('diff'))
        if not m:
            all_match = False
            print(f'Q{q:02d} 불일치: 표({t}) vs 해설({e})')
        else:
            print(f"Q{q:02d}: 정답 {t.get('ans')}, 난이도 [{t.get('diff')}] 일치")

    print(f'전체 일치 여부: {all_match}')
    print(f'정답 분포: {ans_counts}')
    print(f'난이도 분포: {diff_counts}')

    print('\n=== 4. 문제지 본문 내 난이도/배점/금지어 점검 ===')
    part1 = text.split('## [2부]')[0]
    p1_body = part1.split('## [1부]')[1]
    diff_tags = re.findall(r'\[(상|중|하)\]', p1_body)
    print(f'문제지 본문 내 [상/중/하] 노출: {len(diff_tags)}건 ({diff_tags})')

    scores = re.findall(r'\[\d+점\]|\b\d+점\b', text)
    print(f'배점 표기: {len(scores)}건 ({scores})')

    banned = ['통사 구조', '외형률', '두운/각운', '비장미', '파격의 율격', '다의성의 입체적 관계', '대유법', '권력 의지', '구원의 지향', '종교적 초월 세계', '유비쿼터스', '게이트키핑', '확증 편향']
    found_banned = [w for w in banned if w in text]
    print(f'금지 어휘: {found_banned}')

    mech = ['교과서에서 제시된', '교과서에 제시된', '교과서에 실린', '교과서에서 다룬']
    found_mech = [m for m in mech if m in p1_body]
    print(f'기계적 발문: {found_mech}')

    print('\n=== 5. 해설 구성요소 (출제 이유 / 오답 피하기) ===')
    reasons = re.findall(r'-\s*\*\*\[문제를 낸 이유\]\*\*', text)
    wrong_notes = re.findall(r'-\s*\*\*\[오답 피하기\]\*\*', text)
    print(f'[문제를 낸 이유]: {len(reasons)}/15')
    print(f'[오답 피하기]: {len(wrong_notes)}/15')

if __name__ == '__main__':
    run_audit()
