"""
D8: is the pre-registered dR2 information about which bank loses money, or a
level correction on a baseline that drifts across the credit cycle?

Two diagnostics, neither pre-registered, both reported because the
pre-registered statistic cannot be interpreted without them:

  1. re-centred dR2  - both predictions shifted to the test-year mean, which
     removes level drift and leaves only cross-sectional ranking;
  2. out-of-sample Spearman rank correlation between prediction and realised
     charge-off rate.
"""
from pathlib import Path
import importlib.util
import json
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location("rt", HERE / "run_test.py")
rt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rt)
CT = rt.CONTROLS


def load():
    P = pd.read_csv(ROOT / "data" / "raw" / "predictive" / "panel.csv",
                    low_memory=False)
    P = P[(P["hh_book"] >= rt.MIN_BOOK) & (P["bus_book"] >= rt.MIN_BOOK)]
    P = rt.clean(P, rt.CONTROLS + rt.LAGGED + rt.CONSTRUCTS)
    for c in rt.CONTROLS + rt.LAGGED:
        lo, hi = P[c].quantile(0.01), P[c].quantile(0.99)
        P[c] = P[c].clip(lo, hi)
    return P


def run(P, construct, recentre):
    out = []
    for T in range(2008, 2021):
        cols = CT + [construct]
        tr = P[P.origin_year <= T].dropna(subset=["y_hh_3"] + cols)
        te = P[P.origin_year == T + 1].dropna(subset=["y_hh_3"] + cols)
        if len(tr) < 500 or len(te) < 100:
            continue
        lo, hi = tr.y_hh_3.quantile(.01), tr.y_hh_3.quantile(.99)
        ytr = tr.y_hh_3.clip(lo, hi).to_numpy()
        yte = te.y_hh_3.clip(lo, hi).to_numpy()
        Xc_tr = np.column_stack([np.ones(len(tr)), tr[CT].to_numpy()])
        Xc_te = np.column_stack([np.ones(len(te)), te[CT].to_numpy()])
        Xf_tr = np.column_stack([Xc_tr, tr[[construct]].to_numpy()])
        Xf_te = np.column_stack([Xc_te, te[[construct]].to_numpy()])
        pc = Xc_te @ rt.ols_fit(Xc_tr, ytr)
        pf = Xf_te @ rt.ols_fit(Xf_tr, ytr)
        if recentre:
            pc = pc - pc.mean() + yte.mean()
            pf = pf - pf.mean() + yte.mean()
        rho_c = np.corrcoef(pd.Series(pc).rank(), pd.Series(yte).rank())[0, 1]
        rho_f = np.corrcoef(pd.Series(pf).rank(), pd.Series(yte).rank())[0, 1]
        out.append(dict(yr=T + 1, rc=rt.r2_oos(yte, pc),
                        rf=rt.r2_oos(yte, pf),
                        dr2=rt.r2_oos(yte, pf) - rt.r2_oos(yte, pc),
                        rho_c=rho_c, rho_f=rho_f, drho=rho_f - rho_c))
    return pd.DataFrame(out)


def main():
    P = load()
    R = {}
    for construct in ("LB", "Gap"):
        for recentre in (False, True):
            f = run(P, construct, recentre)
            k = f"{construct}|{'recentred' if recentre else 'raw'}"
            R[k] = {"mean_r2_controls": float(f.rc.mean()),
                    "mean_dr2": float(f.dr2.mean()),
                    "years_dr2_positive": int((f.dr2 > 0).sum()),
                    "mean_rho_controls": float(f.rho_c.mean()),
                    "mean_rho_with": float(f.rho_f.mean()),
                    "mean_drho": float(f.drho.mean()),
                    "years_drho_positive": int((f.drho > 0).sum()),
                    "years": len(f), "by_year": f.to_dict("records")}
            r = R[k]
            print(f"  {k:16s} r2_ctrl {r['mean_r2_controls']:+.4f}  "
                  f"dR2 {r['mean_dr2']:+.5f} ({r['years_dr2_positive']}/{r['years']})"
                  f"   rho {r['mean_rho_controls']:+.4f}->{r['mean_rho_with']:+.4f}"
                  f"  d {r['mean_drho']:+.5f} ({r['years_drho_positive']}/{r['years']})")
    (HERE / "ranking.json").write_text(json.dumps(R, indent=2, default=float),
                                       encoding="utf-8")


if __name__ == "__main__":
    main()
