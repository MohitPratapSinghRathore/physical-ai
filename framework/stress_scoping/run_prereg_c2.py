"""Run the test pre-registered in PREREG_C2.md. No specification choices not in that document."""
import json, pathlib, datetime as dt
import numpy as np, pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PANEL = pathlib.Path(r"C:\Users\bdd3\physical-ai-predict\data\raw\predictive\panel.csv")
FAIL = ROOT / "data" / "raw" / "fdic_failures" / "failures.json"

PORT = {
    "household":  {"residential": (["LNRERES"], ["NTRERES"]),
                   "credit_card": (["LNCRCD"], ["NTCRCD"]),
                   "other_consumer": (["LNAUTO", "LNCONOTH"], ["NTAUTO", "NTCONOTH"])},
    "commercial": {"c_and_i": (["LNCI"], ["NTCI"]),
                   "nonres_re": (["LNRENRES"], ["NTRENRES"])},
}
WINDOWS = {"W1_crisis": ((2001, 2006), (2007, 2012)),
           "W2_post":   ((2001, 2013), (2014, 2019))}
MIN_BOOK, TOPQ = 1000.0, 0.05
log = []


def failures():
    R = pd.DataFrame(json.loads(FAIL.read_text()))
    R["FAILDATE"] = pd.to_datetime(R.FAILDATE)
    R["CERT"] = pd.to_numeric(R.CERT, errors="coerce")
    return R.dropna(subset=["CERT"])[["CERT", "FAILDATE"]]


def hyperz(N, K, n, k):
    """two-sided hypergeometric z for k successes in n draws from N with K successes."""
    mu = n * K / N
    var = n * (K / N) * (1 - K / N) * (N - n) / (N - 1)
    return (k - mu) / np.sqrt(var) if var > 0 else np.nan, mu


def build(P, cats):
    D = P.copy()
    for c, (bal, nco) in cats.items():
        D[f"bal_{c}"] = D[bal].fillna(0).sum(axis=1)
        D[f"nco_{c}"] = D[nco].fillna(0).sum(axis=1)
    D["tb"] = sum(D[f"bal_{c}"] for c in cats)
    D["tn"] = sum(D[f"nco_{c}"] for c in cats)
    D = D[(D.tb >= MIN_BOOK)].copy()
    D["y"] = D.tn / D.tb
    for c in cats:
        D[f"s_{c}"] = D[f"bal_{c}"] / D.tb
    return D


