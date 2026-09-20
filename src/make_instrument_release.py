"""Write data/release/architecture/instruments.csv from the instrument table.

The architecture note carries one row per instrument in a markdown table. The
appendix table in the manuscript is generated from this released CSV rather than
retyped, so the two cannot drift apart.

Run:  python src/make_instrument_release.py
"""
import csv
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "framework" / "architecture.md"
OUT = ROOT / "data" / "release" / "architecture" / "instruments.csv"

FIELDS = ["n", "mechanism", "institution", "instrument", "type", "precedent",
          "trigger_and_current_value", "binds_in", "gap_closure"]


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def main():
    rows, seen_header = [], False
    for line in SRC.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            if seen_header and rows:
                break
            continue
        c = cells(line)
        if len(c) != len(FIELDS):
            continue
        if c[0] == "#":
            seen_header = True
            continue
        if set(c[0]) <= set("-: "):
            continue
        if seen_header and c[0].isdigit():
            rows.append(dict(zip(FIELDS, c)))
    assert len(rows) == 12, f"expected twelve instruments, parsed {len(rows)}"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT.relative_to(ROOT)} with {len(rows)} instruments")


if __name__ == "__main__":
    main()
