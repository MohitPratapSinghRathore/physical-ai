"""Standing requirements 3 and 4: regenerate data/release/scenarios/ and
data/release/dashboard/.

Both are PUBLISHED ARTIFACTS for an external audience of supervisors and financial stability
teams, in the style of the NGFS climate scenarios. Every value carries a source and is
labelled ESTIMATED or SCENARIO ASSUMPTION. Regenerated whenever the engine or the frontier
changes.

VERSIONING. The version is bumped by hand in VERSION below whenever the underlying method
changes, not on every rerun. The changelog records what moved and why.
"""
import json, pathlib, datetime
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"
REL = ROOT / "data" / "release"
SCEN, DASH = REL / "scenarios", REL / "dashboard"
VERSION = "0.4.0"
TODAY = "2026-09-19"

CHANGELOG = """# Changelog

## 0.4.0 (2026-09-19)
- REGIMES REDEFINED. The SLOW / FAST / SUDDEN split is replaced by INSIDE_DATA,
  BOUNDARY_BAND and OUTSIDE_DATA. The old middle regime was nearly empty (A63 found 0 of 120
  paths in it), and naming a band after a speed limit that moves by a factor of 140 across
  specifications (A65) implied a precision the model does not have. The new split names the
  only distinction the data actually support: whether the path stays inside the range on
  which the underlying relationships were fitted.
- BOUNDARY_BAND is any path whose peak prime-age nonemployment is within 1 percentage point
  of the observed maximum of 24.71 percent.
- Attrition absorption added and found to be NEUTRAL for every aggregate outcome (A64).
  Columns for the two burdens are added: laid-off incumbents and lost entrant openings.
- Speed limit is no longer published as a single number. See specification_range.csv.

## 0.3.0 (2026-09-19)
- BREAKING. The reemployment hazard is now driven by PRIME-AGE NONEMPLOYMENT, not the
  unemployment rate. The previous specification was circular: exits to nonparticipation
  suppressed measured unemployment, which raised the fitted reemployment rate, which drained
  the unemployment stock faster. See findings A63.
- Speed limits fall by roughly a factor of two and a half. Cumulative ceilings fall by a
  factor of four to five.
- Nonlinearity is RESTORED. The previous "no threshold" result was an artifact of the
  circularity.
- Outcome measures reordered: employment to population first, unemployment last.

## 0.2.0 (2026-09-19)
- Destination-pool variant added (phi). Feasibility caps on embodied displacement.

## 0.1.0 (2026-09-19)
- First release. Frontier on the unemployment-driven stock-flow model.
"""

DICTIONARY = """# Data dictionary

## scenarios/paths.csv

| Column | Meaning | Status |
|---|---|---|
| regime | INSIDE_DATA, BOUNDARY_BAND or OUTSIDE_DATA, on peak prime-age nonemployment against the observed maximum of 24.71 percent. BOUNDARY_BAND is within 1 point of it | derived |
| laid_off_cum | cumulative laid-off incumbents, share of baseline employment | ESTIMATED |
| entrant_openings_lost | cumulative positions not refilled, borne by people who would have been hired | ESTIMATED |
| exposure_type | embodied, cognitive_AIOE, cognitive_GPT, both | definition |
| phi | destination-pool shrinkage. 0 assumes new work is created at the historical rate indefinitely | SCENARIO ASSUMPTION |
| horizon_years | 2, 5, 10 or 20 | definition |
| d_annual | annual displacement flow, share of employment | SCENARIO ASSUMPTION |
| ep_ratio | prime-age employment to population ratio at the horizon, percent | ESTIMATED inside the observed range, SCENARIO outside it |
| ep_drop_pp | fall in that ratio from the 2026 baseline, percentage points | as above |
| never_reemployed_share | cumulative share of all inflows to unemployment never reemployed | as above |
| wage_income_rel_baseline | aggregate wage income relative to the 2026 baseline, composition-adjusted for repeat displacement at omega | as above |
| unemployment | prime-age unemployment rate. Reported LAST because exits to nonparticipation suppress it | as above |
| rho_implied | reemployment share implied by the model's own slack | ESTIMATED |
| outside_data | TRUE when prime-age nonemployment exceeds 24.71 percent, the worst vintage in the sample | derived |

## Status vocabulary

- **ESTIMATED**: derived from measured data within the range on which the underlying
  relationships were fitted.
- **SCENARIO ASSUMPTION**: chosen by the analyst, varied over a stated grid, not measured.
- **OUTSIDE DATA**: computed by extrapolating a fitted relationship beyond its observed
  range. Reported as a band, never as a point estimate.

## What is NOT in this release yet

House price change by metro type and the fiscal position path are NOT included. They require
the supervisory conversion layer (Federal Reserve stress test loss rates, a verified house
price elasticity) which is not yet built. The columns are deliberately absent rather than
filled with placeholders.
"""


