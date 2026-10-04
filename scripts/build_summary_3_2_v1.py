import os
import subprocess
import fitz

def generate_summary_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(base_dir) == 'scripts':

        base_dir = os.path.dirname(base_dir)
    summary_dir = os.path.join(base_dir, '요약')
    os.makedirs(summary_dir, exist_ok=True)

    html_path = os.path.join(summary_dir, '3-2단원_품사의_종류와_특성_요약_v1.html')
    pdf_path = os.path.join(summary_dir, '3-2단원_품사의_종류와_특성_요약_v1.pdf')

    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[교과서 핵심 요약] 3-(2) 품사의 종류와 특성 (미래엔 국어 1-1) [v1]</title>
<style>
  @page {
    size: A4 portrait;
    margin: 6.0mm 8.5mm 6.0mm 8.5mm;
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
    line-height: 1.70;
    letter-spacing: 0.14px;
    font-size: 8.85pt;
    margin: 0;
    padding: 0;
    background: #fff;
  }

  /* 1단 전폭 표제부 */
  .header-box {
    border: 1.8px solid #000;
    padding: 4px 10px;
    margin-bottom: 4px;
    background-color: #fff;
  }
  .header-title {
    font-size: 13.5pt;
    font-weight: bold;
    text-align: center;
    margin: 0 0 2px 0;
    letter-spacing: 0.2px;
  }
  .header-info-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.1pt;
    margin-top: 2px;
    letter-spacing: 0.12px;
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

  /* 단원 개관 1단 박스 */
  .intro-box {
    border: 1.2px solid #333;
    background-color: #f9f9f9;
    padding: 4px 8px;
    margin-bottom: 4px;
    font-size: 8.25pt;
    line-height: 1.64;
    letter-spacing: 0.12px;
  }

  /* 섹션 제목 (대주제) */
  .section-title {
    background-color: #000;
    color: #fff;
    font-size: 9.3pt;
    font-weight: bold;
    padding: 2.2px 6px;
    margin: 4px 0 3px 0;
    border-radius: 2px;
    break-after: avoid;
    letter-spacing: 0.12px;
    line-height: 1.42;
  }

  /* 중제목 */
  .sub-title {
    font-size: 8.85pt;
    font-weight: bold;
    border-left: 3px solid #000;
    padding-left: 5px;
    margin: 3.5px 0 2px 0;
    break-after: avoid;
    letter-spacing: 0.12px;
    line-height: 1.45;
  }

  /* 개념 카드 박스 */
  .card-box {
    border: 1px solid #444;
    background-color: #fafafa;
    padding: 3.5px 6px;
    margin-bottom: 3.5px;
    font-size: 8.25pt;
    line-height: 1.66;
    letter-spacing: 0.13px;
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
    line-height: 1.30;
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

  /* [인포그래픽 1] 한 문장 9품사 올인원 완전체 카드 */
  .sentence-container {
    border: 1.5px solid #000;
    background-color: #fff;
    padding: 3px 6px;
    margin-bottom: 4px;
  }
  .sentence-title {
    font-size: 8.4pt;
    font-weight: bold;
    background-color: #eee;
    border-bottom: 1px solid #444;
    padding: 1.5px 5px;
    margin-bottom: 3px;
    letter-spacing: 0.12px;
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
    line-height: 1.50;
    letter-spacing: 0.08px;
    border: 1px solid #ddd;
    background-color: #fafafa;
  }
  .token-word {
    font-size: 9.1pt;
    font-weight: bold;
    color: #000;
    margin-bottom: 1px;
    display: block;
    letter-spacing: 0.1px;
  }
  .token-pos {
    display: inline-block;
    background-color: #222;
    color: #fff;
    font-size: 7.1pt;
    font-weight: bold;
    padding: 0.5px 3px;
    border-radius: 2px;
    margin-bottom: 1px;
    letter-spacing: 0px;
  }
  .token-func {
    font-size: 6.9pt;
    color: #444;
    line-height: 1.40;
    letter-spacing: 0.05px;
  }

  /* 블록 대분류 헤더 */
  .block-header-black {
    background-color: #000;
    color: #fff;
    font-size: 8.7pt;
    font-weight: bold;
    padding: 2px 6px;
    letter-spacing: 0.12px;
  }
  .block-header-gray {
    background-color: #333;
    color: #fff;
    font-size: 8.7pt;
    font-weight: bold;
    padding: 2px 6px;
    letter-spacing: 0.12px;
  }

  /* 2x2 기능군 카드 테이블 */
  .func-grid-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 3.5px;
  }
  .func-grid-table td {
    width: 50%;
    border: 1px solid #444;
    padding: 3.5px 5.5px;
    vertical-align: top;
    background-color: #fff;
    font-size: 8.15pt;
    line-height: 1.64;
    letter-spacing: 0.13px;
  }
  .pos-card-title {
    font-weight: bold;
    font-size: 8.5pt;
    background-color: #eaeaea;
    border-left: 3px solid #000;
    padding: 1px 4.5px;
    margin-bottom: 2px;
    letter-spacing: 0.12px;
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
    letter-spacing: 0.12px;
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
    line-height: 1.60;
    letter-spacing: 0.12px;
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
    letter-spacing: 0.12px;
  }
  .trap-3col-table td {
    border: 1px solid #444;
    background-color: #fcfcfc;
    padding: 3px 4.5px;
    vertical-align: top;
    font-size: 7.75pt;
    line-height: 1.62;
    letter-spacing: 0.12px;
    width: 33.33%;
  }

  /* 담화 효과 2열 테이블 */
  .effect-2col-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 3.5px;
  }
  .effect-2col-table th {
    border: 1px solid #000;
    background-color: #eaeaea;
    padding: 1.5px 5px;
    font-size: 8.0pt;
    text-align: center;
    font-weight: bold;
    letter-spacing: 0.12px;
  }
  .effect-2col-table td {
    border: 1px solid #555;
    background-color: #fff;
    padding: 2.5px 5px;
    vertical-align: top;
    font-size: 7.75pt;
    line-height: 1.62;
    letter-spacing: 0.12px;
    width: 50%;
  }

  /* 체크리스트 테이블 */
  .check-table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 4px;
  }
  .check-table th {
    border: 1px solid #333;
    background-color: #e5e5e5;
    padding: 2px 4px;
    font-size: 7.9pt;
    text-align: center;
    font-weight: bold;
  }
  .check-table td {
    border: 1px solid #555;
    padding: 2px 5px;
    font-size: 7.75pt;
    line-height: 1.58;
    background-color: #fff;
  }

  /* 총정리 족집게 바 */
  .summary-bar {
    border: 1.3px solid #000;
    background-color: #f5f5f5;
    padding: 3px 6px;
    font-size: 7.9pt;
    line-height: 1.60;
    letter-spacing: 0.12px;
  }
