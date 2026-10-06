#!/usr/bin/env node
// Prepare a neutral ten slide HTML document for the source Puppeteer capture script.
const fs = require('fs');
const path = require('path');
if (process.argv.length < 4 || process.argv.length > 5) {
  console.error('사용: node build-cardnews-html.js cardnews.json 산출/카드뉴스/slide-preview.html [교회 이름]');
  process.exit(2);
}
const cards = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const roles = ['cover','empathy','struggle','text','message','gospel','quotation','practice','invitation','close'];
if (!Array.isArray(cards) || cards.length !== 10 || cards.some((c,i) => c.role !== roles[i] || typeof c.headline !== 'string' || typeof c.body !== 'string')) {
  throw new Error('10장 역할 순서와 headline/body 필수');
}
const fontUrl = 'file://' + encodeURI(path.resolve(__dirname, '../assets/fonts/NotoSansKR.ttf'));
const church = process.argv[4] || '';
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
const html = `<!doctype html><html lang="ko"><meta charset="utf-8"><style>
@font-face{font-family:'Noto Sans KR';src:url('${fontUrl}');font-weight:100 900}
*{box-sizing:border-box}html,body{margin:0;padding:0;width:540px;font-family:'Noto Sans KR','Apple SD Gothic Neo',system-ui,sans-serif}
.slide{width:540px;height:675px;position:relative;overflow:hidden;padding:58px 48px 50px;background:#f5f1e7;color:#273e34;border:1px solid #dad7cd}
.slide:nth-child(3n+2){background:#e4eae3}.slide:nth-child(3n){background:#e9e1d0}
.num{font-size:15px;letter-spacing:.15em;color:#566f5c}.rule{width:56px;height:4px;background:#6c8b70;margin-top:56px}
h1{font-weight:800;font-size:39px;line-height:1.22;letter-spacing:-.04em;margin:22px 0 36px;word-break:keep-all}
p{font-size:24px;line-height:1.55;margin:0;word-break:keep-all}.foot{position:absolute;bottom:38px;left:48px;font-size:14px;letter-spacing:.12em;color:#56705e}
</style>${cards.map((c,i)=>`<section class="slide"><div class="num">${String(i+1).padStart(2,'0')} / 10</div><div class="rule"></div><h1>${esc(c.headline)}</h1><p>${esc(c.body)}</p>${church ? `<div class="foot">${esc(church)}</div>` : ''}</section>`).join('')}</html>`;
const out = path.resolve(process.argv[3]);
fs.mkdirSync(path.dirname(out), {recursive:true});
fs.writeFileSync(out,html);
console.log(`10 slides HTML: ${out}`);
