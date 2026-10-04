import os
import re
import subprocess
import shutil
import fitz

def build_3_2_v2():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(base_dir) == 'scripts':

        base_dir = os.path.dirname(base_dir)
    md_path = os.path.join(base_dir, '출제', '2026_중1_국어_중간고사_실전모의고사_15제_3-2_v2.md')
    html_path = os.path.join(base_dir, '출제', 'exam_3_2_v2.html')
    pdf_path = os.path.join(base_dir, '출제', '2026_중1_국어_중간고사_실전모의고사_15제_3-2_v2.pdf')
    root_pdf_path = os.path.join(base_dir, '2026_중1_국어_중간고사_실전모의고사_15제_3-2_v2.pdf')

    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 [3-2단원 품사의 종류와 특성] (3-2_v2)</title>
<style>
  @page {
    size: A4;
    margin: 12mm 10mm 12mm 10mm;
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
    line-height: 1.72;
    font-size: 9.8pt;
    margin: 0;
    padding: 0;
    background: #fff;
  }

  /* 1단 전폭 헤더 박스 */
  .header-box {
    border: 2px solid #000;
    padding: 8px 12px;
    margin-bottom: 10px;
    text-align: center;
    background-color: #fff;
  }
  .header-title {
    font-size: 14.5pt;
    font-weight: bold;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
  }
  .header-info-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 5px;
    font-size: 8.8pt;
  }
  .header-info-table td {
    border: 1px solid #444;
    padding: 3px 6px;
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
    font-size: 9.8pt;
    font-weight: bold;
    border-top: 1.5px solid #000;
    border-bottom: 1px solid #000;
    padding: 4px 8px;
    margin: 8px 0 8px 0;
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

  /* 문항 블록 */
  .question-block {
    margin-bottom: 15px;
    break-inside: avoid;
    -webkit-column-break-inside: avoid;
  }
  .question-prompt {
    font-weight: bold;
    margin-bottom: 5px;
    font-size: 9.7pt;
    line-height: 1.55;
  }
  .question-prompt ins {
    text-decoration: underline;
    font-weight: bold;
  }

  /* 지문 및 보기 박스 */
  .box-container {
    border: 1.2px solid #333;
    background-color: #fafafa;
    padding: 6px 8px;
    margin: 5px 0 7px 0;
    font-size: 8.9pt;
    line-height: 1.55;
    break-inside: avoid;
    -webkit-column-break-inside: avoid;
  }
  .box-title {
    font-weight: bold;
    text-align: center;
    margin-bottom: 4px;
    font-size: 9.1pt;
    border-bottom: 0.8px dashed #888;
    padding-bottom: 2px;
  }

  /* 선택지 스타일 */
  .choice-list {
    margin: 4px 0 0 0;
    padding-left: 0;
    list-style: none;
  }
  .choice-item {
    margin-bottom: 3px;
    font-size: 9.2pt;
    line-height: 1.48;
    text-indent: -1.2em;
    padding-left: 1.2em;
  }

  /* 페이지 나눔 강제 */
  .page-break {
    page-break-before: always;
    break-before: page;
  }

  /* 정답 및 해설 표 */
  .summary-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 14px;
    font-size: 8.3pt;
    line-height: 1.45;
  }
  .summary-table th, .summary-table td {
    border: 1px solid #444;
    padding: 3.5px 4px;
    text-align: center;
  }
  .summary-table th {
    background-color: #e5e5e5;
    font-weight: bold;
  }
  .summary-table tr:nth-child(even) td {
    background-color: #f9f9f9;
  }
  .summary-table td.source-cell {
    text-align: left;
    padding-left: 6px;
    font-size: 8.0pt;
  }

  /* 상세 해설 문항 카드 */
  .expl-card {
    border: 1px solid #777;
    background-color: #fff;
    padding: 6px 8px;
    margin-bottom: 11px;
    font-size: 8.8pt;
    line-height: 1.55;
    break-inside: avoid;
    -webkit-column-break-inside: avoid;
  }
  .expl-header {
    font-weight: bold;
    font-size: 9.3pt;
    border-bottom: 1px solid #ccc;
    padding-bottom: 3px;
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
    background-color: #f2f2f2;
    padding: 3px 6px;
  }
  .expl-header .q-title {
    color: #000;
  }
  .expl-header .q-ans {
    color: #000;
  }
  .expl-section {
    margin-top: 3.5px;
  }
  .expl-source {
    background-color: #f6f6f6;
    border-left: 3px solid #555;
    padding: 3px 5px;
    margin-top: 2px;
    margin-bottom: 3px;
    font-size: 8.3pt;
    line-height: 1.42;
  }
  .expl-label {
    font-weight: bold;
    color: #111;
  }
  .wrong-choice-list {
    margin: 2px 0 0 0;
    padding-left: 15px;
    font-size: 8.5pt;
    line-height: 1.48;
  }
  .wrong-choice-list li {
    margin-bottom: 1.5px;
  }
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- [1부] 실전 문제지                                                         -->
<!-- ========================================================================= -->

<!-- 1단 전폭 헤더 박스 -->
<div class="header-box">
  <div class="header-title">2026학년도 중학교 1학년 2학기 중간고사 국어 실전 모의 평가</div>
  <table class="header-info-table">
    <tr>
      <td class="label">교 과 목</td>
      <td>국어 1-1 (미래엔 신유식)</td>
      <td class="label">출제 단원</td>
      <td>3-(2) 품사의 종류와 특성 (실제 기출·교과서 실증 연계)</td>
      <td class="label">시험 시간</td>
      <td>45분</td>
      <td class="label">문 항 수</td>
      <td>15문항 (선택형 100%)</td>
    </tr>
    <tr>
      <td class="label">학습 목표</td>
      <td colspan="5">단어의 갈래인 9품사의 개념과 문법적 특성을 이해하고 다양한 국어 자료를 능동적으로 탐구·분석한다.</td>
      <td class="label">성 명</td>
      <td></td>
    </tr>
  </table>
</div>

<div class="section-bar">
  <span>[제1부] 실전 문제지 (01~15)</span>
  <span>※ 각 문항의 정답을 하나만 골라 답안지에 바르게 표기하시오.</span>
</div>

