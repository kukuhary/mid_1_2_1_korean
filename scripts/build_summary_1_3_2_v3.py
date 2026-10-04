import os
import shutil
import subprocess
import fitz

def generate_brainstorming_summary_v3():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(base_dir) == 'scripts':

        base_dir = os.path.dirname(base_dir)
    summary_dir = os.path.join(base_dir, '요약')
    os.makedirs(summary_dir, exist_ok=True)

    # 마크다운 v3 동기화 생성
    md_v2_path = os.path.join(summary_dir, '1단원_3-2단원_통합_핵심요약_v2.md')
    md_v3_path = os.path.join(summary_dir, '1단원_3-2단원_통합_핵심요약_v3.md')
    if os.path.exists(md_v2_path):
        with open(md_v2_path, 'r', encoding='utf-8') as f:
            md_text = f.read()
        md_text = md_text.replace('[v2]', '[v3]').replace('_v2', '_v3')
        with open(md_v3_path, 'w', encoding='utf-8') as f:
            f.write(md_text)

    html_path = os.path.join(summary_dir, '1단원_3-2단원_통합_핵심요약_v3.html')
    pdf_path = os.path.join(summary_dir, '1단원_3-2단원_통합_핵심요약_v3.pdf')
    root_pdf_path = os.path.join(base_dir, '1단원_3-2단원_통합_핵심요약_v3.pdf')

    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[교과서 핵심 요약] 1단원(1·2) &amp; 3단원(2) 브레인스토밍 &amp; 하이라키 마인드맵 통합 요약집 [v3]</title>
