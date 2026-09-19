"""Item 1: the supervisory conversion layer. Every factor with source, date and range.

This is the mapping from macro severity to loss rates and to bank capital capacity. It is
the layer the order-of-stress table needs, and it is built entirely from sources read
directly and recorded here with their numbers, so that a stress-test designer can check each
one against its original.

CONTENTS

  A. Federal Reserve 2026 Dodd-Frank Act stress test: the severely adverse scenario, the
     projected loss rates by loan category, and aggregate capital.
  B. Gerardi, Herkenhoff, Ohanian and Willen: mortgage default conditional on unemployment
     and on negative equity, which is the double trigger.
  C. New York Fed Household Debt and Credit: balances and aggregate delinquency.
  D. What is NOT obtained, named exactly once for the owner.

EVERY FIGURE BELOW WAS READ FROM THE DOCUMENT ITSELF, not from a summary.
"""
import json, pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

# ---------------------------------------------------------------------------
# A. Federal Reserve 2026 DFAST. data/raw/manual/FRB_2026_DFAST_results.pdf, 68 pages,
#    downloaded from federalreserve.gov 2026-09-19. Published June 2026.
# ---------------------------------------------------------------------------
FRB_SCENARIO = {
    "document": "2026 Federal Reserve Stress Test Results, June 2026",
    "url": "https://www.federalreserve.gov/publications/files/2026-dfast-results-20260624.pdf",
    "local": "data/raw/manual/FRB_2026_DFAST_results.pdf",
    "table": "Table 2, key variables in the 2025 and 2026 supervisory severely adverse scenarios",
    "banks_covered": 32,
    "horizon": "2026:Q1 to 2028:Q1, nine quarters",
    "severely_adverse_2026": {
        "unemployment_peak_pct": 10.0,
        "unemployment_rise_pp": 5.5,
        "real_gdp_peak_to_trough_pct": -4.6,
        "house_prices_pct": -30.0,
        "cre_prices_pct": -39.0,
        "equity_prices_pct": -58.0,
        "bbb_spread_rise_pp": 4.7,
    },
    "severely_adverse_2025_for_comparison": {
        "unemployment_peak_pct": 10.0, "unemployment_rise_pp": 5.9,
        "real_gdp_peak_to_trough_pct": -7.8, "house_prices_pct": -33.0,
        "cre_prices_pct": -30.0, "equity_prices_pct": -50.0,
    },
}

# Table 9, projected aggregate loan losses by type, severely adverse, 2026:Q1 to 2028:Q1
FRB_LOSS_RATES = [
    {"loan_type": "TOTAL loan losses", "losses_usd_bn": 624.9, "loss_rate_pct": 6.9,
     "bank_range_pct": "0.7 to 20.7"},
    {"loan_type": "First-lien mortgages, domestic", "losses_usd_bn": 22.5,
     "loss_rate_pct": 1.5, "bank_range_pct": None},
    {"loan_type": "Junior liens and HELOCs, domestic", "losses_usd_bn": 5.5,
     "loss_rate_pct": 3.2, "bank_range_pct": None},
    {"loan_type": "Commercial and industrial", "losses_usd_bn": 158.2,
     "loss_rate_pct": 9.0, "bank_range_pct": "3.4 to 48.5"},
    {"loan_type": "Commercial real estate, domestic", "losses_usd_bn": 76.5,
     "loss_rate_pct": 8.8, "bank_range_pct": None},
    {"loan_type": "Credit cards", "losses_usd_bn": 203.0, "loss_rate_pct": 17.1,
     "bank_range_pct": "9.5 to 22.7"},
    {"loan_type": "Other consumer (INCLUDES student loans AND automobile loans)",
     "losses_usd_bn": 54.1, "loss_rate_pct": 7.3, "bank_range_pct": None},
    {"loan_type": "Other loans (includes international real estate)",
     "losses_usd_bn": 105.0, "loss_rate_pct": 3.8, "bank_range_pct": None},
]

FRB_CAPITAL = {
    "total_losses_absorbed_usd_bn": 708,
    "aggregate_cet1_start_pct": 12.8,
    "aggregate_cet1_start_date": "2025:Q4",
    "aggregate_cet1_minimum_pct": 11.2,
    "aggregate_cet1_end_pct": 12.7,
    "cet1_decline_pp": 1.6,
}

# ---------------------------------------------------------------------------
# B. Gerardi, Herkenhoff, Ohanian and Willen, "Can't Pay or Won't Pay? Unemployment,
#    Negative Equity, and Strategic Default". NBER Working Paper 21630, October 2015;
#    published in the Review of Financial Studies. data/raw/manual/GHOW2018_cant_pay.pdf,
#    74 pages, read directly. Panel Study of Income Dynamics.
# ---------------------------------------------------------------------------
GHOW = {
    "document": "Gerardi, Herkenhoff, Ohanian and Willen, Can't Pay or Won't Pay?",
    "nber_wp": 21630, "wp_date": "October 2015",
    "local": "data/raw/manual/GHOW2018_cant_pay.pdf",
    "unemployed_head_default_effect_pp": 5.0,
    "both_head_and_spouse_unemployed_default_effect_pp": 8.0,
    "job_loss_equity_equivalent_pct": 35.0,
    "unemployed_share_full_sample_pct": 5.0,
    "unemployed_share_of_defaulters_pct": 20.0,
    "defaulters_strategic_pct": 38.0,
    "defaulters_below_subsistence_pct": 30.0,
    "defaulters_intermediate_pct": 33.0,
    "notes": [
        "An unemployed household head is about 5 percentage points more likely to default "
        "than an employed head.",
        "A household in which BOTH head and spouse experience an unemployment spell is more "
        "than 8 percentage points more likely to default. This is the within-household "
        "correlated displacement factor the sudden-shock module needs, and it is "
        "SUPERADDITIVE: 8 against 5, not 10.",
        "Job loss has an equivalent effect on default likelihood as a 35 percent decline in "
        "equity. That is the exchange rate between the two legs of the double trigger.",
        "5 percent of the full sample is unemployed against 20 percent of defaulters.",
    ],
}