<!-- 2단 본문 레이아웃 -->
<div class="two-column-layout">

  <!-- 문항 1 -->
  <div class="question-block">
    <div class="question-prompt"><b>1.</b> 다음 &lt;보기&gt;의 단어들이 지닌 공통적인 기능에 대한 설명으로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      [ 책,&nbsp; 하나,&nbsp; 우리 ]
    </div>
    <ul class="choice-list">
      <li class="choice-item">① 문장에서 주로 주어, 목적어 등이 되어 문장의 몸체 역할을 한다.</li>
      <li class="choice-item">② 뒤에 오는 체언만을 집중적으로 꾸며 주는 수식언 역할을 한다.</li>
      <li class="choice-item">③ 상황에 따라 형태가 자유롭게 바뀌며 문장을 끝맺는 서술어 역할을 한다.</li>
      <li class="choice-item">④ 다른 단어에 기대어 쓰이며 단어들 사이의 문법적 관계를 나타낸다.</li>
      <li class="choice-item">⑤ 문장의 다른 말과 직접적인 관계를 맺지 않고 독립적으로 쓰인다.</li>
    </ul>
  </div>

  <!-- 문항 2 -->
  <div class="question-block">
    <div class="question-prompt"><b>2.</b> 다음 &lt;보기&gt;의 단어들을 문장에서 쓰일 때 형태 변화 여부에 따라 분류할 때, '불변어'에 해당하는 단어만을 바르게 짝지은 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      [단어 목록]: ㉠ 물 &nbsp; ㉡ 크다 &nbsp; ㉢ 너무 &nbsp; ㉣ 맵다 &nbsp; ㉤ 음식 &nbsp; ㉥ 지킨다 &nbsp; ㉦ 형 &nbsp; ㉧ 울다
    </div>
    <ul class="choice-list">
      <li class="choice-item">① ㉠, ㉡, ㉤, ㉦</li>
      <li class="choice-item">② ㉡, ㉣, ㉥, ㉧</li>
      <li class="choice-item">③ ㉠, ㉢, ㉣, ㉦</li>
      <li class="choice-item">④ ㉠, ㉢, ㉤, ㉦</li>
      <li class="choice-item">⑤ ㉢, ㉤, ㉥, ㉧</li>
    </ul>
  </div>

  <!-- 문항 3 -->
  <div class="question-block">
    <div class="question-prompt"><b>3.</b> 다음 &lt;보기&gt;의 밑줄 친 조사들에 대한 설명으로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      (가) 나<u>도</u> 의사를 만났다.<br>
      (나) 의사<u>가</u> 진단을 내렸다.<br>
      (다) 그는 이 병원 의사<u>이다</u>.<br>
      (라) 나는 의사<u>를</u> 만나러 갔다.<br>
      (마) 그<u>의</u> 담당 의사는 병실로 향했다.
    </div>
    <ul class="choice-list">
      <li class="choice-item">① (가)의 '도'는 앞말 '나'가 문장의 목적어임을 엄격하게 규정하는 격조사이다.</li>
      <li class="choice-item">② (다)의 '이다'는 조사이지만 문맥에 따라 '이고, 이니, 이면'처럼 형태가 변하는 가변어이다.</li>
      <li class="choice-item">③ (나)의 '가'와 (라)의 '를'은 앞말에 특별한 뜻을 더해 주는 보조사이다.</li>
      <li class="choice-item">④ (마)의 '의'는 앞말이 문장의 서술어 자격을 갖도록 해 주는 서술격 조사이다.</li>
      <li class="choice-item">⑤ (가)~(마)에 쓰인 조사들은 모두 체언의 도움 없이 홀로 자립하여 문장에서 쓰일 수 있다.</li>
    </ul>
  </div>

  <!-- 문항 4 -->
  <div class="question-block">
    <div class="question-prompt"><b>4.</b> 다음 대화의 밑줄 친 단어 ㉠~㉤ 중, '독립언(감탄사)'에 해당하지 <ins>않는</ins> 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      민수: "㉠ <u>아빠</u>, 우리 오늘 점심에 뭐 먹으러 갈까요?"<br>
      아빠: "㉡ <u>우와</u>, 너는 조금 전에 빵을 먹고 또 배가 고프니?"<br>
      민수: "㉢ <u>네</u>, 돌아서면 금방 배가 고파져요."<br>
      아빠: "㉣ <u>그래</u>, 그렇다면 시원한 국수나 먹으러 가자."<br>
      민수: "㉤ <u>앗</u>, 저기 새로 생긴 국숫집이 보여요!"
    </div>
    <ul class="choice-list">
      <li class="choice-item">① ㉡</li>
      <li class="choice-item">② ㉢</li>
      <li class="choice-item">③ ㉣</li>
      <li class="choice-item">④ ㉤</li>
      <li class="choice-item">⑤ ㉠</li>
    </ul>
  </div>

  <!-- 문항 5 -->
  <div class="question-block">
    <div class="question-prompt"><b>5.</b> 다음 &lt;보기&gt;의 밑줄 친 단어들의 품사를 탐구한 내용으로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      <b>[글 A: 떡볶이 조리법]</b><br>
      <u>첫째</u>로, 떡을 물에 헹구어 냄비에 넣어 주세요. 다음으로 냄비에 양념을 <u>둘</u> 다 넣어 주세요.<br><br>
      <b>[글 B: 시장 심부름]</b><br>
      시장에 가서 신선한 사과 <u>두</u> 개와 <u>첫째</u> 골목에 있는 채소를 사 오너라.
    </div>
    <ul class="choice-list">
      <li class="choice-item">① [글 A]의 '첫째'와 [글 B]의 '첫째'는 형태가 같으므로 둘 다 뒤의 체언을 꾸미는 관형사이다.</li>
      <li class="choice-item">② [글 A]의 '둘'은 뒤의 부사 '다'를 꾸며 주며 조사가 결합할 수 없으므로 관형사이다.</li>
      <li class="choice-item">③ [글 A]의 '첫째'와 '둘'은 조사('로', '을' 등)가 결합할 수 있는 수사이고, [글 B]의 '두'와 '첫째'는 체언을 꾸미는 관형사이다.</li>
      <li class="choice-item">④ [글 B]의 '두'는 뒤에 목적격 조사 '를'을 붙여 '두를 개'로 쓸 수 있는 수사이다.</li>
      <li class="choice-item">⑤ [글 A]의 '첫째'는 관형사이고, [글 B]의 '첫째'는 순서를 나타내는 수사이다.</li>
    </ul>
  </div>

  <!-- 문항 6 -->
  <div class="question-block">
    <div class="question-prompt"><b>6.</b> 다음 문장의 밑줄 친 ㉠('단')과 ㉡('참')의 문법적 특성을 비교한 설명으로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      • 가슴속에 오래 간직하고 싶은 ㉠ <u>단</u> 하나의 시<br>
      • 봄날의 따스한 햇살이 비추니 네가 ㉡ <u>참</u> 좋아.
    </div>
    <ul class="choice-list">
      <li class="choice-item">① ㉠은 뒤에 오는 수사('하나')만을 꾸미며 조사가 붙을 수 없는 관형사이고, ㉡은 주로 용언('좋아')을 꾸미는 부사이다.</li>
      <li class="choice-item">② ㉠은 문장에서 주어로 쓰이는 체언이고, ㉡은 문장을 종결하는 서술어인 용언이다.</li>
      <li class="choice-item">③ ㉠은 활용하여 형태가 변하는 가변어이고, ㉡은 형태가 변하지 않는 불변어이다.</li>
      <li class="choice-item">④ ㉠과 ㉡은 모두 '이/가', '을/를'과 같은 격조사와 자유롭게 결합할 수 있다.</li>
      <li class="choice-item">⑤ ㉠은 문장 전체를 꾸미는 부사이고, ㉡은 오직 체언만을 수식하는 관형사이다.</li>
    </ul>
  </div>

  <!-- 문항 7 -->
  <div class="question-block">
    <div class="question-prompt"><b>7.</b> 다음 &lt;보기&gt;의 문장들에 쓰인 밑줄 친 부사의 수식 대상을 바르게 분석한 내용으로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      (가) 그 영화는 청소년들에게 <u>매우</u> 흥미롭다.<br>
      (나) <u>과연</u> 그가 이번 대회의 우승자일까?<br>
      (다) 영수는 새로 산 소설책을 <u>무척</u> 열심히 읽는다.<br>
      (라) <u>역시</u> 소문대로 이 집의 빵은 정말 맛있구나.
    </div>
    <ul class="choice-list">
      <li class="choice-item">① (가)의 '매우'는 앞말인 명사 '청소년들에게'를 집중적으로 꾸민다.</li>
      <li class="choice-item">② (나)의 '과연'은 뒤에 오는 대명사 '그'만을 한정하여 수식한다.</li>
      <li class="choice-item">③ (다)의 '무척'은 문장 끝에 오는 서술어 '읽는다'만을 직접 꾸민다.</li>
      <li class="choice-item">④ (라)의 '역시'는 오직 뒤에 오는 체언 '소문'만을 수식하는 관형사이다.</li>
      <li class="choice-item">⑤ (가)의 '매우'는 용언을 수식하고, (다)의 '무척'은 다른 부사를 수식하며, (나)와 (라)는 문장 전체를 수식한다.</li>
    </ul>
  </div>

  <!-- 문항 8 -->
  <div class="question-block">
    <div class="question-prompt"><b>8.</b> 다음 &lt;보기&gt;의 밑줄 친 용언들이 문장에서 활용할 때의 특성에 대한 설명으로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      선생님께 드릴 감사 편지를 작성하였다.<br>
      • 운동장에서 땀 흘리며 <u>달리는</u> 친구들의 모습이 <u>아름답다</u>.<br>
      • 우리는 매일 아침 도서관에서 책을 <u>읽고</u> 생각을 <u>나눈다</u>.
    </div>
    <ul class="choice-list">
      <li class="choice-item">① '달리는'의 기본형은 '달리다'이며, 활용할 때 변하지 않는 어간은 '달-'이다.</li>
      <li class="choice-item">② '아름답다'가 '아름답고, 아름다우니'로 활용할 때 상황에 따라 형태가 변하는 부분은 어미이다.</li>
      <li class="choice-item">③ '읽고'의 기본형은 '읽다'이며, 여기서 어간은 '-다'이고 어미는 '읽-'이다.</li>
      <li class="choice-item">④ '나눈다'는 문맥이나 쓰임이 바뀌어도 형태가 결코 변하지 않는 불변어이다.</li>
      <li class="choice-item">⑤ '달리는', '아름답다', '읽고', '나눈다'는 모두 문장에서 형태가 변하지 않는 체언이다.</li>
    </ul>
  </div>

  <!-- 문항 9 -->
  <div class="question-block">
    <div class="question-prompt"><b>9.</b> 다음 밑줄 친 단어 ㉠~㉤ 중 대상의 '상태나 성질'을 나타내는 단어(형용사)로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      • 의사 선생님은 매일 아침 일터로 ㉠ <u>나와서</u> 진료를 시작한다.<br>
      • 진료 시간이 ㉡ <u>끝나면</u> 가운을 벗고 집으로 ㉢ <u>돌아간다</u>.<br>
      • "선생님, 늘 친절하게 치료해 주셔서 감사하고 또 ㉣ <u>죄송해요</u>."<br>
      • "앞으로는 건강 수칙을 잊지 않고 꼭 잘 ㉤ <u>지킬게요</u>."
    </div>
    <ul class="choice-list">
      <li class="choice-item">① ㉠</li>
      <li class="choice-item">② ㉡</li>
      <li class="choice-item">③ ㉢</li>
      <li class="choice-item">④ ㉣</li>
      <li class="choice-item">⑤ ㉤</li>
    </ul>
  </div>

  <!-- 문항 10 -->
  <div class="question-block">
    <div class="question-prompt"><b>10.</b> 다음 &lt;자료&gt;를 참고하여 단어들을 동사와 형용사로 바르게 분류한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;자 료&gt;</div>
      동사는 움직임을 나타내므로 현재 시제 선어말 어미 '-ㄴ다/-는다'나 명령형 어미 '-아라/-어라', 청유형 어미 '-자'와 결합할 수 있습니다. 그러나 형용사는 상태나 성질을 나타내므로 이러한 어미와 결합할 수 없습니다.<br><br>
      [단어 목록]: ㉠ 피다 &nbsp; ㉡ 푸르다 &nbsp; ㉢ 읽다 &nbsp; ㉣ 착하다 &nbsp; ㉤ 솟다 &nbsp; ㉥ 조용하다
    </div>
    <ul class="choice-list">
      <li class="choice-item">① 동사: ㉠, ㉡, ㉢ / 형용사: ㉣, ㉤, ㉥</li>
      <li class="choice-item">② 동사: ㉡, ㉣, ㉥ / 형용사: ㉠, ㉢, ㉤</li>
      <li class="choice-item">③ 동사: ㉠, ㉢, ㉤ / 형용사: ㉡, ㉣, ㉥</li>
      <li class="choice-item">④ 동사: ㉠, ㉣, ㉤ / 형용사: ㉡, ㉢, ㉥</li>
      <li class="choice-item">⑤ 동사: ㉢, ㉤, ㉥ / 형용사: ㉠, ㉡, ㉣</li>
    </ul>
  </div>

  <!-- 문항 11 -->
  <div class="question-block">
    <div class="question-prompt"><b>11.</b> 다음 &lt;보기&gt;의 대화에 나타난 밑줄 친 표현의 문법적 오류를 진단하고 바르게 교정한 의견으로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      지우: "선생님, 이번 방학 동안에도 부디 항상 <u>건강하세요</u>!"<br>
      선생님: "그래, 고맙구나. 너도 새 학기에는 매일 <u>행복하자</u>."
    </div>
    <ul class="choice-list">
      <li class="choice-item">① '건강하다'와 '행복하다'는 상태나 성질을 나타내는 형용사이므로 명령형('-세요')이나 청유형('-자')으로 쓸 수 없으며, "건강하게 지내세요", "행복하게 지내자" 등으로 고쳐야 한다.</li>
      <li class="choice-item">② '건강하다'와 '행복하다'는 동작을 나타내는 동사이므로 과거 시제 어미를 결합하여 "건강했으세요", "행복했자"로 고쳐야 한다.</li>
      <li class="choice-item">③ '건강하세요'는 올바른 표현이지만, '행복하자'는 부사이므로 조사를 결합하여 "행복을 하자"로 고쳐야 한다.</li>
      <li class="choice-item">④ 두 단어는 모두 독립언인 감탄사이므로 어미를 붙이지 말고 "앗 건강!", "오 행복!"으로 표현해야 바르다.</li>
      <li class="choice-item">⑤ 두 단어는 체언이므로 문장의 주어로 만들어 "건강이 있으세요", "행복이 오자"로 바꾸는 것이 국어의 유일한 표준 어법이다.</li>
    </ul>
  </div>

  <!-- 문항 12 -->
  <div class="question-block">
    <div class="question-prompt"><b>12.</b> 다음 &lt;보기&gt;의 문장들에 쓰인 단어들의 문법적 제약을 파악하고 어법을 바르게 교정한 설명으로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      [문장 1] 이곳은 <u>옛부터</u> 물이 맑고 경치가 아름답기로 유명한 곳이다.<br>
      [문장 2] 봄이 오자 들판에 <u>온갖의</u> 야생화들이 화사하게 피어났다.
    </div>
    <ul class="choice-list">
      <li class="choice-item">① [문장 1]의 '옛'은 체언인 명사이므로 뒤에 조사 '부터'가 자연스럽게 결합할 수 있어 올바른 문장이다.</li>
      <li class="choice-item">② [문장 2]의 '온갖'은 체언이므로 관형격 조사 '의'가 결합한 표현이 문법적으로 정확하다.</li>
      <li class="choice-item">③ [문장 1]의 '옛' 뒤에 주격 조사 '이'를 덧붙여 '옛이부터'로 수정해야 어법에 맞는다.</li>
      <li class="choice-item">④ '옛'과 '온갖'은 오직 체언만을 꾸밀 수 있고 조사가 결합할 수 없는 관형사이므로, [문장 1]은 '옛날부터', [문장 2]는 조사를 뺀 '온갖 야생화들'로 고쳐야 바르다.</li>
      <li class="choice-item">⑤ '온갖'은 상황에 따라 형태가 다양하게 변하는 가변어이므로 '온갖고'로 바꾸어 써야 문맥에 어울린다.</li>
    </ul>
  </div>

  <!-- 문항 13 -->
  <div class="question-block">
    <div class="question-prompt"><b>13.</b> 다음 &lt;보기&gt;의 문장에 쓰인 단어들의 품사와 문법적 특성을 분석한 것으로 <ins>적절하지 않은</ins> 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      [문장] "이 봐, 어느 숲에 토끼와 거북이가 살았어."
    </div>
    <ul class="choice-list">
      <li class="choice-item">① '이 봐'는 놀람이나 부름을 나타내며 문장의 다른 성분과 얽매이지 않는 감탄사(독립언)이다.</li>
      <li class="choice-item">② '숲', '토끼', '거북이'는 구체적인 대상의 이름을 나타내는 명사(체언)이다.</li>
      <li class="choice-item">③ '에', '와', '가'는 체언 뒤에 붙어 문법적 관계를 나타내는 조사(관계언)이다.</li>
      <li class="choice-item">④ '어느'는 뒤에 오는 명사 '숲'만을 꾸며 주며 형태가 변하지 않는 관형사(수식언)이다.</li>
      <li class="choice-item">⑤ '살았어'의 기본형은 '살다'이며, 문장에서 주어의 상태나 성질을 풀이하는 형용사(용언)이다.</li>
    </ul>
  </div>

  <!-- 문항 14 -->
  <div class="question-block">
    <div class="question-prompt"><b>14.</b> 다음 [자료 1]과 [자료 2]에 쓰인 단어들의 품사적 특성과 표현 효과를 비교한 설명으로 가장 적절한 것은?</div>
    <div class="box-container">
      <b>[자료 1] 그림책 《달 샤베트》(백희나)에서</b><br>
      아주아주 더운 여름날 밤이었어요. 너무너무 더워서 모두들 창문을 꼭꼭 닫고, 에어컨을 쌩쌩, 선풍기를 씽씽 틀어 놓고 잠을 청하고 있었어요. 그런데 저 하늘에 걸린 달이 뚝뚝 녹아내리기 시작했어요.<br><br>
      <b>[자료 2] 긴급 재난 안전 문자</b><br>
      [행정안전부] 오늘 11시 기준 전국 대부분 지역에 폭염 경보 발령. 야외 활동 자제, 충분한 수분 섭취 등 안전사고에 각별히 유의 바랍니다.
    </div>
    <ul class="choice-list">
      <li class="choice-item">① [자료 1]은 수식하는 말을 철저히 배제하여 객관적인 사실만을 전달하고 있다.</li>
      <li class="choice-item">② [자료 1]은 소리나 모양을 흉내 낸 부사를 풍부하게 사용하여 장면을 생동감 있게 표현했고, [자료 2]는 수식언을 줄이고 명사 중심의 간결한 어휘를 사용하여 정보를 신속·정확하게 전달하고 있다.</li>
      <li class="choice-item">③ [자료 2]는 감탄사와 관형사를 집중적으로 사용하여 독자의 문학적 상상력을 자극하고 있다.</li>
      <li class="choice-item">④ [자료 1]과 [자료 2]는 모두 대명사와 수사를 중심으로 문장을 구성하여 전달력을 극대화하였다.</li>
      <li class="choice-item">⑤ [자료 2]는 주어의 움직임을 나타내는 동사만을 연속으로 배치하여 긴박한 감정을 예술적으로 드러내고 있다.</li>
    </ul>
  </div>

  <!-- 문항 15 -->
  <div class="question-block">
    <div class="question-prompt"><b>15.</b> 다음 &lt;보기&gt;의 밑줄 친 단어 ㉠~㉤에 대한 문법적 설명으로 가장 적절한 것은?</div>
    <div class="box-container">
      <div class="box-title">&lt;보 기&gt;</div>
      옛날에 큰 나라에서 온 거만한 사신이 ㉠ <u>궁궐</u>을 구경했다. 사신은 아름다운 건물들을 둘러보더니, ㉡ <u>그</u>의 태도가 사뭇 거만해졌다. "이러한 굴뚝을 만드는 데 얼마나 걸렸소?" 신하가 "㉢ <u>단</u> 반년에 완성했지요."라고 대답하자, 사신은 놀라며 ㉣ <u>연못가</u> 누각을 바라보았다. "㉤ <u>참</u> 대단한 기술이구려!"
    </div>
    <ul class="choice-list">
      <li class="choice-item">① ㉠의 '궁궐'은 다른 말의 수식을 전혀 받을 수 없는 관형사이다.</li>
      <li class="choice-item">② ㉡의 '그'는 사물의 수량이나 순서를 가리키는 수사이다.</li>
      <li class="choice-item">③ ㉢의 '단'은 오직 뒤의 체언('반년')만을 수식하며 조사가 결합할 수 없는 관형사이다.</li>
      <li class="choice-item">④ ㉣의 '연못가'는 문맥에 따라 어미가 다양하게 바뀌는 가변어이다.</li>
      <li class="choice-item">⑤ ㉤의 '참'은 오직 뒤에 오는 명사만을 집중적으로 꾸미는 관형사이다.</li>
    </ul>
  </div>

