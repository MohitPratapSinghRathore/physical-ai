"""Rebuild the headline numbers and compare them to the released artifacts.

Two stages, both offline.

STAGE 1, RERUN. Four modules are re-executed in a scratch copy of the package, so that
nothing shipped is overwritten. Each reads only files in this package. The values they
produce are compared to the released artifacts they are supposed to reproduce: the
assembled capital tax rate under both rent readings and both taxable-share bases, the
required band, the rate and the required band on each jurisdiction, the value of g at
which the condition closes, the labor backing ratio pair on both coefficient bases, and
the federal exposure share with its creditor and debtor parts.

STAGE 2, READ AND COMPARE. Every value the paper reports is regenerated from
data/release/ by paper_interface/gen_results_macros.py and compared, key by key, to
replication/reported_values.csv, which lists those values as printed. This covers the
quantities whose own rebuild needs raw survey data that this package does not
redistribute: the 1952 to 2025 series, the first-round incidence by holder, the
institution-level summary and the quintile gradient.

Tolerances are stated per quantity below and are absolute.

Run:  python replication/headline.py        (or: make headline)
"""
from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]

RERUNS = [
    {
        "module": "framework/tau_k/assemble.py",
        "produced": "framework/tau_k/tau_k_assembled.json",
        "released": "data/release/tau_k/tau_k_assembled.json",
        "checks": [
            ("assembled rate, Barkai rent reading",
             ["marked_points", "assembled median, Barkai reading"], 1e-4),
            ("assembled rate, Karabarbounis-Neiman reading",
             ["marked_points", "assembled median, Karabarbounis-Neiman reading"], 1e-4),
            ("required rate, easier labor reading", ["required_tau_k", "low"], 1e-4),
            ("required rate, harder labor reading", ["required_tau_k", "high"], 1e-4),
            ("shareholder layer at sourced centrals",
             ["shareholder_layer_at_centrals"], 1e-4),
            ("taxable-share base, CRS alternative",
             ["shareholder_layer_checks", "CRS_implied_taxable_share"], 1e-4),
        ],
    },
    {
        "module": "framework/revision_r2/c_jurisdiction_boundary.py",
        "produced": "framework/revision_r2/c_jurisdiction_boundary.json",
        "released": "data/release/revision_r2/c_jurisdiction_boundary.json",
        "checks": [
            ("assembled rate, federal only",
             ["C1_jurisdiction", "federal only", "assembled_tau_k"], 1e-4),
            ("assembled rate, all government",
             ["C1_jurisdiction", "all government", "assembled_tau_k"], 1e-4),
            ("required band, federal only, easier",
             ["C1_jurisdiction", "federal only", "required_easier"], 1e-4),
            ("required band, federal only, harder",
             ["C1_jurisdiction", "federal only", "required_harder"], 1e-4),
            ("g at which the condition closes, easier",
             ["C3_g_at_which_the_condition_closes", "federal only",
              "g_closing_easier"], 1e-3),
            ("g at which the condition closes, harder",
             ["C3_g_at_which_the_condition_closes", "federal only",
              "g_closing_harder"], 1e-3),
            ("retained wage share", ["retained_wage_share_R"], 1e-6),
        ],
    },
    {
        "module": "framework/revision_r2/b2_headline_effect.py",
        "produced": "framework/revision_r2/b2_headline_effect.json",
        "released": "data/release/revision_r2/b2_headline_effect.json",
        "checks": [
            ("debt-only direct ratio, coverage basis",
             ["published", "ratios", "debt_only_direct"], 1e-4),
            ("debt-only including indirect, coverage basis",
             ["published", "ratios", "debt_only_incl_indirect"], 1e-4),
            ("all-claims direct ratio, coverage basis",
             ["published", "ratios", "all_claims_direct"], 1e-4),
            ("federal exposure union, coverage basis",
             ["published", "exposure", "union"], 1e-4),
            ("federal creditor or guarantor part",
             ["published", "exposure", "creditor"], 1e-4),
            ("federal debtor part", ["published", "exposure", "debtor"], 1e-4),
            ("debt-only direct ratio, wage-share basis",
             ["alternative", "ratios", "debt_only_direct"], 1e-4),
            ("federal exposure union, wage-share basis",
             ["alternative", "exposure", "union"], 1e-4),
        ],
    },
    {
        "module": "framework/revision_r1/a1_pass_through.py",
        "produced": "framework/revision_r1/a1_pass_through.json",
        "released": "data/release/revision_r1/a1_pass_through.json",
        "checks": [
            ("pass-through coefficient g, central", ["g_central_base", "g"], 1e-4),
            ("pass-through coefficient g, low",
             ["g_range_base_construction", 0], 1e-4),
            ("pass-through coefficient g, high",
             ["g_range_base_construction", 1], 1e-4),
        ],
    },
]


