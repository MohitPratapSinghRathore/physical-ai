"""
Run-instruction item 2: reconciliation for ten randomly chosen banks, showing the
raw fields and the constructed twelve-quarter totals.

Shows one class that uses a quarterly field (nt_reres / NTRERESQ) and one that must
be differenced from year-to-date (nt_conoth / NTCONOTH), so both branches of the
section 14.4 rule are visible.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"
WINDOW = [(y, q) for y in (2015, 2016, 2017) for q in (1, 2, 3, 4)]
SEED = 20260921


def main():
    oc = pd.read_csv(RAW / "fdic_outcomes_quarterly.csv")
    frame = pd.read_csv(RAW / "analysis_frame_preshock.csv")
    elig = frame[(~frame["excluded"]) & frame["qual_hh"]]["CERT"]
    win = oc[oc.apply(lambda r: (r["year"], r["q"]) in WINDOW, axis=1)]
    full = win.groupby("CERT").size()
    cands = sorted(set(elig) & set(full[full == 12].index))
    rng = np.random.default_rng(SEED)
    picks = rng.choice(cands, size=10, replace=False)

    lines = []
    lines.append("# YTD reconciliation, ten randomly chosen banks")
    lines.append("")
    lines.append(f"Seed {SEED}. Drawn from the {len(cands)} primary-sample banks "
                 "with all twelve window quarters present.")
    lines.append("")
    lines.append("`NTRERESQ` is a quarterly field and is used as reported. "
                 "`NTCONOTH` has no quarterly field, so it is year-to-date and "
                 "is differenced within each calendar year "
                 "(Q1 = Q1ytd; Q2 = Q2ytd − Q1ytd; and so on). "
                 "YTD values are never summed across quarters.")
    lines.append("")

    for cert in picks:
        d = win[win["CERT"] == cert].sort_values(["year", "q"])
        lines.append(f"## CERT {cert}")
        lines.append("")
        lines.append("| year | q | NTRERESQ (raw, quarterly) | nt_reres_q (used) "
                     "| NTCONOTH (raw, YTD) | nt_conoth_q (constructed) |")
        lines.append("|---|---|---|---|---|---|")
        for _, r in d.iterrows():
            lines.append(
                f"| {int(r['year'])} | {int(r['q'])} | {r['NTRERESQ']:.0f} | "
                f"{r['nt_reres_q']:.0f} | {r['NTCONOTH']:.0f} | "
                f"{r['nt_conoth_q']:.0f} |")
        s_res = d["nt_reres_q"].sum()
        s_con = d["nt_conoth_q"].sum()
        naive = d["NTCONOTH"].sum()
        lines.append("")
        lines.append(f"- twelve-quarter total, residential: **{s_res:,.0f}**")
        lines.append(f"- twelve-quarter total, other consumer: **{s_con:,.0f}**")
        lines.append(f"- what a naive sum of the YTD column would have given: "
                     f"{naive:,.0f}  "
                     f"(**{naive - s_con:+,.0f}** overstatement avoided)")
        lines.append("")

    # aggregate check of the rule's effect
    naive_all = win["NTCONOTH"].sum()
    correct_all = win["nt_conoth_q"].sum()
    lines.append("## Aggregate effect of applying the rule")
    lines.append("")
    lines.append(f"- Correct (YTD differenced): **{correct_all:,.0f}** $000s")
    lines.append(f"- Naive sum of YTD values: {naive_all:,.0f} $000s")
    lines.append(f"- Overstatement avoided: **{naive_all - correct_all:,.0f}** "
                 f"$000s, a factor of {naive_all / correct_all:.2f}x")
    (OUT / "ytd_reconciliation.md").write_text("\n".join(lines),
                                               encoding="utf-8")
    print("\n".join(lines[:60]))
    print("...")
    print("\n".join(lines[-7:]))


if __name__ == "__main__":
    main()