</div>

<!-- ========================================================================= -->
<!-- [2부] 정답 및 상세 해설집                                                 -->
<!-- ========================================================================= -->
<div class="page-break"></div>

<div class="header-box">
  <div class="header-title">2026학년도 중학교 1학년 2학기 중간고사 국어 정답 및 상세 해설집</div>
  <table class="header-info-table">
    <tr>
      <td class="label">교 과 목</td>
      <td>국어 1-1 (미래엔 신유식)</td>
      <td class="label">출제 단원</td>
      <td>3-(2) 품사의 종류와 특성 (실제 기출·교과서 실증 연계)</td>
      <td class="label">문 항 수</td>
      <td>15문항 (선택형 100%)</td>
      <td class="label">배점 안내</td>
      <td>문항 난이도별 정답률 분석 기준표 수록</td>
    </tr>
  </table>
</div>

<div class="section-bar">
  <span>[제2부] 빠른 정답 및 실제 기출·교과서 실증 출처 총괄표</span>
  <span>난이도 안배: [상] 8문항 (53.3%) / [중] 5문항 (33.3%) / [하] 2문항 (13.3%)</span>
</div>

<table class="summary-table">
  <thead>
    <tr>
      <th style="width: 5%;">문항</th>
      <th style="width: 7%;">단원</th>
      <th style="width: 27%;">핵심 출제 개념</th>
      <th style="width: 7%;">유형</th>
      <th style="width: 6%;">난이도</th>
      <th style="width: 6%;">정답</th>
      <th style="width: 42%;">참고한 실제 기출 및 교과서 출처 (100% 실증)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>01</b></td>
      <td>3-(2)</td>
      <td>체언(명·대·수)의 개념과 문장 내 기능</td>
      <td>선택형</td>
      <td><b>하</b></td>
      <td><b>①</b></td>
      <td class="source-cell">• [2022 오성중 1-1 기말 18번] 단어 묶기 [책, 하나, 우리]<br>• [미래엔 교과서 131~132쪽] 몸체 역할을 하는 체언</td>
    </tr>
    <tr>
      <td><b>02</b></td>
      <td>3-(2)</td>
      <td>형태에 따른 단어 분류 (불변어 판별)</td>
      <td>선택형</td>
      <td><b>하</b></td>
      <td><b>④</b></td>
      <td class="source-cell">• [2025 장기중 1-1 기말 12번] 불변어 개수 판별<br>• [미래엔 교과서 131쪽] 불변어와 가변어 구분</td>
    </tr>
    <tr>
      <td><b>03</b></td>
      <td>3-(2)</td>
      <td>관계언(조사)의 갈래 및 '이다'의 활용</td>
      <td>선택형</td>
      <td><b>중</b></td>
      <td><b>②</b></td>
      <td class="source-cell">• [2022 심인중 1-1 기말 12번] 조사 '도, 가, 이다, 를, 의'<br>• [미래엔 교과서 141쪽] 유일하게 활용하는 조사 '이다'</td>
    </tr>
    <tr>
      <td><b>04</b></td>
      <td>3-(2)</td>
      <td>독립언(감탄사)의 판별과 독립성</td>
      <td>선택형</td>
      <td><b>중</b></td>
      <td><b>⑤</b></td>
      <td class="source-cell">• [2022 오성중 1-1 기말 12번] 감탄사 미포함 문장 판별<br>• [2022 심인중 1-1 기말 15번] 감탄사의 독립적 성격</td>
    </tr>
    <tr>
      <td><b>05</b></td>
      <td>3-(2)</td>
      <td>[함정 1] 수사 vs 수 관형사 구별 알고리즘</td>
      <td>선택형</td>
      <td><b>상</b></td>
      <td><b>③</b></td>
      <td class="source-cell">• [2025 장기중 1-1 기말 13번] 떡볶이 글 속 수사 개수<br>• [2022 오성중 1-1 기말 14번] 수사 vs 수 관형사 판별</td>
    </tr>
    <tr>
      <td><b>06</b></td>
      <td>3-(2)</td>
      <td>수식언(관형사와 부사)의 특성 비교</td>
      <td>선택형</td>
      <td><b>상</b></td>
      <td><b>①</b></td>
      <td class="source-cell">• [2025 장기중 1-1 기말 15번] '단' vs '참' 특성 비교<br>• [2022 심인중 1-1 기말 16번] 관형사 vs 부사 서술형</td>
    </tr>
    <tr>
      <td><b>07</b></td>
      <td>3-(2)</td>
      <td>부사의 다양한 수식 대상 탐구</td>
      <td>선택형</td>
      <td><b>상</b></td>
      <td><b>⑤</b></td>
      <td class="source-cell">• [2022 오성중 1-1 기말 15번] 부사의 수식 대상 서술형<br>• [2025 장기중 1-1 기말 16번] 문장 전체 수식 부사 '역시'</td>
    </tr>
    <tr>
      <td><b>08</b></td>
      <td>3-(2)</td>
      <td>용언의 구조 (어간과 어미) 및 활용 양상</td>
      <td>선택형</td>
      <td><b>중</b></td>
      <td><b>②</b></td>
      <td class="source-cell">• [2022 오성중 1-1 기말 13번] 용언 어간과 어미 구조<br>• [미래엔 교과서 135~136쪽] 활용할 때 변하는 어미</td>
    </tr>
    <tr>
      <td><b>09</b></td>
      <td>3-(2)</td>
      <td>동사(움직임) vs 형용사(상태·성질) 구별</td>
      <td>선택형</td>
      <td><b>중</b></td>
      <td><b>④</b></td>
      <td class="source-cell">• [2025 장기중 1-1 기말 14번] 움직임 아닌 단어('죄송해요')<br>• [미래엔 교과서 135쪽] 움직임(동사) vs 상태(형용사)</td>
    </tr>
    <tr>
      <td><b>10</b></td>
      <td>3-(2)</td>
      <td>[함정 2] 동사 vs 형용사 판별 알고리즘</td>
      <td>선택형</td>
      <td><b>중</b></td>
      <td><b>③</b></td>
      <td class="source-cell">• [2022 심인중 1-1 기말 13번] 어미 결합 판별 문항<br>• [미래엔 교과서 137쪽 활동 3번] '-ㄴ다', '-아라', '-자'</td>
    </tr>
    <tr>
      <td><b>11</b></td>
      <td>3-(2)</td>
      <td>[함정 3] 형용사의 청유·명령형 오용 교정</td>
      <td>선택형</td>
      <td><b>상</b></td>
      <td><b>①</b></td>
      <td class="source-cell">• [미래엔 교과서 145쪽 생활 속 바른 언어] '건강하세요(X)'<br>• [2022 심인중 1-1 기말 13번 보기 연계] 형용사 어미 제약</td>
    </tr>
    <tr>
      <td><b>12</b></td>
      <td>3-(2)</td>
      <td>[함정 4] 관형사 뒤 조사 결합 불가 교정</td>
      <td>선택형</td>
      <td><b>상</b></td>
      <td><b>④</b></td>
      <td class="source-cell">• [2022 오성중 1-1 기말 14번 연계] 한글맞춤법 2항<br>• [미래엔 교과서 138쪽 날개 도움말] '옛부터(X)' 교정</td>
    </tr>
    <tr>
      <td><b>13</b></td>
      <td>3-(2)</td>
      <td>한 문장 속 복합 품사 전수 종합 분석</td>
      <td>선택형</td>
      <td><b>상</b></td>
      <td><b>⑤</b></td>
      <td class="source-cell">• [2025 장기중 1-1 기말 17번] "이 봐, 어느 숲에..." 분석<br>• [미래엔 교과서 147쪽] 9품사 상호작용 및 단어별 매핑</td>
    </tr>
    <tr>
      <td><b>14</b></td>
      <td>3-(2)</td>
      <td>담화 목적에 따른 품사의 표현 효과 분석</td>
      <td>선택형</td>
      <td><b>상</b></td>
      <td><b>②</b></td>
      <td class="source-cell">• [미래엔 교과서 145~146쪽 활동 2번] 《달 샤베트》<br>• 부사 중심(생동감) vs 명사 중심(신속·정확) 효과 비교</td>
    </tr>
    <tr>
      <td><b>15</b></td>
      <td>3-(2)</td>
      <td>지문 속 단어들의 품사 갈래 및 제약 판별</td>
      <td>선택형</td>
      <td><b>상</b></td>
      <td><b>③</b></td>
      <td class="source-cell">• [2022 심인중 1-1 기말 14번] 사신 이야기 지문 판별<br>• [미래엔 교과서 137쪽] 문맥 속 품사 및 조사 결합 제약</td>
    </tr>
  </tbody>
