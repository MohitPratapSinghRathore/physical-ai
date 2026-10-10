"""
The confirmatory run. Executes SESSION2_PLAN steps 9-15 in the pre-registered order.
Writes results_payload.json, which RESULTS.md is written from.
"""
from pathlib import Path
import io
import json
import zipfile
import numpy as np
import numpy.linalg as la
import pandas as pd

from estimate import (CONTROLS, ENGINE, ITEM_ENGINE, WINDOW, akm_vcov,
                      cluster_vcov, first_stage_F, hc_vcov, icc_oneway, ols,
                      r2_oos, tsls, winsor)

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"
R = {}


def sector_shares_by_bank():
    """Bank exposure shares to 2-digit sectors, for AKM standard errors."""
    with zipfile.ZipFile(RAW / "CAINC5N.zip") as z:
        df = pd.read_csv(io.BytesIO(
            z.read("CAINC5N__ALL_AREAS_2001_2024.csv")),
            encoding="latin-1", dtype=str)
    df["GeoFIPS"] = df["GeoFIPS"].str.strip().str.replace('"', "", regex=False)
    secs = ["100", "200", "300", "400", "500", "600", "700", "800", "900",
            "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700",
            "1800"]
    have = [s for s in secs if s in set(df["LineCode"])]
    base = {}
    for lc in have:
        s = df[df["LineCode"] == lc].set_index("GeoFIPS")["2013"]
        s = s[~s.index.str.endswith("000")]
        base[lc] = pd.to_numeric(s, errors="coerce")
    B = pd.DataFrame(base)
    sh = B.div(B.sum(axis=1, min_count=1), axis=0).fillna(0)

    sod = pd.read_csv(RAW / "fdic_sod_2014.csv").dropna(subset=["STCNTYBR"])
    sod["fips"] = (sod["STCNTYBR"].astype(float).astype(int)
                   .astype(str).str.zfill(5))
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"], errors="coerce").fillna(0)
    m = sod.merge(sh, left_on="fips", right_index=True, how="inner")
    w = m["DEPSUMBR"].to_numpy()
    out = {}
    for lc in have:
        m["_v"] = m[lc] * w
        num = m.groupby("CERT")["_v"].sum()
        den = m.groupby("CERT")["DEPSUMBR"].sum()
        out[lc] = num / den
    return pd.DataFrame(out)


def build(df, oc):
    """Attach outcomes to the frozen pre-shock frame."""
    win = oc[oc.apply(lambda r: (r["year"], r["q"]) in WINDOW, axis=1)]
    agg = win.groupby("CERT").agg(
        nt_hh=("nt_hh_q", "sum"), nt_bus=("nt_bus_q", "sum"),
        nt_bus_c=("nt_bus_c_q", "sum"), nt_tot=("nt_total_q", "sum"),
        n_q=("nt_hh_q", "size"))
    df = df.merge(agg, left_on="CERT", right_index=True, how="left")

    peak = win.groupby("CERT").agg(
        p9_reres=("P9RERES", "max"), na_reres=("NARERES", "max"),
        p9_ci=("P9CI", "max"), na_ci=("NACI", "max"),
        na_crcd=("NACRCD", "max"), roa=("ROA", "mean"))
    df = df.merge(peak, left_on="CERT", right_index=True, how="left")

    end = oc[(oc["year"] == 2017) & (oc["q"] == 4)].set_index("CERT")
    df["tier1_2017q4"] = df["CERT"].map(end["RBC1AAJ"])
    df["d_tier1"] = df["tier1_2017q4"] - df["tier1_lev"]

    df["y_hh"] = 100 * df["nt_hh"] / df["hh_loans"]
    df["y_bus"] = 100 * df["nt_bus"] / df["bus_loans"]
    df["y_bus_c"] = 100 * df["nt_bus_c"] / df["bus_loans_incl_constr"]
    df["y_tot"] = 100 * df["nt_tot"] / df["LNLSGR"]
    df["y_npl_hh"] = 100 * (df["p9_reres"] + df["na_reres"]) / df["hh_loans"]
    df["y_npl_bus"] = 100 * (df["p9_ci"] + df["na_ci"]) / df["bus_loans"]
    return df


