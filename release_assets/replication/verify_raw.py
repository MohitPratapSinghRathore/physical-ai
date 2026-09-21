"""Check the raw inputs against the checksums the paper was built from.

A mismatch is reported as a vintage difference, not as an error, because these
publishers revise. The exit status is zero when every file is present and matches,
and one when a file is missing; a checksum difference exits zero and prints the
series so that a replicator knows which number may move and why.

Run:  python replication/verify_raw.py     (or: make verify)
"""
from __future__ import annotations

import hashlib
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SUMS = ROOT / "data" / "CHECKSUMS.sha256"


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_dir(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    for q in sorted(p for p in path.rglob("*") if p.is_file()):
        h.update(q.relative_to(path).as_posix().encode())
        h.update(sha256_file(q).encode())
    return h.hexdigest()


def main() -> int:
    if not SUMS.exists():
        print("data/CHECKSUMS.sha256 is missing")
        return 1
    missing, differing, matched = [], [], 0
    for line in SUMS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, rel = line.split("  ", 1)
        rel = rel.split("/ (")[0]
        path = ROOT / rel
        if not path.exists():
            missing.append(rel)
            continue
        actual = sha256_dir(path) if path.is_dir() else sha256_file(path)
        if actual == expected:
            matched += 1
        else:
            differing.append((rel, expected[:12], actual[:12]))

    print(f"{matched} inputs match the vintage the paper used")
    for rel in missing:
        print(f"MISSING   {rel}  (see DATA_SOURCES.md; some sources are manual)")
    for rel, exp, act in differing:
        print(f"VINTAGE   {rel}  expected {exp}..., found {act}...")
        print("          this is a different release of the same series, not a fault;")
        print("          numbers derived from it may move and should be reported as such")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
