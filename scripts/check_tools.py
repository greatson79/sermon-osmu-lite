#!/usr/bin/env python3
# 단계별 준비물 점검. 없어도 오류로 끝내지 않는다(항상 exit 0).
import importlib.util
import pathlib
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
here = pathlib.Path(__file__).resolve().parent


def has(*modules):
    try:
        return all(importlib.util.find_spec(m) for m in modules)
    except (ImportError, ValueError):
        return False


def ok(what):
    print(f'[가능] {what}')


def skip(what, need):
    print(f'[건너뜀] {what} — 텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀 (필요: {need})')


if shutil.which('node') and (here.parent / 'node_modules' / 'puppeteer').is_dir():
    ok('카드뉴스·썸네일 이미지')
else:
    skip('카드뉴스·썸네일 이미지', 'Node.js + Puppeteer, setup.sh(맥) 또는 setup.ps1(윈도우)')
if shutil.which('ffmpeg') and has('PIL'):
    ok('쇼릴 영상 렌더')
else:
    skip('쇼릴 영상 렌더', 'ffmpeg + Python Pillow')
if has('googleapiclient', 'google_auth_oauthlib'):
    ok('유튜브 업로드 도구 (OAuth 파일은 사용자가 따로 준비 · 승인 뒤에만 실행)')
else:
    skip('유튜브 업로드', 'google-api-python-client, google-auth-oauthlib, OAuth 클라이언트 JSON')
sys.exit(0)
