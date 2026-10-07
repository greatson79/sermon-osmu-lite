# Sermon OSMU Lite

설교 원고 한 편을 넣고 명령 하나(`/주간콘텐츠`)를 실행하면, 나눔지 · 카드뉴스 · 신앙에세이 · 썸네일 · 쇼릴 · 유튜브 업로드 문안을 순서대로 만들어 주는 [Claude Code](https://claude.com/claude-code) 스킬 모음입니다. 설교 준비와 원고 쓰기는 포함하지 않습니다. 시작점은 **목회자가 직접 쓴 완성 원고**입니다.

Wave AI Networks가 만들었습니다. MIT 라이선스.

## 설치 (한 줄)

맥:

```bash
git clone https://github.com/greatson79/sermon-osmu-lite && cd sermon-osmu-lite && bash setup.sh
```

윈도우 (PowerShell · 관리자 권한 필요 없음):

```powershell
git clone https://github.com/greatson79/sermon-osmu-lite; cd sermon-osmu-lite; powershell -NoProfile -ExecutionPolicy Bypass -File setup.ps1
```

git이 없으면 저장소 페이지의 Code → Download ZIP으로 받아 압축을 풀고, 그 폴더에서 마지막 한 줄(`powershell -NoProfile -ExecutionPolicy Bypass -File setup.ps1`)만 실행합니다. 이 한 줄은 PowerShell 실행 정책을 바꾸지 않고 이번 실행에만 통과시킵니다.

이미 설치한 분은 저장소를 새로 받아(`git pull` 또는 ZIP 다시 받기) 위 설치 한 줄을 다시 실행하세요. 옛 `.sh` 도구는 백업 폴더로 옮겨지고 새 명령·스킬 문서로 바뀝니다.

`setup.sh`·`setup.ps1`은 명령과 스킬, 렌더 도구, 한글 서체를 Claude Code 설정 폴더(맥 `~/.claude`, 윈도우 `%USERPROFILE%\.claude`, `CLAUDE_CONFIG_DIR`가 지정돼 있으면 그 폴더)에 복사하고 Puppeteer를 설치합니다. 같은 이름의 스킬이나 명령이 이미 있고 내용이 다르면 덮기 전에 `~/.claude/sermon-osmu-backup/<이름>.bak-<날짜시각>`으로 옮기고 그 사실을 출력합니다. npm이 없으면 안내만 하고 나머지 설치는 끝낸 뒤 정상 종료합니다(이미지 단계만 건너뜀).

나눔지나 신앙에세이가 필요 없으면 설치 때 뺄 수 있습니다: `bash setup.sh --without small-group,faith-essay` (윈도우: `... -File setup.ps1 -Without small-group,faith-essay`). 뺀 스킬의 단계는 `/주간콘텐츠`가 오류 없이 건너뜁니다.

## 윈도우 준비물

Node.js(LTS), Python 3, ffmpeg가 필요합니다. 설치한 뒤에는 PowerShell을 새로 열어야 `node`·`python`·`ffmpeg`가 잡힙니다.

- Node.js: https://nodejs.org/en/download
- Python 3: https://www.python.org/downloads/ (설치 화면에서 「Add python.exe to PATH」를 켭니다)
- ffmpeg: `winget install ffmpeg` (또는 https://www.gyan.dev/ffmpeg/builds/ 에서 내려받기)
- Pillow(쇼릴용): `python -m pip install pillow`

## 시작 전 준비 3가지

1. **Claude Code 로그인** — 폴더에서 `claude`를 실행해 로그인되어 있어야 합니다.
2. **이미지 엔진** — 이 팩의 이미지 엔진은 Puppeteer(헤드리스 크롬)입니다. Node.js와 npm이 있으면 `setup.sh`가 설치합니다. 카드뉴스와 썸네일 PNG를 만듭니다.
3. **ffmpeg + 유튜브 OAuth** — 쇼릴 영상은 ffmpeg와 Python Pillow(`python -m pip install pillow`)가 필요합니다. 업로드까지 쓰려면 본인 유튜브 채널의 OAuth 클라이언트 JSON과 `python -m pip install google-api-python-client google-auth-oauthlib`가 필요합니다.

## 원고 넣는 위치

`원고/` 폴더에 원고 파일(.md 또는 .txt) 한 편을 넣습니다. 카드와 썸네일 하단에 교회 이름을 넣으려면 `원고/교회이름.txt`에 한 줄로 적습니다(없으면 비워 둡니다). 산출물은 `산출/<원고 파일명>/` 아래에 생깁니다.

## 사용 흐름

1. 이 폴더에서 Claude Code를 엽니다.
2. `원고/`에 설교 원고를 넣습니다.
3. `/주간콘텐츠`를 한 번 실행합니다. (파일 경로를 직접 주려면 `/주간콘텐츠 경로/원고.md`)
4. 먼저 준비물을 점검하고, 이어서 나눔지 → 카드뉴스 → 신앙에세이 → 썸네일 → 쇼릴 → 업로드 문안 순서로 만듭니다. 마지막에 `verification.md`에 단계별 결과와 빠진 자료(`[미확인]`)가 기록됩니다.

## 준비물이 없으면 — 오류가 아니라 텍스트까지

이미지 엔진, ffmpeg, OAuth 중 없는 것이 있어도 멈추지 않습니다. 그 단계의 텍스트 산출(문안·대본·브리프)은 끝까지 만들고, 이미지·영상·업로드 단계만 「텍스트 산출까지 완료 · 이 단계는 준비물이 없어 건너뜀 (필요: …)」 안내와 함께 건너뜁니다. 준비물을 갖춘 뒤 다시 실행하면 이어서 만들 수 있습니다.

## 만들어지는 것

- 나눔지: 장년 · 청년 · 청소년 · 초등 4종 (문서)
- 카드뉴스: 10장 문안, 도구가 있으면 1080×1350 PNG 10장
- 신앙에세이 초안 (`draft` 상태)
- 썸네일: 제목·성구 브리프, 도구가 있으면 1280×720 PNG 후보 6종
- 쇼릴: 30초 대본 3안과 추천 1안, 도구가 있으면 1080×1920 영상
- 유튜브 업로드 문안: 제목·설명·태그
- `verification.md`: 단계별 산출·검증·미확인 기록

한글 글자는 동봉한 Noto Sans KR(SIL OFL 1.1)로 그립니다.

## 한계

- 업로드는 `/주간콘텐츠`가 하지 않습니다. 영상을 검수하고 직접 승인한 뒤 `scripts/upload_youtube.py`로 따로 실행하며, 기본 공개 범위는 비공개입니다.
- 성경 본문 직인용은 사용자가 제공한 판본 원문만 씁니다. 번역본 본문은 동봉하지 않습니다.
- 기관 로고, 인물 사진, 음원은 동봉하지 않습니다. 쓰려면 사용권이 있는 자산을 직접 준비하세요. 썸네일은 인물·로고가 없으면 중립 템플릿을 씁니다.
- 나눔지 PNG 캡처 도구는 없습니다. 나눔지는 문서까지가 산출입니다.
- 쇼릴은 컷마다 정지 화면이라 한 장면이 2초보다 깁니다(3~7초).
- 윈도우: 한글·공백이 든 폴더 경로는 GitHub Actions 윈도우 러너에서 경로를 흉내 낸 시험만 했습니다(실제 한글 계정 시험이 아님). 백신이 Puppeteer의 크롬 내려받기를 막으면 이미지 단계만 건너뛰어집니다.
- 나눔지는 규칙상 원고 밖의 널리 알려진 이야기를 예로 들 수 있습니다. 그런 곳은 `[미확인]`으로 표시되니 설교자가 확인하세요.
- 성경 본문(판본·구절)을 넣는 자리가 아직 없어서, 성경을 직접 인용하는 부분은 채워지지 않습니다.
- 모든 산출물은 초안입니다. 사용 전 설교자가 원고와 대조해 검수하세요.
- 리눅스는 시험하지 않았습니다.

## 구성

- `.claude/commands/주간콘텐츠.md`: 진입 명령 (유일)
- `.claude/skills/`: 단계별 한국어 스킬과 규칙
- `scripts/`: 렌더·점검 도구(파이썬·Node 한 벌로 맥·윈도우 공통)
- `assets/fonts/`: Noto Sans KR와 라이선스
- `setup.sh`, `setup.ps1`: 설치기(맥 / 윈도우)
- `NOTICE`, `LICENSE`: 출처와 MIT 라이선스
