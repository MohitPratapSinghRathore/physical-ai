"""DAR v2: Step 0 rebuild of the household exposure measures.

Four corrections to the Phase 1 build, each from MASTER_PROMPT_PHASE2.md Step 0:

1. HOUSEHOLD PAEI is the earnings-weighted mean of PAEI across all earners in the
   household, not the reference person's occupation and not a share-attribution of debt
   service. All three are computed so the movement can be reported.

2. MORTGAGE PAYMENT is decontaminated. PUMS MRGP is the first mortgage payment and may
   include real estate taxes (MRGT == 1) and/or fire, hazard and flood insurance
   (MRGI == 1). The clean principal-and-interest subsample is MRGT == 2 and MRGI == 2.
   Both the clean subsample and the full sample are reported.

3. RENTERS are added. Gross rent (GRNTP) is a wage-backed housing obligation in exactly
   the sense the thesis cares about, and renters are where low-wage, high-PAEI workers
   concentrate. Owner, renter and combined results are reported separately, along with
   tenure shares by PAEI quintile.

4. ADJHSG is applied to housing dollar amounts, as the PUMS dictionary instructs.
   For 2023 ADJHSG is exactly 1.000000, so this changes nothing numerically in this
   vintage, but the Phase 1 code would have been wrong on any multi-year build.

Nothing here is a claim about default. It is a claim about which wage income carries which
housing obligations.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
PCOLS = ["SERIALNO", "SPORDER", "OCCP", "PWGTP", "WAGP", "ADJINC"]
HCOLS = ["SERIALNO", "WGTP", "TEN", "MRGP", "MRGT", "MRGI", "GRNTP", "SMOCP",
         "TAXAMT", "INSP", "ADJHSG", "VALP", "HINCP", "NP", "PUMA", "STATE"]


def read_part(zf, fn, cols):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    with z.open(fn) as fh:
        return pd.concat(list(pd.read_csv(
            io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
            usecols=cols, dtype={"SERIALNO": str}, chunksize=400_000, low_memory=False)),
            ignore_index=True)


def wq(values, weights, qs):
    """Weighted quantiles."""
    o = np.argsort(values)
    v, w = np.asarray(values)[o], np.asarray(weights)[o]
    c = np.cumsum(w) / w.sum()
    return np.interp(qs, c, v)


def main():
    occ = pd.read_csv(OUT / "occp_to_paei.csv")

    # ---------------- person side ----------------
    P = pd.concat([read_part(z, f, PCOLS) for z, f in PPART], ignore_index=True)
    P["OCCP"] = pd.to_numeric(P["OCCP"], errors="coerce")
    P["WAGP"] = pd.to_numeric(P["WAGP"], errors="coerce").fillna(0.0)
    P["wage"] = P["WAGP"] * pd.to_numeric(P["ADJINC"], errors="coerce") / 1e6
    P = P.merge(occ[["occp", "PAEI"]], left_on="OCCP", right_on="occp", how="left")

    earn = P[(P["wage"] > 0) & P["PAEI"].notna()].copy()

    # (a) earnings-weighted household PAEI  <- primary measure
    earn["num"] = earn["PAEI"] * earn["wage"]
    g = earn.groupby("SERIALNO").agg(num=("num", "sum"), den=("wage", "sum"))
    hh = pd.DataFrame({"paei_ew": g["num"] / g["den"], "hh_wage": g["den"]})

    # (b) reference-person PAEI  <- Phase 1 style, for comparison
    ref = (P[(P["SPORDER"] == 1)].set_index("SERIALNO")["PAEI"].rename("paei_ref"))
    hh = hh.join(ref, how="left")

    # (c) highest-earner PAEI <- a third variant, reported for robustness
    top = (earn.sort_values("wage").groupby("SERIALNO")["PAEI"].last().rename("paei_top"))
    hh = hh.join(top, how="left")

    # ---------------- household side ----------------
    H = pd.concat([read_part(z, f, HCOLS) for z, f in HPART], ignore_index=True)
    for c in ["WGTP", "TEN", "MRGP", "GRNTP", "SMOCP", "TAXAMT", "INSP", "ADJHSG",
              "VALP", "HINCP", "NP"]:
        H[c] = pd.to_numeric(H[c], errors="coerce")
    for c in ["MRGT", "MRGI"]:
        H[c] = pd.to_numeric(H[c], errors="coerce")
    H["adjhsg"] = H["ADJHSG"] / 1e6
    H = H.merge(hh, left_on="SERIALNO", right_index=True, how="left")

    H["mortgage_annual"] = np.where(H["TEN"] == 1, H["MRGP"] * 12.0 * H["adjhsg"], np.nan)
    H["rent_annual"] = np.where(H["TEN"] == 3, H["GRNTP"] * 12.0 * H["adjhsg"], np.nan)
    # clean principal-and-interest: taxes AND insurance both paid separately
    H["pi_clean"] = (H["MRGT"] == 2) & (H["MRGI"] == 2)

    # ---------------- quintiles on the primary measure ----------------
    base = H[H["paei_ew"].notna() & (H["hh_wage"] > 0)]
    cuts = wq(base["paei_ew"].to_numpy(), base["WGTP"].to_numpy(), [.2, .4, .6, .8])
    for col, name in [("paei_ew", "q_ew"), ("paei_ref", "q_ref"), ("paei_top", "q_top")]:
        H[name] = np.where(H[col].notna(), np.digitize(H[col].to_numpy(), cuts) + 1, np.nan)

    # how much do results move between definitions?
    cmp_ = H[H["q_ew"].notna() & H["q_ref"].notna()]
    move_ref = float((cmp_["q_ew"] != cmp_["q_ref"]).mean() * 100)
    corr_ref = float(H["paei_ew"].corr(H["paei_ref"]))
    cmp2 = H[H["q_ew"].notna() & H["q_top"].notna()]
    move_top = float((cmp2["q_ew"] != cmp2["q_top"]).mean() * 100)
    corr_top = float(H["paei_ew"].corr(H["paei_top"]))

    # ---------------- tenure shares by quintile ----------------
    ten = H[H["q_ew"].notna()].copy()
    ten["grp"] = np.select(
        [ten["TEN"] == 1, ten["TEN"] == 2, ten["TEN"] == 3],
        ["owner_mortgage", "owner_outright", "renter"], default="other")
    tt = (ten.pivot_table(index="q_ew", columns="grp", values="WGTP", aggfunc="sum")
            .fillna(0.0))
    tenure = tt.div(tt.sum(axis=1), axis=0) * 100
    tenure.to_csv(OUT / "tenure_by_paei_quintile.csv")

    # ---------------- exposure tables ----------------
    def table(df, obligation, label, wage_col="hh_wage"):
        d = df[df["q_ew"].notna() & df[obligation].notna() & (df[obligation] > 0)]
        rows = []
        tot_ob = float((d[obligation] * d["WGTP"]).sum())
        tot_wg = float((d[wage_col] * d["WGTP"]).sum())
        for q in [1, 2, 3, 4, 5]:
            s = d[d["q_ew"] == q]
            ob = float((s[obligation] * s["WGTP"]).sum())
            wg = float((s[wage_col] * s["WGTP"]).sum())
            rows.append({
                "measure": label, "paei_quintile": q,
                "households_weighted": float(s["WGTP"].sum()),
                "obligation_usd_bn": ob / 1e9,
                "share_of_obligation_pct": 100 * ob / tot_ob,
                "wage_income_usd_bn": wg / 1e9,
                "share_of_wage_income_pct": 100 * wg / tot_wg,
                "concentration_ratio": (ob / tot_ob) / (wg / tot_wg),
                "obligation_to_income_pct": 100 * ob / wg,
            })
        return pd.DataFrame(rows)

    owners_all = table(H[H["TEN"] == 1], "mortgage_annual", "owner_mortgage_all")
    owners_pi = table(H[(H["TEN"] == 1) & H["pi_clean"]], "mortgage_annual",
                      "owner_mortgage_PI_clean")
    renters = table(H[H["TEN"] == 3], "rent_annual", "renter_gross_rent")

    comb = H.copy()
    comb["housing_annual"] = comb[["mortgage_annual", "rent_annual"]].sum(axis=1, min_count=1)
    combined = table(comb, "housing_annual", "combined_housing")

    allt = pd.concat([owners_all, owners_pi, renters, combined], ignore_index=True)
    allt.round(3).to_csv(OUT / "dar_v2_us.csv", index=False)

    # contamination size
    m = H[(H["TEN"] == 1) & H["mortgage_annual"].notna()]
    share_clean = float(m.loc[m["pi_clean"], "WGTP"].sum() / m["WGTP"].sum() * 100)
    mean_all = float((m["mortgage_annual"] * m["WGTP"]).sum() / m["WGTP"].sum())
    mean_clean = float((m.loc[m["pi_clean"], "mortgage_annual"]
                        * m.loc[m["pi_clean"], "WGTP"]).sum()
                       / m.loc[m["pi_clean"], "WGTP"].sum())

    summary = {
        "pums_year": 2023,
        "household_paei_definition": "earnings-weighted mean of PAEI over earners",
        "quintile_cutpoints_hh_weighted": [float(x) for x in cuts],
        "corr_ew_vs_reference_person": corr_ref,
        "pct_households_changing_quintile_vs_reference_person": move_ref,
        "corr_ew_vs_highest_earner": corr_top,
        "pct_households_changing_quintile_vs_highest_earner": move_top,
        "mortgage_hh_weighted": float(m["WGTP"].sum()),
        "pct_mortgage_hh_with_clean_PI": share_clean,
        "mean_annual_mortgage_payment_all_usd": mean_all,
        "mean_annual_mortgage_payment_PI_clean_usd": mean_clean,
        "contamination_bias_pct": 100 * (mean_all - mean_clean) / mean_clean,
        "renter_hh_weighted": float(H.loc[H["TEN"] == 3, "WGTP"].sum()),
        "total_rent_usd_bn": float((H["rent_annual"] * H["WGTP"]).sum(skipna=True) / 1e9),
        "total_mortgage_usd_bn": float((H["mortgage_annual"] * H["WGTP"]).sum(skipna=True) / 1e9),
    }
    (OUT / "dar_v2_summary.json").write_text(json.dumps(summary, indent=2))

    pd.set_option("display.width", 220)
    print("\n=== Household PAEI definition sensitivity ===")
    print(f"  corr(earnings-weighted, reference person) = {corr_ref:.4f}")
    print(f"  households changing quintile vs reference person: {move_ref:.1f}%")
    print(f"  corr(earnings-weighted, highest earner)   = {corr_top:.4f}")
    print(f"  households changing quintile vs highest earner: {move_top:.1f}%")

    print("\n=== Mortgage payment contamination (MRGT/MRGI inclusion flags) ===")
    print(f"  mortgage households with taxes AND insurance paid separately: {share_clean:.1f}%")
    print(f"  mean annual payment, all:      ${mean_all:,.0f}")
    print(f"  mean annual payment, PI clean: ${mean_clean:,.0f}")
    print(f"  contamination bias: {summary['contamination_bias_pct']:.1f}%")

    print("\n=== Tenure share by PAEI quintile (percent of households) ===")
    print(tenure.round(1).to_string())

    print("\n=== Exposure by PAEI quintile ===")
    for lbl in allt["measure"].unique():
        s = allt[allt["measure"] == lbl]
        print(f"\n-- {lbl} --")
        print(s[["paei_quintile", "obligation_usd_bn", "share_of_obligation_pct",
                 "share_of_wage_income_pct", "concentration_ratio",
                 "obligation_to_income_pct"]].round(2).to_string(index=False))


if __name__ == "__main__":
    main()