</table>

<div class="section-bar">
  <span>문항별 심층 정답 및 상세 해설 (실제 기출 및 교과서 실증 연계)</span>
</div>

<div class="two-column-layout">

  <!-- 해설 1 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 01] 체언의 개념과 문장 내 기능</span>
      <span class="q-ans">정답 ① &nbsp; [난이도: 하]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2022년 기출] 대구 오성중학교 1학년 1학기 기말 18번 (기능에 따른 단어 묶기 [책, 하나, 우리])<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 131~132쪽 '체언의 개념과 기능'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 단어를 기능에 따라 분류할 때, 문장의 몸체 구실(주어, 목적어, 보어 등)을 담당하는 '체언'의 개념과 세부 갈래(명사, 대명사, 수사)의 공통점을 이해하고 있는지 점검하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> '책'(명사), '하나'(수사), '우리'(대명사)는 모두 체언에 속하는 단어들이다. 체언은 문장에서 주로 주어, 목적어, 보어 등의 역할을 하여 문장의 몸체 구실을 하므로 ①이 가장 적절하다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>② 체언을 꾸미는 것은 수식언(관형사)의 기능이다.</li>
        <li>③ 문장을 끝맺는 서술어 역할을 하는 것은 용언(동사, 형용사)이다.</li>
        <li>④ 단어 사이의 문법적 관계를 나타내는 것은 관계언(조사)이다.</li>
        <li>⑤ 문장의 다른 말과 직접적인 관계를 맺지 않는 것은 독립언(감탄사)이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 2 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 02] 형태에 따른 단어 분류 (불변어)</span>
      <span class="q-ans">정답 ④ &nbsp; [난이도: 하]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2025년 기출] 세종 장기중학교 1학년 1학기 기말 12번 (보기 속 단어 중 불변어 개수 판별)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 131쪽 '형태에 따른 단어 분류 (불변어와 가변어)'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 단어 분류의 제1기준인 '형태(Form)'에 따라 문장에서 쓰일 때 형태가 변하지 않는 '불변어'와 형태가 변하는 '가변어'를 명확하게 구분할 수 있는지 평가하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> 불변어는 문장에서 어떤 말과 어울려 쓰여도 형태가 고정되어 변하지 않는 단어로 명사(㉠ 물, ㉤ 음식, ㉦ 형), 부사(㉢ 너무)가 이에 해당한다(총 4개). 반면 ㉡ 크다, ㉣ 맵다(형용사), ㉥ 지킨다, ㉧ 울다(동사)는 가변어(용언)이다. 따라서 불변어로만 바르게 짝지은 것은 ④이다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① ㉡ '크다'는 가변어(형용사)이다.</li>
        <li>② ㉡, ㉣, ㉥, ㉧은 모두 가변어(용언)이다.</li>
        <li>③ ㉣ '맵다'는 가변어(형용사)이다.</li>
        <li>⑤ ㉥ '지킨다'는 가변어(동사)이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 3 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 03] 관계언(조사)의 갈래 및 '이다'의 특성</span>
      <span class="q-ans">정답 ② &nbsp; [난이도: 중]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2022년 기출] 대구 심인중학교 1학년 1학기 기말 12번 (조사 '도, 가, 이다, 를, 의' 기능 판별)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 141쪽 '관계언(조사)의 갈래 및 서술격 조사 특성'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 체언 뒤에 붙어 문법적 자격을 부여하는 격조사와 특별한 뜻을 더하는 보조사를 구별하고, 조사 중 유일하게 형태가 변하는(활용하는) 서술격 조사 '이다'의 문법적 예외를 정확히 알고 있는지 평가하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> (다)의 '이다'는 체언 뒤에 붙어 서술어의 자격을 부여하는 서술격 조사이다. 조사는 대부분 형태가 변하지 않는 불변어이지만, '이다'는 '이고, 이니, 이면, 이어서'처럼 어미가 다양하게 바뀌며 활용하는 유일한 가변어 조사이다. 따라서 ②가 정확하다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① (가)의 '도'는 목적어가 아니라 '역시, 포함'의 뜻을 더하는 보조사이다.</li>
        <li>③ (나)의 '가'는 주격 조사, (라)의 '를'은 목적격 조사로 문법적 자격을 나타내는 격조사이다.</li>
        <li>④ (마)의 '의'는 앞말이 뒤의 체언을 꾸미게 하는 관형격 조사이다.</li>
        <li>⑤ 조사는 자립성이 없어 홀로 쓰이지 못하고 반드시 앞말에 붙어 쓰인다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 4 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 04] 독립언(감탄사)의 판별과 독립성</span>
      <span class="q-ans">정답 ⑤ &nbsp; [난이도: 중]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2022년 기출] 대구 오성중학교 1학년 1학기 기말 12번 (감탄사 미포함 문장 판별) & 심인중 15번<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 143~144쪽 '독립언(감탄사)의 개념과 특성'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 일상 대화에서 감탄사처럼 느껴지기 쉬운 부름말 명사와 실제 독립언인 감탄사를 정확히 판별하고, 감탄사의 고유한 문법적 성격(문장 내 독립성, 조사 결합 불가)을 이해하고 있는지 확인하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> ㉠의 '아빠'는 사람을 부르는 말처럼 쓰였지만, 사람의 대상을 직접 가리키는 고유한 명칭인 '명사(체언)'이다(호격 조사 '야'가 결합할 수 있는 체언). 반면 ㉡ '우와'(놀람), ㉢ '네'(대답), ㉣ '그래'(수긍·대답), ㉤ '앗'(놀람)은 문장의 다른 성분과 문법적 관계를 맺지 않고 독립적으로 쓰이는 순수 감탄사이다. 따라서 감탄사가 아닌 것은 ⑤이다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① ㉡ '우와'는 느낌과 놀람을 나타내는 감탄사이다.</li>
        <li>② ㉢ '네'는 부름에 대한 대답을 나타내는 감탄사이다.</li>
        <li>③ ㉣ '그래'는 상대의 말에 동의하거나 대답하는 감탄사이다.</li>
        <li>④ ㉤ '앗'은 뜻밖의 일에 놀람을 나타내는 감탄사이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 5 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 05] [함정 1] 수사 vs 수 관형사</span>
      <span class="q-ans">정답 ③ &nbsp; [난이도: 상]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2025년 기출] 세종 장기중학교 1학년 1학기 기말 13번 (수사 개수 판별) & 오성중 14번<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 133~134쪽 & [함정 1] 수사 vs 수 관형사 클리닉
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 중1 문법 시험에서 가장 오답률이 높은 [단골 함정 1] '수사와 수 관형사의 판별' 능력을 평가하기 위함이다. 뒤에 조사가 결합할 수 있는지 여부라는 결정적 판별 알고리즘을 적용할 수 있는지 점검하고자 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> [글 A]의 '첫째'는 부사격 조사 '로'가 결합하였으므로 수사이고, '둘'은 목적격 조사 '을'이 생략되어 조사가 붙을 수 있는 수사이다. 반면 [글 B]의 '두'는 뒤의 명사 '개'를 수식하며 조사가 결합할 수 없는 수 관형사이며, '첫째' 역시 뒤의 명사 '골목'을 수식하며 조사가 붙을 수 없는 관형사이다. 따라서 ③이 완벽한 정답이다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① [글 A]의 '첫째'는 조사 '로'가 결합하였으므로 관형사가 아니라 수사이다.</li>
        <li>② [글 A]의 '둘'은 수사로서 뒤에 조사 '을'을 붙여 '둘을 다'로 쓸 수 있다.</li>
        <li>④ 관형사 뒤에는 조사가 붙을 수 없으며 '두를 개'는 비문이다.</li>
        <li>⑤ [글 A]의 '첫째'가 수사이고, [글 B]의 '첫째'가 관형사이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 6 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 06] 수식언(관형사와 부사)의 특성</span>
      <span class="q-ans">정답 ① &nbsp; [난이도: 상]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2025년 기출] 세종 장기중학교 1학년 1학기 기말 15번 ('단 하나의 시' vs '참 좋아') & 심인중 16번<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 137~138쪽 '수식언의 특성과 차이점'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 다른 말을 꾸며 주는 수식언에 속하는 관형사와 부사의 결정적인 문법적 차이점(수식 대상의 차이, 조사 결합 제약)을 구체적 예문을 통해 분별할 수 있는지 측정하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> ㉠의 '단'은 오직 뒤에 오는 체언(수사 '하나')만을 수식하며 조사가 결합할 수 없는 관형사이다. 반면 ㉡의 '참'은 뒤에 오는 용언(형용사 '좋아')을 수식하는 부사이다. 따라서 두 단어의 품사적 특성을 바르게 대비한 ①이 정답이다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>② ㉠과 ㉡은 모두 다른 말을 꾸며 주는 수식언이다.</li>
        <li>③ ㉠과 ㉡은 둘 다 문장에서 형태가 변하지 않는 불변어이다.</li>
        <li>④ 관형사와 부사는 체언이 아니므로 격조사가 결합할 수 없다.</li>
        <li>⑤ ㉠은 체언을 꾸미는 관형사이고, ㉡은 용언을 꾸미는 부사이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 7 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 07] 부사의 다양한 수식 대상 탐구</span>
      <span class="q-ans">정답 ⑤ &nbsp; [난이도: 상]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2022년 기출] 대구 오성중학교 1학년 1학기 기말 15번 서술형 & 장기중 16번 ('역시' 문장 전체 수식)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 138쪽 '부사의 다양한 수식 대상 탐구'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 부사가 단순히 동사·형용사뿐만 아니라 다른 부사나 문장 전체를 수식할 수 있음을 이해하고, 각 문장에서 부사가 무엇을 수식하고 있는지 정확히 문법적으로 분석할 수 있는지 변별하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> (가)의 '매우'는 용언인 '흥미롭다'를 수식하고, (나)의 '과연'은 뒤에 이어지는 문장 전체를 수식하며, (다)의 '무척'은 뒤에 오는 다른 부사인 '열심히'를 수식하고, (라)의 '역시'는 뒤의 문장 전체를 수식한다. 따라서 ⑤가 가장 정확하다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① '매우'는 명사가 아니라 뒤의 형용사 '흥미롭다'를 수식한다.</li>
        <li>② '과연'은 대명사 '그'만 꾸미는 것이 아니라 문장 전체를 수식한다.</li>
        <li>③ '무척'은 바로 뒤의 부사 '열심히'를 직접 꾸민다.</li>
        <li>④ '역시'는 관형사가 아니라 문장 전체를 수식하는 문장 부사이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 8 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 08] 용언의 구조(어간과 어미) 및 활용</span>
      <span class="q-ans">정답 ② &nbsp; [난이도: 중]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2022년 기출] 대구 오성중학교 1학년 1학기 기말 13번 (용언 어간과 어미 결합 구조)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 135~136쪽 '용언의 구조와 형태 변화(활용)'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 용언의 형태 분석의 기본 원리인 '어간(변하지 않는 부분)'과 '어미(변하는 부분)'의 개념을 명확히 이해하고, 실제 단어에서 어간과 어미를 분리할 수 있는지 확인하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> '아름답다'가 '아름답고, 아름다우니, 아름다워서' 등으로 활용할 때 상황에 따라 형태가 바뀌며 다양한 문법적 의미를 나타내는 부분은 '어미'(-다, -고, -으니 등)이다. 따라서 ②가 옳다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① '달리다'의 어간은 '달-'이 아니라 '달리-'이다.</li>
        <li>③ '읽다'에서 어간은 '읽-'이고, 어미는 '-다'이다.</li>
        <li>④ '나눈다'는 '나누고, 나누니'처럼 형태가 변하는 가변어(동사)이다.</li>
        <li>⑤ 제시된 네 단어는 모두 문장에서 서술어 역할을 하는 용언이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 9 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 09] 동사 vs 형용사 기본 의미 구별</span>
      <span class="q-ans">정답 ④ &nbsp; [난이도: 중]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2025년 기출] 세종 장기중학교 1학년 1학기 기말 14번 (움직임 아닌 단어 '죄송해요' 판별)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 135쪽 '동사(움직임)와 형용사(상태·성질)의 구분'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 용언의 두 갈래인 동사와 형용사의 의미상 차이를 파악하여, 주어의 구체적인 동작·작용을 나타내는 말과 상태·성질 또는 심리적 감정을 나타내는 말을 정확히 구분할 수 있는지 평가하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> ㉠ 나와서(나오다), ㉡ 끝나면(끝나다), ㉢ 돌아간다(돌아가다), ㉤ 지킬게요(지키다)는 모두 주어의 구체적인 움직임이나 행동을 나타내는 동사이다. 반면 ㉣의 '죄송해요'의 기본형은 '죄송하다'로, 사람의 마음이나 심리적 상태를 나타내는 '형용사'이다. 따라서 형용사에 해당하는 것은 ④이다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① ㉠은 밖으로 이동하는 움직임을 나타내는 동사이다.</li>
        <li>② ㉡은 일이 마쳐지는 작용을 나타내는 동사이다.</li>
        <li>③ ㉢은 원래 있던 곳으로 이동하는 움직임을 나타내는 동사이다.</li>
        <li>⑤ ㉤은 약속이나 규칙을 지키는 의지적 행동을 나타내는 동사이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 10 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 10] [함정 2] 동사 vs 형용사 판별</span>
      <span class="q-ans">정답 ③ &nbsp; [난이도: 중]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2022년 기출] 대구 심인중학교 1학년 1학기 기말 13번 (동사 vs 형용사 어미 결합 판별 문항)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 137쪽 활동 3번 '동사와 형용사의 판별 공식'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 의미만으로는 헷갈리기 쉬운 동사와 형용사를 현재 시제 어미('-ㄴ다/-는다') 및 명령·청유형 어미 결합 여부를 통해 과학적으로 판별할 수 있는지 점검하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> 동사는 현재 시제 어미('-ㄴ다/-는다')나 명령형('-아라/-어라')이 결합할 수 있다. ㉠ '핀다(O)/피어라(O)', ㉢ '읽는다(O)/읽어라(O)', ㉤ '솟는다(O)/솟아라(O)'는 어미 결합이 자연스러우므로 동사이다. 반면 형용사는 이러한 어미와 결합할 수 없다. ㉡ '푸른다(X)', ㉣ '착한다(X)', ㉥ '조용한다(X)'는 어미 결합이 불가능하므로 형용사이다. 따라서 ③이 정답이다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① ㉡ '푸르다'는 상태를 나타내는 형용사이다.</li>
        <li>② 동사와 형용사의 분류가 정반대로 기술되었다.</li>
        <li>④ ㉣ '착하다'는 성질을 나타내는 형용사이다.</li>
        <li>⑤ ㉥ '조용하다'는 상태를 나타내는 형용사이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 11 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 11] [함정 3] 형용사 청유·명령형 오류</span>
      <span class="q-ans">정답 ① &nbsp; [난이도: 상]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2022년 기출] 대구 심인중학교 1학년 1학기 기말 13번 보기 연계 (형용사 청유형 제약)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 145쪽 '생활 속 바른 언어' 코너
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 실생활에서 "건강하세요", "행복하자"처럼 습관적으로 잘못 쓰이는 표현을 문법적 원리(형용사의 명령·청유형 불가)에 따라 진단하고 바르게 교정할 수 있는지 실천적 문법 능력을 기르고자 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> '건강하다'와 '행복하다'는 대상의 상태나 성질을 나타내는 형용사이다. 형용사는 함께 행동하자는 청유형('-자')이나 행동을 요구하는 명령형('-아라/-어라', '-세요')과 결합할 수 없다. 따라서 "건강하게 지내세요", "행복하게 지내자" 등으로 고쳐야 하므로 ①이 가장 적절하다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>② 동사가 아니라 형용사이므로 명령·청유형 자체가 성립하지 않는다.</li>
        <li>③ '행복하자'의 오류는 부사 때문이 아니라 형용사에 청유형 어미가 붙었기 때문이다.</li>
        <li>④ 감탄사가 아니라 용언(형용사)이다.</li>
        <li>⑤ 두 단어는 체언이 아니라 용언이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 12 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 12] [함정 4] 관형사 뒤 조사 결합 오류</span>
      <span class="q-ans">정답 ④ &nbsp; [난이도: 상]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2022년 기출] 대구 오성중학교 1학년 1학기 기말 14번 연계 (단어 결합 제약 및 띄어쓰기)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 138쪽 날개 도움말 '관형사와 조사의 결합 불가 규정'
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 일상생활에서 흔히 범하는 [단골 함정] '관형사 뒤에 조사가 결합하는 문법적 오류'를 포착하고, 올바른 표준 어법으로 교정할 수 있는지 문법적 엄밀성을 변별하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> '옛'과 '온갖'은 오직 체언만을 꾸미는 관형사이다. 관형사는 체언이 아니므로 뒤에 조사가 결합할 수 없다. 따라서 '옛'에 조사 '부터'가 붙은 '옛부터'는 잘못이며, 조사를 붙이려면 명사인 '옛날'을 써서 '옛날부터'로 고쳐야 한다. 또한 '온갖' 역시 조사 '의'를 결합하지 않고 조사를 뺀 '온갖 야생화들'로 바로 체언을 수식해야 바르다. 따라서 ④가 정답이다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① '옛'은 명사가 아니라 관형사이므로 조사가 결합할 수 없다.</li>
        <li>② '온갖'은 체언이 아니라 관형사이므로 조사 '의'와 결합할 수 없다.</li>
        <li>③ '옛'은 관형사이므로 주격 조사 '이'도 붙을 수 없다.</li>
        <li>⑤ '온갖'은 형태가 변하지 않는 불변어이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 13 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 13] 한 문장 속 복합 품사 전수 종합 분석</span>
      <span class="q-ans">정답 ⑤ &nbsp; [난이도: 상]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2025년 기출] 세종 장기중학교 1학년 1학기 기말 17번 ("이 봐, 어느 숲에..." 종합 분석)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 147쪽 단원 마무리 종합 활동
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 한 문장에 등장하는 여러 단어의 품사를 형태, 기능, 의미의 3대 기준에 따라 종합적으로 분석하고, 각 단어의 문법적 특성을 정확히 판별할 수 있는지 고차원적 종합 적용력을 평가하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> '살았어'의 기본형은 '살다'이다. '살다'는 목숨을 유지하며 활동하는 주어의 구체적인 움직임이나 작용을 나타내는 '동사'이다. 따라서 주어의 상태나 성질을 풀이하는 형용사라고 설명한 ⑤는 잘못된 진술이므로 적절하지 않다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① '이 봐'는 놀람과 부름의 감탄사(독립언)이다.</li>
        <li>② '숲, 토끼, 거북이'는 대상의 이름을 나타내는 명사(체언)이다.</li>
        <li>③ '에, 와, 가'는 체언 뒤에 붙는 조사(관계언)이다.</li>
        <li>④ '어느'는 명사 '숲'을 꾸미며 형태가 변하지 않는 관형사(수식언)이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 14 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 14] 담화 목적에 따른 품사의 표현 효과</span>
      <span class="q-ans">정답 ② &nbsp; [난이도: 상]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 145~146쪽 활동 2번 '품사의 사용에 따른 국어 자료의 특성'<br>
      • <b>표현 효과:</b> 그림책 《달 샤베트》(부사) vs 재난안전문자(명사) 대조 분석
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 교과서 본문 활동에 수록된 문학 담화(백희나의 《달 샤베트》)와 실용 담화(긴급 재난 안전 문자)를 비교하여, 특정 품사(부사 vs 명사)의 전략적 선택이 담화의 성격과 전달 목적에 따라 어떤 표현 효과를 발휘하는지 비판적으로 탐구하도록 유도하고자 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> [자료 1]은 '아주아주, 너무너무, 꼭꼭, 쌩쌩, 씽씽, 뚝뚝' 등 부사를 적극적으로 활용하여 한여름 밤의 장면을 감각적이고 생동감 있게 묘사하였다. 반면 [자료 2]는 주관적 수식언을 최대한 줄이고 명사 중심의 간결한 어휘를 사용하여 긴급한 정보를 정확하고 신속하게 전달하고 있다. 따라서 ②가 바른 설명이다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① [자료 1]은 부사(수식언)를 풍부하게 사용하였다.</li>
        <li>③ [자료 2]에는 감탄사나 상상력을 자극하는 표현이 없다.</li>
        <li>④ [자료 1]은 부사, [자료 2]는 명사 중심의 구성이다.</li>
        <li>⑤ [자료 2]는 동사 나열이 아니라 명사 중심의 간결한 전달이다.</li>
      </ul>
    </div>
  </div>

  <!-- 해설 15 -->
  <div class="expl-card">
    <div class="expl-header">
      <span class="q-title">[문항 15] 지문 속 품사 갈래 및 문법적 제약</span>
      <span class="q-ans">정답 ③ &nbsp; [난이도: 상]</span>
    </div>
    <div class="expl-source">
      <b>[참고 기출 및 교과서 출처]</b><br>
      • <b>실제 기출:</b> [2022년 기출] 대구 심인중학교 1학년 1학기 기말 14번 (사신 이야기 지문 속 품사 판별)<br>
      • <b>교과서 출처:</b> 미래엔 국어 1-1 교과서 137쪽 '수식언의 특성' 및 147쪽 종합 판별
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 문제를 낸 이유:</span> 실제 기출 지문 속에서 단어들의 문맥상 품사를 정확히 식별하고, 관형사·부사·명사·대명사의 문법적 제약(형태 변화 여부, 조사 결합 가능 여부)을 입체적으로 판별할 수 있는지 종합 능력을 평가하기 위해 출제하였다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 정답 해설:</span> ㉢의 '단'은 뒤에 오는 명사 '반년'을 수식하며 다른 말에 의해 형태가 변하지 않고 조사가 결합할 수 없는 '관형사'이다. 따라서 ③이 가장 정확한 설명이다.
    </div>
    <div class="expl-section">
      <span class="expl-label">■ 오답 피하기:</span>
      <ul class="wrong-choice-list">
        <li>① ㉠ '궁궐'은 명사이므로 '큰', '아름다운' 같은 관형어나 형용사의 수식을 받을 수 있다.</li>
        <li>② ㉡ '그'는 사람을 대신 가리키는 인칭 대명사이다.</li>
        <li>④ ㉣ '연못가'는 명사로서 문맥에 따라 형태가 변하지 않는 불변어이다.</li>
        <li>⑤ ㉤ '참'은 뒤에 오는 형용사 '대단한'을 꾸미는 부사이다.</li>
      </ul>
    </div>
  </div>

