"""Item 1: sourced demographic turnover and attrition rates, by exposure group.

SOURCE, and it is a better one than the brief anticipated.

BLS Employment Projections, "Occupational separations and openings", 2025 National Employment
Matrix, projections 2025 to 2035, read from bls.gov on 2026-09-19. It publishes, for every
detailed occupation, as ANNUAL AVERAGE RATES:

    Labor force exit rate            workers leaving the labour force, chiefly retirement
    Occupational transfer rate       workers moving to a different occupation
    Total occupational separations   the sum of the two

That gives all three inputs item 1 asks for from one verified source:

    (a) the demographic drain on the nonemployed stock is the LABOR FORCE EXIT RATE
    (b) the ceiling on attrition absorption alpha is the TOTAL SEPARATIONS RATE: job
        destruction can be met by not replacing separations only up to the rate at which
        separations actually occur
    (c) the occupational transfer rate bounds how fast workers move between occupations at
        all, which is the empirical counterpart of the destination-pool parameter phi

Rates are computed employment-weighted for: all occupations, the top-quintile embodied group,
and the top-quintile cognitive groups on both indices, by joining the Employment Projections
SOC codes to this project's OCCP-based exposure groups through the existing crosswalk.

WHAT THIS DOES NOT SETTLE. The separations rate is the rate at which jobs are VACATED, not
the rate at which an employer can decline to refill them without disrupting production.
Absorbing displacement through attrition also changes WHO bears it: incumbents keep their
jobs and new entrants lose the opening. Both are handled in the model, not here.
"""
import io, json, pathlib, urllib.request
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"
UA = "physical-ai-research/1.0 (team@oviguide.in)"
URL = "https://www.bls.gov/emp/tables/occupational-separations-and-openings.htm"


def fetch():
    p = RAW / "bls_ep" / "occupational_separations_2025_2035.csv"
    if p.exists():
        return pd.read_csv(p)
    h = urllib.request.urlopen(
        urllib.request.Request(URL, headers={"User-Agent": UA}), timeout=120
    ).read().decode("utf-8", "replace")
    t = pd.read_html(io.StringIO(h))[0]
    p.parent.mkdir(parents=True, exist_ok=True)
    t.to_csv(p, index=False)
    return t


