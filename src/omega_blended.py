"""Items 1 and 2: blended omega across all reemployment destinations, and the counterfactual
adjustment.

ITEM 1. BLENDED OMEGA.

BLS Worker Displacement Table 7 prices only full-time to full-time moves. Of 1,942 thousand
long-tenured workers who lost full-time wage and salary jobs and were employed at the January
2026 survey date:

    1,593 thousand  reemployed in FULL-TIME wage and salary work   (82.03 percent)
      197 thousand  reemployed PART-TIME                            (10.14 percent)
      152 thousand  SELF-EMPLOYED or unpaid family workers          ( 7.83 percent)

    full-time      Table 7 banded earnings ratio, midpoints stated in src/bls_dws.py
    part-time      SOURCED. CPS annual averages, median usual weekly earnings of PART-TIME
                   wage and salary workers (Table 38) over FULL-TIME (Table 37), total 16
                   years and over. 2025: 386 / 1,204 = 0.3206. 2024: 380 / 1,159 = 0.3279.
                   CAVEAT, and it matters: this is a ratio of medians across two DIFFERENT
                   populations, not the ratio a displaced full-time worker obtains on moving
                   to part-time. Displaced long-tenured workers are older and more
                   experienced than the median part-time worker, so 0.32 is likely a floor.
                   An upper case of 0.50 is carried as a STATED assumption, not a source.
    self-employed  NOT SOURCED. No series in this repository prices the earnings of newly
                   self-employed displaced workers against their prior wage. Carried as a
                   stated range 0.70 to 1.00, central 0.85, and flagged everywhere.

ITEM 2. COUNTERFACTUAL ADJUSTMENT.

Table 7 compares NOMINAL earnings on the new job against NOMINAL earnings on a job lost up
to three years earlier. Three quantities differ and the fiscal condition needs a specific
one:

    omega_nominal        new nominal wage / old nominal wage. What Table 7 reports.
    omega_real           deflated by consumer prices over the elapsed period. Measures the
                         worker's purchasing power. NOT what the fiscal condition needs.
    omega_counterfactual new nominal wage / the nominal wage the worker WOULD have earned
                         had they not been displaced. Deflated by economy-wide nominal WAGE
                         growth over the elapsed period.

THE FISCAL CONDITION NEEDS omega_counterfactual. The condition tau_k*s + tau_l*rho*omega >=
tau_l compares tax raised on the post-displacement wage bill against tax that WOULD have been
raised on the same workers absent displacement. The counterfactual wage bill grows with
economy-wide wages. Using omega_nominal credits displacement with the general wage growth
that would have happened anyway, which overstates the retained tax base and therefore
understates the break-even reemployment rate.

ELAPSED TIME. The survey window is job losses January 2023 through December 2025 with status
measured January 2026. Taking displacement as uniform over the 36-month window, mean elapsed
time to the survey date is 18 months, 1.5 years. Reported across 1.0 to 2.0 years.

Wage growth: Employment Cost Index, wages and salaries, private industry (FRED ECIWAG),
which holds occupation and industry composition fixed and is therefore the right series for
a counterfactual wage path. Consumer prices: CPIAUCSL, used only for the real variant.
"""
import io, json, pathlib, urllib.request
import numpy as np
import pandas as pd
import importlib.util

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"
UA = "physical-ai-research/1.0 (team@oviguide.in)"

spec = importlib.util.spec_from_file_location("bd", ROOT / "src" / "bls_dws.py")
BD = importlib.util.module_from_spec(spec); spec.loader.exec_module(BD)

# CPS annual averages, verified 2026-09-19 against bls.gov/cps/cpsaat37.htm and cpsaat38.htm
CPS_PT_FT = {
    2025: {"part_time_median_weekly": 386, "full_time_median_weekly": 1204,
           "part_time_thousands": 25000, "full_time_thousands": 121470},
    2024: {"part_time_median_weekly": 380, "full_time_median_weekly": 1159,
           "part_time_thousands": 24307, "full_time_thousands": 120053},
}
PT_UPPER_ASSUMED = 0.50          # stated, not sourced
SELF_EMPLOYED = {"low": 0.70, "central": 0.85, "high": 1.00}   # stated, not sourced
ELAPSED_YEARS = {"low": 1.0, "central": 1.5, "high": 2.0}


def fred(series):
    p = RAW / "fred" / f"{series}.csv"
    if p.exists():
        d = pd.read_csv(p)
    else:
        u = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}"
        r = urllib.request.Request(u, headers={"User-Agent": UA})
        d = pd.read_csv(io.StringIO(urllib.request.urlopen(r, timeout=60)
                                    .read().decode("utf-8")))
        p.parent.mkdir(parents=True, exist_ok=True)
        d.to_csv(p, index=False)
    d.columns = ["date", "value"]
    d["date"] = pd.to_datetime(d["date"])
    d["value"] = pd.to_numeric(d["value"], errors="coerce")
    return d.dropna().set_index("date")["value"]


def annual_growth(s, start, end):
    """Compound annual growth rate of series s between two dates."""
    a = float(s.asof(pd.Timestamp(start)))
    b = float(s.asof(pd.Timestamp(end)))
    yrs = (pd.Timestamp(end) - pd.Timestamp(start)).days / 365.25
    return (b / a) ** (1.0 / yrs) - 1.0, a, b, yrs


