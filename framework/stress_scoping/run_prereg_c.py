"""Run the test pre-registered in PREREG_C.md. No specification choices here that are
not in that document.

Three rules, all normalised to the realised system household charge-off rate in the test
window, so they compete only on the cross-section:

  1. pooled CLASS-style regression, AR(1) plus macro plus bank controls, common coefficients
  2. reliability-weighted own-history factors, estimated on TRAINING years only
  3. pro rata, the shortcut the companion stress test used

Run:  python framework/stress_scoping/run_prereg_c.py
"""
import json
import pathlib

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FRED = ROOT / "data" / "raw" / "fred"
PANEL = pathlib.Path(r"C:\Users\bdd3\physical-ai-predict\data\raw\predictive\panel.csv")

# household categories only, as pre-registered
CATS = {"residential":    (["LNRERES"], ["NTRERES"]),
        "credit_card":    (["LNCRCD"], ["NTCRCD"]),
        "other_consumer": (["LNAUTO", "LNCONOTH"], ["NTAUTO", "NTCONOTH"])}
WINDOWS = {"W1_crisis": ((2001, 2006), (2007, 2010)),
           "W2_post":   ((2001, 2013), (2014, 2019))}
MIN_BOOK = 1000.0
MARGIN = 0.020          # the pre-registered 2.0 percent of RMSE


def macro():
    out = {}
    for sid, name in (("UNRATE", "unrate"), ("GDP", "gdp"), ("DRSFRMACBS", "delinq")):
        d = pd.read_csv(FRED / f"{sid}.csv")
        d.columns = [c.lower() for c in d.columns]
        dc = [c for c in d.columns if "date" in c][0]
        vc = [c for c in d.columns if c != dc][0]
        d[dc] = pd.to_datetime(d[dc])
        out[name] = d.groupby(d[dc].dt.year)[vc].mean()
    M = pd.DataFrame(out)
    M["gdp_growth"] = M.gdp.pct_change() * 100
    M["d_delinq"] = M.delinq.diff()
    return M[["unrate", "gdp_growth", "d_delinq"]].dropna()


def load():
    P = pd.read_csv(PANEL, low_memory=False)
    P = P[(P.hh_book >= MIN_BOOK)].copy()
    for c, (bal, nco) in CATS.items():
        P[f"bal_{c}"] = P[bal].fillna(0).sum(axis=1)
        P[f"nco_{c}"] = P[nco].fillna(0).sum(axis=1)
    P["hh_bal"] = sum(P[f"bal_{c}"] for c in CATS)
    P["hh_nco"] = sum(P[f"nco_{c}"] for c in CATS)
    P = P[P.hh_bal > 0].copy()
    P["y"] = P.hh_nco / P.hh_bal
    for c in CATS:
        P[f"s_{c}"] = P[f"bal_{c}"] / P.hh_bal
        P[f"r_{c}"] = np.where(P[f"bal_{c}"] > 0, P[f"nco_{c}"] / P[f"bal_{c}"].replace(0, np.nan), np.nan)
    return P


def ols(X, y):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b


