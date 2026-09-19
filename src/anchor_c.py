"""A3: anchor c empirically, and convergently validate S.

Logic. Current robots deploy where environments are structured. So among occupations that
require a body (high P), observed robot adoption should be CONCENTRATED at high S and
ABSENT at high structure deficit. If it is not, S is not measuring what we claim and the
index fails.

Sign convention, stated explicitly because it is easy to invert:
    S_rank       percentile rank of structure. HIGH = structured.  Adoption should RISE.
    deficit_rank 1 - S_rank, i.e. unstructuredness. Adoption should FALL.
c lives on the DEFICIT scale (an occupation is exposed when deficit <= c), so c_today is
located on deficit_rank: the deficit percentile above which observed adoption is
effectively absent.

Construction.
  1. ACES 2022 robotic equipment capital expenditure by NAICS sector (Census experimental
     data product, Table 1a).
  2. Census 2017 industry code list to map PUMS INDP to NAICS.
  3. PUMS OCCP x INDP employment matrix.
  4. Sector robot intensity = robotic capex per worker in that sector.
  5. Occupation robot exposure = sum over industries of (share of that occupation's
     employment in industry i) x intensity_i.

This is a CONVERGENT test, not a direct one: adoption is observed at industry level while S
is occupational, so the variation identifying the test is the industry mix of each
occupation. Occupations concentrated in the same industry receive similar intensity, which
limits power. Reported as a limitation, per owner instruction.
"""
import io, json, pathlib, re, zipfile
import numpy as np
import pandas as pd
from scipy import stats

ROOT = pathlib.Path(__file__).parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "data" / "processed"
FIG = ROOT / "paper" / "figures"
FIG.mkdir(parents=True, exist_ok=True)


def aces_sectors():
    """NAICS sector -> robotic equipment capex, USD millions, 2022."""
    d = pd.read_excel(RAW / "robots" / "aces2022_table1a.xlsx", "Table 1a", header=None)
    hdr = d.index[d[0].astype(str).str.strip() == "NAICS code"]
    body = d.loc[hdr[0] + 1:, [0, 1, 2]].copy()
    body.columns = ["naics", "sector", "capex_musd"]
    body = body[body["naics"].notna() & body["sector"].notna()]
    body["sector"] = body["sector"].astype(str).str.strip()
    body = body[body["sector"].str.lower() != "total"]
    body["capex_musd"] = pd.to_numeric(body["capex_musd"], errors="coerce")
    body = body.dropna(subset=["capex_musd"])
    body["naics"] = body["naics"].astype(str).str.strip()
    return body.reset_index(drop=True)


def naics2_set(code):
    """Expand an ACES NAICS label ('31-33', '44-45', '113-115') to 2-digit prefixes."""
    code = str(code).strip()
    out = set()
    for part in code.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")[:2]
            a, b = a.strip(), b.strip()
            if len(a) <= 2 and len(b) <= 2 and a.isdigit() and b.isdigit():
                out.update(str(x) for x in range(int(a), int(b) + 1))
            elif a.isdigit():
                out.add(a[:2])
        elif part.isdigit():
            out.add(part[:2])
    return out


def indp_to_naics2():
    """PUMS INDP code -> 2-digit NAICS, from the Census 2017 industry code list."""
    d = pd.read_excel(RAW / "crosswalk" / "census2017_ind_naics.xlsx",
                      "2017 Census Industry Code List", header=None)
    rows = []
    for _, r in d.iterrows():
        code, naics = r[3], r[4]
        if pd.isna(code) or pd.isna(naics):
            continue
        code = str(code).strip()
        if not re.fullmatch(r"\d{3,4}", code):
            continue
        n2 = str(naics).strip()[:2]
        if n2.isdigit():
            rows.append({"indp": int(code), "naics2": n2})
    return pd.DataFrame(rows).drop_duplicates("indp")


def pums_occ_ind():
    frames = []
    z = zipfile.ZipFile(RAW / "pums" / "csv_pus.zip")
    for fn in ["psam_pusa.csv", "psam_pusb.csv"]:
        with z.open(fn) as fh:
            for ch in pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8", errors="replace"),
                                  usecols=["OCCP", "INDP", "PWGTP"],
                                  chunksize=500_000, low_memory=False):
                frames.append(ch)
    P = pd.concat(frames, ignore_index=True)
    for c in ["OCCP", "INDP", "PWGTP"]:
        P[c] = pd.to_numeric(P[c], errors="coerce")
    P = P.dropna(subset=["OCCP", "INDP", "PWGTP"])
    P["occp"] = P["OCCP"].astype(int)
    P["indp"] = P["INDP"].astype(int)
    return P.groupby(["occp", "indp"])["PWGTP"].sum().rename("emp").reset_index()


