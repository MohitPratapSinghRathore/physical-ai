"""rho and omega sourced from the BLS Worker Displacement release, replacing stipulated values.

SOURCE, read directly from the BLS site on 2026-09-19 and recorded in data/SOURCES.md:
    "Displaced Workers Summary", USDL, Bureau of Labor Statistics.
    Survey reference period: job losses January 2023 through December 2025.
    Status measured: January 2026.
    Table 1  Long-tenured displaced workers by age, sex, race, Hispanic or Latino ethnicity,
             and employment status in January 2026.
    Table 7  Long-tenured displaced workers who lost full-time wage and salary jobs and were
             reemployed in January 2026 by industry of lost job and characteristics of new
             job.

RHO, taken directly, no assumption:
    Table 1 total row. 3,324 thousand long-tenured displaced workers; 2,199 thousand employed
    in January 2026. rho = 2199 / 3324 = 0.6615.

OMEGA, NOT taken directly, because Table 7 reports a BANDED distribution and not a mean.
Table 7 total row, workers who lost full-time wage and salary jobs and were reemployed in
full-time wage and salary jobs AND reported earnings on the lost job (1,342 thousand):

    20 percent or more below        369
    below, but within 20 percent    317
    equal or above, within 20 pct   354
    20 percent or more above        302

The two outer bands are open-ended, so a mean requires a midpoint assumption for them and
that assumption is stated, varied, and never hidden. Closed bands take their midpoints, 0.90
and 1.10. Three cases are reported.

A SECOND assumption is needed because the engine applies omega to EVERY reemployed worker,
while Table 7 prices only full-time to full-time moves. Of 1,942 thousand reemployed, 1,593
went to full-time wage and salary work, 197 to part-time and 152 to self-employment or
unpaid family work. Earnings are not published for the latter two. Two bounds are reported:
an UPPER bound assuming they match the full-time ratio, and a LOWER bound assigning
part-time 0.50 and self-employment 0.85 of the prior wage, both stated as assumptions.

WHY THIS REPLACES JACOBSON, LALONDE AND SULLIVAN AT 0.75. The engine's omega is the wage
ratio CONDITIONAL ON REEMPLOYMENT at a point in time. JLS measures long-run earnings losses
of mass-layoff workers including spells of non-employment, which is a different estimand and
a larger loss. The repository was using a total-loss parameter where a
conditional-on-reemployment parameter was required. That was an error of concept, not of
arithmetic, and it made omega too low and therefore the break-even reemployment share too
high.

LIMITATION, stated: the DWS universe is LONG-TENURED displaced workers, three or more years
on the lost job. Short-tenure displacement is not covered, and there is no reason to assume
AI displacement resembles the long-tenured population. This is the main external validity
caveat on both parameters.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

RELEASE = {
    "title": "Displaced Workers Summary",
    "agency": "US Bureau of Labor Statistics",
    "reference_period_job_loss": "January 2023 through December 2025",
    "status_measured": "January 2026",
    "url": "https://www.bls.gov/news.release/disp.nr0.htm",
    "tables_url": "https://www.bls.gov/news.release/disp.toc.htm",
    "retrieved": "2026-09-19",
}

# ---- Table 1, total row, thousands ----
T1 = {"total": 3324, "employed": 2199, "unemployed": 609, "not_in_labor_force": 522}

# ---- Table 7, total row, thousands ----
T7 = {"reemployed_total": 1942,
      "to_full_time_wage_salary": 1593,
      "to_part_time": 197,
      "to_self_employed_or_unpaid_family": 152,
      "earnings_bands_full_time": {
          "20_pct_or_more_below": 369,
          "below_within_20_pct": 317,
          "equal_or_above_within_20_pct": 354,
          "20_pct_or_more_above": 302}}

# midpoint assumptions for the two OPEN bands; closed bands are fixed at 0.90 and 1.10
OPEN_BAND_CASES = {
    "conservative": {"below": 0.60, "above": 1.30},
    "central": {"below": 0.65, "above": 1.35},
    "generous": {"below": 0.70, "above": 1.40},
}
NONFT_ASSUMPTION = {"part_time": 0.50, "self_employed": 0.85}

# P1r parameters, unchanged, from src/p1r_fixes.py
TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}
TAU_K = {"equipment_0.05": 0.05, "net_capital_0.10": 0.10, "statutory_upper_0.21": 0.21}


def rho():
    return T1["employed"] / T1["total"]


def omega_full_time(case):
    b = T7["earnings_bands_full_time"]
    m = OPEN_BAND_CASES[case]
    num = (b["20_pct_or_more_below"] * m["below"]
           + b["below_within_20_pct"] * 0.90
           + b["equal_or_above_within_20_pct"] * 1.10
           + b["20_pct_or_more_above"] * m["above"])
    return num / sum(b.values())


def omega_all(case, bound):
    wft = omega_full_time(case)
    if bound == "upper":
        return wft
    n = T7["reemployed_total"]
    return (T7["to_full_time_wage_salary"] * wft
            + T7["to_part_time"] * NONFT_ASSUMPTION["part_time"]
            + T7["to_self_employed_or_unpaid_family"] * NONFT_ASSUMPTION["self_employed"]) / n


def main():
    r = rho()
    rows = []
    for case in OPEN_BAND_CASES:
        for bound in ("lower", "upper"):
            rows.append({"open_band_case": case, "non_full_time_bound": bound,
                         "omega_full_time_only": omega_full_time(case),
                         "omega_all_reemployed": omega_all(case, bound)})
    W = pd.DataFrame(rows)
    lo = float(W["omega_all_reemployed"].min())
    hi = float(W["omega_all_reemployed"].max())
    central = float(W[(W.open_band_case == "central")]["omega_all_reemployed"].mean())

    # break-even rho* = (1 - tau_k/tau_l) / omega, at the OBSERVED omega range
    grid = []
    for ln, tl in TAU_L.items():
        for kn, tk in TAU_K.items():
            base = 1.0 - tk / tl
            for wl, wv in [("observed_low", lo), ("observed_central", central),
                           ("observed_high", hi), ("stipulated_JLS_0.75", 0.75)]:
                rs = base / wv
                grid.append({"tau_l": ln, "tau_k": kn, "omega_label": wl, "omega": wv,
                             "rho_star": rs, "feasible": rs <= 1.0,
                             "observed_rho": r, "met": r >= rs})
    G = pd.DataFrame(grid)
    W.round(5).to_csv(OUT / "bls_dws_omega.csv", index=False)
    G.round(5).to_csv(OUT / "bls_dws_rho_star_grid.csv", index=False)
    (OUT / "bls_dws_summary.json").write_text(json.dumps({
        "release": RELEASE, "table_1_total_row_thousands": T1,
        "table_7_total_row_thousands": T7,
        "rho_observed": r,
        "omega_range_all_reemployed": {"low": lo, "central": central, "high": hi},
        "omega_full_time_only_range": {
            "low": float(W["omega_full_time_only"].min()),
            "high": float(W["omega_full_time_only"].max())},
        "open_band_midpoint_assumptions": OPEN_BAND_CASES,
        "non_full_time_assumptions": NONFT_ASSUMPTION,
    }, indent=2))

    pd.set_option("display.width", 240)
    print("=== RHO, taken directly from Table 1, no assumption ===")
    print(f"  long-tenured displaced workers   {T1['total']:,} thousand")
    print(f"  employed in January 2026         {T1['employed']:,} thousand")
    print(f"  RHO = {r:.4f}   (unemployed {T1['unemployed']/T1['total']:.4f}, "
          f"not in labour force {T1['not_in_labor_force']/T1['total']:.4f})")
    print("\n=== OMEGA, requires stated midpoint assumptions on two open bands ===")
    print(W.round(4).to_string(index=False))
    print(f"\n  OMEGA range over all reemployed: {lo:.4f} to {hi:.4f}, central {central:.4f}")
    print(f"  against the stipulated Jacobson, LaLonde and Sullivan value of 0.75")

    print("\n=== BREAK-EVEN rho* = (1 - tau_k/tau_l)/omega, AT THE OBSERVED OMEGA ===")
    pv = G.pivot_table(index=["tau_l", "omega_label"], columns="tau_k", values="rho_star")
    print(pv.round(3).to_string())
    print(f"\n  OBSERVED rho = {r:.4f}")
    obs = G[G["omega_label"] != "stipulated_JLS_0.75"]
    print(f"  cells where the observed rho MEETS break-even: "
          f"{int(obs['met'].sum())} of {len(obs)}")
    stip = G[G["omega_label"] == "stipulated_JLS_0.75"]
    print(f"  the same count at the stipulated omega = 0.75: "
          f"{int(stip['met'].sum())} of {len(stip)}")
    print("\n  rho* range in the cells the project treats as central "
          "(tau_l bottom_up, tau_k net_capital_0.10):")
    c = G[(G.tau_k == "net_capital_0.10") & (G.tau_l != "AMR_0.255")]
    for _, x in c.iterrows():
        print(f"    tau_l {x.tau_l:18s} omega {x.omega_label:20s} "
              f"rho* {x.rho_star:.4f}  met {x.met}")


if __name__ == "__main__":
    main()
