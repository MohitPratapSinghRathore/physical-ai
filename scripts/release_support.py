"""Second stage of the release build: everything generated rather than copied.

Writes, into the release directory only:
  replication/reported_values.csv   the paper's reported values, parsed from the
                                    private macro file, so the harness can compare
  data/CHECKSUMS.sha256             SHA256 of every raw input the paper used
  DATA_SOURCES.md                   publisher, identifier, vintage, access date,
                                    licence and checksum for every raw input
  DATA_DICTIONARY.md                every released file, column by column
  METHODS_MAP.md                    paper object to script to artifact

Run after scripts/make_replication_package.py.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import pathlib
import re
import sys
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parents[1]

# Raw inputs the paper used. Access dates are the project's own fetch dates; the
# "manual" flag marks sources that refused automated access from this environment.
RAW_SOURCES = [
    ("Financial Accounts of the United States (Z.1)", "Federal Reserve Board",
     "Z.1 quarterly data package, all tables", "2026 Q2 release", "2026-09-19",
     "US Government work, public domain", "framework/labor_backing/_z1_cache.zip", False),
    ("Distributional Financial Accounts", "Federal Reserve Board",
     "DFA levels by wealth percentile", "2026 Q2", "2026-09-19",
     "US Government work, public domain", "framework/labor_backing/_dfa_cache.zip", False),
    ("Survey of Income and Program Participation", "US Census Bureau",
     "SIPP 2023 panel, wave 1, household and person files", "2023 panel", "2026-09-18",
     "US Government work, public domain", "data/raw/sipp", False),
    ("American Community Survey PUMS", "US Census Bureau",
     "ACS 1-year PUMS, housing and person records", "2024", "2026-09-18",
     "US Government work, public domain", "data/raw/pums", False),
    ("Worker Displacement Survey", "Bureau of Labor Statistics",
     "Displaced worker supplement, fourteen biennial vintages", "1996 to 2024",
     "2026-09-18", "US Government work, public domain; site blocks automated access",
     "data/raw/bls_ep", True),
    ("Occupational Employment and O*NET task data", "BLS and O*NET Resource Center",
     "O*NET database, task and work-activity files", "28.3", "2026-09-18",
     "O*NET is CC BY 4.0; attribution required", "data/raw/onet", False),
    ("Statistics of Income", "Internal Revenue Service",
     "Table 1.4, adjusted gross income by source", "2021 to 2023", "2026-09-19",
     "US Government work, public domain", "data/raw/irs", False),
    ("House Price Index", "Federal Housing Finance Agency",
     "All-transactions index, national", "2026 Q2", "2026-09-19",
     "US Government work; FHFA terms permit reuse with attribution",
     "data/raw/hpi", False),
    ("Enterprise annual filings", "Fannie Mae and Freddie Mac via SEC EDGAR",
     "Form 10-K, single-family credit statistics", "fiscal 2025", "2026-09-19",
     "SEC EDGAR, public filings; fair-access policy applies", "data/raw/gse", False),
    ("Company filings for the AI side", "Nine registrants via SEC EDGAR",
     "Form 10-K and 10-Q, capital spending, cash flow, debt", "fiscal 2025",
     "2026-09-19", "SEC EDGAR, public filings", "data/raw/sec", False),
    ("Institution panel, banks", "FDIC",
     "BankFind Suite institutions file, all insured banks", "2026-06-30", "2026-09-20",
     "US Government work, public domain; FDIC API is scriptable",
     "framework/institutions/fdic_institutions_20260630.csv", False),
    ("Institution panel, credit unions", "NCUA",
     "5300 call report, all federally insured credit unions", "2026-06-30",
     "2026-09-20", "US Government work, public domain; bulk file is a manual download",
     "framework/institutions/ncua_2026-06.zip", True),
    ("Macroeconomic series", "Federal Reserve Bank of St Louis (FRED)",
     "Named series listed in src/fetch_fred.py", "2026-09-19", "2026-09-19",
     "FRED terms permit redistribution of derived work; series are public",
     "data/raw/fred", False),
    ("Supervisory stress test results", "Federal Reserve Board",
     "DFAST 2026 severely adverse scenario, loss rates", "2026", "2026-09-20",
     "US Government work, public domain", "data/raw/manual", False),
    ("Trustees Report", "Social Security and Medicare Boards of Trustees",
     "Summary tables, fund income and depletion dates", "2026", "2026-09-20",
     "US Government work, public domain", "data/raw/manual", False),
    ("Congressional Budget Office publications", "CBO",
     "Taxing capital income, effective rates", "2014", "2026-09-20",
     "CBO material is in the public domain; site blocks automated access",
     "data/raw/manual", True),
    ("Congressional Research Service R47113", "CRS",
     "Table 5, shareholder-level effective rates", "2024", "2026-09-20",
     "CRS reports are US Government works; site blocks automated access",
     "data/raw/manual", True),
]

# Paper object -> script that produces it -> artifact it is read from.
METHODS_MAP = [
    ("Table 1, the thirteen claim classes", "framework/labor_backing/build_direct.py",
     "data/release/labor_backing/direct_ratio_latest.json"),
    ("Table 2, the bridge to backing coefficients",
     "framework/revision_r2/b1_bridge_table.py", "data/release/revision_r2/b1_bridge.csv"),
    ("Table 3, debt-only sensitivity", "framework/labor_backing/build_sensitivity.py",
     "data/release/labor_backing/debt_only_sensitivity.csv"),
    ("Table 4, holders of wage-backed claims", "framework/labor_backing/build_direct.py",
     "framework/labor_backing/holder_matrix_latest.csv"),
    ("Table 5, the assembled capital rate", "framework/tau_k/assemble.py",
     "data/release/tau_k/tau_k_assembled.json"),
    ("Table 6, the levers ranked", "framework/tau_k/assemble.py",
     "data/release/tau_k/tau_k_assembled.json"),
    ("Table 7, first-round incidence by holder", "src/incidence_run.py",
     "data/release/dose_response/dose_response_first_round.csv"),
    ("Table 8, liquid runway by quintile", "src/sipp_buffers_v2.py",
     "data/release/incidence/household_balance_sheets.csv"),
    ("Table 9, institutions by business model", "framework/institutions/apply_losses.py",
     "data/release/institutions/a2_distribution_by_class.csv"),
    ("Table 10, relief instruments", "framework/revision_r1/a3_relief_feedback.py",
     "data/release/revision_r1/a3_relief_feedback.csv"),
    ("Table 11, the AI side by tier", "framework/ai_bust/b1_tiers.py",
     "data/release/ai_bust/b1_tiers.json"),
    ("Table 12, the instrument table", "src/make_instrument_release.py",
     "data/release/architecture/instruments.csv"),
    ("Table 13, quantities removed", "paper_interface/gen_tables.py",
     "data/release/stated_limitations.csv"),
    ("Figure 1, the series 1952 to 2025", "paper_interface/gen_figures.py",
     "data/release/labor_backing/debt_only_ratio_timeseries.csv"),
    ("Figure 2, holders of the two sides", "paper_interface/gen_figures.py",
     "data/release/labor_backing/two_sided_bet.json"),
    ("Figure 3, the capital tax map", "paper_interface/gen_figures.py",
     "data/release/tau_k/tau_k_assembled.json"),
    ("Figure 4, federal share by displacement level", "paper_interface/gen_figures.py",
     "data/release/incidence/federal_share_by_dose.csv"),
    ("Figure 5, breaches by business model", "paper_interface/gen_figures.py",
     "data/release/institutions/a2_distribution_by_class.csv"),
    ("Figure 6, the fiscal boundary", "paper_interface/gen_figures.py",
     "data/release/revision_r2/c4_boundary_grid.csv"),
    ("Headline: debt-only ratio pair", "framework/labor_backing/build_debt_only.py",
     "data/release/labor_backing/debt_only_ratio.json"),
    ("Headline: federal exposure share", "framework/labor_backing/item3_sovereign_robustness.py",
     "data/release/labor_backing/item3_sovereign_robustness.json"),
    ("Headline: assembled rate by jurisdiction and the boundary",
     "framework/revision_r2/c_jurisdiction_boundary.py",
     "data/release/revision_r2/c_jurisdiction_boundary.json"),
    ("Headline: backing basis and its effect",
     "framework/revision_r2/b2_headline_effect.py",
     "data/release/revision_r2/b2_headline_effect.json"),
    ("Headline: the rebuild scoreboard", "src/make_replication_release.py",
     "data/release/replication_rounds.csv"),
    ("Every reported value", "paper_interface/gen_results_macros.py",
     "replication/reported_values.csv"),
]

STATUS_HINT = {
    "measured": "measured from a published source or a survey",
    "rebuilt": "reproduced by an independent computational rebuild",
    "scenario": "conditional arithmetic on a stated input",
}


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def reported_values(out: pathlib.Path) -> int:
    src = ROOT / "paper" / "results_macros.tex"
    rows = re.findall(r"csname result@([A-Za-z]+)\\endcsname\{(.*?)\}$",
                      src.read_text(encoding="utf-8"), re.M)
    dst = out / "replication" / "reported_values.csv"
    dst.parent.mkdir(parents=True, exist_ok=True)
    with dst.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["key", "value_as_printed"])
        w.writerows(rows)
    return len(rows)


def checksums(out: pathlib.Path) -> list[tuple[str, str, int]]:
    """SHA256 of the raw files the paper used, computed in the private tree."""
    done = []
    for _, _, _, _, _, _, rel, _ in RAW_SOURCES:
        p = ROOT / rel
        if p.is_file():
            done.append((rel, sha256(p), p.stat().st_size))
        elif p.is_dir():
            files = sorted(q for q in p.rglob("*") if q.is_file())
            h = hashlib.sha256()
            size = 0
            for q in files:
                h.update(q.relative_to(p).as_posix().encode())
                h.update(sha256(q).encode())
                size += q.stat().st_size
            done.append((rel + "/ (directory digest over "
                         + str(len(files)) + " files)", h.hexdigest(), size))
        else:
            done.append((rel, "NOT PRESENT IN THE PRIVATE TREE", 0))
    path = out / "data" / "CHECKSUMS.sha256"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(f"{h}  {rel}\n" for rel, h, _ in done), encoding="utf-8")
    return done


def data_sources(out: pathlib.Path, sums: list[tuple[str, str, int]]) -> None:
    by_rel = {rel.split("/ (")[0]: (h, size) for rel, h, size in sums}
    lines = ["# Data sources", "",
             "Every raw input the paper used. None of it is redistributed in this",
             "package: the table gives the publisher, the identifier, the vintage, the",
             "access date, the terms, and a SHA256 of the file or directory as used, so a",
             "replicator can confirm they have the same bytes.", "",
             "A different checksum means a different vintage, not an error. `make verify`",
             "reports the difference and names the series rather than failing silently.",
             "",
             "| source | publisher | series or table | vintage | accessed | terms | local path | SHA256 |",
             "|---|---|---|---|---|---|---|---|"]
    manual = []
    for name, pub, ident, vintage, acc, lic, rel, is_manual in RAW_SOURCES:
        h, _ = by_rel.get(rel, ("unavailable", 0))
        lines.append(f"| {name} | {pub} | {ident} | {vintage} | {acc} | {lic} | "
                     f"`{rel}` | `{h[:16]}...` |")
        if is_manual:
            manual.append((name, pub, rel))
    lines += ["", "## Inputs that must be fetched by hand", "",
              "These publishers returned 403 to automated requests from the environment",
              "the paper was built in. Download them in a browser and place them at the",
              "path given; `make verify` then checks the checksum.", ""]
    for name, pub, rel in manual:
        lines.append(f"- **{name}** ({pub}) into `{rel}`")
    lines += ["", "Everything else is fetched by `make fetch`.", ""]
    (out / "DATA_SOURCES.md").write_text("\n".join(lines), encoding="utf-8")


def describe_csv(path: pathlib.Path) -> list[str]:
    try:
        with path.open(newline="", encoding="utf-8") as fh:
            r = csv.reader(fh)
            header = next(r, [])
            first = next(r, [])
    except (UnicodeDecodeError, StopIteration):
        return []
    out = []
    for i, col in enumerate(header):
        sample = first[i] if i < len(first) else ""
        kind = "number" if re.fullmatch(r"-?\d+(\.\d+)?([eE]-?\d+)?", sample or "x") \
            else "text"
        out.append(f"| `{col}` | {kind} | example `{sample[:24]}` | |")
    return out


def data_dictionary(out: pathlib.Path) -> None:
    lines = ["# Data dictionary", "",
             "Every file in `data/release/` and every shipped processed input. Columns",
             "are read from the files themselves; the definition column is completed by",
             "hand and the status column carries the paper's own vocabulary: measured,",
             "rebuilt, scenario.", "",
             "Regenerate the skeleton with `python replication/make_dictionary.py`.", ""]
    for base in ["data/release", "data/processed"]:
        for path in sorted((out / base).rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(out).as_posix()
            lines.append(f"## `{rel}`")
            lines.append("")
            if path.suffix == ".json":
                try:
                    obj = json.loads(path.read_text(encoding="utf-8"))
                    keys = list(obj)[:24] if isinstance(obj, dict) else []
                    status = obj.get("status", "") if isinstance(obj, dict) else ""
                except json.JSONDecodeError:
                    keys, status = [], ""
                if status:
                    lines.append(f"Status as recorded in the file: {status}")
                    lines.append("")
                lines.append("Top-level keys: " + ", ".join(f"`{k}`" for k in keys))
            elif path.suffix == ".csv":
                rows = describe_csv(path)
                if rows:
                    lines.append("| column | type | example | definition |")
                    lines.append("|---|---|---|---|")
                    lines.extend(rows)
                else:
                    lines.append("(empty or non-tabular)")
            else:
                lines.append("(documentation file)")
            lines.append("")
    (out / "DATA_DICTIONARY.md").write_text("\n".join(lines), encoding="utf-8")


def methods_map(out: pathlib.Path) -> list[str]:
    problems = []
    lines = ["# Methods map", "",
             "Every table, figure and headline number in the paper, the script that",
             "produces it, and the artifact it is read from. Paths are relative to the",
             "root of this package.", "",
             "| paper object | script | artifact |", "|---|---|---|"]
    for obj, script, artifact in METHODS_MAP:
        lines.append(f"| {obj} | `{script}` | `{artifact}` |")
        if not (out / script).exists():
            problems.append(f"METHODS_MAP: missing script {script}")
        if not (out / artifact).exists():
            problems.append(f"METHODS_MAP: missing artifact {artifact}")
    lines.append("")
    (out / "METHODS_MAP.md").write_text("\n".join(lines), encoding="utf-8")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT.parent / "labor-backing-replication"))
    args = ap.parse_args()
    out = pathlib.Path(args.out).resolve()

    n = reported_values(out)
    print(f"replication/reported_values.csv: {n} reported values")
    sums = checksums(out)
    missing = [rel for rel, h, _ in sums if h.startswith("NOT PRESENT")]
    print(f"data/CHECKSUMS.sha256: {len(sums)} entries, {len(missing)} not present")
    for rel in missing:
        print(f"  not present: {rel}")
    data_sources(out, sums)
    data_dictionary(out)
    for problem in methods_map(out):
        print(problem)
    print(f"generated docs in {out}")
    print(f"build date {date.today().isoformat()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
