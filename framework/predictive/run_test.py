"""
The confirmatory forward-chaining test, then the specification curve.

Order is fixed by PREREGISTRATION.md: the confirmatory test runs first and the
curve is a calibration exercise whose only outputs are counts.
"""
from pathlib import Path
import json
import numpy as np
import numpy.linalg as la
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "predictive"
OUT = Path(__file__).resolve().parent
RNG = np.random.default_rng(20260926)

CONTROLS = ["sh_resre", "sh_consumer", "sh_cre", "sh_constr", "sh_ci",
            "sh_ag", "sh_sec", "tier1_lev", "cre_conc", "log_assets",
            "dep_assets", "brokered", "loans_assets"]
LAGGED = ["lag_nco"]
CONSTRUCTS = ["LB", "LB_debtor", "Gap", "LB_debtor_pw"]
OUTCOMES = ["y_hh_3", "y_tot_3", "y_bus_3", "y_npl_hh", "d_tier1", "failed"]
HORIZ = {"h1": 1, "h2": 2, "h3": 3}


MIN_BOOK = 1000.0      # $1m in $000s: the pilot's section 14.1 denominator rule


def clean(d, cols):
    d = d.copy()
    for c in cols:
        d[c] = pd.to_numeric(d[c], errors="coerce")
        d[c] = d[c].replace([np.inf, -np.inf], np.nan)
        d[c] = d[c].fillna(d[c].median())
    return d


def ols_fit(X, y):
    b, *_ = la.lstsq(X, y, rcond=None)
    return b


def r2_oos(y, yhat):
    ss = ((y - yhat) ** 2).sum()
    st = ((y - y.mean()) ** 2).sum()
    return 1 - ss / st if st > 0 else np.nan


def forward_chain(P, outcome, construct, controls):
    """Train on origin years <= T, test on T+1. Returns per-year dR2_oos."""
    res = []
    cols = controls + [construct]
    for T in range(2008, 2021):
        tr = P[(P["origin_year"] <= T)]
        te = P[P["origin_year"] == T + 1]
        tr = tr.dropna(subset=[outcome] + cols)
        te = te.dropna(subset=[outcome] + cols)
        if len(tr) < 500 or len(te) < 100:
            continue
        lo, hi = tr[outcome].quantile(0.01), tr[outcome].quantile(0.99)
        ytr = tr[outcome].clip(lo, hi).to_numpy()
        yte = te[outcome].clip(lo, hi).to_numpy()
        Xc_tr = np.column_stack([np.ones(len(tr)), tr[controls].to_numpy()])
        Xc_te = np.column_stack([np.ones(len(te)), te[controls].to_numpy()])
        Xf_tr = np.column_stack([Xc_tr, tr[[construct]].to_numpy()])
        Xf_te = np.column_stack([Xc_te, te[[construct]].to_numpy()])
        r_c = r2_oos(yte, Xc_te @ ols_fit(Xc_tr, ytr))
        r_f = r2_oos(yte, Xf_te @ ols_fit(Xf_tr, ytr))
        res.append({"test_year": T + 1, "n_train": len(tr), "n_test": len(te),
                    "r2_controls": r_c, "r2_with": r_f, "dr2": r_f - r_c})
    return pd.DataFrame(res)


def tstat(P, outcome, construct, controls):
    d = P.dropna(subset=[outcome, construct] + controls)
    if len(d) < 200:
        return np.nan, np.nan, 0
    lo, hi = d[outcome].quantile(0.01), d[outcome].quantile(0.99)
    y = d[outcome].clip(lo, hi).to_numpy()
    X = np.column_stack([np.ones(len(d)), d[controls].to_numpy()
                         if controls else np.empty((len(d), 0)),
                         d[[construct]].to_numpy()])
    b = ols_fit(X, y)
    e = y - X @ b
    XtXi = la.pinv(X.T @ X)
    # D7: cluster by BANK, not origin year. The panel has 10,842 banks with
    # about 14 observations each and OVERLAPPING three-year outcome windows,
    # so the dominant correlation is within bank across years. Clustering on
    # 21 year-groups understates the standard errors badly.
    # D7 (revised): TWO-WAY clustering by bank and by origin year. Bank alone
    # misses the common credit-cycle shock, which every bank shares; year alone
    # (21 groups) misses within-bank serial correlation across overlapping
    # three-year outcome windows. Cameron-Gelbach-Miller: V_bank + V_year -
    # V_bank*year.
    Xe = X * e[:, None]

    def meat_by(keys):
        c = pd.factorize(keys)[0]
        S = np.zeros((c.max() + 1, X.shape[1]))
        np.add.at(S, c, Xe)
        return S.T @ S

    cert = d["CERT"].to_numpy()
    yr = d["origin_year"].to_numpy()
    meat = (meat_by(cert) + meat_by(yr)
            - meat_by(pd.Series(cert).astype(str) + "_"
                      + pd.Series(yr).astype(str)))
    V = XtXi @ meat @ XtXi
    if V[-1, -1] <= 0:        # two-way meat can lose positive definiteness
        V = XtXi @ meat_by(cert) @ XtXi
    se = float(np.sqrt(max(V[-1, -1], 1e-300)))
    return float(b[-1]), float(b[-1] / se) if se > 0 else np.nan, len(d)


