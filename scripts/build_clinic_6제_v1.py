import os
import re
import subprocess
import shutil
import fitz

def build_clinic_6제_v1():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(base_dir) == 'scripts':

        base_dir = os.path.dirname(base_dir)
    html_path = os.path.join(base_dir, '출제', 'exam_clinic_6제_v1.html')
    pdf_path = os.path.join(base_dir, '출제', '2026_중1_국어_오답클리닉_실전모의고사_6제_v1.pdf')
    root_pdf_path = os.path.join(base_dir, '2026_중1_국어_오답클리닉_실전모의고사_6제_v1.pdf')

    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>2026학년도 중간고사 대비 국어 오답 클리닉 실전 모의 평가 6제 (v1)</title>
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
    font-size: 14pt;
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
    font-size: 9.6pt;
    font-weight: bold;
    border-top: 1.5px solid #000;
    border-bottom: 1px solid #000;
    padding: 4px 8px;
    margin: 7px 0 8px 0;
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
    margin-bottom: 13px;
    break-inside: avoid;
    -webkit-column-break-inside: avoid;
  }
  .question-prompt {
    font-weight: bold;
    margin-bottom: 5px;
    font-size: 9.6pt;
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
    margin-bottom: 12px;
    font-size: 8.5pt;
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
    font-size: 9.5pt;
  }
  .summary-table td.src {
    font-size: 8.2pt;
    text-align: left;
    padding-left: 5px;
  }

  /* 해설 카드 */
  .expl-card {
    border: 1px solid #444;
    padding: 7px 9px;
    margin-bottom: 11px;
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
    font-size: 10pt;
    font-weight: bold;
  }
  .expl-badge {
    border: 1px solid #000;
    padding: 1px 5px;
    font-size: 7.8pt;
    font-weight: bold;
    background-color: #eaeaea;
  }
  .expl-ref-src {
    font-size: 8pt;
    color: #333;
    margin-bottom: 4px;
    background-color: #f2f2f2;
    padding: 2px 5px;
    border-left: 3px solid #555;
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
    margin-bottom: 2px;
    font-size: 8.3pt;
    line-height: 1.45;
  }
