"""
SESSION2_PLAN steps 2-6: assemble the complete pre-shock analysis frame.

NO OUTCOME IS OPENED HERE. Everything is dated 2014-06-30 or earlier, or is a
treatment-side variable (the 2014-2016 wage-bill shock and its instrument).

Produces data/raw/validation/analysis_frame_preshock.csv, which step 8 joins
outcomes onto. Nothing in this file may be revised once outcomes are opened.
"""
from pathlib import Path
import io
import json
import zipfile
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "validation"
OUT = ROOT / "framework" / "validation"

HELD_OUT_STATES = {"48": "TX", "38": "ND", "40": "OK", "35": "NM",
                   "56": "WY", "02": "AK", "22": "LA", "54": "WV"}
MIN_CELL_DENOM_FRAC = 0.05
MIN_CELL_DENOM_ABS = 5_000
MAX_COUNTIES = 100
MIN_ASSETS = 50_000          # $50m, call report in $000s


def load_cainc5n():
    with zipfile.ZipFile(RAW / "CAINC5N.zip") as z:
        df = pd.read_csv(io.BytesIO(
            z.read("CAINC5N__ALL_AREAS_2001_2024.csv")),
            encoding="latin-1", dtype=str)
    df["GeoFIPS"] = df["GeoFIPS"].str.strip().str.replace('"', "", regex=False)
    return df


def mining_exposure(df):
    """Section 12.6: primary = impute suppressed counties from the state
    residual in proportion to QCEW mining establishment counts."""
    mine = df[df["LineCode"] == "200"].set_index("GeoFIPS")["2013"]
    earn = df[df["LineCode"] == "35"].set_index("GeoFIPS")["2013"]
    earn_n = pd.to_numeric(earn, errors="coerce")

    cty = ~mine.index.str.endswith("000")
    m_cty = pd.to_numeric(mine[cty], errors="coerce")
    st_tot = pd.to_numeric(mine[mine.index.str.endswith("000")
                                & (mine.index != "00000")], errors="coerce")
    st_tot.index = st_tot.index.str[:2]
    st_tot = st_tot[~st_tot.index.duplicated()]

    # QCEW establishment counts for the suppressed cells
    keep = []
    with zipfile.ZipFile(RAW / "qcew_2013_annual.zip") as z:
        with z.open("2013.annual.singlefile.csv") as f:
            for chunk in pd.read_csv(f, dtype=str, chunksize=500_000):
                m = chunk[(chunk["industry_code"] == "21")
                          & (chunk["agglvl_code"] == "74")
                          & (chunk["own_code"] == "5")]
                if len(m):
                    keep.append(m[["area_fips", "annual_avg_estabs"]])
    q = pd.concat(keep).set_index("area_fips")["annual_avg_estabs"]
    q = pd.to_numeric(q, errors="coerce").fillna(0)

    disclosed = m_cty.dropna()
    sup_idx = m_cty[m_cty.isna()].index
    imputed = pd.Series(0.0, index=sup_idx)
    state_of_sup = pd.Series(sup_idx.str[:2], index=sup_idx)
    disc_by_state = disclosed.groupby(disclosed.index.str[:2]).sum()

    for s, grp in imputed.groupby(state_of_sup):
        tot = st_tot.get(s, np.nan)
        if pd.isna(tot):
            continue
        resid = max(tot - disc_by_state.get(s, 0.0), 0.0)
        est = q.reindex(grp.index).fillna(0)
        if est.sum() > 0:
            imputed.loc[grp.index] = resid * est / est.sum()

    m_imputed = pd.concat([disclosed, imputed]).sort_index()
    out = pd.DataFrame({
        "mining_earn_imputed": m_imputed,
        "mining_earn_disclosed": m_cty,
        "earn_total": earn_n.reindex(m_imputed.index),
    })
    out["expo_imputed"] = out["mining_earn_imputed"] / out["earn_total"]
    out["expo_disclosed_only"] = out["mining_earn_disclosed"] / out["earn_total"]
    out["expo_zero"] = out["expo_disclosed_only"].fillna(0.0)
    out["was_suppressed"] = out.index.isin(sup_idx)
    return out.replace([np.inf, -np.inf], np.nan)