def run(D, cats, tr, te, F):
    T = D[(D.origin_year >= tr[0]) & (D.origin_year <= tr[1])]
    E = D[(D.origin_year >= te[0]) & (D.origin_year <= te[1])]
    common = set(T.CERT) & set(E.CERT)
    T, E = T[T.CERT.isin(common)].copy(), E[E.CERT.isin(common)].copy()
    lo, hi = T.y.quantile(.01), T.y.quantile(.99)
    T["y"] = T.y.clip(lo, hi)

    # rho on training only
    mix = [f"s_{c}" for c in cats]
    X = np.column_stack([np.ones(len(T))] + [T[m].fillna(0).to_numpy() for m in mix])
    b, *_ = np.linalg.lstsq(X, T.y.to_numpy(), rcond=None)
    T = T.assign(_res=T.y.to_numpy() - X @ b)
    rho = float(T.groupby("CERT")["_res"].transform("mean").var() / T["_res"].var())

    fac, rawf = {}, {}
    for c in cats:
        g = T[T[f"bal_{c}"] > 0].groupby("CERT").agg(
            bb=(f"bal_{c}", "sum"), nn=(f"nco_{c}", "sum"), TT=(f"bal_{c}", "size"))
        sysr = g.nn.sum() / g.bb.sum()
        raw = (g.nn / g.bb) / sysr if sysr > 0 else g.bb * 0 + 1
        w = g.TT * rho / (1 + (g.TT - 1) * rho)
        fac[c] = (1 + (raw - 1) * w).clip(.1, 5.).to_dict()
        rawf[c] = raw.clip(.1, 5.).to_dict()

    sys_te = {c: float(E[f"nco_{c}"].sum() / E[f"bal_{c}"].sum())
              if E[f"bal_{c}"].sum() > 0 else 0. for c in cats}

    # bank-level cross-section: average shares over the test window
    B = E.groupby("CERT").agg(**{f"s_{c}": (f"s_{c}", "mean") for c in cats},
                              tier1=("tier1_lev", "mean"), la=("log_assets", "mean"),
                              y=("y", "mean"))
    r1 = sum(B[f"s_{c}"].fillna(0) * sys_te[c] for c in cats)
    r2 = sum(B[f"s_{c}"].fillna(0) * sys_te[c] *
             pd.Series(B.index.map(fac[c]), index=B.index).astype(float).fillna(1.) for c in cats)
    # R3: mix removed, rank on own-history ratio alone
    r3 = sum(pd.Series(B.index.map(rawf[c]), index=B.index).astype(float).fillna(1.)
             * B[f"s_{c}"].fillna(0) for c in cats)
    B["R1_group_rate"], B["R2_own_history"], B["R3_mix_residual"] = r1, r2, r3

    end = dt.datetime(te[1], 12, 31)
    win = F[(F.FAILDATE > end) & (F.FAILDATE <= end + pd.DateOffset(years=3))]
    B["failed"] = B.index.isin(set(win.CERT)).astype(int)

    N, K = len(B), int(B.failed.sum())
    n = int(TOPQ * N)
    out = {"_meta": {"banks": N, "failures_in_window": K, "flagged_n": n,
                     "base_rate": round(K / N, 5), "rho_training": round(rho, 4)}}
    if K == 0:
        log.append(f"window ending {te[1]}: ZERO failures in the 3-year follow-up, "
                   f"test is undefined here")
        return out, B
    for rule in ("R1_group_rate", "R2_own_history", "R3_mix_residual"):
        top = B.nlargest(n, rule)
        k = int(top.failed.sum())
        z, mu = hyperz(N, K, n, k)
        out[rule] = {"flagged_failures": k, "expected": round(float(mu), 2),
                     "lift": round(k / mu, 3) if mu > 0 else None, "z": round(float(z), 2),
                     "median_tier1_flagged": round(float(top.tier1.median()), 3),
                     "median_tier1_rest": round(float(B.drop(top.index).tier1.median()), 3),
                     "median_logassets_flagged": round(float(top.la.median()), 3),
                     "median_logassets_rest": round(float(B.drop(top.index).la.median()), 3)}
    return out, B


def main():
    P = pd.read_csv(PANEL, low_memory=False)
    F = failures()
    res = {}
    for pname, cats in PORT.items():
        D = build(P, cats)
        res[pname] = {}
        print(f"\n################ PORTFOLIO: {pname}  (banks {D.CERT.nunique():,}) ################")
        for wname, (tr, te) in WINDOWS.items():
            r, _ = run(D, cats, tr, te, F)
            res[pname][wname] = r
            m = r["_meta"]
            print(f"\n=== {wname}  train {tr}  test {te} ===")
            print(f"  banks {m['banks']:,}  failures in 3y follow-up {m['failures_in_window']}  "
                  f"base {100*m['base_rate']:.3f}%  flagged n={m['flagged_n']}  rho {m['rho_training']}")
            for rule in ("R1_group_rate", "R2_own_history", "R3_mix_residual"):
                if rule not in r:
                    continue
                d = r[rule]
                print(f"  {rule:16s} fail {d['flagged_failures']:3d} vs {d['expected']:6.2f} exp"
                      f"  lift {d['lift']:5.2f}x  z {d['z']:+6.2f}"
                      f"   tier1 flagged {d['median_tier1_flagged']:6.3f} vs rest {d['median_tier1_rest']:6.3f}")
    res["_violations"] = log
    (HERE / "prereg_c2_results.json").write_text(json.dumps(res, indent=2, default=float))
    if log:
        print("\nVIOLATIONS AND NOTES:")
        for x in log:
            print("  " + x)


if __name__ == "__main__":
    main()