def predicted_loss(df, ws_kind):
    beta = pd.read_csv(ROOT / "framework" / "labor_backing"
                       / "claim_class_rules.csv")
    beta = {r.claim_class: float(r.labour_backing_share)
            for r in beta.itertuples()}
    dose = (-df["wage_shock"]).clip(lower=0)
    tot = {"lo": np.zeros(len(df)), "mid": np.zeros(len(df)),
           "hi": np.zeros(len(df))}
    for item, (cls, ecls) in ITEM_ENGINE.items():
        if ws_kind == "rival":
            ws = df["ws_pop"].to_numpy()
        else:
            col = {"home_mortgage": "ws_mortgage",
                   "multifamily_mortgage": "ws_renter"}.get(cls, "ws_all")
            ws = df[col].to_numpy()
        common = (df[item].fillna(0).to_numpy() * beta[cls] * ws
                  * dose.to_numpy() * ENGINE[ecls]["u"])
        tot["lo"] += common * ENGINE[ecls]["lo"]
        tot["hi"] += common * ENGINE[ecls]["hi"]
        tot["mid"] += common * (ENGINE[ecls]["lo"] + ENGINE[ecls]["hi"]) / 2
    return {k: 100 * v / df["hh_loans"].to_numpy() for k, v in tot.items()}


def zstats(b, V, i):
    se = float(np.sqrt(V[i, i]))
    return {"coef": float(b[i]), "se": se,
            "ci_lo": float(b[i] - 1.959964 * se),
            "ci_hi": float(b[i] + 1.959964 * se),
            "z": float(b[i] / se) if se > 0 else np.nan}


