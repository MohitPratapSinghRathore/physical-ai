"""Write data/release/replication_rounds.csv, the scoreboard for the three rebuild rounds.

The counts are computed from the rounds' own comparison artifacts, never typed:
round two from notes/replication/round2/comparison_round2.csv, round three from the
verdict column of the comparison tables in notes/replication/round3/comparison_round3.md.
The manuscript's replication figures come from this file through
paper/gen_results_macros.py.

Run:  python src/make_replication_release.py
"""
import csv
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "release" / "replication_rounds.csv"


def round_two():
    path = ROOT / "notes" / "replication" / "round2" / "comparison_round2.csv"
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    v = Counter(r["verdict"] for r in rows)
    sealed = len(rows) - v["NOT SEALED"] - v["IDENTITY CHECK"]
    return {
        "round": 2,
        "quantities_scored": len(rows),
        "sealed_counterparts": sealed,
        "inside_tolerance": v["MATCH (within tolerance)"],
        "within_five_percent": v["MATCH (within tolerance)"] + v["WITHIN 5 PERCENT"],
        "mismatches": v["MISMATCH"],
        "source": str(path.relative_to(ROOT)).replace("\\", "/"),
    }


def round_three():
    path = ROOT / "notes" / "replication" / "round3" / "comparison_round3.md"
    verdicts = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip().strip("*") for c in line.strip("|").split("|")]
        if len(cells) < 4:
            continue
        verdict = cells[-1].lower()
        if any(k in verdict for k in ("match", "exact", "agree", "mismatch")):
            verdicts.append(verdict)
    tol = sum(1 for v in verdicts if "within tolerance" in v)
    mis = sum(1 for v in verdicts if "mismatch" in v)
    return {
        "round": 3,
        "quantities_scored": len(verdicts),
        "sealed_counterparts": len(verdicts),
        "inside_tolerance": len(verdicts) - mis,
        "within_five_percent": len(verdicts) - mis,
        "mismatches": mis,
        "within_rounding": len(verdicts) - tol - mis,
        "source": str(path.relative_to(ROOT)).replace("\\", "/"),
    }


def main():
    r2, r3 = round_two(), round_three()
    r2["within_rounding"] = ""
    fields = ["round", "quantities_scored", "sealed_counterparts", "inside_tolerance",
              "within_five_percent", "within_rounding", "mismatches", "source"]
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerow({k: r2[k] for k in fields})
        w.writerow({k: r3[k] for k in fields})
    print("wrote", OUT)
    for r in (r2, r3):
        print(" ", r)


if __name__ == "__main__":
    main()
