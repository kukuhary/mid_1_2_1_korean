import os
import re
import subprocess
import shutil
import fitz

def build_3_2_v3():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(base_dir) == 'scripts':

        base_dir = os.path.dirname(base_dir)
    md_path = os.path.join(base_dir, '출제', '2026_중1_국어_중간고사_실전모의고사_15제_3-2_v3.md')
    html_path = os.path.join(base_dir, '출제', 'exam_3_2_v3.html')
    pdf_path = os.path.join(base_dir, '출제', '2026_중1_국어_중간고사_실전모의고사_15제_3-2_v3.pdf')
    root_pdf_path = os.path.join(base_dir, '2026_중1_국어_중간고사_실전모의고사_15제_3-2_v3.pdf')

    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>2026학년도 중간고사 대비 국어 실전 모의 평가 15제 [3-(2) 품사의 종류와 특성] (3-2_v3)</title>
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
    margin-bottom: 14px;
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
    text-align: center;
  }
  .summary-table th, .summary-table td {
    border: 1px solid #555;
    padding: 4px 3px;
  }
  .summary-table th {
    background-color: #e0e0e0;
    font-weight: bold;
  }
  .summary-table td.ans {
    font-weight: bold;
    font-size: 9.2pt;
  }
  .summary-table td.src {
    font-size: 7.8pt;
    text-align: left;
    padding-left: 5px;
  }

  /* 해설 카드 */
  .expl-card {
    border: 1px solid #444;
    padding: 7px 9px;
    margin-bottom: 12px;
    background-color: #fff;
    break-inside: avoid;
    -webkit-column-break-inside: avoid;
    font-size: 8.8pt;
    line-height: 1.58;
  }
  .expl-header {
    border-bottom: 1px solid #000;
    padding-bottom: 4px;
    margin-bottom: 5px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .expl-qnum {
    font-size: 10.2pt;
    font-weight: bold;
  }
  .expl-badge {
    border: 1px solid #000;
    padding: 1px 5px;
    font-size: 8pt;
    font-weight: bold;
    background-color: #eaeaea;
  }
  .expl-ref-src {
    font-size: 7.9pt;
    color: #333;
    margin-bottom: 4px;
    background-color: #f2f2f2;
    padding: 2px 5px;
    border-left: 3px solid #555;
  }
  .expl-why {
    background-color: #f7f7f7;
    border: 1px dashed #888;
    padding: 4px 6px;
    margin-bottom: 5px;
    font-size: 8.2pt;
    line-height: 1.45;
  }
  .expl-why-title {
    font-weight: bold;
    margin-bottom: 2px;
  }
  .expl-sec-title {
    font-weight: bold;
    margin-top: 4px;
    margin-bottom: 2px;
    font-size: 8.6pt;
    text-decoration: underline;
  }
  .wrong-choice-list {
    margin: 3px 0 0 0;
    padding-left: 12px;
  }
  .wrong-choice-item {
    margin-bottom: 3px;
    font-size: 8.3pt;
    line-height: 1.45;
  }
</style>
</head>
<body>

  <!-- ==================== [1부] 실전 문제지 (Part 1) ==================== -->
  
  <!-- 1단 전폭 헤더 -->
  <div class="header-box">
    <div class="header-title">2026학년도 1학년 2학기 중간고사 대비 국어 실전 모의고사 (3-2_v3)</div>
    <div style="font-size: 9.5pt; font-weight: bold; color: #333;">[ 대단원 3. 능동적인 언어생활 - (2) 품사의 종류와 특성 집중 평가 (일반 중학교 표준 난이도형) ]</div>
    <table class="header-info-table">
      <tr>
        <td class="label">교과서 출처</td>
        <td>미래엔 중1-1 (131~147쪽)</td>
        <td class="label">제한 시간</td>
        <td>45분</td>
        <td class="label">문항 구성</td>
        <td>총 15문항 (5지 선다형)</td>
        <td class="label">난이도 체계</td>
        <td>일반 중학교 표준 (상3/중8/하4)</td>
      </tr>
    </table>
  </div>

  <div class="section-bar">
    <span>제 1 교시 : 국어영역 [선택형 15문항]</span>
    <span>※ 문제지에 난이도 및 배점은 표기되지 않습니다.</span>
  </div>

  <!-- 2단 본문 문제지 -->
  <div class="two-column-layout">

    <!-- 문항 1 -->
    <div class="question-block">
      <div class="question-prompt">1. 국어의 '단어'와 '품사'에 대한 설명으로 가장 적절한 것은?</div>
      <ul class="choice-list">
        <li class="choice-item">① 품사란 단어를 일정한 기준에 따라 공통된 성질을 지닌 것끼리 묶어 나눈 갈래이다.</li>
        <li class="choice-item">② 단어는 문장에서 반드시 두 개 이상의 형태소가 결합해야만 성립할 수 있다.</li>
        <li class="choice-item">③ 우리말의 모든 단어는 문장에 쓰일 때 문맥에 따라 형태가 자유롭게 변한다.</li>
        <li class="choice-item">④ 품사를 분류할 때는 단어가 지닌 글자 수와 음절의 길이를 가장 먼저 고려한다.</li>
        <li class="choice-item">⑤ 단어는 홀로 쓰일 수 있는 말이어야 하므로, 체언 뒤에 붙는 조사는 단어가 아니다.</li>
      </ul>
    </div>

    <!-- 문항 2 -->
    <div class="question-block">
      <div class="question-prompt">2. 다음 &lt;보기&gt;에서 설명하는 국어의 단어 분류 3대 기준을 바르게 짝지은 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        우리말의 단어를 분류할 때는 세 가지 기준을 적용합니다.<br>
        • (가): 문장에서 단어가 쓰일 때 형태가 변하는지 변하지 않는지를 따집니다.<br>
        • (나): 단어가 문장 안에서 다른 말과 맺는 관계나 구실을 따집니다.<br>
        • (다): 단어가 지니고 있는 고유한 뜻이나 성질을 따집니다.
      </div>
      <ul class="choice-list">
        <li class="choice-item">① (가) 기능 &nbsp; - &nbsp; (나) 형태 &nbsp; - &nbsp; (다) 의미</li>
        <li class="choice-item">② (가) 형태 &nbsp; - &nbsp; (나) 기능 &nbsp; - &nbsp; (다) 의미</li>
        <li class="choice-item">③ (가) 의미 &nbsp; - &nbsp; (나) 형태 &nbsp; - &nbsp; (다) 기능</li>
        <li class="choice-item">④ (가) 형태 &nbsp; - &nbsp; (나) 의미 &nbsp; - &nbsp; (다) 기능</li>
        <li class="choice-item">⑤ (가) 기능 &nbsp; - &nbsp; (나) 의미 &nbsp; - &nbsp; (다) 형태</li>
      </ul>
    </div>

    <!-- 문항 3 -->
    <div class="question-block">
      <div class="question-prompt">3. 다음 &lt;보기&gt;의 단어 목록에서 문장에 쓰일 때 형태가 변하지 않는 '불변어'만을 바르게 고른 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        [단어 목록]: ㉠ 나무 &nbsp; ㉡ 푸르다 &nbsp; ㉢ 달린다 &nbsp; ㉣ 셋 &nbsp; ㉤ 하늘 &nbsp; ㉥ 높다
      </div>
      <ul class="choice-list">
        <li class="choice-item">① ㉠, ㉡, ㉢</li>
        <li class="choice-item">② ㉡, ㉢, ㉥</li>
        <li class="choice-item">③ ㉠, ㉣, ㉤</li>
        <li class="choice-item">④ ㉣, ㉤, ㉥</li>
        <li class="choice-item">⑤ ㉠, ㉢, ㉤</li>
      </ul>
    </div>

    <!-- 문항 4 -->
    <div class="question-block">
      <div class="question-prompt">4. 다음 문장의 밑줄 친 단어 중, 사물의 '수량이나 순서'를 나타내는 '수사'에 해당하는 것은?</div>
      <ul class="choice-list">
        <li class="choice-item">① 영수는 오늘 아침 일찍 <u>도서관</u>에 갔다.</li>
        <li class="choice-item">② <u>우리</u>는 방과 후에 함께 운동하기로 약속했다.</li>
        <li class="choice-item">③ 맑은 가을 하늘에 <u>구름</u>이 평화롭게 떠 있다.</li>
        <li class="choice-item">④ 달리기 시합에서 결승선을 통과한 선수는 모두 <u>셋</u>이었다.</li>
        <li class="choice-item">⑤ <u>이것</u>은 내가 가장 아끼는 국어 공책이다.</li>
      </ul>
    </div>

    <!-- 문항 5 -->
    <div class="question-block">
      <div class="question-prompt">5. 다음 &lt;보기&gt;의 밑줄 친 단어들이 지닌 공통적인 문법적 특성으로 가장 적절한 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        • 지우는 오늘 도서관에서 <u>새</u> 책을 빌렸다.<br>
        • 삼촌은 옷장에서 <u>헌</u> 옷을 꺼내 정리하셨다.<br>
        • 우리는 <u>옛</u> 이야기를 들으며 밤을 지새웠다.
      </div>
      <ul class="choice-list">
        <li class="choice-item">① 상황에 따라 '새고, 새니'처럼 형태가 다양하게 변하는 가변어이다.</li>
        <li class="choice-item">② 문장에서 주로 주어나 목적어가 되어 몸체 구실을 하는 체언이다.</li>
        <li class="choice-item">③ '이/가', '을/를'과 같은 격조사와 자유롭게 결합하여 쓰인다.</li>
        <li class="choice-item">④ 주로 뒤에 오는 용언(동사·형용사)의 움직임이나 상태를 수식한다.</li>
        <li class="choice-item">⑤ 형태가 변하지 않으며, 뒤에 오는 체언의 뜻을 한정하여 꾸며 준다.</li>
      </ul>
    </div>

    <!-- 문항 6 -->
    <div class="question-block">
      <div class="question-prompt">6. 다음 &lt;보기&gt;의 문장에서 밑줄 친 단어 ㉠('빨리')과 ㉡('매우')에 대한 설명으로 가장 적절한 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        • 토끼가 들판을 ㉠ <u>빨리</u> 달린다.<br>
        • 봄 동산에 핀 진달래꽃이 ㉡ <u>매우</u> 아름답다.
      </div>
      <ul class="choice-list">
        <li class="choice-item">① ㉠은 동사('달린다')를 꾸미고, ㉡은 형용사('아름답다')를 꾸미는 부사이다.</li>
        <li class="choice-item">② ㉠과 ㉡은 모두 체언의 바로 앞에서 체언만을 꾸미는 관형사이다.</li>
        <li class="choice-item">③ ㉠은 형태가 변하는 가변어이고, ㉡은 형태가 변하지 않는 불변어이다.</li>
        <li class="choice-item">④ ㉠과 ㉡은 문장에서 독립적으로 쓰이며 느낌이나 놀람을 나타내는 감탄사이다.</li>
        <li class="choice-item">⑤ ㉠은 주어 역할을 담당하고, ㉡은 문장을 종결하는 서술어 역할을 담당한다.</li>
      </ul>
    </div>

    <!-- 문항 7 -->
    <div class="question-block">
      <div class="question-prompt">7. 국어의 '조사'에 대한 설명으로 가장 적절한 것은?</div>
      <ul class="choice-list">
        <li class="choice-item">① 조사는 자립성이 매우 강하므로 다른 단어와 항상 띄어 써야 한다.</li>
        <li class="choice-item">② 주로 체언의 뒤에 붙어서 그 말이 다른 말과 맺는 문법적 관계를 나타낸다.</li>
        <li class="choice-item">③ 모든 조사는 문맥이나 상황에 따라 형태가 자유롭게 변하는 가변어이다.</li>
        <li class="choice-item">④ 조사는 문장의 주체로서 사물의 이름이나 수량을 나타내는 구실을 한다.</li>
        <li class="choice-item">⑤ 조사는 다른 단어의 도움 없이 문장의 맨 앞에서 홀로 쓰일 수 있다.</li>
      </ul>
    </div>

    <!-- 문항 8 -->
    <div class="question-block">
      <div class="question-prompt">8. 다음 &lt;보기&gt;의 밑줄 친 단어 '이다'에 대한 설명으로 가장 적절한 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        • 영수는 성실한 중학교 <u>학생이다</u>.<br>
        • 영수는 우리 반 <u>반장이고</u>, 민수는 <u>부반장이다</u>.<br>
        • 그 사람이 만약 참된 <u>친구이면</u> 진심으로 도와줄 것이다.
      </div>
      <ul class="choice-list">
        <li class="choice-item">① 체언에 속하며 사람의 구체적인 명칭을 대신 나타내는 대명사이다.</li>
        <li class="choice-item">② 사물의 움직임이나 작용을 나타내는 단어이므로 동사로 분류된다.</li>
        <li class="choice-item">③ 조사이지만 문맥에 따라 '이고, 이니, 이면'처럼 형태가 변하는 가변어이다.</li>
        <li class="choice-item">④ 형태가 절대 변하지 않는 불변어이며, 체언의 뜻을 꾸며 주는 수식언이다.</li>
        <li class="choice-item">⑤ 문장에서 다른 말과 전혀 관계를 맺지 않고 독립적으로 쓰이는 감탄사이다.</li>
      </ul>
    </div>

    <!-- 문항 9 -->
    <div class="question-block">
      <div class="question-prompt">9. 다음 대화의 밑줄 친 단어 중, '독립언(감탄사)'에 해당하지 <ins>않는</ins> 것은?</div>
      <ul class="choice-list">
        <li class="choice-item">① "㉠ <u>어머나</u>, 벌써 시험 볼 시간이 다 되었네!"</li>
        <li class="choice-item">② "㉡ <u>앗</u>, 필통을 교실 사물함에 두고 왔어요."</li>
        <li class="choice-item">③ "㉢ <u>네</u>, 지금 바로 가서 가지고 오겠습니다."</li>
        <li class="choice-item">④ "㉣ <u>민수야</u>, 계단에서 뛰지 말고 조심해서 다녀오렴."</li>
        <li class="choice-item">⑤ "㉤ <u>와</u>, 다행히 시험 시작 전에 무사히 도착했구나."</li>
      </ul>
    </div>

    <!-- 문항 10 -->
    <div class="question-block">
      <div class="question-prompt">10. 다음 &lt;보기&gt;의 용언에 대한 설명으로 가장 적절한 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        [기본형]: '먹다'<br>
        [활용형]: 먹고, 먹으니, 먹어서, 먹는다, 먹자
      </div>
      <ul class="choice-list">
        <li class="choice-item">① '먹다'가 다양하게 모습을 바꿀 때 변하지 않는 부분인 '먹-'을 '어미'라고 한다.</li>
        <li class="choice-item">② '먹다'가 활용할 때 상황에 따라 형태가 변하는 '-고, -으니, -어서'를 '어간'이라고 한다.</li>
        <li class="choice-item">③ '먹다'는 문맥에 따라 형태가 바뀌지 않고 고정되어 쓰이는 불변어이다.</li>
        <li class="choice-item">④ '먹다'의 어간과 어미는 각각 독립하여 혼자서 문장으로 쓰일 수 있다.</li>
        <li class="choice-item">⑤ 용언이 활용할 때 형태가 변하지 않고 중심 의미를 담고 있는 앞부분을 '어간'이라고 한다.</li>
      </ul>
    </div>

    <!-- 문항 11 -->
    <div class="question-block">
      <div class="question-prompt">11. 다음 밑줄 친 단어 중 대상의 '성질이나 상태'를 나타내는 '형용사'로 가장 적절한 것은?</div>
      <ul class="choice-list">
        <li class="choice-item">① 가을바람이 불어오니 하늘이 무척 <u>높다</u>.</li>
        <li class="choice-item">② 동생이 운동장에서 축구공을 힘차게 <u>찬다</u>.</li>
        <li class="choice-item">③ 누나는 아침마다 공원을 힘차게 <u>달린다</u>.</li>
        <li class="choice-item">④ 친구들이 음악에 맞추어 신나게 춤을 <u>춘다</u>.</li>
        <li class="choice-item">⑤ 우리는 주말마다 도서관에서 책을 <u>읽는다</u>.</li>
      </ul>
    </div>

    <!-- 문항 12 -->
    <div class="question-block">
      <div class="question-prompt">12. 다음 &lt;자료&gt;의 설명에 따라 단어를 동사와 형용사로 바르게 짝지은 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;자 료&gt;</div>
        용언의 기본형에 현재 시제 어미 '-ㄴ다/-는다'를 결합해 보면 동사와 형용사를 구별할 수 있습니다.<br>
        • 현재 시제 어미가 결합할 수 있으면 ➔ 동사<br>
        • 현재 시제 어미가 결합할 수 없으면 ➔ 형용사
      </div>
      <ul class="choice-list">
        <li class="choice-item">① 동사: 예쁘다, 착하다 &nbsp;/&nbsp; 형용사: 가다, 웃다</li>
        <li class="choice-item">② 동사: 가다, 웃다 &nbsp;/&nbsp; 형용사: 예쁘다, 착하다</li>
        <li class="choice-item">③ 동사: 조용하다, 솟다 &nbsp;/&nbsp; 형용사: 읽다, 푸르다</li>
        <li class="choice-item">④ 동사: 맑다, 먹다 &nbsp;/&nbsp; 형용사: 빠르다, 솟다</li>
        <li class="choice-item">⑤ 동사: 작다, 넓다 &nbsp;/&nbsp; 형용사: 자다, 놀다</li>
      </ul>
    </div>

    <!-- 문항 13 -->
    <div class="question-block">
      <div class="question-prompt">13. 다음 &lt;보기&gt;의 밑줄 친 단어 ㉠과 ㉡의 품사를 바르게 분석한 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        • 우리는 사과 ㉠ <u>하나를</u> 반으로 나누어 먹었다.<br>
        • 바구니 속에 신선한 사과 ㉡ <u>한</u> 개가 놓여 있었다.
      </div>
      <ul class="choice-list">
        <li class="choice-item">① ㉠은 명사이고, ㉡은 수사이다.</li>
        <li class="choice-item">② ㉠은 관형사이고, ㉡은 부사이다.</li>
        <li class="choice-item">③ ㉠은 조사가 결합한 수사이고, ㉡은 뒤의 명사를 꾸미는 관형사이다.</li>
        <li class="choice-item">④ ㉠은 뒤의 명사를 수식하는 관형사이고, ㉡은 조사가 붙을 수 있는 수사이다.</li>
        <li class="choice-item">⑤ ㉠과 ㉡은 모두 사물의 수량을 나타내므로 품사가 동일한 수사이다.</li>
      </ul>
    </div>

    <!-- 문항 14 -->
    <div class="question-block">
      <div class="question-prompt">14. 다음 대화에 나타난 밑줄 친 표현의 어법상 문제점을 바르게 지적한 설명으로 가장 적절한 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        민지: "선생님, 이번 방학에도 부디 항상 <u>건강하세요</u>!"<br>
        지우: "선생님, 우리 다음 학기에도 모두 함께 <u>행복하자</u>!"
      </div>
      <ul class="choice-list">
        <li class="choice-item">① '건강하다'와 '행복하다'는 동작을 나타내는 동사이므로 과거 시제로만 써야 한다.</li>
        <li class="choice-item">② '건강하다'는 체언이므로 뒤에 조사를 붙여 '건강을 하세요'로 바꾸어야 한다.</li>
        <li class="choice-item">③ '행복하다'는 문장 전체를 꾸미는 부사이므로 어미와 결합할 수 없다.</li>
        <li class="choice-item">④ '건강하다'와 '행복하다'는 상태를 나타내는 형용사이므로 명령형이나 청유형 어미와 결합할 수 없다.</li>
        <li class="choice-item">⑤ 두 단어는 독립언인 감탄사이므로 문장의 서술어 자리에 올 수 없다.</li>
      </ul>
    </div>

    <!-- 문항 15 -->
    <div class="question-block">
      <div class="question-prompt">15. 다음 밑줄 친 문장 중 문법적으로 올바른 표현으로 가장 적절한 것은?</div>
      <ul class="choice-list">
        <li class="choice-item">① 이곳은 <u>옛부터</u> 전해 내려오는 유서 깊은 마을이다.</li>
        <li class="choice-item">② 봄이 되자 마당에 <u>온갖의</u> 꽃들이 활짝 피어났다.</li>
        <li class="choice-item">③ 그는 <u>새의</u> 신발을 신고 즐겁게 학교에 등교했다.</li>
        <li class="choice-item">④ 저 가게는 <u>헌으로</u> 된 책들을 저렴하게 판매한다.</li>
        <li class="choice-item">⑤ 우리 고장에는 <u>옛날부터</u> 전해 내려오는 아름다운 전설이 있다.</li>
      </ul>
    </div>

  </div> <!-- end of two-column-layout (Part 1) -->


  <!-- ==================== [2부] 정답 및 해설집 (Part 2) ==================== -->
  <div class="page-break"></div>

  <!-- 해설지 헤더 -->
  <div class="header-box">
    <div class="header-title">[정답 및 상세 해설집] 1학년 국어 3-(2) 품사의 종류와 특성 (3-2_v3)</div>
    <div style="font-size: 9.2pt; color: #333;">미래엔 교과서 단원 성취기준 부합 / 일반 중학교 표준 난이도 안배 (상3 / 중8 / 하4) / 100% 흑백 조판</div>
  </div>

  <div class="section-bar">
    <span>빠른 정답 및 출제 정보 총괄표</span>
    <span>난이도 분포: [상] 3문항 (20%) / [중] 8문항 (53.3%) / [하] 4문항 (26.7%)</span>
  </div>

  <!-- 정답 총괄표 -->
  <table class="summary-table">
    <thead>
      <tr>
        <th style="width: 7%;">문항</th>
        <th style="width: 8%;">정답</th>
        <th style="width: 8%;">난이도</th>
        <th style="width: 32%;">출제 핵심 개념</th>
        <th style="width: 45%;">참고 기출 및 교과서 출처</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>01</td><td class="ans">①</td><td>[하]</td><td>단어와 품사의 기본 정의</td><td class="src">미래엔 131쪽 / [2022 오성중 18번 변형]</td></tr>
      <tr><td>02</td><td class="ans">②</td><td>[하]</td><td>단어 분류 3대 기준 (형태, 기능, 의미)</td><td class="src">미래엔 131쪽 / [2025 장기중 12번 연계]</td></tr>
      <tr><td>03</td><td class="ans">③</td><td>[하]</td><td>형태에 따른 분류 (불변어 vs 가변어)</td><td class="src">미래엔 131~132쪽 / [2025 장기중 12번]</td></tr>
      <tr><td>04</td><td class="ans">④</td><td>[하]</td><td>체언(명사, 대명사, 수사)의 기본 식별</td><td class="src">미래엔 132~133쪽 / [2022 오성중 18번]</td></tr>
      <tr><td>05</td><td class="ans">⑤</td><td>[중]</td><td>수식언(관형사)의 기본 특성과 체언 수식</td><td class="src">미래엔 138쪽 / [2025 장기중 15번]</td></tr>
      <tr><td>06</td><td class="ans">①</td><td>[중]</td><td>수식언(부사)의 기본 기능과 용언 수식</td><td class="src">미래엔 139쪽 / [2022 심인중 16번]</td></tr>
      <tr><td>07</td><td class="ans">②</td><td>[중]</td><td>관계언(조사)의 특성과 앞말 붙여쓰기</td><td class="src">미래엔 141쪽 / [2022 심인중 12번]</td></tr>
      <tr><td>08</td><td class="ans">③</td><td>[중]</td><td>서술격 조사 '이다'의 특성과 활용</td><td class="src">미래엔 141쪽 / [2022 심인중 12번]</td></tr>
      <tr><td>09</td><td class="ans">④</td><td>[중]</td><td>독립언(감탄사)의 특성과 호칭어 구별</td><td class="src">미래엔 142쪽 / [2022 오성중 12번]</td></tr>
      <tr><td>10</td><td class="ans">⑤</td><td>[중]</td><td>용언의 구조 (어간과 어미의 역할)</td><td class="src">미래엔 135~136쪽 / [2022 오성중 13번]</td></tr>
      <tr><td>11</td><td class="ans">①</td><td>[중]</td><td>동사와 형용사의 기본 의미 구별</td><td class="src">미래엔 135쪽 / [2025 장기중 14번]</td></tr>
      <tr><td>12</td><td class="ans">②</td><td>[중]</td><td>동사 vs 형용사 판별 알고리즘 ('-ㄴ다/-는다')</td><td class="src">미래엔 137쪽 / [2022 심인중 13번]</td></tr>
      <tr><td>13</td><td class="ans">③</td><td>[상]</td><td>[변별 1] 수사 vs 수 관형사의 판별 구별</td><td class="src">미래엔 138쪽 / [2025 장기중 13번]</td></tr>
      <tr><td>14</td><td class="ans">④</td><td>[상]</td><td>[변별 2] 형용사의 청유·명령형 오류 교정</td><td class="src">미래엔 145쪽 / [2022 심인중 13번]</td></tr>
      <tr><td>15</td><td class="ans">⑤</td><td>[상]</td><td>[변별 3] 관형사 뒤 조사 결합 불가 교정</td><td class="src">미래엔 138쪽 / [2022 오성중 14번]</td></tr>
    </tbody>
  </table>

  <!-- 해설 2단 레이아웃 -->
  <div class="two-column-layout">

    <!-- 해설 01 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 01] 정답 ①</span>
        <span class="expl-badge">난이도 [하]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 131쪽 / [2022 오성중 18번 변형]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 단어의 갈래를 이해하고 품사의 특성을 탐구한다.<br>
        • 단원 목표: 품사의 개념을 명확히 이해하고 설명할 수 있다.<br>
        • 출제 의도: 품사 학습의 첫걸음으로서 품사의 정의를 바르게 알고 있는지 확인한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>품사는 단어를 일정한 기준(형태, 기능, 의미)에 따라 공통된 성질을 가진 것끼리 묶어 나눈 갈래이므로 ①번이 정확한 설명이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">② 단어는 하나의 형태소로도 이루어질 수 있다('하늘', '물' 등 단일어).</li>
        <li class="wrong-choice-item">③ 형태가 변하는 단어는 가변어(동사, 형용사, 서술격 조사)뿐이며 대다수는 불변어이다.</li>
        <li class="wrong-choice-item">④ 품사 분류 3대 기준은 형태, 기능, 의미이며 글자 수나 음절 길이는 무관하다.</li>
        <li class="wrong-choice-item">⑤ 조사는 자립할 수 있는 말(체언)에 쉽게 분리되므로 단어로 인정한다.</li>
      </ul>
    </div>

    <!-- 해설 02 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 02] 정답 ②</span>
        <span class="expl-badge">난이도 [하]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 131쪽 / [2025 장기중 12번 연계]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 단어의 갈래를 이해하고 품사의 특성을 탐구한다.<br>
        • 단원 목표: 단어를 분류하는 3대 기준을 체계적으로 이해한다.<br>
        • 출제 의도: 단어 분류의 3대 기준인 형태, 기능, 의미를 정확히 매핑하는지 점검한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>(가)는 형태 변화 여부를 따지므로 <strong>형태</strong>, (나)는 문장 안에서의 역할이나 구실을 따지므로 <strong>기능</strong>, (다)는 단어의 뜻이나 성질을 따지므로 <strong>의미</strong>이다. 따라서 바른 것은 ②번이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">①, ③, ④, ⑤는 형태, 기능, 의미의 정의를 잘못 매칭하였다.</li>
      </ul>
    </div>

    <!-- 해설 03 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 03] 정답 ③</span>
        <span class="expl-badge">난이도 [하]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 131~132쪽 / [2025 장기중 12번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 형태에 따른 단어 분류 기준을 이해한다.<br>
        • 단원 목표: 불변어와 가변어를 정확히 구별할 수 있다.<br>
        • 출제 의도: 일상 단어 목록에서 형태가 변하지 않는 불변어를 올바르게 식별하는지 평가한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>불변어는 형태가 변하지 않는 단어이다. ㉠ '나무'(명사), ㉣ '셋'(수사), ㉤ '하늘'(명사)은 불변어이다. 반면 ㉡ '푸르다', ㉢ '달린다', ㉥ '높다'는 활용하는 가변어(용언)이다. 따라서 ③번이 정답이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">①, ②, ④, ⑤는 가변어인 ㉡, ㉢, ㉥이 포함되어 있어 오답이다.</li>
      </ul>
    </div>

    <!-- 해설 04 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 04] 정답 ④</span>
        <span class="expl-badge">난이도 [하]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 132~133쪽 / [2022 오성중 18번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 체언의 하위 갈래인 명사, 대명사, 수사를 구별한다.<br>
        • 단원 목표: 사물의 수량이나 순서를 나타내는 수사의 개념을 익힌다.<br>
        • 출제 의도: 명사, 대명사, 수사 중 수사를 명확히 판별할 수 있는지 확인한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>④번의 '셋'은 사물의 수량을 나타내는 말이므로 <strong>수사</strong>이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① '도서관'은 구체적 장소의 명칭인 명사이다.</li>
        <li class="wrong-choice-item">② '우리'는 화자와 청자를 가리키는 대명사이다.</li>
        <li class="wrong-choice-item">③ '구름'은 사물의 이름을 나타내는 명사이다.</li>
        <li class="wrong-choice-item">⑤ '이것'은 사물을 지시하는 대명사이다.</li>
      </ul>
    </div>

    <!-- 해설 05 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 05] 정답 ⑤</span>
        <span class="expl-badge">난이도 [중]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 138쪽 / [2025 장기중 15번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 수식언의 특성을 이해하고 관형사의 역할을 파악한다.<br>
        • 단원 목표: 관형사가 체언을 수식하는 고유한 기능을 이해한다.<br>
        • 출제 의도: 관형사의 불변어 특성과 체언 수식 기능을 종합적으로 알고 있는지 확인한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>'새', '헌', '옛'은 모두 형태가 변하지 않는 불변어이며, 뒤에 오는 체언('책', '옷', '이야기')을 직접 꾸며 주는 <strong>관형사</strong>이다. 따라서 ⑤번이 바르다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① 관형사는 활용하지 않는 불변어이다.</li>
        <li class="wrong-choice-item">② 주어·목적어가 되는 몸체 구실은 체언의 특성이다.</li>
        <li class="wrong-choice-item">③ 관형사는 조사가 결합할 수 없다.</li>
        <li class="wrong-choice-item">④ 용언을 주로 꾸미는 것은 부사의 역할이다.</li>
      </ul>
    </div>

    <!-- 해설 06 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 06] 정답 ①</span>
        <span class="expl-badge">난이도 [중]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 139쪽 / [2022 심인중 16번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 부사의 수식 기능과 용언과의 관계를 이해한다.<br>
        • 단원 목표: 부사가 주로 동사와 형용사를 수식함을 확인한다.<br>
        • 출제 의도: 동사를 꾸미는 부사와 형용사를 꾸미는 부사의 구체 사례를 바르게 분석하는지 평가한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>㉠ '빨리'는 동사 '달린다'를 수식하고, ㉡ '매우'는 형용사 '아름답다'를 수식하는 <strong>부사</strong>이다. 따라서 ①번이 정확하다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">② 체언을 주로 꾸미는 것은 관형사이다.</li>
        <li class="wrong-choice-item">③ 부사는 모두 형태가 변하지 않는 불변어이다.</li>
        <li class="wrong-choice-item">④ 느낌·놀람을 나타내며 독립적인 것은 감탄사이다.</li>
        <li class="wrong-choice-item">⑤ '빨리'와 '매우'는 주어·서술어가 아니라 부사어이다.</li>
      </ul>
    </div>

    <!-- 해설 07 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 07] 정답 ②</span>
        <span class="expl-badge">난이도 [중]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 141쪽 / [2022 심인중 12번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 조사의 문법적 기능과 표기 원칙을 이해한다.<br>
        • 단원 목표: 조사가 체언에 붙어 관계를 나타냄을 파악한다.<br>
        • 출제 의도: 조사의 자립성 한계와 앞말 붙여쓰기 및 문법 구실을 바르게 이해했는지 점검한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>조사는 주로 체언의 뒤에 붙어서 앞말이 다른 말과 맺는 문법적 관계를 나타내거나 특별한 뜻을 더해 준다. 따라서 ②번이 바르다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① 조사는 자립성이 없어 앞말에 반드시 붙여 쓴다(맞춤법 41항).</li>
        <li class="wrong-choice-item">③ 조사는 '이다'를 제외하고 모두 형태가 불변이다.</li>
        <li class="wrong-choice-item">④ 사물의 이름이나 수량을 나타내는 것은 체언이다.</li>
        <li class="wrong-choice-item">⑤ 조사는 자립성이 없어 문장 맨 앞에 홀로 쓰이지 못한다.</li>
      </ul>
    </div>

    <!-- 해설 08 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 08] 정답 ③</span>
        <span class="expl-badge">난이도 [중]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 141쪽 / [2022 심인중 12번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 조사 중 유일한 가변어인 서술격 조사를 이해한다.<br>
        • 단원 목표: '이다'의 문법적 특성을 올바르게 설명할 수 있다.<br>
        • 출제 의도: 조사는 불변어이지만 '이다'만은 가변어라는 핵심 개념을 점검한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>'이다'는 체언 뒤에 붙어 서술어 자격을 부여하는 서술격 조사이다. 조사는 원칙적으로 불변어이지만, '이다'는 '이고, 이니, 이면'처럼 형태가 변하는 유일한 <strong>가변어</strong>이다. 따라서 ③번이 정확하다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① '이다'는 대명사가 아니라 관계언(조사)이다.</li>
        <li class="wrong-choice-item">② 움직임을 나타내지 않으며 동사가 아니다.</li>
        <li class="wrong-choice-item">④ 불변어가 아니며 수식언도 아니다.</li>
        <li class="wrong-choice-item">⑤ 감탄사가 아니라 체언에 결합하는 조사이다.</li>
      </ul>
    </div>

    <!-- 해설 09 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 09] 정답 ④</span>
        <span class="expl-badge">난이도 [중]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 142쪽 / [2022 오성중 12번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 감탄사의 개념과 다른 단어와의 차이점을 이해한다.<br>
        • 단원 목표: 부름말이나 감탄사를 정확히 판별할 수 있다.<br>
        • 출제 의도: 감탄사와 체언에 조사가 붙은 부름말('민수야')을 혼동하지 않는지 평가한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>㉣의 '민수야'는 사람 이름인 명사 '민수'에 호격 조사 '야'가 결합한 말이므로 감탄사가 아니다. 따라서 ④번이 정답이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① '어머나'는 놀람의 감탄사이다.</li>
        <li class="wrong-choice-item">② '앗'은 놀람의 감탄사이다.</li>
        <li class="wrong-choice-item">③ '네'는 대답의 감탄사이다.</li>
        <li class="wrong-choice-item">⑤ '와'는 감탄의 감탄사이다.</li>
      </ul>
    </div>

    <!-- 해설 10 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 10] 정답 ⑤</span>
        <span class="expl-badge">난이도 [중]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 135~136쪽 / [2022 오성중 13번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 용언의 어간과 어미 개념을 이해한다.<br>
        • 단원 목표: 활용할 때 형태가 변하는 부분과 변하지 않는 부분을 구별한다.<br>
        • 출제 의도: 기본형에서 어간과 어미의 명칭과 역할을 정확히 알고 있는지 확인한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>용언이 활용할 때 변하지 않는 앞부분을 <strong>어간</strong>, 뒤에서 다양하게 모습을 바꾸는 뒷부분을 <strong>어미</strong>라고 한다. 따라서 ⑤번이 정확한 설명이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① 변하지 않는 부분 '먹-'은 '어간'이다.</li>
        <li class="wrong-choice-item">② 상황에 따라 형태가 변하는 뒷부분은 '어미'이다.</li>
        <li class="wrong-choice-item">③ '먹다'는 다양하게 활용하는 가변어이다.</li>
        <li class="wrong-choice-item">④ 어간과 어미는 혼자서 홀로 쓰일 수 없다.</li>
      </ul>
    </div>

    <!-- 해설 11 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 11] 정답 ①</span>
        <span class="expl-badge">난이도 [중]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 135쪽 / [2025 장기중 14번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 동사와 형용사의 의미상 차이를 이해한다.<br>
        • 단원 목표: 움직임(동사)과 상태·성질(형용사)을 명확히 구별한다.<br>
        • 출제 의도: 상태나 성질을 나타내는 형용사를 정확히 골라내는지 확인한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>①번의 '높다'는 대상(하늘)의 상태나 성질을 나타내는 <strong>형용사</strong>이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">② '찬다'(기본형 '차다')는 공을 차는 움직임인 동사이다.</li>
        <li class="wrong-choice-item">③ '달린다'(기본형 '달리다')는 움직임인 동사이다.</li>
        <li class="wrong-choice-item">④ '춘다'(기본형 '추다')는 춤추는 움직임인 동사이다.</li>
        <li class="wrong-choice-item">⑤ '읽는다'(기본형 '읽다')는 책 읽는 움직임인 동사이다.</li>
      </ul>
    </div>

    <!-- 해설 12 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 12] 정답 ②</span>
        <span class="expl-badge">난이도 [중]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 137쪽 / [2022 심인중 13번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 동사와 형용사를 구별하는 문법적 기준을 적용한다.<br>
        • 단원 목표: 현재 시제 어미 결합 여부를 통해 동사와 형용사를 판별한다.<br>
        • 출제 의도: 교과서 핵심 판별 공식인 '-ㄴ다/-는다' 결합 테스트를 정확히 수행하는지 점검한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>'간다', '웃는다'처럼 현재 시제 어미가 자연스럽게 붙으면 <strong>동사</strong>이고, '예쁜다(X)', '착한다(X)'처럼 결합할 수 없으면 <strong>형용사</strong>이다. 따라서 바르게 짝지은 것은 ②번이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">①은 동사와 형용사가 정반대로 뒤바뀌어 있다.</li>
        <li class="wrong-choice-item">③ '조용하다'는 형용사, '솟다'는 동사이다.</li>
        <li class="wrong-choice-item">④ '맑다'는 형용사, '빠르다'는 형용사이다.</li>
        <li class="wrong-choice-item">⑤ '작다, 넓다'는 형용사이고, '자다, 놀다'는 동사이다.</li>
      </ul>
    </div>

    <!-- 해설 13 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 13] 정답 ③</span>
        <span class="expl-badge">난이도 [상]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 138쪽 / [2025 장기중 13번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 수사와 관형사의 문법적 차이를 탐구한다.<br>
        • 단원 목표: 수사와 수 관형사를 조사 결합 여부로 정확히 구별한다.<br>
        • 출제 의도: 학생들이 가장 많이 혼동하는 수사와 관형사의 판별 기준을 정확히 적용하는지 변별한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>㉠의 '하나를'은 조사 '를'이 결합하였으므로 <strong>수사</strong>이다. ㉡의 '한'은 조사가 결합하지 못하고 뒤의 의존 명사 '개'를 수식하므로 <strong>관형사</strong>이다. 따라서 ③번이 정확하다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① ㉠은 수사이며 ㉡은 관형사이다.</li>
        <li class="wrong-choice-item">② ㉠은 조사가 붙어 관형사가 될 수 없다.</li>
        <li class="wrong-choice-item">④ ㉠과 ㉡의 설명이 뒤바뀌어 있다.</li>
        <li class="wrong-choice-item">⑤ 기능과 형태가 다르므로 동일 품사가 아니다.</li>
      </ul>
    </div>

    <!-- 해설 14 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 14] 정답 ④</span>
        <span class="expl-badge">난이도 [상]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 145쪽 / [2022 심인중 13번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 어법에 맞게 국어를 바르게 사용하는 태도를 지닌다.<br>
        • 단원 목표: 형용사의 어미 결합 제약을 실생활 대화에 적용하여 오류를 바로잡는다.<br>
        • 출제 의도: 실생활에서 흔히 틀리는 '건강하세요', '행복하자'의 문법적 원인을 이해하는지 변별한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>'건강하다'와 '행복하다'는 상태를 나타내는 형용사이므로 명령형('-세요')이나 청유형('-자') 어미와 결합할 수 없다. 따라서 "건강하게 지내세요", "행복하게 지내자" 등으로 고쳐야 한다. 따라서 ④번이 바른 지적이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① 두 단어는 움직임을 나타내는 동사가 아니다.</li>
        <li class="wrong-choice-item">② '건강하다'는 용언이므로 체언이 아니다.</li>
        <li class="wrong-choice-item">③ '행복하다'는 부사가 아니라 형용사이다.</li>
        <li class="wrong-choice-item">⑤ 감탄사가 아니라 서술어로 쓰이는 형용사이다.</li>
      </ul>
    </div>

    <!-- 해설 15 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 15] 정답 ⑤</span>
        <span class="expl-badge">난이도 [상]</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 교과서 138쪽 / [2022 오성중 14번]</div>
      <div class="expl-why">
        <div class="expl-why-title">[문제를 낸 이유]</div>
        • 2022 개정 성취기준: 관형사의 문법적 제약(조사 결합 불가)을 이해한다.<br>
        • 단원 목표: 관형사 뒤에 조사를 붙여 쓰는 어법 오류를 바로잡는다.<br>
        • 출제 의도: 관형사 뒤에 조사가 결합할 수 없다는 국어 맞춤법 규정을 실증적으로 점검한다.
      </div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>관형사('옛', '온갖', '새', '헌')는 뒤에 조사가 결합할 수 없다. 따라서 '옛부터(X)'는 명사 '옛날'에 조사 '부터'가 결합한 <strong>'옛날부터(O)'</strong>로 표현해야 어법상 올바르다. 따라서 ⑤번이 유일하게 바른 문장이다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① 관형사 '옛'에 조사 '부터'가 붙어 틀림 ('옛날부터'로 수정).</li>
        <li class="wrong-choice-item">② 관형사 '온갖'에 조사 '의'가 붙어 틀림 ('온갖'으로 수정).</li>
        <li class="wrong-choice-item">③ 관형사 '새'에 조사 '의'가 붙어 틀림 ('새'로 수정).</li>
        <li class="wrong-choice-item">④ 관형사 '헌'에 조사 '으로'가 붙어 틀림 ('헌'으로 수정).</li>
      </ul>
    </div>

  </div> <!-- end of two-column-layout (Part 2) -->

