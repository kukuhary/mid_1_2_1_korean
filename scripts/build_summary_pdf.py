import os
import subprocess
import fitz

def generate_summary_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(base_dir) == 'scripts':

        base_dir = os.path.dirname(base_dir)
    summary_dir = os.path.join(base_dir, '요약')
    os.makedirs(summary_dir, exist_ok=True)

    html_path = os.path.join(summary_dir, '3단원_능동적인_언어생활_요약.html')
    pdf_path = os.path.join(summary_dir, '3단원_능동적인_언어생활_요약.pdf')

    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[교과서 핵심 요약] 3. 능동적인 언어생활 (미래엔 국어 1-1)</title>
<style>
  @page {
    size: A4 portrait;
    margin: 10mm 10mm 10mm 10mm;
    @bottom-center {
      content: "- " counter(page) " -";
      font-size: 8.5pt;
      font-family: 'Malgun Gothic', sans-serif;
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
    line-height: 1.56;
    font-size: 9.1pt;
    margin: 0;
    padding: 0;
    background: #fff;
  }

  /* 1단 전폭 표제부 */
  .header-box {
    border: 1.8px solid #000;
    padding: 6px 10px;
    margin-bottom: 7px;
    background-color: #fff;
  }
  .header-title {
    font-size: 14pt;
    font-weight: bold;
    text-align: center;
    margin: 0 0 4px 0;
    letter-spacing: -0.5px;
  }
  .header-info-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.2pt;
    margin-top: 3px;
  }
  .header-info-table td {
    border: 1px solid #444;
    padding: 2.5px 5px;
    text-align: center;
    background-color: #f7f7f7;
  }
  .header-info-table td.label {
    font-weight: bold;
    background-color: #eaeaea;
    width: 13%;
  }

  /* 2단 분할 레이아웃 */
  .two-column-layout {
    column-count: 2;
    column-gap: 6.5mm;
    column-rule: 0.8px solid #777;
    text-align: justify;
  }

  /* 대단원 개관 1단 박스 */
  .intro-box {
    border: 1.2px solid #333;
    background-color: #f9f9f9;
    padding: 5px 8px;
    margin-bottom: 7px;
    font-size: 8.6pt;
    line-height: 1.5;
  }

  /* 섹션 제목 (대주제) */
  .section-title {
    background-color: #000;
    color: #fff;
    font-size: 9.7pt;
    font-weight: bold;
    padding: 3px 6px;
    margin: 7px 0 5px 0;
    border-radius: 2px;
    break-after: avoid;
    letter-spacing: -0.3px;
  }

  /* 중제목 */
  .sub-title {
    font-size: 9.2pt;
    font-weight: bold;
    border-left: 3px solid #000;
    padding-left: 5px;
    margin: 6px 0 3px 0;
    break-after: avoid;
  }

  /* 소제목 */
  .sub-sub-title {
    font-size: 8.8pt;
    font-weight: bold;
    margin: 4px 0 2px 0;
    color: #222;
    break-after: avoid;
  }

  /* 개념 카드 박스 */
  .card-box {
    border: 1px solid #444;
    background-color: #fafafa;
    padding: 4.5px 6.5px;
    margin-bottom: 5px;
    font-size: 8.5pt;
    line-height: 1.5;
    break-inside: avoid;
  }

  /* 시험 빈출 함정 박스 */
  .trap-box {
    border: 1.4px solid #000;
    background-color: #f4f4f4;
    padding: 4.5px 6.5px;
    margin-bottom: 5px;
    font-size: 8.4pt;
    line-height: 1.5;
    break-inside: avoid;
  }
  .trap-title {
    font-weight: bold;
    font-size: 8.8pt;
    border-bottom: 1px solid #888;
    padding-bottom: 2px;
    margin-bottom: 3px;
  }

  /* 예시 및 탐구 박스 */
  .example-box {
    border: 1px dashed #555;
    background-color: #fff;
    padding: 4.5px 6px;
    margin-bottom: 5px;
    font-size: 8.4pt;
    line-height: 1.48;
    break-inside: avoid;
  }

  /* 표 스타일 */
  .summary-table {
    width: 100%;
    border-collapse: collapse;
    margin: 4px 0 5px 0;
    font-size: 8.0pt;
    line-height: 1.38;
    break-inside: avoid;
  }
  .summary-table th {
    border: 1px solid #333;
    background-color: #eaeaea;
    padding: 3px 3px;
    font-weight: bold;
    text-align: center;
  }
  .summary-table td {
    border: 1px solid #555;
    padding: 3px 3px;
    vertical-align: middle;
  }
  .summary-table td.center {
    text-align: center;
  }

  /* 리스트 */
  ul, ol {
    margin: 2px 0 3px 0;
    padding-left: 15px;
  }
  li {
    margin-bottom: 1.5px;
  }

  .emp {
    font-weight: bold;
    text-decoration: underline;
  }
  .badge-frequent {
    display: inline-block;
    background-color: #000;
    color: #fff;
    font-size: 7.2pt;
    font-weight: bold;
    padding: 0.5px 3.5px;
    border: 1px solid #000;
    border-radius: 2px;
    margin-right: 3px;
    vertical-align: 1px;
    letter-spacing: -0.3px;
  }
  .badge-trap {
    display: inline-block;
    background-color: #fff;
    color: #000;
    border: 1.4px solid #000;
    font-size: 7.2pt;
    font-weight: bold;
    padding: 0px 3px;
    border-radius: 2px;
    margin-right: 3px;
    vertical-align: 1px;
    letter-spacing: -0.3px;
  }

  /* 페이지 분할 */
  .page-break {
    page-break-after: always;
    break-after: page;
  }

  /* ================================================================= */
  /* 페이지 2 전용 1단 전폭 다이어그램 스타일 */
  /* ================================================================= */
  .page-2-container {
    width: 100%;
  }

  /* 개념 한줄 요약 바 */
  .concept-bar {
    border: 1.2px solid #333;
    background-color: #f7f7f7;
    padding: 4px 8px;
    margin-bottom: 6px;
    font-size: 8.5pt;
    line-height: 1.45;
  }

  /* 품사 마스터 다이어그램 테이블 */
  .pos-master-diagram {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 6px;
    font-size: 8.0pt;
    line-height: 1.36;
  }
  .pos-master-diagram th, .pos-master-diagram td {
    border: 1px solid #333;
    padding: 3px 3.5px;
    vertical-align: top;
  }
  .th-immutable {
    background-color: #111;
    color: #fff;
    font-size: 9.0pt;
    font-weight: bold;
    text-align: center;
    padding: 3px;
  }
  .th-mutable {
    background-color: #333;
    color: #fff;
    font-size: 9.0pt;
    font-weight: bold;
    text-align: center;
    padding: 3px;
  }
  .th-func {
    background-color: #dedede;
    color: #000;
    font-size: 8.3pt;
    font-weight: bold;
    text-align: center;
  }
  .th-func-m {
    background-color: #cccccc;
    color: #000;
    font-size: 8.3pt;
    font-weight: bold;
    text-align: center;
  }
  .th-pos {
    background-color: #f0f0f0;
    color: #000;
    font-size: 8.3pt;
    font-weight: bold;
    text-align: center;
    border-bottom: 1.6px solid #000 !important;
  }
  .td-pos-body {
    font-size: 7.7pt;
    line-height: 1.33;
    background-color: #fff;
  }

  /* 알고리즘 순서도 다이어그램 */
  .flowchart-container {
    border: 1.4px solid #000;
    background-color: #fafafa;
    padding: 5px 8px;
    margin-bottom: 6px;
    font-size: 8.2pt;
  }
  .flow-title {
    font-weight: bold;
    font-size: 8.8pt;
    border-bottom: 1px solid #888;
    padding-bottom: 2px;
    margin-bottom: 4px;
  }
  .flow-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 2px;
  }
  .flow-table td {
    padding: 2.5px 4px;
    vertical-align: middle;
    font-size: 8.0pt;
    border: none;
  }
  .flow-badge-step {
    display: inline-block;
    background-color: #eee;
    border: 1px solid #333;
    font-weight: bold;
    padding: 1px 5px;
    border-radius: 2px;
    font-size: 7.8pt;
  }

  /* 3대 함정 3분할 테이블 */
  .trap-3col-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 6px;
  }
  .trap-3col-table th {
    border: 1px solid #000;
    background-color: #222;
    color: #fff;
    padding: 2.5px 4px;
    font-size: 8.2pt;
    text-align: center;
  }
  .trap-3col-table td {
    border: 1px solid #444;
    background-color: #fcfcfc;
    padding: 4px 5px;
    vertical-align: top;
    font-size: 7.9pt;
    line-height: 1.42;
  }

  /* 텍스트 효과 2분할 테이블 */
  .effect-2col-table {
    width: 100%;
    border-collapse: collapse;
  }
  .effect-2col-table th {
    border: 1px solid #000;
    background-color: #eaeaea;
    padding: 2.5px 5px;
    font-size: 8.2pt;
    text-align: center;
    font-weight: bold;
  }
  .effect-2col-table td {
    border: 1px solid #555;
    background-color: #fff;
    padding: 3.5px 6px;
    vertical-align: top;
    font-size: 7.9pt;
    line-height: 1.42;
  }