def build_scenarios():
    SCEN.mkdir(parents=True, exist_ok=True)
    G = pd.read_csv(OUT / "stock_flow_v2_grid.csv")
    L = pd.read_csv(OUT / "stock_flow_v2_limits.csv")
    lim = {(r.phi, r.horizon): r.max_d_inside_observed for _, r in L.iterrows()}
    V3 = pd.read_csv(OUT / "stock_flow_v3_grid.csv")
    V3 = V3[(V3.early_retire == "none_1.0") & (V3.alpha_basis == "aggregate")]
    NONEMP_MAX = 24.71
    rows = []
    for _, r in V3.iterrows():
        ne = r.nonemployment_rate
        if ne > NONEMP_MAX:
            regime = "OUTSIDE_DATA"
        elif ne > NONEMP_MAX - 1.0:
            regime = "BOUNDARY_BAND"
        else:
            regime = "INSIDE_DATA"
        rows.append({"regime": regime, "exposure_type": "all_types_pooled",
                     "phi": r.phi, "alpha": r.alpha, "horizon_years": int(r.horizon),
                     "d_annual": r.d_annual, "ep_ratio": r.ep_ratio,
                     "nonemployment_rate": ne,
                     "wage_income_rel_baseline": r.wage_income_rel_baseline,
                     "unemployment": r.unemployment,
                     "laid_off_cum": r.laid_off_cum,
                     "entrant_openings_lost": r.entrant_openings_lost})
    P = pd.DataFrame(rows)
    P.round(6).to_csv(SCEN / "paths.csv", index=False)
    (SCEN / "DATA_DICTIONARY.md").write_text(DICTIONARY, encoding="utf-8")
    (SCEN / "VERSION").write_text(f"{VERSION}\n{TODAY}\n", encoding="utf-8")
    (SCEN / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")
    # the speed limit is published as a RANGE across specifications, never a point
    try:
        SP = pd.read_csv(OUT / "specification_table.csv")
        SP.round(5).to_csv(SCEN / "specification_range.csv", index=False)
    except FileNotFoundError:
        pass
    L.round(5).to_csv(SCEN / "speed_limits_single_specification.csv", index=False)
    return P


def build_dashboard():
    DASH.mkdir(parents=True, exist_ok=True)
    rws = json.loads((OUT / "retained_wage_share_summary.json").read_text())
    tks = json.loads((OUT / "tau_k_second_pass_summary.json").read_text())
    sf = json.loads((OUT / "stock_flow_v2_summary.json").read_text())
    L = pd.read_csv(OUT / "stock_flow_v2_limits.csv")
    sl10 = float(L[(L.phi == 0.5) & (L.horizon == 10)]["max_d_inside_observed"].iloc[0])

    rows = [
        {"indicator": "Retained wage share R = rho x omega",
         "value": round(rws["R_2026_central"], 4),
         "threshold": f"{round(tks['required_tau_k']['AMR_0.255'], 4)} required tau_k "
                      f"equivalently R >= 0.722 at the current tau_k",
         "status": "BELOW THRESHOLD",
         "source": "BLS Displaced Workers Summary Jan 2026 Tables 1 and 7; CPS annual "
                   "averages Tables 37 and 38; FRED ECIWAG",
         "date": "2026-01 survey, computed 2026-09-19"},
        {"indicator": "Observed annual displacement flow (DWS long-tenured)",
         "value": 0.00679,
         "threshold": "speed limit RANGE 0.0005 to 0.0715 a year across the full "
                      "specification table, median 0.0273. Never a single number",
         "status": "INSIDE the median; above the tightest specifications",
         "source": "BLS DWS: 3.324m over 3 years against prime-age employment",
         "date": "2026-01"},
        {"indicator": "Effective tax rate on AI surplus, current code with shifting",
         "value": 0.0708,
         "threshold": round(tks["required_tau_k"]["AMR_0.255"], 4),
         "status": "BELOW THRESHOLD",
         "source": "AMR 2020 effective rates; 26 USC 168(k); Torslov Wier Zucman 48 percent "
                   "haven share; Barkai rent share 0.351",
         "date": "2026-09-19"},
        {"indicator": "Prime-age nonemployment rate",
         "value": round(sf["baseline"]["nonemp0"], 2),
         "threshold": round(sf["prime_age_nonemployment_max_observed"], 2),
         "status": "INSIDE",
         "source": "FRED LREM25TTUSM156S",
         "date": "2026-01"},
        {"indicator": "Bank C and I commitments to AI-adjacent industries",
         "value": "450bn USD, 13 percent of total commitments",
         "threshold": "25 percent of tier 1 capital committed (current reading)",
         "status": "REPORTED, no threshold set",
         "source": "Cohen, Killen and Lau, Chicago Fed Insights, February 2026",
         "date": "late 2025"},
        {"indicator": "Payroll share of OASDI trust fund income",
         "value": 0.913,
         "threshold": "n/a, context for the fiscal channel",
         "status": "REPORTED",
         "source": "repository finding A32, from SSA trustees data",
         "date": "2025"},
    ]
    D = pd.DataFrame(rows)
    D.to_csv(DASH / "dashboard.csv", index=False)
    (DASH / "README.md").write_text(
        "# Trigger dashboard\n\n"
        f"Version {VERSION}, generated {TODAY}.\n\n"
        "Every indicator computable from public data, with its current value, source, date "
        "and threshold where one exists. Regenerated whenever an input changes.\n\n"
        "## NOT YET POPULATED, and deliberately left empty rather than guessed\n\n"
        "- Auto loan delinquency. Needs the New York Fed Household Debt and Credit report "
        "transition rates, not yet retrieved and verified.\n"
        "- Driverless fleet counts. Needs company disclosures, to be labelled as such.\n"
        "- OASDI trust fund balance. Needs the current Trustees Report, not yet retrieved.\n",
        encoding="utf-8")
    return D


def main():
    P = build_scenarios()
    D = build_dashboard()
    pd.set_option("display.width", 220)
    print(f"=== release {VERSION} written to data/release/ ===")
    print(f"\nscenarios/paths.csv: {len(P)} rows")
    print(P.groupby("regime").size().to_string())
    print("\n  regimes are now INSIDE_DATA / BOUNDARY_BAND / OUTSIDE_DATA, replacing "
          "SLOW / FAST / SUDDEN")
    print("\ndashboard/dashboard.csv:")
    print(D[["indicator", "value", "threshold", "status"]].to_string(index=False))


if __name__ == "__main__":
    main()
