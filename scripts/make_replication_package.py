"""Build the public replication package outside the repository.

Reads the private repository and writes ../labor-backing-replication/. Nothing in the
private repository is modified. Every file that enters the package is either copied
verbatim or passed through a sanitiser that removes local paths and contact details.

Run:  python scripts/make_replication_package.py [--out ../labor-backing-replication]

The manifest below is the release decision, file by file. INCLUDE copies verbatim,
SANITISE copies through the rewriter, and anything not listed does not ship.
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# --------------------------------------------------------------------------- manifest

INCLUDE_DIRS = [
    # (source, destination, glob patterns kept, patterns dropped)
    ("src", "src", ["*.py", "*.sh"], []),
    ("src/stress", "src/stress", ["*.py"], []),
    ("src/verify", "src/verify", ["*.py"], []),
    ("framework/labor_backing", "framework/labor_backing",
     ["*.py", "*.csv", "*.json", "*.md"], ["seal_*.py"]),
    ("framework/tau_k", "framework/tau_k", ["*.py", "*.csv", "*.json", "*.md"], []),
    ("framework/institutions", "framework/institutions",
     ["*.py", "*.csv", "*.json", "*.md"],
     ["fdic_institutions_*.csv", "ncua_institutions_*.csv"]),
    ("framework/ai_bust", "framework/ai_bust", ["*.py", "*.csv", "*.json", "*.md"], []),
    ("framework/revision_r1", "framework/revision_r1",
     ["*.py", "*.csv", "*.json", "*.md"], []),
    ("framework/revision_r2", "framework/revision_r2",
     ["*.py", "*.csv", "*.json", "*.md"], []),
    ("data/release", "data/release", ["*"], []),
    ("notes/sources", "docs/source_extractions", ["*.md"], []),
    ("notes/replication", "docs/rebuilds", ["*.md", "*.csv"], ["sealed_*"]),
    ("notes/replication/round2", "docs/rebuilds/round2", ["*.md", "*.csv"], ["sealed_*"]),
    ("notes/replication/round3", "docs/rebuilds/round3", ["*.md", "*.csv"], ["sealed_*"]),
]

INCLUDE_FILES = [
    ("framework/architecture.md", "framework/architecture.md"),
    ("framework/architecture_spec.md", "framework/architecture_spec.md"),
    ("framework/propositions.md", "framework/propositions.md"),
    ("notes/replication_brief.md", "docs/rebuilds/replication_brief.md"),
    ("notes/replication_brief_debt_only.md", "docs/rebuilds/replication_brief_debt_only.md"),
    ("notes/replication_brief_v2.md", "docs/rebuilds/replication_brief_v2.md"),
    ("notes/replication_brief_v2_2_addendum.md",
     "docs/rebuilds/replication_brief_v2_2_addendum.md"),
    ("paper/gen_results_macros.py", "paper_interface/gen_results_macros.py"),
    ("paper/gen_figures.py", "paper_interface/gen_figures.py"),
    ("paper/gen_tables.py", "paper_interface/gen_tables.py"),
    ("paper/qa_gates.py", "paper_interface/qa_gates.py"),
    ("paper/pdf_gates.py", "paper_interface/pdf_gates.py"),
    ("paper/wordcount.py", "paper_interface/wordcount.py"),
]

# Small processed inputs the headline rebuild reads. Everything here is a derived
# intermediate, never a redistributed raw file.
PROCESSED_INPUTS = [
    "replication_r_sensitivity.json",
    "labor_tax_share.json",
    "retained_wage_share_summary.json",
    "retained_wage_share_grid.csv",
    "dose_response_first_round.csv",
    "second_round_fed_mapping.csv",
    "balance_benchmark.csv",
    "bls_dws_summary.json",
    "conversion_layer.json",
    "fiscal_channel_summary.json",
    "fiscal_extended_axis.csv",
    "rho_bounded_dose_grid.csv",
    "under_reporting_factors.csv",
    "capacities.json",
    "scenario_axis_levels.csv",
    "legA_tier2.csv",
    "verify/hand_check_credit.csv",
    "verify/hand_check_credit.json",
]

# Directories never copied, at any depth.
DENY_DIRS = {"__pycache__", ".git", ".venv", "_unreviewed", "_fred", "sealed",
             "node_modules", ".ipynb_checkpoints", ".pytest_cache"}

# Files never copied, by name or suffix.
DENY_SUFFIXES = {".pyc", ".pyo", ".zip", ".pdf", ".aux", ".log", ".bbl", ".blg",
                 ".out", ".tex", ".bib", ".DS_Store"}
DENY_NAME_RE = re.compile(r"(sealed|expected_values|REQUESTS|GATE_REPORT|prereg_|"
                          r"decisions|open_questions|webb_email|MASTER_PROMPT|"
                          r"PROJECT_BRIEF|unverified)", re.I)

# --------------------------------------------------------------------------- sanitiser

SANITISE_RULES = [
    # contact details used for SEC/FDIC fair-access User-Agent headers
    (re.compile(r'OWNER_NAME\s*=\s*"[^"]*"'),
     'OWNER_NAME = os.environ.get("CONTACT_NAME", "Replication User")'),
    (re.compile(r'OWNER_EMAIL\s*=\s*"[^"]*"'),
     'OWNER_EMAIL = os.environ.get("CONTACT_EMAIL", "replication@example.org")'),
    (re.compile(r"team@oviguide\.in"), "${CONTACT_EMAIL}"),
    (re.compile(r"\bGunveer Kalsi\b"), "${CONTACT_NAME}"),
    # absolute paths of any kind
    (re.compile(r"[A-Za-z]:[\\/]+Users[\\/]+[A-Za-z0-9_.-]+[\\/]+[^\s\"']*"), "<path>"),
    (re.compile(r"/home/[A-Za-z0-9_.-]+/[^\s\"']*"), "<path>"),
    (re.compile(r"/Users/[A-Za-z0-9_.-]+/[^\s\"']*"), "<path>"),
]

NEEDS_OS_IMPORT = re.compile(r"os\.environ")


def sanitise(text: str, name: str) -> tuple[str, list[str]]:
    hits = []
    for pattern, repl in SANITISE_RULES:
        if pattern.search(text):
            hits.append(f"{name}: {pattern.pattern[:44]}")
            text = pattern.sub(repl, text)
    if name.endswith(".py") and NEEDS_OS_IMPORT.search(text) and not re.search(
            r"^import os$", text, re.M):
        text = re.sub(r"(^\"\"\".*?\"\"\"\n)", r"\1import os\n", text, count=1, flags=re.S)
        if not re.search(r"^import os$", text, re.M):
            text = "import os\n" + text
    return text, hits


def denied(path: pathlib.Path) -> bool:
    if any(part in DENY_DIRS for part in path.parts):
        return True
    if path.suffix.lower() in DENY_SUFFIXES:
        return True
    return bool(DENY_NAME_RE.search(path.name))


def copy_file(src: pathlib.Path, dst: pathlib.Path, report: list[str]) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() in {".py", ".sh", ".md", ".json", ".csv", ".txt", ".cfg", ".toml"}:
        try:
            text = src.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            shutil.copy2(src, dst)
            return True
        text, hits = sanitise(text, src.as_posix())
        report.extend(hits)
        dst.write_text(text, encoding="utf-8")
    else:
        shutil.copy2(src, dst)
    return True


def build(out: pathlib.Path) -> list[str]:
    report: list[str] = []
    # clear the contents rather than the directory itself: on Windows the directory
    # can be held open by an indexer while its children are removable
    out.mkdir(parents=True, exist_ok=True)
    for child in out.iterdir():
        if child.name in {".git", "dist", "build"}:
            continue          # never touch the release repository's own history
        if child.is_dir():
            shutil.rmtree(child, ignore_errors=True)
        else:
            child.unlink()

    n = 0
    for rel, dest, keep, drop in INCLUDE_DIRS:
        base = ROOT / rel
        if not base.exists():
            report.append(f"MISSING SOURCE DIR {rel}")
            continue
        for pattern in keep:
            for src in sorted(base.glob(pattern)):
                if not src.is_file() or denied(src.relative_to(ROOT)):
                    continue
                if any(src.match(d) for d in drop):
                    continue
                copy_file(src, out / dest / src.name, report)
                n += 1
        # one level of subdirectories for data/release only
        if rel == "data/release":
            for sub in sorted(p for p in base.iterdir() if p.is_dir()):
                for src in sorted(sub.rglob("*")):
                    if src.is_file() and not denied(src.relative_to(ROOT)):
                        copy_file(src, out / dest / sub.name / src.name, report)
                        n += 1

    for rel, dest in INCLUDE_FILES:
        src = ROOT / rel
        if not src.exists():
            report.append(f"MISSING SOURCE FILE {rel}")
            continue
        copy_file(src, out / dest, report)
        n += 1

    # the validation pilot: four documents only, exported from the pilot branch.
    # No pilot code or data enters the package; the paper cites these in its limitations.
    import subprocess
    PILOT_COMMIT = "acaf6ba"
    PILOT_DOCS = [("PREREGISTRATION.md", "preregistration.md"),
                  ("DEVIATIONS.md", "deviations.md"),
                  ("RESULTS.md", "results.md"),
                  ("OWNER_SUMMARY.md", "close_out.md")]
    for src_name, dst_name in PILOT_DOCS:
        rev = f"{PILOT_COMMIT}:framework/validation/{src_name}"
        try:
            blob = subprocess.run(["git", "show", rev], cwd=ROOT, capture_output=True,
                                  check=True).stdout.decode("utf-8")
        except (subprocess.CalledProcessError, OSError) as exc:
            report.append(f"PILOT DOC MISSING {src_name}: {exc}")
            continue
        text, hits = sanitise(blob, f"pilot/{src_name}")
        report.extend(hits)
        dst = out / "docs" / "validation_pilot" / dst_name
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(text, encoding="utf-8")
        n += 1

    # static release assets: Makefile, harness, documentation templates
    assets = ROOT / "release_assets"
    for src in sorted(assets.rglob("*")):
        if src.is_file():
            copy_file(src, out / src.relative_to(assets), report)
            n += 1

    for name in PROCESSED_INPUTS:
        src = ROOT / "data" / "processed" / name
        if not src.exists():
            report.append(f"MISSING PROCESSED INPUT {name}")
            continue
        copy_file(src, out / "data" / "processed" / name, report)
        n += 1

    report.append(f"copied {n} files")
    return report


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT.parent / "labor-backing-replication"))
    args = ap.parse_args()
    out = pathlib.Path(args.out).resolve()
    for line in build(out):
        print(line)
    total = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    count = sum(1 for p in out.rglob("*") if p.is_file())
    print(f"package: {count} files, {total / 1e6:.1f} MB at {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
