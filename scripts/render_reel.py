#!/usr/bin/env python3
"""Generalized 30-second 9:16 render from manuscript-anchored cuts."""
import argparse
import json
import pathlib
import subprocess
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')
SKIP = '텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀'
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print(SKIP + ' (필요: Python Pillow — pip install pillow)')
    sys.exit(0)

W, H = 1080, 1920


def wrap(draw, text, font, limit):
    lines, line = [], ''
    for word in text.split():
        trial = f'{line} {word}'.strip()
        if draw.textbbox((0, 0), trial, font=font)[2] > limit and line:
            lines.append(line); line = word
        else:
            line = trial
    if line: lines.append(line)
    if len(lines) > 4: raise ValueError('caption exceeds safe area')
    return lines


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cuts', type=pathlib.Path, required=True)
    ap.add_argument('--manuscript', type=pathlib.Path, required=True)
    default_font = pathlib.Path(__file__).resolve().parent.parent / 'assets' / 'fonts' / 'NotoSansKR.ttf'
    ap.add_argument('--font', type=pathlib.Path, default=default_font)
    ap.add_argument('--out', type=pathlib.Path, required=True)
    ap.add_argument('--audio', type=pathlib.Path)
    args = ap.parse_args()
    if not shutil.which('ffmpeg'):
        print(SKIP + ' (필요: ffmpeg)')
        return
    cuts = json.loads(args.cuts.read_text(encoding='utf-8'))
    manuscript = args.manuscript.read_text(encoding='utf-8')
    if not 2 <= len(cuts) <= 12 or abs(sum(float(c['seconds']) for c in cuts) - 30) > .01:
        raise SystemExit('2–12 cuts must sum to 30 seconds')
    if not args.font.is_file(): raise SystemExit('서체 파일이 없다: assets/fonts/NotoSansKR.ttf 또는 --font 로 지정')
    frames = (args.out.parent / (args.out.stem + '_frames')).resolve()
    frames.mkdir(parents=True, exist_ok=True)
    font = ImageFont.truetype(str(args.font), 70)
    try:
        font.set_variation_by_name('Bold')
    except (AttributeError, OSError):
        pass
    concat = []
    for i, cut in enumerate(cuts, 1):
        text = cut['text'].strip()
        if text not in manuscript:
            raise SystemExit(f'cut {i} text is not a literal manuscript substring')
        im = Image.new('RGB', (W, H), '#263c35')
        d = ImageDraw.Draw(im)
        lines = wrap(d, text, font, 920)
        top = 860 - len(lines) * 45
        for line in lines:
            d.text((W // 2, top), line, font=font, fill='#f5efe2', anchor='ma')
            top += 105
        if top > 1600: raise SystemExit(f'cut {i} exceeds 4:5 safe area')
        frame = frames / f'cut-{i:02d}.png'
        im.save(frame)
        frame_ref = frame.as_posix().replace("'", "'\\''")
        concat.extend([f"file '{frame_ref}'", f"duration {float(cut['seconds']):.3f}"])
    concat.append(f"file '{frame_ref}'")
    playlist = frames / 'concat.txt'
    playlist.write_bytes(('\n'.join(concat) + '\n').encode('utf-8'))
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', str(playlist)]
    if args.audio:
        cmd.extend(['-i', str(args.audio), '-map', '0:v', '-map', '1:a', '-shortest', '-c:a', 'aac'])
    else:
        cmd.extend(['-map', '0:v'])
    cmd.extend(['-vf', 'fps=30', '-t', '30', '-pix_fmt', 'yuv420p', '-c:v', 'libx264', '-movflags', '+faststart', str(args.out)])
    subprocess.run(cmd, check=True)
    print('rendered 1080x1920, 30 seconds:', args.out.name)


if __name__ == '__main__':
    main()