</style>
</head>
<body>

  <!-- ================================================================= -->
  <!-- PAGE 1: 단원 개관 + 3대 분류 기준 + 9품사 올인원 문장 + 5대 기능군 계통도 -->
  <!-- ================================================================= -->
  <div class="page-1-container">

    <!-- 상단 표제부 (1단 전폭) -->
    <div class="header-box">
      <div class="header-title">[2026 중간고사 대비] 교과서 핵심 요약집 — 3-(2) 품사의 종류와 특성</div>
      <table class="header-info-table">
        <tr>
          <td class="label">교과서 출처</td>
          <td>2022 개정 중학교 국어 1-1 (미래엔 신유식)</td>
          <td class="label">단원명</td>
          <td>3. 능동적인 언어생활 - (2) 품사의 종류와 특성</td>
          <td class="label">판본 규격</td>
          <td>소단원 (2) 문법 단독 집중판 (100% 흑백 벡터 조판)</td>
        </tr>
      </table>
    </div>

    <!-- 단원 개관 및 핵심 성취 기준 -->
    <div class="intro-box">
      <b>[소단원 핵심 성취 기준 및 학습 목표]</b><br>
      • <b>성취 기준</b>: [문법] 품사의 종류와 특성을 이해하고 다양한 국어 자료를 분석할 수 있다.<br>
      • <b>학습 목표</b>: 단어를 문법적 성질에 따라 9품사로 분류하고, 각 품사의 문법적 기능과 담화 속 활용 효과를 체계적으로 이해한다.
    </div>

    <!-- 1. 단어와 품사의 기본 개념 및 3대 분류 기준 -->
    <div class="section-title">1. 단어와 품사의 개념 및 3대 분류 기준</div>
    <div class="card-box">
      • <b>단어(單語)</b>: 자립하여 홀로 쓰일 수 있는 말(자립 형태소). 단, 자립성은 없으나 체언 뒤에 붙어 <u>쉽게 분리될 수 있는 말(조사)</u>도 단어로 인정함.<br>
      • <b>품사(品詞)</b>: 단어를 공통된 문법적 성질에 따라 갈래지어 묶은 것.<br>
      • <b>품사 분류의 3대 기준</b>:<br>
      &nbsp;&nbsp;① <b>형태(Form)</b>: 문장에서 쓰일 때 형태의 변화 여부 ➔ <b>불변어</b>(형태 불변) vs <b>가변어</b>(형태 변화/활용, <span class="badge-trap">[함정]</span> 서술격 조사 '이다' 포함)<br>
      &nbsp;&nbsp;② <b>기능(Function)</b>: 문장 안에서 담당하는 문법적 역할 ➔ <b>체언 · 수식언 · 관계언 · 독립언 · 용언</b> (5대 기능군)<br>
      &nbsp;&nbsp;③ <b>의미(Meaning)</b>: 단어가 나타내는 고유한 의미 범주 ➔ <b>명사 · 대명사 · 수사 · 관형사 · 부사 · 조사 · 감탄사 · 동사 · 형용사</b> (9품사)
    </div>

    <!-- 2. [인포그래픽 1] 한 문장 9품사 올인원 완전체 카드 -->
    <div class="sentence-container">
      <div class="sentence-title">
        ★ [인포그래픽 1] <span class="badge-frequent">[빈출]</span> <b>9품사 올인원 완전체 문장</b> — "앗! 그가 새 옷 둘을 아주 예쁘게 입는다."
      </div>
      <table class="sentence-table">
        <tr>
          <td>
            <span class="token-word">앗!</span>
            <span class="token-pos">감탄사</span><br>
            <span class="token-func">독립언<br>(불변어)</span>
          </td>
          <td>
            <span class="token-word">그</span>
            <span class="token-pos">대명사</span><br>
            <span class="token-func">체언<br>(불변어)</span>
          </td>
          <td>
            <span class="token-word">가</span>
            <span class="token-pos">조사</span><br>
            <span class="token-func">관계언<br>(불변어)</span>
          </td>
          <td>
            <span class="token-word">새</span>
            <span class="token-pos">관형사</span><br>
            <span class="token-func">수식언<br>(불변어)</span>
          </td>
          <td>
            <span class="token-word">옷</span>
            <span class="token-pos">명사</span><br>
            <span class="token-func">체언<br>(불변어)</span>
          </td>
          <td>
            <span class="token-word">둘</span>
            <span class="token-pos">수사</span><br>
            <span class="token-func">체언<br>(불변어)</span>
          </td>
          <td>
            <span class="token-word">을</span>
            <span class="token-pos">조사</span><br>
            <span class="token-func">관계언<br>(불변어)</span>
          </td>
          <td>
            <span class="token-word">아주</span>
            <span class="token-pos">부사</span><br>
            <span class="token-func">수식언<br>(불변어)</span>
          </td>
          <td>
            <span class="token-word">예쁘게</span>
            <span class="token-pos">형용사</span><br>
            <span class="token-func">용언<br>(가변어)</span>
          </td>
          <td>
            <span class="token-word">입는다</span>
            <span class="token-pos">동사</span><br>
            <span class="token-func">용언<br>(가변어)</span>
          </td>
        </tr>
      </table>
    </div>

    <!-- 3. [인포그래픽 2] 5대 기능군 블록 카드형 9품사 계통도 -->
    <div class="section-title">2. 5대 기능군 블록 카드형 9품사 계통도</div>

    <!-- 불변어 4대 기능군 -->
    <div class="block-header-black">■ [불변어 기능군] 문장에서 쓰일 때 형태가 변하지 않는 단어 (체언 · 수식언 · 관계언 · 독립언)</div>
    <table class="func-grid-table">
      <tr>
        <td>
          <div class="pos-card-title">① 체언(體言) — 문장의 몸체 (주어·목적어·보어 구실)</div>
          • <b>명사</b>: 구체적·추상적 이름 (<span class="badge-ex">철수</span>, <span class="badge-ex">하늘</span>, <span class="badge-ex">평화</span>, <span class="badge-ex">바람</span>)<br>
          • <b>대명사</b>: 이름 대신 가리킴 (<span class="badge-ex">나</span>, <span class="badge-ex">우리</span>, <span class="badge-ex">이것</span>, <span class="badge-ex">여기</span>, <span class="badge-ex">그</span>)<br>
          • <b>수사</b>: 수량이나 순서 (<span class="badge-ex">하나</span>, <span class="badge-ex">둘</span>, <span class="badge-ex">첫째</span>, <span class="badge-ex">일</span>, <span class="badge-ex">이</span>)<br>
          • <b>공통 특징</b>: 형태가 변하지 않으며, 뒤에 다양한 <u>조사가 자유롭게 결합</u>함.
        </td>
        <td>
          <div class="pos-card-title">② 수식언(修飾言) — 다른 말을 꾸며 뜻을 한정하는 구실</div>
          • <b>관형사</b>: <u>오직 체언(명·대·수)만 전문 수식</u> (<span class="badge-ex">새</span>, <span class="badge-ex">헌</span>, <span class="badge-ex">옛</span>, <span class="badge-ex">이</span>, <span class="badge-ex">모든</span>)<br>
          • <b>부사</b>: <u>주로 용언(동·형) 및 문장 전체 수식</u> (<span class="badge-ex">아주</span>, <span class="badge-ex">빨리</span>, <span class="badge-ex">참</span>, <span class="badge-ex">과연</span>)<br>
          • <span class="badge-trap">[함정]</span> 관형사 뒤에는 <b>조사가 결코 결합할 수 없음</b>!
        </td>
      </tr>
      <tr>
        <td>
          <div class="pos-card-title">③ 관계언(關係言) — 문법적 관계를 표시하거나 뜻을 더함</div>
          • <b>조사</b>: 주로 체언 뒤에 붙어 자격을 부여함 (<span class="badge-ex">이/가</span>, <span class="badge-ex">을/를</span>, <span class="badge-ex">의</span>, <span class="badge-ex">도</span>, <span class="badge-ex">만</span>)<br>
          • <span class="badge-trap">[함정]</span> 서술격 조사 <b>'이다'</b>: 조사이지만 용언처럼 형태가 변하므로 <b>유일하게 가변어에 속하는 조사 예외</b>! (이다, 이고, 이니, 이면)
        </td>
        <td>
          <div class="pos-card-title">④ 독립언(獨立言) — 문장의 다른 성분과 직접 관계 없음</div>
          • <b>감탄사</b>: 놀람, 느낌, 부름, 대답 (<span class="badge-ex">앗</span>, <span class="badge-ex">어머나</span>, <span class="badge-ex">야</span>, <span class="badge-ex">네</span>, <span class="badge-ex">아니요</span>)<br>
          • <b>특징</b>: 문장 맨 앞에 주로 오며, 생략해도 문장이 온전히 성립함.<br>
          • <span class="badge-trap">[함정]</span> "영수야!"의 '야'는 감탄사가 아니라 <b>체언+호격조사</b>!
        </td>
      </tr>
    </table>

    <!-- 가변어 1대 기능군 (용언) -->
    <div class="block-header-gray">■ [가변어 기능군] 문장에서 쓰일 때 형태가 변하는(활용하는) 단어 — 용언 (동사 vs 형용사)</div>
    <table class="func-grid-table">
      <tr>
        <td>
          <div class="pos-card-title">⑤ 용언(用言) — 동사 (움직임·동작·작용)</div>
          • <b>개념</b>: 대상의 움직임이나 작용을 나타내는 단어.<br>
          • <b>대표 예시</b>: <span class="badge-ex">가다</span>, <span class="badge-ex">먹다</span>, <span class="badge-ex">달리다</span>, <span class="badge-ex">읽다</span>, <span class="badge-ex">입다</span>, <span class="badge-ex">솟다</span><br>
          • <b>문법 판정</b>: 현재 시제 어미('-ㄴ다/-는다') 결합 가능! 명령형('-어라') 및 청유형('-자') 결합 가능!
        </td>
        <td>
          <div class="pos-card-title">⑤ 용언(用言) — 형용사 (성질·상태)</div>
          • <b>개념</b>: 대상의 성질이나 상태를 나타내는 단어.<br>
          • <b>대표 예시</b>: <span class="badge-ex">예쁘다</span>, <span class="badge-ex">푸르다</span>, <span class="badge-ex">조용하다</span>, <span class="badge-ex">착하다</span>, <span class="badge-ex">맑다</span><br>
          • <b>문법 판정</b>: 현재 시제 어미 결합 <b>불가</b>(예쁜다X)! 명령형·청유형 결합 <b>불가</b>(예뻐라[명령]X, 조용하자X)!
        </td>
      </tr>
    </table>

  </div>
  <!-- 1페이지 끝 -->

  <div class="page-break"></div>

  <!-- ================================================================= -->
  <!-- PAGE 2: 판별 알고리즘 + 3대 문법 함정 + 담화 활용 효과 + 실전 체크 -->
  <!-- ================================================================= -->
  <div class="page-2-container">

    <!-- 4. [인포그래픽 3] 동사 vs 형용사 초고속 판별 알고리즘 -->
    <div class="section-title" style="margin-top:0;">3. [함정] 동사 vs 형용사 초고속 판별 알고리즘 & 검증 체크리스트</div>

    <div class="flow-container">
      <div class="flow-title">
        ★ [판별 순서도] <b>동사 vs 형용사 1초 판별 저울</b> — 기본형 어간에 현재 시제 어미('-ㄴ다/-는다')를 결합하라!
      </div>
      <table class="flow-table">
        <tr>
          <td style="width:25%;">
            <div class="flow-step-box" style="background-color:#fff; text-align:center;">
              <b>[검증 대상 단어]</b><br>기본형 어간 분리<br>예: '먹-', '예쁘-'
            </div>
          </td>
          <td class="flow-arrow-cell">➔</td>
          <td style="width:38%;">
            <div class="flow-step-box" style="background-color:#f5f5f5; border:1.5px solid #000; text-align:center;">
              <b>[핵심 판별 저울 공식]</b><br>
              현재 시제 <b>'-ㄴ다 / -는다'</b> 결합!<br>
              또는 명령(<b>-아라</b>) / 청유(<b>-자</b>) 결합!
            </div>
          </td>
          <td class="flow-arrow-cell">➔</td>
          <td style="width:37%;">
            <div class="flow-step-box" style="background-color:#fff;">
              • <b>자연스러우면 (O)</b> ➔ <b>[동사]</b><br>
              &nbsp;&nbsp;먹는다(O), 달린다(O), 늙는다(O)<br>
              • <b>어색·불가능 (X)</b> ➔ <b>[형용사]</b><br>
              &nbsp;&nbsp;예쁜다(X), 푸른다(X), 젊는다(X)
            </div>
          </td>
        </tr>
      </table>
    </div>

    <!-- 판별 5대 검증 체크리스트 표 -->
    <table class="check-table">
      <tr>
        <th style="width:25%;">검증 문법 기준</th>
        <th style="width:37%;">동사 (움직임·작용)</th>
        <th style="width:38%;">형용사 (성질·상태)</th>
      </tr>
      <tr>
        <td><b>현재 시제 ('-ㄴ다/-는다')</b></td>
        <td>결합 가능: 읽는다(O), 간다(O)</td>
        <td><b>결합 불가</b>: 조용한다(X), 착한다(X)</td>
      </tr>
      <tr>
        <td><b>명령형 어미 ('-아라/-어라')</b></td>
        <td>결합 가능: 빨리 뛰어라(O)</td>
        <td><b>결합 불가</b>: 예뻐라[명령](X), 조용해라[상태](X)</td>
      </tr>
      <tr>
        <td><b>청유형 어미 ('-자')</b></td>
        <td>결합 가능: 내일 함께 가자(O)</td>
        <td><b>결합 불가</b>: 항상 건강하자(X), 행복하자(X)</td>
      </tr>
      <tr>
        <td><b>현재 진행형 ('-고 있다')</b></td>
        <td>결합 가능: 밥을 먹고 있다(O)</td>
        <td><b>결합 불가</b>: 하늘이 푸르고 있다(X)</td>
      </tr>
      <tr>
        <td><b>목적·의도 ('-러 / -려')</b></td>
        <td>결합 가능: 놀러 가다(O), 자려고 하다(O)</td>
        <td><b>결합 불가</b>: 예쁘러 가다(X), 맑으려 하다(X)</td>
      </tr>
    </table>

    <!-- 5. [인포그래픽 4] 실전 시험 단골 3대 문법 함정 정복 클리닉 -->
    <div class="section-title">4. [함정] 실전 시험 단골 3대 문법 함정 정복 클리닉</div>
    <table class="trap-3col-table">
      <tr>
        <th><span class="badge-trap">[함정 1]</span> 수사 vs 수 관형사 구별</th>
        <th><span class="badge-trap">[함정 2]</span> 관형사 뒤 조사 결합 오류</th>
        <th><span class="badge-trap">[함정 3]</span> 형용사의 청유·명령형 오류</th>
      </tr>
      <tr>
        <td>
          • 뒤에 <b>조사가 결합할 수 있으면</b> ➔ <b>[수사]</b><br>
          &nbsp;&nbsp;"사과 <b>둘을</b> 먹었다." (조사 '을' 결합 O)<br>
          • 뒤의 명사를 수식, <b>조사가 못 붙으면</b> ➔ <b>[관형사]</b><br>
          &nbsp;&nbsp;"사과 <b>두</b> 개를 먹었다." (명사 '개' 수식)
        </td>
        <td>
          • 관형사는 체언만 꾸미며 <b>조사 결합 절대 불가</b><br>
          • (X) "<b>옛부터</b> 전해 내려온 마을 이야기"<br>
          • (O) "<b>옛날부터</b> 전해 내려온 마을 이야기"<br>
          &nbsp;&nbsp;(관형사 '옛' ➔ 명사 '옛날' 교체 후 조사 결합)
        </td>
        <td>
          • 형용사는 상태이므로 <b>청유('-자')·명령 불가</b><br>
          • (X) "우리 앞으로 항상 <b>행복하자</b>."<br>
          • (O) "우리 앞으로 <b>행복하게 살자</b>." (동사 결합)<br>
          • (O) "마음이 <b>착해지자</b>." (동사화)
        </td>
      </tr>
    </table>

    <!-- 6. [인포그래픽 5] 담화 성격 및 연설문 속 품사의 전략적 활용 효과 -->
    <div class="section-title">5. [빈출] 담화 성격 및 연설문 속 품사의 전략적 활용 효과</div>
    <table class="effect-2col-table">
      <tr>
        <th><span class="badge-frequent">[빈출]</span> 그림책 《달 샤베트》(백희나) — 감각적 담화</th>
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

    <div class="card-box" style="margin-bottom:3.5px;">
      <b>[창의 연계 제재] 〈세상을 움직인 연설가〉 속 품사 전략</b><br>
      • <b>김구</b>: '독립', '민족' 등 핵심 <b>명사</b> 반복 ➔ 광복을 향한 단호한 의지 강조.<br>
      • <b>스티브 잡스</b>: '대단한', '놀랍다' 등 감정 호소 <b>형용사</b> 활용 ➔ 청중의 감동과 공감 유도.<br>
      • <b>말랄라 유사프자이</b>: '파괴되다', '막다' 등 역동적 <b>동사</b>와 핵심 <b>명사</b> 결합 ➔ 교육권 보장 촉구 호소력 극대화.<br>
      • <b>스파르시 샤</b>: '십오 년', '백삼십 번' 등 정확한 <b>수사</b> 제시 ➔ 객관적 수치를 통한 극복 의지의 진정성 확보.
    </div>

    <!-- 7. 실전 족집게 체크 바 -->
    <div class="summary-bar">
      <b>[시험 직전 5초 체크포인트]</b><br>
      ① 품사 3대 분류 기준: <b>형태</b>(불변어/가변어) ➔ <b>기능</b>(체언/수식언/관계언/독립언/용언) ➔ <b>의미</b>(9품사)<br>
      ② 서술격 조사 '이다'는 조사(관계언)이지만 형태가 변하는 유일한 <b>가변어</b>이다.<br>
      ③ 수사 뒤에는 조사가 붙을 수 있고("둘을"), 수 관형사 뒤에는 조사가 결코 붙을 수 없다("두 개").<br>
      ④ '젊다'는 형용사(젊는다X), '늙다'는 동사(늙는다O)이다. 형용사에는 청유형('-자')과 명령형('-아라/-어라')을 쓸 수 없다!
    </div>

  </div>
  <!-- 2페이지 끝 -->

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

    if len(doc) == 2:
        print("\n>>> SUCCESS: Exact 2-Page Match! <<<")
    else:
        print(f"\n>>> WARNING: Expected 2 pages, but got {len(doc)} pages! <<<")

if __name__ == '__main__':
    generate_summary_pdf()