def dig(obj, path):
    for key in path:
        obj = obj[int(key)] if isinstance(obj, list) else obj[key]
    return obj


def scratch_copy() -> pathlib.Path:
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="lbr_headline_"))
    for rel in ["framework", "data", "src", "paper_interface", "replication"]:
        src = ROOT / rel
        if src.exists():
            shutil.copytree(src, tmp / rel)
    (tmp / "paper" / "figures").mkdir(parents=True, exist_ok=True)
    return tmp


def run_module(tmp: pathlib.Path, module: str) -> tuple[bool, str]:
    proc = subprocess.run([sys.executable, module], cwd=tmp,
                          capture_output=True, text=True)
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout).strip().splitlines()
        return False, (tail[-1][:150] if tail else "no output")
    return True, ""


def parse_macros(text: str) -> dict[str, str]:
    return {m.group(1): m.group(2) for m in
            re.finditer(r"csname result@([A-Za-z]+)\\endcsname\{(.*?)\}$", text, re.M)}


def main() -> int:
    results: list[tuple[str, str, str, str]] = []
    tmp = scratch_copy()

    for spec in RERUNS:
        ok, err = run_module(tmp, spec["module"])
        if not ok:
            for label, _, _ in spec["checks"]:
                results.append((label, "n/a", "n/a", f"FAIL ({err})"))
            continue
        produced = json.loads((tmp / spec["produced"]).read_text(encoding="utf-8"))
        released = json.loads((ROOT / spec["released"]).read_text(encoding="utf-8"))
        for label, path, tol in spec["checks"]:
            try:
                a, b = float(dig(produced, path)), float(dig(released, path))
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                results.append((label, "n/a", "n/a", f"FAIL (missing {exc})"))
                continue
            results.append((label, f"{a:.6g}", f"{b:.6g}",
                            "PASS" if abs(a - b) <= tol else "FAIL"))

    ok, err = run_module(tmp, "paper_interface/gen_results_macros.py")
    expected_path = ROOT / "replication" / "reported_values.csv"
    if not ok:
        results.append(("every value reported in the paper", "n/a", "n/a",
                        f"FAIL ({err})"))
    elif not expected_path.exists():
        results.append(("every value reported in the paper", "n/a", "n/a",
                        "FAIL (reported_values.csv missing)"))
    else:
        produced = parse_macros(
            (tmp / "paper" / "results_macros.tex").read_text(encoding="utf-8"))
        expected = {}
        for line in expected_path.read_text(encoding="utf-8").splitlines()[1:]:
            if "," in line:
                k, v = line.split(",", 1)
                expected[k.strip()] = v.strip().strip('"')
        missing = [k for k in expected if k not in produced]
        differing = [k for k in expected
                     if k in produced and produced[k].strip() != expected[k]]
        n = len(expected)
        detail = f"{n - len(missing) - len(differing)}/{n} match"
        if missing:
            detail += f"; missing {missing[:3]}"
        if differing:
            detail += f"; differ {differing[:3]}"
        results.append(("every value reported in the paper", detail, f"{n} values",
                        "PASS" if not missing and not differing else "FAIL"))

    width = max(len(r[0]) for r in results) + 2
    print(f"{'quantity'.ljust(width)}{'rebuilt':>18}{'released':>14}   verdict")
    print("-" * (width + 46))
    for label, a, b, verdict in results:
        print(f"{label.ljust(width)}{a:>18}{b:>14}   {verdict}")
    failed = sum(1 for r in results if r[3].startswith("FAIL"))
    print("-" * (width + 46))
    print(f"{len(results) - failed} PASS, {failed} FAIL")
    shutil.rmtree(tmp, ignore_errors=True)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
