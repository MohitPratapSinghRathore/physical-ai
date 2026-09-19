"""Debt-at-Automation-Risk (DAR), United States, ACS PUMS 2023 x PAEI x O*NET 31.0.

Question. Leg W is credit underwritten against human labor income. If Physical AI displaces
labor, the relevant quantity is not aggregate exposure but exposure WHERE THE DEBT IS. This
module measures how much US mortgage debt service is paid out of wages earned in
high-Physical-AI-exposure occupations.

Construction.
  1. PAEI (data/processed/paei_onet.csv) is at O*NET-SOC (8 digit). Aggregate to 6-digit SOC.
  2. Census 2018 occupation codes (PUMS OCCP) map to SOC via the Census crosswalk.
  3. For each mortgage-holding household (TEN == 1), split household wage income by the
     PAEI of each earner's occupation.
  4. Household annual mortgage-related outlay is MRGP * 12 (first mortgage payment,
     including any escrowed taxes and insurance the respondent reports there).
  5. DAR_q = sum over households of (annual mortgage outlay) x (share of household wage
     income earned in PAEI quintile q), weighted by household weight WGTP.

Interpretation. DAR is a measure of debt service exposure, not of a debt stock. PUMS carries
no mortgage balance. The stock version requires SCF or credit-bureau microdata and is a
later extension; see notes/open_questions.md.

Income adjustment. WAGP is in the dollars of the survey year and is multiplied by ADJINC to
put it on a constant 2023 basis, per the PUMS documentation. MRGP is a current monthly
amount and is NOT adjusted by ADJINC.
"""
import io, json, pathlib, zipfile
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

PUMS_YEAR = 2023
PPART = [("csv_pus.zip", "psam_pusa.csv"), ("csv_pus.zip", "psam_pusb.csv")]
HPART = [("csv_hus.zip", "psam_husa.csv"), ("csv_hus.zip", "psam_husb.csv")]
PCOLS = ["SERIALNO", "OCCP", "PWGTP", "WAGP", "ADJINC", "AGEP", "WKHP"]
HCOLS = ["SERIALNO", "WGTP", "TEN", "MRGP", "VALP", "HINCP", "NP"]


def soc6(code):
    """O*NET-SOC 8-digit -> 6-digit SOC."""
    return str(code)[:7]


def load_paei():
    p = pd.read_csv(OUT / "paei_onet.csv")
    p["soc6"] = p["onet_soc"].map(soc6)
    # several O*NET detail occupations map to one SOC; unweighted mean is the
    # documented O*NET-to-SOC aggregation in the absence of employment weights
    g = p.groupby("soc6").agg(PAEI=("PAEI", "mean"), P=("embodiment_P", "mean"),
                              S=("structure_S", "mean"), n_onet=("PAEI", "size"))
    return g.reset_index()


def load_crosswalk():
    d = pd.read_excel(RAW / "crosswalk" / "census2018_occ_soc.xlsx",
                      "2018 Census Occ Code List", header=None)
    d = d.iloc[:, [1, 2, 3]]
    d.columns = ["title", "occp", "soc"]
    d = d.dropna(subset=["occp", "soc"])
    d["occp"] = d["occp"].astype(str).str.strip()
    # drop the major-group header rows, which carry code RANGES like "0010-3550"
    d = d[~d["occp"].str.contains("-")]
    d["occp"] = pd.to_numeric(d["occp"], errors="coerce")
    d = d.dropna(subset=["occp"])
    d["occp"] = d["occp"].astype(int)
    d["soc"] = d["soc"].astype(str).str.strip().str.split(",").str[0].str.strip()
    d = d[d["soc"].str.match(r"^\d{2}-\d{4}$")]
    return d[["occp", "soc", "title"]].drop_duplicates("occp")


def map_occp_to_paei(cw, paei):
    """Exact 6-digit SOC join; fall back to the SOC broad group (first 5 digits)."""
    m = cw.merge(paei, left_on="soc", right_on="soc6", how="left")
    paei = paei.copy()
    paei["broad"] = paei["soc6"].str[:6]
    bg = paei.groupby("broad").agg(PAEI_b=("PAEI", "mean"), P_b=("P", "mean"), S_b=("S", "mean"))
    m["broad"] = m["soc"].str[:6]
    m = m.merge(bg, on="broad", how="left")
    for c, b in [("PAEI", "PAEI_b"), ("P", "P_b"), ("S", "S_b")]:
        m[c] = m[c].fillna(m[b])
    m["matched"] = m["PAEI"].notna()
    return m[["occp", "soc", "title", "PAEI", "P", "S", "matched"]]


def read_part(zf, fn, cols, dtypes=None):
    z = zipfile.ZipFile(RAW / "pums" / zf)
    chunks = []
    with z.open(fn) as fh:
        for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                              usecols=cols, dtype=dtypes, chunksize=400_000,
                              low_memory=False):
            chunks.append(ch)
    return pd.concat(chunks, ignore_index=True)


