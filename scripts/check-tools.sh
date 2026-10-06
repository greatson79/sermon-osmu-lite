#!/usr/bin/env bash
# 단계별 준비물 점검. 없어도 오류로 끝내지 않는다(항상 exit 0).
here="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
ok() { echo "[가능] $1"; }
skip() { echo "[건너뜀] $1 — 텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀 (필요: $2)"; }
if command -v node >/dev/null && [ -d "$here/../node_modules/puppeteer" ]; then
  ok "카드뉴스·썸네일 이미지"
else
  skip "카드뉴스·썸네일 이미지" "Node.js + Puppeteer, bash setup.sh"
fi
if command -v ffmpeg >/dev/null && python3 -c "import PIL" 2>/dev/null; then
  ok "쇼릴 영상 렌더"
else
  skip "쇼릴 영상 렌더" "ffmpeg + Python Pillow"
fi
if python3 -c "import googleapiclient, google_auth_oauthlib" 2>/dev/null; then
  ok "유튜브 업로드 도구 (OAuth 파일은 사용자가 따로 준비 · 승인 뒤에만 실행)"
else
  skip "유튜브 업로드" "google-api-python-client, google-auth-oauthlib, OAuth 클라이언트 JSON"
fi
exit 0
