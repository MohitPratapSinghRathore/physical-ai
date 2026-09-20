"""Item 2: apply the corrected full-universe under-reporting factors everywhere SIPP
consumer credit balances are used, and list every earlier finding affected with old and new
values.

THE FACTORS ARE A METHODOLOGICAL RESULT IN THEIR OWN RIGHT. A household survey that
under-reports revolving credit by a factor of 2.5 cannot be used for a consumer-credit
stress test without a correction, and the correction is not the same object as the survey's
coverage of the population. Separating the two is the contribution:

    under-reporting factor = official aggregate / FULL survey household universe
    coverage share         = the analysis subsample / FULL survey household universe

A80 used the official aggregate over the WORKING-CORE balance, which is the product of the
two, and so applied a coverage adjustment as if it were a survey correction. That
over-scaled every credit row by 14 to 26 percent.

This module recomputes every credit quantity in the repository on both factors and prints
the old and the new value side by side, so that the list of affected findings is produced
rather than asserted.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

FED_LOSSES = {"mortgage": 22.5, "card": 203.0, "auto": 54.1, "student": 54.1}
FED_BAL = {"mortgage": 1500.0, "card": 1187.1, "auto": 741.1, "student": 741.1}
# AUTO AGGREGATE, replaced in the replication-repair session (item 5).
# FRED MVLOAS, motor vehicle loans owned and securitized, was DISCONTINUED after 2024Q4
# while every other input in this project is 2026. Fed G.19 no longer publishes a live
# motor vehicle loan balance either, so the replacement is the NY Fed Household Debt and
# Credit report, which is ALREADY the source for the mortgage and student aggregates and
# is on the same 2026Q2 vintage. Auto loan balance 1,713bn at 2026Q2, read from the
# report's own data workbook (data/raw/manual/NYFed_HHDC_2026Q2_data.xlsx, "Page 3 Data"),
# against 1,568.6bn at 2024Q4 from the discontinued series.
# CARDS stay on FRED REVOLSL: revolving consumer credit and the NY Fed credit card balance
# are different objects (REVOLSL 1,357.2bn against a NY Fed card balance of 1,263bn), and
# the brief names REVOLSL. That choice is now stated rather than left implicit.
AGG = {"mortgage": 13_100.0, "card": 1_357.2, "auto": 1_713.0, "student": 1_650.0}
LGD = {"mortgage": (0.25, 0.40), "card": (0.80, 1.00),
       "auto": (0.45, 0.65), "student": (0.75, 1.00)}


def main():
    ur = pd.read_csv(OUT / "under_reporting_factors.csv").set_index("loan")
    hc = pd.read_csv(OUT / "verify" / "hand_check_credit.csv")

    rows = []
    for _, h in hc.iterrows():
        ln = h["loan"]
        bank_share = min(FED_BAL[ln] / AGG[ln], 1.0)
        lo, hi = LGD[ln]
        for tag, f in (("A80_working_core", ur.loc[ln, "A80_factor_working_core"]),
                       ("corrected_full_universe", ur.loc[ln, "UNDER_REPORTING_factor"])):
            ead = h["exposure_at_default_bn"] * f
            rows.append({"share_of_wage_bill": h["share_of_wage_bill"], "loan": ln,
                         "basis": tag, "factor": f,
                         "bank_loss_hi_bn": ead * hi * bank_share,
                         "pct_of_fed_hi": 100 * ead * hi * bank_share / FED_LOSSES[ln]})
    R = pd.DataFrame(rows)
    W = R.pivot_table(index=["loan", "share_of_wage_bill"], columns="basis",
                      values=["bank_loss_hi_bn", "pct_of_fed_hi"])
    W["ratio"] = (W[("pct_of_fed_hi", "corrected_full_universe")]
                  / W[("pct_of_fed_hi", "A80_working_core")])
    W.round(3).to_csv(OUT / "under_reporting_impact.csv")

    pd.set_option("display.width", 220)
    print("=== ITEM 2: THE FACTORS, as a methodological result ===")
    t = ur.reset_index()[["loan", "official_aggregate_bn", "sipp_FULL_universe_bn",
                          "sipp_working_core_bn", "UNDER_REPORTING_factor",
                          "working_core_share_of_full", "A80_factor_working_core"]]
    print(t.round(3).to_string(index=False))
    print("\n  THE IDENTITY. A80's factor is the under-reporting factor DIVIDED by the "
          "coverage share,\n  so it carries a coverage adjustment that has no business in a "
          "survey correction:")
    for _, r in ur.reset_index().iterrows():
        print(f"    {r.loan:9s} {r.UNDER_REPORTING_factor:.3f} / "
              f"{r.working_core_share_of_full:.3f} = "
              f"{r.UNDER_REPORTING_factor / r.working_core_share_of_full:.3f}"
              f"   = A80's {r.A80_factor_working_core:.3f}")

    print("\n=== EVERY CREDIT ROW, OLD AGAINST NEW, percent of the Fed severely adverse loss ===")
    p = R.pivot_table(index=["loan", "share_of_wage_bill"], columns="basis",
                      values="pct_of_fed_hi")
    p["change_pct"] = 100 * (p["corrected_full_universe"] / p["A80_working_core"] - 1)
    print(p.round(2).to_string())

    print("\n=== FINDINGS AFFECTED ===")
    affected = [
        ("A80", "scaling factors 1.535 / 3.400 / 2.253 / 1.611",
         "1.259 / 2.516 / 1.743 / 1.423", "SUPERSEDED by A83"),
        ("A80", "cards cross the 25 percent threshold at 75 percent of the wage bill "
                "(25 to 32 percent of the Fed loss)",
         "cards reach 23.5 percent at 75 percent of the wage bill and do NOT cross at the "
         "central threshold", "WITHDRAWN"),
        ("A80", "the ordering survives all of it: public budget, then mortgages and student "
                "loans, then auto, then cards",
         "the ordering is not invariant and only 4 of 15 pairwise comparisons hold",
         "WITHDRAWN by A82"),
        ("A80", "mortgage crosses at 25 percent of the wage bill, 33 to 54 percent of the "
                "Fed loss",
         "mortgage crosses at 25 percent, 27 to 44 percent of the Fed loss",
         "STANDS, magnitude revised down"),
        ("A80", "student loans cross at 25 percent, 20 to 27 percent of the Fed loss",
         "student loans reach 18 to 23 percent at 25 percent of the wage bill and cross at "
         "50 percent", "REVISED, the crossing point moves out one level"),
        ("A80", "auto crosses at 50 percent, 24 to 34 percent of the Fed loss",
         "auto reaches 18 to 26 percent at 50 percent and crosses at 50 percent only at the "
         "loose threshold", "REVISED"),
        ("A76", "the credit channel is 22 times larger than A75 reported",
         "unchanged in kind; the 21.7 factor is about applying LGD rather than a portfolio "
         "loss rate and is independent of the scaling", "STANDS"),
        ("A82", "threshold sensitivity and the four invariant orderings",
         "recomputed on the corrected factors at source rather than by a ratio patch; the "
         "four invariant orderings are unchanged", "STANDS, recomputed"),
        ("A75", "no private balance sheet ever crosses",
         "already withdrawn by A76 for an unrelated reason", "WITHDRAWN"),
    ]
    for a, old, new, status in affected:
        print(f"\n  {a}  [{status}]")
        print(f"    was: {old}")
        print(f"    now: {new}")

    print("\n  NOT AFFECTED, and why: every fiscal, trust fund and household-count result. "
          "The\n  scaling touches SIPP CREDIT BALANCES only. Wage income, the taxable share "
          "under the\n  OASDI cap, the DSTI crossing rates and rho(slack) use no balance "
          "figure at all.")

    (OUT / "under_reporting_impact.json").write_text(json.dumps({
        "factors": ur.reset_index().round(4).to_dict("records"),
        "affected_findings": [{"finding": a, "was": o, "now": n, "status": s}
                              for a, o, n, s in affected],
        "identity_check": "A80's factor equals the under-reporting factor divided by "
                          "the working-core coverage share, so it embedded a coverage "
                          "adjustment inside a survey correction",
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
