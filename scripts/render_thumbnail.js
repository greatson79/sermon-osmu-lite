#!/usr/bin/env node
// Adapted from the six-template Puppeteer thumbnail workflow; all private photos and marks removed.
const fs=require('fs'), path=require('path');
let puppeteer;try{puppeteer=require('puppeteer');}catch(e){console.log('텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀 (필요: Node.js + Puppeteer — setup.sh·setup.ps1 로 설치)');process.exit(0);}
const argv=process.argv.slice(2); const opt={};
for(let i=0;i<argv.length;i++) if(argv[i].startsWith('--')) opt[argv[i].slice(2)]=argv[++i];
if(!opt.title||!opt.scripture||!opt.out) throw new Error('사용: --title 제목 --scripture 본문 --out 폴더 [--church 교회이름] [--tpl T01..T06|all]');
const fontUrl=require('url').pathToFileURL(path.resolve(__dirname,'../assets/fonts/NotoSansKR.ttf')).href;
const esc=s=>String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
const T={
 T01:['#233c32','#f2eee4','center','background:radial-gradient(circle at 25% 25%,#547463,#233c32 65%)'],
 T02:['#243e37','#f5e4a0','left','background:linear-gradient(110deg,#1e3931 0%,#45695d 100%)'],
 T03:['#192a27','#f8f1de','left','background:linear-gradient(180deg,#4b655f,#192a27 80%)'],
 T04:['#ead898','#253c32','left','background:linear-gradient(100deg,#ead898 0 56%,#d5e0d4 56%)'],
 T05:['#f3f0e7','#355545','left','background:radial-gradient(circle at 78% 50%,#d6e4d4,#f3f0e7 58%)'],
 T06:['#e4ebe4','#1e4132','center','background:linear-gradient(145deg,#e4ebe4,#bfcec1)']
};
const chosen=opt.tpl==='all'||!opt.tpl?Object.keys(T):[opt.tpl];
fs.mkdirSync(opt.out,{recursive:true});
(async()=>{const browser=await puppeteer.launch({headless:'new'});const page=await browser.newPage();await page.setViewport({width:1280,height:720,deviceScaleFactor:1});
for(const id of chosen){if(!T[id])throw new Error('unknown template '+id);const [bg,fg,align,background]=T[id];
const html=`<!doctype html><html lang="ko"><meta charset="utf-8"><style>@font-face{font-family:'Noto Sans KR';src:url('${fontUrl}');font-weight:100 900}*{box-sizing:border-box}body{margin:0;width:1280px;height:720px;overflow:hidden;font-family:'Noto Sans KR','Apple SD Gothic Neo',system-ui,sans-serif;color:${fg};background:${bg};${background}}.tag{position:absolute;top:62px;left:74px;font-size:24px;letter-spacing:.16em}.title{position:absolute;left:74px;right:74px;top:210px;text-align:${align};font-size:92px;font-weight:800;line-height:1.13;word-break:keep-all}.ref{position:absolute;bottom:92px;left:74px;font-size:31px}.brand{position:absolute;bottom:40px;right:74px;font-size:21px;letter-spacing:.12em}</style><div class="title">${esc(opt.title)}</div><div class="ref">${esc(opt.scripture)}</div>${opt.church?`<div class="brand">${esc(opt.church)}</div>`:''}</html>`;
const tmp=path.join(require('os').tmpdir(),'osmu-thumb-'+id+'.html');fs.writeFileSync(tmp,html);await page.goto(require('url').pathToFileURL(tmp).href);await page.evaluate(()=>document.fonts.ready);const file=path.join(opt.out,id+'.png');await page.screenshot({path:file});console.log('OK '+id+' 1280x720');}
await browser.close();})().catch(e=>{console.error(e);process.exit(1)});