def main():
    print("loading PAEI and crosswalk ...")
    paei = load_paei()
    cw = load_crosswalk()
    occ = map_occp_to_paei(cw, paei)
    print(f"  crosswalk rows: {len(cw)}; PAEI matched: {int(occ['matched'].sum())}"
          f" ({100*occ['matched'].mean():.1f}%)")
    occ.to_csv(OUT / "occp_to_paei.csv", index=False)

    print("loading PUMS person records ...")
    P = pd.concat([read_part(zf, fn, PCOLS, {"SERIALNO": str}) for zf, fn in PPART],
                  ignore_index=True)
    print(f"  persons: {len(P):,}")

    print("loading PUMS housing records ...")
    H = pd.concat([read_part(zf, fn, HCOLS, {"SERIALNO": str}) for zf, fn in HPART],
                  ignore_index=True)
    print(f"  households: {len(H):,}")

    # --- person side: wage income on a constant basis, attach PAEI ---
    P = P[P["OCCP"].notna()].copy()
    P["OCCP"] = pd.to_numeric(P["OCCP"], errors="coerce")
    P = P.dropna(subset=["OCCP"])
    P["OCCP"] = P["OCCP"].astype(int)
    P["WAGP"] = pd.to_numeric(P["WAGP"], errors="coerce").fillna(0.0)
    P["ADJINC"] = pd.to_numeric(P["ADJINC"], errors="coerce") / 1_000_000.0
    P["wage_adj"] = P["WAGP"] * P["ADJINC"]
    P = P.merge(occ[["occp", "PAEI", "P", "S"]], left_on="OCCP", right_on="occp", how="left")

    wage_total = float((P["wage_adj"] * P["PWGTP"]).sum())
    wage_matched = float((P["wage_adj"] * P["PWGTP"])[P["PAEI"].notna()].sum())
    print(f"  wage income covered by PAEI match: {100*wage_matched/wage_total:.1f}%")

    # --- household side: mortgage holders ---
    H["TEN"] = pd.to_numeric(H["TEN"], errors="coerce")
    H["MRGP"] = pd.to_numeric(H["MRGP"], errors="coerce")
    H["WGTP"] = pd.to_numeric(H["WGTP"], errors="coerce")
    H["VALP"] = pd.to_numeric(H["VALP"], errors="coerce")
    M = H[(H["TEN"] == 1) & H["MRGP"].notna() & (H["MRGP"] > 0)].copy()
    M["mortgage_annual"] = M["MRGP"] * 12.0
    print(f"  mortgage-holding households (unweighted): {len(M):,}"
          f"  weighted: {M['WGTP'].sum():,.0f}")

    # --- quintiles of PAEI, employment-weighted over wage earners ---
    W = P[P["PAEI"].notna() & (P["wage_adj"] > 0)].copy()
    qs = np.asarray([
        np.interp(q, np.cumsum(W.sort_values("PAEI")["PWGTP"].to_numpy()) / W["PWGTP"].sum(),
                  W.sort_values("PAEI")["PAEI"].to_numpy())
        for q in (0.2, 0.4, 0.6, 0.8)])
    print(f"  PAEI quintile cut points (employment weighted): {np.round(qs, 4).tolist()}")
    P["paei_q"] = np.digitize(P["PAEI"].to_numpy(), qs) + 1
    P.loc[P["PAEI"].isna(), "paei_q"] = np.nan

    # --- split each household's wage income across PAEI quintiles ---
    P["wt_wage"] = P["wage_adj"]
    hh_tot = P.groupby("SERIALNO")["wt_wage"].sum().rename("hh_wage")
    byq = (P.dropna(subset=["paei_q"])
             .groupby(["SERIALNO", "paei_q"])["wt_wage"].sum().unstack(fill_value=0.0))
    byq.columns = [f"q{int(c)}" for c in byq.columns]
    shares = byq.join(hh_tot, how="right").fillna(0.0)
    qcols = [c for c in shares.columns if c.startswith("q")]
    for c in qcols:
        shares[c] = np.where(shares["hh_wage"] > 0, shares[c] / shares["hh_wage"], 0.0)

    M = M.merge(shares[qcols + ["hh_wage"]], left_on="SERIALNO", right_index=True, how="left")
    M[qcols] = M[qcols].fillna(0.0)
    M["hh_wage"] = M["hh_wage"].fillna(0.0)

    # --- DAR ---
    total_ms = float((M["mortgage_annual"] * M["WGTP"]).sum())
    rows = []
    for c in sorted(qcols):
        v = float((M["mortgage_annual"] * M[c] * M["WGTP"]).sum())
        rows.append({"paei_quintile": c, "mortgage_service_usd_bn": v / 1e9,
                     "share_of_total_pct": 100 * v / total_ms})
    wage_only = sum(r["mortgage_service_usd_bn"] for r in rows)
    nonwage = total_ms / 1e9 - wage_only
    dar = pd.DataFrame(rows)
    dar.loc[len(dar)] = {"paei_quintile": "no_wage_income",
                         "mortgage_service_usd_bn": nonwage,
                         "share_of_total_pct": 100 * nonwage / (total_ms / 1e9)}

    summary = {
        "pums_year": PUMS_YEAR, "onet_version": "31.0",
        "mortgage_households_weighted": float(M["WGTP"].sum()),
        "total_mortgage_service_usd_bn": total_ms / 1e9,
        "wage_financed_share_pct": 100 * wage_only / (total_ms / 1e9),
        "paei_quintile_cutpoints": [float(x) for x in qs],
        "wage_coverage_by_paei_match_pct": 100 * wage_matched / wage_total,
        "occp_codes_matched_pct": float(100 * occ["matched"].mean()),
        "top_quintile_share_pct": float(dar.loc[dar.paei_quintile == "q5", "share_of_total_pct"].iloc[0]),
        "top_two_quintile_share_pct": float(
            dar.loc[dar.paei_quintile.isin(["q4", "q5"]), "share_of_total_pct"].sum()),
    }
    dar.round(3).to_csv(OUT / "dar_us.csv", index=False)
    (OUT / "dar_us_summary.json").write_text(json.dumps(summary, indent=2))

    print("\n=== DAR: US mortgage debt service by PAEI quintile of the wage earner ===")
    print(dar.round(2).to_string(index=False))
    print()
    for k, v in summary.items():
        print(f"  {k:38s} {v if not isinstance(v, float) else round(v, 3)}")


if __name__ == "__main__":
    main()
