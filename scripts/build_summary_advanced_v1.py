import os
import subprocess
import fitz

def generate_advanced_summary_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if os.path.basename(base_dir) == 'scripts':

        base_dir = os.path.dirname(base_dir)
    summary_dir = os.path.join(base_dir, '요약')
    os.makedirs(summary_dir, exist_ok=True)

    html_path = os.path.join(summary_dir, '3-2단원_품사_교과서외_심화문법_요약_v1.html')
    pdf_path = os.path.join(summary_dir, '3-2단원_품사_교과서외_심화문법_요약_v1.pdf')

    html_content = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>[학교 학습지 심화 특강] 3-(2) 품사의 세부 갈래와 심화 문법 요약 (교과서 외 100% 대비) [v1]</title>
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
    line-height: 1.62;
    letter-spacing: 0.12px;
    font-size: 8.7pt;
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
    font-size: 13.0pt;
    font-weight: bold;
    text-align: center;
    margin: 0 0 2px 0;
    letter-spacing: 0.2px;
  }
  .header-info-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.0pt;
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

  /* 개관 박스 */
  .intro-box {
    border: 1.2px solid #333;
    background-color: #f9f9f9;
    padding: 4px 8px;
    margin-bottom: 4px;
    font-size: 8.2pt;
    line-height: 1.58;
    letter-spacing: 0.1px;
  }

  /* 섹션 제목 (대주제) */
  .section-title {
    background-color: #000;
    color: #fff;
    font-size: 9.1pt;
    font-weight: bold;
    padding: 2.2px 6px;
    margin: 4px 0 3px 0;
    border-radius: 2px;
    break-after: avoid;
    letter-spacing: 0.12px;
  }

  /* 소제목 */
  .sub-title {
    font-size: 8.7pt;
    font-weight: bold;
    color: #111;
    margin: 3px 0 2px 0;
    padding-left: 4px;
    border-left: 3.5px solid #000;
    line-height: 1.35;
  }

  /* 표준 테이블 스타일 */
  table.data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.1pt;
    margin-bottom: 4px;
    letter-spacing: 0.08px;
    line-height: 1.48;
  }
  table.data-table th, table.data-table td {
    border: 1px solid #555;
    padding: 2.5px 5px;
  }
  table.data-table th {
    background-color: #eaeaea;
    font-weight: bold;
    text-align: center;
    color: #000;
  }
  table.data-table td.center {
    text-align: center;
  }
  table.data-table td.category {
    background-color: #f5f5f5;
    font-weight: bold;
    text-align: center;
    width: 17%;
  }

  /* 함정 클리닉 박스 */
  .trap-box {
    border: 1.2px dashed #000;
    background-color: #f7f7f7;
    padding: 3.5px 7px;
    margin: 3px 0 4px 0;
    font-size: 8.15pt;
    line-height: 1.52;
  }
  .trap-badge {
    background-color: #000;
    color: #fff;
    font-weight: bold;
    font-size: 7.6pt;
    padding: 1px 4px;
    border-radius: 2px;
    margin-right: 4px;
  }

  /* 하이라이트 배지 */
  .key-badge {
    display: inline-block;
    border: 1px solid #000;
    background-color: #eaeaea;
    font-weight: bold;
    padding: 0 3px;
    border-radius: 2px;
    margin: 0 1px;
    font-size: 7.9pt;
  }

  /* 페이지 브레이크 */
  .page-break {
    page-break-before: always;
    break-before: page;
  }

  /* 페이지 컨테이너 */
  .page-container {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
</head>
<body>

  <!-- ================= [ 1페이지 시작 ] ================= -->
  <div class="page-container">
    <div>
      <!-- 1. 표제부 -->
      <div class="header-box">
        <div class="header-title">[학교 학습지 심화 특강] 3-(2) 품사의 세부 갈래와 심화 문법 요약</div>
        <table class="header-info-table">
          <tr>
            <td class="label">대상 학년</td>
            <td>중1 (2026학년도 2학기 중간대비)</td>
            <td class="label">원천 자료</td>
            <td>남서울중 1학년 국어 학습지 (2페이지 심화)</td>
            <td class="label">성격 규정</td>
            <td><b>교과서 미수록 학교별 단골 킬러 문법 총정리</b></td>
          </tr>
        </table>
      </div>

      <!-- 2. 기획 개관 박스 -->
      <div class="intro-box">
        <b>[출제 배경 및 학습 전략]</b> 미래엔 교과서 본문은 9품사의 5기능과 기본 정의까지만 다루지만, 실제 학교 현장에서는 <b>내신 변별력 확보를 위해 중2~고1 수준의 9품사 세부 하위 분류</b>를 학습지로 배부하여 시험에 출제합니다. 본 문서는 <b>교과서에 없지만 시험장에서 오답률 1위를 기록하는 학습지 단독 문법</b>을 100% 압축 정리한 필수 정복서입니다.
      </div>

      <!-- 3. 체언의 심화 분류 -->
      <div class="section-title">1. [체언의 심화 분류] 명사 · 대명사 · 수사의 세부 하위 갈래 (교과서 외 100% 출제)</div>

      <div class="sub-title">1) 명사(名詞)의 3대 세부 분류 체계</div>
      <table class="data-table">
        <tr>
          <th style="width: 18%;">분류 기준</th>
          <th style="width: 18%;">세부 갈래</th>
          <th>개념 정의 및 특징</th>
          <th style="width: 32%;">대표 예시 단어</th>
        </tr>
        <tr>
          <td class="center" rowspan="2"><b>구체성 유무</b></td>
          <td class="center"><b>구체 명사</b></td>
          <td>구체적인 모양이나 형체가 있어 감각으로 인지할 수 있는 대상</td>
          <td>나무, 하늘, 집, 자동차, 연필, 책</td>
        </tr>
        <tr>
          <td class="center"><b>추상 명사</b></td>
          <td>물리적 형체 없이 머릿속 생각, 감정, 상태, 개념을 나타내는 대상</td>
          <td>우정, 행복, 노력, 희망, 사랑, 평화</td>
        </tr>
        <tr>
          <td class="center" rowspan="2"><b>사용 범위</b></td>
          <td class="center"><b>고유 명사</b></td>
          <td>특정한 인물, 지명, 기관 등 유일무이한 대상에만 붙여진 독점적 이름</td>
          <td>이순신, 신사임당, 부산, 대한민국, 한글</td>
        </tr>
        <tr>
          <td class="center"><b>보통 명사</b></td>
          <td>같은 특성을 지닌 일반 대상들에 두루 통용되어 쓰이는 이름</td>
          <td>과일, 사람, 동물, 꽃, 책상, 학생</td>
        </tr>
        <tr>
          <td class="center" rowspan="2"><b>자립성 유무<br>(★ 최다 빈출)</b></td>
          <td class="center"><b>자립 명사</b></td>
          <td>다른 말의 도움을 받지 않고 문장에서 단독으로 쓰일 수 있는 명사</td>
          <td>어머니, 바다, 친구, 하늘, 나무</td>
        </tr>
        <tr>
          <td class="center"><b>의존 명사</b></td>
          <td><b>반드시 앞말(관형어)의 꾸밈을 받아야만</b> 문장에 쓰일 수 있는 불완전 체언</td>
          <td>먹을 <b>것</b>, 한 <b>명</b>, 두 <b>개</b>, 갈 <b>수</b> 있다</td>
        </tr>
      </table>

      <div class="trap-box">
        <span class="trap-badge">[함정] 의존 명사 vs 조사·접미사 완벽 판별</span>
        ① <b>띄어쓰기 원칙</b>: 의존 명사는 엄연한 '단어(체언)'이므로 <b>앞말과 반드시 띄어 씀</b> (예: <code>먹을 V 것</code>, <code>사과 V 세 V 개</code>).<br>
        ② <b>조사 결합 가능</b>: 뒤에 조사가 자유롭게 결합할 수 있음 (예: <code>아는 것<b>이</b> 힘이다</code>, <code>갈 수<b>가</b> 없다</code>, <code>두 개<b>를</b> 샀다</code>).
      </div>

      <div class="sub-title">2) 대명사 · 수사의 세부 분류</div>
      <table class="data-table">
        <tr>
          <th style="width: 15%;">품사</th>
          <th style="width: 20%;">세부 갈래</th>
          <th>개념 정의</th>
          <th style="width: 40%;">대표 예시 단어</th>
        </tr>
        <tr>
          <td class="center" rowspan="2"><b>대명사</b></td>
          <td class="center"><b>인칭 대명사</b></td>
          <td><b>사람의 이름</b>을 대신하여 가리킴</td>
          <td>• 1인칭: 나, 저, 우리 / 2인칭: 너, 당신, 여러분<br>• 3인칭: 그, 그이, 저분, 그분</td>
        </tr>
        <tr>
          <td class="center"><b>지시 대명사</b></td>
          <td><b>사물이나 장소, 방향</b>을 대신 가리킴</td>
          <td>• 사물: 이것, 그것, 저것, 무엇<br>• 장소: 여기, 저기, 거기, 어디</td>
        </tr>
        <tr>
          <td class="center" rowspan="2"><b>수사</b></td>
          <td class="center"><b>양수사 (量數詞)</b></td>
          <td>사물의 <b>수량(개수, 분량)</b>을 나타냄</td>
          <td>하나, 둘, 셋, 넷, 일, 이, 삼, 백, 천</td>
        </tr>
        <tr>
          <td class="center"><b>서수사 (序數詞)</b></td>
          <td>사물의 <b>순서(차례)</b>를 나타냄</td>
          <td>첫째, 둘째, 셋째, 제일(第一), 제이(第二)</td>
        </tr>
      </table>

      <!-- 4. 관계언의 심화 분류 -->
      <div class="section-title">2. [관계언의 심화 분류] 조사의 3대 갈래 체계 (격조사 · 접속조사 · 보조사)</div>
      <table class="data-table">
        <tr>
          <th style="width: 17%;">조사의 종류</th>
          <th style="width: 25%;">핵심 역할 및 문법적 특성</th>
          <th style="width: 28%;">대표 조사 목록</th>
          <th>실전문장 적용 분석</th>
        </tr>
        <tr>
          <td class="center"><b>격조사</b><br>(문장성분 자격)</td>
          <td>체언 뒤에 붙어 그 말이 문장 안에서 <b>일정한 문법적 자격(문장 성분)</b>을 갖추도록 결정함</td>
          <td>• <b>주격</b>: 이/가, 께서<br>• <b>목적격</b>: 을/를<br>• <b>관형격</b>: 의<br>• <b>부사격</b>: 에, 에서, 에게, 로<br>• <b>서술격</b>: -이다 (가변어)</td>
          <td>• 봄<b>이</b> 왔다. (주어 자격)<br>• 책<b>을</b> 읽는다. (목적어 자격)<br>• 형<b>의</b> 옷 (관형어 자격)<br>• 마당<b>에서</b> 논다. (부사어 자격)<br>• 그는 학생<b>이다</b>. (서술어 자격)</td>
        </tr>
        <tr>
          <td class="center"><b>접속조사</b><br>(대등한 연결)</td>
          <td>두 단어를 <b>대등한 자격</b>으로 직접 이어 주는 구실을 함</td>
          <td><b>과/와, 하고, (이)랑</b></td>
          <td>• 사과<b>와</b> 배를 먹었다.<br>• 너<b>하고</b> 나랑 함께 가자.</td>
        </tr>
        <tr>
          <td class="center"><b>보조사</b><br>(특별한 뜻 첨가)<br><b>(★ 킬러 함정)</b></td>
          <td>체언 등에 붙어 <b>특별한 의미(뉘앙스)를 덧붙여 주는</b> 조사 (문장 성분 자격 부여 X)</td>
          <td>• <b>은/는</b> (대조, 화제)<br>• <b>도</b> (포함, 역시)<br>• <b>만</b> (단독, 유일)<br>• <b>마저/조차</b> (극한, 마지노선)</td>
          <td>• 형<b>은</b> 크고 동생<b>은</b> 작다. (대조)<br>• 나<b>도</b> 그 비밀을 안다. (포함)<br>• 오직 너<b>만</b> 믿는다. (유일)<br>• 마지막 희망<b>마저</b> 사라졌다.</td>
        </tr>
      </table>

      <div class="trap-box">
        <span class="trap-badge">[함정] 격조사 vs 보조사 구별 1초 판별법</span>
        ① <b>'은/는'은 주격 조사가 아니라 [보조사]이다!</b> (학교 시험 1순위 함정). 국어의 주격 조사는 오직 <code>이/가</code>, <code>께서</code>뿐임.<br>
        ② 격조사는 단순 문법적 자격만 주지만, 보조사는 문맥에 <b>'대조/포함/단독' 등의 특별한 뉘앙스</b>를 형성함.
      </div>
    </div>
  </div>
  <!-- ================= [ 1페이지 끝 ] ================= -->

  <div class="page-break"></div>

  <!-- ================= [ 2페이지 시작 ] ================= -->
  <div class="page-container">
    <div>
      <!-- 5. 수식언의 심화 분류 -->
      <div class="section-title">3. [수식언의 심화 분류] 관형사 · 부사의 세부 갈래 (성분 부사 vs 문장 부사)</div>

      <div class="sub-title">1) 관형사(冠形詞)의 세부 분류: 성상 · 지시 · 수 관형사</div>
      <table class="data-table">
        <tr>
          <th style="width: 20%;">세부 갈래</th>
          <th>개념 정의 및 수식 방식</th>
          <th style="width: 45%;">대표 예시 단어 및 쓰임</th>
        </tr>
        <tr>
          <td class="center"><b>성상 관형사</b></td>
          <td>사물의 <b>성질이나 상태</b>를 구체적으로 규정하며 체언을 꾸밈</td>
          <td><b>새</b> 옷, <b>헌</b> 신발, <b>옛</b> 추억, <b>온갖</b> 정성, <b>순</b> 우리말</td>
        </tr>
        <tr>
          <td class="center"><b>지시 관형사</b></td>
          <td>특정한 대상을 <b>가리키며(지시하며)</b> 체언을 꾸밈</td>
          <td><b>이</b> 책, <b>그</b> 사람, <b>저</b> 산, <b>무슨</b> 일, <b>어느</b> 마을, <b>딴</b> 생각</td>
        </tr>
        <tr>
          <td class="center"><b>수 관형사</b></td>
          <td>뒤에 오는 명사의 <b>수량이나 순서</b>를 매김 (조사 결합 절대 불가)</td>
          <td><b>한</b> 명, <b>두</b> 개, <b>세</b> 사람, <b>첫째</b> 아들, <b>여러</b> 나라</td>
        </tr>
      </table>

      <div class="sub-title">2) 부사(副詞)의 세부 분류: 성분 부사 vs 문장 부사</div>
      <table class="data-table">
        <tr>
          <th style="width: 17%;">상위 분류</th>
          <th style="width: 18%;">하위 갈래</th>
          <th>개념 정의 및 기능</th>
          <th style="width: 38%;">대표 예시 단어 및 적용 문장</th>
        </tr>
        <tr>
          <td class="center" rowspan="3"><b>성분 부사</b><br>(문장 특정 성분 수식)</td>
          <td class="center"><b>성상 부사</b></td>
          <td>용언 등의 모양, 상태, 성질, 정도를 구체적으로 한정함</td>
          <td>꽃이 <b>활짝</b> 피었다. <b>매우</b> 빠르다. <b>잘</b> 달린다.</td>
        </tr>
        <tr>
          <td class="center"><b>지시 부사</b></td>
          <td>장소, 시간, 앞서 나온 이야기 사실을 가리키며 꾸밈</td>
          <td><b>이리</b> 오너라. <b>그리</b> 가거라. <b>오늘</b> 떠난다.</td>
        </tr>
        <tr>
          <td class="center"><b>부정 부사</b></td>
          <td>용언 바로 앞에서 그 동작이나 상태를 부정함</td>
          <td>밥을 <b>못</b> 먹었다. 학교에 <b>안(아니)</b> 간다.</td>
        </tr>
        <tr>
          <td class="center" rowspan="2"><b>문장 부사</b><br>(문장 전체 수식)</td>
          <td class="center"><b>양태 부사</b></td>
          <td><b>말하는 이의 심리적 태도나 판단</b>을 문장 전체에 부여함</td>
          <td><b>설마</b> 그럴까? <b>과연</b> 명불허전이다. <b>제발</b> 도와줘.</td>
        </tr>
        <tr>
          <td class="center"><b>접속 부사</b></td>
          <td>단어와 단어, 앞 문장과 뒤 문장을 논리적으로 이어 줌</td>
          <td>봄이 왔다. <b>그리고</b> 꽃이 피었다. / <b>그러나</b>, <b>곧</b></td>
        </tr>
      </table>

      <!-- 6. 용언 및 독립언의 심화 분류 -->
      <div class="section-title">4. [용언 · 독립언의 심화 분류] 자동사/타동사 & 성상/지시 형용사 & 감탄사의 갈래</div>
      <table class="data-table">
        <tr>
          <th style="width: 12%;">품사</th>
          <th style="width: 18%;">세부 갈래</th>
          <th>개념 정의 및 판별 핵심</th>
          <th style="width: 38%;">대표 예시 단어</th>
        </tr>
        <tr>
          <td class="center" rowspan="2"><b>동사</b></td>
          <td class="center"><b>자동사 (自動詞)</b></td>
          <td>동작이 주어 자신에게만 미침 (<b>목적어 '을/를' 불필요</b>)</td>
          <td>새가 <b>날다</b>, 꽃이 <b>피다</b>, 집에 <b>가다</b>, 바람이 <b>불다</b></td>
        </tr>
        <tr>
          <td class="center"><b>타동사 (他動詞)</b></td>
          <td>동작이 다른 대상에 미침 (<b>반드시 목적어 '을/를' 필요</b>)</td>
          <td>옷을 <b>입는다</b>, 책을 <b>본다</b>, 물을 <b>마시다</b>, 밥을 <b>먹다</b></td>
        </tr>
        <tr>
          <td class="center" rowspan="2"><b>형용사</b></td>
          <td class="center"><b>성상 형용사</b></td>
          <td>대상의 성질이나 상태를 직접 나타냄</td>
          <td>마음이 <b>착하다</b>, 방이 <b>넓다</b>, 눈이 <b>하얗다</b>, 물이 <b>맑다</b></td>
        </tr>
        <tr>
          <td class="center"><b>지시 형용사</b></td>
          <td>성질·상태·시간 등이 어떠하다는 것을 대신 가리킴</td>
          <td>성격이 <b>이러하다</b>, 모양이 <b>그러하다</b>, 처지가 <b>저러하다</b></td>
        </tr>
        <tr>
          <td class="center"><b>감탄사</b></td>
          <td class="center"><b>놀람 / 부름 / 대답</b></td>
          <td>느낌·놀람 / 부름 / 대답의 세 갈래로 독립적으로 쓰임</td>
          <td>• 놀람: <b>앗, 어머, 아차</b> / • 부름: <b>야, 여보세요</b> / • 대답: <b>네, 아니요</b></td>
        </tr>
      </table>

      <!-- 7. 교과서 밖 심화 3대 판별 공식 클리닉 -->
      <div class="section-title">5. [실전 킬러 문항 정복] 교과서 외 심화 3대 문법 판별 클리닉</div>
      <table class="data-table">
        <tr>
          <th style="width: 25%;">킬러 함정 유형</th>
          <th style="width: 35%;">1초 판별 기준 및 공식</th>
          <th>실전 적용 및 오류 교정 사례</th>
        </tr>
        <tr>
          <td class="center"><b>[클리닉 1]<br>수사 vs 수 관형사</b></td>
          <td>뒤에 <b>조사가 붙을 수 있으면 ➔ [수사]</b><br>뒤에 <b>명사를 꾸미고 조사 불가 ➔ [수 관형사]</b></td>
          <td>• 사과 <b>둘을</b> 먹었다. (수사 '둘' + 목적격 조사 '을')<br>• 사과 <b>두</b> 개를 먹었다. (명사 '개'를 꾸미는 수 관형사 '두')</td>
        </tr>
        <tr>
          <td class="center"><b>[클리닉 2]<br>자동사 vs 타동사</b></td>
          <td>목적격 조사 <b>'을/를'을 넣어서 성립하면 ➔ [타동사]</b><br>목적격 조사 <b>'을/를' 결합이 불가능하면 ➔ [자동사]</b></td>
          <td>• 밥<b>을</b> 먹는다(O), 책<b>을</b> 읽는다(O) ➔ 먹다, 읽다는 <b>타동사</b><br>• 하늘<b>을</b> 솟는다(X), 꽃<b>을</b> 핀다(X) ➔ 솟다, 피다는 <b>자동사</b></td>
        </tr>
        <tr>
          <td class="center"><b>[클리닉 3]<br>자립 명사 vs 의존 명사</b></td>
          <td>문장 첫머리에 <b>홀로 쓰일 수 있으면 ➔ [자립 명사]</b><br>앞말(관형어) 꾸밈 없이 <b>홀로 쓰이지 못하면 ➔ [의존 명사]</b></td>
          <td>• <b>친구</b>가 집에 놀러 왔다. ('친구'는 단독 성립 ➔ 자립 명사)<br>• (X) "것이 좋다" ➔ (O) "<b>먹을</b> 것이 좋다" ('것'은 의존 명사)</td>
        </tr>
      </table>

      <!-- 시험 직전 30초 체크포인트 -->
      <div class="intro-box" style="margin-top: 4px; background-color: #f5f5f5; border: 1.5px solid #000;">
        <b>[시험 직전 30초 체크포인트]</b><br>
        ① <b>조사 판별</b>: <code>이/가</code>는 주격 조사(격조사), <code>은/는</code>은 대조를 나타내는 <b>보조사</b>이다!<br>
        ② <b>의존 명사</b>: <code>것, 수, 개, 명, 줄, 리</code>는 혼자 못 쓰이지만 엄연한 명사이므로 <b>앞말과 띄어 쓴다!</b><br>
        ③ <b>부사의 종류</b>: <code>설마, 과연, 제발, 결코</code>는 문장 전체를 수식하는 <b>문장 부사(양태 부사)</b>이다!
      </div>
    </div>
  </div>
  <!-- ================= [ 2페이지 끝 ] ================= -->

</body>
</html>
"""

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"[1] Saved Advanced Summary HTML: {html_path} ({os.path.getsize(html_path)} bytes)")

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
    generate_advanced_summary_pdf()
