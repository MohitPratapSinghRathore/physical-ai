"""Count the claims register by status, reproducibly.

WHY THIS EXISTS. Every session has reported a status tally for notes/claims_register.md and
every tally was produced ad hoc, by eye or by a throwaway command. The counts drifted: a
session reported 142 rows with 57 standing, and a mechanical count of the same file at that
commit does not reproduce it. A governance document whose headline count cannot be rebuilt
is not governance. From here the tally comes from this script and nowhere else.

THE RULE. A claim row is any table row whose first cell is a claim number. Its STATUS is the
third cell, lowercased, matched against the status vocabulary in priority order, so that a
cell reading "provisional, superseded by A83" counts as superseded. Numbers are reused
across the two tables in the file (the main register and the engine-based table both run
from 36), so rows are counted, not numbers.
"""
import pathlib, re
from collections import Counter

ROOT = pathlib.Path(__file__).parents[1]
VOCAB = ["superseded", "withdrawn", "refuted", "downgraded", "split", "provisional",
         "standing"]


def count(path=None):
    t = (path or ROOT / "notes" / "claims_register.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\|\s*\d+[a-z]?\s*\|.*$", t, re.M)
    c, unclassified = Counter(), []
    for r in rows:
        f = r.split("|")
        s = f[3].lower() if len(f) > 3 else ""
        for k in VOCAB:
            if k in s:
                c[k] += 1
                break
        else:
            c["unclassified"] += 1
            unclassified.append(f[1].strip() + ": " + s.strip()[:60])
    return c, len(rows), unclassified


def main():
    c, n, un = count()
    print("=== CLAIMS REGISTER, mechanical count ===")
    for k in VOCAB + ["unclassified"]:
        if c[k]:
            print(f"  {k:14s} {c[k]:4d}")
    print(f"  {'TOTAL ROWS':14s} {n:4d}")
    if un:
        print("\n  rows whose status cell matches no vocabulary term:")
        for u in un:
            print(f"    {u}")


if __name__ == "__main__":
    main()
