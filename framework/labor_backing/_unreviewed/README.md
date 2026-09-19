# QUARANTINED. Nothing in the pipeline may read from this directory.

Everything formerly in `framework/labor_backing/` was moved here on owner instruction after
the parallel session that produced most of it was closed. `framework/labor_backing/` itself
is now empty and stays empty.

## Why

The computation files were **built on fiscal inputs that have since been superseded four
times**: the A70 amortisation error (corrected in A72), the A75 loss conversion error
(corrected in A76), the saturated fiscal columns (corrected in A77), and the trust fund
denominator error that violated a plausibility bound (corrected in A79). Any labour backing
ratio computed on those inputs inherits all four.

## One file has a different status and it is recorded here so it is not lost

`feasibility.md` is **the reviewed specification**, not a computation. It was written and
reviewed in a working session, it contains no superseded fiscal numbers, and it is the
document Part B should be rerun against. It is here only because the instruction was to clear
the directory completely. **It is not suspect; the computation files are.**

## Contents

| File | Status |
|---|---|
| feasibility.md | **REVIEWED SPECIFICATION**, safe, see above |
| build_labor_backing.py | unreviewed computation |
| sipp_wage_backed_shares.py | unreviewed computation |
| connect_to_results.py | unreviewed computation |
| make_figure.py | unreviewed computation |
| claim_classes.csv | unreviewed output |
| holders.csv | unreviewed output |
| labor_backing_summary.json | unreviewed output |
| ratio_time_series.csv | unreviewed output |
| sipp_wage_backed_shares.csv | unreviewed output |
| sipp_wage_backed_shares.json | unreviewed output |
| connection_table.csv | unreviewed output |
| connection_diagnostics.json | unreviewed output |
| fig_labour_backing_ratio.png | unreviewed figure |

More files were present than the previous quarantine recorded: the parallel session had
produced a figure and a set of connection diagnostics before it was closed. All are here.

Part B will be rerun from scratch in its own session against `feasibility.md`.
