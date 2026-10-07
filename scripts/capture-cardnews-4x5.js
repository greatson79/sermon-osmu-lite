#!/usr/bin/env node
/**
 * 카드뉴스 HTML → 4:5 개별 슬라이드 PNG 캡쳐 스크립트
 * 인스타그램 / 페이스북용 (1080×1350)
 *
 * 사용법: node capture-cardnews-4x5.js <slide-preview.html 경로>
 * 예시:   node capture-cardnews-4x5.js 산출/카드뉴스/slide-preview.html
 *
 * 출력: 같은 폴더에 slide-1.png, slide-2.png, ... 개별 파일 생성
 * 크기: 1080×1350 (540×675 CSS × deviceScaleFactor 2)
 */

let puppeteer;
try { puppeteer = require('puppeteer'); } catch (e) {
  console.log('텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀 (필요: Node.js + Puppeteer — setup.sh·setup.ps1 로 설치)');
  process.exit(0);
}
const path = require('path');
const fs = require('fs');

const htmlPath = process.argv[2];
if (!htmlPath) {
  console.error('사용법: node capture-cardnews-4x5.js <slide-preview.html 경로>');
  console.error('예시:   node capture-cardnews-4x5.js 산출/카드뉴스/slide-preview.html');
  process.exit(1);
}

const absHtml = path.resolve(htmlPath);
if (!fs.existsSync(absHtml)) {
  console.error(`파일을 찾을 수 없습니다: ${absHtml}`);
  process.exit(1);
}

const outDir = path.dirname(absHtml);

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();

  // 4:5 출력: 540×675 CSS + deviceScaleFactor 2 = 1080×1350 PNG
  await page.setViewport({ width: 540, height: 675, deviceScaleFactor: 2 });

  await page.goto(require('url').pathToFileURL(absHtml).href, { waitUntil: 'networkidle0', timeout: 30000 });

  // 웹폰트 로딩 대기
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 2000));

  const slideCount = await page.$$eval('.slide', els => els.length);
  if (slideCount === 0) {
    console.error('슬라이드를 찾을 수 없습니다 (.slide 클래스 요소 없음)');
    await browser.close();
    process.exit(1);
  }

  console.log(`카드뉴스 캡쳐 시작 — 4:5 인스타그램 / 페이스북 (${slideCount}장)`);
  console.log(`출력 크기: 1080×1350px`);

  let success = 0;
  const slides = await page.$$('.slide');

  for (let i = 0; i < slides.length; i++) {
    const slideNum = i + 1;
    const pngFile = path.join(outDir, `slide-${slideNum}.png`);
    try {
      await slides[i].screenshot({ path: pngFile, type: 'png' });
      console.log(`  ✓ slide-${slideNum}.png  (1080×1350)`);
      success++;
    } catch (err) {
      console.error(`  ✗ slide-${slideNum}.png 실패: ${err.message}`);
    }
  }

  await browser.close();
  console.log(`\n캡쳐 완료`);
  console.log(`├── 성공: ${success}/${slideCount}장`);
  console.log(`└── 저장 위치: ${outDir}`);
})();