def run_window(P, M, tr, te, log):
    tr0, tr1 = tr
    te0, te1 = te
    T = P[(P.origin_year >= tr0) & (P.origin_year <= tr1)].copy()
    E = P[(P.origin_year >= te0) & (P.origin_year <= te1)].copy()
    common = set(T.CERT) & set(E.CERT)
    T, E = T[T.CERT.isin(common)].copy(), E[E.CERT.isin(common)].copy()

    lo, hi = T.y.quantile(0.01), T.y.quantile(0.99)       # training-window winsorisation only
    T["y"] = T.y.clip(lo, hi)
    E["y"] = E.y.clip(lo, hi)

    # ---- 1. pooled CLASS-style regression, per category, common coefficients
    Tl = T.sort_values(["CERT", "origin_year"]).copy()
    El = E.sort_values(["CERT", "origin_year"]).copy()
    pred_cls = pd.Series(0.0, index=E.index)
    for c in CATS:
        for D in (Tl, El):
            D[f"lag_{c}"] = D.groupby("CERT")[f"r_{c}"].shift(1)
        tt = Tl.dropna(subset=[f"lag_{c}", f"r_{c}", "log_assets", "tier1_lev"])
        tt = tt[tt[f"bal_{c}"] > 0]
        if len(tt) < 200:
            log.append(f"category {c}: only {len(tt)} training rows, coefficients may be weak")
        mm = M.reindex(tt.origin_year).to_numpy()
        X = np.column_stack([np.ones(len(tt)), tt[f"lag_{c}"], mm,
                             tt.log_assets, tt.tier1_lev])
        b = ols(np.nan_to_num(X), tt[f"r_{c}"].to_numpy())
        ee = El.copy()
        ee[f"lag_{c}"] = ee[f"lag_{c}"].fillna(tt[f"r_{c}"].median())
        mme = M.reindex(ee.origin_year).to_numpy()
        Xe = np.column_stack([np.ones(len(ee)), ee[f"lag_{c}"], mme,
                              ee.log_assets.fillna(ee.log_assets.median()),
                              ee.tier1_lev.fillna(ee.tier1_lev.median())])
        rc = np.nan_to_num(Xe) @ b
        pred_cls = pred_cls + ee[f"s_{c}"].fillna(0).to_numpy() * np.clip(rc, 0, None)

    # ---- rho and own-history factors, TRAINING ONLY
    mix = [f"s_{c}" for c in CATS]
    Xm = np.column_stack([np.ones(len(T))] + [T[m].fillna(0).to_numpy() for m in mix])
    bm = ols(Xm, T.y.to_numpy())
    res = T.y.to_numpy() - Xm @ bm
    T["_res"] = res
    rho = float(T.groupby("CERT")["_res"].transform("mean").var() / T["_res"].var())
    log.append(f"rho estimated on training window only = {rho:.4f}")

    fac = {}
    for c in CATS:
        g = T[T[f"bal_{c}"] > 0].groupby("CERT").agg(
            b=(f"bal_{c}", "sum"), n=(f"nco_{c}", "sum"), T=(f"bal_{c}", "size"))
        sysr = g.n.sum() / g.b.sum()
        raw = (g.n / g.b) / sysr if sysr > 0 else 1.0
        w = g["T"] * rho / (1 + (g["T"] - 1) * rho)
        fac[c] = (1 + (raw - 1) * w).clip(0.1, 5.0).to_dict()

    # ---- system category rates realised in the TEST window (scenario is given)
    sys_te = {c: float(E[f"nco_{c}"].sum() / E[f"bal_{c}"].sum())
              if E[f"bal_{c}"].sum() > 0 else 0.0 for c in CATS}

    pred_pro = pd.Series(0.0, index=E.index)
    pred_own = pd.Series(0.0, index=E.index)
    for c in CATS:
        s = E[f"s_{c}"].fillna(0).to_numpy()
        f = E.CERT.map(fac[c]).fillna(1.0).to_numpy()
        pred_pro = pred_pro + s * sys_te[c]
        pred_own = pred_own + s * sys_te[c] * f

    # ---- normalise all three to the realised system household rate
    realised_sys = float(E.hh_nco.sum() / E.hh_bal.sum())
    out = {}
    for name, p in (("pooled_class", pred_cls), ("own_history", pred_own), ("pro_rata", pred_pro)):
        p = np.asarray(p, dtype=float)
        p = p * (realised_sys / p.mean()) if p.mean() > 0 else p
        err = p - E.y.to_numpy()
        out[name] = {"rmse": float(np.sqrt(np.mean(err ** 2))),
                     "mae": float(np.mean(np.abs(err)))}
    out["_meta"] = {"banks": int(E.CERT.nunique()), "test_rows": int(len(E)),
                    "rho_training": round(rho, 4),
                    "realised_system_rate": round(realised_sys, 6)}
    return out, E, {"own": pred_own, "pro": pred_pro, "cls": pred_cls}


def main():
    log = []
    P, M = load(), macro()
    res = {}
    for wname, (tr, te) in WINDOWS.items():
        r, E, preds = run_window(P, M, tr, te, log)
        base = r["pooled_class"]["rmse"]
        r["improvement_vs_pooled"] = {
            k: round((base - r[k]["rmse"]) / base, 4) for k in ("own_history", "pro_rata")}
        r["clears_margin"] = bool(r["improvement_vs_pooled"]["own_history"] >= MARGIN)
        res[wname] = r
        print(f"\n=== {wname}  train {tr}  test {te} ===")
        print(f"  banks {r['_meta']['banks']:,}   rows {r['_meta']['test_rows']:,}   "
              f"rho(train) {r['_meta']['rho_training']}")
        for k in ("pooled_class", "own_history", "pro_rata"):
            print(f"  {k:14s} RMSE {r[k]['rmse']:.6f}   MAE {r[k]['mae']:.6f}")
        print(f"  own-history vs pooled: {100*r['improvement_vs_pooled']['own_history']:+.2f} percent"
              f"   margin {100*MARGIN:.1f} percent -> {'CLEARS' if r['clears_margin'] else 'FAILS'}")

    cleared = [w for w in WINDOWS if res[w]["clears_margin"]]
    verdict = ("PROCEED" if len(cleared) == 2 else
               "KILL" if len(cleared) == 0 else "INCONCLUSIVE")
    res["_verdict"] = verdict
    res["_windows_cleared"] = cleared
    res["_violations"] = log
    (HERE / "prereg_c_results.json").write_text(json.dumps(res, indent=2, default=float))
    print(f"\nWINDOWS CLEARING THE MARGIN: {len(cleared)} of 2  ->  VERDICT: {verdict}")
    if log:
        print("\nviolations and notes:")
        for x in log:
            print("  " + x)


if __name__ == "__main__":
    main()
