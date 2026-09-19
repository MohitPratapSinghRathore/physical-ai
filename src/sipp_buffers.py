"""Item 4: non-mortgage credit and liquid buffers by pathway. SIPP 2025.

This is the test the household story has been pointing at since Step 0. The mortgage channel
is modest (A29: 21.3 percent of national mortgage debt service on the headline definition),
and the manipulation pathway in particular sits in lower-income renting households where
mortgage credit is not. If Physical AI exposure concentrates anywhere in household credit,
it should be in unsecured and vehicle debt and in thin liquid buffers.

Source: SIPP 2025 person file, pipe-delimited. Household-level aggregates (TH*) are used for
debt and assets, taken at MONTHCODE 12 because the asset and debt items are measured as of
December of the reference year. Weights are WPFINWGT.

Variables:
    TJB1_OCC     occupation code for job 1
    THDEBT_CC    credit card and store bills      THDEBT_ED   educational debt
    THDEBT_VEH   vehicle debt                     THDEBT_OT   other debt
    THDEBT_MD    medical debt                     THDEBT_USEC all unsecured debt
    THDEBT_HOME  debt against primary residence   THDEBT_AST  all debt
    THVAL_BANK   assets held at financial institutions (the liquid buffer)
    THNETWORTH   household net worth
    TRENTMORT    household rent or mortgage paid in December
    EAWBMORT     was unable to pay rent or mortgage (hardship indicator)
    TPTOTINC     personal monthly earnings and income

Buffer is reported two ways because there is no single right denominator: liquid assets
against one month of household income, and against one month of the housing payment.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"

COLS = ["SSUID", "ERESIDENCEID", "PNUM", "MONTHCODE", "WPFINWGT", "TJB1_OCC",
        "TPTOTINC", "THDEBT_CC", "THDEBT_ED", "THDEBT_VEH", "THDEBT_OT", "THDEBT_MD",
        "THDEBT_USEC", "THDEBT_HOME", "THDEBT_AST", "THVAL_BANK", "THNETWORTH",
        "TRENTMORT", "EAWBMORT"]
PATHS = ["driving", "gated", "manipulation"]


def wq(v, w, q):
    m = np.isfinite(v) & np.isfinite(w) & (w > 0)
    v, w = np.asarray(v)[m], np.asarray(w)[m]
    if not len(v):
        return np.nan
    o = np.argsort(v)
    return float(np.interp(q, np.cumsum(w[o]) / w[o].sum(), v[o]))


def main():
    fl = pd.read_csv(OUT / "pathway_assignment.csv")
    fl = fl[fl["employment"].notna() & (fl["employment"] > 0)]
    pmap = dict(zip(fl["occp"], fl["pathway"]))

    z = zipfile.ZipFile(RAW / "sipp" / "pu2025_csv.zip")
    parts = []
    with z.open("pu2025.csv") as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              sep="|", usecols=COLS, chunksize=200_000,
                              low_memory=False):
            parts.append(ch[ch["MONTHCODE"] == 12])
    D = pd.concat(parts, ignore_index=True)
    print(f"SIPP December person records: {len(D):,}")

    D["occ"] = pd.to_numeric(D["TJB1_OCC"], errors="coerce")
    D["path"] = D["occ"].map(pmap)
    matched = D["path"].notna()
    print(f"occupation codes matching the pathway spine: {100*matched.mean():.1f}% of "
          f"person-months with an occupation "
          f"({100*matched.sum()/D['occ'].notna().sum():.1f}% of those with any occupation)")

    # household-level frame: one row per household, plus which pathways it contains
    D["hh"] = D["SSUID"].astype(str) + "_" + D["ERESIDENCEID"].astype(str)
    hh = D.groupby("hh").agg(
        wgt=("WPFINWGT", "max"),
        inc_m=("TPTOTINC", "sum"),
        cc=("THDEBT_CC", "max"), ed=("THDEBT_ED", "max"), veh=("THDEBT_VEH", "max"),
        ot=("THDEBT_OT", "max"), md=("THDEBT_MD", "max"), usec=("THDEBT_USEC", "max"),
        home=("THDEBT_HOME", "max"), allb=("THDEBT_AST", "max"),
        bank=("THVAL_BANK", "max"), nw=("THNETWORTH", "max"),
        rentmort=("TRENTMORT", "max"), awb=("EAWBMORT", "max")).reset_index()
    for p in PATHS:
        m = D[D["path"] == p].groupby("hh").size().rename(p)
        hh = hh.join(m, on="hh")
        hh[p] = hh[p].fillna(0) > 0
    hh["any_embodied"] = hh[PATHS].any(axis=1)

    for c in ["inc_m", "cc", "ed", "veh", "ot", "md", "usec", "home", "allb", "bank",
              "nw", "rentmort"]:
        hh[c] = pd.to_numeric(hh[c], errors="coerce").fillna(0.0)
    hh["inc_a"] = hh["inc_m"] * 12.0
    hh = hh[hh["wgt"] > 0]
    print(f"households: {len(hh):,} unweighted, {hh['wgt'].sum():,.0f} weighted")

    groups = {"driving": hh["driving"], "gated": hh["gated"],
              "manipulation": hh["manipulation"],
              "all_embodied": hh["any_embodied"],
              "no_embodied_worker": ~hh["any_embodied"]}

    rows = []
    for g, m in groups.items():
        d = hh[m]
        w = d["wgt"].to_numpy(float)
        tot_inc = float((d["inc_a"] * w).sum())
        r = {"group": g, "households_weighted": float(w.sum()),
             "median_annual_income_usd": wq(d["inc_a"], w, 0.5)}
        for lab, col in [("credit_card", "cc"), ("student", "ed"), ("vehicle", "veh"),
                         ("other", "ot"), ("medical", "md"), ("unsecured_total", "usec"),
                         ("nonmortgage_total", None), ("mortgage", "home")]:
            if col is None:
                v = d["usec"] + d["veh"]
            else:
                v = d[col]
            r[f"{lab}_dti_pct"] = 100 * float((v * w).sum()) / tot_inc if tot_inc else np.nan
            r[f"{lab}_median_usd"] = wq(v, w, 0.5)
            r[f"{lab}_pct_holding"] = 100 * float(w[(v > 0).to_numpy()].sum()) / float(w.sum())
        # liquid buffers
        inc_mo = d["inc_m"].replace(0, np.nan)
        r["pct_liquid_under_1mo_income"] = 100 * float(
            w[(d["bank"] < inc_mo).fillna(True).to_numpy()].sum()) / float(w.sum())
        hp = d["rentmort"].replace(0, np.nan)
        ok = hp.notna().to_numpy()
        r["pct_liquid_under_1mo_housing"] = (
            100 * float(w[ok & (d["bank"] < hp).fillna(False).to_numpy()].sum())
            / float(w[ok].sum()) if ok.sum() else np.nan)
        r["median_liquid_usd"] = wq(d["bank"], w, 0.5)
        r["median_net_worth_usd"] = wq(d["nw"], w, 0.5)
        awb = pd.to_numeric(d["awb"], errors="coerce")
        okw = awb.isin([1, 2]).to_numpy()
        r["pct_unable_to_pay_rent_or_mortgage"] = (
            100 * float(w[okw & (awb == 1).to_numpy()].sum()) / float(w[okw].sum())
            if okw.sum() else np.nan)
        rows.append(r)
    T = pd.DataFrame(rows)
    T.round(3).to_csv(OUT / "sipp_buffers.csv", index=False)
    (OUT / "sipp_buffers_summary.json").write_text(
        json.dumps(T.round(4).to_dict("records"), indent=2))

    pd.set_option("display.width", 250)
    print("\n=== Debt to income by type (percent of annual household income) ===")
    print(T[["group", "credit_card_dti_pct", "student_dti_pct", "vehicle_dti_pct",
             "medical_dti_pct", "unsecured_total_dti_pct", "nonmortgage_total_dti_pct",
             "mortgage_dti_pct"]].round(1).to_string(index=False))
    print("\n=== Liquid buffers and hardship ===")
    print(T[["group", "median_annual_income_usd", "median_liquid_usd",
             "median_net_worth_usd", "pct_liquid_under_1mo_income",
             "pct_liquid_under_1mo_housing",
             "pct_unable_to_pay_rent_or_mortgage"]].round(1).to_string(index=False))
    print("\n=== Vehicle debt (the driving pathway question) ===")
    print(T[["group", "vehicle_dti_pct", "vehicle_median_usd",
             "vehicle_pct_holding"]].round(1).to_string(index=False))


if __name__ == "__main__":
    main()
