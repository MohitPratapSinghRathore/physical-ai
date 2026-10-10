"""Run the test pre-registered in PREREG_C3.md. Predictors strictly as-of the last
training year; failures counted DURING the test window."""
import json, pathlib, datetime as dt
import numpy as np, pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PANEL = pathlib.Path(r"C:\Users\bdd3\physical-ai-predict\data\raw\predictive\panel.csv")
FAIL = ROOT / "data" / "raw" / "fdic_failures" / "failures.json"

PORT = {"household": {"residential": (["LNRERES"], ["NTRERES"]),
                      "credit_card": (["LNCRCD"], ["NTCRCD"]),
                      "other_consumer": (["LNAUTO", "LNCONOTH"], ["NTAUTO", "NTCONOTH"])},
        "commercial": {"c_and_i": (["LNCI"], ["NTCI"]),
                       "nonres_re": (["LNRENRES"], ["NTRENRES"])}}
WINDOWS = {"W1": ((2001, 2006), (2007, 2012)), "W2": ((2001, 2013), (2014, 2019))}
PRIMARY = ("W1",)          # fixed in PREREG_C3 section 2
MIN_BOOK, TOPQ = 1000.0, 0.05
log = []


def hyperz(N, K, n, k):
    mu = n * K / N
    var = n * (K / N) * (1 - K / N) * (N - n) / (N - 1)
    return ((k - mu) / np.sqrt(var) if var > 0 else np.nan), mu


def run(P, F, cats, tr, te):
    D = P.copy()
    for c, (bal, nco) in cats.items():
        D[f"bal_{c}"] = D[bal].fillna(0).sum(axis=1)
        D[f"nco_{c}"] = D[nco].fillna(0).sum(axis=1)
    D["tb"] = sum(D[f"bal_{c}"] for c in cats)
    D["tn"] = sum(D[f"nco_{c}"] for c in cats)
    T = D[(D.origin_year >= tr[0]) & (D.origin_year <= tr[1]) & (D.tb >= MIN_BOOK)].copy()
    T["y"] = T.tn / T.tb
    lo, hi = T.y.quantile(.01), T.y.quantile(.99)
    T["y"] = T.y.clip(lo, hi)
    for c in cats:
        T[f"s_{c}"] = T[f"bal_{c}"] / T.tb

    # rho, training only
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

    # as-of balance sheet: the bank's LAST training year
    A = T.sort_values("origin_year").groupby("CERT").tail(1).set_index("CERT")
    # realised system category rates in the test window (scenario is given)
    E = D[(D.origin_year >= te[0]) & (D.origin_year <= te[1])]
    sys_te = {c: float(E[f"nco_{c}"].sum() / E[f"bal_{c}"].sum())
              if E[f"bal_{c}"].sum() > 0 else 0. for c in cats}

    B = pd.DataFrame(index=A.index)
    B["tier1"], B["la"] = A.tier1_lev, A.log_assets
    r1 = sum(A[f"s_{c}"].fillna(0) * sys_te[c] for c in cats)
    fser = {c: pd.Series(A.index.map(fac[c]), index=A.index).astype(float).fillna(1.) for c in cats}
    rser = {c: pd.Series(A.index.map(rawf[c]), index=A.index).astype(float).fillna(1.) for c in cats}
    B["R1_group_rate"] = r1
    B["R2_own_history"] = sum(A[f"s_{c}"].fillna(0) * sys_te[c] * fser[c] for c in cats)
    B["R3_mix_residual"] = sum(A[f"s_{c}"].fillna(0) * rser[c] for c in cats)

    w = F[(F.FAILDATE >= dt.datetime(te[0], 1, 1)) & (F.FAILDATE <= dt.datetime(te[1], 12, 31))]
    B["failed"] = B.index.isin(set(w.CERT)).astype(int)

    N, K, n = len(B), int(B.failed.sum()), int(TOPQ * len(B))
    zmin, _ = hyperz(N, K, n, 0)
    out = {"_meta": {"N": N, "K": K, "n": n, "base_pct": round(100 * K / N, 3),
                     "rho_training": round(rho, 4), "min_attainable_z": round(float(zmin), 2),
                     "downside_reachable": bool(zmin < -1.96)}}
    for rule in ("R1_group_rate", "R2_own_history", "R3_mix_residual"):
        top = B.nlargest(n, rule)
        k = int(top.failed.sum())
        z, mu = hyperz(N, K, n, k)
        rest = B.drop(top.index)
        out[rule] = {"k": k, "expected": round(float(mu), 2),
                     "lift": round(k / mu, 3) if mu > 0 else None, "z": round(float(z), 2),
                     "tier1_flagged": round(float(top.tier1.median()), 3),
                     "tier1_rest": round(float(rest.tier1.median()), 3),
                     "tier1_gap": round(float(top.tier1.median() - rest.tier1.median()), 3),
                     "la_flagged": round(float(top.la.median()), 3),
                     "la_rest": round(float(rest.la.median()), 3)}
    return out


