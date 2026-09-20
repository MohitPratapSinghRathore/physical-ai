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

U = {
    "theta_taxable": {
        "range": [0.20, 0.60],
        "bound": "a share, so [0,1]; narrowed only by the qualitative fact that retirement "
                 "accounts and foreign holders together are widely described as the "
                 "majority of US corporate equity.",
        "sought": "Rosenthal and Austin, Tax Policy Center. Site returned HTTP 403.",
    },
    "shareholder_rate": {
        "range": [0.15, 0.238],
        "bound": "statutory ceiling: the top long-term capital gain and qualified dividend "
                 "rate of 20 percent plus the 3.8 percent net investment income tax is 23.8 "
                 "percent, which no shareholder layer may exceed.",
        "sought": "a sourced average realised rate across the holder distribution.",
    },
    "deferral_factor": {
        "range": [0.40, 1.00],
        "bound": "a share, so [0,1]. 1.0 is immediate realisation, the ceiling; deferral and "
                 "basis step-up can only reduce it.",
        "sought": "a sourced accrual-equivalent discount.",
    },
    "state_cit_effective": {
        "range": [0.00, 0.095],
        "bound": "state statutory corporate rates run from zero to roughly the high single "
                 "digits; the upper end is a ceiling, not an estimate.",
        "sought": "a verified apportioned effective state rate.",
    },
    "debt_share": {
        "range": [0.00, 0.40],
        "bound": "a share. Zero is all-equity, which is the reported AI financing structure "
                 "on the nine filers own books in this project Module B.",
        "sought": "a verified marginal debt share for AI capital spending.",
    },
    "bondholder_rate": {
        "range": [0.15, 0.37],
        "bound": "ordinary income treatment, so the top ordinary rate is the ceiling.",
        "sought": "a sourced average bondholder marginal rate.",
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

CEILINGS = {"shareholder_rate": 0.238, "bondholder_rate": 0.37, "state_cit_effective": 0.095,
            "theta_taxable": 1.0, "deferral_factor": 1.0, "debt_share": 1.0,
            "shifted_share": 1.0}


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
        "not_verified_swept": U,
        "the_main_result_of_this_module":
            "Of the components needed to pin the rate, five are verified and seven are not. "
            "The seven include every parameter of the shareholder layer. A point estimate of "
            "tau_k therefore cannot be asserted from sources, and the honest object is a map "
            "over the unverified components rather than a verdict.",
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