def bartik(df):
    """Leave-one-out shift-share on 2-digit NAICS county earnings shares."""
    sectors = ["100", "200", "300", "400", "500", "600", "700", "800", "900",
               "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700",
               "1800", "1900", "2000", "2001", "2002"]
    have = sorted(set(df["LineCode"].unique()) & set(sectors))
    frames = {}
    for lc in have:
        s = df[df["LineCode"] == lc].set_index("GeoFIPS")
        s = s[~s.index.str.endswith("000")]
        frames[lc] = pd.DataFrame({
            "y2013": pd.to_numeric(s["2013"], errors="coerce"),
            "y2014": pd.to_numeric(s["2014"], errors="coerce"),
            "y2016": pd.to_numeric(s["2016"], errors="coerce")})
    idx = frames[have[0]].index
    base = pd.DataFrame(index=idx)
    for lc in have:
        base[lc] = frames[lc]["y2013"].reindex(idx)
    base_tot = base.sum(axis=1, min_count=1)
    shares = base.div(base_tot, axis=0)

    z = pd.Series(0.0, index=idx)
    contrib = pd.Series(0.0, index=idx)
    rotemberg = {}
    for lc in have:
        a = frames[lc]["y2014"].reindex(idx)
        b = frames[lc]["y2016"].reindex(idx)
        nat_a, nat_b = a.sum(), b.sum()
        # leave-one-out national growth: exclude own county
        g_loo = ((nat_b - b.fillna(0)) - (nat_a - a.fillna(0))) \
            / (nat_a - a.fillna(0))
        s_k = shares[lc].fillna(0)
        z = z.add(s_k * g_loo, fill_value=0)
        rotemberg[lc] = float((s_k * g_loo).var())
        contrib += (s_k * g_loo).abs()
    tot = sum(rotemberg.values())
    rotemberg = {k: v / tot for k, v in sorted(
        rotemberg.items(), key=lambda kv: -kv[1])}
    return z.replace([np.inf, -np.inf], np.nan), shares, rotemberg


