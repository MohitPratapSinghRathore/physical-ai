"""
Layer 2 (2020 episode), per PREREGISTRATION section 6.

Construct rebuilt on 2019Q2 balance sheets and 2018 county income; shock and
instrument on 2019->2020; outcome window 2020Q1-2022Q4.

Section 6 states in advance: Layer 2 is confounded by CARES, PPP and expanded
unemployment insurance, which broke the normal link from income loss to credit
loss, and it CANNOT rescue a Layer 1 failure.
"""
from pathlib import Path
import io
import json
import zipfile
import numpy as np
import pandas as pd

from estimate import CONTROLS, first_stage_F, r2_oos, tsls
from build_debtor_wage_shares import read_zip_csv, wage_share

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"
MIN_CELL = 100
L2_CONTROLS = ["sh_resre", "sh_consumer", "sh_cre", "sh_constr", "sh_ci",
               "sh_ag", "sh_sec", "tier1_lev", "cre_conc", "log_assets",
               "dep_assets", "brokered", "loans_assets"]
HELD_OUT = {"48", "38", "40", "35", "56", "02", "22", "54"}


def debtor_shares_2019():
    h = read_zip_csv(RAW / "pums2019" / "csv_hus.zip",
                     ["SERIALNO", "PUMA", "ST", "TEN", "WGTP", "HINCP",
                      "MRGP", "GRNTP", "ADJINC", "TYPE", "NP", "TYPEHUGQ"])
    sercol = "SERIALNO" if "SERIALNO" in h.columns else "serialno"
    tcol = "TYPE" if "TYPE" in h.columns else "TYPEHUGQ"
    for c in ["TEN", "WGTP", "HINCP", "MRGP", "GRNTP", "ADJINC", tcol, "NP"]:
        if c in h.columns:
            h[c] = pd.to_numeric(h[c], errors="coerce")
    h = h[(h[tcol] == 1) & (h["NP"] > 0) & (h["WGTP"] > 0)]
    h["puma_id"] = h["ST"].str.zfill(2) + h["PUMA"].str.zfill(5)

    p = read_zip_csv(RAW / "pums2019" / "csv_pus.zip",
                     ["SERIALNO", "WAGP", "ADJINC"])
    psc = "SERIALNO" if "SERIALNO" in p.columns else "serialno"
    p["WAGP"] = pd.to_numeric(p["WAGP"], errors="coerce").fillna(0)
    wage = p.groupby(psc)["WAGP"].sum().rename("hh_wage")
    h = h.merge(wage, left_on=sercol, right_index=True, how="left")
    h["hh_wage"] = h["hh_wage"].fillna(0)
    adj = h["ADJINC"] / 1e6
    h["hh_wage_adj"] = h["hh_wage"] * adj
    h["hincp_adj"] = h["HINCP"] * adj

    groups = {"mortgage": h["TEN"] == 1, "renter": h["TEN"] == 3,
              "all": h["TEN"].notna()}
    rows = []
    for name, mask in groups.items():
        g = h[mask]
        hh = g.groupby("puma_id").apply(
            lambda d: wage_share(d, "WGTP"), include_groups=False)
        n = g.groupby("puma_id").size().rename("n_hh")
        r = pd.DataFrame({"wage_share": hh, "n_hh": n})
        r["group"] = name
        rows.append(r.reset_index())
    puma = pd.concat(rows, ignore_index=True)
    puma = puma[puma["n_hh"] >= MIN_CELL]

    cnt = pd.read_csv(RAW / "puma2010_to_county_afact_hu.csv",
                      dtype={"puma_id": str, "county_fips": str})
    out = []
    for name in groups:
        s = puma[puma["group"] == name]
        m = cnt.merge(s, on="puma_id", how="inner")
        agg = m.groupby("county_fips").apply(
            lambda d: (d["wage_share"] * d["hu"]).sum() / d["hu"].sum()
            if d["hu"].sum() > 0 else np.nan, include_groups=False)
        out.append(agg.rename(f"ws_{name}"))
    return pd.concat(out, axis=1)


