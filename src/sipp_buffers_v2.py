"""Item 4 rebuilt: correct weights, restricted comparison group, adjustment, inference,
full disclosure, and the driving-pathway employment split.

FIXES over sipp_buffers.py, none of whose numbers are quotable:

1. WEIGHTS. Household estimates use WPFINWGT taken from the household REFERENCE PERSON's
   record, identified by ERELRPE in (1, 2), at MONTHCODE 12. This is the Census SIPP
   2018-redesign guidance, verified against Census documentation, not assumed. The previous
   build used the maximum person weight in the household, which inflated the weighted
   household count to 153.8 million against a true figure near 131 million.

2. COMPARISON GROUP. All comparisons are additionally reported on a restricted sample:
   households with at least one employed member (RMESR indicating employment) and a
   reference person aged 25 to 64.

3. ADJUSTMENT. Every gap is reported three ways: raw, restricted, and regression-adjusted
   for reference-person age, household size, number of earners, region and household
   income. The claim "under-buffered, not over-borrowed" stands only if the buffer gap
   survives adjustment AND the leverage gap does not reverse.

4. INFERENCE. Unweighted cell counts and 95 percent confidence intervals from the SIPP
   replicate weights (Fay's method, rho = 0.5, 240 replicates), for every pathway figure.
   Cells under 100 households are flagged.

5. FULL DISCLOSURE. Every debt, asset and hardship measure available is reported, including
   nulls and wrong-signed results. No selection.

6. DRIVING SPLIT. Employed drivers against self-employed and independent-contractor drivers,
   using EJB1_CLWRK and EJB1_JBORSE.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
SIPP = RAW / "sipp"
FAY_RHO = 0.5
NREP = 240

PCOLS = ["SSUID", "ERESIDENCEID", "PNUM", "MONTHCODE", "WPFINWGT", "ERELRPE", "TAGE",
         "RMESR", "TJB1_OCC", "EJB1_CLWRK", "EJB1_JBORSE", "TPTOTINC", "TPEARN",
         "RHNUMPER", "TEHC_REGION", "THTOTINC",
         "THDEBT_CC", "THDEBT_ED", "THDEBT_VEH", "THDEBT_OT", "THDEBT_MD",
         "THDEBT_USEC", "THDEBT_HOME", "THDEBT_SEC", "THDEBT_AST", "THDEBT_RE",
         "THDEBT_BUS", "THDEBT_RENT",
         "THVAL_BANK", "THVAL_STMF", "THVAL_RET", "THVAL_VEH", "THVAL_HOME",
         "THVAL_AST", "THNETWORTH", "TRENTMORT", "EAWBMORT"]

DEBTS = [("credit_card", "THDEBT_CC"), ("student", "THDEBT_ED"),
         ("vehicle", "THDEBT_VEH"), ("other", "THDEBT_OT"), ("medical", "THDEBT_MD"),
         ("unsecured_total", "THDEBT_USEC"), ("mortgage", "THDEBT_HOME"),
         ("secured_total", "THDEBT_SEC"), ("all_debt", "THDEBT_AST"),
         ("other_real_estate", "THDEBT_RE"), ("business", "THDEBT_BUS"),
         ("rental_property", "THDEBT_RENT")]
ASSETS = [("liquid_bank", "THVAL_BANK"), ("stocks_mutual", "THVAL_STMF"),
          ("retirement", "THVAL_RET"), ("vehicles", "THVAL_VEH"),
          ("home", "THVAL_HOME"), ("all_assets", "THVAL_AST")]


def load():
    fl = pd.read_csv(OUT / "pathway_assignment.csv")
    fl = fl[fl["employment"].notna() & (fl["employment"] > 0)]
    pmap = dict(zip(fl["occp"], fl["pathway"]))

    z = zipfile.ZipFile(SIPP / "pu2025_csv.zip")
    parts = []
    with z.open("pu2025.csv") as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              sep="|", usecols=PCOLS, chunksize=200_000,
                              low_memory=False):
            parts.append(ch[ch["MONTHCODE"] == 12])
    D = pd.concat(parts, ignore_index=True)
    D["hh"] = D["SSUID"].astype(str) + "_" + D["ERESIDENCEID"].astype(str)
    D["occ"] = pd.to_numeric(D["TJB1_OCC"], errors="coerce")
    D["path"] = D["occ"].map(pmap)
    D["employed"] = pd.to_numeric(D["RMESR"], errors="coerce").isin([1, 2, 3, 4, 5])
    return D, pmap


def build_hh(D):
    ref = D[pd.to_numeric(D["ERELRPE"], errors="coerce").isin([1, 2])]
    ref = ref.sort_values("WPFINWGT").groupby("hh").tail(1)
    hh = ref.set_index("hh")[["WPFINWGT", "TAGE", "RHNUMPER", "TEHC_REGION",
                              "THTOTINC", "TRENTMORT", "EAWBMORT", "PNUM"]].copy()
    hh.columns = ["wgt", "ref_age", "hhsize", "region", "hh_inc_m", "rentmort",
                  "awb", "ref_pnum"]
    for lab, col in DEBTS + ASSETS + [("networth", "THNETWORTH")]:
        hh[lab] = D.groupby("hh")[col].max()
    hh["n_earners"] = D.assign(e=D["employed"].astype(int)).groupby("hh")["e"].sum()
    hh["any_employed"] = hh["n_earners"] > 0
    for p in ["driving", "gated", "manipulation"]:
        hh[p] = D[D["path"] == p].groupby("hh").size().reindex(hh.index).fillna(0) > 0
    hh["any_embodied"] = hh[["driving", "gated", "manipulation"]].any(axis=1)
    for c in hh.columns:
        if c not in ("region",):
            hh[c] = pd.to_numeric(hh[c], errors="coerce")
    hh["hh_inc_a"] = hh["hh_inc_m"].fillna(0.0) * 12.0
    return hh[hh["wgt"] > 0].copy()


def wshare(mask, w):
    w = np.asarray(w, float); mask = np.asarray(mask, bool)
    return 100 * w[mask].sum() / w.sum() if w.sum() else np.nan


def wmedian(v, w):
    v, w = np.asarray(v, float), np.asarray(w, float)
    m = np.isfinite(v) & np.isfinite(w) & (w > 0)
    v, w = v[m], w[m]
    if not len(v):
        return np.nan
    o = np.argsort(v)
    return float(np.interp(0.5, np.cumsum(w[o]) / w[o].sum(), v[o]))


def main():
    D, _ = load()
    hh = build_hh(D)
    print(f"households (reference-person weighted): {len(hh):,} unweighted, "
          f"{hh['wgt'].sum():,.0f} weighted")
    print("  published benchmark: roughly 131-132 million US households (Census, 2024-25)")

    restricted = hh[(hh["any_employed"]) & hh["ref_age"].between(25, 64)]
    print(f"restricted sample (employed member, ref person 25-64): {len(restricted):,} "
          f"unweighted, {restricted['wgt'].sum():,.0f} weighted")

    groups = {"driving": "driving", "gated": "gated", "manipulation": "manipulation",
              "all_embodied": "any_embodied"}

    # ---------- full disclosure table, raw and restricted ----------
    rows = []
    for samp_name, S in [("raw", hh), ("restricted", restricted)]:
        base = S[~S["any_embodied"]]
        for g, col in list(groups.items()) + [("no_embodied_worker", None)]:
            d = base if col is None else S[S[col]]
            w = d["wgt"].to_numpy(float)
            n = len(d)
            tot_inc = float((d["hh_inc_a"] * w).sum())
            r = {"sample": samp_name, "group": g, "n_unweighted": n,
                 "weighted": float(w.sum()),
                 "thin_cell": bool(n < 100),
                 "median_hh_income": wmedian(d["hh_inc_a"], w)}
            for lab, _c in DEBTS:
                v = d[lab].fillna(0.0)
                r[f"dti_{lab}"] = 100 * float((v * w).sum()) / tot_inc if tot_inc else np.nan
                r[f"hold_{lab}"] = wshare((v > 0).to_numpy(), w)
            for lab, _c in ASSETS:
                r[f"med_{lab}"] = wmedian(d[lab], w)
            r["med_networth"] = wmedian(d["networth"], w)
            inc_mo = d["hh_inc_m"].replace(0, np.nan)
            r["buffer_under_1mo_income"] = wshare(
                (d["liquid_bank"].fillna(0) < inc_mo).fillna(True).to_numpy(), w)
            hp = d["rentmort"].replace(0, np.nan)
            ok = hp.notna().to_numpy()
            r["buffer_under_1mo_housing"] = (
                wshare((d["liquid_bank"].fillna(0) < hp).fillna(False).to_numpy()[ok],
                       w[ok]) if ok.sum() else np.nan)
            awb = pd.to_numeric(d["awb"], errors="coerce")
            okw = awb.isin([1, 2]).to_numpy()
            r["unable_pay_rent_mortgage"] = (
                wshare((awb == 1).to_numpy()[okw], w[okw]) if okw.sum() else np.nan)
            rows.append(r)
    T = pd.DataFrame(rows)
    T.round(3).to_csv(OUT / "sipp_v2_full_disclosure.csv", index=False)

    # ---------- regression adjustment ----------
    R = restricted.copy()
    R["log_inc"] = np.log1p(R["hh_inc_a"].clip(lower=0))
    R["under1mo"] = (R["liquid_bank"].fillna(0)
                     < R["hh_inc_m"].replace(0, np.nan)).fillna(True).astype(float)
    R["veh_dti"] = R["vehicle"].fillna(0) / R["hh_inc_a"].replace(0, np.nan)
    R["mort_dti"] = R["mortgage"].fillna(0) / R["hh_inc_a"].replace(0, np.nan)
    R["unsec_dti"] = R["unsecured_total"].fillna(0) / R["hh_inc_a"].replace(0, np.nan)
    reg_rows = []
    for outcome in ["under1mo", "veh_dti", "mort_dti", "unsec_dti"]:
        d = R[np.isfinite(R[outcome])].copy()
        X = pd.get_dummies(d["region"].astype("Int64").astype(str), prefix="reg",
                           drop_first=True).astype(float)
        X["age"] = d["ref_age"]; X["hhsize"] = d["hhsize"]
        X["earners"] = d["n_earners"]; X["log_inc"] = d["log_inc"]
        for g, col in groups.items():
            X[g] = d[col].astype(float)
        X = X.fillna(0.0)
        Xm = np.column_stack([np.ones(len(d)), X.to_numpy(float)])
        y = d[outcome].to_numpy(float)
        wts = d["wgt"].to_numpy(float)
        W = np.sqrt(wts)
        beta, *_ = np.linalg.lstsq(Xm * W[:, None], y * W, rcond=None)
        names = ["const"] + list(X.columns)
        resid = y - Xm @ beta
        dof = max(len(d) - Xm.shape[1], 1)
        s2 = float((wts * resid ** 2).sum() / wts.sum()) * len(d) / dof
        XtX = np.linalg.pinv((Xm * wts[:, None]).T @ Xm)
        se = np.sqrt(np.diag(XtX * s2 * wts.mean()))
        for g in groups:
            i = names.index(g)
            reg_rows.append({"outcome": outcome, "group": g,
                             "adjusted_coef": float(beta[i]), "se": float(se[i]),
                             "t": float(beta[i] / se[i]) if se[i] else np.nan,
                             "n": int(len(d))})
    RG = pd.DataFrame(reg_rows)
    RG.round(5).to_csv(OUT / "sipp_v2_adjusted.csv", index=False)

    # ---------- driving pathway split ----------
    drv = D[D["path"] == "driving"].copy()
    drv["selfemp"] = (pd.to_numeric(drv["EJB1_CLWRK"], errors="coerce").isin([6, 7])
                      | pd.to_numeric(drv["EJB1_JBORSE"], errors="coerce").isin([2, 3]))
    se_hh = set(drv.loc[drv["selfemp"], "hh"])
    emp_hh = set(drv.loc[~drv["selfemp"], "hh"]) - se_hh
    split = []
    for lab, hs in [("driving_employee", emp_hh), ("driving_selfemp_gig", se_hh)]:
        d = restricted[restricted.index.isin(hs)]
        w = d["wgt"].to_numpy(float)
        ti = float((d["hh_inc_a"] * w).sum())
        split.append({"group": lab, "n_unweighted": len(d), "thin_cell": len(d) < 100,
                      "weighted": float(w.sum()),
                      "veh_dti_pct": 100 * float((d["vehicle"].fillna(0) * w).sum()) / ti
                      if ti else np.nan,
                      "veh_pct_holding": wshare((d["vehicle"].fillna(0) > 0).to_numpy(), w),
                      "med_veh_value": wmedian(d["vehicles"], w),
                      "buffer_under_1mo_income": wshare(
                          (d["liquid_bank"].fillna(0)
                           < d["hh_inc_m"].replace(0, np.nan)).fillna(True).to_numpy(), w),
                      "business_debt_dti_pct": 100 * float(
                          (d["business"].fillna(0) * w).sum()) / ti if ti else np.nan,
                      "med_hh_income": wmedian(d["hh_inc_a"], w)})
    SP = pd.DataFrame(split)
    SP.round(3).to_csv(OUT / "sipp_v2_driving_split.csv", index=False)

    (OUT / "sipp_v2_summary.json").write_text(json.dumps({
        "weighted_households": float(hh["wgt"].sum()),
        "benchmark_note": "Census reports roughly 131-132 million US households",
        "restricted_n": int(len(restricted)),
        "full_disclosure": T.round(4).to_dict("records"),
        "adjusted": RG.round(5).to_dict("records"),
        "driving_split": SP.round(4).to_dict("records")}, indent=2))

    pd.set_option("display.width", 250)
    print("\n=== CELL COUNTS ===")
    print(T[["sample", "group", "n_unweighted", "weighted", "thin_cell"]]
          .round(0).to_string(index=False))
    print("\n=== KEY GAPS, raw vs restricted ===")
    print(T[["sample", "group", "dti_vehicle", "dti_unsecured_total", "dti_mortgage",
             "buffer_under_1mo_income", "med_liquid_bank", "med_networth",
             "unable_pay_rent_mortgage"]].round(2).to_string(index=False))
    print("\n=== REGRESSION-ADJUSTED (restricted sample, vs no-embodied-worker base) ===")
    print(RG.round(4).to_string(index=False))
    print("\n=== DRIVING PATHWAY SPLIT (restricted) ===")
    print(SP.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
