"""
Build the bank-year panel: constructs and controls at t, outcomes t+1..t+3.

DEVIATION, logged: the debtor-specific county wage shares exist only for the ACS
2009-2013 vintage, so they are held constant across origin years exactly as the
accounts hold the class coefficients constant. Population wage shares vary by
year from BEA. Recorded in DEVIATIONS.md.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "predictive"
LB = ROOT / "framework" / "labor_backing"
OUT = Path(__file__).resolve().parent

CLASS_ITEM = {
    "home_mortgage": ("LNRERES", "mortgage"),
    "multifamily_mortgage": ("LNREMULT", "renter"),
    "credit_card": ("LNCRCD", "all"),
    "auto_loan": ("LNAUTO", "all"),
    "other_consumer": ("LNCONOTH", "all"),
    "commercial_mortgage": ("LNRENRES", None),
    "noncorporate_business_debt": ("LNREAG", None),
    "corporate_loans": ("LNCI", None),
    "state_local_debt": ("SCMUNI", "all"),
    "treasury": ("SCOTHER", "all"),
}
HH_NT = ["NTRERES", "NTCRCD", "NTAUTO", "NTCONOTH"]
BUS_NT = ["NTCI", "NTRENRES"]


def county_wage_share_by_year():
    bea = pd.read_csv(RAW / "bea_cainc4_all_areas.csv", dtype=str)
    bea["GeoFIPS"] = bea["GeoFIPS"].str.strip().str.replace('"', "",
                                                            regex=False)
    out = {}
    for yr in range(2000, 2023):
        y = str(yr)
        if y not in bea.columns:
            continue
        k = bea[bea["LineCode"].isin(["10", "50"])].copy()
        k[y] = pd.to_numeric(k[y], errors="coerce")
        w = k.pivot_table(index="GeoFIPS", columns="LineCode", values=y,
                          aggfunc="first")
        if "10" not in w or "50" not in w:
            continue
        w = w[w["10"] > 0]
        s = (w["50"] / w["10"])
        out[yr] = s[~s.index.str.endswith("000")]
    return out


def main():
    fin = pd.read_csv(RAW / "fin_june.csv", low_memory=False)
    dec = pd.read_csv(RAW / "fin_dec.csv", low_memory=False)
    sod = pd.read_csv(RAW / "sod.csv", low_memory=False)

    num = [c for c in fin.columns if c not in
           ("NAMEFULL", "STNAME", "ID", "REPDTE")]
    fin[num] = fin[num].apply(pd.to_numeric, errors="coerce")
    for c in dec.columns:
        if c not in ("ID", "REPDTE"):
            dec[c] = pd.to_numeric(dec[c], errors="coerce")

    fin["SCOTHER"] = (fin["SC"].fillna(0) - fin["SCMUNI"].fillna(0)
                      ).clip(lower=0)
    fin["book"] = fin["LNLSGR"].fillna(0) + fin["SC"].fillna(0)
    fin = fin[(fin["book"] > 0) & (fin["ASSET"] > 0) & (fin["LNLSGR"] > 0)]

    beta = pd.read_csv(LB / "claim_class_rules.csv")
    beta = {r.claim_class: float(r.labour_backing_share)
            for r in beta.itertuples()}

    # county wage shares
    ws_year = county_wage_share_by_year()
    deb = pd.read_csv(RAW / "county_debtor_wage_shares_2013.csv",
                      dtype={"county_fips": str})
    deb_map = {g: d.set_index("county_fips")["wage_share"]
               for g, d in deb.groupby("group")}
    # payment-weighted variant, where it exists (mortgage and renter groups)
    debpw_map = {g: d.set_index("county_fips")["wage_share_payment_wtd"].where(
                     lambda s: s > 0)
                 for g, d in deb.groupby("group")}

    sod = sod.dropna(subset=["STCNTYBR"])
    sod["fips"] = (pd.to_numeric(sod["STCNTYBR"], errors="coerce")
                   .dropna().astype(int).astype(str).str.zfill(5)
                   .reindex(sod.index))
    sod = sod.dropna(subset=["fips"])
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"],
                                    errors="coerce").fillna(0)
    sod["YEAR"] = pd.to_numeric(sod["YEAR"], errors="coerce")

    def dep_weight(year, series):
        s = sod[sod["YEAR"] == year].copy()
        s["v"] = s["fips"].map(series)
        s = s.dropna(subset=["v"])
        if s.empty:
            return pd.Series(dtype=float)
        g = s.groupby("CERT").apply(
            lambda d: np.average(d["v"], weights=d["DEPSUMBR"])
            if d["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)
        return g

    rows = []
    for y, g in fin.groupby("origin_year"):
        y = int(y)
        pop = ws_year.get(y, ws_year.get(max(ws_year)))
        ws_pop = dep_weight(y, pop)
        ws_deb = {k: dep_weight(y, v) for k, v in deb_map.items()}
        ws_debpw = {k: dep_weight(y, v.dropna())
                    for k, v in debpw_map.items()}
        n_cty = sod[sod["YEAR"] == y].groupby("CERT")["fips"].nunique()

        g = g.copy()
        g["ws_pop"] = g["CERT"].map(ws_pop)
        for k, v in ws_deb.items():
            g[f"ws_{k}"] = g["CERT"].map(v)
        for k, v in ws_debpw.items():
            g[f"wspw_{k}"] = g["CERT"].map(v)
        g["n_counties"] = g["CERT"].map(n_cty)

        b = g["book"]
        comp = np.zeros(len(g))
        lbd = np.zeros(len(g))
        lbpw = np.zeros(len(g))
        for cls, (item, grp) in CLASS_ITEM.items():
            share = g[item].fillna(0) / b
            comp = comp + share * beta[cls]
            if grp is not None:
                w = g.get(f"ws_{grp}")
                lbd = lbd + share * beta[cls] * (w if w is not None else 0)
                wp = g.get(f"wspw_{grp}")
                wp = w if wp is None else wp.fillna(w)
                lbpw = lbpw + share * beta[cls] * (wp if wp is not None else 0)
        g["lb_composition"] = comp
        # NOTE: LB_bank and the pilot's Rival are IDENTICAL by construction -
        # both are the composition leg times the POPULATION wage share. The
        # pre-registration listed them as separate constructs; they are not.
        # The fourth construct is the payment-weighted debtor variant instead.
        # Logged in DEVIATIONS.md.
        g["LB"] = comp * g["ws_pop"]
        g["LB_debtor"] = lbd
        g["LB_debtor_pw"] = lbpw
        g["Gap"] = g["LB_debtor"] - g["LB"]

        g["sh_resre"] = g["LNRERES"].fillna(0) / b
        g["sh_consumer"] = (g["LNCRCD"].fillna(0) + g["LNAUTO"].fillna(0)
                            + g["LNCONOTH"].fillna(0)) / b
        g["sh_cre"] = (g["LNRENRES"].fillna(0) + g["LNREMULT"].fillna(0)) / b
        g["sh_constr"] = g["LNRECONS"].fillna(0) / b
        g["sh_ci"] = g["LNCI"].fillna(0) / b
        g["sh_ag"] = (g["LNAG"].fillna(0) + g["LNREAG"].fillna(0)) / b
        g["sh_sec"] = g["SC"].fillna(0) / b
        g["tier1_lev"] = g["RBC1AAJ"]
        g["cre_conc"] = ((g["LNRECONS"].fillna(0) + g["LNRENRES"].fillna(0)
                          + g["LNREMULT"].fillna(0)) / g["RBCT1J"]).replace(
                              [np.inf, -np.inf], np.nan) * 100
        g["log_assets"] = np.log(g["ASSET"])
        g["dep_assets"] = g["DEP"] / g["ASSET"]
        g["brokered"] = g["BRO"].fillna(0) / g["DEP"].replace(0, np.nan)
        g["loans_assets"] = g["LNLSGR"] / g["ASSET"]
        g["hh_book"] = g[["LNRERES", "LNCRCD", "LNAUTO",
                          "LNCONOTH"]].fillna(0).sum(axis=1)
        g["bus_book"] = g[["LNCI", "LNRENRES"]].fillna(0).sum(axis=1)
        # lagged charge-offs: the strongest conventional predictor
        g["lag_nco"] = g[HH_NT].fillna(0).sum(axis=1) / g["hh_book"].replace(
            0, np.nan)
        rows.append(g)
    P = pd.concat(rows, ignore_index=True)

    # outcomes: cumulative Dec-31 YTD charge-offs over t+1..t+3
    dec["hh_nco"] = dec[HH_NT].fillna(0).sum(axis=1)
    dec["bus_nco"] = dec[BUS_NT].fillna(0).sum(axis=1)
    d = dec.set_index(["CERT", "out_year"])
    for h in (1, 2, 3):
        for nm, col in (("hh", "hh_nco"), ("bus", "bus_nco"),
                        ("tot", "NTLNLS")):
            key = P.set_index(["CERT", P["origin_year"] + h]).index
            P[f"{nm}_y{h}"] = d[col].reindex(key).to_numpy()
    for nm in ("hh", "bus", "tot"):
        P[f"{nm}_c1"] = P[f"{nm}_y1"]
        P[f"{nm}_c2"] = P[[f"{nm}_y1", f"{nm}_y2"]].sum(axis=1, min_count=1)
        P[f"{nm}_c3"] = P[[f"{nm}_y1", f"{nm}_y2",
                           f"{nm}_y3"]].sum(axis=1, min_count=1)
    # outcome rates
    for h in (1, 2, 3):
        P[f"y_hh_{h}"] = 100 * P[f"hh_c{h}"] / P["hh_book"].replace(0, np.nan)
        P[f"y_bus_{h}"] = 100 * P[f"bus_c{h}"] / P["bus_book"].replace(0, np.nan)
        P[f"y_tot_{h}"] = 100 * P[f"tot_c{h}"] / P["LNLSGR"].replace(0, np.nan)
    end = d["RBC1AAJ"]
    P["tier1_end"] = end.reindex(
        P.set_index(["CERT", P["origin_year"] + 3]).index).to_numpy()
    P["d_tier1"] = P["tier1_end"] - P["tier1_lev"]
    P["npl_hh"] = (d["P9RERES"].reindex(
        P.set_index(["CERT", P["origin_year"] + 1]).index).to_numpy()
        + d["NARERES"].reindex(
            P.set_index(["CERT", P["origin_year"] + 1]).index).to_numpy())
    P["y_npl_hh"] = 100 * P["npl_hh"] / P["hh_book"].replace(0, np.nan)
    P["failed"] = P["hh_y3"].isna().astype(int)

    P.to_csv(RAW / "panel.csv", index=False)
    rep = {"rows": int(len(P)),
           "origin_years": [int(P.origin_year.min()), int(P.origin_year.max())],
           "banks": int(P.CERT.nunique()),
           "with_LB": int(P["LB"].notna().sum()),
           "with_y_hh_3": int(P["y_hh_3"].notna().sum()),
           "per_year": P.groupby("origin_year")["LB"].count().to_dict()}
    (OUT / "panel_summary.json").write_text(json.dumps(rep, indent=2,
                                                       default=int),
                                            encoding="utf-8")
    print(json.dumps(rep, indent=2, default=int)[:900])


if __name__ == "__main__":
    main()
