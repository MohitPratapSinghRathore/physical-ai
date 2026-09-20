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
VERSION = "0.8.0"
TODAY = "2026-09-20"

CHANGELOG = """# Changelog

## 0.8.0 (2026-09-20)
Independent replication round one matched 21 of 51 quantities. This release is the repair.
The mismatches are classified in notes/replication/round1_mismatch_classification.md and the
rebuilt brief is notes/replication_brief_v2.md.

- THE BREAK-EVEN CAPITAL TAX RATE WAS WRONG AND IS CORRECTED. The replicator found the
  sealed case A maximum of 0.378371 above the highest reading of tau_l, which the brief's own
  definition tau_l * (1 - R) makes impossible. Two defects multiplied: the expression divided
  a loss that ALREADY nets out tau_k by a surplus, and numerator and denominator were built
  on two different wage bill totals. Case A is now 0.125 to 0.301 and case B 0.182 to 0.650,
  replacing 0.214 to 0.378 and 0.561 to 0.860. Plausibility bounds are now enforced: case A
  cannot exceed tau_l + g, no rate can exceed 1, and case B cannot fall below case A.
- THE WAGE BILL BASE IS CORRECTED THROUGHOUT. A dose is converted to dollars on FRED WASCUR
  national wages and salaries, the base tau_l is actually built on. The fiscal modules were
  using compensation of employees, which includes employer pension and health contributions
  that bear neither the income tax nor the payroll tax, and the second-round module was using
  this project's occupational grid, which is 73.9 percent of national wages. Fiscal dollar
  figures fall 17.6 percent; second-round demand figures rise 35.4 percent.
- THE TRUST FUND DENOMINATORS ARE READ FROM THE TRUSTEES REPORT, not derived. HI payroll
  income is 403.2bn, replacing 462.4bn, which is HI TOTAL income including interest,
  government contributions and premiums. HI's own payroll share of fund income, 0.8720,
  replaces the OASDI share of 0.9126 that was being applied to both funds.
- THE TRUST FUND RESERVE COLUMN IS FILLED and DEPLETION TIMING is added as a second capacity
  measure: OASI 2,338.3bn depleting 2032 Q4, DI 223.0bn not depleting within 75 years, HI
  255.7bn depleting 2033 Q2. HI was NOT in deficit in 2025: its reserves rose by 18.2bn.
- THE AUTO AGGREGATE MOVES OFF A DISCONTINUED SERIES. FRED MVLOAS ended at 2024Q4 while every
  other input is 2026. Replaced with the NY Fed Household Debt and Credit auto loan balance,
  1,713bn at 2026Q2, the same source and vintage as the mortgage and student aggregates. The
  auto under-reporting factor moves from 1.743 to 1.904; the auto bank loss does not move,
  because the bank-held share carries the same denominator and the two cancel.
- THE DASHBOARD gains auto loan delinquency, the trust fund reserve balances and the
  depletion dates, which standing requirement 4 asks for and which were previously recorded
  as blocked.

## 0.7.0 (2026-09-20)
- THE TABLE IS REORGANISED BY WAGE QUINTILE. Exposure type turned out to be a pay proxy in
  three independent tests, so the organising dimension is now where in the wage distribution
  displacement falls, and the exposure indices are named scenarios for that.
- CASE A AND CASE B. Every fiscal number now carries its case: output preserved with income
  redistributed to capital (A), or output falling with demand so the taxable surplus falls
  too (B). Case B raises the fiscal loss by 25 to 44 percent and the break-even capital tax
  rate from 0.21 to 0.38 up to 0.56 to 0.86.
- DEBT PATHS ARE INCREMENTS over a no-displacement baseline under the same interest rate and
  growth assumptions. The earlier 389 percent emerging-market figure is WITHDRAWN as a
  statement about automation: it was almost entirely baseline compounding.
- SECOND-ROUND SENSITIVITY across sourced ranges for the marginal propensity to consume, the
  income elasticity of house prices, the Okun coefficient and the loss mapping. The bank-loss
  headline spans a factor of nine, and "a demand event first" survives only conditionally.

## 0.6.0 (2026-09-20)
- THE ORDER OF STRESS IS RETIRED AND REPLACED BY A DOSE-RESPONSE TABLE. Ranking balance
  sheets by which crosses its materiality threshold first is not meaningful when each sheet
  is measured against a different yardstick: only 4 of 15 pairwise orderings survived moving
  the thresholds. Every cell now reports the loss in dollars, as a share of GDP, and as a
  share of that sheet's own SOURCED absorbing capacity, in two columns, first round and with
  second-round effects.
- SECOND-ROUND MODULE added: demand through a marginal propensity to consume derived from
  Mian, Straub and Sufi; house prices through the Harter-Dreiman income elasticity, larger
  in supply-constrained high-cost metros; business credit, commercial real estate and cards
  through the Federal Reserve mapping only. All SCENARIO, all banded.
- SOVEREIGN CONSOLIDATION added: the share of every loss that ultimately lands on the
  federal government, after credit risk transfer and private mortgage insurance take the
  first loss on the agency book.
- SURVEY UNDER-REPORTING CORRECTED AT SOURCE. The earlier factors conflated under-reporting
  with sample coverage and were 14 to 26 percent too large. Every credit row falls.
- EXPOSURE-TYPE CONTRASTS DOWNGRADED. Neither the household nor the fiscal contrast survives
  controlling for pay. The scenario axis is now reported by WAGE QUINTILE as well as by
  exposure index, and the exposure indices are named scenarios for where in the wage
  distribution displacement falls.
- MORTGAGE HOLDER SPLIT SOURCED. The flagged 60 to 70 percent agency range is replaced by a
  decomposition read from the GSEs' own 2025 Forms 10-K: GSE 51.1 percent, FHA 12.6 percent
  (flagged proxy), bank portfolio 11.5 percent, residual 24.9 percent.
- REINSTATEMENT TERM added to the labour model from Acemoglu and Restrepo 2019, after which
  the labour model is FROZEN as an appendix scenario generator.
- SEALED EXPECTED VALUES published alongside a replication brief.

## 0.5.0 (2026-09-19)
- Supervisory conversion layer added: Federal Reserve 2026 DFAST severely adverse scenario
  and Table 9 loss rates, Gerardi et al. conditional default, NY Fed household debt.
- Five dashboard rows filled, including three ENTRY-LEVEL indicators that detect
  attrition-led automation, which A64 showed the existing indicator set cannot see.

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


def _nyfed_auto_delinquency_pct():
    """Percent of auto loan balance 90+ days delinquent, latest quarter, read from the NY
    Fed report's own data workbook. Standing requirement 4 names this indicator."""
    import openpyxl
    wb = openpyxl.load_workbook(
        ROOT / "data" / "raw" / "manual" / "NYFed_HHDC_2026Q2_data.xlsx",
        read_only=True, data_only=True)
    ws = wb["Page 12 Data"]
    rows = list(ws.iter_rows(values_only=True))
    header = next(list(r) for r in rows if r and "AUTO" in [str(c).strip().upper()
                                                            if c else "" for c in r])
    col = [str(c).strip().upper() if c else "" for c in header].index("AUTO")
    data = [r for r in rows if r and r[0] and isinstance(r[1], (int, float))]
    return round(float(data[-1][col]), 2)


