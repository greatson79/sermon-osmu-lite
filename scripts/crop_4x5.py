#!/usr/bin/env python3
# 4:5 파생본(인스타·페북 피드용) — 9:16 마스터의 가운데 1080x1350 을 잘라낸다(위·아래 285px 제거 · 소리 그대로).
# 사용: crop_4x5.py <마스터.mp4> [프레임 뽑을 초=3]  →  <마스터>_4x5.mp4 + <마스터>_4x5_프레임.png(검수용 1장)
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
if len(sys.argv) < 2:
    raise SystemExit('사용: crop_4x5.py <마스터.mp4> [프레임 뽑을 초=3]')
if not shutil.which('ffmpeg'):
    print('텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀 (필요: ffmpeg)')
    sys.exit(0)
src = sys.argv[1]
out = (src[:-4] if src.endswith('.mp4') else src) + '_4x5'
sec = sys.argv[2] if len(sys.argv) > 2 else '3'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-vf', 'crop=1080:1350:0:285', '-c:v', 'libx264',
                '-preset', 'medium', '-crf', '18', '-c:a', 'copy', '-movflags', '+faststart', out + '.mp4'], check=True)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', sec, '-i', out + '.mp4', '-frames:v', '1', out + '_프레임.png'], check=True)
print('done: ' + out + '.mp4')
