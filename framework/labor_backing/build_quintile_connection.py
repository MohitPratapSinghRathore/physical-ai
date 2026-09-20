"""B5 (by wage quintile) and B8 (the connection test). PROVISIONAL throughout.

B5. The labour backing of claims ATTRIBUTABLE to each wage quintile. The quintiles are
    the paper's organising dimension (claim 175), so the ratio is cut the same way. The
    quintile shares are SIPP working-core balances, which are the same balances the
    dose-response table uses, carrying the CORRECTED under-reporting factors.

B8. The connection test. The stock of a claim class whose first-round servicing income
    is removed by a dose is

        impaired_stock = direct labour backing  x  dose  x  (1 - R)

    where dose is the share of the TOTAL WAGE BILL displaced and R is the retained wage
    share at that dose. This is a STOCK. The dose-response table reports a FLOW of
    losses. The two are reconciled by an implied annual loss rate on impaired claims,

        implied_loss_rate = dose_response_loss / impaired_stock

    which should sit near (probability of default uplift) x (loss given default). The
    Gerardi, Herkenhoff, Ohanian and Willen one-earner uplift is 5.0 points and the loss
    given default ranges used in the table are mortgage 0.25 to 0.40, card 0.80 to 1.00,
    auto 0.45 to 0.65, student 0.75 to 1.00. So the household benchmark band is roughly
    0.0125 to 0.05. Anything far outside that band is a GAP and the reason is reported.

PLAUSIBILITY BOUNDS: quintile shares sum to 1 within each class; every impaired stock is
at or below the class labour-backed stock; every implied loss rate lies in [0, 1].
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[1]
PROC = ROOT / "data" / "processed"

import config as C

QLABEL = {0: "Q1_bottom", 1: "Q2", 2: "Q3_middle", 3: "Q4", 4: "Q5_top"}
# household claim class -> the SIPP quintile balance column that distributes it
QCOL = {"home_mortgage": "mortgage_balance_bn", "credit_card": "card_balance_bn",
        "auto_loan": "auto_balance_bn", "student_loan": "student_balance_bn",
        "other_consumer": "card_balance_bn"}
LGD = {"home_mortgage": (0.25, 0.40), "credit_card": (0.80, 1.00),
       "auto_loan": (0.45, 0.65), "student_loan": (0.75, 1.00)}
GHOW_ONE_EARNER = 0.050


def main():
    cls = pd.read_csv(HERE / "claim_class_rules.csv").set_index("claim_class")
    summ = json.loads((HERE / "direct_ratio_latest.json").read_text())
    Q = pd.read_csv(PROC / "sipp_by_wage_quintile.csv")
    qsum = json.loads((PROC / "wage_quintile_summary.json").read_text())
    wshare = {int(k): v for k, v in qsum["quintile_wage_bill_shares"].items()}

    lb = {k: v["labour_backed_bn"] for k, v in summ["by_class"].items()}

    # ---------------- B5
    rows = []
    for _, r in Q.iterrows():
        q = int(r["q"])
        for k, col in QCOL.items():
            sh = float(r[col]) / float(Q[col].sum())
            rows.append(dict(wage_quintile=QLABEL[q], q=q, claim_class=k,
                             quintile_share_of_class=round(sh, 6),
                             class_labour_backed_bn=lb[k],
                             quintile_labour_backed_bn=round(lb[k] * sh, 2),
                             quintile_wage_bill_share=wshare[q]))
    B5 = pd.DataFrame(rows)
    agg = B5.groupby(["wage_quintile", "q", "quintile_wage_bill_share"], as_index=False)[
        "quintile_labour_backed_bn"].sum().sort_values("q")
    agg["share_of_household_labour_backed"] = (
        agg["quintile_labour_backed_bn"] / agg["quintile_labour_backed_bn"].sum()).round(6)
    # claims carried per dollar of wage bill: the quintile's exposure intensity
    agg["labour_backed_per_unit_wage_bill"] = (
        agg["share_of_household_labour_backed"] / agg["quintile_wage_bill_share"]).round(4)
    B5.to_csv(HERE / "quintile_labour_backing_by_class.csv", index=False)
    agg.to_csv(HERE / "quintile_labour_backing.csv", index=False)

    # ---------------- B8
    cases = pd.read_csv(PROC / "cases_A_and_B.csv")
    dr = pd.read_csv(PROC / "dose_response_first_round.csv")
    dr = dr[(dr.incidence == "c_sourced_mix") & (dr.horizon_years == 10)]

    # dose-response loss column for each claim class we can compare
    LOSSCOL = {"home_mortgage": "mortgage_national_loss_hi_bn",
               "auto_loan": "auto_lenders_loss_hi_bn",
               "credit_card": "card_consumer_lenders_loss_hi_bn",
               "student_loan": "student_loan_holders_loss_hi_bn"}

    crows = []
    for _, c in cases.iterrows():
        et, dose, R = c["exposure_type"], float(c["dose"]), float(c["R"])
        d = dr[(dr.exposure_type == et) & (dr.dose_share_of_total_wage_bill == dose)]
        if d.empty:
            continue
        d = d.iloc[0]
        for k in ["home_mortgage", "credit_card", "auto_loan", "student_loan",
                  "multifamily_mortgage", "treasury"]:
            impaired = lb[k] * dose * (1.0 - R)
            # VARIANT, and it matters. (1 - R) is the fraction of wage income actually
            # lost after reemployment, which is the right adjustment for a REVENUE
            # claim. It is the wrong adjustment for a CREDIT claim: a displaced
            # borrower's whole balance is at risk of default, not the lost-income
            # fraction of it. The no-R variant is therefore the right comparator for the
            # household classes and the with-R version for the fiscal class.
            impaired_noR = lb[k] * dose
            row = dict(exposure_type=et, dose=dose, retained_wage_share_R=R,
                       claim_class=k, class_labour_backed_bn=lb[k],
                       impaired_stock_bn=round(impaired, 2),
                       impaired_stock_no_R_bn=round(impaired_noR, 2),
                       inside_observed_data_range=bool(c["inside_observed_data_range"]))
            if k in LOSSCOL:
                loss = float(d[LOSSCOL[k]])
                row["dose_response_loss_bn"] = round(loss, 3)
                row["implied_annual_loss_rate_on_impaired"] = (
                    round(loss / impaired, 6) if impaired > 0 else np.nan)
                row["implied_rate_no_R"] = (
                    round(loss / impaired_noR, 6) if impaired_noR > 0 else np.nan)
                lo, hi = LGD[k]
                row["benchmark_lo"] = round(GHOW_ONE_EARNER * lo, 6)
                row["benchmark_hi"] = round(GHOW_ONE_EARNER * hi, 6)
                row["inside_benchmark_band"] = bool(
                    impaired > 0 and row["benchmark_lo"] <= row["implied_annual_loss_rate_on_impaired"]
                    <= row["benchmark_hi"])
                row["inside_benchmark_band_no_R"] = bool(
                    impaired_noR > 0 and row["benchmark_lo"] <= row["implied_rate_no_R"]
                    <= row["benchmark_hi"])
            elif k == "treasury":
                loss = float(d["public_budget_loss_hi_bn"])
                row["dose_response_loss_bn"] = round(loss, 3)
                row["implied_annual_loss_rate_on_impaired"] = (
                    round(loss / impaired, 6) if impaired > 0 else np.nan)
                row["implied_rate_no_R"] = (
                    round(loss / impaired_noR, 6) if impaired_noR > 0 else np.nan)
                row["benchmark_lo"] = np.nan
                row["benchmark_hi"] = np.nan
                row["inside_benchmark_band"] = False
                row["inside_benchmark_band_no_R"] = False
            elif k == "multifamily_mortgage":
                row["dose_response_loss_bn"] = np.nan
                row["implied_rate_no_R"] = np.nan
                row["implied_annual_loss_rate_on_impaired"] = np.nan
                row["benchmark_lo"] = np.nan
                row["benchmark_hi"] = np.nan
                row["inside_benchmark_band"] = False
                row["inside_benchmark_band_no_R"] = False
            crows.append(row)
    B8 = pd.DataFrame(crows)
    B8.to_csv(HERE / "connection_test.csv", index=False)

    inside = B8[B8.inside_observed_data_range & B8.claim_class.isin(LOSSCOL)]
    agree = inside.groupby("claim_class").agg(
        n=("inside_benchmark_band", "size"),
        n_inside_band=("inside_benchmark_band", "sum"),
        n_inside_band_no_R=("inside_benchmark_band_no_R", "sum"),
        implied_rate_min=("implied_annual_loss_rate_on_impaired", "min"),
        implied_rate_max=("implied_annual_loss_rate_on_impaired", "max"),
        implied_no_R_min=("implied_rate_no_R", "min"),
        implied_no_R_max=("implied_rate_no_R", "max"),
        benchmark_lo=("benchmark_lo", "min"), benchmark_hi=("benchmark_hi", "max")
    ).reset_index()
    agree.to_csv(HERE / "connection_agreement.csv", index=False)

    # ---------------- plausibility
    checks = []

    def chk(n, ok, d):
        checks.append(dict(check=n, verdict="OK" if ok else "VIOLATION", detail=d))

    for k, g in B5.groupby("claim_class"):
        s = g["quintile_share_of_class"].sum()
        chk(f"quintile shares sum to 1: {k}", abs(s - 1) < 1e-5, f"{s:.8f}")
    chk("quintile wage bill shares sum to 1",
        abs(sum(wshare.values()) - 1) < 1e-3, f"{sum(wshare.values()):.6f}")
    bad = B8[B8.impaired_stock_bn > B8.class_labour_backed_bn + 1e-6]
    chk("impaired stock <= class labour-backed stock", bad.empty,
        f"{len(bad)} rows above")
    r = B8["implied_annual_loss_rate_on_impaired"].dropna()
    chk("implied loss rates in [0,1]", bool(((r >= 0) & (r <= 1)).all()),
        f"min {r.min():.4f} max {r.max():.4f}")
    P = pd.DataFrame(checks).sort_values("verdict")
    P.to_csv(HERE / "plausibility_quintile_connection.csv", index=False)

    print("=== B5 labour backing by wage quintile ===")
    print(agg.to_string(index=False))
    print("\n=== B8 connection test, rows INSIDE the observed data range ===")
    print(agree.to_string(index=False))
    print(f"\nplausibility: {len(P)} checks, {(P.verdict=='VIOLATION').sum()} violations")
    if (P.verdict == "VIOLATION").any():
        print(P[P.verdict == "VIOLATION"].to_string(index=False))


if __name__ == "__main__":
    main()
