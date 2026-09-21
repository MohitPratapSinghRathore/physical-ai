"""Secrets, identity and hygiene scan over a built release tree.

Run on the package before the first commit and again on each variant.

  python scripts/release_scan.py --tree ../labor-backing-replication
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

SECRET_PATTERNS = [
    ("GitHub personal access token", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}")),
    ("GitHub fine-grained token", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("Zenodo or generic bearer token", re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}")),
    ("assigned API key", re.compile(r"(?i)(api[_-]?key|api[_-]?token|access[_-]?token)"
                                    r"\s*[:=]\s*[\"']([A-Za-z0-9_\-]{16,})[\"']")),
    ("assigned password", re.compile(r"(?i)(password|passwd|secret)\s*[:=]\s*"
                                     r"[\"']([^\"']{6,})[\"']")),
    ("FRED style 32-char key", re.compile(r"(?i)fred[_-]?api[_-]?key\s*[:=]\s*"
                                          r"[\"']?[a-z0-9]{32}")),
]

IDENTITY_PATTERNS = [
    ("email address", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("home directory path", re.compile(r"([A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9_.-]+"
                                       r"|/home/[A-Za-z0-9_.-]+|/Users/[A-Za-z0-9_.-]+)")),
    ("personal name", re.compile(r"\b(Rathore|Gunveer|Kalsi|Sriharsha|Meduri|"
                                 r"Mohit Pratap|Pratap Chandra)\b")),
    ("organisation", re.compile(r"(?i)\b(oviqo|oviguide)\b")),
    ("machine name", re.compile(r"(?i)\b(DESKTOP-[A-Z0-9]+|LAPTOP-[A-Z0-9]+)\b")),
    ("chat or prompt text", re.compile(r"(?i)(you are claude|system prompt|"
                                       r"^\s*(user|assistant):)", re.M)),
]

ALLOWED_EMAILS = {"replication@example.org", "you@example.org", "anonymous@example.org",
                  "AdminContact@sample.com", "noreply@anthropic.com"}

SKIP_SUFFIXES = {".png", ".pdf", ".zip", ".xlsx", ".xls", ".pyc"}


def scan(tree: pathlib.Path) -> tuple[list[str], list[str], list[str]]:
    secrets, identity, hygiene = [], [], []
    total = 0
    for path in sorted(tree.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        total += 1
        rel = path.relative_to(tree).as_posix()
        if path.stat().st_size > 50 * 1024 * 1024:
            hygiene.append(f"over 50 MB: {rel}")
        if path.name in {".env"} or path.name.startswith(".env.") and \
                path.name != ".env.example":
            hygiene.append(f"env file present: {rel}")
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for label, pattern in SECRET_PATTERNS:
            for m in pattern.finditer(text):
                secrets.append(f"{rel}: {label}: {m.group(0)[:40]}")
        for label, pattern in IDENTITY_PATTERNS:
            for m in pattern.finditer(text):
                hit = m.group(0)
                if label == "email address" and hit in ALLOWED_EMAILS:
                    continue
                identity.append(f"{rel}: {label}: {hit[:60]}")
    hygiene.append(f"{total} files scanned")
    return secrets, identity, hygiene


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--allow-identity", action="store_true",
                    help="named variant: identity hits are expected and are listed only")
    args = ap.parse_args()
    tree = pathlib.Path(args.tree).resolve()

    secrets, identity, hygiene = scan(tree)
    print("== secrets ==")
    print("\n".join("  " + s for s in secrets) if secrets else "  none")
    print("== identity ==")
    if identity:
        seen = {}
        for line in identity:
            key = line.split(": ", 1)[1]
            seen.setdefault(key, []).append(line.split(":")[0])
        for key, files in sorted(seen.items()):
            print(f"  {key}  in {len(files)} file(s): {', '.join(sorted(set(files))[:4])}")
    else:
        print("  none")
    print("== hygiene ==")
    for h in hygiene:
        print("  " + h)

    if secrets:
        print("\nSCAN FAILED: secret pattern present")
        return 1
    if identity and not args.allow_identity:
        print("\nSCAN FAILED: identifying string present")
        return 1
    print("\nSCAN PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
