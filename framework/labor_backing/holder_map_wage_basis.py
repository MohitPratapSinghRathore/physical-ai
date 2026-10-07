"""Rebuild the holder map on the ADOPTED WAGE BASIS so it reconciles with the claim-class
table.

WHY. The published holder map is built on the coverage construction of the household
coefficients, while the claim-class table is on the adopted wage basis. The two totals
differ by 423.3 billion dollars, so a reader cannot multiply a holder share by the headline
stock. Explaining that in a caption is weaker than removing it.

HOW. The published holder matrix carries, for every claim class and holder, the holder
share of that class and the class level. Holder shares are properties of the Z.1 instrument
and of the consolidation rules; they do not depend on any backing coefficient. So the
adopted-basis map is the same shares applied to the class level times the adopted
coefficient. Nothing else changes, and the coverage-basis column reproduces the published
map exactly, which is the check that the rescaling is faithful.

Run:  python framework/labor_backing/holder_map_wage_basis.py
"""
import json
import pathlib

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / "data" / "release" / "labor_backing" / "holder_map_wage_basis.json"

LABEL = {"federal_government": "Federal government", "banks": "Banks",
         "rest_of_world": "Rest of the world", "other_financial": "Other financial",
         "households": "Households, direct", "state_local_government": "State and local government",
         "insurers": "Insurers", "pensions": "Pension funds",
         "nonfinancial_business": "Nonfinancial business",
         "residual_unallocated": "Unallocated remainder"}


def main():
    H = pd.read_csv(HERE / "holder_matrix_latest.csv")
    b2 = json.loads((ROOT / "data/release/revision_r2/b2_headline_effect.json").read_text())
    adopted = {k: float(v["alternative"]) for k, v in b2["coefficients"].items()}

    # coverage-basis coefficient implied by the matrix itself
    H["beta_coverage"] = H.class_labour_backed_bn / H.class_total_bn
    H["beta_wage"] = H.apply(
        lambda r: adopted.get(r.claim_class, r.beta_coverage), axis=1)
    H["coverage_bn"] = H.holder_share * H.class_total_bn * H.beta_coverage
    H["wage_bn"] = H.holder_share * H.class_total_bn * H.beta_wage

    cov = H.groupby("holder")["coverage_bn"].sum()
    wag = H.groupby("holder")["wage_bn"].sum()
    tc, tw = float(cov.sum()), float(wag.sum())

    # check against the published map
    pub = json.loads((ROOT / "data/release/labor_backing/direct_ratio_latest.json").read_text())
    pub_bn = pub["labour_backed_by_holder_bn"]
    worst = max(abs(float(cov.get(k, 0)) - float(v)) for k, v in pub_bn.items())

    rows = []
    for h in wag.sort_values(ascending=False).index:
        rows.append({"holder": h, "label": LABEL.get(h, h),
                     "coverage_bn": round(float(cov.get(h, 0.0)), 1),
                     "wage_bn": round(float(wag[h]), 1),
                     "coverage_share": round(float(cov.get(h, 0.0)) / tc, 4),
                     "wage_share": round(float(wag[h]) / tw, 4)})

    res = {"description": "Holder map on the adopted wage basis, so that holder amounts sum to "
                          "the wage-backed total reported in the claim-class table. Holder "
                          "shares are properties of the instrument and the consolidation rules "
                          "and do not depend on the backing coefficient.",
           "year": int(H.year.iloc[0]),
           "total_coverage_basis_bn": round(tc, 1),
           "total_wage_basis_bn": round(tw, 1),
           "gap_bn": round(tc - tw, 1),
           "max_abs_deviation_from_published_coverage_map_bn": round(worst, 2),
           "adopted_coefficients": adopted,
           "by_holder": rows}
    OUT.write_text(json.dumps(res, indent=2))

    print(f"reproduces the published coverage map to within {worst:.2f} bn")
    print(f"coverage total {tc:,.1f}   wage-basis total {tw:,.1f}   gap {tc-tw:,.1f}\n")
    print(f"{'holder':26s} {'coverage $bn':>13s} {'wage $bn':>11s} {'cov sh':>8s} {'wage sh':>8s}")
    for r in rows:
        print(f"{r['label']:26s} {r['coverage_bn']:13,.1f} {r['wage_bn']:11,.1f} "
              f"{r['coverage_share']:8.4f} {r['wage_share']:8.4f}")


if __name__ == "__main__":
    main()