def main():
    R = {"note": ("Layer 2 is confounded by CARES, PPP and expanded UI, and "
                  "per section 6 cannot rescue a Layer 1 failure.")}

    cache = OUT / "county_debtor_wage_shares_2019.csv"
    if cache.exists():
        cw = pd.read_csv(cache, dtype={"county_fips": str}).set_index(
            "county_fips")
    else:
        cw = debtor_shares_2019()
        cw.to_csv(cache)
    print(f"  county debtor shares 2019: {len(cw)}")

    bea = pd.read_csv(RAW / "bea_cainc4_all_areas.csv", dtype=str)
    bea["GeoFIPS"] = bea["GeoFIPS"].str.strip().str.replace('"', "", regex=False)

    def ln(lc, yr):
        s = bea[bea["LineCode"] == lc].set_index("GeoFIPS")[yr]
        return pd.to_numeric(s[~s.index.str.endswith("000")], errors="coerce")

    ws_pop = (ln("50", "2018") / ln("10", "2018")).replace(
        [np.inf, -np.inf], np.nan)
    shock = ((ln("50", "2020") - ln("50", "2019"))
             / ln("50", "2019")).replace([np.inf, -np.inf], np.nan)

    # instrument: 2018 shares x national 2019->2020 growth, leave-one-out
    with zipfile.ZipFile(RAW / "CAINC5N.zip") as z:
        d5 = pd.read_csv(io.BytesIO(
            z.read("CAINC5N__ALL_AREAS_2001_2024.csv")),
            encoding="latin-1", dtype=str)
    d5["GeoFIPS"] = d5["GeoFIPS"].str.strip().str.replace('"', "", regex=False)
    secs = [s for s in ["100", "200", "300", "400", "500", "600", "700", "800",
                        "900", "1000", "1100", "1200", "1300", "1400", "1500",
                        "1600", "1700", "1800"] if s in set(d5["LineCode"])]
    fr = {}
    for lc in secs:
        s = d5[d5["LineCode"] == lc].set_index("GeoFIPS")
        s = s[~s.index.str.endswith("000")]
        fr[lc] = {y: pd.to_numeric(s[y], errors="coerce")
                  for y in ("2018", "2019", "2020")}
    idx = fr[secs[0]]["2018"].index
    base = pd.DataFrame({lc: fr[lc]["2018"].reindex(idx) for lc in secs})
    sh = base.div(base.sum(axis=1, min_count=1), axis=0)
    z_b = pd.Series(0.0, index=idx)
    for lc in secs:
        a = fr[lc]["2019"].reindex(idx)
        b = fr[lc]["2020"].reindex(idx)
        g = ((b.sum() - b.fillna(0)) - (a.sum() - a.fillna(0))) \
            / (a.sum() - a.fillna(0))
        z_b = z_b.add(sh[lc].fillna(0) * g, fill_value=0)

    county = pd.DataFrame({"ws_pop": ws_pop, "wage_shock": shock,
                           "z_bartik": z_b}).join(cw)

    # ---- banks ----------------------------------------------------------
    sod = pd.read_csv(RAW / "fdic_sod_2019.csv").dropna(subset=["STCNTYBR"])
    sod["fips"] = (sod["STCNTYBR"].astype(float).astype(int)
                   .astype(str).str.zfill(5))
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"], errors="coerce").fillna(0)

    def dw(col):
        s = sod.copy()
        s["v"] = s["fips"].map(county[col])
        s = s.dropna(subset=["v"])
        return s.groupby("CERT").apply(
            lambda d: np.average(d["v"], weights=d["DEPSUMBR"])
            if d["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)

    bank = pd.DataFrame({c: dw(c) for c in
                         ["ws_pop", "wage_shock", "z_bartik",
                          "ws_mortgage", "ws_renter", "ws_all"]})
    sod["ho"] = sod["fips"].str[:2].isin(HELD_OUT)
    bank["dep_share_heldout"] = sod.groupby("CERT").apply(
        lambda d: np.average(d["ho"].astype(float), weights=d["DEPSUMBR"])
        if d["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)
    bank["n_counties"] = sod.groupby("CERT")["fips"].nunique()

    fin = pd.read_csv(RAW / "fdic_financials_20190630.csv")
    num = [c for c in fin.columns
           if c not in ("NAMEFULL", "STNAME", "ID", "REPDTE")]
    fin[num] = fin[num].apply(pd.to_numeric, errors="coerce")
    fin["SCOTHER"] = (fin["SC"].fillna(0) - fin["SCMUNI"].fillna(0)).clip(lower=0)
    fin["book"] = fin["LNLSGR"].fillna(0) + fin["SC"].fillna(0)
    fin = fin[(fin["book"] > 0) & (fin["LNLSGR"] > 0) & (fin["ASSET"] > 0)]
    f = fin.merge(bank, left_on="CERT", right_index=True, how="left")

    beta = pd.read_csv(ROOT / "framework" / "labor_backing"
                       / "claim_class_rules.csv")
    beta = {r.claim_class: float(r.labour_backing_share)
            for r in beta.itertuples()}
    CM = {"LNRERES": ("home_mortgage", "ws_mortgage"),
          "LNREMULT": ("multifamily_mortgage", "ws_renter"),
          "LNCRCD": ("credit_card", "ws_all"),
          "LNAUTO": ("auto_loan", "ws_all"),
          "LNCONOTH": ("other_consumer", "ws_all"),
          "SCMUNI": ("state_local_debt", "ws_all"),
          "SCOTHER": ("treasury", "ws_all")}
    b = f["book"]
    comp = np.zeros(len(f)); deb = np.zeros(len(f))
    for item, (cls, wcol) in CM.items():
        share = f[item].fillna(0) / b
        comp += share * beta[cls]
        deb += share * beta[cls] * f[wcol]
    f["lb_rival"] = comp * f["ws_pop"]
    f["lb_debtor"] = deb
    f["gap"] = f["lb_debtor"] - f["lb_rival"]

    f["sh_resre"] = f["LNRERES"].fillna(0)/b
    f["sh_cre"] = (f["LNRENRES"].fillna(0)+f["LNREMULT"].fillna(0))/b
    f["sh_constr"] = f["LNRECONS"].fillna(0)/b
    f["sh_ci"] = f["LNCI"].fillna(0)/b
    f["sh_consumer"] = (f["LNCRCD"].fillna(0)+f["LNAUTO"].fillna(0)
                        + f["LNCONOTH"].fillna(0))/b
    f["sh_ag"] = (f["LNAG"].fillna(0)+f["LNREAG"].fillna(0))/b
    f["sh_sec"] = f["SC"].fillna(0)/b
    f["tier1_lev"] = f["RBC1AAJ"]
    f["cre_conc"] = ((f["LNRECONS"].fillna(0)+f["LNRENRES"].fillna(0)
                      + f["LNREMULT"].fillna(0))/f["RBCT1J"]).replace(
                          [np.inf, -np.inf], np.nan)*100
    f["log_assets"] = np.log(f["ASSET"])
    f["dep_assets"] = f["DEP"]/f["ASSET"]
    f["brokered"] = f["BRO"].fillna(0)/f["DEP"].replace(0, np.nan)
    f["loans_assets"] = f["LNLSGR"]/f["ASSET"]
    f["hh_loans"] = f[["LNRERES", "LNCRCD", "LNAUTO", "LNCONOTH"]].fillna(0).sum(axis=1)
    f["hh_frac"] = f["hh_loans"]/f["LNLSGR"]
    f["held_out"] = f["dep_share_heldout"] > 0.50

    # ---- outcomes 2020Q1-2022Q4, section 14.4 rule -----------------------
    oc = pd.read_csv(RAW / "fdic_outcomes_2020_raw.csv")
    oc["year"] = oc["REPDTE"].astype(str).str[:4].astype(int)
    oc["q"] = oc["REPDTE"].astype(str).str[4:].map(
        {"0331": 1, "0630": 2, "0930": 3, "1231": 4})
    for c in oc.columns:
        if c != "REPDTE":
            oc[c] = pd.to_numeric(oc[c], errors="coerce")
    oc = oc.sort_values(["CERT", "year", "q"])
    for nm, ytd, qf in [("reres", "NTRERES", "NTRERESQ"),
                        ("crcd", "NTCRCD", "NTCRCDQ"),
                        ("auto", "NTAUTO", "NTAUTOQ"),
                        ("conoth", "NTCONOTH", None)]:
        if qf and qf in oc.columns and oc[qf].notna().any():
            oc[f"{nm}_q"] = oc[qf]
        else:
            g = oc.groupby(["CERT", "year"])[ytd]
            oc[f"{nm}_q"] = oc[ytd] - g.shift(1).fillna(0)
            oc.loc[oc["q"] == 1, f"{nm}_q"] = oc.loc[oc["q"] == 1, ytd]
    oc["hh_q"] = oc[["reres_q", "crcd_q", "auto_q", "conoth_q"]].sum(
        axis=1, min_count=1)
    agg = oc.groupby("CERT")["hh_q"].sum().rename("nt_hh")
    f = f.merge(agg, left_on="CERT", right_index=True, how="left")
    f["y_hh"] = 100 * f["nt_hh"] / f["hh_loans"]

    d = f[(f["ASSET"] >= 50_000) & (f["sh_consumer"] <= .90)
          & (f["sh_ci"] <= .90) & (f["n_counties"] <= 100)
          & (f["hh_loans"] >= 5_000) & (f["hh_frac"] >= .05)].copy()
    d = d.dropna(subset=["y_hh", "gap", "lb_rival", "wage_shock", "z_bartik"])
    for c in L2_CONTROLS:
        d[c] = d[c].fillna(d[c].median())
    tr = d[~d["held_out"]].copy()
    te = d[d["held_out"]].copy()
    lo, hi = tr["y_hh"].quantile(.01), tr["y_hh"].quantile(.99)
    for x in (tr, te):
        x["y"] = x["y_hh"].clip(lo, hi)
    for v in ("gap", "lb_rival", "wage_shock", "z_bartik"):
        mu, sd = tr[v].mean(), tr[v].std()
        for x in (tr, te):
            x[v+"_s"] = (x[v]-mu)/sd
    ysd = tr["y"].std(); ymu = tr["y"].mean()
    for x in (tr, te):
        x["y_s"] = (x["y"]-ymu)/ysd

    exog = np.column_stack([np.ones(len(tr)), tr[L2_CONTROLS].to_numpy(),
                            tr[["gap_s", "lb_rival_s"]].to_numpy()])
    endog = np.column_stack([tr["wage_shock_s"],
                             tr["lb_rival_s"]*tr["wage_shock_s"],
                             tr["gap_s"]*tr["wage_shock_s"]])
    Z = np.column_stack([tr["z_bartik_s"],
                         tr["lb_rival_s"]*tr["z_bartik_s"],
                         tr["gap_s"]*tr["z_bartik_s"]])
    fit = tsls(tr["y_s"].to_numpy(), endog, exog, Z,
               groups=tr["STNAME"].to_numpy())
    k0 = exog.shape[1]
    R["n_train"] = int(len(tr)); R["n_test"] = int(len(te))
    for j, nm in enumerate(["shock", "rival_x_shock", "gap_x_shock"]):
        se = float(np.sqrt(fit["V_cl"][k0+j, k0+j]))
        R[nm] = {"coef": float(fit["beta"][k0+j]), "se": se,
                 "ci_lo": float(fit["beta"][k0+j]-1.96*se),
                 "ci_hi": float(fit["beta"][k0+j]+1.96*se)}
    R["first_stage_F"] = first_stage_F(endog, exog, Z, tr["STNAME"].to_numpy())
    R["gap_sd"] = float(d["gap"].std())
    R["wage_shock_mean"] = float(d["wage_shock"].mean())
    (OUT / "layer2_payload.json").write_text(
        json.dumps(R, indent=2, default=float), encoding="utf-8")
    print(json.dumps(R, indent=2, default=float))


if __name__ == "__main__":
    main()
