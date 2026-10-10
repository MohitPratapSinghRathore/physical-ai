"""
Run steps (e), (f), (g): arrangements, sensitivities and the 2019 stability
check. Executes SPECIFICATION sections 7, 8 and 11.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

from engine import (ALLOCATIONS, DEBT_CLASSES, G_GRID, KAPPA, OWNERSHIP,
                    PRIMARY, R_RETAINED, R_SENS, S_GRID, analytic_boundary,
                    cap_and_redistribute, gamma, income_after, load, prepare,
                    wage_loss)

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

TAU_K = {"assembled_0.086": 0.086, "required_low_0.110": 0.110,
         "required_high_0.137": 0.137}
OMEGA = [0.01, 0.02, 0.05, 0.10]
ANNUITY_C = 0.04
EQUITY_AGG = 33387.3e9            # DFA 2022Q4, dollars
RET_EQ_SHARE = 0.25               # Rosenthal-Mucciolo IRA + DB + DC
PI_GRID = [0.0, 0.25, 0.50, 1.00]
REFI = {"none": 0.0, "minus100bp": 0.11, "minus200bp": 0.21}
S_REPORT = [0.01, 0.02, 0.05, 0.10]


def base_case(d, s, exposure="cognitive_AIOE", r_ret=R_RETAINED):
    p = PRIMARY
    w = d["wageinc"].clip(lower=0).to_numpy()
    wt = d["wgt5"].to_numpy()
    delta = wage_loss(d, s, p["allocation"], exposure, r_ret)
    gam = gamma(d, s, p["ownership"], p["kappa"])
    delta = cap_and_redistribute(d, delta, gam, s * float((w * wt).sum()))
    return delta, gam


def need_growth(d, delta, gam, extra=0.0, pay_scale=1.0):
    """Growth that makes the worst-affected indebted household whole.
    `extra` is a per-household income addition; `pay_scale` scales required
    payments (refinancing), which changes who is indebted-and-affected but not
    the income test itself."""
    inc = d["inc"].to_numpy()
    net = inc - delta + gam + extra
    m = (d["valid"].to_numpy() & (d["debt_total"].to_numpy() > 0) & (net > 0))
    if not m.any():
        return np.nan
    return float(np.nanmax(inc[m] / net[m] - 1.0))


def main():
    D = prepare(load(2022))
    imps = sorted(D["imp"].unique())
    R = {}

    # ---------------- (e) ARRANGEMENTS ---------------------------------
    rows = []
    for imp in imps:
        d = D[D["imp"] == imp]
        wt = d["wgt5"].to_numpy()
        w = d["wageinc"].clip(lower=0).to_numpy()
        W = float((w * wt).sum())
        nh = float(wt.sum())
        for s in S_REPORT:
            delta, gam = base_case(d, s)
            base_b = need_growth(d, delta, gam)
            rows.append(dict(imp=imp, s=s, arrangement="none", param="",
                             boundary=base_b, fiscal_cost_bn=0.0))

            # 7.1 capital-tax-funded per-capita transfer
            for name, tk in TAU_K.items():
                pot = s * W * KAPPA[PRIMARY["kappa"]] * tk
                transfer = pot / nh
                b = need_growth(d, delta, gam, extra=transfer)
                rows.append(dict(imp=imp, s=s, arrangement="capital_tax",
                                 param=name, boundary=b,
                                 fiscal_cost_bn=pot / 1e9))

            # 7.2 universal capital fund
            for om in OMEGA:
                pot = om * EQUITY_AGG * ANNUITY_C
                b = need_growth(d, delta, gam, extra=pot / nh)
                rows.append(dict(imp=imp, s=s, arrangement="universal_fund",
                                 param=f"omega={om}", boundary=b,
                                 fiscal_cost_bn=pot / 1e9))

            # 7.3 broadened retirement ownership, liquid and illiquid
            ret_pot = s * W * RET_EQ_SHARE
            for liq in (True, False):
                extra = (ret_pot / nh) if liq else 0.0
                b = need_growth(d, delta, gam, extra=extra)
                rows.append(dict(
                    imp=imp, s=s, arrangement="broadened_retirement",
                    param="liquid" if liq else "illiquid", boundary=b,
                    fiscal_cost_bn=(ret_pot / 1e9) if liq else 0.0))
    A = pd.DataFrame(rows)
    Am = A.groupby(["s", "arrangement", "param"]).agg(
        boundary=("boundary", "mean"),
        fiscal_cost_bn=("fiscal_cost_bn", "mean")).reset_index()
    Am.to_csv(OUT / "arrangements.csv", index=False)
    R["arrangements"] = Am.to_dict("records")
    print("ARRANGEMENTS (primary cell; boundary = growth making the "
          "worst-affected indebted household whole)")
    for s in S_REPORT:
        sub = Am[Am["s"] == s]
        b0 = float(sub[sub["arrangement"] == "none"]["boundary"].iloc[0])
        print(f"\n  s={s:.2f}  no arrangement: {b0:.4f}")
        for _, r in sub[sub["arrangement"] != "none"].iterrows():
            print(f"    {r['arrangement']:22s} {r['param']:14s} "
                  f"boundary {r['boundary']:8.4f}  "
                  f"delta {r['boundary']-b0:+8.4f}  "
                  f"cost {r['fiscal_cost_bn']:8.1f}bn")

    # ---------------- (f) SENSITIVITIES ---------------------------------
    srows = []
    for imp in imps:
        d = D[D["imp"] == imp]
        wt = d["wgt5"].to_numpy()
        w = d["wageinc"].clip(lower=0).to_numpy()
        W = float((w * wt).sum())
        inc = d["inc"].to_numpy()
        tpay = d["tpay"].to_numpy()
        for s in S_REPORT:
            delta, gam = base_case(d, s)
            b0 = need_growth(d, delta, gam)
            srows.append(dict(imp=imp, s=s, sens="baseline", param="",
                              boundary=b0))

            # 8.1 price pass-through on NON-DEBT spending
            for pi in PI_GRID:
                # the productivity gain is g; at the boundary the relevant
                # relief is pi * g * (income - payments). Solve the fixed
                # point on the grid rather than analytically.
                bb = np.nan
                for g in G_GRID:
                    relief = pi * g * np.maximum(inc - tpay, 0.0)
                    ia = (1 + g) * (inc - delta + gam) + relief
                    r = (ia < inc) & d["valid"].to_numpy() \
                        & (d["debt_total"].to_numpy() > 0)
                    if not r.any():
                        bb = float(g)
                        break
                srows.append(dict(imp=imp, s=s, sens="price_passthrough",
                                  param=f"pi={pi}", boundary=bb))

            # 8.2 higher retained wage share
            for rr in R_SENS:
                dl, gm = base_case(d, s, r_ret=rr)
                srows.append(dict(imp=imp, s=s, sens="retained_wage_share",
                                  param=f"R={rr}",
                                  boundary=need_growth(d, dl, gm)))

            # 8.3 refinancing: payments fall, so fewer households are
            # indebted-and-affected at the margin
            for name, cut in REFI.items():
                ts = tpay * (1 - cut)
                net = inc - delta + gam
                m = (d["valid"].to_numpy() & (d["debt_total"].to_numpy() > 0)
                     & (net > 0) & (ts > 0))
                b = float(np.nanmax(inc[m] / net[m] - 1.0)) if m.any() \
                    else np.nan
                srows.append(dict(imp=imp, s=s, sens="refinancing",
                                  param=name, boundary=b))

            # 8.4 broader household equity ownership
            for kap in ("cash_flow", "accrual", "counterfactual"):
                gm = gamma(d, s, PRIMARY["ownership"], kap)
                dl = cap_and_redistribute(d, wage_loss(
                    d, s, PRIMARY["allocation"]), gm, s * W)
                srows.append(dict(imp=imp, s=s, sens="kappa",
                                  param=kap, boundary=need_growth(d, dl, gm)))
            # equity over-statement treated as real (1.50 factor on the gain)
            gm = gamma(d, s, PRIMARY["ownership"], PRIMARY["kappa"]) * 1.504
            dl = cap_and_redistribute(d, wage_loss(
                d, s, PRIMARY["allocation"]), gm, s * W)
            srows.append(dict(imp=imp, s=s, sens="equity_overstatement_real",
                              param="x1.504", boundary=need_growth(d, dl, gm)))

            # 8.5 transfers indexed to the shift
            other = (d["ssretinc"] + d["transfothinc"]).to_numpy()
            srows.append(dict(imp=imp, s=s, sens="indexed_transfers",
                              param="", boundary=need_growth(
                                  d, delta, gam, extra=s * other)))
    S = pd.DataFrame(srows)
    Sm = S.groupby(["s", "sens", "param"])["boundary"].mean().reset_index()
    Sm.to_csv(OUT / "sensitivities.csv", index=False)
    R["sensitivities"] = Sm.to_dict("records")
    print("\n\nSENSITIVITIES")
    for s in S_REPORT:
        sub = Sm[Sm["s"] == s]
        b0 = float(sub[sub["sens"] == "baseline"]["boundary"].iloc[0])
        print(f"\n  s={s:.2f}  baseline {b0:.4f}")
        for _, r in sub[sub["sens"] != "baseline"].iterrows():
            d_ = r["boundary"] - b0
            print(f"    {r['sens']:26s} {r['param']:14s} "
                  f"{r['boundary']:8.4f}  delta {d_:+8.4f}")

    # ---------------- (g) 2019 STABILITY --------------------------------
    D19 = prepare(load(2019))
    st = []
    for yr, DD in (("2022", D), ("2019", D19)):
        for imp in sorted(DD["imp"].unique()):
            d = DD[DD["imp"] == imp]
            for s in S_REPORT:
                dl, gm = base_case(d, s)
                st.append(dict(year=yr, imp=imp, s=s,
                               boundary=need_growth(d, dl, gm)))
    ST = pd.DataFrame(st).groupby(["year", "s"])["boundary"].mean(
        ).reset_index()
    piv = ST.pivot(index="s", columns="year", values="boundary")
    piv["pct_change"] = (piv["2019"] - piv["2022"]) / piv["2022"] * 100
    piv["unstable_gt25pct"] = piv["pct_change"].abs() > 25
    piv.to_csv(OUT / "stability_2019.csv")
    R["stability"] = piv.reset_index().to_dict("records")
    print("\n\n2019 STABILITY CHECK")
    print(piv.round(4).to_string())

    (OUT / "arrangements_results.json").write_text(
        json.dumps(R, indent=2, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()
