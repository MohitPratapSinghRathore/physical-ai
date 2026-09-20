"""TAU_K REBUILT FROM COMPONENTS. Item 2 of the closing task.

THE OBJECT. The marginal effective tax rate on a dollar of AI surplus earned in the United
States, inclusive of EVERY layer that reaches that dollar: entity-level federal tax, state
corporate tax, the preferential regimes on foreign and foreign-derived income, and the
shareholder-level tax on the distribution. It is a MARGINAL, FLOW rate. Item 6 argues the
base, and states the counter-argument.

NO LAYER IS COUNTED TWICE. See definitions.md. In one line: Acemoglu, Manera and Restrepo
(2020) already include personal-level taxes in their effective rates, and their algebra under
full expensing collapses the C-corporation equity-financed normal-return rate to the
SHAREHOLDER rate alone. So a construction that stops at the entity level, as this project
operative 0.0708 does, omits a layer rather than avoiding double-counting. That omission
biases 0.0708 DOWNWARD, which is the direction the IMF comparison already suggested.

VERIFICATION STATUS IS CARRIED PER COMPONENT and it is the main result of this module.
Only five components could be verified from primary sources in this session. The rest are
swept, not asserted, and are listed in lit/unverified.md carrying no dependent claim.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent

# ----------------------------------------------------------------------------- VERIFIED

V_FED_CIT = 0.21   # 26 USC 11(b), flat. Unchanged by Pub. L. 119-21.

# VERIFIED TODAY, and the pre-2025 descriptions are now WRONG. Pub. L. 119-21 (4 July 2025)
# renamed 26 USC 951A from "Global intangible low-taxed income" to "Net CFC tested income"
# and reset the 26 USC 250(a)(1) deductions. Cornell LII text read 2026-09-20:
#   250(a)(1)(A) "33.34 percent of the foreign-derived deduction eligible income"
#   250(a)(1)(B) "40 percent of ... the net CFC tested income amount"
FDDEI_DEDUCTION = 0.3334
CFC_DEDUCTION = 0.40
V_FDDEI_RATE = V_FED_CIT * (1 - FDDEI_DEDUCTION)      # 0.13999 -> 14.0 percent
V_CFC_RATE = V_FED_CIT * (1 - CFC_DEDUCTION)          # 0.126   -> 12.6 percent
# The pre-2025 figures, kept only so a reader can see that they have moved:
PRE2025_FDII_RATE = V_FED_CIT * (1 - 0.375)           # 0.13125
PRE2025_GILTI_RATE = V_FED_CIT * (1 - 0.50)           # 0.105

# ONE verified source only. A second was sought and not obtained, so the shifted share is
# also swept below rather than fixed at this value.
V_SHIFTED = 0.48

# THE RENT SHARE, TWO READINGS, NEVER AVERAGED. They are incompatible readings of one
# accounting residual, not endpoints of an interval.
RENT_READINGS = {"Barkai": 0.351, "Karabarbounis_Neiman_case_R": 0.00}

# ------------------------------------------------------------------------- NOT VERIFIED
# Every one of these was sought from a primary source this session and could not be
# obtained. They are SWEPT over the stated ranges and no point value is asserted. Each
# range is bounded by statute or by structure, and the bound is named.

# ------------------------------------------ SOURCED IN A115, no longer swept blind
# Both were verified from the documents the owner supplied. Full extraction, with tables,
# page references and the method, is in notes/sources/SHAREHOLDER_PARAMS_extracted.md.

# THETA, the share of US corporate equity held in TAXABLE accounts.
# Rosenthal and Austin (Tax Notes, 16 May 2016, p. 923) Table 2: 0.242 of C corporation
# stock in 2015, down from 0.836 in 1965. Rosenthal and Burke (2020, NYU Tax Policy
# Colloquium, quoted in CRS R47113 note 9): 0.25, with 0.30 in retirement assets and the
# remainder foreign. Rosenthal and Mucciolo (Tax Notes Federal 183(1), 1 April 2024)
# Table 5: 0.27 of total US equity in 2022; Table 7: 0.28 of publicly traded stock.
# Method: Fed Financial Accounts L.224, with the residual household sector decomposed,
# pass-through issuances removed and their holdings allocated to beneficial owners.
# Non-taxable holders in 2022: foreign 0.42, IRAs 0.11, DB 0.07, DC 0.07, nonprofits 0.04,
# life insurance separate accounts 0.02, government 0.01.
THETA_TAXABLE = {"low": 0.24, "central": 0.27, "high": 0.28,
                 "low_source": "Rosenthal and Austin 2016 Table 2, C corporation stock, 2015",
                 "central_source": "Rosenthal and Mucciolo 2024 Table 5, total US equity, 2022",
                 "high_source": "Rosenthal and Mucciolo 2024 Table 7, publicly traded, 2022"}

# THE DEFERRAL FACTOR, effective over statutory, from deferral, unindexed inflation,
# step-up in basis at death, and the distribution of shareholder rates. CRS R47113 Table 5,
# third row, taken BEFORE its taxable-share adjustment so that theta is not counted twice:
#   no-dividend stock   9.8 / 23.8 = 0.4118
#   4 percent dividend 18.8 / 23.8 = 0.7899
# CRS states dividends are now "closer to 2 percent" because buybacks exceed half of
# distributions, "so the rate is somewhere in between": the midpoint is 0.6008.
# INDEPENDENT CROSS-CHECK, CBO 2014 Tables A-3 and A-4: gains are 3.4 pct short-term at
# 32.3, 49.6 pct long-term at 21.2, and 46.9 pct held until death and UNTAXED, implying
# 11.61 / 23.8 = 0.488, inside this range. Two separate datasets agree that roughly half of
# accrued gains never bear tax.
DEFERRAL_FACTOR = {"low": 0.4118, "central": 0.6008, "high": 0.7899,
                   "low_source": "CRS R47113 Table 5, no-dividend stock, 7-year holding",
                   "central_source": "CRS R47113 Table 5, midpoint, dividends near 2 percent",
                   "high_source": "CRS R47113 Table 5, 4 percent dividend stock",
                   "cross_check_cbo_2014": 0.488}

# THE DEBT SHARE, sourced in A117 from the Federal Reserve Z.1 at 2026Q2, nonfinancial
# corporate business (sector 10), read from this project own Z.1 cache. Debt is bonds
# (FL103163005, 8,278.0bn) plus loans (FL103168005, FL103169005, FL103169100) plus
# commercial mortgages (FL103165505), totalling 13,658.2bn.
#   against EQUITY AT MARKET VALUE, LM103164105 = 83,050.8bn -> 0.1412
#   against NET WORTH AT BOOK,      FL102090005 = 39,097.6bn -> 0.2589
# The basis is stated because it is the whole of the difference between the two ends.
#
# THE CAVEAT, which is load-bearing and is stated wherever this number is used. This is the
# economy-wide STOCK ratio for all nonfinancial corporations. What the assembly needs is the
# MARGINAL debt share of AI capital spending, a flow. Module B reading of the nine filers own
# books is that AI financing is predominantly EQUITY, which is BELOW this range. So the
# sourced range is, if anything, generous to the fiscal condition: a lower debt share raises
# the assembled rate, because AMR debt-financed normal return is negative.
DEBT_SHARE = {"low": 0.1412, "central": 0.2001, "high": 0.2589,
              "low_source": "Fed Z.1 2026Q2, debt over debt plus equity at MARKET value",
              "central_source": "midpoint of the two valuation bases",
              "high_source": "Fed Z.1 2026Q2, debt over debt plus net worth at BOOK value",
              "caveat": "economy-wide stock ratio used as a proxy for the marginal flow; "
                        "Module B points below this range, which would raise the rate"}

# The superseded blind sweeps, RETAINED as a sensitivity so the effect of sourcing is visible.
# THE BONDHOLDER RATE, sourced in A116 the same way as the shareholder layer: a taxable
# share of the instrument times a marginal rate on the income for taxable holders.
# CBO 2014 Table A-3, C corporation debt, from Fed Flow of Funds (8 March 2012), 2007:
#   nontaxable 0.328, temporarily deferred 0.149, FULLY TAXABLE 0.523.
#   CBO repeats the 0.328 twice in text: "almost one-third of interest income is sheltered"
#   (p.10) and "about 33 percent of interest payments made by C corporations ... were never
#   taxed" (p.24). The table already contains the fund look-through and the household
#   residual treatment.
# CBO 2014 Table A-4, from the 2006 SOI Public Use File:
#   INTEREST INCOME 0.274, below the 0.434 top statutory rate because many recipients sit in
#   lower brackets. Nonqualified annuity distributions 0.215.
# Fed Z.1 at 2026Q2 corroborates the direction: of 18,115.7bn of corporate and foreign bonds,
# the rest of the world holds 28.7 percent and households and nonprofits hold 1.1 percent
# DIRECTLY, nonprofits alone accounting for all of it. Taxable household exposure is almost
# entirely indirect, through mutual funds (14.8) and life insurance (21.8), which is what
# CBO looks through. See framework/tau_k/z1_bond_holders.json.
BONDHOLDER_RATE = {"low": 0.523 * 0.274,
                   "central": (0.523 * 0.274 + (0.523 * 0.274 + 0.149 * 0.215)) / 2,
                   "high": 0.523 * 0.274 + 0.149 * 0.215,
                   "low_source": "CBO 2014 Tables A-3 and A-4: fully taxable share only",
                   "central_source": "midpoint of the two bounds",
                   "high_source": "plus the temporarily deferred tranche at CBO's own "
                                  "nonqualified annuity rate, with no credit for deferral, "
                                  "so an upper bound",
                   "published_cross_check": "CBO 2014 Table 2: the ETR on C-corporation "
                                            "debt-financed investment is -0.06, and AMR's "
                                            "tau_b - tau_c at this range is -0.067 to "
                                            "-0.035. Sign and magnitude agree."}

# The superseded blind sweeps, RETAINED as a sensitivity so the effect of sourcing is visible.
SUPERSEDED_SWEEP = {"theta_taxable": [0.20, 0.60], "deferral_factor": [0.40, 1.00],
                    "bondholder_rate": [0.15, 0.37],
                    "debt_share": [0.00, 0.40]}

U = {
    "shareholder_rate": {
        "range": [0.15, 0.238],
        "bound": "statutory ceiling: the top long-term capital gain and qualified dividend "
                 "rate of 20 percent plus the 3.8 percent net investment income tax is 23.8 "
                 "percent, which no shareholder layer may exceed.",
        "sought": "a sourced average realised rate across the holder distribution.",
    },
    "state_cit_effective": {
        "range": [0.00, 0.095],
        "bound": "state statutory corporate rates run from zero to roughly the high single "
                 "digits; the upper end is a ceiling, not an estimate.",
        "sought": "a verified apportioned effective state rate.",
    },
    "shifted_share": {
        "range": [0.30, 0.60],
        "bound": "a share. Centred on the one verified value, 0.48 (Torslov, Wier and "
                 "Zucman), and swept because a SECOND verified source was required and not "
                 "obtained.",
        "sought": "Clausing (NBER w28442) and Garcia-Bernardo, Jansky and Zucman (NBER "
                  "w30086, title verified, abstract not retrievable). Neither abstract "
                  "could be read from a primary source in this session.",
    },
}

CEILINGS = {"shareholder_rate": 0.238, "state_cit_effective": 0.095,
            "shifted_share": 1.0, "debt_share": 1.0,
            "theta_taxable": 1.0, "deferral_factor": 1.0,
            "bondholder_rate": 0.434}   # CBO: top ordinary rate incl. the 3.8 pct NIIT


def dump():
    out = {
        "object": "marginal effective tax rate on a dollar of US AI surplus, all layers",
        "verified": {
            "federal_cit": V_FED_CIT,
            "fddei_effective_rate_CURRENT": round(V_FDDEI_RATE, 5),
            "net_cfc_tested_income_effective_rate_CURRENT": round(V_CFC_RATE, 5),
            "pre2025_fdii_rate_SUPERSEDED": round(PRE2025_FDII_RATE, 5),
            "pre2025_gilti_rate_SUPERSEDED": round(PRE2025_GILTI_RATE, 5),
            "statutory_change": "Pub. L. 119-21, 4 July 2025. 26 USC 951A recaptioned from "
                                "Global intangible low-taxed income to Net CFC tested "
                                "income; 26 USC 250(a)(1) deductions set to 33.34 and 40 "
                                "percent. Verified from Cornell LII on 2026-09-20. The "
                                "pre-2025 rates of 13.125 and 10.5 percent are SUPERSEDED "
                                "and must not be used.",
            "shifted_share_single_verified_value": V_SHIFTED,
            "rent_readings_NEVER_AVERAGED": RENT_READINGS,
        },
        "SOURCED_A115": {"theta_taxable": THETA_TAXABLE,
                         "deferral_factor": DEFERRAL_FACTOR,
                         "bondholder_rate": BONDHOLDER_RATE,
                         "debt_share": DEBT_SHARE,
                         "superseded_blind_sweep": SUPERSEDED_SWEEP},
        "not_verified_swept": U,
        "the_main_result_of_this_module":
            "A117: the debt share is sourced too. Nine components verified, three swept.",
    }
    (HERE / "components.json").write_text(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    dump()
    print("VERIFIED COMPONENTS")
    print("  federal CIT                      0.21000   26 USC 11(b)")
    print(f"  FDDEI effective, CURRENT         {V_FDDEI_RATE:.5f}   "
          f"was {PRE2025_FDII_RATE:.5f} pre-2025")
    print(f"  net CFC tested income, CURRENT   {V_CFC_RATE:.5f}   "
          f"was {PRE2025_GILTI_RATE:.5f} pre-2025")
    print("  shifted share                    0.48000   Torslov, Wier and Zucman")
    print(f"  rent share, two readings         {RENT_READINGS}")
    print("\nNOT VERIFIED, SWEPT, no point value asserted")
    for k, v in U.items():
        print(f"  {k:20s} {str(v['range']):14s} ceiling named: {v['bound'][:52]}")
