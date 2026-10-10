"""
V2, POST HOC. Executes SPECIFICATION_V2.md.

Every number this produces is post hoc: the definition was chosen after the v1
results were seen. See SPECIFICATION_V2.md and the labelling instruction in its
section 6.

Order fixed by SPECIFICATION_V2: stability check first, then the distribution,
then the arrangements' effect on the median, then the section 5.3 convention
test on the median.
"""
from pathlib import Path
import io
import json
import zipfile
import numpy as np
import pandas as pd

from engine import (ALLOCATIONS, BASES, KAPPA, OWNERSHIP, PRIMARY, R_RETAINED,
                    S_GRID, cap_and_redistribute, gamma, load, prepare,
                    wage_loss)

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
RAW = ROOT / "data" / "raw" / "household_condition"

TAU_K = {"assembled_0.086": 0.086, "required_low_0.110": 0.110,
         "required_high_0.137": 0.137}
OMEGA = [0.01, 0.02, 0.05, 0.10]
ANNUITY_C = 0.04
EQUITY_AGG = 33387.3e9
RET_EQ_SHARE = 0.25
RESTORED_AT = [0.05, 0.10, 0.20]
S_REPORT = [0.01, 0.02, 0.05, 0.10]


def restoring_rates(d, s, alloc, own, kap, exposure="cognitive_AIOE",
                    r_ret=R_RETAINED, extra=0.0):
    """g_i for each household whose capacity falls, with its debt weight.
    Households driven to non-positive net income carry g_i = +inf: they are
    never restored by growth, and excluding them would understate."""
    w = d["wageinc"].clip(lower=0).to_numpy()
    wt = d["wgt5"].to_numpy()
    delta = wage_loss(d, s, alloc, exposure, r_ret)
    gam = gamma(d, s, own, kap)
    delta = cap_and_redistribute(d, delta, gam, s * float((w * wt).sum()))
    inc = d["inc"].to_numpy()
    net = inc - delta + gam + extra
    bal = d["debt_total"].to_numpy()
    affected = (d["valid"].to_numpy() & (bal > 0) & (net < inc))
    gi = np.full(len(d), np.nan)
    pos = affected & (net > 0)
    gi[pos] = inc[pos] / net[pos] - 1.0
    gi[affected & (net <= 0)] = np.inf
    return gi, (bal * wt), affected


def wq_percentile(vals, weights, q):
    """Debt-weighted percentile. +inf values are kept in the weighting."""
    m = ~np.isnan(vals)
    v, wgt = vals[m], weights[m]
    o = np.argsort(v, kind="stable")
    v, wgt = v[o], wgt[o]
    tot = wgt.sum()
    if tot <= 0:
        return np.nan
    cw = np.cumsum(wgt) / tot
    idx = np.searchsorted(cw, q)
    if idx >= len(v):
        return float(v[-1])
    return float(v[idx])


def summarise(gi, dw, affected):
    m = affected & ~np.isnan(gi)
    v, wgt = gi[m], dw[m]
    if wgt.sum() <= 0:
        return {k: np.nan for k in
                ("median", "q25", "q75", "p90", "p100", "iqr",
                 *[f"restored_at_{r}" for r in RESTORED_AT],
                 "share_never_restored")}
    out = {"median": wq_percentile(v, wgt, 0.50),
           "q25": wq_percentile(v, wgt, 0.25),
           "q75": wq_percentile(v, wgt, 0.75),
           "p90": wq_percentile(v, wgt, 0.90),
           "p100": float(np.max(v))}
    out["iqr"] = out["q75"] - out["q25"]
    for r in RESTORED_AT:
        out[f"restored_at_{r}"] = float((wgt * (v <= r)).sum() / wgt.sum())
    out["share_never_restored"] = float(
        (wgt * np.isinf(v)).sum() / wgt.sum())
    return out