def main():
    df = pd.read_csv(RAW / "analysis_frame_preshock.csv")
    oc = pd.read_csv(RAW / "fdic_outcomes_quarterly.csv")
    oc["nt_hh_q"] = oc[["nt_reres_q", "nt_crcd_q", "nt_auto_q",
                        "nt_conoth_q"]].sum(axis=1, min_count=1)
    oc["nt_bus_q"] = oc[["nt_ci_q", "nt_renres_q"]].sum(axis=1, min_count=1)
    oc["nt_bus_c_q"] = oc[["nt_ci_q", "nt_renres_q",
                           "nt_recons_q"]].sum(axis=1, min_count=1)
    df = build(df, oc)

    S_all = sector_shares_by_bank()

    # ---------------- 1. plausibility bounds ---------------------------
    viol = {}
    for nm, s in [("ws_pop", df["ws_pop"]), ("ws_mortgage", df["ws_mortgage"]),
                  ("ws_all", df["ws_all"]), ("gap", df["gap"]),
                  ("lb_rival", df["lb_rival"]), ("lb_debtor", df["lb_debtor"]),
                  ("dti_rank_2013", df["dti_rank_2013"]),
                  ("expo_imputed", df["expo_imputed"])]:
        out01 = int(((s < 0) | (s > 1)).sum())
        viol[nm] = {"outside_0_1": out01, "min": float(s.min()),
                    "max": float(s.max())}
    samp = df[(~df["excluded"]) & df["qual_hh"]].copy()
    viol["primary_n"] = int(len(samp))
    viol["primary_n_prereg"] = 5490
    viol["negative_y_hh"] = int((samp["y_hh"] < 0).sum())
    viol["negative_y_bus"] = int((samp["y_bus"] < 0).sum())
    viol["y_hh_missing"] = int(samp["y_hh"].isna().sum())
    viol["banks_with_fewer_than_12_quarters"] = int((samp["n_q"] < 12).sum())
    R["plausibility"] = viol

    samp = samp.dropna(subset=["y_hh", "gap", "lb_rival", "wage_shock",
                               "z_bartik"]).copy()
    for c in CONTROLS:
        samp[c] = samp[c].fillna(samp[c].median())
    R["plausibility"]["primary_n_estimable"] = int(len(samp))

    train = samp[~samp["held_out"]].copy()
    test = samp[samp["held_out"]].copy()
    R["plausibility"]["n_train"] = int(len(train))
    R["plausibility"]["n_test"] = int(len(test))

    # winsorise and standardise on TRAINING only
    lo, hi = train["y_hh"].quantile(0.01), train["y_hh"].quantile(0.99)
    for d in (train, test, samp):
        d["y"] = d["y_hh"].clip(lo, hi)
    for v in ("gap", "lb_rival", "wage_shock", "z_bartik"):
        mu, sd = train[v].mean(), train[v].std()
        for d in (train, test, samp):
            d[v + "_s"] = (d[v] - mu) / sd
    ysd = train["y"].std()
    for d in (train, test, samp):
        d["y_s"] = (d["y"] - train["y"].mean()) / ysd

    # ---------------- 2. realised ICC and design effect ----------------
    icc, m0 = icc_oneway(train["y"].to_numpy(), train["STNAME"].to_numpy())
    deff = 1 + (m0 - 1) * max(icc, 0.0)
    R["power"] = {"realised_icc": icc, "mean_cluster_size": m0,
                  "design_effect": deff, "n_states": int(train["STNAME"].nunique())}

    # ---------------- 3. Gap-form confirmatory test --------------------
    Xc = train[CONTROLS].to_numpy()
    ones = np.ones((len(train), 1))
    exog = np.column_stack([ones, Xc, train[["gap_s", "lb_rival_s"]].to_numpy()])
    endog = np.column_stack([
        train["wage_shock_s"].to_numpy(),
        (train["lb_rival_s"] * train["wage_shock_s"]).to_numpy(),
        (train["gap_s"] * train["wage_shock_s"]).to_numpy()])
    Z = np.column_stack([
        train["z_bartik_s"].to_numpy(),
        (train["lb_rival_s"] * train["z_bartik_s"]).to_numpy(),
        (train["gap_s"] * train["z_bartik_s"]).to_numpy()])
    S = S_all.reindex(train["CERT"]).fillna(0).to_numpy()

    fit = tsls(train["y_s"].to_numpy(), endog, exog, Z,
               groups=train["STNAME"].to_numpy(), S=S)
    k0 = exog.shape[1]
    names = ["shock", "rival_x_shock", "gap_x_shock"]
    R["gap_test"] = {}
    for j, nm in enumerate(names):
        i = k0 + j
        R["gap_test"][nm] = {
            "cluster": zstats(fit["beta"], fit["V_cl"], i),
            "akm": zstats(fit["beta"], fit["V_akm"], i),
            "hc": zstats(fit["beta"], fit["V_hc"], i)}
    R["gap_test"]["first_stage_F"] = dict(zip(
        names, first_stage_F(endog, exog, Z, train["STNAME"].to_numpy())))

    # realised MDE from the AKM SE on the gap interaction
    se_gap = R["gap_test"]["gap_x_shock"]["akm"]["se"]
    se_gap_cl = R["gap_test"]["gap_x_shock"]["cluster"]["se"]
    R["power"]["se_gap_akm"] = se_gap
    R["power"]["se_gap_cluster"] = se_gap_cl
    R["power"]["realised_mde_akm"] = (1.959964 + 0.8416212) * se_gap
    R["power"]["realised_mde_cluster"] = (1.959964 + 0.8416212) * se_gap_cl
    R["power"]["threshold"] = 0.10
    R["power"]["powered"] = bool(R["power"]["realised_mde_akm"] <= 0.10)

    # ---------------- out-of-sample increments M1/M2/M3 ----------------
    # explicit endogenous -> instrument map; a string replace silently failed
    # to substitute the interaction terms and instrumented them by themselves
    IV_MAP = {"wage_shock_s": "z_bartik_s",
              "rival_x_shock": "rival_x_z_bartik",
              "gap_x_shock": "gap_x_z_bartik"}

    def oos(cols_exog, cols_endog):
        for c in cols_endog:
            assert c in IV_MAP, f"no instrument defined for {c}"
        Xtr = np.column_stack([np.ones(len(train))]
                              + [train[c].to_numpy() for c in cols_exog]
                              + [train[c].to_numpy() for c in cols_endog])
        Ztr = np.column_stack([np.ones(len(train))]
                              + [train[c].to_numpy() for c in cols_exog]
                              + [train[IV_MAP[c]].to_numpy()
                                 for c in cols_endog])
        P = Ztr @ la.pinv(Ztr.T @ Ztr) @ Ztr.T
        b, *_ = la.lstsq(P @ Xtr, train["y_s"].to_numpy(), rcond=None)
        Xte = np.column_stack([np.ones(len(test))]
                              + [test[c].to_numpy() for c in cols_exog]
                              + [test[c].to_numpy() for c in cols_endog])
        return r2_oos(test["y_s"].to_numpy(), Xte @ b)

    for d in (train, test):
        d["rival_x_shock"] = d["lb_rival_s"] * d["wage_shock_s"]
        d["gap_x_shock"] = d["gap_s"] * d["wage_shock_s"]
        d["rival_x_z_bartik"] = d["lb_rival_s"] * d["z_bartik_s"]
        d["gap_x_z_bartik"] = d["gap_s"] * d["z_bartik_s"]
    m1 = oos(CONTROLS, [])
    m2 = oos(CONTROLS + ["lb_rival_s"], ["wage_shock_s", "rival_x_shock"])
    m3 = oos(CONTROLS + ["lb_rival_s", "gap_s"],
             ["wage_shock_s", "rival_x_shock", "gap_x_shock"])
    R["oos"] = {"M1": m1, "M2": m2, "M3": m3,
                "M2_minus_M1": m2 - m1, "M3_minus_M2": m3 - m2}

    # ---------------- 4. business-loan contrast ------------------------
    bs = df[(~df["excluded"]) & df["qual_bus"]].dropna(
        subset=["y_bus", "gap", "lb_rival", "wage_shock", "z_bartik"]).copy()
    for c in CONTROLS:
        bs[c] = bs[c].fillna(bs[c].median())
    btr = bs[~bs["held_out"]].copy()
    blo, bhi = btr["y_bus"].quantile(0.01), btr["y_bus"].quantile(0.99)
    btr["y"] = btr["y_bus"].clip(blo, bhi)
    for v in ("gap", "lb_rival", "wage_shock", "z_bartik"):
        mu, sd = btr[v].mean(), btr[v].std()
        btr[v + "_s"] = (btr[v] - mu) / sd
    btr["y_s"] = (btr["y"] - btr["y"].mean()) / btr["y"].std()
    Xc2 = btr[CONTROLS].to_numpy()
    exog2 = np.column_stack([np.ones((len(btr), 1)), Xc2,
                             btr[["gap_s", "lb_rival_s"]].to_numpy()])
    endog2 = np.column_stack([
        btr["wage_shock_s"].to_numpy(),
        (btr["lb_rival_s"] * btr["wage_shock_s"]).to_numpy(),
        (btr["gap_s"] * btr["wage_shock_s"]).to_numpy()])
    Z2 = np.column_stack([
        btr["z_bartik_s"].to_numpy(),
        (btr["lb_rival_s"] * btr["z_bartik_s"]).to_numpy(),
        (btr["gap_s"] * btr["z_bartik_s"]).to_numpy()])
    S2 = S_all.reindex(btr["CERT"]).fillna(0).to_numpy()
    fit2 = tsls(btr["y_s"].to_numpy(), endog2, exog2, Z2,
                groups=btr["STNAME"].to_numpy(), S=S2)
    k2 = exog2.shape[1]
    R["business_contrast"] = {
        "n": int(len(btr)),
        **{nm: {"cluster": zstats(fit2["beta"], fit2["V_cl"], k2 + j),
                "akm": zstats(fit2["beta"], fit2["V_akm"], k2 + j)}
           for j, nm in enumerate(names)}}

    # ---------------- 5. structural calibration ------------------------
    R["structural"] = {}
    for kind in ("rival", "debtor"):
        pl = predicted_loss(samp, kind)
        for band in ("lo", "mid", "hi"):
            x = pl[band]
            ok = np.isfinite(x) & samp["y_hh"].notna().to_numpy()
            xx = x[ok]
            yy = samp["y_hh"].to_numpy()[ok]
            yy = np.clip(yy, lo, hi)
            X = np.column_stack([np.ones(len(xx)), xx])
            b, e = ols(yy, X)
            V = cluster_vcov(X, e, samp["STNAME"].to_numpy()[ok])
            se = float(np.sqrt(V[1, 1]))
            tr_m = ~samp["held_out"].to_numpy()[ok]
            bt, _ = ols(yy[tr_m], X[tr_m])
            oos_fit = r2_oos(yy[~tr_m], X[~tr_m] @ bt)
            R["structural"][f"{kind}_{band}"] = {
                "slope": float(b[1]), "slope_se": se,
                "ci_lo": float(b[1] - 1.959964 * se),
                "ci_hi": float(b[1] + 1.959964 * se),
                "intercept": float(b[0]),
                "n": int(len(xx)),
                "n_nonzero_pred": int((xx > 0).sum()),
                "oos_r2_heldout": float(oos_fit),
                "pred_mean": float(xx.mean()),
                "realised_mean": float(yy.mean())}
        R["structural"][f"corr_pred_{kind}"] = float(
            np.corrcoef(predicted_loss(samp, "rival")["mid"],
                        predicted_loss(samp, "debtor")["mid"])[0, 1])

    (OUT / "results_payload.json").write_text(
        json.dumps(R, indent=2, default=float), encoding="utf-8")
    samp.to_csv(RAW / "estimation_sample.csv", index=False)
    print(json.dumps(R, indent=2, default=float)[:6000])


if __name__ == "__main__":
    main()