_TR = json.loads((ROOT / "data" / "processed"
                  / "owner_sources.json").read_text())["trustees_2026"]
_AUTO_DELINQ = _nyfed_auto_delinquency_pct()


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
        {"indicator": "Effective tax rate on AI surplus, assembled from components, "
                      "all tax layers counted once, Barkai rent reading",
         "value": "0.086 central, 0.070 to 0.102 (Barkai); 0.015 (Karabarbounis-Neiman)",
         "threshold": f'{round(tks["required_tau_k"]["AMR_0.255"], 4)} to 0.1373',
         "status": "BELOW THRESHOLD under BOTH rent readings, and ROBUST: passes in under "
                   "1 percent of the remaining parameter space against the easier "
                   "labour-tax reading and NOWHERE against the harder. No single unsourced "
                   "parameter can cross a threshold alone",
         "source": "framework/tau_k/. AMR 2020 expensing algebra; 26 USC 11(b); 26 USC "
                   "250(a)(1) as amended by Pub. L. 119-21 of 2025, giving 14.0 and 12.6 "
                   "percent; Barkai and Karabarbounis-Neiman rent readings. A115 SOURCED "
                   "the taxable-shareholder share (0.24 to 0.28, Rosenthal and Austin 2016, "
                   "Rosenthal and Mucciolo 2024) and the deferral factor (0.412 to 0.790, "
                   "CRS R47113, cross-checked against CBO 2014). The bondholder rate "
                   "A116 sourced the bondholder rate (0.143 to 0.175, CBO 2014 Tables A-3 "
                   "and A-4, cross-checked against CBO Table 2 measured -6 percent). The "
                   "debt share of AI capex remains unsourced at 37 percent of residual "
                   "variance",
         "date": "2026-09-20, sourced A115 and A116"},
        {"indicator": "Effective tax rate on AI surplus, entity level only, SUPERSEDED",
         "value": 0.0708,
         "threshold": round(tks["required_tau_k"]["AMR_0.255"], 4),
         "status": "SUPERSEDED by the component rebuild. It omitted shareholder-level tax "
                   "entirely and is the bottom edge of the assembled range, not its centre",
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
        {"indicator": "Recent college graduate unemployment rate",
         "value": 5.6,
         "threshold": "no threshold set; entry-level blind-spot indicator",
         "status": "ELEVATED per the source",
         "source": "Federal Reserve Bank of New York, The Labor Market for Recent College "
                   "Graduates",
         "date": "2026:Q2"},
        {"indicator": "Recent college graduate underemployment rate",
         "value": 42.0,
         "threshold": "no threshold set; entry-level blind-spot indicator",
         "status": "REPORTED, edged up per the source",
         "source": "Federal Reserve Bank of New York, The Labor Market for Recent College "
                   "Graduates",
         "date": "2026:Q2"},
        {"indicator": "Employment gap, workers aged 22 to 25 in AI-exposed occupations",
         "value": "19 percent below the less-exposed counterfactual",
         "threshold": "no threshold set; this is the attrition blind-spot indicator",
         "status": "WIDENING since first documented August 2025",
         "source": "Brynjolfsson, Chandar and Chen, Canaries in the Coal Mine?, August "
                   "2026, ADP payroll microdata. Operates through REDUCED HIRING, not "
                   "increased separations",
         "date": "through June 2026"},
        {"indicator": "Household debt in any stage of delinquency",
         "value": 4.7,
         "threshold": "no threshold set",
         "status": "REPORTED, down 0.1pp on the quarter",
         "source": "New York Fed Household Debt and Credit 2026:Q2",
         "date": "2026-06"},
        {"indicator": "Aggregate CET1 under the Fed severely adverse scenario",
         "value": "12.8 falling to a minimum of 11.2 percent",
         "threshold": "regulatory minimums; all 32 banks remain above",
         "status": "REPORTED, the capacity benchmark",
         "source": "Federal Reserve 2026 Dodd-Frank Act stress test results, June 2026",
         "date": "2026-06"},
        {"indicator": "Payroll share of OASDI trust fund income",
         "value": round(_TR["payroll_share_of_oasdi_income"], 4),
         "threshold": "n/a, context for the fiscal channel",
         "status": "REPORTED",
         "source": "2026 Trustees Reports summary Table 5, placed by the owner at "
                   "data/raw/owner/. SUPERSEDES the 0.913 derived in A32",
         "date": "2025"},
        {"indicator": "Payroll share of HI trust fund income",
         "value": round(_TR["hi_payroll_income_bn"] / _TR["hi_total_income_bn"], 4),
         "threshold": "n/a, context for the fiscal channel",
         "status": "REPORTED. It is NOT the OASDI share, and using the OASDI share for HI "
                   "overstated every HI ratio by a factor of 1.047",
         "source": "2026 Trustees Reports summary Table 5",
         "date": "2025"},
        {"indicator": "Auto loan balance 90+ days delinquent",
         "value": _AUTO_DELINQ,
         "threshold": "no threshold set; the pathway-specific credit indicator standing "
                      "requirement 4 asks for",
         "status": "REPORTED. Filled this release; previously recorded as not retrieved",
         "source": "NY Fed Household Debt and Credit 2026:Q2 data workbook, Page 12 Data, "
                   "percent of balance 90+ days delinquent by loan type",
         "date": "2026-06"},
        {"indicator": "OASI trust fund reserves",
         "value": _TR["funds"]["OASI"]["reserves_end_2025_bn"],
         "threshold": "depleted 2032 Q4, after which 78 percent of scheduled benefits are "
                      "payable",
         "status": "FALLING. Net change in 2025 was -200.0bn",
         "source": "2026 Trustees Reports summary Tables 4, 7 and 8",
         "date": "end of 2025"},
        {"indicator": "DI trust fund reserves",
         "value": _TR["funds"]["DI"]["reserves_end_2025_bn"],
         "threshold": "not depleted within the 75-year projection window",
         "status": "RISING. Net change in 2025 was +39.8bn",
         "source": "2026 Trustees Reports summary Tables 4 and 8",
         "date": "end of 2025"},
        {"indicator": "HI trust fund reserves",
         "value": _TR["funds"]["HI"]["reserves_end_2025_bn"],
         "threshold": "depleted 2033 Q2, after which 89 percent of scheduled benefits are "
                      "payable",
         "status": "RISING in 2025 (+18.2bn). HI is NOT yet in deficit: the Trustees put "
                   "the first year cost exceeds income excluding interest at 2026",
         "source": "2026 Trustees Reports summary Tables 4, 7, 8 and 12",
         "date": "end of 2025"},
        {"indicator": "Combined OASDI reserve depletion date",
         "value": "2034 Q3",
         "threshold": "83 percent of scheduled benefits payable at depletion",
         "status": "A CAPACITY MEASURE IN TIME. A reserve stock says how much; a depletion "
                   "date says how long, and for a fund running down that is the number a "
                   "supervisor uses",
         "source": "2026 Trustees Reports summary Tables 7 and 8",
         "date": "2026 report"},
    ]
    D = pd.DataFrame(rows)
    D.to_csv(DASH / "dashboard.csv", index=False)
    (DASH / "README.md").write_text(
        "# Trigger dashboard\n\n"
        f"Version {VERSION}, generated {TODAY}.\n\n"
        "Every indicator computable from public data, with its current value, source, date "
        "and threshold where one exists. Regenerated whenever an input changes.\n\n"
        "## NOT YET POPULATED, and deliberately left empty rather than guessed\n\n"
        "- Driverless fleet counts. Needs company disclosures, to be labelled as such.\n\n"
        "## FILLED IN 0.8.0, previously recorded as blocked\n\n"
        "- Auto loan delinquency, from the NY Fed Household Debt and Credit 2026:Q2 data "
        "workbook.\n"
        "- OASDI and HI trust fund reserve balances and depletion dates, from the 2026 "
        "Trustees Reports summary tables the owner placed in data/raw/owner/.\n",
        encoding="utf-8")
    return D



