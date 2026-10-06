---
name: sns-cardnews-build
description: >
  [TLDR] sns-cardnews 스위트의 빌드 하위 스킬. slides.md(확정 카피)와 design-brief.md
  (디자인 지시)를 받아 slide-preview.html(1080×1350 시뮬레이션)을 구현하고, Puppeteer
  캡쳐 스크립트로 slide-1.png ~ slide-10.png(1080×1350 고해상도)를 생성한다.
  [Triggers] 대표 스킬(sns-cardnews)이 카피 확정(표지 제목 택1 포함) 후 5단계에서
  호출한다. 사용자가 직접 호출하지 않는다. 제목 변경 등 텍스트 수정 후 재캡처가 필요할
  때도 이 스킬이 재호출된다.
  [Detailed Methodology] ①HTML 구현 규칙: 각 슬라이드는 `.slide` 클래스·540×675px(4:5)·
  Noto Serif KR(display)×Noto Sans KR(body) 웹폰트·design-brief.md의 슬라이드별
  배경/레이아웃/특수 요소(고스트 타이포·그레인·컬러 바)를 그대로 구현·전 장 동일 레이아웃
  금지·슬라이드 10은 사용자가 제공한 교회 로고 파일이 있을 때만 <img>로 배치(없으면 로고 없이 교회 이름만)·이모지를
  아이콘으로 쓰지 않는다(SVG 프리미티브 사용). ②캡쳐: `node scripts/capture-cardnews-4x5.js
  <출력폴더>/slide-preview.html` 실행 — 540×675 뷰포트 × deviceScaleFactor 2 = 1080×1350.
  ③실측 자가확인: 생성된 PNG 개수(10장)·파일 크기 0 아님·해상도를 실측하고 결과를
  보고한다("됐을 것"이 아니라 실행 출력 기준). 캡쳐 실패 시 1회 재시도 후 실패 내용을
  정직 보고한다. ④플레이스홀더 금지: "{제목}" 같은 템플릿 변수가 최종 HTML에 남으면
  빌드 실패로 판정한다. 시각 품질 판정(디자인이 브리프에 부합하는가)은 이 스킬의 자가
  주장이 아니라 sns-cardnews-verify의 몫이다.
disable-model-invocation: true
---

# Builder (하위 스킬)

## 입력 → 출력

| 입력 | 출력 |
|------|------|
| slides.md(확정)·design-brief.md·config/ | `slide-preview.html` + `slide-1.png`~`slide-10.png` |

## HTML 구현 규칙

- 각 슬라이드 = `.slide` 클래스, **540×675px (4:5)** — 캡쳐 스크립트가 이 클래스를 찾는다
- Noto Serif KR(제목·인용) × Noto Sans KR(본문) — Google Fonts 로드
- design-brief.md 슬라이드별 지시(배경·레이아웃·강조·특수 요소)를 1:1 구현
- 슬라이드 10: 사용자가 제공한 교회 로고 파일이 있으면 `<img>`로 배치(없으면 생략 · 어두운 배경이면 brief의 필터 지시 적용)
- 이모지 아이콘 금지 — SVG 프리미티브 사용
- 템플릿 변수(`{...}`) 잔존 = 빌드 실패

## 캡쳐

```bash
node scripts/capture-cardnews-4x5.js <출력폴더>/slide-preview.html
```

성공 기준(실측): PNG 10개 존재 · 각 파일 > 0 byte · 스크립트 출력 "성공: 10/10장".
실측 결과를 그대로 보고한다. 부분 성공(예: 8/10)을 완료로 보고하지 않는다.

## 재빌드(델타) 모드

텍스트 일부만 바뀐 재호출이면: 해당 슬라이드 텍스트만 교체 → 전체 재캡처 1회
(개별 장만 캡처하지 않는다 — 스크립트가 전 장을 다시 뜬다). 변경된 장 번호를 보고에 명시.

---
> ★**캡처 스크립트 참조 정정 (2026-08-13)**: 구 참조 `capture-cardnews.js`(★1:1 1080×1080 구 스펙)를 **`capture-cardnews-4x5.js`**(비율 4:5·기준 1080×1350)로 교체했다. ★주석이 아니라 **참조 자체**를 신본으로 바꾼 이유 = **스킬이 호출하는 것은 기계가 하는 일**이라 주석으로는 오호출이 막히지 않는다.
