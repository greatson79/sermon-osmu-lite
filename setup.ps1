# Windows PowerShell 5.1 이상 · 관리자 권한 불필요 · setup.sh 와 같은 동작
# 사용: powershell -NoProfile -ExecutionPolicy Bypass -File setup.ps1 [-Without small-group,faith-essay]
param([string[]]$Without = @())
$ErrorActionPreference = 'Stop'
$skipSkills = @($Without -split ',' | Where-Object { $_ })
$packDir = $PSScriptRoot
if ($env:CLAUDE_CONFIG_DIR) { $configDir = $env:CLAUDE_CONFIG_DIR } else { $configDir = Join-Path $env:USERPROFILE '.claude' }
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupDir = Join-Path $configDir 'sermon-osmu-backup'
$toolsDir = Join-Path $configDir 'sermon-osmu-tools'
foreach ($d in @('skills', 'commands', 'sermon-osmu-tools\scripts')) {
    New-Item -ItemType Directory -Force -Path (Join-Path $configDir $d) | Out-Null
}

# 폴더면 (상대경로 + 해시) 목록, 파일이면 해시 하나 — 내용이 같은지 비교용.
function Get-Sig($p) {
    if (Test-Path -LiteralPath $p -PathType Container) {
        $root = (Resolve-Path -LiteralPath $p).Path
        (Get-ChildItem -LiteralPath $p -Recurse -File -Force | ForEach-Object {
            $_.FullName.Substring($root.Length) + ':' + (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
        } | Sort-Object) -join "`n"
    } else {
        (Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash
    }
}

# 이미 있는 같은 이름의 스킬·명령은 덮기 전에 <이름>.bak-<날짜시각> 으로 옮긴다(내용이 같으면 그대로 둔다).
function Backup-IfDifferent($src, $dst, $name) {
    if (-not (Test-Path -LiteralPath $dst)) { return }
    if ((Get-Sig $src) -eq (Get-Sig $dst)) { return }
    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
    $to = Join-Path $backupDir "$name.bak-$stamp"
    Move-Item -LiteralPath $dst -Destination $to
    Write-Host "백업: 기존 $name 을(를) $to 로 옮겼습니다."
}

foreach ($skillDir in Get-ChildItem -LiteralPath (Join-Path $packDir '.claude\skills') -Directory) {
    $name = $skillDir.Name
    if ($skipSkills -contains $name) { Write-Host "제외: $name 스킬은 설치하지 않습니다(-Without)."; continue }
    $dst = Join-Path $configDir "skills\$name"
    Backup-IfDifferent $skillDir.FullName $dst $name
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Get-ChildItem -LiteralPath $skillDir.FullName -Force | Copy-Item -Destination $dst -Recurse -Force
}
$cmdSrc = Join-Path $packDir '.claude\commands\주간콘텐츠.md'
$cmdDst = Join-Path $configDir 'commands\주간콘텐츠.md'
Backup-IfDifferent $cmdSrc $cmdDst '주간콘텐츠.md'
Copy-Item -LiteralPath $cmdSrc -Destination $cmdDst -Force
# 옛 판의 bash 도구 3개(고정 파일명)는 .py 로 바뀌었다 — 이미 설치된 곳에 남아 있으면 백업 폴더로 옮긴다.
foreach ($old in @('check-tools.sh', 'crop_4x5.sh', 'loud.sh')) {
    $oldPath = Join-Path $toolsDir "scripts\$old"
    if (Test-Path -LiteralPath $oldPath) {
        New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
        $to = Join-Path $backupDir "$old.bak-$stamp"
        Move-Item -LiteralPath $oldPath -Destination $to
        Write-Host "백업: 옛 도구 $old 을(를) $to 로 옮겼습니다."
    }
}
Get-ChildItem -LiteralPath (Join-Path $packDir 'scripts') -File | Copy-Item -Destination (Join-Path $toolsDir 'scripts') -Force
New-Item -ItemType Directory -Force -Path (Join-Path $toolsDir 'assets') | Out-Null
Copy-Item -LiteralPath (Join-Path $packDir 'assets\fonts') -Destination (Join-Path $toolsDir 'assets') -Recurse -Force
Copy-Item -LiteralPath (Join-Path $packDir 'package.json') -Destination (Join-Path $toolsDir 'package.json') -Force
Copy-Item -LiteralPath (Join-Path $packDir 'package-lock.json') -Destination (Join-Path $toolsDir 'package-lock.json') -Force

if ($env:SKIP_NODE_INSTALL -ne '1') {
    $npm = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if (-not $npm) { $npm = Get-Command npm -ErrorAction SilentlyContinue }
    if ($npm) {
        $ErrorActionPreference = 'Continue'
        # --prefix 대신 도구 폴더로 들어가 실행한다(npm 11.19 는 다른 프로젝트 폴더에서 --prefix 로 부르면 lock 불일치로 거부함)
        Push-Location $toolsDir
        & $npm.Source ci --omit=dev
        $npmExit = $LASTEXITCODE
        Pop-Location
        $ErrorActionPreference = 'Stop'
        if ($npmExit -ne 0) {
            Write-Host '안내: Puppeteer 설치에 실패했습니다. 카드·썸네일 이미지 단계는 건너뜁니다(텍스트 산출은 그대로 됩니다).'
        }
    } else {
        Write-Host '안내: npm 이 없어 Puppeteer 를 설치하지 않았습니다. 카드·썸네일 이미지 단계는 건너뜁니다(텍스트 산출은 그대로 됩니다). Node.js 설치 후 setup.ps1 을 다시 실행하세요.'
    }
}
Write-Host "Installed /주간콘텐츠 and downstream skills in $configDir"
exit 0