def build_dose_response():
    """The dose-response table and the sovereign consolidation, as published artifacts."""
    import shutil
    DR = REL / "dose_response"
    DR.mkdir(parents=True, exist_ok=True)
    moved = []
    for src, dst in [("dose_response_two_columns.csv", "dose_response_two_columns.csv"),
                     ("dose_response_first_round.csv", "dose_response_first_round.csv"),
                     ("sovereign_consolidation.csv", "sovereign_consolidation.csv"),
                     ("wage_targeted_dose_response.csv", "by_wage_quintile.csv"),
                     ("two_worlds.csv", "policy_response_two_worlds.csv"),
                     ("second_round_severity.csv", "second_round_severity.csv"),
                     ("wage_quintile_dose_response.csv",
                      "by_wage_quintile_dose_response.csv"),
                     ("cases_A_and_B.csv", "cases_A_and_B.csv"),
                     ("debt_increments.csv", "debt_increments.csv"),
                     ("second_round_sensitivity.csv", "second_round_sensitivity.csv"),
                     ("capacities.json", "absorbing_capacities.json")]:
        s = OUT / src
        if s.exists():
            shutil.copyfile(s, DR / dst)
            moved.append(dst)
    (DR / "README.md").write_text(
        "# Dose-response table\n\n"
        f"Version {VERSION}, generated {TODAY}.\n\n"
        "Rows are displacement as a share of the TOTAL US wage bill. Columns are balance "
        "sheets. Every cell reports the loss in dollars, as a share of GDP, and as a share "
        "of that sheet's own absorbing capacity, whose measure and source are in "
        "`absorbing_capacities.json`.\n\n"
        "## Two columns, and what they mean\n\n"
        "**First round** is an accounting exercise on measured balances: displaced "
        "households, their obligations, and a default uplift from Gerardi, Herkenhoff, "
        "Ohanian and Willen. It holds house prices, consumer demand, business revenue and "
        "the employment of non-displaced workers FIXED. Against an economy-wide supervisory "
        "scenario it is a LOWER BOUND, not an estimate.\n\n"
        "**With second-round effects** is SCENARIO throughout. It maps each dose onto a "
        "macroeconomic severity and then borrows the Federal Reserve's own 2026 severely "
        "adverse loss rates at that severity. Beyond the Fed's own scenario the numbers are "
        "an extrapolation of its rates and are labelled as such.\n\n"
        "## What must travel with every number\n\n"
        "- **Cognitive exposure measures TASK OVERLAP, not displacement and not timing.** "
        "Top-quintile occupations on either cognitive index include a great deal of work "
        "more likely to be augmented than replaced.\n"
        "- **Only the 5 and 10 percent doses are fully inside the observed data range for "
        "every exposure type.** At 25 percent the embodied rows are already outside it.\n"
        "- **No single exposure type can deliver a 75 percent dose.** Embodied saturates at "
        "33.7 percent of the total wage bill, cognitive AIOE at 47.4 and cognitive GPT at "
        "53.6. Saturated rows report the loss at the largest attainable dose.\n"
        "- **No result is quoted as a cumulative percentage without its horizon.**\n"
        "- **No dollar figure is quoted without naming the incidence assumption.** On "
        "household counts incidence moves the answer by 5 to 9 percent; on dollars by 1.75 "
        "to 3.01 times.\n"
        "- **Exposure type is mostly a pay proxy.** Neither the household nor the fiscal "
        "exposure-type contrast survives controlling for wage level. `by_wage_quintile.csv` "
        "is the version organised around the primitive that actually does the work.\n",
        encoding="utf-8")
    return moved


def main():
    P = build_scenarios()
    D = build_dashboard()
    pd.set_option("display.width", 220)
    moved = build_dose_response()
    print(f"=== release {VERSION} written to data/release/ ===")
    print(f"  dose_response/: {', '.join(moved)}")
    print(f"\nscenarios/paths.csv: {len(P)} rows")
    print(P.groupby("regime").size().to_string())
    print("\n  regimes are now INSIDE_DATA / BOUNDARY_BAND / OUTSIDE_DATA, replacing "
          "SLOW / FAST / SUDDEN")
    print("\ndashboard/dashboard.csv:")
    print(D[["indicator", "value", "threshold", "status"]].to_string(index=False))


if __name__ == "__main__":
    main()
