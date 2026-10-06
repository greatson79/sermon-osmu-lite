#!/bin/bash
# 4:5 파생본(인스타·페북 피드용) — 9:16 마스터의 가운데 1080x1350 을 잘라낸다(위·아래 285px 제거 · 소리 그대로).
# 사용: crop_4x5.sh <마스터.mp4> [프레임 뽑을 초=3]  →  <마스터>_4x5.mp4 + <마스터>_4x5_프레임.png(검수용 1장)
set -euo pipefail
IN="$1"; O="${IN%.mp4}_4x5"
ffmpeg -y -loglevel error -i "$IN" -vf "crop=1080:1350:0:285" -c:v libx264 -preset medium -crf 18 -c:a copy -movflags +faststart "$O.mp4"
ffmpeg -y -loglevel error -ss "${2:-3}" -i "$O.mp4" -frames:v 1 "${O}_프레임.png"
echo "done: $O.mp4"