def main():
    t7 = BD.T7
    n = t7["reemployed_total"]
    sh = {"full_time": t7["to_full_time_wage_salary"] / n,
          "part_time": t7["to_part_time"] / n,
          "self_employed": t7["to_self_employed_or_unpaid_family"] / n}

    pt_sourced = {y: v["part_time_median_weekly"] / v["full_time_median_weekly"]
                  for y, v in CPS_PT_FT.items()}
    pt_central = pt_sourced[2025]

    # ---- item 1: blended omega ----
    rows = []
    for band in BD.OPEN_BAND_CASES:
        wft = BD.omega_full_time(band)
        for pt_lab, pt in [("cps_sourced_0.32", pt_central),
                           ("assumed_upper_0.50", PT_UPPER_ASSUMED)]:
            for se_lab, se in SELF_EMPLOYED.items():
                w = sh["full_time"] * wft + sh["part_time"] * pt + sh["self_employed"] * se
                rows.append({"open_band_case": band, "omega_full_time": wft,
                             "part_time_case": pt_lab, "part_time_ratio": pt,
                             "self_employed_case": se_lab, "self_employed_ratio": se,
                             "omega_blended_nominal": w})
    W = pd.DataFrame(rows)
    blo, bhi = float(W.omega_blended_nominal.min()), float(W.omega_blended_nominal.max())
    bcen = float(W[(W.open_band_case == "central")
                   & (W.part_time_case == "cps_sourced_0.32")
                   & (W.self_employed_case == "central")]["omega_blended_nominal"].iloc[0])

    # ---- item 2: counterfactual and real adjustment ----
    eci = fred("ECIWAG")
    cpi = fred("CPIAUCSL")
    g_w, w0, w1, yrs_w = annual_growth(eci, "2023-01-01", "2026-01-01")
    g_p, p0, p1, yrs_p = annual_growth(cpi, "2023-01-01", "2026-01-01")

    adj = []
    for elab, e in ELAPSED_YEARS.items():
        adj.append({"elapsed_case": elab, "elapsed_years": e,
                    "omega_nominal": bcen,
                    "omega_real": bcen / (1 + g_p) ** e,
                    "omega_counterfactual": bcen / (1 + g_w) ** e})
    A = pd.DataFrame(adj)
    cf_cen = float(A[A.elapsed_case == "central"]["omega_counterfactual"].iloc[0])
    cf_lo = float(A["omega_counterfactual"].min())
    cf_hi = float(A["omega_counterfactual"].max())

    # blended range carried through the counterfactual at central elapsed
    W["omega_blended_counterfactual"] = W["omega_blended_nominal"] / (1 + g_w) ** 1.5
    cflo = float(W.omega_blended_counterfactual.min())
    cfhi = float(W.omega_blended_counterfactual.max())

    W.round(5).to_csv(OUT / "omega_blended.csv", index=False)
    A.round(5).to_csv(OUT / "omega_counterfactual.csv", index=False)
    (OUT / "omega_blended_summary.json").write_text(json.dumps({
        "reemployment_destination_shares": sh,
        "part_time_ratio_sourced": pt_sourced,
        "part_time_upper_assumed": PT_UPPER_ASSUMED,
        "self_employed_assumed": SELF_EMPLOYED,
        "omega_full_time_only": {c: BD.omega_full_time(c) for c in BD.OPEN_BAND_CASES},
        "omega_blended_nominal": {"low": blo, "central": bcen, "high": bhi},
        "eci_wages_growth_annual_2023_2026": g_w,
        "cpi_growth_annual_2023_2026": g_p,
        "omega_blended_counterfactual": {"low": cflo, "central": cf_cen, "high": cfhi},
        "elapsed_years": ELAPSED_YEARS,
    }, indent=2))

    pd.set_option("display.width", 240)
    print("=== reemployment destinations, DWS Table 7 total row ===")
    for k, v in sh.items():
        print(f"  {k:14s} {v*100:5.2f}%")
    print(f"\n=== part-time earnings ratio, CPS annual averages (SOURCED) ===")
    for y, v in sorted(pt_sourced.items(), reverse=True):
        c = CPS_PT_FT[y]
        print(f"  {y}: {c['part_time_median_weekly']} / "
              f"{c['full_time_median_weekly']} = {v:.4f}")
    print(f"\n=== ITEM 1: BLENDED OMEGA, nominal ===")
    print(W.groupby(["part_time_case", "self_employed_case"])["omega_blended_nominal"]
          .agg(["min", "max"]).round(4).to_string())
    print(f"\n  blended nominal: central {bcen:.4f}, full range {blo:.4f} to {bhi:.4f}")
    print(f"  against full-time-only omega of "
          f"{BD.omega_full_time('central'):.4f} and the old stipulated 0.75")

    print(f"\n=== ITEM 2: counterfactual adjustment ===")
    print(f"  ECI wages and salaries  {w0:.1f} -> {w1:.1f} over {yrs_w:.2f}y, "
          f"{g_w*100:.2f}% a year")
    print(f"  CPI                     {p0:.1f} -> {p1:.1f} over {yrs_p:.2f}y, "
          f"{g_p*100:.2f}% a year")
    print(A.round(4).to_string(index=False))
    print(f"\n  OMEGA THE FISCAL CONDITION NEEDS (counterfactual, blended): "
          f"central {cf_cen:.4f}, range over all cases {cflo:.4f} to {cfhi:.4f}")


if __name__ == "__main__":
    main()
