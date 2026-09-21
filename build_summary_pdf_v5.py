import os
import subprocess
import fitz

def generate_summary_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    summary_dir = os.path.join(base_dir, '요약')
    os.makedirs(summary_dir, exist_ok=True)

    html_path = os.path.join(summary_dir, '3단원_능동적인_언어생활_요약_v5.html')
    pdf_path = os.path.join(summary_dir, '3단원_능동적인_언어생활_요약_v5.pdf')

    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[교과서 핵심 요약] 3. 능동적인 언어생활 (미래엔 국어 1-1) [v5]</title>
<style>
  @page {
    size: A4 portrait;
    margin: 7.2mm 9.5mm 7.2mm 9.5mm;
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
    line-height: 1.60;
    letter-spacing: 0.15px;
    font-size: 8.85pt;
    margin: 0;
    padding: 0;
    background: #fff;
  }

  /* 1단 전폭 표제부 */
  .header-box {
    border: 1.8px solid #000;
    padding: 4.5px 10px;
    margin-bottom: 4.5px;
    background-color: #fff;
  }
  .header-title {
    font-size: 13.5pt;
    font-weight: bold;
    text-align: center;
    margin: 0 0 2.5px 0;
    letter-spacing: 0.2px;
  }
  .header-info-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.1pt;
    margin-top: 2px;
    letter-spacing: 0.1px;
  }
  .header-info-table td {
    border: 1px solid #444;
    padding: 2px 5px;
    text-align: center;
    background-color: #f7f7f7;
    line-height: 1.45;
  }
  .header-info-table td.label {
    font-weight: bold;
    background-color: #eaeaea;
    width: 13%;
  }

  /* 2단 분할 레이아웃 (1페이지 본문) */
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
    padding: 4.5px 8px;
    margin-bottom: 4.5px;
    font-size: 8.35pt;
    line-height: 1.54;
    letter-spacing: 0.1px;
  }

  /* 섹션 제목 (대주제) */
  .section-title {
    background-color: #000;
    color: #fff;
    font-size: 9.3pt;
    font-weight: bold;
    padding: 2px 6px;
    margin: 4.5px 0 3.5px 0;
    border-radius: 2px;
    break-after: avoid;
    letter-spacing: 0.1px;
    line-height: 1.40;
  }

  /* 중제목 */
  .sub-title {
    font-size: 8.9pt;
    font-weight: bold;
    border-left: 3px solid #000;
    padding-left: 5px;
    margin: 4px 0 2px 0;
    break-after: avoid;
    letter-spacing: 0.1px;
    line-height: 1.42;
  }

  /* 개념 카드 박스 */
  .card-box {
    border: 1px solid #444;
    background-color: #fafafa;
    padding: 3.5px 6px;
    margin-bottom: 3.5px;
    font-size: 8.25pt;
    line-height: 1.54;
    letter-spacing: 0.12px;
    break-inside: avoid;
  }

  /* 예시 및 탐구 박스 */
  .example-box {
    border: 1px dashed #555;
    background-color: #fff;
    padding: 3.5px 6px;
    margin-bottom: 3.5px;
    font-size: 8.15pt;
    line-height: 1.52;
    letter-spacing: 0.12px;
    break-inside: avoid;
  }

  /* 배지 스타일 */
  .badge-frequent {
    display: inline-block;
    background-color: #000;
    color: #fff;
    font-size: 7.5pt;
    font-weight: bold;
    padding: 1px 4px;
    border-radius: 2px;
    margin-right: 2px;
    vertical-align: middle;
    letter-spacing: 0px;
  }
  .badge-trap {
    display: inline-block;
    border: 1.3px solid #000;
    background-color: #fff;
    color: #000;
    font-size: 7.5pt;
    font-weight: bold;
    padding: 0.5px 3.5px;
    border-radius: 2px;
    margin-right: 2px;
    vertical-align: middle;
    letter-spacing: 0px;
  }
  .badge-ex {
    display: inline-block;
    background-color: #f0f0f0;
    border: 0.9px solid #333;
    color: #000;
    font-weight: bold;
    font-size: 8.1pt;
    padding: 0.5px 3.5px;
    border-radius: 2px;
    margin: 0.5px 1px;
    line-height: 1.25;
    letter-spacing: 0.05px;
  }

  .emp {
    font-weight: bold;
    text-decoration: underline;
  }

  /* 강제 페이지 분할 */
  .page-break {
    page-break-after: always;
    break-after: page;
  }

  /* ================================================================= */
  /* 2페이지 전용 시각화 인포그래픽 스타일 (1단 전폭 시원한 조판) */
  /* ================================================================= */
  .page-2-container {
    width: 100%;
  }

  .concept-bar {
    border: 1.2px solid #333;
    background-color: #f7f7f7;
    padding: 3px 6px;
    margin-bottom: 4px;
    font-size: 8.15pt;
    line-height: 1.44;
    letter-spacing: 0.1px;
  }

  /* [인포그래픽 1] 한 문장 9품사 상호작용 카드 */
  .sentence-container {
    border: 1.5px solid #000;
    background-color: #fff;
    padding: 3.5px 6px;
    margin-bottom: 4.5px;
  }
  .sentence-title {
    font-size: 8.4pt;
    font-weight: bold;
    background-color: #eee;
    border-bottom: 1px solid #444;
    padding: 1.5px 5px;
    margin-bottom: 3px;
    letter-spacing: 0.1px;
  }
  .sentence-table {
    width: 100%;
    border-collapse: collapse;
    text-align: center;
  }
  .sentence-table td {
    padding: 2px 1.5px;
    vertical-align: top;
    font-size: 7.7pt;
    line-height: 1.30;
    letter-spacing: 0.05px;
    border: 1px solid #ddd;
    background-color: #fafafa;
  }
  .token-word {
    font-size: 9.2pt;
    font-weight: bold;
    color: #000;
    margin-bottom: 1.5px;
    display: block;
    letter-spacing: 0.1px;
  }
  .token-pos {
    display: inline-block;
    background-color: #222;
    color: #fff;
    font-size: 7.2pt;
    font-weight: bold;
    padding: 0.5px 3px;
    border-radius: 2px;
    margin-bottom: 1.5px;
    letter-spacing: 0px;
  }
  .token-func {
    font-size: 7.0pt;
    color: #444;
    line-height: 1.24;
    letter-spacing: 0.05px;
  }

  /* 블록 대분류 헤더 */
  .block-header-black {
    background-color: #000;
    color: #fff;
    font-size: 8.8pt;
    font-weight: bold;
    padding: 2px 6px;
    letter-spacing: 0.1px;
  }
  .block-header-gray {
    background-color: #333;
    color: #fff;
    font-size: 8.8pt;
    font-weight: bold;
    padding: 2px 6px;
    letter-spacing: 0.1px;
  }

  /* 2x2 기능군 카드 테이블 */
  .func-grid-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 4px;
  }
  .func-grid-table td {
    width: 50%;
    border: 1px solid #444;
    padding: 3.5px 5.5px;
    vertical-align: top;
    background-color: #fff;
    font-size: 8.15pt;
    line-height: 1.48;
    letter-spacing: 0.1px;
  }
  .pos-card-title {
    font-weight: bold;
    font-size: 8.5pt;
    background-color: #eaeaea;
    border-left: 3px solid #000;
    padding: 1px 4.5px;
    margin-bottom: 2.5px;
    letter-spacing: 0.1px;
  }

  .trap-note {
    border-left: 2px solid #000;
    background-color: #f5f5f5;
    padding: 1.5px 4.5px;
    font-size: 7.75pt;
    margin-top: 2.5px;
    line-height: 1.38;
    letter-spacing: 0.08px;
  }

  /* 순서도 판별 저울 다이어그램 */
  .flow-container {
    border: 1.4px solid #000;
    background-color: #fafafa;
    padding: 3.5px 6px;
    margin-bottom: 4px;
  }
  .flow-title {
    font-weight: bold;
    font-size: 8.6pt;
    border-bottom: 1px solid #888;
    padding-bottom: 1.5px;
    margin-bottom: 2.5px;
    letter-spacing: 0.1px;
  }
  .flow-table {
    width: 100%;
    border-collapse: collapse;
  }
  .flow-table td {
    vertical-align: middle;
    padding: 1px;
    border: none;
  }
  .flow-step-box {
    border: 1.2px solid #222;
    background-color: #fff;
    padding: 3px 5px;
    font-size: 7.85pt;
    line-height: 1.44;
    letter-spacing: 0.08px;
    border-radius: 2px;
  }
  .flow-arrow-cell {
    text-align: center;
    font-weight: bold;
    font-size: 8.5pt;
    color: #333;
    width: 28px;
    line-height: 1.3;
  }

  /* 3대 함정 3열 테이블 */
  .trap-3col-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 4px;
  }
  .trap-3col-table th {
    border: 1px solid #000;
    background-color: #222;
    color: #fff;
    padding: 2px 4px;
    font-size: 8.0pt;
    text-align: center;
    letter-spacing: 0.1px;
  }
  .trap-3col-table td {
    border: 1px solid #444;
    background-color: #fcfcfc;
    padding: 3px 4.5px;
    vertical-align: top;
    font-size: 7.75pt;
    line-height: 1.46;
    letter-spacing: 0.08px;
    width: 33.33%;
  }

  /* 담화 효과 2열 테이블 */
  .effect-2col-table {
    width: 100%;
    border-collapse: collapse;
  }
  .effect-2col-table th {
    border: 1px solid #000;
    background-color: #eaeaea;
    padding: 1.5px 5px;
    font-size: 8.0pt;
    text-align: center;
    font-weight: bold;
    letter-spacing: 0.1px;
  }
  .effect-2col-table td {
    border: 1px solid #555;
    background-color: #fff;
    padding: 2.5px 5px;
    vertical-align: top;
    font-size: 7.75pt;
    line-height: 1.44;
    letter-spacing: 0.08px;
    width: 50%;
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
          <td>GEMINI.md 준수 ([빈출]/[함정] 엄선, 100% 흑백 인쇄, v5)</td>
        </tr>
      </table>
    </div>

    <!-- 대단원 개관 박스 (1단 전폭) -->
    <div class="intro-box">
      <b>【단원 개관 및 성취 기준】</b> 다양한 담화 상황에서 화자의 숨겨진 의도와 관점, 가치관을 능동적으로 파악하는 <b>[듣기·말하기 능력]</b>과 우리말 단어의 갈래인 '품사'의 3대 분류 기준과 9품사의 문법적 특성을 깊이 이해하여 일상 언어생활 자료를 비판적·체계적으로 분석하는 <b>[문법 탐구 능력]</b>을 기른다.
      <div style="margin-top: 2px; font-size: 8.0pt; color: #333; line-height: 1.45;">
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
  <!-- PAGE 2: 소단원 (2) 품사의 종류와 특성 (인포그래픽 시각화 마스터) -->
  <!-- ================================================================= -->
  <div class="page-2-container">

    <div class="section-title" style="margin-top:0;">제2부. 소단원 (2) 품사의 종류와 특성 (인포그래픽 시각화 마스터)</div>

    <!-- 1. 단어와 품사의 개념 바 -->
    <div class="concept-bar">
      <b>【기본 개념】</b>
      • <b>단어(單語)</b>: 홀로 쓰일 수 있는 말(자립 형태소) 또는 앞말에 붙어 쉽게 분리될 수 있는 말(조사).
      &nbsp;|&nbsp;
      • <b>품사(品詞)</b>: 공통된 문법적 성질(형태, 기능, 의미)을 가진 단어들의 갈래.
    </div>

    <!-- 2. [인포그래픽 1] 한 문장으로 끝내는 9품사 상호작용 카드 -->
    <div class="sentence-container">
      <div class="sentence-title">
        <span class="badge-frequent">[빈출]</span> <b>한 문장 9품사 상호작용 지도</b> — <i>"앗! 새 옷을 입은 그가 참 빨리 달린다."</i>
      </div>
      <table class="sentence-table">
        <tr>
          <td style="width: 11%;">
            <span class="token-word">앗!</span>
            <span class="token-pos">감탄사</span><br>
            <span class="token-func"><b>[독립언]</b><br>혼자 느낌 표출</span>
          </td>
          <td style="width: 14%;">
            <span class="token-word">새</span>
            <span class="token-pos">관형사</span><br>
            <span class="token-func"><b>[수식언]</b><br>체언(옷) 수식 ➔</span>
          </td>
          <td style="width: 15%;">
            <span class="token-word">옷 을</span>
            <span class="token-pos">명사+조사</span><br>
            <span class="token-func"><b>[체언+관계언]</b><br>사물명 + 목적격</span>
          </td>
          <td style="width: 15%;">
            <span class="token-word">그 가</span>
            <span class="token-pos">대명사+조사</span><br>
            <span class="token-func"><b>[체언+관계언]</b><br>대신지칭 + 주격</span>
          </td>
          <td style="width: 14%;">
            <span class="token-word">참</span>
            <span class="token-pos">부사</span><br>
            <span class="token-func"><b>[수식언]</b><br>부사(빨리) 수식 ➔</span>
          </td>
          <td style="width: 15%;">
            <span class="token-word">빨리</span>
            <span class="token-pos">부사</span><br>
            <span class="token-func"><b>[수식언]</b><br>동사(달린다) 수식 ➔</span>
          </td>
          <td style="width: 16%;">
            <span class="token-word">달린다</span>
            <span class="token-pos">동사</span><br>
            <span class="token-func"><b>[용언]</b><br>주어의 동작 서술</span>
          </td>
        </tr>
      </table>
    </div>

    <!-- 3. 불변어 블록 (형태 1) -->
    <div class="block-header-black">
      ■ 1. 형태(形態) 기준 ➔ 【 불 변 어 】 (문장에서 쓰일 때 형태가 변하지 않는 단어)
    </div>
    <table class="func-grid-table">
      <tr>
        <td>
          <div class="pos-card-title">① 체 언 (문장의 몸체 구실: 주어·목적어·보어)</div>
          • <b>명사 (이름)</b>: <span class="badge-ex">나무</span> <span class="badge-ex">바다</span> <span class="badge-ex">평화</span> <span class="badge-ex">사랑</span><br>
          • <b>대명사 (대신)</b>: <span class="badge-ex">나</span> <span class="badge-ex">너</span> <span class="badge-ex">우리</span> <span class="badge-ex">이것</span> <span class="badge-ex">저기</span><br>
          • <b>수사 (수량·순서)</b>: <span class="badge-ex">하나</span> <span class="badge-ex">둘</span> <span class="badge-ex">셋</span> <span class="badge-ex">첫째</span> <span class="badge-ex">둘째</span>
        </td>
        <td>
          <div class="pos-card-title">② 수 식 언 (다른 말을 꾸며 주는 구실)</div>
          • <b>관형사</b>: 오직 <u>체언만 수식</u> / 형태 불변 / <u>조사 결합 불가</u><br>
          &nbsp;&nbsp;➔ <span class="badge-ex">새</span> <span class="badge-ex">헌</span> <span class="badge-ex">옛</span> <span class="badge-ex">모든</span> <span class="badge-ex">이</span> <span class="badge-ex">그</span> <span class="badge-ex">저</span><br>
          • <b>부사</b>: 주로 <u>용언(동사·형용사) 수식</u> / 문장 전체 수식<br>
          &nbsp;&nbsp;➔ <span class="badge-ex">참</span> <span class="badge-ex">너무</span> <span class="badge-ex">아주</span> <span class="badge-ex">반드시</span> <span class="badge-ex">과연</span>
        </td>
      </tr>
      <tr>
        <td>
          <div class="pos-card-title">③ 관 계 언 (문법적 관계 표시 및 특별한 뜻)</div>
          • <b>조사</b>: 주로 체언 뒤 결합 / 자립성 없어 <u>앞말에 붙여 씀</u><br>
          &nbsp;&nbsp;➔ <span class="badge-ex">이/가</span> <span class="badge-ex">을/를</span> <span class="badge-ex">은/는</span> <span class="badge-ex">도</span> <span class="badge-ex">만</span> <span class="badge-ex">부터</span><br>
          <div class="trap-note">
            ※ <b><span class="badge-trap">[함정]</span></b> 서술격 조사 <b>'이다'</b>는 기능상 조사(관계언)이나, 용언처럼 형태가 변하므로(이다, 이고, 이니) <u>형태상 가변어</u>에 속함!
          </div>
        </td>
        <td>
          <div class="pos-card-title">④ 독 립 언 (다른 성분과 직접 관계없이 독립적)</div>
          • <b>감탄사</b>: 말하는 이의 놀람, 느낌, 부름, 대답<br>
          &nbsp;&nbsp;➔ <span class="badge-ex">앗!</span> <span class="badge-ex">으악!</span> <span class="badge-ex">어머나!</span> <span class="badge-ex">야!</span> <span class="badge-ex">네</span> <span class="badge-ex">아니요</span><br>
          <div class="trap-note">
            • <b>특징</b>: 문장에서 생략해도 문장의 기본 골격과 의미 성립에 영향 없음.
          </div>
        </td>
      </tr>
    </table>

    <!-- 4. 가변어 블록 (형태 2) -->
    <div class="block-header-gray">
      ■ 2. 형태(形態) 기준 ➔ 【 가 변 어 】 (문장에서 쓰일 때 형태가 변하는 단어 / 활용)
    </div>
    <div style="border: 1px solid #444; background-color: #fff; padding: 3px 6px; margin-bottom: 4px;">
      <table style="width: 100%; border-collapse: collapse; margin-bottom: 2px;">
        <tr>
          <td style="width: 50%; vertical-align: top; padding-right: 5px;">
            <div class="pos-card-title">⑤ 용 언 ─ 동 사 (움직임·동작·작용)</div>
            • 대상의 움직임이나 작용을 서술함.<br>
            ➔ <span class="badge-ex">가다</span> <span class="badge-ex">먹다</span> <span class="badge-ex">뛰다</span> <span class="badge-ex">읽다</span> <span class="badge-ex">나오다</span>
          </td>
          <td style="width: 50%; vertical-align: top; padding-left: 5px;">
            <div class="pos-card-title">⑤ 용 언 ─ 형용사 (상태·성질)</div>
            • 대상의 상태나 성질을 서술함.<br>
            ➔ <span class="badge-ex">예쁘다</span> <span class="badge-ex">푸르다</span> <span class="badge-ex">맵다</span> <span class="badge-ex">착하다</span> <span class="badge-ex">알맞다</span>
          </td>
        </tr>
      </table>
      <div style="border-top: 1px dashed #777; padding-top: 1.5px; font-size: 7.75pt; line-height: 1.40; color: #222; letter-spacing: 0.08px;">
        • <b>용언의 활용(活用)</b>: <u>어간</u>(활용 시 형태가 변하지 않는 줄기, 예: '먹-') + <u>어미</u>(활용 시 형태가 변하는 꼬리, 예: '-고', '-어', '-으니') / <u>기본형</u>: 어간 + '-다'
      </div>
    </div>

    <!-- 5. [인포그래픽 3] 동사 vs 형용사 초고속 판별 저울 (순서도) -->
    <div class="flow-container">
      <div class="flow-title">
        <span class="badge-trap">[함정]</span> <b>동사 vs 형용사 초고속 1초 판별 저울 (알고리즘 순서도)</b>
      </div>
      <table class="flow-table">
        <tr>
          <td style="width: 47%;">
            <div class="flow-step-box">
              <b>【1단계: '-ㄴ다/-는다' 결합 저울】</b><br>
              용언 어간에 현재 시제 <b>'-ㄴ-/-는-'</b> 결합<br>
              • 저울 통과 <b>(YES)</b> ➔ <b>【 동  사 】</b> (먹는다 O, 달린다 O)<br>
              • 저울 탈락 <b>( NO )</b> ➔ <b>【 형용사 】</b> (푸른다 X, 예쁜다 X)
            </div>
          </td>
          <td class="flow-arrow-cell">
            ➔<br>검증<br>➔
          </td>
          <td style="width: 47%;">
            <div class="flow-step-box">
              <b>【2단계: 명령·청유형 결합 검증】</b><br>
              명령 <b>'-아라/-어라'</b>, 청유 <b>'-자'</b> 결합<br>
              • 결합 가능 <b>(YES)</b> ➔ <b>【 동  사 】</b> (먹어라 O, 같이 먹자 O)<br>
              • 결합 불가 <b>( NO )</b> ➔ <b>【 형용사 】</b> (푸르러라 X, 예쁘자 X)
            </div>
          </td>
        </tr>
      </table>
    </div>

    <!-- 6. [인포그래픽 4] 실전 단골 3대 문법 함정 정복 클리닉 -->
    <table class="trap-3col-table">
      <tr>
        <th><span class="badge-trap">[함정 1]</span> 수사 vs 수 관형사</th>
        <th><span class="badge-trap">[함정 2]</span> 관형사 뒤 조사 결합 오류</th>
        <th><span class="badge-trap">[함정 3]</span> 형용사 청유·명령형 오류</th>
      </tr>
      <tr>
        <td>
          • 뒤에 <b>조사가 결합할 수 있으면</b> ➔ <b>[수사]</b><br>
          &nbsp;&nbsp;"사과 <b>둘을</b> 먹었다." (조사 '을' 결합)<br>
          • 체언 수식, <b>조사가 결코 못 붙으면</b> ➔ <b>[관형사]</b><br>
          &nbsp;&nbsp;"사과 <b>두</b> 개를 먹었다." (명사 '개' 수식)
        </td>
        <td>
          • 관형사는 체언만 꾸미며 <b>조사 결합 절대 불가</b><br>
          • (X) "<b>옛부터</b> 전해 내려온 이야기"<br>
          • (O) "<b>옛날부터</b> 전해 내려온 이야기"<br>
          &nbsp;&nbsp;(관형사 '옛' ➔ 명사 '옛날' 교체 후 조사 결합)
        </td>
        <td>
          • 형용사는 상태이므로 <b>청유('-자')·명령 불가</b><br>
          • (X) "항상 마음이 <b>예쁘자</b> / <b>착해라</b>."<br>
          • (O) "마음을 <b>예쁘게 가꾸자</b>."<br>
          • (O) "마음이 <b>착해지자</b>." (동사화)
        </td>
      </tr>
    </table>

    <!-- 7. [인포그래픽 5] 담화 성격별 품사 활용 효과 -->
    <table class="effect-2col-table">
      <tr>
        <th><span class="badge-frequent">[빈출]</span> 그림책 《달 샤베트》(백희나) — 문학·감각적 담화</th>
        <th><span class="badge-frequent">[빈출]</span> 재난 안전 문자 — 실용·정보 전달 담화</th>
      </tr>
      <tr>
        <td>
          • <b>주요 품사</b>: 의성어·의태어 <b>부사</b> 다채롭게 활용 (<span class="badge-ex">아주아주</span> <span class="badge-ex">너무너무</span> <span class="badge-ex">꼭꼭</span> <span class="badge-ex">쌩쌩</span> <span class="badge-ex">똑똑</span>)<br>
          • <b>표현 효과</b>: 장면의 소리와 움직임을 <u>생동감 있고 감각적으로 묘사</u>하여 독자의 상상력과 흥미를 극대화함.
        </td>
        <td>
          • <b>주요 품사</b>: 수식언(관형사·부사) 최대한 배제, <b>명사 위주</b> 간결한 서술 (폭염 경보, 야외 활동 자제, 충분한 수분 섭취)<br>
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