def main():
    T = fetch()
    T.columns = [str(c).strip() for c in T.columns]
    ren = {}
    for c in T.columns:
        cl = c.lower()
        if "matrix code" in cl:
            ren[c] = "soc"
        elif "matrix title" in cl:
            ren[c] = "title"
        elif "occupation type" in cl:
            ren[c] = "occ_type"
        elif cl.startswith("employment, 2025"):
            ren[c] = "emp_2025"
        elif "labor force exit rate" in cl:
            ren[c] = "exit_rate"
        elif "occupational transfer rate" in cl:
            ren[c] = "transfer_rate"
        elif "total occupational separations rate" in cl:
            ren[c] = "separations_rate"
    T = T.rename(columns=ren)
    for c in ["emp_2025", "exit_rate", "transfer_rate", "separations_rate"]:
        T[c] = pd.to_numeric(T[c], errors="coerce")
    T["soc"] = T["soc"].astype(str).str.strip()

    total = T[T["soc"] == "00-0000"].iloc[0]
    print("=== BLS Employment Projections 2025 to 2035, TOTAL all occupations ===")
    print(f"  employment 2025        {total.emp_2025:,.1f} thousand")
    print(f"  labour force exit rate {total.exit_rate:.2f}% a year")
    print(f"  occupational transfer  {total.transfer_rate:.2f}% a year")
    print(f"  TOTAL separations      {total.separations_rate:.2f}% a year")

    D = T[(T["occ_type"].astype(str).str.lower() == "line item")].copy()
    D = D.dropna(subset=["emp_2025", "separations_rate"])
    print(f"\n  detailed occupations with rates: {len(D):,}")

    # join to the exposure groups through the existing OCCP to SOC crosswalk
    import sys
    sys.path.insert(0, str(ROOT))
    from src.stress import scenarios as SC
    B = SC.occupation_scores()
    _, groups = SC._h3().build_groups()
    cw = pd.read_csv(OUT / "occp_to_paei.csv")[["occp", "soc"]].drop_duplicates()
    cw["soc"] = cw["soc"].astype(str).str.strip()
    M = cw.merge(D[["soc", "exit_rate", "transfer_rate", "separations_rate"]],
                 on="soc", how="left")
    B2 = B.merge(M.groupby("occp", as_index=False)[
        ["exit_rate", "transfer_rate", "separations_rate"]].mean(), on="occp", how="left")
    cov = B2["separations_rate"].notna()
    print(f"  OCCP codes matched to a separations rate: {int(cov.sum())} of {len(B2)} "
          f"({100*B2.loc[cov,'employment'].sum()/B2['employment'].sum():.1f}% of employment)")

    def wavg(df, col):
        d = df.dropna(subset=[col])
        if d["employment"].sum() == 0:
            return np.nan
        return float(np.average(d[col], weights=d["employment"]))

    rows = []
    sets = {"all_occupations": set(B2["occp"]),
            "embodied_top_quintile": groups["embodied"],
            "cognitive_AIOE_top_quintile": groups["cognitive_AIOE"],
            "cognitive_GPT_top_quintile": groups["cognitive_GPT"]}
    for name, s in sets.items():
        d = B2[B2["occp"].isin(s)]
        rows.append({"group": name,
                     "employment": float(d["employment"].sum()),
                     "labour_force_exit_rate_pct": wavg(d, "exit_rate"),
                     "occupational_transfer_rate_pct": wavg(d, "transfer_rate"),
                     "total_separations_rate_pct": wavg(d, "separations_rate")})
    R = pd.DataFrame(rows)
    R.round(4).to_csv(OUT / "separations_by_group.csv", index=False)

    pd.set_option("display.width", 220)
    print("\n=== EMPLOYMENT-WEIGHTED ANNUAL RATES by exposure group, percent ===")
    print(R.assign(employment_m=lambda x: x.employment / 1e6).drop(columns="employment")
          .round(3).to_string(index=False))

    emb = R[R.group == "embodied_top_quintile"].iloc[0]
    cog = R[R.group == "cognitive_AIOE_top_quintile"].iloc[0]
    allo = R[R.group == "all_occupations"].iloc[0]
    print("\n=== what these bound ===")
    print(f"  (a) demographic drain on the nonemployed stock: labour force exit rate, "
          f"{allo.labour_force_exit_rate_pct:.2f}% a year economy wide, "
          f"{emb.labour_force_exit_rate_pct:.2f}% in embodied-exposed occupations")
    print(f"  (b) CEILING on attrition absorption alpha: the total separations rate, "
          f"{emb.total_separations_rate_pct:.2f}% a year in embodied-exposed occupations "
          f"and {cog.total_separations_rate_pct:.2f}% in cognitive-exposed")
    print(f"  (c) observed occupational mobility: transfer rate "
          f"{allo.occupational_transfer_rate_pct:.2f}% a year economy wide")

    (OUT / "separations_summary.json").write_text(json.dumps({
        "source": "BLS Employment Projections, Occupational separations and openings, "
                  "2025 National Employment Matrix, projections 2025 to 2035",
        "url": URL, "retrieved": "2026-09-19",
        "total_all_occupations": {"employment_thousands": float(total.emp_2025),
                                  "exit_rate_pct": float(total.exit_rate),
                                  "transfer_rate_pct": float(total.transfer_rate),
                                  "separations_rate_pct": float(total.separations_rate)},
        "by_group": R.round(4).to_dict("records"),
        "coverage_share_of_employment": float(
            B2.loc[cov, "employment"].sum() / B2["employment"].sum()),
    }, indent=2))


if __name__ == "__main__":
    main()
