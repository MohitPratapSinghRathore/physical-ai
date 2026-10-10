"""Referee-requested rebuild of the decomposition.

Three defects in the published version, all raised by the referee:
  1. the pro rata benchmark was a pooled regression on seven loan shares, which is not the
     object a category allocation rule implies. Build it directly:
         pro_rata_hat(i,t) = sum_c w(i,c,t-1) * lambda(c,t)
     with lagged weights and the realised category rate, denominators aligned to the outcome.
  2. no year effects, so common shocks were being counted as bank-specific persistence and
     were inflating the reported autocorrelation.
  3. bank means were not corrected for estimation noise, so Var(alpha_hat) overstated
     Var(alpha) by sigma2_eps * mean(1/T_i).
Also reports annual cross-sectional performance and the crisis/pooled comparison the referee
corrected.
"""
import json, pathlib
import numpy as np, pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
PANEL = pathlib.Path(r"C:\Users\bdd3\physical-ai-predict\data\raw\predictive\panel.csv")
CATS = {"residential": (["LNRERES"], ["NTRERES"]),
        "credit_card": (["LNCRCD"], ["NTCRCD"]),
        "other_consumer": (["LNAUTO", "LNCONOTH"], ["NTAUTO", "NTCONOTH"])}
MIN_BOOK = 1000.0


def load():
    P = pd.read_csv(PANEL, low_memory=False)
    for c, (bal, nco) in CATS.items():
        P[f"bal_{c}"] = P[bal].fillna(0).sum(axis=1)
        P[f"nco_{c}"] = P[nco].fillna(0).sum(axis=1)
    P["tb"] = sum(P[f"bal_{c}"] for c in CATS)
    P["tn"] = sum(P[f"nco_{c}"] for c in CATS)
    P = P[(P.tb >= MIN_BOOK)].copy()
    P["y"] = P.tn / P.tb
    lo, hi = P.y.quantile(.005), P.y.quantile(.995)
    P["y"] = P.y.clip(lo, hi)
    for c in CATS:
        P[f"w_{c}"] = P[f"bal_{c}"] / P.tb
    return P.sort_values(["CERT", "origin_year"])