</style>
</head>
<body>

  <!-- ==================== [1부] 실전 문제지 (Part 1) ==================== -->
  
  <!-- 1단 전폭 헤더 -->
  <div class="header-box">
    <div class="header-title">2026학년도 1학년 중간고사 대비 국어 실전 모의 평가 [오답 클리닉 특화 6제]</div>
    <div style="font-size: 9.3pt; font-weight: bold; color: #333;">[ 미래엔 교과서 본문 100% 직수록 / 비유·운율·어간과 어미 실전 예문 매칭 집중 평가 ]</div>
    <table class="header-info-table">
      <tr>
        <td class="label">교과서 출처</td>
        <td>미래엔 중1-1 (1단원), 중1-2 (3단원)</td>
        <td class="label">제한 시간</td>
        <td>15분</td>
        <td class="label">문항 구성</td>
        <td>총 6문항 (5지 선다형)</td>
        <td class="label">수험생 확인</td>
        <td>1학년 &nbsp; &nbsp; 반 &nbsp; &nbsp; 번 &nbsp; 성명: &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</td>
      </tr>
    </table>
  </div>

  <div class="section-bar">
    <span>제 1 교시 : 국어영역 [선택형 6문항]</span>
    <span>※ 문제지에 배점 및 난이도는 표기되지 않습니다.</span>
  </div>

  <!-- 2단 본문 문제지 -->
  <div class="two-column-layout">

    <!-- [01~04] 지문 박스 -->
    <div class="box-container">
      <div class="box-title">[01~04] 다음 글을 읽고 물음에 답하시오.</div>
      <strong>[가]</strong><br>
      길은 ㉠ <u>포도 덩굴</u><br>
      몇백 년이나 자라 땅덩이를 다 덮었다<br><br>
      이 덩굴 가지마다<br>
      ㉡ <u>포도송이 같은 마을</u>이 있고<br>
      포도알 같은 집들이 달렸다<br><br>
      포도알이 늘 때마다 포도송이는 커 가고<br>
      갈봄 없이 자라 가는<br><br>
      이 덩굴을 통하여<br>
      사람과 사람이 도와 가고 마을과 마을은 이어져서<br><br>
      세계는 ㉢ <u>한 덩이 과일</u>로<br>
      토실토실 익어 가고 있는 것이다.<br>
      <div style="text-align: right; font-size: 8.2pt; color: #555;">- 김종상, 〈길〉</div>
      <hr style="border: 0; border-top: 0.8px dashed #aaa; margin: 5px 0;">
      <strong>[나]</strong><br>
      ㉣ <u>아씨처럼 나린다</u><br>
      ㉤ <u>보슬보슬</u> 햇비<br>
      맞아 주자 다 같이<br>
      옥수숫대처럼 크게 닷 자 엿 자 자라게<br>
      ㉥ <u>해님이 웃는다</u> 나 보고 웃는다.<br><br>
      하늘 다리 놓였다 ㉦ <u>알롱알롱</u> 무지개<br>
      ㉧ <u>노래하자</u> 즐겁게 동무들아 이리 오나<br>
      다 같이 ㉨ <u>춤을 추자</u><br>
      해님이 웃는다 즐거워 웃는다.<br>
      <div style="text-align: right; font-size: 8.2pt; color: #555;">- 윤동주, 〈햇비〉</div>
    </div>

    <!-- 문항 1 -->
    <div class="question-block">
      <div class="question-prompt">1. 윗글 [가]의 밑줄 친 ㉠(<code>길은 포도 덩굴</code>)과 표현 방식이 같은 것만을 &lt;보기&gt;에서 있는 대로 고른 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        ㄱ. 내 누님같이 생긴 꽃이여.<br>
        ㄴ. 비 갠 하늘에 걸린 무지개는 아름다운 하늘 다리이다.<br>
        ㄷ. 맑은 밤하늘 아래 내 마음은 잔잔한 호수이다.<br>
        ㄹ. 호박잎 같은 어머니의 손등에 주름이 깊게 패었다.
      </div>
      <ul class="choice-list">
        <li class="choice-item">① ㄱ, ㄴ</li>
        <li class="choice-item">② ㄱ, ㄹ</li>
        <li class="choice-item">③ ㄴ, ㄷ</li>
        <li class="choice-item">④ ㄴ, ㄹ</li>
        <li class="choice-item">⑤ ㄷ, ㄹ</li>
      </ul>
    </div>

    <!-- 문항 2 -->
    <div class="question-block">
      <div class="question-prompt">2. 윗글 [나]의 밑줄 친 ㉣(<code>아씨처럼 나린다</code>)과 표현 방식이 같은 것은?</div>
      <ul class="choice-list">
        <li class="choice-item">① ㉠: 길은 포도 덩굴 몇백 년이나 자라 땅덩이를 다 덮었다.</li>
        <li class="choice-item">② ㉡: 이 덩굴 가지마다 포도송이 같은 마을이 있고 집들이 달렸다.</li>
        <li class="choice-item">③ ㉢: 세계는 한 덩이 과일로 토실토실 익어 가고 있는 것이다.</li>
        <li class="choice-item">④ ㉥: 해님이 웃는다 나 보고 웃는다.</li>
        <li class="choice-item">⑤ 하늘 다리 놓였다 알롱알롱 무지개.</li>
      </ul>
    </div>

    <!-- 문항 3 -->
    <div class="question-block">
      <div class="question-prompt">3. 윗글 [나]의 밑줄 친 ㉤(<code>보슬보슬</code>), ㉦(<code>알롱알롱</code>)과 같은 방식으로 말의 가락(운율)을 느끼게 하는 구절은?</div>
      <ul class="choice-list">
        <li class="choice-item">① 이 덩굴을 통하여 사람과 사람이 도와 가고</li>
        <li class="choice-item">② 골짜기 바위틈에서 맑은 샘물이 <u>졸졸졸</u> 솟아난다.</li>
        <li class="choice-item">③ 나도 별과 같은 사람이 될 수 있을까.</li>
        <li class="choice-item">④ 포도알이 늘 때마다 포도송이는 커 가고</li>
        <li class="choice-item">⑤ 동무들아 이리 오나, 우리 함께 손잡고 가자.</li>
      </ul>
    </div>

    <!-- 문항 4 -->
    <div class="question-block">
      <div class="question-prompt">4. 윗글 [나]의 밑줄 친 ㉧(<code>노래하자</code>), ㉨(<code>춤을 추자</code>)과 가락(운율)을 형성하는 방식이 가장 유사한 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;참고 자료: 미래엔 교과서 1단원 수록 시&gt;</div>
        (가) 나도 별과 같은 사람이 / 될 수 있을까. / 외로워 쳐다보면 / 눈 마주쳐 마음 비춰 주는 / 그런 사람이 될 수 있을까.<br>
        (나) 나도 꽃이 될 수 있을까. / 눈물짓듯 웃어 주는 / 하얀 들꽃이 될 수 있을까.<br>
        <div style="text-align: right; font-size: 8pt; color: #555;">- 이성선, 〈사랑하는 별 하나〉</div>
      </div>
      <ul class="choice-list">
        <li class="choice-item">① (가), (나)에서 문장의 끝마다 <strong>'~될 수 있을까'</strong>라는 종결 표현을 거듭 사용하였다.</li>
        <li class="choice-item">② (가), (나)에서 소리나 모양을 흉내 낸 말을 수없이 바꾸어 썼다.</li>
        <li class="choice-item">③ (가), (나)에서 각 줄의 첫 글자를 모두 같은 글자로 통일하였다.</li>
        <li class="choice-item">④ (가), (나)에서 글자 수를 세 글자, 네 글자로 한 치의 오차도 없이 맞추었다.</li>
        <li class="choice-item">⑤ (가), (나)에서 사람이 아닌 대상을 사람처럼 빗대어 행동하게 하였다.</li>
      </ul>
    </div>

    <!-- [05~06] 지문 박스 -->
    <div class="box-container">
      <div class="box-title">[05~06] 다음 글을 읽고 물음에 답하시오.</div>
      [교과서 본문 예문: 미래엔 국어 1-2 3-(2) 품사의 종류와 특성]<br>
      • 맑은 날에는 높은 하늘이 매우 ㉮ <u>푸르다</u>.<br>
      • 영수는 방과 후에 도서관에서 책을 ㉯ <u>읽는다</u>.<br>
      • 가을바람이 솔솔 불어오니 참 ㉰ <u>시원하다</u>.<br>
      • 우리는 쉬는 시간에 음악에 맞춰 신나게 ㉱ <u>춤춘다</u>.<br>
      • 저녁노을이 붉게 ㉲ <u>물들었다</u>.
    </div>

    <!-- 문항 5 -->
    <div class="question-block">
      <div class="question-prompt">5. 윗글의 밑줄 친 ㉮~㉲ 중, 문맥에 따라 형태가 바뀔 때 &lt;보기&gt;의 [설명]에 해당하는 부분(어간)만을 바르게 짝지은 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        [설명]: 용언(동사·형용사)이 여러 형태로 모습을 바꾸며 쓰일 때, 형태가 변하지 않고 실질적인 중심 의미를 담고 있는 앞부분.
      </div>
      <ul class="choice-list">
        <li class="choice-item">① ㉮: 푸- &nbsp;/&nbsp; ㉯: 읽는-</li>
        <li class="choice-item">② ㉮: 푸르- &nbsp;/&nbsp; ㉯: 읽-</li>
        <li class="choice-item">③ ㉯: 읽는- &nbsp;/&nbsp; ㉰: 시원-</li>
        <li class="choice-item">④ ㉰: 시원- &nbsp;/&nbsp; ㉱: 춤춘-</li>
        <li class="choice-item">⑤ ㉱: 춤춘- &nbsp;/&nbsp; ㉲: 물들었-</li>
      </ul>
    </div>

    <!-- 문항 6 -->
    <div class="question-block">
      <div class="question-prompt">6. 다음 &lt;보기&gt;의 안내에 따라 윗글의 밑줄 친 단어의 '기본형'과 '어간', '어미'를 바르게 나눈 것은?</div>
      <div class="box-container">
        <div class="box-title">&lt;보 기&gt;</div>
        [예시]: "친구가 사과를 <u>먹었다</u>."<br>
        • 기본형: 먹다<br>
        • 변하지 않는 부분(어간): 먹-<br>
        • 변하는 부분(어미): -었다
      </div>
      <ul class="choice-list">
        <li class="choice-item">① ㉮ <u>푸르다</u> ➔ 기본형: 푸다 / 어간: 푸- / 어미: -르다</li>
        <li class="choice-item">② ㉯ <u>읽는다</u> ➔ 기본형: 읽는다 / 어간: 읽는- / 어미: -다</li>
        <li class="choice-item">③ ㉰ <u>시원하다</u> ➔ 기본형: 시원하다 / 어간: 시원- / 어미: -하다</li>
        <li class="choice-item">④ ㉱ <u>춤춘다</u> ➔ 기본형: 춤추다 / 어간: 춤추- / 어미: -ㄴ다</li>
        <li class="choice-item">⑤ ㉲ <u>물들었다</u> ➔ 기본형: 물들이다 / 어간: 물들었- / 어미: -다</li>
      </ul>
    </div>

  </div> <!-- end of two-column-layout (Part 1) -->


  <!-- ==================== [2부] 정답 및 해설집 (Part 2) ==================== -->
  <div class="page-break"></div>

  <!-- 해설지 헤더 -->
  <div class="header-box">
    <div class="header-title">[정답 및 상세 해설집] 오답 클리닉 실전 모의 평가 6제 (v1)</div>
    <div style="font-size: 9pt; color: #333;">미래엔 교과서 본문 1:1 완벽 연계 / 비유·운율·어간어미 실전 예문 매칭 완벽 해설</div>
  </div>

  <div class="section-bar">
    <span>빠른 정답 및 출제 분석표</span>
    <span>교과서 본문 기반 실전 평가</span>
  </div>

  <!-- 정답 총괄표 -->
  <table class="summary-table">
    <thead>
      <tr>
        <th style="width: 10%;">문항</th>
        <th style="width: 12%;">정답</th>
        <th style="width: 40%;">출제 핵심 개념</th>
        <th style="width: 38%;">교과서 본문 출처</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>01</td><td class="ans">③</td><td>은유법 예문 매칭 ('A는 B이다' 구조)</td><td class="src">미래엔 중1-1 (16~18쪽, 김종상 〈길〉)</td></tr>
      <tr><td>02</td><td class="ans">②</td><td>직유법 예문 매칭 ('~처럼', '~같은' 연결어)</td><td class="src">미래엔 중1-1 (19~20쪽, 윤동주 〈햇비〉)</td></tr>
      <tr><td>03</td><td class="ans">②</td><td>음성 상징어(의성어·의태어) 반복을 통한 운율</td><td class="src">미래엔 중1-1 (19~20쪽, 윤동주 〈햇비〉)</td></tr>
      <tr><td>04</td><td class="ans">①</td><td>동일 종결 어미 반복을 통한 운율 형성</td><td class="src">미래엔 중1-1 (22~23쪽, 이성선 〈사랑하는 별 하나〉)</td></tr>
      <tr><td>05</td><td class="ans">②</td><td>용언의 어간(활용 시 변하지 않는 부분) 식별</td><td class="src">미래엔 중1-2 (135~136쪽, 용언의 활용)</td></tr>
      <tr><td>06</td><td class="ans">④</td><td>용언의 어간과 어미 실전 분절 분석</td><td class="src">미래엔 중1-2 (135~136쪽, 동사의 활용)</td></tr>
    </tbody>
  </table>

  <!-- 해설 2단 레이아웃 -->
  <div class="two-column-layout">

    <!-- 해설 01 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 01] 정답 ③</span>
        <span class="expl-badge">은유법 매칭</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 중1-1 국어 16~18쪽 (김종상, 〈길〉)</div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>본문의 ㉠ <code>길은 포도 덩굴</code>은 연결어(~처럼, ~같이 등) 없이 <strong>'A(길)는 B(포도 덩굴)이다'</strong> 형태로 두 대상을 빗댄 <strong>은유법</strong>입니다.
      <br>• <strong>ㄴ</strong>: '무지개(A)는 하늘 다리(B)이다' ➔ 은유법
      <br>• <strong>ㄷ</strong>: '내 마음(A)은 호수(B)이다' ➔ 은유법
      <br>따라서 은유법만을 고른 것은 ③(ㄴ, ㄷ)입니다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item"><strong>ㄱ</strong>: '누님<strong>같이</strong>'라는 연결어가 쓰인 <strong>직유법</strong>입니다.</li>
        <li class="wrong-choice-item"><strong>ㄹ</strong>: '호박잎 <strong>같은</strong>'이라는 연결어가 쓰인 <strong>직유법</strong>입니다.</li>
      </ul>
    </div>

    <!-- 해설 02 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 02] 정답 ②</span>
        <span class="expl-badge">직유법 매칭</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 중1-1 국어 19~20쪽 (윤동주, 〈햇비〉)</div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>㉣ <code>아씨처럼 나린다</code>는 <strong>'~처럼'</strong>이라는 연결어를 사용하여 햇비가 내리는 조용하고 고운 모습을 직접 빗댄 <strong>직유법</strong>입니다.
      <br><strong>②번의 ㉡ <code>포도송이 같은 마을</code></strong> 역시 <strong>'~같은'</strong>이라는 연결어를 사용하여 마을의 모습을 직접 빗댄 <strong>직유법</strong>이므로 표현 방식이 같습니다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① ㉠(<code>길은 포도 덩굴</code>), ③ ㉢(<code>세계는 한 덩이 과일</code>), ⑤(<code>하늘 다리</code>)는 연결어가 없는 <strong>은유법</strong>입니다.</li>
        <li class="wrong-choice-item">④ ㉥(<code>해님이 웃는다</code>)은 사람이 아닌 해를 사람처럼 나타낸 <strong>의인법</strong>입니다.</li>
      </ul>
    </div>

    <!-- 해설 03 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 03] 정답 ②</span>
        <span class="expl-badge">음성상징어 운율</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 중1-1 국어 19~20쪽 (윤동주, 〈햇비〉)</div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>본문의 ㉤ <code>보슬보슬</code>과 ㉦ <code>알롱알롱</code>은 소리나 모양을 흉내 낸 <strong>음성 상징어(의태어)</strong>를 사용하여 경쾌한 말의 가락(운율)을 형성합니다.
      <br><strong>②번의 '졸졸졸'</strong> 역시 샘물이 솟아 흘러가는 소리를 흉내 낸 <strong>의성어(음성 상징어)</strong>를 활용하여 같은 방식으로 운율을 느끼게 합니다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① 단어('사람')와 조사의 반복을 통한 운율</li>
        <li class="wrong-choice-item">③ 종결 어미('~ㄹ까')의 반복을 통한 운율</li>
        <li class="wrong-choice-item">④ 비슷한 문장 구조('~ㄹ 때마다 ~는 커 가고')의 대구적 반복</li>
        <li class="wrong-choice-item">⑤ 청유형 종결 어미('~자')를 통한 운율 형성</li>
      </ul>
    </div>

    <!-- 해설 04 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 04] 정답 ①</span>
        <span class="expl-badge">어미 반복 운율</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 중1-1 국어 22~23쪽 (이성선, 〈사랑하는 별 하나〉)</div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>본문의 ㉧ <code>노래하자</code>, ㉨ <code>춤을 추자</code>는 문장의 끝마다 <strong>'~자'라는 동일한 청유형 종결 어미를 반복</strong>하여 리듬감을 만듭니다.
      <br>교과서 수록작인 이성선의 〈사랑하는 별 하나〉 역시 문장 끝마다 <strong>'~될 수 있을까'라는 동일한 종결 표현을 거듭 사용</strong>하여 가락을 형성하고 있으므로 운율 형성 방식이 일치합니다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">③ '첫 글자 통일'은 현대시의 운율 형성 방법이 아닙니다.</li>
        <li class="wrong-choice-item">④ 글자 수의 엄격한 고정은 정형시(시조 등)의 특징입니다.</li>
      </ul>
    </div>

    <!-- 해설 05 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 05] 정답 ②</span>
        <span class="expl-badge">어간 식별</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 중1-2 국어 135~136쪽 (용언의 활용)</div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>&lt;보기&gt;의 설명은 용언(동사·형용사)이 활용할 때 형태가 변하지 않는 <strong>'어간'</strong>에 대한 설명입니다.
      <br>• ㉮ <code>푸르다</code>: <strong>푸르</strong>-고, <strong>푸르</strong>-니 ➔ 어간: <strong>'푸르-'</strong>
      <br>• ㉯ <code>읽는다</code>: <strong>읽</strong>-고, <strong>읽</strong>-으니 ➔ 어간: <strong>'읽-'</strong>
      <br>따라서 어간만을 바르게 짝지은 것은 ②번입니다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">㉰ <code>시원하다</code>: <strong>시원하</strong>-고 ➔ 어간은 <strong>'시원하-'</strong></li>
        <li class="wrong-choice-item">㉱ <code>춤춘다</code>: <strong>춤추</strong>-고 ➔ 어간은 <strong>'춤추-'</strong></li>
        <li class="wrong-choice-item">㉲ <code>물들었다</code>: <strong>물들</strong>-고 ➔ 어간은 <strong>'물들-'</strong></li>
      </ul>
    </div>

    <!-- 해설 06 -->
    <div class="expl-card">
      <div class="expl-header">
        <span class="expl-qnum">[문항 06] 정답 ④</span>
        <span class="expl-badge">어간·어미 분절</span>
      </div>
      <div class="expl-ref-src">출처: 미래엔 중1-2 국어 135~136쪽 (동사의 활용)</div>
      <div class="expl-sec-title">[정답 및 핵심 풀이]</div>
      <div>㉱ <code>춤춘다</code>: 기본형은 <strong>'춤추다'</strong>입니다. '춤추고, 춤추니, 춤추어서'로 활용하므로 변하지 않는 어간은 <strong>'춤추-'</strong>이며, 현재 시제를 나타내는 어미 <strong>'-ㄴ다'</strong>가 결합한 구조입니다. 따라서 ④번이 정확합니다.</div>
      <div class="expl-sec-title">[오답 피하기]</div>
      <ul class="wrong-choice-list">
        <li class="wrong-choice-item">① ㉮ <code>푸르다</code> ➔ 기본형: 푸르다 / 어간: 푸르- / 어미: -다</li>
        <li class="wrong-choice-item">② ㉯ <code>읽는다</code> ➔ 기본형: 읽다 / 어간: 읽- / 어미: -는다</li>
        <li class="wrong-choice-item">③ ㉰ <code>시원하다</code> ➔ 기본형: 시원하다 / 어간: 시원하- / 어미: -다</li>
        <li class="wrong-choice-item">⑤ ㉲ <code>물들었다</code> ➔ 기본형: 물들다 / 어간: 물들- / 어미: -었다</li>
      </ul>
    </div>

    <!-- 시험장 직전 핵심 공식 클리닉 카드 -->
    <div class="expl-card" style="border: 1.5px solid #000; background-color: #fcfcfc;">
      <div class="expl-header" style="background-color: #eee; margin: -7px -9px 6px -9px; padding: 5px 9px;">
        <span class="expl-qnum" style="font-size: 9.3pt;">[오답 극복! 시험장 3대 직관 판별 공식]</span>
        <span class="expl-badge">필수 암기</span>
      </div>
      <div style="font-size: 8.3pt; line-height: 1.5;">
        <strong>1. 직유 vs 은유 판별</strong><br>
        • <strong>'~처럼, ~같이, ~듯이'</strong>가 있으면? ➔ <strong>직유법</strong><br>
        • 연결어 없이 <strong>'A는 B이다'</strong> 형태면? ➔ <strong>은유법</strong><br><br>
        <strong>2. 시의 운율 판별 (반복의 원리)</strong><br>
        • '보슬보슬, 알롱알롱, 졸졸졸' ➔ <strong>음성 상징어 반복</strong><br>
        • '~자, ~ㄹ까' ➔ <strong>동일한 종결 어미 반복</strong><br><br>
        <strong>3. 용언의 어간 vs 어미 판별</strong><br>
        • <strong>'-고, -니, -어서'</strong>를 붙여 변형해 본다!<br>
        • 끝까지 형태가 <strong>안 바뀌는 앞부분 = 어간</strong> (푸르-, 읽-, 춤추-)<br>
        • 상황에 따라 <strong>모습이 바뀌는 뒷부분 = 어미</strong> (-다, -고, -는다, -ㄴ다)
      </div>
    </div>

  </div> <!-- end of two-column-layout (Part 2) -->