def main():
    P = pd.read_csv(PANEL, low_memory=False)
    F = pd.DataFrame(json.loads(FAIL.read_text()))
    F["FAILDATE"] = pd.to_datetime(F.FAILDATE)
    F["CERT"] = pd.to_numeric(F.CERT, errors="coerce")
    F = F.dropna(subset=["CERT"])

    res, h = {}, {}
    for wname, (tr, te) in WINDOWS.items():
        res[wname] = {}
        for pname, cats in PORT.items():
            r = run(P, F, cats, tr, te)
            res[wname][pname] = r
            m = r["_meta"]
            tag = "PRIMARY" if wname in PRIMARY else "descriptive, excluded from verdict"
            print(f"\n=== {wname} {pname}  train {tr} test {te}   [{tag}] ===")
            print(f"  N={m['N']:,} K={m['K']} base={m['base_pct']}% n={m['n']} "
                  f"rho={m['rho_training']} min-z={m['min_attainable_z']} "
                  f"reachable={m['downside_reachable']}")
            for rule in ("R1_group_rate", "R2_own_history", "R3_mix_residual"):
                d = r[rule]
                print(f"  {rule:16s} k={d['k']:3d}/{d['expected']:5.1f} lift {d['lift']:5.2f}x "
                      f"z {d['z']:+6.2f} | tier1 {d['tier1_flagged']:6.3f} vs "
                      f"{d['tier1_rest']:6.3f} gap {d['tier1_gap']:+6.3f}")
            if wname in PRIMARY:
                h[pname] = r

    # verdict per PREREG_C3 section 5, W1 arms only
    H1 = all(h[p]["R1_group_rate"]["z"] < -1.96 for p in h)
    H2 = all(h[p]["R1_group_rate"]["tier1_gap"] > h[p]["R3_mix_residual"]["tier1_gap"]
             and h[p]["R1_group_rate"]["tier1_gap"] > 0 for p in h)
    H3 = all(min(h[p]["R2_own_history"]["lift"], h[p]["R3_mix_residual"]["lift"]) > 1
             and max(h[p]["R2_own_history"]["z"], h[p]["R3_mix_residual"]["z"]) > 1.96 for p in h)
    verdict = ("PROCEED" if H1 and H2 else "PROCEED NARROWED" if H1 else
               "MECHANISM ONLY" if H2 and H3 else "KILL")
    res["_hypotheses"] = {"H1_antiselection": H1, "H2_capital_mechanism": H2, "H3_detection": H3}
    res["_verdict"] = verdict
    res["_violations"] = log
    (HERE / "prereg_c3_results.json").write_text(json.dumps(res, indent=2, default=float))
    print(f"\nH1 {H1}   H2 {H2}   H3 {H3}   ->  VERDICT: {verdict}")


if __name__ == "__main__":
    main()