def main():
    P = load()
    out = {}

    # ---- realised system category rate by year, lambda(c,t)
    lam = {c: (P.groupby("origin_year")[f"nco_{c}"].sum()
               / P.groupby("origin_year")[f"bal_{c}"].sum()) for c in CATS}
    # ---- lagged weights w(i,c,t-1)
    for c in CATS:
        P[f"wlag_{c}"] = P.groupby("CERT")[f"w_{c}"].shift(1)
    P["prorata_hat"] = sum(P[f"wlag_{c}"] * P.origin_year.map(lam[c]) for c in CATS)
    D = P.dropna(subset=["prorata_hat", "y"]).copy()

    # ================= 1. the direct pro rata benchmark =================
    ss = lambda a: float(np.sum((a - np.mean(a)) ** 2))
    r2_direct = 1 - ss(D.y - D.prorata_hat) / ss(D.y)
    # the published object: pooled regression on contemporaneous shares
    mix = [f"w_{c}" for c in CATS]
    X = np.column_stack([np.ones(len(D))] + [D[m].to_numpy() for m in mix])
    b, *_ = np.linalg.lstsq(X, D.y.to_numpy(), rcond=None)
    r2_reg = 1 - ss(D.y.to_numpy() - X @ b) / ss(D.y.to_numpy())
    out["benchmark"] = {
        "n_obs": int(len(D)), "n_banks": int(D.CERT.nunique()),
        "r2_pooled_share_regression": round(float(r2_reg), 4),
        "r2_direct_prorata_rule": round(float(r2_direct), 4),
        "note": ("the direct rule is the object a category allocation implies; the share "
                 "regression is a best-fit upper bound on it because its coefficients are "
                 "fitted, while the rule's are the realised category rates")}

    # ================= 2. variance model with year effects =================
    # y = mix(lagged weights x category rates) + year effect + bank effect + resid
    D["_m"] = D.prorata_hat
    Xm = np.column_stack([np.ones(len(D)), D._m.to_numpy()])
    bm, *_ = np.linalg.lstsq(Xm, D.y.to_numpy(), rcond=None)
    D["_r1"] = D.y.to_numpy() - Xm @ bm                      # after mix
    yr = D.groupby("origin_year")["_r1"].transform("mean")
    D["_r2"] = D["_r1"] - yr                                 # after year effects
    g = D.groupby("CERT")["_r2"]
    bmean, T = g.transform("mean"), g.transform("size")
    D["_r3"] = D["_r2"] - bmean                              # after bank effects

    v_tot = D.y.var()
    v_mix = (D.y.var() - D["_r1"].var())
    v_yr = (D["_r1"].var() - D["_r2"].var())
    s2_eps = float(D["_r3"].var())
    v_bank_raw = float(bmean.groupby(D.CERT).first().var())
    Ti = T.groupby(D.CERT).first()
    shrink = s2_eps * float(np.mean(1.0 / Ti))
    v_bank_corr = max(v_bank_raw - shrink, 0.0)

    denom = float(v_tot)
    out["variance_model"] = {
        "share_mix": round(float(v_mix / denom), 4),
        "share_year_effects": round(float(v_yr / denom), 4),
        "share_bank_persistent_uncorrected": round(float(v_bank_raw / denom), 4),
        "estimation_noise_in_bank_means": round(float(shrink / denom), 4),
        "share_bank_persistent_corrected": round(float(v_bank_corr / denom), 4),
        "share_transitory": round(float(s2_eps / denom), 4),
        "mean_history_length": round(float(Ti.mean()), 2)}

    # ================= 3. the ICC / autocorrelation tension =================
    icc_simple = float(v_bank_corr / (v_bank_corr + s2_eps))
    R = D[["CERT", "origin_year", "_r1", "_r2", "_r3"]].copy()
    ac = {}
    for col in ("_r1", "_r2", "_r3"):
        S = R.pivot_table(index="CERT", columns="origin_year", values=col)
        a, bb = [], []
        for y0 in sorted(S.columns)[:-1]:
            if y0 + 1 in S.columns:
                m = S[[y0, y0 + 1]].dropna()
                a += list(m[y0]); bb += list(m[y0 + 1])
        ac[col] = float(np.corrcoef(a, bb)[0, 1])
    out["icc_vs_autocorr"] = {
        "icc_implied_by_corrected_decomposition": round(icc_simple, 4),
        "autocorr_after_mix_only": round(ac["_r1"], 4),
        "autocorr_after_mix_and_year": round(ac["_r2"], 4),
        "autocorr_of_within_bank_residual": round(ac["_r3"], 4),
        "note": ("the published 0.494 was measured after mix only, so it carried common year "
                 "shocks. Removing year effects separates the two. A within-bank residual "
                 "autocorrelation materially above zero means the transitory part is itself "
                 "serially correlated, which is the structure Spearman-Brown does NOT assume")}

    # ================= 4. annual cross-sectional performance =================
    ann = {}
    for y0, G in D.groupby("origin_year"):
        if len(G) < 200:
            continue
        ann[int(y0)] = round(float(1 - ss(G.y - G.prorata_hat) / ss(G.y)), 4)
    out["annual_cross_sectional_r2_direct_rule"] = ann
    per = {"pre_crisis_2001_2006": [y for y in ann if 2001 <= y <= 2006],
           "crisis_2007_2010": [y for y in ann if 2007 <= y <= 2010],
           "post_2011_2021": [y for y in ann if y >= 2011]}
    out["period_means"] = {k: round(float(np.mean([ann[y] for y in v])), 4)
                           for k, v in per.items() if v}

    (HERE / "decomp_v2.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