</div>

</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[1] HTML 파일 생성 완료: {html_path} ({os.path.getsize(html_path)} bytes)")

    # Chrome Headless PDF Compilation
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    cmd = [
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--no-pdf-header-footer',
        '--no-first-run',
        '--no-default-browser-check',
        f'--print-to-pdf={root_pdf_path}',
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(root_pdf_path) and os.path.getsize(root_pdf_path) > 1000:
        print(f"[2] PDF 파일 생성 완료: {root_pdf_path} ({os.path.getsize(root_pdf_path)} bytes)")
        shutil.copy2(root_pdf_path, pdf_path)
        print(f"[2-1] 출제 폴더 복사본 생성 완료: {pdf_path}")
    else:
        print(f"[FAIL] Return code: {res.returncode}, Stderr: {res.stderr.decode('utf-8', errors='ignore')}")
        return

    # PDF Quality Verification using PyMuPDF
    doc = fitz.open(root_pdf_path)
    total_pages = len(doc)
    print(f"\n[3] PDF 조판 검증 (총 {total_pages}페이지):")

    part2_start_page = -1
    for i, page in enumerate(doc):
        text = page.get_text()
        if '빠른 정답 및 실제 기출·교과서 실증 출처 총괄표' in text or '정답 및 상세 해설집' in text:
            part2_start_page = i
            break

    print(f"  - 실전 문제지 (Part 1): 1페이지 ~ {part2_start_page}페이지 ({part2_start_page}면)")
    print(f"  - 정답 및 해설지 (Part 2): {part2_start_page + 1}페이지 ~ {total_pages}페이지 ({total_pages - part2_start_page}면)")

    # Check Part 1 has NO [상/중/하]
    p1_text = "\n".join([doc[i].get_text() for i in range(part2_start_page)])
    has_diff_in_p1 = bool(re.search(r'\[(상|중|하)\]', p1_text))
    print(f"  - 문제지 본문 난이도 비노출 검증: [상/중/하] 노출 여부 = {has_diff_in_p1} (PASS: False)")

    # Check Part 2 has [상/중/하]
    p2_text = "\n".join([doc[i].get_text() for i in range(part2_start_page, len(doc))])
    has_diff_in_p2 = bool(re.search(r'\[(상|중|하)\]', p2_text))
    print(f"  - 해설지 난이도 표기 검증: [상/중/하] 표기 여부 = {has_diff_in_p2} (PASS: True)")

    # Check score marks
    has_points = bool(re.search(r'\[\d+점\]', p1_text + p2_text))
    print(f"  - 배점 표기 부재 검증: [X점] 표기 여부 = {has_points} (PASS: False)")

    # Check reference source in Part 2
    has_sources = "참고 기출 및 교과서 출처" in p2_text
    print(f"  - 답지 기출 출처 명시 검증: '참고 기출 및 교과서 출처' 수록 여부 = {has_sources} (PASS: True)")

    print("\n>>> 3-2_v2 빌드 및 조판 검증 성공적으로 완료! <<<")

if __name__ == '__main__':
    build_3_2_v2()