</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[1] HTML 템플릿 생성 완료: {html_path}")

    # Edge headless PDF 렌더링
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_exe = next((p for p in edge_paths if os.path.exists(p)), None)
    if not edge_exe:
        print("[ERROR] Microsoft Edge 실행 파일을 찾을 수 없습니다.")
        return

    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_path}",
        html_path
    ]

    print(f"[2] PDF 빌드 실행 중: {pdf_path}")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        print(f"[OK] PDF 파일 생성 성공: {pdf_path}")
        shutil.copyfile(pdf_path, root_pdf_path)
        print(f"[OK] 루트 디렉토리 PDF 동기화 복사 완료: {root_pdf_path}")
    else:
        print(f"[FAIL] Return code: {res.returncode}, Stderr: {res.stderr.decode('utf-8', errors='ignore')}")
        return

    # PyMuPDF를 통한 정밀 조판 검증
    doc = fitz.open(root_pdf_path)
    total_pages = len(doc)
    print(f"\n[3] PDF 조판 검증 (총 {total_pages}페이지):")

    part2_start_page = -1
    for i, page in enumerate(doc):
        text = page.get_text()
        if '빠른 정답 및 출제 정보 총괄표' in text or '정답 및 상세 해설집' in text:
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
    has_sources = "출처: 미래엔 교과서" in p2_text
    print(f"  - 답지 출처 명시 검증: '출처: 미래엔 교과서' 수록 여부 = {has_sources} (PASS: True)")

    print("\n>>> 3-2_v3 빌드 및 조판 검증 성공적으로 완료! <<<")

if __name__ == '__main__':
    build_3_2_v3()
