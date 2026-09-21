import os

def create_v6_md():
    with open('2026_중1_국어_중간고사_실전모의고사_15제_v5.md', 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Update header
    old_header = '# [2026학년도 중간고사 대비] 중학 국어 실전 모의 평가 15제 (v5: 흑백 2단 & 가독성 향상형)\n\n- **버전**: v5.0 (폰트 크기 및 줄간격·문항 간격 확대 최적화 버전)'
    new_header = '# [2026학년도 중간고사 대비] 중학 국어 실전 모의 평가 15제 (v6: 출제오류 전면교정 & 가독성 강화형)\n\n- **버전**: v6.0 (교과서 원문 정합성 및 개념 오류 전면 교정 완료 버전)'
    if old_header in text:
        text = text.replace(old_header, new_header)
    else:
        print("Warning: old_header not found directly")

    # 2. Update Q03 choice 5
    old_q3_5 = "⑤ '보슬보슬', '알롱알롱'과 같은 음성 상징어를 사용하여 시적 장면에 감각적 생동감을 부여하였다."
    new_q3_5 = "⑤ '보슬보슬', '알롱알롱'과 같이 말의 소리와 느낌을 살린 감각적 시어를 활용하여 생동감을 부여하였다."
    text = text.replace(old_q3_5, new_q3_5)

    # 3. Update Lee Seong-seon poem to exact textbook original
    old_poem = """사랑하는 별 하나
이성선

나도 별과 같은 사람은
하늘에 가지고 싶다.
어둠 속에서 무너지려는
마음을 비춰 주는
풍뎅이 눈물 같은 별 하나

나도 별과 같은 사람은
들판에 가지고 싶다.
새벽길에 풀잎 끝에
눈물짓듯 웃어 주는
풀잎 이슬 같은 별 하나

나도 별과 같은 사람은
이 세상에 가지고 싶다.
내가 부르면
어디서나 소리 없이
다가와 안아 주는 꽃 하나

나도 별과 같은 사람은
가슴속에 가지고 싶다.
내가 어둠 속을 헤맬 때
가만히 내 작은 손을 잡고
길을 비춰 주는 별 하나"""

    new_poem = """사랑하는 별 하나
이성선

나도 별과 같은 사람이
될 수 있을까.
외로워 쳐다보면
눈 마주쳐 마음 비춰 주는
그런 사람이 될 수 있을까.

나도 꽃이 될 수 있을까.
세상일이 괴로워 쓸쓸히 밖으로 나서는 날에
가슴에 화안히 안기어
눈물짓듯 웃어 주는
하얀 들꽃이 될 수 있을까.

가슴에 사랑하는 별 하나를 갖고 싶다.
외로울 때 부르면 다가오는
별 하나를 갖고 싶다.
마음 어두운 밤 깊을수록
우러러 쳐다보면
반짝이는 그 맑은 눈빛으로 나를 씻어
길을 비추어 주는
그런 사람 하나 갖고 싶다."""

    text = text.replace(old_poem, new_poem)

    # 4. Update Q14 item ㄹ
    old_q14_r = '㉣ 시각 장애인을 배려하고 차별 없는 언어를 쓰기 위해 손모아장갑이라는 대체어를 사용하였다.'
    new_q14_r = '㉣ 청각·언어 장애인을 배려하고 차별 없는 언어를 쓰기 위해 손모아장갑이라는 대체어를 사용하였다.'
    text = text.replace(old_q14_r, new_q14_r)

    # 5. Update Q06 explanation
    old_expl_6_intro = "어둠과 새벽길로 형상화된 인생의 시련 속에서 '무너지려는 마음을 비춰 주고 안아 주는 존재'"
    new_expl_6_intro = "시련과 외로움 속에서 '눈 마주쳐 마음 비춰 주는 존재', '가슴에 화안히 안기어 눈물짓듯 웃어 주는 존재'"
    text = text.replace(old_expl_6_intro, new_expl_6_intro)

    old_expl_6_body = "시에서 '별'과 '꽃'은 '어둠 속에서 무너지려는 마음을 비춰 주는 존재', '풀잎 끝에 눈물짓듯 웃어 주는 존재', '소리 없이 다가와 안아 주는 존재'로 묘사된다. 즉, 삶에 지치고 외로운 사람에게 따뜻한 위로와 희망, 구원이 되어 주는 순수하고 진실한 대상을 상징하므로 ②가 옳다."
    new_expl_6_body = "시에서 화자는 1~2연에서 '눈 마주쳐 마음 비춰 주는 별과 같은 사람', '세상일이 괴로울 때 화안히 안기어 눈물짓듯 웃어 주는 하얀 들꽃'과 같은 이타적인 존재가 되고 싶어 하며, 3연에서는 어두운 밤길을 비추어 주는 '사랑하는 별 하나'와 같은 사람을 곁에 두고 싶어 한다. 따라서 '별'과 '꽃'은 외롭고 힘든 사람에게 위로와 빛, 희망이 되어 주는 순수하고 진실한 대상을 상징하므로 ②가 정답이다."
    text = text.replace(old_expl_6_body, new_expl_6_body)

    # 6. Update Q14 explanation item ㄹ
    old_expl_14_r = "㉣ '손모아장갑': 장애인을 비하하지 않기 위해 만든 바람직한 대체어이다."
    new_expl_14_r = "㉣ '손모아장갑': 청각·언어 장애인을 차별하는 말을 개선하기 위해 만든 바람직한 대체어이다."
    text = text.replace(old_expl_14_r, new_expl_14_r)

    v6_file = '2026_중1_국어_중간고사_실전모의고사_15제_v6.md'
    with open(v6_file, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"{v6_file} created successfully! Length: {len(text)} characters.")

if __name__ == '__main__':
    create_v6_md()
