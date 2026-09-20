"""Closing pass item 2. Realised capital gains inside the receipts split, sourced and bounded.

THE PROBLEM, restated. The labour-linked share of federal receipts is built as

    (social insurance contributions in full) + (w x federal personal current taxes)
    -------------------------------------------------------------------------------
                            federal current receipts

with w the SOI wage share of AGI. **Realised capital gains sit inside AGI**, so w is pushed
down by them, and the construction implicitly taxes a dollar of capital gain at the same rate
as a dollar of wages. It does not: long-term gains bear preferential rates. **The current
construction therefore UNDERSTATES the labour-linked share of the individual income tax**,
and the limitation has until now read "capital gains receipts are unsourced".

THE BOUND, now sourced. IRS Statistics of Income Table 1.4, "All Returns: Sources of Income,
Adjustments, and Tax Items, by Size of Adjusted Gross Income", 2021 to 2023, already in
data/raw/irs/. Realised gains are taken as capital gain distributions reported on Form 1040
(col 36) plus taxable net gain from Schedule D (col 38) less taxable net loss (col 40).

  LOWER BOUND, the current construction: w = wages / AGI. A dollar of gain is treated as
    bearing the same tax as a dollar of wages.
  UPPER BOUND: w = wages / (AGI less realised gains). Gains are removed from the taxable base
    entirely, which is the limit at which they bear no tax at all.

The truth is between: gains bear a positive but preferential rate. Neither end is asserted as
the answer, and the width of the band is the honest statement of what we do not know.

ONE THING THE SOURCING REVEALS, and it is the same lesson as the debt-only ratio. Realised
gains swing violently: 15.4 percent of AGI in 2021, 6.2 percent in 2023. **The wage share of
AGI swings with them, 0.610 to 0.668. The wage share EXCLUDING gains does not: 0.712 to
0.721 across the same three years.** So the upper bound is not only an upper bound, it is the
more stable series.
"""
import json
import pathlib

import pandas as pd

HERE = pathlib.Path(__file__).parent
PROC = pathlib.Path(__file__).resolve().parents[2] / "data" / "processed"
IRS = pathlib.Path(__file__).resolve().parents[2] / "data" / "raw" / "irs"

FILES = {2021: "21in14ar.xls", 2022: "22in14ar.xls", 2023: "23in14ar.xls"}
COL = {"agi": 2, "wages": 6, "cg_dist": 36, "cg_gain": 38, "cg_loss": 40}


def soi_year(f):
    d = pd.read_excel(IRS / f, header=None)
    lab = d.iloc[:, 0].astype(str).str.strip().str.lower()
    i = [k for k, v in lab.items() if v == "all returns, total"][0]
    r = d.iloc[i]
    agi = float(r[COL["agi"]]) / 1e6
    wages = float(r[COL["wages"]]) / 1e6
    cg = (float(r[COL["cg_dist"]]) + float(r[COL["cg_gain"]])
          - float(r[COL["cg_loss"]])) / 1e6
    return agi, wages, cg