def main():
    df = load_cainc5n()

    print("Step 3: mining exposure, three handlings")
    expo = mining_exposure(df)
    print(f"  counties: {len(expo)}   suppressed imputed: "
          f"{int(expo['was_suppressed'].sum())}")
    print(f"  expo_imputed >10%: {(expo['expo_imputed'] > .10).sum()}   "
          f"disclosed-only >10%: {(expo['expo_disclosed_only'] > .10).sum()}")

    print("Step 5: leave-one-out shift-share instrument")
    z, shares, rot = bartik(df)
    print(f"  counties with instrument: {z.notna().sum()}")
    print("  top Rotemberg weights: " + ", ".join(
        f"{k}={v:.3f}" for k, v in list(rot.items())[:5]))

    # ---- county frame -----------------------------------------------------
    bea = pd.read_csv(RAW / "bea_cainc4_all_areas.csv", dtype=str)
    bea["GeoFIPS"] = bea["GeoFIPS"].str.strip().str.replace('"', "", regex=False)

    def line(lc, yr):
        s = bea[bea["LineCode"] == lc].set_index("GeoFIPS")[yr]
        s = s[~s.index.str.endswith("000")]
        return pd.to_numeric(s, errors="coerce")

    wage14, wage16 = line("50", "2014"), line("50", "2016")
    pi13, pop13 = line("10", "2013"), line("20", "2013")
    county = pd.DataFrame({
        "wage_shock": (wage16 - wage14) / wage14,
        "pi_per_cap_2013": pi13 / pop13,
    }).replace([np.inf, -np.inf], np.nan)
    county["z_bartik"] = z
    county = county.join(expo[["expo_imputed", "expo_disclosed_only",
                               "expo_zero", "was_suppressed"]])

    # LAUS
    laus = pd.read_csv(OUT / "county_unemployment_preshock.csv",
                       dtype={"fips": str}).set_index("fips")
    county["unemp_2013"] = laus["unemp_2013"]

    # FHFA pre-shock house price growth 2011->2013
    hpi = pd.read_excel(RAW / "fhfa" / "hpi_at_county.xlsx", dtype=str,
                        skiprows=4)
    hpi.columns = ["state", "cname", "fips", "year", "chg", "hpi",
                   "hpi1990", "hpi2000"]
    hpi = hpi[hpi["fips"].str.len() == 5]
    hpi["year"] = pd.to_numeric(hpi["year"], errors="coerce")
    hpi["hpi_n"] = pd.to_numeric(hpi["hpi"].replace(".", None), errors="coerce")
    w = hpi[hpi["year"].isin([2011, 2013])].pivot_table(
        index="fips", columns="year", values="hpi_n")
    county["hpi_growth_11_13"] = (w[2013] / w[2011] - 1)

    # EFA county DTI as an ordinal rank (section 12.7)
    with zipfile.ZipFile(RAW / "efa" / "household-debt.zip") as zf:
        efa = pd.read_csv(io.BytesIO(
            zf.read("household-debt-by-county.csv")),
            dtype={"area_fips": str})
    e13 = efa[(efa["year"] == 2013) & (efa["qtr"] == 4)].copy()
    bins = (e13[["low", "high"]].drop_duplicates()
            .sort_values("low").reset_index(drop=True))
    bins["bin_idx"] = bins.index
    e13 = e13.merge(bins, on=["low", "high"], how="left")
    e13["dti_rank"] = e13["bin_idx"] / (len(bins) - 1)
    county["dti_rank_2013"] = e13.set_index("area_fips")["dti_rank"]

    county.to_csv(RAW / "county_frame_preshock.csv")
    print(f"  county frame: {len(county)} rows; "
          f"unemp {county.unemp_2013.notna().sum()}, "
          f"hpi {county.hpi_growth_11_13.notna().sum()}, "
          f"dti {county.dti_rank_2013.notna().sum()}")

    # ---- aggregate to banks ----------------------------------------------
    sod = pd.read_csv(RAW / "fdic_sod_2014.csv").dropna(subset=["STCNTYBR"])
    sod["fips"] = (sod["STCNTYBR"].astype(float).astype(int)
                   .astype(str).str.zfill(5))
    sod["DEPSUMBR"] = pd.to_numeric(sod["DEPSUMBR"], errors="coerce").fillna(0)
    sod = sod[sod["DEPSUMBR"] >= 0]

    def dw(col):
        s = sod.copy()
        s["v"] = s["fips"].map(county[col])
        s = s.dropna(subset=["v"])
        return s.groupby("CERT").apply(
            lambda d: np.average(d["v"], weights=d["DEPSUMBR"])
            if d["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)

    bank = pd.DataFrame({c: dw(c) for c in [
        "wage_shock", "z_bartik", "pi_per_cap_2013", "unemp_2013",
        "hpi_growth_11_13", "dti_rank_2013", "expo_imputed",
        "expo_disclosed_only", "expo_zero"]})
    bank["n_counties"] = sod.groupby("CERT")["fips"].nunique()
    sod["in_ho"] = sod["fips"].str[:2].isin(HELD_OUT_STATES)
    bank["dep_share_heldout"] = sod.groupby("CERT").apply(
        lambda d: np.average(d["in_ho"].astype(float), weights=d["DEPSUMBR"])
        if d["DEPSUMBR"].sum() > 0 else np.nan, include_groups=False)

    # ---- merge constructs and balance sheet ------------------------------
    deb = pd.read_csv(RAW / "preshock_debtor_panel_2014.csv")
    base = pd.read_csv(RAW / "preshock_panel_2014.csv")
    den = pd.read_csv(RAW / "outcome_denominators_2014.csv")
    fin = pd.read_csv(RAW / "fdic_financials_20140630.csv")
    num = [c for c in fin.columns
           if c not in ("NAMEFULL", "STNAME", "ID", "REPDTE")]
    fin[num] = fin[num].apply(pd.to_numeric, errors="coerce")

    f = deb.merge(base[["CERT", "lb_bank", "tier1_lev", "cre_conc",
                        "log_assets", "dep_assets", "brokered",
                        "loans_assets", "geo_wage_share"]],
                  on="CERT", how="left", suffixes=("", "_dup"))
    f = f.merge(den[["CERT", "hh_loans", "bus_loans", "bus_loans_incl_constr",
                     "hh_frac", "bus_frac", "energy_adjacent_ci"]],
                on="CERT", how="left")
    f = f.merge(fin[["CERT", "ASSET", "LNLSGR", "LNCI", "LNRERES", "LNCRCD",
                     "LNAUTO", "LNCONOTH", "LNRENRES", "LNREMULT",
                     "LNRECONS"]], on="CERT", how="left")
    f = f.merge(bank, left_on="CERT", right_index=True, how="left")
    f["gap"] = f["lb_debtor"] - f["lb_rival"]

    # ---- pre-registered exclusions (section 2) ---------------------------
    n0 = len(f)
    excl = {}
    f["ex_small"] = f["ASSET"] < MIN_ASSETS
    f["ex_monoline"] = (f["sh_consumer"] > 0.90) | (f["sh_ci"] > 0.90)
    f["ex_nocounty"] = f["wage_shock"].isna()
    f["ex_footprint"] = f["n_counties"] > MAX_COUNTIES
    for k in ["ex_small", "ex_monoline", "ex_nocounty", "ex_footprint"]:
        excl[k] = int(f[k].sum())
    f["excluded"] = f[["ex_small", "ex_monoline", "ex_nocounty",
                       "ex_footprint"]].any(axis=1)

    f["qual_hh"] = ((f["hh_loans"] >= MIN_CELL_DENOM_ABS)
                    & (f["hh_frac"] >= MIN_CELL_DENOM_FRAC))
    f["qual_bus"] = ((f["bus_loans"] >= MIN_CELL_DENOM_ABS)
                     & (f["bus_frac"] >= MIN_CELL_DENOM_FRAC))
    f["held_out"] = f["dep_share_heldout"] > 0.50

    f.to_csv(RAW / "analysis_frame_preshock.csv", index=False)

    summary = {
        "n_start": n0,
        "exclusions": excl,
        "n_after_exclusions": int((~f["excluded"]).sum()),
        "n_primary_sample": int((~f["excluded"] & f["qual_hh"]).sum()),
        "n_business_sample": int((~f["excluded"] & f["qual_bus"]).sum()),
        "n_primary_heldout": int((~f["excluded"] & f["qual_hh"]
                                  & f["held_out"]).sum()),
        "n_primary_training": int((~f["excluded"] & f["qual_hh"]
                                   & ~f["held_out"]).sum()),
        "rotemberg_top10": dict(list(rot.items())[:10]),
        "instrument_coverage_counties": int(z.notna().sum()),
    }
    (OUT / "preshock_assembly_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    print("\nSAMPLE")
    print(json.dumps(summary, indent=2)[:1400])


if __name__ == "__main__":
    main()
