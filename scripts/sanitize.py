#!/usr/bin/env python3
"""Fail closed release scan for a candidate pack directory."""
import argparse
import base64
import hashlib
import pathlib
import re
import sys

PATTERNS = {
    "home_path": r"/Us" + r"ers/[A-Za-z][A-Za-z0-9_-]*/|/home/(?!user/)[a-z][a-z0-9_-]*/",
    "email": r"[A-Za-z0-9._%+-]+" + r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "phone": r"(?<!\d)(?:01[016789]-?\d{3,4}-?\d{4}|0[2-9]\d?-?\d{3,4}-?\d{4})(?!\d)",
    "private_key": r"-----BEGIN\s+(?:RSA\s+|EC\s+|OPENSSH\s+)?PRIVATE KEY-----",
    "aws_key": r"AKIA" + r"[0-9A-Z]{16}",
    "github_token": r"gh[pousr]_" + r"[A-Za-z0-9_]{36,}|github_pat_[A-Za-z0-9_]{22,}",
    "google_secret": r"GOCSPX-" + r"[A-Za-z0-9_-]+",
    "jwt": r"eyJ[A-Za-z0-9_-]{20,}\.eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]+",
    "credential_url": r"(?:postgres|mysql|mongodb|redis)://[^:]+:[^@]+@[^\s'\"]+",
    "secret_assignment": r"(?i)(?:api[_-]?key|secret|password|token)\s*[=:]\s*['\"]?[A-Za-z0-9+/=_-]{16,}",
    "private_ip": r"\b(?:192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(?:1[6-9]|2\d|3[01])\.\d+\.\d+)\b",
}
# 검토 완료된 동봉 바이너리: 경로 -> SHA-256 (assets/fonts/README.md 에 출처 기록)
ALLOWED_ASSETS = {"assets/fonts/NotoSansKR.ttf": "194018e6b2b293a7964f037b25c0249ce1418bc9ab3c971060a03aa57861e252"}
DANGEROUS = {"credentials.json", "token.json", ".env", "service-account.json"}
DANGEROUS_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".jks", ".map"}


def source_index(roots, sizes):
    result = {size: [] for size in sizes}
    if not sizes:
        return result
    for root in roots:
        for path in root.rglob("*"):
            if path.is_file() and path.stat().st_size in sizes:
                result[path.stat().st_size].append((path, hashlib.sha256(path.read_bytes()).hexdigest()))
    return result


def scan(root, sources=()):
    findings = []
    assets = []
    for path in sorted(root.rglob("*")):
        if ".git" in path.relative_to(root).parts:
            continue
        if path.is_dir():
            if path.name in {"node_modules", "__pycache__", ".moai", "sessions", ".secrets", "secrets", ".venv", "venv"}:
                findings.append((str(path.relative_to(root)), "dangerous_directory"))
            continue
        rel = str(path.relative_to(root))
        if path.name in DANGEROUS or path.name.startswith(".env.") or ".bak-" in path.name or "백업" in path.name or path.suffix in DANGEROUS_SUFFIXES:
            findings.append((rel, "dangerous_file"))
        try:
            data = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            assets.append((rel, path.read_bytes()))
            continue
        for match in re.finditer(r"[A-Za-z0-9+/]{2000,}={0,2}", data):
            try:
                decoded = base64.b64decode(match.group(), validate=True)
            except ValueError:
                findings.append((rel, "long_encoded_text"))
                continue
            assets.append((f"{rel}:{data.count(chr(10), 0, match.start()) + 1}", decoded))
        for name, pattern in PATTERNS.items():
            for match in re.finditer(pattern, data):
                line = data.count("\n", 0, match.start()) + 1
                findings.append((f"{rel}:{line}", name))
    index = source_index(sources, {len(blob) for _, blob in assets})
    for rel, blob in assets:
        digest = hashlib.sha256(blob).hexdigest()
        if ALLOWED_ASSETS.get(rel) == digest:
            continue
        peers = index.get(len(blob), [])
        match = next((p for p, sha in peers if sha == digest), None)
        category = "source_asset_match" if match else "same_size_source_asset" if peers else "unreviewed_asset"
        findings.append((rel, category))
    return findings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pack_dir", type=pathlib.Path)
    parser.add_argument("--source", action="append", type=pathlib.Path, default=[])
    args = parser.parse_args()
    root = args.pack_dir.resolve()
    findings = scan(root, [p.resolve() for p in args.source])
    if findings:
        print("FAIL")
        for place, category in findings:
            print(f"{category} {place}")
        raise SystemExit(1)
    print("PASS: 0 findings across all pack files")


if __name__ == "__main__":
    main()