def main():
    aces = aces_sectors()
    cw = indp_to_naics2()
    oi = pums_occ_ind()
    oi = oi.merge(cw, on="indp", how="left")
    matched = oi["naics2"].notna()
    print(f"OCCPxINDP cells: {len(oi):,}; INDP mapped to NAICS2: {100*matched.mean():.1f}% "
          f"({100*oi.loc[matched,'emp'].sum()/oi['emp'].sum():.1f}% of employment)")

    # sector employment and robot intensity
    sec_emp = oi[matched].groupby("naics2")["emp"].sum().rename("sector_emp").reset_index()
    rows = []
    for _, r in aces.iterrows():
        s = naics2_set(r["naics"])
        e = sec_emp[sec_emp["naics2"].isin(s)]["sector_emp"].sum()
        if e > 0:
            rows.append({"naics_label": r["naics"], "sector": r["sector"],
                         "capex_musd": r["capex_musd"], "sector_emp": e,
                         "naics2_set": sorted(s),
                         "robot_usd_per_worker": r["capex_musd"] * 1e6 / e})
    SEC = pd.DataFrame(rows)
    SEC.round(3).to_csv(OUT / "robot_intensity_by_sector.csv", index=False)

    n2i = {}
    for _, r in SEC.iterrows():
        for n in r["naics2_set"]:
            n2i[n] = max(n2i.get(n, 0.0), r["robot_usd_per_worker"])
    oi["intensity"] = oi["naics2"].map(n2i)

    # occupation robot exposure = employment-share-weighted sector intensity
    oi2 = oi[oi["intensity"].notna()].copy()
    occ = (oi2.groupby("occp")
           .apply(lambda d: pd.Series({
               "robot_exposure": float(np.average(d["intensity"], weights=d["emp"])),
               "emp_in_matched_ind": float(d["emp"].sum())}), include_groups=False)
           .reset_index())

    spine = pd.read_csv(OUT / "occp_to_paei.csv")
    grid = pd.read_csv(OUT / "paei_c.csv")
    sr = grid[grid["c"] == 0.0][["occp", "structure_S_rank", "structure_deficit_rank",
                                 "employment", "embodiment_P", "structure_S"]].copy()
    M = sr.merge(occ, on="occp", how="inner")
    M = M[M["employment"].notna() & (M["employment"] > 0)]
    M = M.merge(spine[["occp", "title"]], on="occp", how="left")

    P_MED = float(M["embodiment_P"].median())
    hi = M[M["embodiment_P"] >= P_MED].copy()
    lo = M[M["embodiment_P"] < P_MED].copy()
    print(f"\noccupations with robot exposure and employment: {len(M)}; "
          f"high-P (>= {P_MED:.3f}): {len(hi)}")

    def tests(d, label):
        w = d["employment"].to_numpy(float)
        x = d["structure_S_rank"].to_numpy(float)
        y = d["robot_exposure"].to_numpy(float)
        dfc = d["structure_deficit_rank"].to_numpy(float)
        res = {
            "n": int(len(d)),
            "spearman_S_rank": float(stats.spearmanr(x, y)[0]),
            "spearman_S_rank_p": float(stats.spearmanr(x, y)[1]),
            "pearson_S_rank": float(stats.pearsonr(x, y)[0]),
            "spearman_deficit": float(stats.spearmanr(dfc, y)[0]),
            "spearman_deficit_p": float(stats.spearmanr(dfc, y)[1]),
        }
        mx, my = np.average(x, weights=w), np.average(y, weights=w)
        cov = np.average((x - mx) * (y - my), weights=w)
        res["pearson_S_rank_empwt"] = float(
            cov / np.sqrt(np.average((x - mx) ** 2, weights=w)
                          * np.average((y - my) ** 2, weights=w)))
        print(f"\n-- {label} (n={res['n']}) --")
        print(f"   Spearman(robot exposure, S_rank)   = {res['spearman_S_rank']:+.3f} "
              f"(p={res['spearman_S_rank_p']:.2e})   [expect POSITIVE if S is valid]")
        print(f"   Spearman(robot exposure, deficit)  = {res['spearman_deficit']:+.3f} "
              f"(p={res['spearman_deficit_p']:.2e})   [expect NEGATIVE if S is valid]")
        print(f"   Pearson employment-weighted, S_rank = {res['pearson_S_rank_empwt']:+.3f}")
        return res

    r_hi = tests(hi, "HIGH-P occupations (the gate test)")
    r_lo = tests(lo, "low-P occupations (context)")
    r_all = tests(M, "all occupations")

    # ---- locate c_today on the deficit scale ----
    hi = hi.sort_values("structure_deficit_rank")
    dec = pd.cut(hi["structure_deficit_rank"], np.arange(0, 1.0001, 0.1),
                 include_lowest=True)
    prof = (hi.groupby(dec, observed=True)
            .apply(lambda d: pd.Series({
                "n": len(d),
                "employment": d["employment"].sum(),
                "mean_robot_usd_per_worker": float(
                    np.average(d["robot_exposure"], weights=d["employment"]))}),
                   include_groups=False).reset_index())
    prof["deficit_bin"] = prof["structure_deficit_rank"].astype(str)
    peak = prof["mean_robot_usd_per_worker"].max()
    prof["pct_of_peak"] = 100 * prof["mean_robot_usd_per_worker"] / peak

    below = prof[prof["pct_of_peak"] < 20.0]
    c_today = float(below["structure_deficit_rank"].iloc[0].left) if len(below) else np.nan

    # employment-weighted cumulative share of robot spend by deficit
    hi["rob_dollars"] = hi["robot_exposure"] * hi["employment"]
    hi["cum_share"] = hi["rob_dollars"].cumsum() / hi["rob_dollars"].sum()
    c_p90 = float(np.interp(0.90, hi["cum_share"], hi["structure_deficit_rank"]))
    c_p95 = float(np.interp(0.95, hi["cum_share"], hi["structure_deficit_rank"]))

    gate_pass = (r_hi["spearman_S_rank"] > 0) and (r_hi["spearman_S_rank_p"] < 0.05)

    res = {
        "gate": "PASS" if gate_pass else "FAIL",
        "gate_criterion": ("among high-P occupations, observed robot adoption must rise in "
                           "S_rank (equivalently fall in structure deficit), significantly"),
        "P_median_gate": P_MED,
        "high_P": r_hi, "low_P": r_lo, "all": r_all,
        "c_today_deficit_scale": {
            "first_decile_below_20pct_of_peak": c_today,
            "deficit_at_90pct_of_cumulative_robot_spend": c_p90,
            "deficit_at_95pct_of_cumulative_robot_spend": c_p95,
        },
        "aces_year": 2022,
        "aces_total_robotic_capex_musd": float(aces["capex_musd"].sum()),
        "limitation": ("convergent not direct: adoption observed at NAICS sector level, S "
                       "is occupational; identifying variation is each occupation's "
                       "industry mix"),
    }
    (OUT / "anchor_c_summary.json").write_text(json.dumps(res, indent=2, default=str))
    prof.round(3).to_csv(OUT / "robot_adoption_by_deficit_decile.csv", index=False)

    pd.set_option("display.width", 200)
    print("\n=== Robot adoption profile across structure deficit (high-P occupations) ===")
    print(prof[["deficit_bin", "n", "employment", "mean_robot_usd_per_worker",
                "pct_of_peak"]].round(2).to_string(index=False))
    print(f"\n  c_today candidates (deficit scale):")
    print(f"    first decile below 20% of peak intensity: {c_today}")
    print(f"    deficit at 90% of cumulative robot spend: {c_p90:.3f}")
    print(f"    deficit at 95% of cumulative robot spend: {c_p95:.3f}")
    print(f"\n=== GATE: {res['gate']} ===")

    print("\ntop sectors by robot intensity (USD per worker):")
    print(SEC.sort_values("robot_usd_per_worker", ascending=False)
          .head(8)[["sector", "capex_musd", "sector_emp", "robot_usd_per_worker"]]
          .round(2).to_string(index=False, max_colwidth=44))


if __name__ == "__main__":
    main()