# ---------------------------------------------------------------------------
# C. New York Fed Household Debt and Credit, 2026:Q2, released August 2026.
#    data/raw/manual/NYFed_HHDC_2026Q2.pdf, 46 pages, read directly.
# ---------------------------------------------------------------------------
NYFED = {
    "document": "Quarterly Report on Household Debt and Credit, 2026:Q2",
    "released": "August 2026",
    "local": "data/raw/manual/NYFed_HHDC_2026Q2.pdf",
    "total_household_debt_usd_tn": 18.8,
    "mortgage_balances_usd_tn": 13.1,
    "heloc_balances_usd_bn": 459,
    "auto_balance_change_usd_bn": 28,
    "auto_originations_usd_bn": 211,
    "share_of_debt_in_any_delinquency_pct": 4.7,
    "notes": [
        "Aggregate delinquency 4.7 percent of outstanding debt at end June 2026, down 0.1 "
        "percentage points on the quarter.",
        "Transition into early delinquency upticked slightly for auto loans and mortgages.",
        "AUTO IS NOT BROKEN OUT AS A LOSS RATE HERE. The report publishes balances, "
        "originations and delinquency transitions as charts; the loss rate this project "
        "needs is not in the text.",
    ],
}

# ---------------------------------------------------------------------------
# D. NOT OBTAINED. Named once, precisely, for the owner.
# ---------------------------------------------------------------------------
MISSING = [
    {"needed": "Auto loan LOSS RATE, separately from student loans",
     "why": "The Federal Reserve's Table 9 folds automobile loans and student loans "
            "together into Other consumer at 7.3 percent. The order-of-stress table needs "
            "them apart, because the driving pathway sits in auto and the entrant incidence "
            "case sits in student loans.",
     "exact_document": "Either (a) the FR Y-14M auto loan schedule aggregates, or (b) the "
                       "New York Fed Household Debt and Credit companion data file "
                       "hhd_c_report_2026q2.xlsx, which carries the auto 90-plus "
                       "delinquency transition series behind chart 25, or (c) a rating "
                       "agency auto ABS loss index such as the Fitch or S and P US Auto "
                       "Loan ABS index.",
     "status": "The NY Fed PDF was obtained and read; the companion xlsx was not "
               "retrieved in this session."},
    {"needed": "Agency multifamily debt service coverage ratio underwriting standards",
     "why": "The landlord and multifamily lender balance sheet needs a stated DSCR norm to "
            "define its materiality threshold.",
     "exact_document": "Fannie Mae Multifamily Selling and Servicing Guide, Part III "
                       "underwriting, the minimum DSCR table; mfguide.fanniemae.com is "
                       "reachable but the specific DSCR table was not extracted in this "
                       "session. Freddie Mac Multifamily Seller/Servicer Guide is the "
                       "equivalent alternative.",
     "status": "Host reachable, extraction not done."},
]


def main():
    L = pd.DataFrame(FRB_LOSS_RATES)
    L.to_csv(OUT / "conversion_frb_loss_rates.csv", index=False)
    bundle = {"frb_scenario": FRB_SCENARIO, "frb_loss_rates": FRB_LOSS_RATES,
              "frb_capital": FRB_CAPITAL, "ghow_default": GHOW, "nyfed": NYFED,
              "not_obtained": MISSING, "compiled": "2026-09-19"}
    (OUT / "conversion_layer.json").write_text(json.dumps(bundle, indent=2))

    pd.set_option("display.width", 240)
    print("=== A. FEDERAL RESERVE 2026 SEVERELY ADVERSE SCENARIO (the benchmark) ===")
    for k, v in FRB_SCENARIO["severely_adverse_2026"].items():
        print(f"  {k:36s} {v}")
    print(f"\n  32 banks, nine quarters 2026:Q1 to 2028:Q1")

    print("\n=== Table 9: projected loss rates by loan category ===")
    print(L.to_string(index=False))

    print("\n=== aggregate capital ===")
    for k, v in FRB_CAPITAL.items():
        print(f"  {k:36s} {v}")

    print("\n=== B. GERARDI, HERKENHOFF, OHANIAN AND WILLEN: the double trigger ===")
    print(f"  unemployed head, default effect            +{GHOW['unemployed_head_default_effect_pp']} pp")
    print(f"  BOTH head and spouse unemployed            +{GHOW['both_head_and_spouse_unemployed_default_effect_pp']} pp  "
          f"(superadditive, not 10)")
    print(f"  job loss equals an equity decline of       {GHOW['job_loss_equity_equivalent_pct']}%")
    print(f"  defaulters unable to pay without dropping below subsistence: "
          f"{GHOW['defaulters_below_subsistence_pct']}%")

    print("\n=== C. NEW YORK FED HOUSEHOLD DEBT AND CREDIT 2026:Q2 ===")
    print(f"  total household debt {NYFED['total_household_debt_usd_tn']}tn, "
          f"mortgages {NYFED['mortgage_balances_usd_tn']}tn")
    print(f"  share of debt in any stage of delinquency: "
          f"{NYFED['share_of_debt_in_any_delinquency_pct']}%")

    print("\n=== D. NOT OBTAINED, named once ===")
    for m in MISSING:
        print(f"\n  NEEDED: {m['needed']}")
        print(f"    why:      {m['why']}")
        print(f"    document: {m['exact_document']}")
        print(f"    status:   {m['status']}")


if __name__ == "__main__":
    main()
