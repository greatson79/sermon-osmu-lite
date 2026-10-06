#!/bin/bash
# 사용: loud.sh <wav> → 통합 음량(LUFS)·트루피크
ffmpeg -hide_banner -nostats -i "$1" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I:|Peak:|LRA:)" | tr -s ' ' | tr '\n' ' '; echo