def main():
    P = pd.read_csv(RAW / "panel.csv", low_memory=False)
    # D5: a minimum household book, as the pilot's section 14.1 required. One
    # bank with a $4,000 book produced lag_nco = 19,645 and a test-year R2 of
    # -6.9 million, which alone created a spurious "success".
    n0 = len(P)
    P = P[(P["hh_book"] >= MIN_BOOK) & (P["bus_book"] >= MIN_BOOK)]
    print(f"minimum-book rule: {n0} -> {len(P)} rows")
    P = clean(P, CONTROLS + LAGGED + CONSTRUCTS)
    # D6: winsorise CONTROLS at 1/99 as well as outcomes; a control with an
    # extreme value destroys an out-of-sample R2 without carrying information.
    for c in CONTROLS + LAGGED:
        lo, hi = P[c].quantile(0.01), P[c].quantile(0.99)
        P[c] = P[c].clip(lo, hi)
    R = {}

    # plausibility
    viol = {}
    for c in CONSTRUCTS:
        viol[c] = {"min": float(P[c].min()), "max": float(P[c].max()),
                   "outside_0_1": int(((P[c] < 0) | (P[c] > 1)).sum())}
    viol["rows"] = int(len(P))
    viol["banks"] = int(P["CERT"].nunique())
    viol["negative_y_hh_3"] = int((P["y_hh_3"] < 0).sum())
    R["plausibility"] = viol
    print("PLAUSIBILITY"); print(json.dumps(viol, indent=1)[:600])

    # ---------------- confirmatory ----------------
    print("\nCONFIRMATORY: forward-chaining, outcome y_hh_3\n")
    conf = {}
    for construct in ("LB", "Gap"):
        for cname, ctrl in (("conventional", CONTROLS),
                            ("conventional+lagged", CONTROLS + LAGGED)):
            f = forward_chain(P, "y_hh_3", construct, ctrl)
            if f.empty:
                continue
            mean_d = float(f["dr2"].mean())
            pos = int((f["dr2"] > 0).sum())
            conf[f"{construct}|{cname}"] = {
                "mean_dr2": mean_d, "years": len(f),
                "years_positive": pos,
                "mean_r2_controls": float(f["r2_controls"].mean()),
                "success": bool(mean_d >= 0.01 and pos >= 8),
                "kill": bool(mean_d <= 0.002 or pos < 7),
                "by_year": f.to_dict("records")}
            print(f"  {construct:10s} {cname:22s} mean dR2 {mean_d:+.5f}  "
                  f"positive {pos}/{len(f)}  "
                  f"{'SUCCESS' if conf[f'{construct}|{cname}']['success'] else ('KILL' if conf[f'{construct}|{cname}']['kill'] else 'inconclusive')}")
    R["confirmatory"] = conf

    # ---------------- specification curve ----------------
    print("\nSPECIFICATION CURVE\n")
    samples = {
        "all": lambda d: d,
        "assets_gt_1bn": lambda d: d[d["ASSET"] > 1_000_000],
        "assets_lt_1bn": lambda d: d[d["ASSET"] <= 1_000_000],
        "counties_ge_5": lambda d: d[d["n_counties"] >= 5],
    }
    ctrlsets = {"none": [], "conventional": CONTROLS,
                "conventional+lagged": CONTROLS + LAGGED}
    rows = []
    for construct in CONSTRUCTS:
        for outcome in OUTCOMES:
            for hz, h in HORIZ.items():
                oc = outcome
                if outcome.startswith("y_hh") or outcome.startswith("y_tot") \
                        or outcome.startswith("y_bus"):
                    oc = outcome[:-1] + str(h)
                for sname, sfun in samples.items():
                    for kname, ctrl in ctrlsets.items():
                        d = sfun(P)
                        if oc not in d.columns:
                            continue
                        coef, t, n = tstat(d, oc, construct, ctrl)
                        rows.append(dict(construct=construct, outcome=oc,
                                         horizon=hz, sample=sname,
                                         controls=kname, coef=coef, t=t, n=n))
    S = pd.DataFrame(rows)
    S["abs_t"] = S["t"].abs()
    S = S.dropna(subset=["t"])
    S.to_csv(OUT / "spec_curve.csv", index=False)

    n_spec = len(S)
    sig = int((S["abs_t"] > 1.96).sum())
    expect = 0.05 * n_spec
    # Romano-Wolf: max-t null by simulation
    boot = np.array([np.abs(RNG.normal(0, 1, n_spec)).max()
                     for _ in range(10000)])
    rw_thresh = float(np.quantile(boot, 0.95))
    rw_sig = int((S["abs_t"] > rw_thresh).sum())

    R["spec_curve"] = {
        "n_specifications": n_spec,
        "significant_p05": sig,
        "expected_by_chance": expect,
        "ratio": sig / expect if expect else np.nan,
        "romano_wolf_threshold": rw_thresh,
        "surviving_romano_wolf": rw_sig,
        "max_abs_t": float(S["abs_t"].max()),
        "median_abs_t": float(S["abs_t"].median()),
    }
    print(f"  specifications run          {n_spec}")
    print(f"  significant at p<0.05       {sig}")
    print(f"  expected by chance          {expect:.1f}")
    print(f"  ratio                       {sig/expect:.2f}x")
    print(f"  Romano-Wolf 95% threshold   |t| > {rw_thresh:.3f}")
    print(f"  surviving Romano-Wolf       {rw_sig}")
    print(f"  max |t| {S['abs_t'].max():.2f}   median |t| {S['abs_t'].median():.2f}")

    (OUT / "results.json").write_text(json.dumps(R, indent=2, default=float),
                                      encoding="utf-8")


if __name__ == "__main__":
    main()