</style>
</head>
<body>

  <!-- ================================================================= -->
  <!-- PAGE 1: 표제부 + 소단원 (1) 추론하며 듣기 + 대단원 연계 활동 -->
  <!-- ================================================================= -->
  <div class="page-1-container">

    <!-- 상단 표제부 (1단 전폭) -->
    <div class="header-box">
      <div class="header-title">[2026 중간고사 대비] 교과서 핵심 요약집 — 3. 능동적인 언어생활</div>
      <table class="header-info-table">
        <tr>
          <td class="label">과목 / 학년</td>
          <td>중학 국어 1학년</td>
          <td class="label">교과서 출처</td>
          <td>2022 개정 미래엔(신유식) 국어 1-1 대단원 3</td>
          <td class="label">단원 구성</td>
          <td>⑴ 추론하며 듣기 / ⑵ 품사의 종류와 특성</td>
        </tr>
        <tr>
          <td class="label">해당 시험</td>
          <td>2026학년도 2학기 중간고사</td>
          <td class="label">핵심 영역</td>
          <td>듣기·말하기 & 문법 (통합 단원)</td>
          <td class="label">조판 규격</td>
          <td>요약.md 준수 ([빈출]/[함정] 엄선, 100% 흑백 인쇄)</td>
        </tr>
      </table>
    </div>

    <!-- 대단원 개관 박스 (1단 전폭) -->
    <div class="intro-box">
      <b>【단원 개관 및 성취 기준】</b> 다양한 담화 상황에서 화자의 숨겨진 의도와 관점, 가치관을 능동적으로 파악하는 <b>[듣기·말하기 능력]</b>과 우리말 단어의 갈래인 '품사'의 3대 분류 기준과 9품사의 문법적 특성을 깊이 이해하여 일상 언어생활 자료를 비판적·체계적으로 분석하는 <b>[문법 탐구 능력]</b>을 기른다.
      <div style="margin-top: 2px; font-size: 8.3pt; color: #333;">
        • 성취 기준 1: 화자의 의도와 관점, 가치관을 추론하며 들을 수 있다. (듣기·말하기)<br>
        • 성취 기준 2: 품사의 종류와 특성을 이해하고 다양한 국어 자료를 분석할 수 있다. (문법)
      </div>
    </div>

    <!-- 2단 본문 시작 (소단원 1 + 대단원 연계 활동) -->
    <div class="two-column-layout">

      <div class="section-title">제1부. 소단원 (1) 추론하며 듣기</div>

      <div class="sub-title">1. 추론하며 듣기의 핵심 개념</div>
      <div class="card-box">
        • <b>발화(發話)</b>: 머릿속 생각·감정을 음성 언어로 나타낸 것.<br>
        • <b>담화(談話)</b>: 발화가 모여 이루어진 의사소통의 통일된 덩어리(대화, 연설, 뉴스, 토의 등).<br>
        • <b>추론(推論)하며 듣기</b>: 겉으로 직접 드러나지 않은 화자의 <u>숨겨진 의도, 관점, 가치관, 목적</u>을 여러 단서를 종합하여 미루어 짐작하며 듣는 방법.
      </div>

      <div class="sub-title"><span class="badge-frequent">[빈출]</span> 2. 화자의 의도·관점 추론 시 고려할 3대 요소</div>
      <div class="card-box">
        <b>① 상황 맥락 (가장 기본적 단서)</b><br>
        담화가 이루어지는 <u>시간, 장소, 화자와 청자의 관계, 대화의 주제 및 목적</u>을 종합적으로 파악함.<br>
        <b>② 언어적 표현</b><br>
        화자가 사용한 구체적 단어, 어휘 선택, 문장 형식.<br>
        <b>③ 준언어적(반언어적) & 비언어적 표현</b><br>
        • <b>준언어적 표현</b>: 목소리 크기, 성량, 억양(높낮이), 말투(어조), 말의 빠르기 등.<br>
        • <b>비언어적 표현</b>: 표정, 시선(눈빛), 몸짓, 손짓, 자세 등.<br>
        ➔ <span class="emp">동일한 문장이라도 준·비언어적 표현에 따라 의도가 정반대가 됨!</span>
      </div>

      <div class="sub-title">3. 추론하며 듣기의 효과 및 가치</div>
      <div class="card-box">
        • 겉표면의 말에 얽매이지 않고 화자의 <u>참된 의도를 온전히 이해</u>할 수 있음.<br>
        • 화자의 관점과 가치관을 깊이 있게 파악하여 오해를 방지하고 성숙하고 원활한 의사소통을 유지함.
      </div>

      <div class="sub-title">4. 교과서 핵심 탐구 제재 및 분석</div>
      <div class="example-box">
        <b><span class="badge-trap">[함정]</span> [제재 1] "저희는 3시까지만 영업합니다."</b><br>
        • <b>라온이의 오해</b>: "3시까지 먹고 가면 된다"고 단순 해석.<br>
        • <b>다감이의 추론</b>: 현재 2시 40분. 조리(15분)와 식사(15분) 시간을 고려할 때 <u>"지금 주문과 식사가 어렵다"</u>는 완곡한 거절임을 올바르게 추론함.<br><br>

        <b><span class="badge-frequent">[빈출]</span> [제재 2] "네가 그린 거니?"의 상황별 의도 차이</b><br>
        • 멋진 그림 + 밝은 표정·감탄 말투 ➔ <u>칭찬과 놀람</u>.<br>
        • 낙서된 벽 + 굳은 표정·무거운 말투 ➔ <u>나무람과 추궁</u>.<br>
        ➔ 언어 표현이 같아도 맥락과 비언어적 표현에 따라 해석이 달라짐.<br><br>

        <b><span class="badge-trap">[함정]</span> [제재 3] "텔레비전 소리가 너무 크지 않니?"</b><br>
        • 형식은 의문문이지만, 실제 의도는 <u>"소리를 줄여라"</u>라는 완곡한 요청·지시.<br><br>

        <b>[제재 4] 뉴스 〈고궁 시각 장애인 영상 해설 도입〉</b><br>
        • 시각 장애인 영상 해설과 청각 장애인 수어 설명 도입.<br>
        • <b>기자의 관점·가치관</b>: 장애인의 문화 향유권을 배려하고 차별을 해소하려는 정책에 대한 <u>매우 긍정적인 관점</u>.<br><br>

        <b>[제재 5] 연설 〈더 크게 소리쳐!〉 (이시타 카트얄)</b><br>
        • 어른들에게 "커서 뭐가 될래?" 대신 <u>"지금 네가 원하는 것이 무엇인가?"</u>를 물어봐 달라고 요청.<br>
        • <b>화자의 가치관</b>: 미래만을 위해 현재를 유예·희생하지 말고, 청소년의 <u>현재 삶과 열정의 가치를 존중</u>해야 함.
      </div>

      <div class="section-title">제3부. 대단원 연계 활동 및 세상 읽기</div>
      <div class="card-box">
        • <b>창의 활동 〈라디오 뉴스 만들기〉</b>: 기획 의도와 관점을 명확히 세우고, 품사의 특성을 고려하여 객관적이고 정확한 어휘로 대본 작성.<br>
        • <b>세상을 움직인 연설가</b>:<br>
          - <b>김구</b>: '독립', '민족' 등 명사를 반복하여 광복의 의지 강조.<br>
          - <b>스티브 잡스</b>: '대단한', '놀랍다' 등 감정 호소 형용사 다수 활용.<br>
          - <b>말랄라</b>: '파괴되다', '막다' 등 동사와 '권리', '평화' 등 추상 명사 활용.<br>
          - <b>스파르시 샤</b>: '십오 년', '백삼십 번' 등 수사 활용으로 감동 극대화.
      </div>

    </div>
    <!-- 2단 본문 끝 -->

  </div>
  <!-- 1페이지 컨테이너 끝 -->

  <!-- 1페이지와 2페이지 강제 분할 -->
  <div class="page-break"></div>

  <!-- ================================================================= -->
  <!-- PAGE 2: 소단원 (2) 품사의 종류와 특성 (1단 전폭 다이어그램 위주) -->
  <!-- ================================================================= -->
  <div class="page-2-container">

    <div class="section-title" style="margin-top:0;">제2부. 소단원 (2) 품사의 종류와 특성 (1단 전폭 마스터)</div>

    <!-- 1. 단어와 품사의 개념 바 -->
    <div class="concept-bar">
      <b>【기본 개념】</b>
      • <b>단어(單語)</b>: 홀로 쓰일 수 있는 말(자립 형태소) 또는 앞말에 붙어 쉽게 분리될 수 있는 말(조사).
      &nbsp;|&nbsp;
      • <b>품사(品詞)</b>: 공통된 문법적 성질(형태, 기능, 의미)을 가진 단어들의 갈래.
    </div>

    <!-- 2. 9품사 3대 분류 체계 종합 마스터 다이어그램 -->
    <div style="margin-bottom: 2px;">
      <span class="badge-frequent">[빈출]</span> <b>품사의 3대 분류 기준 및 9품사 종합 계통 다이어그램</b>
    </div>
    <table class="pos-master-diagram">
      <tr>
        <th colspan="7" class="th-immutable">1. 형태(形態) 기준 ➔ 【 불 변 어 】 (문장에서 쓰일 때 형태가 변하지 않는 단어)</th>
        <th colspan="2" class="th-mutable">【 가 변 어 】 (형태가 변하는 단어 / 활용)</th>
      </tr>
      <tr>
        <th colspan="3" class="th-func">체 언 (몸체 역할)</th>
        <th colspan="2" class="th-func">수 식 언 (꾸며 주는 말)</th>
        <th class="th-func">관 계 언 (문법 관계)</th>
        <th class="th-func">독 립 언 (독립적)</th>
        <th colspan="2" class="th-func-m">용 언 (서술하는 말)</th>
      </tr>
      <tr>
        <th class="th-pos" style="width:11.1%;">명 사</th>
        <th class="th-pos" style="width:11.1%;">대명사</th>
        <th class="th-pos" style="width:11.1%;">수 사</th>
        <th class="th-pos" style="width:11.1%;">관형사</th>
        <th class="th-pos" style="width:11.1%;">부 사</th>
        <th class="th-pos" style="width:11.1%;">조 사</th>
        <th class="th-pos" style="width:11.1%;">감탄사</th>
        <th class="th-pos" style="width:11.2%;">동 사</th>
        <th class="th-pos" style="width:11.2%;">형용사</th>
      </tr>
      <tr>
        <td class="td-pos-body">
          <b>사물의 이름</b><br>
          • 구체: 나무, 바다<br>
          • 추상: 평화, 사랑
        </td>
        <td class="td-pos-body">
          <b>이름 대신 가리킴</b><br>
          • 인칭: 나, 너, 우리<br>
          • 지시: 이것, 저기
        </td>
        <td class="td-pos-body">
          <b>수량이나 순서</b><br>
          • 양: 하나, 둘, 셋<br>
          • 서: 첫째, 둘째
        </td>
        <td class="td-pos-body">
          <b>체언만을 수식</b><br>
          • 형태 불변<br>
          • 조사 결합 불가<br>
          (새, 헌, 옛, 모든)
        </td>
        <td class="td-pos-body">
          <b>주로 용언 수식</b><br>
          • 문장 전체 수식<br>
          (참, 너무, 아주, 반드시, 과연)
        </td>
        <td class="td-pos-body">
          <b>체언 뒤 결합</b><br>
          • 격조사: 이/가, 을/를<br>
          • 보조사: 은/는, 도<br>
          • 앞말에 붙여 씀
        </td>
        <td class="td-pos-body">
          <b>놀람, 느낌, 부름</b><br>
          • 다른 성분과 무관<br>
          (앗!, 어머나!, 야!, 네, 아니요)
        </td>
        <td class="td-pos-body">
          <b>움직임(동작)·작용</b><br>
          (가다, 먹다, 뛰다, 읽다, 달리다)
        </td>
        <td class="td-pos-body">
          <b>상태나 성질</b><br>
          (예쁘다, 푸르다, 맵다, 착하다, 빠르다)
        </td>
      </tr>
    </table>
    <div style="border: 1px dashed #444; background-color: #f7f7f7; padding: 3px 6px; font-size: 7.9pt; margin-bottom: 7px;">
      <b>※ <span class="badge-trap">[함정]</span> 서술격 조사 '이다'의 특이성</b>: '이다'는 기능상 <u>체언 뒤에 붙는 [관계언]</u>이지만, 용언처럼 형태가 변하므로(이다, 이고, 이니, 이면) 형태상 <u>[가변어]</u>에 속함! ➔ <i>"모든 조사는 불변어이다" 선택지는 오답!</i>
    </div>

    <!-- 3. 동사 vs 형용사 판별 알고리즘 순서도 -->
    <div class="flowchart-container">
      <div class="flow-title"><span class="badge-trap">[함정]</span> (최다 빈출+함정 중복) 동사와 형용사의 판별 알고리즘 (순서도 다이어그램)</div>
      <table class="flow-table">
        <tr>
          <td style="width:18%; text-align:center;">
            <div class="flow-badge-step">용언의 기본형 어간</div>
            <div style="font-size:7.5pt; color:#444; margin-top:2px;">(예: 먹-, 푸르-)</div>
          </td>
          <td style="width:5%; text-align:center; font-weight:bold;">➔</td>
          <td style="width:42%;">
            <b>[1단계 검증] 현재 시제 선어말 어미 결합</b><br>
            • 어간 + <b>`-ㄴ-/-는-`</b> 결합 시 자연스러움 (O) ➔ <span style="background-color:#000; color:#fff; font-weight:bold; padding:0 4px;">【 동 사 】</span> (예: 밥을 먹는다)<br>
            • 어간 + <b>`-ㄴ-/-는-`</b> 결합 시 어색함/불가 (X) ➔ <span style="border:1.2px solid #000; font-weight:bold; padding:0 4px;">【 형용사 】</span> (예: 하늘이 푸른다 X)
          </td>
          <td style="width:35%; border-left:1px dashed #888; padding-left:7px;">
            <b>[2단계 검증] 명령·청유 어미 결합</b><br>
            • 명령형(<b>`-아라/-어라`</b>), 청유형(<b>`-자`</b>) 가능 ➔ <b>[동사]</b><br>
            • 명령형, 청유형 결합 결코 불가 ➔ <b>[형용사]</b><br>
            <i>* 주의: "마음이 예쁘자(X)" ➔ 형용사에 청유형 불가!</i>
          </td>
        </tr>
      </table>
    </div>

    <!-- 4. 실전 시험 단골 3대 문법 함정 정복 -->
    <div style="margin-bottom: 2px;">
      <span class="badge-trap">[함정]</span> <b>실전 시험 단골 3대 문법 함정 정복 클리닉</b>
    </div>
    <table class="trap-3col-table">
      <tr>
        <th style="width:33.3%;">[함정 1] 수사 vs 수 관형사 구별</th>
        <th style="width:33.3%;">[함정 2] 관형사 뒤 조사 결합 불가 어법</th>
        <th style="width:33.4%;">[함정 3] 형용사 청유·명령형 오류 교정</th>
      </tr>
      <tr>
        <td>
          • 뒤에 <u>조사가 결합할 수 있으면</u> ➔ <b>수사</b><br>
            - "사과 <b>둘을</b> 먹었다." (수사 '둘' + 조사 '을')<br>
          • <u>명사를 수식하고 조사가 못 붙으면</u> ➔ <b>관형사</b><br>
            - "사과 <b>두</b> 개를 먹었다." (명사 '개' 꾸밈)
        </td>
        <td>
          • (X) "<u>옛부터</u> 전해 내려온 마을 전설"<br>
            ➔ '옛'은 관형사이므로 조사 '부터' 결합 불가!<br>
          • (O) "<u>옛날부터</u> 전해 내려온 마을 전설"<br>
            ➔ 명사 '옛날' 뒤에 보조사 '부터' 결합 정상
        </td>
        <td>
          • (X) "항상 마음이 <u>예쁘자</u>."<br>
            ➔ '예쁘다'는 상태를 나타내는 형용사이므로 청유형 어미 '-자'를 쓸 수 없음!<br>
          • (O) "마음을 <u>예쁘게 가꾸자</u>." / "<u>예뻐지자</u>."
        </td>
      </tr>
    </table>

    <!-- 5. 텍스트 성격과 품사의 활용 효과 -->
    <div style="margin-bottom: 2px;">
      <span class="badge-frequent">[빈출]</span> <b>담화 및 텍스트의 성격에 따른 품사의 전략적 활용 효과</b>
    </div>
    <table class="effect-2col-table">
      <tr>
        <th style="width:50%;">그림책 《달 샤베트》(백희나) — 문학·감각적 담화</th>
        <th style="width:50%;">재난 안전 문자 — 실용·정보 전달 담화</th>
      </tr>
      <tr>
        <td>
          • <b>주요 품사 활용</b>: 의성어·의태어 <b>부사</b> 다채롭게 활용<br>
            (<code>아주아주</code>, <code>너무너무</code>, <code>꼭꼭</code>, <code>쌩쌩</code>, <code>씽씽</code>, <code>똑똑</code>)<br>
          • <b>표현 효과</b>: 장면의 소리와 움직임을 <u>생동감 있고 감각적으로 묘사</u>하여 독자의 상상력과 흥미를 극대화함.
        </td>
        <td>
          • <b>주요 품사 활용</b>: 수식언(관형사·부사) 최대한 배제, <b>명사 위주</b> 간결한 서술<br>
            (폭염 경보, 야외 활동 자제, 충분한 수분 섭취)<br>
          • <b>표현 효과</b>: 긴급한 정보를 <u>신속·정확하고 객관적이며 신뢰성 있게</u> 청자에게 직관적으로 전달함.
        </td>
      </tr>
    </table>

  </div>
  <!-- 2페이지 컨테이너 끝 -->

</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[1] Saved Summary HTML: {html_path} ({os.path.getsize(html_path)} bytes)")

    # Chrome headless for PDF generation
    chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    if not os.path.exists(chrome_path):
        chrome_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

    cmd = [
        chrome_path,
        '--headless=new',
        '--disable-gpu',
        '--no-pdf-header-footer',
        f'--print-to-pdf={pdf_path}',
        html_path
    ]
    res = subprocess.run(cmd, capture_output=True)
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 1000:
        print(f"[2] PDF Generated: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
    else:
        print(f"[FAIL] Return code: {res.returncode}, Stderr: {res.stderr.decode('utf-8', errors='ignore')}")
        return

    # Verify with PyMuPDF
    doc = fitz.open(pdf_path)
    print(f"[3] Total Pages in Summary PDF: {len(doc)}")
    for i, page in enumerate(doc):
        text = page.get_text()
        print(f"  - Page {i+1}: {len(text)} characters extracted")

    print("\n>>> Summary PDF Build & Verification Complete! <<<")

if __name__ == '__main__':
    generate_summary_pdf()
