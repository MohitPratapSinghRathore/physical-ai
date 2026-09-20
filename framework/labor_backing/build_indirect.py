"""B2: the INDIRECT extension, reported separately and NEVER blended into the headline.

The direct ratio (B1) sets business-revenue-serviced classes to zero, because the cash
flow that services them is business revenue and not wages. B2 asks the second-round
question instead: what share of business revenue is ultimately funded by labour income.

    indirect labour backing of business revenue
        = consumption's share of final demand  x  labour's share of personal income
        = PCE / GDP                            x  WASCUR / PI

This is the paper's FIRST-ROUND versus SECOND-ROUND distinction expressed as a ratio.
The first-round number says who is paid out of wages now. The second-round number says
who is paid out of revenue that wages generate. They are different objects and a reader
who averages them has the analysis wrong.

WASCUR and not COE, per the standing requirement: compensation of employees includes
employer pension and health contributions, which bear neither the income tax nor the
payroll tax, and tau_l is built on WASCUR.

PLAUSIBILITY BOUNDS: each of the two shares in [0, 1]; their product in [0, 1] and below
each of them; the combined ratio at or above the direct ratio, because the indirect
extension only ever ADDS backing to classes the direct rule set to zero.

PROVISIONAL. Produced in one session.
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
ROOT = HERE.parents[1]
FRED = ROOT / "data" / "raw" / "fred"
LFRED = HERE / "_fred"

import config as C


def ann(path, sid):
    d = pd.read_csv(path / f"{sid}.csv")
    d.columns = [c.strip() for c in d.columns]
    dc, vc = d.columns[0], d.columns[1]
    d[dc] = pd.to_datetime(d[dc])
    d[vc] = pd.to_numeric(d[vc], errors="coerce")
    return d.dropna(subset=[vc]).groupby(d[dc].dt.year)[vc].mean()


def main():
    pce, gdp = ann(LFRED, "PCEC"), ann(FRED, "GDP")
    was, pi = ann(FRED, "WASCUR"), ann(LFRED, "PI")
    years = sorted(set(pce.index) & set(gdp.index) & set(was.index) & set(pi.index))

    D = pd.read_csv(HERE / "direct_ratio_timeseries.csv").set_index("year")
    cls = pd.read_csv(HERE / "claim_class_rules.csv").set_index("claim_class")

    rows = []
    for y in years:
        cons = float(pce[y] / gdp[y])
        lab = float(was[y] / pi[y])
        ind = cons * lab
        r = dict(year=y, consumption_share_of_final_demand=round(cons, 6),
                 labour_share_of_personal_income=round(lab, 6),
                 indirect_labour_backing_of_business_revenue=round(ind, 6))
        if y in D.index:
            r.update(direct_ratio=float(D.loc[y, "direct_labour_backing_ratio"]))
        rows.append(r)
    B = pd.DataFrame(rows)

    # combined extension in the LATEST year only, class by class, so the zero-by-rule
    # classes can be seen taking the indirect share and nothing else moves
    latest = int(D.index.max())
    ind = float(B[B.year == latest]["indirect_labour_backing_of_business_revenue"].iloc[0])
    zero_keys = [c["key"] for c in C.CLASSES if c["backing"] == "zero"]
    tot = float(D.loc[latest, "total_claims_bn"])
    direct_bn = float(D.loc[latest, "labour_backed_bn"])
    zero_bn = float(cls.loc[zero_keys, "level_bn"].sum())
    combined_bn = direct_bn + zero_bn * ind
    B.to_csv(HERE / "indirect_extension_timeseries.csv", index=False)

    out = dict(
        status="PROVISIONAL, reported SEPARATELY, never blended into the B1 headline",
        latest_year=latest,
        consumption_share_of_final_demand=float(
            B[B.year == latest]["consumption_share_of_final_demand"].iloc[0]),
        labour_share_of_personal_income=float(
            B[B.year == latest]["labour_share_of_personal_income"].iloc[0]),
        indirect_labour_backing_of_business_revenue=ind,
        business_revenue_serviced_classes=zero_keys,
        business_revenue_serviced_bn=round(zero_bn, 1),
        direct_labour_backed_bn=round(direct_bn, 1),
        direct_ratio=round(direct_bn / tot, 6),
        combined_first_and_second_round_bn=round(combined_bn, 1),
        combined_first_and_second_round_ratio=round(combined_bn / tot, 6),
        reading="The direct ratio is the first round. The combined ratio adds the second "
                "round and is NOT the headline. The gap between them is the size of the "
                "demand channel on the liability side.",
    )
    (HERE / "indirect_extension.json").write_text(json.dumps(out, indent=1))

    checks = []

    def chk(n, ok, d):
        checks.append(dict(check=n, verdict="OK" if ok else "VIOLATION", detail=d))

    c_, l_ = out["consumption_share_of_final_demand"], out["labour_share_of_personal_income"]
    chk("consumption share in [0,1]", 0 <= c_ <= 1, f"{c_:.4f}")
    chk("labour share of personal income in [0,1]", 0 <= l_ <= 1, f"{l_:.4f}")
    chk("indirect share in [0,1]", 0 <= ind <= 1, f"{ind:.4f}")
    chk("indirect share below each component", ind <= min(c_, l_), f"{ind:.4f}")
    chk("combined ratio >= direct ratio",
        out["combined_first_and_second_round_ratio"] >= out["direct_ratio"],
        f"{out['combined_first_and_second_round_ratio']:.4f} >= {out['direct_ratio']:.4f}")
    chk("combined ratio in [0,1]", 0 <= out["combined_first_and_second_round_ratio"] <= 1,
        f"{out['combined_first_and_second_round_ratio']:.4f}")
    P = pd.DataFrame(checks).sort_values("verdict")
    P.to_csv(HERE / "plausibility_indirect.csv", index=False)

    print(f"latest year {latest}")
    print(f"  consumption share of final demand   {c_:.4f}")
    print(f"  labour share of personal income     {l_:.4f}")
    print(f"  INDIRECT backing of business revenue{ind:>8.4f}")
    print(f"  direct ratio (B1, the headline)     {out['direct_ratio']:.4f}")
    print(f"  combined, NOT the headline          {out['combined_first_and_second_round_ratio']:.4f}")
    print(f"  series {B.year.min()} to {B.year.max()}")
    print(f"  plausibility: {len(P)} checks, {(P.verdict=='VIOLATION').sum()} violations")


if __name__ == "__main__":
    main()