</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[1] HTML 템플릿 생성 완료: {html_path}")

    # Edge 브라우저 실행 파일 탐색
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_exe = None
    for p in edge_paths:
        if os.path.exists(p):
            edge_exe = p
            break

    if not edge_exe:
        print("[FAIL] Microsoft Edge 실행 파일을 찾을 수 없습니다.")
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
        if '빠른 정답 및 출제 분석표' in text or '정답 및 상세 해설집' in text:
            part2_start_page = i
            break

    print(f"  - 실전 문제지 (Part 1): 1페이지 ~ {part2_start_page}페이지 ({part2_start_page}면)")
    print(f"  - 정답 및 해설지 (Part 2): {part2_start_page + 1}페이지 ~ {total_pages}페이지 ({total_pages - part2_start_page}면)")

    p1_text = "\n".join([doc[i].get_text() for i in range(part2_start_page)])
    has_diff_in_p1 = bool(re.search(r'\[(상|중|하)\]', p1_text))
    print(f"  - 문제지 본문 난이도 비노출 검증: [상/중/하] 노출 여부 = {has_diff_in_p1} (PASS: False)")

    has_points = bool(re.search(r'\[\d+점\]', p1_text))
    print(f"  - 배점 표기 부재 검증: [X점] 표기 여부 = {has_points} (PASS: False)")

    p2_text = "\n".join([doc[i].get_text() for i in range(part2_start_page, len(doc))])
    has_sources = "출처: 미래엔" in p2_text
    print(f"  - 답지 출처 명시 검증: '출처: 미래엔' 수록 여부 = {has_sources} (PASS: True)")

    print("\n>>> 오답 클리닉 실전 모의평가 6제 빌드 완료! <<<")

if __name__ == '__main__':
    build_clinic_6제_v1()
