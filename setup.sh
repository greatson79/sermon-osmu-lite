#!/usr/bin/env bash
set -euo pipefail
pack_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
config_dir="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
stamp="$(date +%Y%m%d-%H%M%S)"
backup_dir="$config_dir/sermon-osmu-backup"
mkdir -p "$config_dir/skills" "$config_dir/commands" "$config_dir/sermon-osmu-tools/scripts"

# 이미 있는 같은 이름의 스킬·명령은 덮기 전에 <이름>.bak-<날짜시각> 으로 옮긴다(내용이 같으면 그대로 둔다).
backup_if_different() {
  local src="$1" dst="$2" name="$3"
  [ -e "$dst" ] || return 0
  if diff -rq "$src" "$dst" >/dev/null 2>&1; then return 0; fi
  mkdir -p "$backup_dir"
  mv "$dst" "$backup_dir/$name.bak-$stamp"
  echo "백업: 기존 $name 을(를) $backup_dir/$name.bak-$stamp 로 옮겼습니다."
}

for skill_dir in "$pack_dir"/.claude/skills/*; do
  [ -d "$skill_dir" ] || continue
  name="$(basename "$skill_dir")"
  backup_if_different "$skill_dir" "$config_dir/skills/$name" "$name"
  mkdir -p "$config_dir/skills/$name"
  cp -R "$skill_dir/." "$config_dir/skills/$name/"
done
backup_if_different "$pack_dir/.claude/commands/주간콘텐츠.md" "$config_dir/commands/주간콘텐츠.md" "주간콘텐츠.md"
cp "$pack_dir/.claude/commands/주간콘텐츠.md" "$config_dir/commands/주간콘텐츠.md"
cp "$pack_dir"/scripts/* "$config_dir/sermon-osmu-tools/scripts/"
mkdir -p "$config_dir/sermon-osmu-tools/assets"
cp -R "$pack_dir/assets/fonts" "$config_dir/sermon-osmu-tools/assets/"
cp "$pack_dir/package.json" "$config_dir/sermon-osmu-tools/package.json"
cp "$pack_dir/package-lock.json" "$config_dir/sermon-osmu-tools/package-lock.json"
if [ "${SKIP_NODE_INSTALL:-0}" != "1" ]; then
  if command -v npm >/dev/null; then
    npm ci --prefix "$config_dir/sermon-osmu-tools" --omit=dev \
      || echo '안내: Puppeteer 설치에 실패했습니다. 카드·썸네일 이미지 단계는 건너뜁니다(텍스트 산출은 그대로 됩니다).'
  else
    echo '안내: npm 이 없어 Puppeteer 를 설치하지 않았습니다. 카드·썸네일 이미지 단계는 건너뜁니다(텍스트 산출은 그대로 됩니다). Node.js 설치 후 setup.sh 를 다시 실행하세요.'
  fi
fi
printf 'Installed /주간콘텐츠 and downstream skills in %s\n' "$config_dir"
