#!/usr/bin/env python3
# 사용: loud.py <wav> → 통합 음량(LUFS)·트루피크
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
if len(sys.argv) < 2:
    raise SystemExit('사용: loud.py <wav>')
if not shutil.which('ffmpeg'):
    print('텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀 (필요: ffmpeg)')
    sys.exit(0)
r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', sys.argv[1], '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
lines = [re.sub(r' +', ' ', l) for l in r.stdout.decode('utf-8', 'replace').splitlines() if re.match(r'\s+(I:|Peak:|LRA:)', l)]
print(''.join(l + ' ' for l in lines))
