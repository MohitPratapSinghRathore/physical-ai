"""Part 2: the cognitive contrast. Registered in notes/prereg_cognitive_contrast.md first.

Same source, weights, sample restriction, adjustment set, debt/asset/buffer measures and
inference as A31. Cognitive exposure replaces embodiment P, measured with Felten, Raj and
Seamans AIOE and with Eloundou et al. GPT exposure, both already crosswalked to OCCP.

Cognitive exposure indices measure TASK OVERLAP, not displacement and not timing. This
compares WHERE WAGE-BACKED DEBT SITS, not which technology arrives first.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd
from scipy import stats
import importlib.util

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
spec = importlib.util.spec_from_file_location("sb2", ROOT / "src" / "sipp_buffers_v2.py")
sb2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(sb2)

DEBTS = sb2.DEBTS
ASSETS = sb2.ASSETS


def build_groups():
    """Top-quintile cognitive and top-quintile embodied occupation sets, employment weighted."""
    grid = pd.read_csv(OUT / "paei_c.csv")
    base = grid[grid["c"] == 0.0][["occp", "title", "embodiment_P", "employment",
                                   "wage_bill"]].dropna(subset=["employment"])
    base = base[base["employment"] > 0].copy()

    val = pd.read_csv(OUT / "paei_validation.csv")
    val["soc"] = val["onet_soc"].astype(str).str[:7]
    cw = pd.read_csv(OUT / "occp_to_paei.csv")[["occp", "soc"]]
    agg = val.groupby("soc").agg(aioe=("aioe", "mean"),
                                 gpt=("dv_rating_beta", "mean")).reset_index()
    m = cw.merge(agg, on="soc", how="left")
    B = base.merge(m[["occp", "aioe", "gpt"]], on="occp", how="left")

    def top_q(col):
        d = B.dropna(subset=[col]).sort_values(col)
        c = np.cumsum(d["employment"].to_numpy()) / d["employment"].sum()
        cut = np.interp(0.80, c, d[col].to_numpy())
        return set(B.loc[B[col] >= cut, "occp"]), float(cut)

    cog_a, cut_a = top_q("aioe")
    cog_g, cut_g = top_q("gpt")
    d = B.sort_values("embodiment_P")
    c = np.cumsum(d["employment"].to_numpy()) / d["employment"].sum()
    cutP = float(np.interp(0.80, c, d["embodiment_P"].to_numpy()))
    emb = set(B.loc[B["embodiment_P"] >= cutP, "occp"])
    return B, {"cognitive_AIOE_top20": cog_a, "cognitive_GPT_top20": cog_g,
               "embodied_top20": emb}, {"aioe": cut_a, "gpt": cut_g, "P": cutP}


def main():
    B, groups, cuts = build_groups()
    for g, s in groups.items():
        sub = B[B["occp"].isin(s)]
        print(f"{g:22s} {len(s):4d} occupations, {sub['employment'].sum():>12,.0f} workers, "
              f"wage bill ${sub['wage_bill'].sum()/1e9:,.1f}bn")

    D, _ = sb2.load()
    hh = sb2.build_hh(D)
    D["hh"] = D["SSUID"].astype(str) + "_" + D["ERESIDENCEID"].astype(str)
    for g, s in groups.items():
        hh[g] = D[D["occ"].isin(s)].groupby("hh").size().reindex(hh.index).fillna(0) > 0
    hh["any_exposed"] = hh[list(groups)].any(axis=1)
    R = hh[(hh["any_employed"]) & hh["ref_age"].between(25, 64)].copy()
    base_mask = ~R[list(groups)].any(axis=1)
    print(f"\nrestricted sample: {len(R):,}; base (no top-quintile exposure): "
          f"{int(base_mask.sum()):,}")

    # ---------- full disclosure levels ----------
    rows = []
    for g in list(groups) + ["no_top_quintile_exposure"]:
        d = R[base_mask] if g == "no_top_quintile_exposure" else R[R[g]]
        w = d["wgt"].to_numpy(float)
        ti = float((d["hh_inc_a"] * w).sum())
        r = {"group": g, "n": len(d), "thin": len(d) < 100, "weighted": float(w.sum()),
             "median_hh_income": sb2.wmedian(d["hh_inc_a"], w)}
        for lab, _c in DEBTS:
            v = d[lab].fillna(0.0)
            r[f"dti_{lab}"] = 100 * float((v * w).sum()) / ti if ti else np.nan
        for lab, _c in ASSETS:
            r[f"med_{lab}"] = sb2.wmedian(d[lab], w)
        r["med_networth"] = sb2.wmedian(d["networth"], w)
        r["buffer_under_1mo"] = sb2.wshare(
            (d["liquid_bank"].fillna(0) < d["hh_inc_m"].replace(0, np.nan)).fillna(True).to_numpy(), w)
        awb = pd.to_numeric(d["awb"], errors="coerce")
        ok = awb.isin([1, 2]).to_numpy()
        r["unable_pay"] = sb2.wshare((awb == 1).to_numpy()[ok], w[ok]) if ok.sum() else np.nan
        rows.append(r)
    T = pd.DataFrame(rows)
    T.round(3).to_csv(OUT / "cognitive_contrast_levels.csv", index=False)

    # ---------- regression adjustment, same control set ----------
    R["log_inc"] = np.log1p(R["hh_inc_a"].clip(lower=0))
    R["under1mo"] = (R["liquid_bank"].fillna(0)
                     < R["hh_inc_m"].replace(0, np.nan)).fillna(True).astype(float)
    for lab in ["mortgage", "all_debt", "vehicle", "unsecured_total", "credit_card"]:
        R[f"dti_{lab}"] = R[lab].fillna(0) / R["hh_inc_a"].replace(0, np.nan)
    reg = []
    for outcome in ["under1mo", "dti_mortgage", "dti_all_debt", "dti_unsecured_total"]:
        d = R[np.isfinite(R[outcome])].copy()
        X = pd.get_dummies(d["region"].astype("Int64").astype(str), prefix="r",
                           drop_first=True).astype(float)
        X["age"] = d["ref_age"]; X["hhsize"] = d["hhsize"]
        X["earners"] = d["n_earners"]; X["log_inc"] = d["log_inc"]
        for g in groups:
            X[g] = d[g].astype(float)
        X = X.fillna(0.0)
        Xm = np.column_stack([np.ones(len(d)), X.to_numpy(float)])
        y = d[outcome].to_numpy(float); wt = d["wgt"].to_numpy(float)
        Wr = np.sqrt(wt)
        beta, *_ = np.linalg.lstsq(Xm * Wr[:, None], y * Wr, rcond=None)
        names = ["const"] + list(X.columns)
        resid = y - Xm @ beta
        dof = max(len(d) - Xm.shape[1], 1)
        s2 = float((wt * resid ** 2).sum() / wt.sum()) * len(d) / dof
        se = np.sqrt(np.diag(np.linalg.pinv((Xm * wt[:, None]).T @ Xm) * s2 * wt.mean()))
        for g in groups:
            i = names.index(g)
            reg.append({"outcome": outcome, "group": g, "coef": float(beta[i]),
                        "se": float(se[i]),
                        "t": float(beta[i] / se[i]) if se[i] else np.nan})
    RG = pd.DataFrame(reg)
    RG.round(5).to_csv(OUT / "cognitive_contrast_adjusted.csv", index=False)

    # ---------- shares of national debt service / rent held ----------
    shares = []
    tot_m = float((R["mortgage"].fillna(0) * R["wgt"]).sum())
    tot_c = float((R["credit_card"].fillna(0) + R["vehicle"].fillna(0)
                   + R["unsecured_total"].fillna(0)) * R["wgt"]).sum() if False else \
        float(((R["unsecured_total"].fillna(0) + R["vehicle"].fillna(0)) * R["wgt"]).sum())
    tot_rent = float((R["rentmort"].fillna(0) * R["wgt"]).sum())
    for g in groups:
        d = R[R[g]]
        shares.append({"group": g,
                       "share_mortgage_balance_pct": 100 * float(
                           (d["mortgage"].fillna(0) * d["wgt"]).sum()) / tot_m,
                       "share_consumer_balance_pct": 100 * float(
                           ((d["unsecured_total"].fillna(0) + d["vehicle"].fillna(0))
                            * d["wgt"]).sum()) / tot_c,
                       "share_rent_or_mortgage_payment_pct": 100 * float(
                           (d["rentmort"].fillna(0) * d["wgt"]).sum()) / tot_rent})
    S = pd.DataFrame(shares)
    S.round(2).to_csv(OUT / "cognitive_contrast_shares.csv", index=False)

    # ---------- P1r repeated with wage-appropriate labour tax rates ----------
    # effective labour tax rises with earnings: approximate with the ratio of group mean
    # wage to the economy-wide mean, applied to the progressive federal income component.
    w_all = json.loads((OUT / "legW_us_derived.json").read_text())
    econ_mean = w_all["wage_bill_usd_bn"] * 1e9 / 183665726
    p1 = []
    for g, s in groups.items():
        sub = B[B["occp"].isin(s)]
        mw = sub["wage_bill"].sum() / sub["employment"].sum()
        ratio = mw / econ_mean
        # federal income tax component scales with earnings; payroll is capped so it does not
        fed_inc = 0.1285 * min(ratio, 2.0)
        payroll = 0.1552 * (1.0 if ratio <= 1 else max(0.6, 1 / ratio))
        sl = 0.0346 * min(ratio, 2.0)
        tau_l_g = fed_inc + payroll + sl
        p1.append({"group": g, "mean_wage_usd": mw, "wage_ratio_to_economy": ratio,
                   "tau_l_group": tau_l_g,
                   "loss_per_dollar_at_s1_tauk10": tau_l_g - 0.10,
                   "loss_per_dollar_at_s0": tau_l_g,
                   "rho_star_with_labour_share": max(
                       (tau_l_g - (0.337 * tau_l_g + 0.663 * 0.10)) / (tau_l_g * 0.75), 0.0)})
    P1 = pd.DataFrame(p1)
    P1.round(4).to_csv(OUT / "cognitive_contrast_p1r.csv", index=False)

    (OUT / "cognitive_contrast_summary.json").write_text(json.dumps(
        {"cuts": cuts, "levels": T.round(4).to_dict("records"),
         "adjusted": RG.round(5).to_dict("records"),
         "shares": S.round(3).to_dict("records"),
         "p1r_by_group": P1.round(4).to_dict("records")}, indent=2))

    pd.set_option("display.width", 250)
    print("\n=== LEVELS, restricted sample ===")
    print(T[["group", "n", "median_hh_income", "dti_mortgage", "dti_all_debt",
             "dti_unsecured_total", "dti_vehicle", "buffer_under_1mo",
             "med_liquid_bank", "med_networth"]].round(2).to_string(index=False))
    print("\n=== ADJUSTED (vs households with no top-quintile exposure) ===")
    print(RG.round(4).to_string(index=False))
    print("\n=== SHARES of the restricted-sample totals ===")
    print(S.round(2).to_string(index=False))
    print("\n=== P1r with wage-appropriate labour tax rates ===")
    print(P1.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