def main():
    D22 = prepare(load(2022))
    p = PRIMARY
    R = {"WARNING": "V2 IS POST HOC. Definition chosen after v1 results were "
                    "seen. See SPECIFICATION_V2.md."}

    # ============ 1. STABILITY CHECK, REPORTED FIRST =====================
    print("V2, POST HOC.  SPECIFICATION_V2 section 4: STABILITY CHECK FIRST\n")
    D19 = prepare(load(2019))
    strows = []
    for yr, DD in (("2022", D22), ("2019", D19)):
        for imp in sorted(DD["imp"].unique()):
            d = DD[DD["imp"] == imp]
            for s in S_REPORT:
                gi, dw, aff = restoring_rates(d, s, p["allocation"],
                                              p["ownership"], p["kappa"])
                st = summarise(gi, dw, aff)
                st.update(year=yr, imp=imp, s=s)
                strows.append(st)
    ST = pd.DataFrame(strows).groupby(["year", "s"]).mean(
        numeric_only=True).reset_index().drop(columns=["imp"])
    piv = ST.pivot(index="s", columns="year",
                   values=["median", "q25", "q75"])
    stab = {}
    print(f"{'s':>6} {'stat':>8} {'2022':>9} {'2019':>9} {'change':>9}  verdict")
    for stat in ("median", "q25", "q75"):
        for s in S_REPORT:
            a = float(ST[(ST["year"] == "2022") & (ST["s"] == s)][stat].iloc[0])
            b = float(ST[(ST["year"] == "2019") & (ST["s"] == s)][stat].iloc[0])
            ch = (b - a) / a * 100 if a else np.nan
            bad = (not np.isfinite(ch)) or abs(ch) > 25 or (np.sign(a) !=
                                                            np.sign(b))
            stab[f"{stat}_s{s}"] = {"y2022": a, "y2019": b, "pct_change": ch,
                                    "unstable": bool(bad)}
            print(f"{s:>6.2f} {stat:>8} {a:>9.4f} {b:>9.4f} {ch:>8.1f}%  "
                  f"{'UNSTABLE' if bad else 'stable'}")
    n_bad = sum(v["unstable"] for v in stab.values())
    R["stability"] = stab
    R["stability_failures"] = n_bad
    R["stability_verdict"] = (
        "PASS: the median and quartiles are stable within 25 percent"
        if n_bad == 0 else
        f"FAIL on {n_bad} of {len(stab)} statistics")
    print(f"\n  {R['stability_verdict']}")
    print("  (v1's maximum failed at every s by 50 to 65 percent)")
    ST.to_csv(OUT / "v2_stability.csv", index=False)

    # ============ 2. THE DISTRIBUTION ====================================
    rows = []
    for imp in sorted(D22["imp"].unique()):
        d = D22[D22["imp"] == imp]
        for s in S_GRID:
            for alloc in ALLOCATIONS:
                for own in OWNERSHIP:
                    for basis in BASES:
                        for kap in KAPPA:
                            gi, dw, aff = restoring_rates(d, float(s), alloc,
                                                          own, kap)
                            r = summarise(gi, dw, aff)
                            r.update(imp=imp, s=float(s), allocation=alloc,
                                     ownership=own, basis=basis, kappa=kap)
                            rows.append(r)
    V = pd.DataFrame(rows)
    Vm = V.groupby(["s", "allocation", "ownership", "basis", "kappa"]).mean(
        numeric_only=True).reset_index().drop(columns=["imp"])
    Vm.to_csv(OUT / "v2_distribution.csv", index=False)
    prim = Vm[(Vm["allocation"] == p["allocation"])
              & (Vm["ownership"] == p["ownership"])
              & (Vm["basis"] == p["basis"]) & (Vm["kappa"] == p["kappa"])]
    R["primary_distribution"] = prim.to_dict("records")
    print("\n\nDEBT-WEIGHTED DISTRIBUTION OF THE RESTORING RATE, primary cell")
    print(f"{'s':>6} {'q25':>8} {'median':>8} {'q75':>8} {'p90':>8} "
          f"{'p100 (v1)':>12} {'@5%':>7} {'@10%':>7} {'@20%':>7}")
    for _, r in prim.iterrows():
        print(f"{r['s']:>6.2f} {r['q25']:>8.4f} {r['median']:>8.4f} "
              f"{r['q75']:>8.4f} {r['p90']:>8.4f} {r['p100']:>12.4g} "
              f"{r['restored_at_0.05']:>7.3f} {r['restored_at_0.1']:>7.3f} "
              f"{r['restored_at_0.2']:>7.3f}")

    # replicate-weight interval on the primary median, s=0.05
    zrw = zipfile.ZipFile(RAW / "scf2022rw1s.zip")
    rw = pd.read_stata(io.BytesIO(zrw.read(zrw.namelist()[0])))
    rcols = [c for c in rw.columns if c.lower().startswith("wt1b")][:200]
    se = {}
    for s in (0.05, 0.10):
        pe, reps = [], []
        for imp in sorted(D22["imp"].unique()):
            d = D22[D22["imp"] == imp].merge(rw[["yy1"] + rcols], on="yy1",
                                             how="left")
            gi, dw, aff = restoring_rates(d, s, p["allocation"],
                                          p["ownership"], p["kappa"])
            pe.append(summarise(gi, dw, aff)["median"])
            if imp == 1:
                for c in rcols:
                    dd = d.copy()
                    dd["wgt5"] = dd[c].fillna(0.0) * 5
                    gi2, dw2, aff2 = restoring_rates(dd, s, p["allocation"],
                                                     p["ownership"],
                                                     p["kappa"])
                    reps.append(summarise(gi2, dw2, aff2)["median"])
        pe = np.asarray([x for x in pe if np.isfinite(x)])
        reps = np.asarray([x for x in reps if np.isfinite(x)])
        m = float(pe.mean())
        vb = float(pe.var(ddof=1)) if pe.size > 1 else 0.0
        vw = float(reps.var(ddof=1)) if reps.size > 1 else np.nan
        tot = vw + (1 + 1 / 5) * vb
        se[str(s)] = {"median": m, "se": float(np.sqrt(tot)),
                      "ci_lo": m - 1.96 * np.sqrt(tot),
                      "ci_hi": m + 1.96 * np.sqrt(tot),
                      "replicates": int(reps.size)}
    R["median_se"] = se
    print("\nprimary median with interval (Rubin + 200 replicates)")
    for k, v in se.items():
        print(f"  s={k}: {v['median']:.4f} "
              f"[{v['ci_lo']:.4f}, {v['ci_hi']:.4f}]")

    # ============ 3. ARRANGEMENTS, EFFECT ON THE MEDIAN ==================
    arows = []
    for imp in sorted(D22["imp"].unique()):
        d = D22[D22["imp"] == imp]
        wt = d["wgt5"].to_numpy()
        w = d["wageinc"].clip(lower=0).to_numpy()
        W = float((w * wt).sum())
        nh = float(wt.sum())
        for s in S_REPORT:
            def med(extra=0.0):
                gi, dw, aff = restoring_rates(d, s, p["allocation"],
                                              p["ownership"], p["kappa"],
                                              extra=extra)
                return summarise(gi, dw, aff)
            base = med()
            arows.append(dict(imp=imp, s=s, arrangement="none", param="",
                              cost_bn=0.0, **base))
            for name, tk in TAU_K.items():
                pot = s * W * KAPPA[p["kappa"]] * tk
                arows.append(dict(imp=imp, s=s, arrangement="capital_tax",
                                  param=name, cost_bn=pot / 1e9,
                                  **med(pot / nh)))
            for om in OMEGA:
                pot = om * EQUITY_AGG * ANNUITY_C
                arows.append(dict(imp=imp, s=s, arrangement="universal_fund",
                                  param=f"omega={om}", cost_bn=pot / 1e9,
                                  **med(pot / nh)))
            ret = s * W * RET_EQ_SHARE
            arows.append(dict(imp=imp, s=s,
                              arrangement="broadened_retirement",
                              param="liquid", cost_bn=ret / 1e9,
                              **med(ret / nh)))
            arows.append(dict(imp=imp, s=s,
                              arrangement="broadened_retirement",
                              param="illiquid", cost_bn=0.0, **med(0.0)))
    A = pd.DataFrame(arows).groupby(
        ["s", "arrangement", "param"]).mean(numeric_only=True).reset_index(
        ).drop(columns=["imp"])
    A.to_csv(OUT / "v2_arrangements.csv", index=False)
    R["arrangements"] = A.to_dict("records")
    print("\n\nARRANGEMENTS, effect on the DEBT-WEIGHTED MEDIAN")
    for s in S_REPORT:
        sub = A[A["s"] == s]
        b0 = float(sub[sub["arrangement"] == "none"]["median"].iloc[0])
        print(f"\n  s={s:.2f}  median with no arrangement {b0:.4f}")
        for _, r in sub[sub["arrangement"] != "none"].iterrows():
            print(f"    {r['arrangement']:22s} {str(r['param']):14s} "
                  f"{r['median']:8.4f}  delta {r['median']-b0:+8.4f}  "
                  f"@10% {r['restored_at_0.1']:.3f}  "
                  f"cost {r['cost_bn']:7.1f}bn")

    # ============ 4. SECTION 5.3 CONVENTION TEST ON THE MEDIAN ===========
    pc = Vm[(Vm["allocation"] == p["allocation"])
            & (Vm["ownership"] == p["ownership"])
            & (Vm["basis"] == p["basis"]) & (Vm["kappa"] == p["kappa"])]
    s_spread = float(pc["median"].max() - pc["median"].min())
    cs = []
    for s in S_GRID:
        sub = Vm[(Vm["s"] == float(s))
                 & (Vm["allocation"] == p["allocation"])
                 & (Vm["ownership"] == p["ownership"])]
        cs.append(float(sub["median"].max() - sub["median"].min()))
    conv = float(np.nanmax(cs))
    R["s53_convention_test"] = {
        "s_grid_spread_of_median": s_spread,
        "convention_spread_of_median_max": conv,
        "convention_exceeds_s": bool(conv > s_spread),
        "per_s": dict(zip([float(x) for x in S_GRID], cs))}
    print(f"\n\nSECTION 5.3 CONVENTION TEST, on the median")
    print(f"  spread of the median across the s grid: {s_spread:.4f}")
    print(f"  spread across conventions, worst over s: {conv:.4f}")
    print(f"  CONVENTION SPREAD EXCEEDS s SPREAD: {conv > s_spread}")
    print(f"  (v1 on its maximum: 0.050 against 0.057, No by 0.007)")

    (OUT / "v2_results.json").write_text(
        json.dumps(R, indent=2, default=float), encoding="utf-8")


if __name__ == "__main__":
    main()