<style>
  @page {
    size: A4 portrait;
    margin: 7mm 10mm 7mm 10mm;
    @bottom-center {
      content: "- " counter(page) " -";
      font-size: 10pt;
      font-family: 'Malgun Gothic', sans-serif;
      font-weight: bold;
      color: #000;
    }
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  body {
    font-family: 'Malgun Gothic', '맑은 고딕', 'Apple SD Gothic Neo', sans-serif;
    color: #000;
    background: #fff;
    margin: 0;
    padding: 0;
    font-size: 12.0pt;
    line-height: 1.98;
    letter-spacing: 1.35px;
    word-break: keep-all;
  }
  .page-section {
    page-break-after: always;
    break-after: page;
    page-break-inside: avoid;
    break-inside: avoid;
  }
  .page-section:last-child {
    page-break-after: auto;
    break-after: auto;
  }
  /* 상단 헤더 박스 */
  .header-box {
    border: 2.5px solid #000;
    padding: 5px 12px;
    margin-bottom: 6px;
    background-color: #fff;
    border-radius: 8px;
  }
  .header-title {
    font-size: 14.5pt;
    font-weight: 900;
    text-align: center;
    margin: 0 0 2px 0;
    letter-spacing: 1.4px;
    line-height: 1.28;
  }
  .header-sub {
    font-size: 9.8pt;
    text-align: center;
    border-top: 1.5px dashed #333;
    padding-top: 3px;
    line-height: 1.4;
    letter-spacing: 0.9px;
  }
  /* 대단원/파트 배너 */
  .part-banner {
    background-color: #000;
    color: #fff;
    font-size: 12.4pt;
    font-weight: 900;
    padding: 5px 14px;
    margin: 0 0 7px 0;
    border-radius: 8px;
    letter-spacing: 1.3px;
    line-height: 1.32;
  }
  /* SVG 마인드맵 컨테이너: 가로 폭 700px 1:1 무축소 매핑으로 폰트 축소 원천 차단 */
  .mindmap-container {
    border: 2.5px solid #000;
    border-radius: 12px;
    background-color: #fff;
    padding: 6px 10px;
    margin-bottom: 8px;
    text-align: center;
  }
  .mindmap-container svg {
    width: 100%;
    height: auto;
    display: block;
    margin: 0 auto;
  }
  .mindmap-container svg text {
    letter-spacing: 0.2px;
  }
  .mindmap-caption {
    font-size: 11.4pt;
    font-weight: 900;
    background-color: #f0f0f0;
    border: 2px solid #000;
    border-radius: 6px;
    padding: 3px 14px;
    margin-bottom: 5px;
    display: inline-block;
    letter-spacing: 1.2px;
    line-height: 1.32;
  }
  /* 브레인스토밍 다단계 하이라키(Hierarchy) 트리 구조 */
  .hierarchy-board {
    border: 2px solid #000;
    border-radius: 12px;
    padding: 8px 14px;
    background-color: #fff;
  }
  .root-node {
    display: inline-block;
    background-color: #000;
    color: #fff;
    font-size: 12.2pt;
    font-weight: 900;
    padding: 3px 14px;
    border-radius: 25px;
    margin-bottom: 7px;
    letter-spacing: 1.3px;
    line-height: 1.38;
  }
  .level-1-list {
    margin: 0;
    padding-left: 14px;
    border-left: 3.5px solid #000;
    margin-left: 8px;
  }
  .level-1-item {
    position: relative;
    margin-bottom: 8px;
    padding-left: 14px;
  }
  .level-1-item:last-child {
    margin-bottom: 2px;
  }
  .level-1-item::before {
    content: "";
    position: absolute;
    left: -14px;
    top: 13px;
    width: 21px;
    height: 3.5px;
    background-color: #000;
  }
  .level-1-title {
    display: inline-block;
    border: 2px solid #000;
    background-color: #f4f4f4;
    font-size: 11.8pt;
    font-weight: 900;
    padding: 2px 12px;
    border-radius: 8px;
    margin-bottom: 4px;
    letter-spacing: 1.25px;
    line-height: 1.42;
  }
  .level-2-list {
    margin: 0;
    padding-left: 18px;
    border-left: 2px dashed #222;
    margin-left: 10px;
  }
  .level-2-item {
    position: relative;
    margin-bottom: 4px;
    padding-left: 12px;
    font-size: 11.6pt;
    line-height: 1.88;
    letter-spacing: 1.3px;
  }
  .level-2-item:last-child {
    margin-bottom: 2px;
  }
  .level-2-item::before {
    content: "┗━";
    position: absolute;
    left: -17px;
    top: 0;
    font-weight: 900;
    color: #000;
  }
  .level-3-box {
    border-left: 3px solid #000;
    background-color: #fafafa;
    padding: 5px 12px;
    margin-top: 3px;
    margin-bottom: 3px;
    border-radius: 0 8px 8px 0;
    font-size: 11.3pt;
    line-height: 1.90;
    letter-spacing: 1.25px;
  }
  .badge-freq {
    display: inline-block;
    background-color: #000;
    color: #fff;
    font-size: 10.0pt;
    font-weight: 900;
    padding: 1px 7px;
    border-radius: 4px;
    margin-right: 5px;
    letter-spacing: 1.0px;
    line-height: 1.32;
    vertical-align: middle;
  }
  .badge-trap {
    display: inline-block;
    border: 2px solid #000;
    background-color: #fff;
    color: #000;
    font-size: 10.0pt;
    font-weight: 900;
    padding: 1px 7px;
    border-radius: 4px;
    margin-right: 5px;
    letter-spacing: 1.0px;
    line-height: 1.32;
    vertical-align: middle;
  }
  .kw-pill {
    display: inline-block;
    border: 1.5px solid #000;
    background-color: #eee;
    padding: 0px 6px;
    border-radius: 6px;
    font-weight: 900;
    margin: 0 2px;
    line-height: 1.4;
  }
</style>
</head>
<body>

  <!-- =========================================================================
       PAGE 1: 1-(1) 〈길〉 — 비유와 운율 방사형 브레인스토밍 마인드맵 & 하이라키
       ========================================================================= -->
  <div class="page-section">
    <div class="header-box">
      <div class="header-title">[브레인스토밍 &amp; 하이라키 요약] 1단원(1·2) &amp; 3단원(2) 통합 마인드맵 [v3]</div>
      <div class="header-sub">
        <b>[적용 범위]</b> 미래엔 국어 1-1: <b>1.(1) 길 · 1.(2) 사랑하는 별 하나 (12~41쪽)</b> / <b>3.(2) 품사의 종류와 특성 (122~149쪽)</b><br>
        <b>[조판 규격]</b> GEMINI.md 준수 · <b>다이어그램(SVG) 내부 글자 크기 1.7배 확대(11~14.5pt)</b> · 100% 흑백 마인드맵 &amp; 다단계 하이라키
      </div>
    </div>

    <div class="part-banner">[Page 1] 1-(1) 〈길〉 — 시의 비유와 운율 방사형 브레인스토밍 마인드맵 (12~21쪽)</div>

    <!-- [다이어그램 1] 가로 폭 700px 1:1 무축소 + 대형 폰트(15~18.5px = 11.3~14.0pt) -->
    <div class="mindmap-container">
      <div class="mindmap-caption">[브레인스토밍 마인드맵 1] 중심 코어 『비유와 운율』에서 뻗어 나가는 방사형 개념 지도</div>
      <svg viewBox="0 0 700 206" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow1" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#000"/>
          </marker>
        </defs>
        <!-- 중앙 코어 노드 -->
        <ellipse cx="350" cy="103" rx="82" ry="48" fill="#fff" stroke="#000" stroke-width="3.5"/>
        <ellipse cx="350" cy="103" rx="75" ry="41" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="8,4"/>
        <text x="350" y="96" font-family="Malgun Gothic" font-size="18.5" font-weight="900" text-anchor="middle" letter-spacing="1">1-(1) 비유와</text>
        <text x="350" y="121" font-family="Malgun Gothic" font-size="18.5" font-weight="900" text-anchor="middle" letter-spacing="1">운율 핵심</text>

        <!-- 1. 좌상단: 직유법 -->
        <path d="M 276 80 L 246 44" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow1)"/>
        <rect x="4" y="6" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="30" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">직유법 [빈출]</text>
        <text x="123" y="53" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">같이 · 처럼 · 듯이 · 인 양</text>

        <!-- 2. 좌중단: 은유법 -->
        <path d="M 268 103 L 246 103" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow1)"/>
        <rect x="4" y="74" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="98" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">은유법 [빈출] ('A는 B')</text>
        <text x="123" y="121" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">길=포도 덩굴 / 세계=과일</text>

        <!-- 3. 좌하단: 의인법 -->
        <path d="M 276 126 L 246 162" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow1)"/>
        <rect x="4" y="142" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="166" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">의인법 (사람처럼 표현)</text>
        <text x="123" y="189" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">"해님이 웃는다" (〈햇비〉)</text>

        <!-- 4. 우상단: 비유의 2대 효과 -->
        <path d="M 424 80 L 454 44" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow1)"/>
        <rect x="458" y="6" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="30" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">비유의 2대 표현 효과</text>
        <text x="577" y="53" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">참신·생생 / 구체적 인상</text>

        <!-- 5. 우중단: 운율 형성 3요소 -->
        <path d="M 432 103 L 454 103" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow1)"/>
        <rect x="458" y="74" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="98" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">운율 형성 3요소 (가락)</text>
        <text x="577" y="121" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">반복 · 음수율 · 의성·의태어</text>

        <!-- 6. 우하단: 3연 함정 -->
        <path d="M 424 126 L 454 162" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow1)"/>
        <rect x="458" y="142" width="238" height="58" rx="16" fill="#fff" stroke="#000" stroke-width="3.0"/>
        <text x="577" y="166" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">[함정] 〈길〉 3연 시어</text>
        <text x="577" y="189" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">원관념 없이 보조관념만 제시</text>
      </svg>
    </div>

    <!-- 하이라키 트리 구조 1 -->
    <div class="hierarchy-board">
      <div class="root-node">[Root 1] 시의 비유(比喩)와 운율(韻律) 핵심 하이라키</div>
      <div class="level-1-list">
        <div class="level-1-item">
          <div class="level-1-title">1. 비유 (比喩) — 원관념을 비슷한 성질의 보조 관념에 빗대기 <span class="badge-freq">[빈출]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>원리와 효과</b> : <span class="kw-pill">원관념</span>을 유사한 <span class="kw-pill">보조 관념</span>에 빗대어 ① <b>참신하고 생생한 느낌</b>, ② <b>구체적이고 선명한 인상</b>을 줌</div>
            <div class="level-2-item"><b>3대 비유법 하이라키</b>
              <div class="level-3-box">
                • <b>① 직유법</b> : <b>‘같이(같은), 처럼, 듯이, 인 양’</b> 연결어 사용 ➔ <i>담요처럼(13쪽), 포도송이 같은 마을(14쪽), 아씨처럼 · 옥수숫대처럼(22쪽)</i><br>
                • <b>② 은유법</b> : 연결어 없이 <b>‘A는 B이다’</b> 형식 ➔ <i>길은 포도 덩굴 · 세계는 한 덩이 과일(14~15쪽), 하늘 다리(22쪽), 꿈=여행(23쪽)</i><br>
                • <b>③ 의인법</b> : 사물에 <b>사람의 동작·감정</b> 부여 ➔ <i>해님이 웃는다 / 나 보고 웃는다 / 즐거워 웃는다(22쪽 〈햇비〉)</i>
              </div>
            </div>
          </div>
        </div>

        <div class="level-1-item">
          <div class="level-1-title">2. 운율 (韻律) — 시를 읽을 때 느껴지는 말의 가락(리듬감) <span class="badge-freq">[빈출]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>형성 3요소</b> : ① <b>소리·단어·구절·문장 구조 반복</b> &nbsp; ② <b>규칙적 끊어 읽기</b> &nbsp; ③ <b>의성어·의태어(`토실토실, 보슬보슬, 알롱알롱`)</b></div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 2: 1-(1) 〈길〉 · 〈햇비〉 · 〈문어의 꿈〉 좌➔우 베지어 가지 하이라키 맵
       ========================================================================= -->
  <div class="page-section">
    <div class="part-banner">[Page 2] 1-(1) 수록 작품 3종 (〈길〉 · 〈햇비〉 · 〈문어의 꿈〉) 가지 분기형 하이라키 (14~27쪽)</div>

    <!-- [다이어그램 2] 좌➔우 가지 맵: viewBox(700x234) + 대형 폰트(14.5~16.5px = 11.0~12.5pt) -->
    <div class="mindmap-container">
      <div class="mindmap-caption">[하이라키 가지 맵 2] 좌측 루트에서 우측으로 뻗어 나가는 1-(1) 수록 작품 3종 구조도</div>
      <svg viewBox="0 0 700 234" xmlns="http://www.w3.org/2000/svg">
        <!-- 루트 박스 -->
        <rect x="2" y="86" width="104" height="62" rx="10" fill="#f0f0f0" stroke="#000" stroke-width="3"/>
        <text x="54" y="113" font-family="Malgun Gothic" font-size="16.5" font-weight="900" text-anchor="middle">1-(1) 작품</text>
        <text x="54" y="136" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">비유·운율</text>

        <!-- 1차 가지 1: 김종상 <길> -->
        <path d="M 106 117 C 116 117, 118 45, 126 45 L 242 45" fill="none" stroke="#000" stroke-width="3"/>
        <rect x="124" y="28" width="118" height="34" rx="8" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="51" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">김종상 〈길〉</text>

        <path d="M 242 45 C 254 45, 256 19, 264 19 L 698 19" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="14" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">1·2연 : 길(포도 덩굴: 은유) / 마을(포도송이)·집(포도알: 직유)</text>

        <path d="M 242 45 L 698 45" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="40" font-family="Malgun Gothic" font-size="14.5" font-weight="900">[함정] 3연 : 포도알·포도송이·이 덩굴 (원관념 없이 보조관념만)</text>

        <path d="M 242 45 C 254 45, 256 71, 264 71 L 698 71" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="66" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">4·5연 : 세계=한 덩이 과일(은유) / 토실토실 익어 감(의태어)</text>

        <!-- 1차 가지 2: 윤동주 <햇비> -->
        <path d="M 106 117 L 242 117" fill="none" stroke="#000" stroke-width="3"/>
        <rect x="124" y="100" width="118" height="34" rx="8" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="123" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">윤동주 〈햇비〉</text>

        <path d="M 242 117 C 254 117, 256 102, 264 102 L 698 102" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="97" font-family="Malgun Gothic" font-size="14.5" font-weight="900">[함정] 직유 : 아씨처럼(=햇비) vs 옥수숫대처럼(=자라는 아이들)</text>

        <path d="M 242 117 C 254 117, 256 128, 264 128 L 698 128" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="123" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">은유·의인 : 하늘 다리(=무지개: 은유) / 해님이 웃는다(의인법)</text>

        <path d="M 242 117 C 254 117, 256 154, 264 154 L 698 154" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="149" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">운율 : 보슬보슬·알롱알롱(의태어) + 4·2(3)조 + 1·2연 대칭</text>

        <!-- 1차 가지 3: 문어의 꿈 & 27쪽 어휘 -->
        <path d="M 106 117 C 116 117, 118 198, 126 198 L 242 198" fill="none" stroke="#000" stroke-width="3"/>
        <rect x="124" y="181" width="118" height="34" rx="8" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="204" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">문어의 꿈·어휘</text>

        <path d="M 242 198 C 254 198, 256 186, 264 186 L 698 186" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="181" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">〈문어의 꿈〉 : 꿈=여행(은유) / '~면 나는 ~ 문어' 구조 반복</text>

        <path d="M 242 198 C 254 198, 256 214, 264 214 L 698 214" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="209" font-family="Malgun Gothic" font-size="14.5" font-weight="900">[함정] 27쪽 : 토실토실(➔한들한들) · 특수(➔특성) · 참견(➔참신)</text>
      </svg>
    </div>

    <!-- 하이라키 트리 구조 2 -->
    <div class="hierarchy-board">
      <div class="root-node">[Root 2] 〈길〉 · 〈햇비〉 · 〈문어의 꿈〉 교과서 원문 &amp; 핵심 포인트 하이라키</div>
      <div class="level-1-list">
        <div class="level-1-item">
          <div class="level-1-title">1. 김종상, 〈길〉 (14~15쪽) 1연~5연 본문 원문 및 비유 하이라키 <span class="badge-freq">[빈출]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>[1연~2연 원문]</b> : <b>“길은 포도 덩굴</b>(은유) / 몇백 년이나 자라 땅덩이를 다 덮었다 // 이 덩굴 가지(작은 길)마다 / <b>포도송이 같은 마을</b>(직유)이 있고 / <b>포도알 같은 집들</b>(직유)이 달렸다”</div>
            <div class="level-2-item"><b>[3연~5연 원문]</b> : “<b>포도알</b>(집)이 늘 때마다 <b>포도송이</b>(마을)는 커 가고 / <b>갈봄 없이</b>(사계절 내내) 자라 가는 <b>이 덩굴</b>(길)을 통하여 // 사람과 사람이 도와 가고 마을과 마을은 이어져서 // <b>세계는 한 덩이 과일로</b>(은유) / <b>토실토실</b>(의태어) 익어 가고 있는 것이다.”</div>
            <div class="level-2-item"><span class="badge-trap">[함정]</span> <b>출제 1순위 함정</b> : 2연은 원관념(`마을, 집들`)과 연결어(`같은`)가 있는 <b>직유법</b>이나, <b>3연의 `포도알, 포도송이, 이 덩굴`은 원관념 없이 보조 관념만으로 대상을 가리킴!</b></div>
          </div>
        </div>

        <div class="level-1-item">
          <div class="level-1-title">2. 윤동주, 〈햇비〉 (22쪽) &amp; 안예은, 〈문어의 꿈〉 (23쪽) 하이라키 <span class="badge-trap">[함정]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>〈햇비〉 핵심 원문</b> : “<b>아씨처럼</b> 나린다 <b>보슬보슬</b> 햇비 / 맞아 주자 다 같이 <b>옥수숫대처럼 크게</b> 닷 자 엿 자 자라게 / <b>해님이 웃는다 나 보고 웃는다</b> // <b>하늘 다리</b> 놓였다 <b>알롱알롱</b> 무지개 ... <b>해님이 웃는다 즐거워 웃는다.</b>”</div>
            <div class="level-2-item"><span class="badge-trap">[함정]</span> <b>원관념 매핑 주의</b> : `아씨처럼`의 원관념은 <b>‘햇비’</b>이지만, `옥수숫대처럼 크게`의 원관념은 햇비가 아니라 <b>햇비를 맞으며 자라는 ‘우리(아이들)’</b>임!</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 3: 1-(2) 〈사랑하는 별 하나〉 — 상징 브레인스토밍 마인드맵 & 하이라키
       ========================================================================= -->
  <div class="page-section">
    <div class="part-banner">[Page 3] 1-(2) 〈사랑하는 별 하나〉 — 상징(象徵)의 원리와 방사형 마인드맵 (28~35쪽)</div>

    <!-- [다이어그램 3] 1:1 무축소 viewBox(700x206) + 대형 폰트(15~18.5px) -->
    <div class="mindmap-container">
      <div class="mindmap-caption">[브레인스토밍 마인드맵 3] 중심 코어 『상징(象徵)과 별·들꽃』에서 확장되는 방사형 사고 지도</div>
      <svg viewBox="0 0 700 206" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow3" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#000"/>
          </marker>
        </defs>
        <ellipse cx="350" cy="103" rx="84" ry="48" fill="#fff" stroke="#000" stroke-width="3.5"/>
        <ellipse cx="350" cy="103" rx="77" ry="41" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="8,4"/>
        <text x="350" y="96" font-family="Malgun Gothic" font-size="18.5" font-weight="900" text-anchor="middle" letter-spacing="1">1-(2) 상징(象徵)</text>
        <text x="350" y="121" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle" letter-spacing="0.5">사랑하는 별 하나</text>

        <!-- 1. 좌상단: 상징의 개념 -->
        <path d="M 276 80 L 246 44" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow3)"/>
        <rect x="4" y="6" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="30" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">상징의 개념 [빈출]</text>
        <text x="123" y="53" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">추상적 개념 ➔ 구체적 대상</text>

        <!-- 2. 좌중단: 비유 vs 상징 -->
        <path d="M 266 103 L 246 103" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow3)"/>
        <rect x="4" y="74" width="238" height="58" rx="16" fill="#fff" stroke="#000" stroke-width="3.0"/>
        <text x="123" y="98" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">[함정] 비유 vs 상징</text>
        <text x="123" y="121" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">비유(A·B 공존) / 상징(B만!)</text>

        <!-- 3. 좌하단: 다의성 -->
        <path d="M 276 126 L 246 162" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow3)"/>
        <rect x="4" y="142" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="166" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">상징의 다의성 (대추)</text>
        <text x="123" y="189" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">원관념 생략 ➔ 다양한 해석</text>

        <!-- 4. 우상단: 1~2연 소망 -->
        <path d="M 424 80 L 454 44" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow3)"/>
        <rect x="458" y="6" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="30" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">1~2연 (~될 수 있을까)</text>
        <text x="577" y="53" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">나 ➔ 타인에게 위로(별·들꽃)</text>

        <!-- 5. 우중단: 3~4연 소망 -->
        <path d="M 434 103 L 454 103" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow3)"/>
        <rect x="458" y="74" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="98" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">3~4연 (~갖고 싶다)</text>
        <text x="577" y="121" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">타인 ➔ 나를 정화·인도(별)</text>

        <!-- 6. 우하단: 시적 허용 -->
        <path d="M 424 126 L 454 162" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow3)"/>
        <rect x="458" y="142" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="166" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">핵심 표현 기법</text>
        <text x="577" y="189" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">화안히(시적 허용)·눈물짓듯</text>
      </svg>
    </div>

    <!-- 하이라키 트리 구조 3 -->
    <div class="hierarchy-board">
      <div class="root-node">[Root 3] 상징(象徵)의 원리 및 〈사랑하는 별 하나〉 대칭 하이라키</div>
      <div class="level-1-list">
        <div class="level-1-item">
          <div class="level-1-title">1. 상징(象徵)의 뜻 · 다의성 · 비유와의 차이점 <span class="badge-trap">[함정]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>정의 및 다의성(29쪽 《소나기》 ‘대추’)</b> : <b>추상적 개념(원관념)</b>을 숨기고 <b>구체적 대상(‘대추’)만 제시</b>하므로 다감이(<b>친하게 지내고 싶은 마음</b>)와 현주(<b>건강하라는 뜻</b>)처럼 <b>다양하게 해석</b>됨</div>
            <div class="level-2-item"><span class="badge-trap">[함정]</span> <b>비유 vs 상징 구별</b> : 1연 <b>“별(B)과 같은 사람(A)”</b>은 원관념이 드러난 <b>[직유법(비유)]</b> / 3연 <b>“사랑하는 별(B) 하나를 갖고 싶다”</b>는 원관념이 생략된 <b>[상징]</b>!</div>
          </div>
        </div>

        <div class="level-1-item">
          <div class="level-1-title">2. 이성선, 〈사랑하는 별 하나〉 (30~31쪽) 전반부 vs 후반부 대칭 하이라키 <span class="badge-freq">[빈출]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>[1연~2연: `~ 될 수 있을까`] (나 ➔ 타인)</b> : 외롭고 괴로운 이에게 가슴에 <b>‘화안히’</b>(`환히`의 시적 허용) 안기어 <b>‘눈물짓듯 웃어 주는’</b>(직유+의인: 슬픔 공감·위로) <b>‘별과 같은 사람 · 꽃 · 하얀 들꽃’</b>이 되고 싶은 소망</div>
            <div class="level-2-item"><b>[3연~4연: `~ 갖고 싶다`] (타인 ➔ 나)</b> : <b>‘마음 어두운 밤 깊을수록’</b>(고통 심화) 우러러 쳐다보면 <b>‘맑은 눈빛으로 나를 씻어’</b>(정화) <b>‘길을 비추어 주는’</b>(방향 인도) <b>‘별 하나 · 그런 사람’</b>을 만나고 싶은 소망</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 4: 1-(2) 〈파랑새〉 & 38쪽 협동 시 4대 명언 좌➔우 가지 하이라키 맵
       ========================================================================= -->
  <div class="page-section">
    <div class="part-banner">[Page 4] 1-(2) 〈파랑새〉 (모리스 마테를링크) &amp; 38쪽 4대 명언 가지 분기형 하이라키 (36~41쪽)</div>

    <!-- [다이어그램 4] 1:1 무축소 viewBox(700x236) + 대형 폰트(14.5~16.5px) -->
    <div class="mindmap-container">
      <div class="mindmap-caption">[하이라키 가지 맵 4] 〈파랑새〉 서사 구조 및 38쪽 4대 명언 상징물 매핑 트리</div>
      <svg viewBox="0 0 700 236" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="87" width="104" height="62" rx="10" fill="#f0f0f0" stroke="#000" stroke-width="3"/>
        <text x="54" y="114" font-family="Malgun Gothic" font-size="16.5" font-weight="900" text-anchor="middle">1-(2) 상징</text>
        <text x="54" y="137" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">파랑새·명언</text>

        <!-- 1차 가지 1: <파랑새> -->
        <path d="M 106 118 C 116 118, 118 58, 126 58 L 242 58" fill="none" stroke="#000" stroke-width="3"/>
        <rect x="124" y="41" width="118" height="34" rx="8" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="64" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">희곡 〈파랑새〉</text>

        <path d="M 242 58 C 254 58, 256 19, 264 19 L 698 19" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="14" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">꿈속 여행 : 추억의 나라 · 밤의 궁전 · 숲 (진정한 파랑새 못 찾음)</text>

        <path d="M 242 58 C 254 58, 256 45, 264 45 L 698 45" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="40" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">행복의 나라 : 건강·맑은 공기·부모님 사랑·봄·엄마의 행복이 집에 존재</text>

        <path d="M 242 58 C 254 58, 256 71, 264 71 L 698 71" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="66" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">잠 깬 우리 집 : 내 방 새장 속 파랑새 발견 ➔ 아픈 이웃 소녀 병 치유</text>

        <path d="M 242 58 C 254 58, 256 97, 264 97 L 698 97" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="92" font-family="Malgun Gothic" font-size="14.5" font-weight="900">상징 의미 : 파랑새 = 진정한 행복 (일상 속 가까이 &amp; 나누는 마음)</text>

        <!-- 1차 가지 2: 38쪽 4대 명언 -->
        <path d="M 106 118 C 116 118, 118 178, 126 178 L 242 178" fill="none" stroke="#000" stroke-width="3"/>
        <rect x="124" y="161" width="118" height="34" rx="8" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="184" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">38쪽 4대 명언</text>

        <path d="M 242 178 C 254 178, 256 140, 264 140 L 698 140" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="135" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">① 안중근 (불굴의 정의) ➔ 사계절 푸른 소나무, 바위 뚫는 새싹</text>

        <path d="M 242 178 C 254 178, 256 166, 264 166 L 698 166" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="161" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">② 나폴레옹 (도전·용기) ➔ 거친 파도를 헤치고 나아가는 배</text>

        <path d="M 242 178 C 254 178, 256 192, 264 192 L 698 192" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="187" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">③ 헬렌 켈러 (새로운 희망) ➔ 어둠 뒤 아침 해, 겨울 이긴 봄꽃</text>

        <path d="M 242 178 C 254 178, 256 218, 264 218 L 698 218" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="213" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">④ 테레사 (소중한 인생의 가치) ➔ 반짝이는 보석, 정성껏 가꾼 꽃</text>
      </svg>
    </div>

    <!-- 하이라키 트리 구조 4 -->
    <div class="hierarchy-board">
      <div class="root-node">[Root 4] 〈파랑새〉 핵심 대사 원문 &amp; 41쪽 필수 어휘 하이라키</div>
      <div class="level-1-list">
        <div class="level-1-item">
          <div class="level-1-title">1. 모리스 마테를링크, 〈파랑새〉 (36~37쪽) 핵심 대사 원문 분석 <span class="badge-freq">[빈출]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>[행복의 나라]</b> : “안녕! 우리들은 <b>너희 집에 사는 행복들</b>이야. 나는 <b>건강의 행복! 맑은 공기의 행복! 부모님을 사랑하는 행복! 봄의 행복! 엄마의 행복!</b> ... 우리들은 늘 사람들 곁에 있어. <b>사람들이 그걸 모를 뿐이지.</b>”</div>
            <div class="level-2-item"><b>[잠에서 깬 우리 집 &amp; 결말]</b> : “아, 파랑새다! 그렇게 찾았는데. <b>파랑새가 우리 집에 있었어!</b>” ➔ 이웃집 아픈 소녀에게 선물하여 병이 나음 ➔ 새가 <b>포르르</b> 날아가자 틸틸이 말함: <b>“괜찮아. 내가 또 파랑새를 찾아 줄게. 파랑새는 우리 가까이에 있으니까.”</b></div>
          </div>
        </div>

        <div class="level-1-item">
          <div class="level-1-title">2. 교과서 41쪽 어휘로 마무리 (사전적 의미 완벽 대조)</div>
          <div class="level-2-list">
            <div class="level-2-item"><span class="kw-pill">우러르다</span> : 위를 향해 고개를 쳐들다 &nbsp;|&nbsp; <span class="kw-pill">조잘대다</span> : 낮은 목소리로 빠르게 말하다 &nbsp;|&nbsp; <span class="kw-pill">포르르</span> : 작은 새가 날아오르는 모양</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 5: 3-(2) 〈품사의 종류와 특성〉 — 한 문장 9품사 방사형 브레인스토밍 맵
       ========================================================================= -->
  <div class="page-section">
    <div class="part-banner">[Page 5] 3-(2) 〈품사의 종류와 특성〉 — 한 문장 9품사 올인원 방사형 브레인스토밍 맵 (122~135쪽)</div>

    <!-- [다이어그램 5] 1:1 무축소 viewBox(700x206) + 대형 폰트(15~18px) -->
    <div class="mindmap-container">
      <div class="mindmap-caption">[브레인스토밍 마인드맵 5] 올인원 문장 『앗! 그가 새 옷 둘을 아주 예쁘게 입는다』 9품사 방사형 지도</div>
      <svg viewBox="0 0 700 206" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow5" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#000"/>
          </marker>
        </defs>
        <ellipse cx="350" cy="103" rx="88" ry="50" fill="#fff" stroke="#000" stroke-width="3.5"/>
        <ellipse cx="350" cy="103" rx="81" ry="43" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="8,4"/>
        <text x="350" y="88" font-family="Malgun Gothic" font-size="17.5" font-weight="900" text-anchor="middle">9품사 올인원</text>
        <text x="350" y="110" font-family="Malgun Gothic" font-size="14.5" font-weight="bold" text-anchor="middle">"앗! 그가 새 옷 둘을</text>
        <text x="350" y="130" font-family="Malgun Gothic" font-size="14.5" font-weight="bold" text-anchor="middle">아주 예쁘게 입는다"</text>

        <!-- 1. 좌상단: 체언 -->
        <path d="M 274 80 L 246 44" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow5)"/>
        <rect x="4" y="6" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="30" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">① 체언 (불변어)</text>
        <text x="123" y="53" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">그(대) · 옷(명) · 둘(수사)</text>

        <!-- 2. 좌중단: 수식언 -->
        <path d="M 262 103 L 246 103" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow5)"/>
        <rect x="4" y="74" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="98" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">② 수식언 (불변어)</text>
        <text x="123" y="121" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">새(관형사) · 아주(부사)</text>

        <!-- 3. 좌하단: 독립언 -->
        <path d="M 274 126 L 246 162" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow5)"/>
        <rect x="4" y="142" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="166" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">③ 독립언 (감탄사)</text>
        <text x="123" y="189" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">"앗!" (놀람·느낌·부름·대답)</text>

        <!-- 4. 우상단: 관계언 -->
        <path d="M 426 80 L 454 44" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow5)"/>
        <rect x="458" y="6" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="30" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">④ 관계언 (조사)</text>
        <text x="577" y="53" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">가·을 (예외 가변어: 이다)</text>

        <!-- 5. 우중단: 용언 -->
        <path d="M 438 103 L 454 103" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow5)"/>
        <rect x="458" y="74" width="238" height="58" rx="16" fill="#fff" stroke="#000" stroke-width="3.0"/>
        <text x="577" y="98" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">⑤ 용언 (가변어: 활용)</text>
        <text x="577" y="121" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">예쁘게(형용사)·입는다(동사)</text>

        <!-- 6. 우하단: 품사 3대 기준 -->
        <path d="M 426 126 L 454 162" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow5)"/>
        <rect x="458" y="142" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="166" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">품사 3대 분류 기준 [빈출]</text>
        <text x="577" y="189" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">①형태(2) ➔ ②기능(5) ➔ ③의미(9)</text>
      </svg>
    </div>

    <!-- 하이라키 트리 구조 5 -->
    <div class="hierarchy-board">
      <div class="root-node">[Root 5] 단어(낱말)의 정의 &amp; 품사 3대 분류 기준 하이라키</div>
      <div class="level-1-list">
        <div class="level-1-item">
          <div class="level-1-title">1. 단어(낱말)의 정의와 ‘조사’의 예외적 지위 <span class="badge-trap">[함정]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>기본 원칙</b> : 문장에서 <b>홀로 쓰일 수 있는 말(자립성)</b>을 단어로 인정함</div>
            <div class="level-2-item"><span class="badge-trap">[함정]</span> <b>조사의 단어 인정</b> : <b>‘조사’(`이/가, 을/를, 은/는, 도, 만`)</b>는 홀로 쓰일 수 없으나, 자립할 수 있는 말 뒤에 붙어 <b>쉽게 분리할 수 있으므로 단어로 인정함!</b> (예: `"그가"` = `그` + `가` ➔ <b>2개의 단어!</b>)</div>
          </div>
        </div>

        <div class="level-1-item">
          <div class="level-1-title">2. 품사를 나누는 3대 분류 기준 하이라키 (128~130쪽) <span class="badge-freq">[빈출]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>[기준 1 : 형태]</b> 문장에서 쓰일 때 형태가 변하는가? ➔ <span class="kw-pill">불변어 (형태 불변)</span> vs <span class="kw-pill">가변어 (형태 변화: 활용)</span></div>
            <div class="level-2-item"><b>[기준 2 : 기능]</b> 문장에서 어떤 문법적 구실을 하는가? ➔ <span class="kw-pill">체언 · 용언 · 수식언 · 관계언 · 독립언</span> (5대 기능군)</div>
            <div class="level-2-item"><b>[기준 3 : 의미]</b> 단어 갈래 전체가 공통으로 지닌 의미는 무엇인가? ➔ <span class="kw-pill">명·대·수·동·형·관·부·조·감</span> (9품사)</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 6: 3-(2) 9품사 전체 계통 좌➔우 베지어 가지 분기형 하이라키 맵
       ========================================================================= -->
  <div class="page-section">
    <div class="part-banner">[Page 6] 3-(2) 9품사 전체 계통 (형태 ➔ 5기능 ➔ 9품사) 좌➔우 가지 분기형 하이라키</div>

    <!-- [다이어그램 6] 1:1 무축소 viewBox(700x246) + 대형 폰트(14.5~16.5px) -->
    <div class="mindmap-container">
      <div class="mindmap-caption">[하이라키 가지 맵 6] 9품사 마스터 트리 (불변어 4기능·7품사 vs 가변어 1기능·2품사+예외)</div>
      <svg viewBox="0 0 700 246" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="92" width="104" height="62" rx="10" fill="#f0f0f0" stroke="#000" stroke-width="3"/>
        <text x="54" y="119" font-family="Malgun Gothic" font-size="16.5" font-weight="900" text-anchor="middle">국어 9품사</text>
        <text x="54" y="142" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">5기능·9품사</text>

        <!-- 1. 체언 가지 -->
        <path d="M 106 123 C 116 123, 118 42, 126 42 L 242 42" fill="none" stroke="#000" stroke-width="2.8"/>
        <rect x="124" y="26" width="118" height="32" rx="7" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="48" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">체언 (불변어)</text>

        <path d="M 242 42 C 254 42, 256 18, 264 18 L 698 18" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="13" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">명사 : 구체 대상(집, 사과, 컵) · 추상 대상(사랑, 노력, 희망, 가을)</text>
        <path d="M 242 42 L 698 42" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="37" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">대명사 : 사람(나, 그, 누구) · 사물(이것, 이) · 장소(여기, 거기, 이곳)</text>
        <path d="M 242 42 C 254 42, 256 66, 264 66 L 698 66" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="61" font-family="Malgun Gothic" font-size="14.5" font-weight="900">수사 : 수량(하나, 둘)·순서(첫째) + [함정] 뒤에 조사 결합 가능!</text>

        <!-- 2. 수식언 가지 -->
        <path d="M 106 123 C 116 123, 118 104, 126 104 L 242 104" fill="none" stroke="#000" stroke-width="2.8"/>
        <rect x="124" y="88" width="118" height="32" rx="7" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="110" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">수식언 (불변어)</text>

        <path d="M 242 104 C 254 104, 256 92, 264 92 L 698 92" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="87" font-family="Malgun Gothic" font-size="14.5" font-weight="900">관형사 : 체언만 수식 (새, 헌, 옛, 이, 그, 한, 두) + [함정] 조사 불가!</text>
        <path d="M 242 104 C 254 104, 256 116, 264 116 L 698 116" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="111" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">부사 : 주로 용언 수식 (아주, 참, 꼭꼭, 쌩쌩) + 문장 전체('역시') 수식</text>

        <!-- 3. 관계언 가지 -->
        <path d="M 106 123 C 116 123, 118 145, 126 145 L 242 145" fill="none" stroke="#000" stroke-width="2.8"/>
        <rect x="124" y="129" width="118" height="32" rx="7" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="151" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">관계언 (조사)</text>

        <path d="M 242 145 L 698 145" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="140" font-family="Malgun Gothic" font-size="14.5" font-weight="900">조사 : 관계(가, 를)·뜻 추가(도, 만) / [함정] 서술격 조사 '이다'는 가변어</text>

        <!-- 4. 독립언 가지 -->
        <path d="M 106 123 C 116 123, 118 180, 126 180 L 242 180" fill="none" stroke="#000" stroke-width="2.8"/>
        <rect x="124" y="164" width="118" height="32" rx="7" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="186" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">독립언 (불변어)</text>

        <path d="M 242 180 L 698 180" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="175" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">감탄사 : 놀람·느낌(앗, 우아) · 부름(야, 이봐, 여보게) · 대답(네, 응)</text>

        <!-- 5. 용언 가지 -->
        <path d="M 106 123 C 116 123, 118 220, 126 220 L 242 220" fill="none" stroke="#000" stroke-width="2.8"/>
        <rect x="124" y="204" width="118" height="32" rx="7" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="226" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">용언 (가변어)</text>

        <path d="M 242 220 C 254 220, 256 208, 264 208 L 698 208" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="203" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">동사 : 움직임·작용 (먹다, 입다, 나오다, 되다, 벗다, 돌아가다, 자라다)</text>
        <path d="M 242 220 C 254 220, 256 234, 264 234 L 698 234" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="229" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">형용사 : 성질·상태 (짜다, 빨갛다, 노랗다, 예쁘다, 무뚝뚝하다, 없다)</text>
      </svg>
    </div>

    <!-- 하이라키 트리 구조 6 -->
    <div class="hierarchy-board">
      <div class="root-node">[Root 6] 교과서 129~134쪽 4대 필수 탐구 본문 품사 해부 하이라키</div>
      <div class="level-1-list">
        <div class="level-1-item">
          <div class="level-1-title">1. 교과서 129쪽 분류 예문 &amp; 131쪽 느티나무 대명사 본문 <span class="badge-trap">[함정]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><span class="badge-trap">[함정]</span> <b>129쪽 예문</b> : <b>“준수가 빨간 자두와 노란 참외를 둘 다 먹었다.”</b> ➔ <b>`빨간`(빨갛다), `노란`(노랗다)</b>은 자두·참외를 꾸며 주지만 어미가 변하는 <b>[형용사]</b>임! (`둘`=수사)</div>
            <div class="level-2-item"><b>131쪽 느티나무 본문 대명사 지시 대상</b> : <b>`이것`</b>(느티나무: 사물) / <b>`누가`</b>(모르는 사람) / <b>`그`</b>(한 노인: 사람) / <b>`이곳`</b>(느티나무 자리: 장소) / <b>`거기`</b>(정원: 장소)</div>
          </div>
        </div>

        <div class="level-1-item">
          <div class="level-1-title">2. 교과서 133쪽 폴 세잔 정물화 &amp; 134쪽 양귀자 소설 본문 <span class="badge-freq">[빈출]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>133쪽 폴 세잔 본문</b> : `하나의 장면`(`하나`=조사 `의` 결합 ➔ <b>수사!</b>) / <b>`이는 매우 독창적인 방법`</b>(`이`=보조사 `는` 결합 ➔ 관형사가 아니라 <b>대명사!</b>)</div>
            <div class="level-2-item"><b>134쪽 양귀자 〈길모퉁이에서 만난 사람〉</b> : 동사 5개(<span class="kw-pill">나와서, 되면, 벗고, 돌아간다, 나누는</span>) vs 형용사 4개(<span class="kw-pill">무뚝뚝하고, 뻣뻣하다, 싱거운, 없다</span>)</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 7: 3-(2) 동사 vs 형용사 판별 & 3대 함정 클리닉 좌➔우 가지 하이라키 맵
       ========================================================================= -->
  <div class="page-section">
    <div class="part-banner">[Page 7] 3-(2) 동사 vs 형용사 1초 판별 저울 &amp; 144쪽 어법 오류 클리닉 하이라키</div>

    <!-- [다이어그램 7] 1:1 무축소 viewBox(700x234) + 대형 폰트(14.5~16.5px) -->
    <div class="mindmap-container">
      <div class="mindmap-caption">[하이라키 가지 맵 7] 시험 출제율 100% 『동사 vs 형용사 판별법』 및 『3대 함정 비교』 트리</div>
      <svg viewBox="0 0 700 234" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="86" width="104" height="62" rx="10" fill="#f0f0f0" stroke="#000" stroke-width="3"/>
        <text x="54" y="113" font-family="Malgun Gothic" font-size="16.5" font-weight="900" text-anchor="middle">품사 킬러 함정</text>
        <text x="54" y="136" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">판별·어법교정</text>

        <!-- 1차 가지 1: 동사 vs 형용사 -->
        <path d="M 106 117 C 116 117, 118 45, 126 45 L 242 45" fill="none" stroke="#000" stroke-width="3"/>
        <rect x="124" y="28" width="118" height="34" rx="8" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="51" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">동사 vs 형용사</text>

        <path d="M 242 45 C 254 45, 256 19, 264 19 L 698 19" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="14" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">① 현재(-ㄴ다/-는다) : 간다·나무가 큰다(동사O) vs 예쁜다X·없는다X(형용사)</text>
        <path d="M 242 45 L 698 45" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="40" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">② 명령형(-아라/-어라) : 가라!·먹어라!(동사O) vs 커라!X·예뻐라!X(형용사)</text>
        <path d="M 242 45 C 254 45, 256 71, 264 71 L 698 71" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="66" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">③ 청유형(-자) : 가자·먹자(동사O) vs 손이 크자X·마음이 예쁘자X(형용사)</text>

        <!-- 1차 가지 2: 체언 vs 관형사 -->
        <path d="M 106 117 L 242 117" fill="none" stroke="#000" stroke-width="3"/>
        <rect x="124" y="100" width="118" height="34" rx="8" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="123" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">체언 vs 관형사</text>

        <path d="M 242 117 C 254 117, 256 104, 264 104 L 698 104" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="99" font-family="Malgun Gothic" font-size="14.5" font-weight="900">조사 결합 : "둘을/하나의"(수사: 조사O) vs "두 사람/한 장면"(관형사: 조사X)</text>
        <path d="M 242 117 C 254 117, 256 132, 264 132 L 698 132" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="127" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">지시어 구별 : "그는(대명사) 그(관형사) 책" / "이는(대명사)" vs "이(관형사) 책"</text>

        <!-- 1차 가지 3: 144쪽 오류 3종 -->
        <path d="M 106 117 C 116 117, 118 190, 126 190 L 242 190" fill="none" stroke="#000" stroke-width="3"/>
        <rect x="124" y="173" width="118" height="34" rx="8" fill="#fff" stroke="#000" stroke-width="2.2"/>
        <text x="183" y="196" font-family="Malgun Gothic" font-size="15.5" font-weight="900" text-anchor="middle">144쪽 오류 3종</text>

        <path d="M 242 190 C 254 190, 256 164, 264 164 L 698 164" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="159" font-family="Malgun Gothic" font-size="14.5" font-weight="900">① "옛부터 내려온"(X) ➔ 관형사 '옛' 조사 불가 ➔ "옛날부터/예로부터"(O)</text>
        <path d="M 242 190 L 698 190" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="185" font-family="Malgun Gothic" font-size="14.5" font-weight="900">② "마음이 예쁘자"(X) ➔ 형용사 청유형 불가 ➔ "마음을 예쁘게 가꾸자"(O)</text>
        <path d="M 242 190 C 254 190, 256 216, 264 216 L 698 216" fill="none" stroke="#000" stroke-width="2"/>
        <text x="268" y="211" font-family="Malgun Gothic" font-size="14.5" font-weight="bold">③ "놀이터 주차 금지... 그곳에 주차"(X) ➔ 지시 모순 ➔ "다른 곳에 주차"(O)</text>
      </svg>
    </div>

    <!-- 하이라키 트리 구조 7 -->
    <div class="hierarchy-board">
      <div class="root-node">[Root 7] 동사·형용사 겸용 단어(`크다·밝다`) &amp; 144쪽 어법 오류 정밀 클리닉</div>
      <div class="level-1-list">
        <div class="level-1-item">
          <div class="level-1-title">1. 문맥에 따라 품사가 달라지는 다의어 판별 (`크다` · `밝다`) <span class="badge-trap">[함정]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>‘크다’의 두 얼굴</b> : <b>“나무가 쑥쑥 큰다(`-ㄴ다` 결합 O / 자라다)” ➔ [동사]</b> vs <b>“형은 키가 크다(`키가 큰다` X / 상태)” ➔ [형용사]</b></div>
            <div class="level-2-item"><b>‘밝다’의 두 얼굴</b> : <b>“동창이 밝는다(`-는다` 결합 O / 날이 새다)” ➔ [동사]</b> vs <b>“달빛이 매우 밝다(`달빛이 밝는다` X / 상태)” ➔ [형용사]</b></div>
          </div>
        </div>

        <div class="level-1-item">
          <div class="level-1-title">2. 교과서 144쪽 실전 국어 자료 어법 오류 3종 서술형 완벽 대비 <span class="badge-trap">[함정]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>[신문 기사 헤드라인] “옛부터 전해 내려온”</b> ➔ `옛`은 체언만 꾸미는 <b>관형사</b>라 조사(`부터`) 결합 불가 ➔ <b>“옛날부터 / 예로부터”</b>로 교정</div>
            <div class="level-2-item"><b>[나의 좌우명] “항상 마음이 예쁘자.”</b> ➔ `예쁘다`는 <b>형용사</b>라 청유형 어미(`-자`) 결합 불가 ➔ <b>“항상 마음을 예쁘게 가꾸자(예뻐지자)”</b>로 교정</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- =========================================================================
       PAGE 8: 3-(2) 실전 담화 (달 샤베트 vs 재난 문자) & 148쪽 연설가 4인 마인드맵
       ========================================================================= -->
  <div class="page-section">
    <div class="part-banner">[Page 8] 3-(2) 담화별 품사 효과 (《달 샤베트》 vs 안전 문자) &amp; 148쪽 연설문 브레인스토밍</div>

    <!-- [다이어그램 8] 1:1 무축소 viewBox(700x206) + 대형 폰트(15~18px) -->
    <div class="mindmap-container">
      <div class="mindmap-caption">[브레인스토밍 마인드맵 8] 글의 갈래와 목적에 따른 품사 선택의 효과 (145~148쪽)</div>
      <svg viewBox="0 0 700 206" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="arrow8" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 9 5 L 0 9 z" fill="#000"/>
          </marker>
        </defs>
        <ellipse cx="350" cy="103" rx="84" ry="48" fill="#fff" stroke="#000" stroke-width="3.5"/>
        <ellipse cx="350" cy="103" rx="77" ry="41" fill="none" stroke="#000" stroke-width="1.5" stroke-dasharray="8,4"/>
        <text x="350" y="96" font-family="Malgun Gothic" font-size="18" font-weight="900" text-anchor="middle">담화·연설문 속</text>
        <text x="350" y="121" font-family="Malgun Gothic" font-size="18" font-weight="900" text-anchor="middle">품사 사용 효과</text>

        <!-- 1. 좌상단: 달 샤베트 -->
        <path d="M 276 80 L 246 44" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow8)"/>
        <rect x="4" y="6" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="30" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">《달 샤베트》 [빈출]</text>
        <text x="123" y="53" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">부사(꼭꼭·쌩쌩) ➔ 생생한 느낌</text>

        <!-- 2. 좌중단: 안전 안내 문자 -->
        <path d="M 266 103 L 246 103" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow8)"/>
        <rect x="4" y="74" width="238" height="58" rx="16" fill="#fff" stroke="#000" stroke-width="3.0"/>
        <text x="123" y="98" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">안전 안내 문자 [빈출]</text>
        <text x="123" y="121" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">명사 중심 ➔ 신속·정확·간결</text>

        <!-- 3. 좌하단: 부사 남발 함정 -->
        <path d="M 276 126 L 246 162" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow8)"/>
        <rect x="4" y="142" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="123" y="166" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">[함정] 재난 문자에 부사</text>
        <text x="123" y="189" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">신속성 저하 · 공식 신뢰도 하락</text>

        <!-- 4. 우상단: 백범 김구 & 스티브 잡스 -->
        <path d="M 424 80 L 454 44" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow8)"/>
        <rect x="458" y="6" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="30" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">김구(명사) · 잡스(형용사)</text>
        <text x="577" y="53" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">독립 의지 강조 / 감정에 호소</text>

        <!-- 5. 우중단: 말랄라 -->
        <path d="M 434 103 L 454 103" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow8)"/>
        <rect x="458" y="74" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="98" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">말랄라 (동사·추상명사)</text>
        <text x="577" y="121" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">파괴되다 / 권리·교육 보장 촉구</text>

        <!-- 6. 우하단: 스파르시 샤 -->
        <path d="M 424 126 L 454 162" fill="none" stroke="#000" stroke-width="2.8" marker-end="url(#arrow8)"/>
        <rect x="458" y="142" width="238" height="58" rx="16" fill="#f5f5f5" stroke="#000" stroke-width="2.6"/>
        <text x="577" y="166" font-family="Malgun Gothic" font-size="17" font-weight="900" text-anchor="middle">스파르시 샤 (수사 제시)</text>
        <text x="577" y="189" font-family="Malgun Gothic" font-size="15" font-weight="bold" text-anchor="middle">십오·백삼십 ➔ 사실성·설득력</text>
      </svg>
    </div>

    <!-- 하이라키 트리 구조 8 -->
    <div class="hierarchy-board">
      <div class="root-node">[Root 8] 교과서 145~148쪽 그림책 · 재난 문자 · 연설문 4종 본문 하이라키</div>
      <div class="level-1-list">
        <div class="level-1-item">
          <div class="level-1-title">1. 그림책 《달 샤베트》 vs 폭염 안전 안내 문자 품사 대비 (145~146쪽) <span class="badge-freq">[빈출]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>[본문 1] 백희나, 《달 샤베트》</b> : “<b>아주아주</b> 무더운 여름날 밤... <b>너무너무</b> 더워서... 창문을 <b>꼭꼭</b> 닫고, 에어컨을 <b>쌩쌩</b>, 선풍기를 <b>씽씽</b> 틀며... 커다란 달이 <b>똑똑</b> 녹아내리고 있었습니다.” ➔ <b>[부사(음성 상징어)]</b> 집중 사용으로 장면을 <b>생생하고 실감 나게</b> 전달함</div>
            <div class="level-2-item"><b>[본문 2] 폭염 안전 안내 문자</b> : “안전 안내, 오늘 10시 <b>폭염</b> 예정, 낮 동안 <b>외출 자제</b>, <b>물놀이</b> 안전 <b>유의</b> 바람.” ➔ 수식언을 빼고 <b>[명사]</b> 중심으로 써서 긴급 정보를 <b>신속·정확·간결하게</b> 전달함 (<span class="badge-trap">[함정]</span> 부사 남발 시 신뢰도 하락!)</div>
          </div>
        </div>

        <div class="level-1-item">
          <div class="level-1-title">2. 세상을 움직인 연설가 4인의 품사 전략 (148쪽) <span class="badge-freq">[빈출]</span></div>
          <div class="level-2-list">
            <div class="level-2-item"><b>① 백범 김구</b> : `독립, 우리나라, 민족` 등 <b>[명사] 반복</b> ➔ 자주독립 의지 강조 &nbsp;|&nbsp; <b>② 스티브 잡스</b> : `대단한, 멋진` 등 <b>[형용사] 다수</b> ➔ 감정에 호소·도전 격려</div>
            <div class="level-2-item"><b>③ 말랄라</b> : `파괴되다` <b>[동사]</b> + `권리, 교육` <b>[추상 명사]</b> ➔ 교육권 보장 촉구 &nbsp;|&nbsp; <b>④ 스파르시 샤</b> : `십오(년), 백삼십(번)` <b>[수사] 제시</b> ➔ 사실성·설득력 확보</div>
          </div>
        </div>
      </div>
    </div>
  </div>

</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[1] Saved HTML: {html_path} ({os.path.getsize(html_path)} bytes)")

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
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        # shutil.copy2(pdf_path, root_pdf_path)
        doc = fitz.open(pdf_path)
        print(f"[2] Generated PDF: {pdf_path} ({len(doc)} pages)")
        preview_dir = r'C:\Users\kkj\.gemini\antigravity\brain\f75f4039-dfb5-40ea-b50b-f93f45c08126'
        os.makedirs(preview_dir, exist_ok=True)
        # Save cropped diagram 1 & diagram 2 previews
        page1 = doc[0]
        rect1 = fitz.Rect(20, 95, 575, 345)
        pix1 = page1.get_pixmap(dpi=200, clip=rect1)
        pix1.save(os.path.join(preview_dir, 'diagram1_v3_crop.png'))
        page2 = doc[1]
        rect2 = fitz.Rect(20, 45, 575, 315)
        pix2 = page2.get_pixmap(dpi=200, clip=rect2)
        pix2.save(os.path.join(preview_dir, 'diagram2_v3_crop.png'))
        doc.close()
    else:
        print("PDF generation failed:", res.stderr.decode('utf-8', errors='ignore'))

if __name__ == '__main__':
    generate_brainstorming_summary_v3()