def main():
    lts = json.loads((PROC / "labor_tax_share.json").read_text())
    socins = lts["fed_social_insurance_contrib_usd_bn"]
    personal = lts["fed_personal_current_taxes_usd_bn"]
    receipts = lts["fed_current_receipts_usd_bn"]

    rows = []
    for y, f in FILES.items():
        agi, wages, cg = soi_year(f)
        w_lo = wages / agi
        w_hi = wages / (agi - cg)
        share_lo = (socins + w_lo * personal) / receipts
        share_hi = (socins + w_hi * personal) / receipts
        rows.append({
            "year": y, "agi_bn": round(agi, 1), "wages_bn": round(wages, 1),
            "realised_capital_gains_bn": round(cg, 1),
            "capital_gains_share_of_agi": round(cg / agi, 4),
            "w_wages_over_agi_LOWER": round(w_lo, 4),
            "w_wages_over_agi_ex_gains_UPPER": round(w_hi, 4),
            "labour_linked_receipts_share_LOWER": round(share_lo, 4),
            "labour_linked_receipts_share_UPPER": round(share_hi, 4),
        })
    D = pd.DataFrame(rows)
    D.to_csv(HERE / "capital_gains_bound.csv", index=False)

    latest = D[D.year == 2023].iloc[0]
    lo = float(latest.labour_linked_receipts_share_LOWER)
    hi = float(latest.labour_linked_receipts_share_UPPER)
    factor = float(latest.w_wages_over_agi_ex_gains_UPPER) / \
        float(latest.w_wages_over_agi_LOWER)

    # ---- downstream: everything that scales with the labour-linked receipts share
    lb = json.loads((HERE / "direct_ratio_latest.json").read_text())
    treas = lb["by_class"]["treasury"]
    treas_lo = treas["backing"]
    # the Treasury backing is socins-in-full plus w x personal over receipts, so raising w
    # raises it by the SAME income-tax component, not proportionally. Rebuild it the same way.
    w_component_lo = (treas_lo * receipts - socins) / personal
    w_component_hi = min(w_component_lo * factor, 1.0)
    treas_hi = (socins + w_component_hi * personal) / receipts

    lb_bn = lb["labour_backed_bn"]
    d_treas_bn = treas["level_bn"] * (treas_hi - treas_lo)
    lb_bn_hi = lb_bn + d_treas_bn
    sov = lb["sovereign_exposure"]
    union_hi = (sov["labour_backed_sovereign_exposure_bn"] + d_treas_bn) / lb_bn_hi
    ratio_hi = lb_bn_hi / lb["total_claims_bn"]

    out = {
        "status": "MEASURED from IRS SOI Table 1.4, 2021 to 2023. Reported as a BOUND, not "
                  "a point: the truth lies between, because gains bear a positive but "
                  "preferential rate.",
        "source": "IRS Statistics of Income Table 1.4, All Returns: Sources of Income, "
                  "Adjustments, and Tax Items, by Size of Adjusted Gross Income",
        "by_year": rows,
        "capital_gains_share_of_agi_range": [
            round(float(D.capital_gains_share_of_agi.min()), 4),
            round(float(D.capital_gains_share_of_agi.max()), 4)],
        "wage_share_of_agi_range": [round(float(D.w_wages_over_agi_LOWER.min()), 4),
                                    round(float(D.w_wages_over_agi_LOWER.max()), 4)],
        "wage_share_EX_GAINS_range": [
            round(float(D.w_wages_over_agi_ex_gains_UPPER.min()), 4),
            round(float(D.w_wages_over_agi_ex_gains_UPPER.max()), 4)],
        "labour_linked_receipts_share_2023": {"lower": lo, "upper": round(hi, 4)},
        "downstream_2025": {
            "treasury_class_backing": {"lower": round(treas_lo, 6),
                                       "upper": round(treas_hi, 6)},
            "all_claims_labour_backing_ratio": {
                "lower": lb["direct_labour_backing_ratio"], "upper": round(ratio_hi, 6)},
            "sovereign_union_share": {"lower": sov["share_union"],
                                      "upper": round(union_hi, 6)},
        },
        "stability_point": "Realised gains swing from 15.4 pct of AGI in 2021 to 6.2 pct in "
                           "2023, and the wage share of AGI swings with them (0.610 to "
                           "0.668). The wage share EXCLUDING gains barely moves (0.712 to "
                           "0.721). The upper bound is also the more stable series.",
        "limitation_wording_NEW": "Realised capital gains are 6.2 to 15.4 percent of AGI "
                                  "(IRS SOI 2021 to 2023) and bear preferential rates, so "
                                  "the labour-linked share of federal receipts is a BOUND, "
                                  "0.634 to 0.653 on 2023 data, not a point. Every fiscal "
                                  "magnitude that scales with it carries that band. The "
                                  "sovereign share moves by under 1 percent across it.",
    }
    (HERE / "capital_gains_bound.json").write_text(json.dumps(out, indent=2))

    pd.set_option("display.width", 220)
    print(D.to_string(index=False))
    print()
    print(f"labour-linked receipts share, 2023: {lo:.4f} to {hi:.4f} "
          f"(band {100*(hi/lo-1):.2f} pct wide)")
    print(f"Treasury class backing:  {treas_lo:.6f} to {treas_hi:.6f}")
    print(f"all-claims labour backing ratio: {lb['direct_labour_backing_ratio']:.6f} to "
          f"{ratio_hi:.6f}")
    print(f"sovereign union share:   {sov['share_union']:.6f} to {union_hi:.6f}  "
          f"({100*(union_hi/sov['share_union']-1):+.2f} pct)")


if __name__ == "__main__":
    main()
