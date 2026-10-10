"""
Option 1: map labour-backed claims to their regulatory capital treatment.

Risk weights are quoted from 12 CFR 217.32 (US Basel III standardised approach),
verified from primary text:
  217.32(a)(1)(i)  US government, central bank, US government agency      0%
  217.32(a)(1)(i)  directly and unconditionally guaranteed by US govt     0%
  217.32(c)(1)     GSE exposure other than equity or preferred stock     20%
  217.32(e)        general obligation of a US public sector entity       20%
  217.32(g)(1)     first-lien residential mortgage, prudent underwriting 50%
  217.32(g)(2)     other first-lien and all junior-lien residential     100%
  217.32(f)(1)     corporate exposures                                  100%
  217.32(l)(3)     equity exposure to a publicly traded entity          300%

Concentration: 12 CFR 252.77 exempts direct claims on, and portions fully
guaranteed by, Fannie Mae and Freddie Mac while in FHFA conservatorship, among
other categories.

COMPUTES A MAPPING, NOT AN ESTIMATE.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

# risk weight applied by a REGULATED BANK holding the claim, by claim class.
# Where a class is held in more than one legal form the range is given and the
# central column is the form in which most of the class actually sits.
RW = {
    "treasury":                   dict(central=0.00, lo=0.00, hi=0.00,
                                       cite="217.32(a)(1)(i)",
                                       form="direct US government obligation"),
    "home_mortgage":              dict(central=0.20, lo=0.00, hi=1.00,
                                       cite="217.32(a)(1)(i), (c)(1), (g)",
                                       form="mostly agency MBS at 20pct; "
                                            "Ginnie 0pct; whole loan 50pct"),
    "multifamily_mortgage":       dict(central=0.50, lo=0.20, hi=1.00,
                                       cite="217.32(c)(1), (g)",
                                       form="agency multifamily 20pct, "
                                            "whole loan 50 to 100pct"),
    "student_loan":               dict(central=0.00, lo=0.00, hi=1.00,
                                       cite="217.32(a)(1)(i)",
                                       form="97pct federally held Direct "
                                            "Loans, no bank capital at all"),
    "credit_card":                dict(central=1.00, lo=1.00, hi=1.00,
                                       cite="217.32(f)(1)", form="bank held"),
    "auto_loan":                  dict(central=1.00, lo=1.00, hi=1.00,
                                       cite="217.32(f)(1)", form="bank held"),
    "other_consumer":             dict(central=1.00, lo=1.00, hi=1.00,
                                       cite="217.32(f)(1)", form="bank held"),
    "state_local_debt":           dict(central=0.20, lo=0.20, hi=0.50,
                                       cite="217.32(e)",
                                       form="general obligation 20pct, "
                                            "revenue 50pct"),
    "corporate_bonds":            dict(central=1.00, lo=1.00, hi=1.00,
                                       cite="217.32(f)(1)", form="corporate"),
    "corporate_loans":            dict(central=1.00, lo=1.00, hi=1.00,
                                       cite="217.32(f)(1)", form="corporate"),
    "noncorporate_business_debt": dict(central=1.00, lo=1.00, hi=1.00,
                                       cite="217.32(f)(1)", form="corporate"),
    "commercial_mortgage":        dict(central=1.00, lo=1.00, hi=1.50,
                                       cite="217.32(f)(1), (j) HVCRE",
                                       form="CRE 100pct, HVCRE 150pct"),
    "corporate_equity":           dict(central=3.00, lo=1.00, hi=6.00,
                                       cite="217.52, 217.53",
                                       form="publicly traded equity"),
}

# exempt from the single-counterparty credit limit, 12 CFR 252.77
SCCL_EXEMPT = {"treasury": True, "home_mortgage": True,
               "multifamily_mortgage": True, "student_loan": True,
               "state_local_debt": False, "credit_card": False,
               "auto_loan": False, "other_consumer": False,
               "corporate_bonds": False, "corporate_loans": False,
               "noncorporate_business_debt": False,
               "commercial_mortgage": False, "corporate_equity": False}


def main():
    rules = pd.read_csv(ROOT / "framework" / "labor_backing"
                        / "claim_class_rules.csv")
    rules["labour_backed_bn"] = (rules["level_bn"]
                                 * rules["labour_backing_share"])
    rules["rw_central"] = rules["claim_class"].map(
        lambda c: RW[c]["central"])
    rules["rw_lo"] = rules["claim_class"].map(lambda c: RW[c]["lo"])
    rules["rw_hi"] = rules["claim_class"].map(lambda c: RW[c]["hi"])
    rules["rw_cite"] = rules["claim_class"].map(lambda c: RW[c]["cite"])
    rules["rw_form"] = rules["claim_class"].map(lambda c: RW[c]["form"])
    rules["sccl_exempt"] = rules["claim_class"].map(SCCL_EXEMPT)

    lb = rules["labour_backed_bn"]
    tot_lb = float(lb.sum())
    tot_claims = float(rules["level_bn"].sum())

    # share of LABOUR-BACKED claims at or below 20 percent risk weight
    low = rules["rw_central"] <= 0.20
    share_low = float(lb[low].sum() / tot_lb)
    share_zero = float(lb[rules["rw_central"] == 0.0].sum() / tot_lb)
    share_exempt = float(lb[rules["sccl_exempt"]].sum() / tot_lb)

    # the same shares over ALL claims, for contrast
    share_low_all = float(rules.loc[low, "level_bn"].sum() / tot_claims)

    # labour-backing-weighted mean risk weight, against the claim-weighted one
    lbw_rw = float((rules["rw_central"] * lb).sum() / tot_lb)
    clw_rw = float((rules["rw_central"] * rules["level_bn"]).sum()
                   / tot_claims)

    # THE SHARPER TEST: across classes, does a higher labour backing coefficient
    # go with a LOWER risk weight? Claim-size weighted and unweighted.
    x = rules["labour_backing_share"].to_numpy()
    y = rules["rw_central"].to_numpy()
    w = rules["level_bn"].to_numpy()
    r_unw = float(np.corrcoef(x, y)[0, 1])
    mx, my = np.average(x, weights=w), np.average(y, weights=w)
    cov = np.average((x - mx) * (y - my), weights=w)
    r_w = float(cov / np.sqrt(np.average((x - mx) ** 2, weights=w)
                              * np.average((y - my) ** 2, weights=w)))
    # excluding equity, whose 300 percent weight dominates any correlation
    m = rules["claim_class"] != "corporate_equity"
    r_unw_noeq = float(np.corrcoef(x[m], y[m])[0, 1])

    res = {
        "total_claims_bn": tot_claims,
        "total_labour_backed_bn": tot_lb,
        "share_of_labour_backed_at_rw_le_20pct": share_low,
        "share_of_labour_backed_at_rw_zero": share_zero,
        "share_of_labour_backed_sccl_exempt": share_exempt,
        "share_of_ALL_claims_at_rw_le_20pct": share_low_all,
        "labour_backed_weighted_mean_rw": lbw_rw,
        "claim_weighted_mean_rw": clw_rw,
        "corr_labour_backing_vs_risk_weight_unweighted": r_unw,
        "corr_labour_backing_vs_risk_weight_claim_weighted": r_w,
        "corr_excluding_corporate_equity_unweighted": r_unw_noeq,
        "criterion3_threshold": 0.50,
        "criterion3_met": bool(share_low > 0.50),
    }
    rules.to_csv(OUT / "risk_weight_map.csv", index=False)
    (OUT / "risk_weight_map.json").write_text(
        json.dumps(res, indent=2, default=float), encoding="utf-8")

    cols = ["claim_class", "level_bn", "labour_backing_share",
            "labour_backed_bn", "rw_central", "sccl_exempt", "rw_form"]
    print(rules[cols].sort_values("labour_backed_bn", ascending=False)
          .to_string(index=False))
    print()
    for k, v in res.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
