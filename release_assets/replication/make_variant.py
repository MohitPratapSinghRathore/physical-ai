"""Produce the anonymous and the named archive variants from this one tree.

  python replication/make_variant.py --variant anon    (or: make anon)
  python replication/make_variant.py --variant named   (or: make named)

The anonymous variant strips author names, affiliations, emails, the organisation name,
repository URLs and the private-hash mapping from every file, including CITATION.cff,
.zenodo.json and RELEASE_NOTES.md, and writes no git configuration. It then runs the
identity scan over its own output and refuses to finish if anything identifying remains.

Each variant is written to dist/<variant>/ and is ready for `git archive` or a plain zip.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

# Strings that must not appear in the anonymous variant. Add to this list rather than
# relying on the substitutions alone: the scan is the gate, the substitutions are the fix.
IDENTIFYING = [
    "Rathore", "Mohit", "Gunveer", "Kalsi", "Sriharsha", "Meduri",
    "Pratap Chandra", "Mandal", "Oviqo", "oviguide", "gunveerkalsi",
    "mohitpratapsinghr", "sriharshameduri", "Indian Institute of Management",
    "github.com/", "MohitPratapSinghRathore",
]

SUBSTITUTIONS = [
    (re.compile(r"(?m)^\s*-\s*family-names:.*$\n(\s*given-names:.*$\n)?"
                r"(\s*affiliation:.*$\n)?(\s*orcid:.*$\n)?"),
     "  - name: Author removed for double-anonymous peer review\n"),
    (re.compile(r'\{"name": "[^"]*", "affiliation": "[^"]*", "orcid": "[^"]*"\}'),
     '{"name": "Author removed for double-anonymous peer review"}'),
    (re.compile(r"(?i)\b(Rathore|Gunveer|Kalsi|Sriharsha|Meduri|Mandal)\b"), "[removed]"),
    (re.compile(r"(?i)\bMohit Pratap Singh\b|\bPratap Chandra\b"), "[removed]"),
    (re.compile(r"(?i)\bOviqo\b|\boviguide\.in\b"), "[removed]"),
    (re.compile(r"(?i)Indian Institute of Management[^,.\n]*"), "[removed]"),
    (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
     "anonymous@example.org"),
    (re.compile(r"https?://github\.com/\S+"), "https://example.org/repository-removed"),
    # the private-hash mapping, which exists only for the authors
    (re.compile(r"(?m)^.*private repository commit.*$\n?"), ""),
    (re.compile(r"(?m)^.*\b[0-9a-f]{40}\b.*$\n?"), ""),
]

TEXT_SUFFIXES = {".md", ".py", ".cff", ".json", ".txt", ".yml", ".yaml", ".sh",
                 ".csv", ".lock", ".example", ""}


def anonymise(text: str) -> str:
    for pattern, repl in SUBSTITUTIONS:
        text = pattern.sub(repl, text)
    return text


def build(variant: str) -> pathlib.Path:
    out = DIST / variant
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for src in sorted(ROOT.rglob("*")):
        if not src.is_file():
            continue
        rel = src.relative_to(ROOT)
        if rel.parts[0] in {"dist", ".git", "build"}:
            continue
        # the variant builder carries the list of identifying terms, so it is not part
        # of the anonymous archive: a referee does not need it and it would trip the scan
        if variant == "anon" and rel.as_posix() == "replication/make_variant.py":
            continue
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if variant == "anon" and (src.suffix.lower() in TEXT_SUFFIXES):
            try:
                dst.write_text(anonymise(src.read_text(encoding="utf-8")),
                               encoding="utf-8")
                continue
            except UnicodeDecodeError:
                pass
        shutil.copy2(src, dst)
    return out


def scan(out: pathlib.Path) -> list[str]:
    hits = []
    for path in sorted(out.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for needle in IDENTIFYING:
            if needle.lower() in text.lower():
                hits.append(f"{path.relative_to(out).as_posix()}: {needle}")
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["anon", "named"], required=True)
    args = ap.parse_args()

    out = build(args.variant)
    files = sum(1 for p in out.rglob("*") if p.is_file())
    size = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    print(f"{args.variant}: {files} files, {size / 1e6:.1f} MB at {out}")

    if args.variant == "anon":
        hits = scan(out)
        if hits:
            print(f"IDENTITY SCAN FAILED: {len(hits)} hits")
            for h in hits[:40]:
                print("  " + h)
            return 1
        print("identity scan: clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
