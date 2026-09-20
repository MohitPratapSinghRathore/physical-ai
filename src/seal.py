"""SEALED EXPECTED VALUES for the replication brief.

Writes notes/sealed/sealed_expected_values_round2.json, the file a fresh instance opens only
AFTER rebuilding the quantities in notes/replication_brief_v2.md from raw data.

WHY notes/sealed/ AND NOT data/release/. data/release/ is a PUBLICATION folder: the scenario
file and the trigger dashboard are meant to be handed to a supervisor. Expected values and
tolerances are the opposite of that. They exist to be withheld from a replicator until their
own rebuild is finished, and shipping them in the published artifact would defeat the whole
exercise. They live beside the brief instead. It carries
the expected value, the tolerance and the construction's one-line identity, and nothing that
would let a replicator shortcut the rebuild.

ROUND TWO. Round one is FROZEN at notes/sealed/sealed_expected_values_round1_ARCHIVED.json
and is never regenerated: it is the record the first replication was scored against and
rewriting it would destroy that record. This module writes round two to its own path.
Neither file goes anywhere near notes/replication/, which is the replicator's own folder.

WHAT MOVED BETWEEN THE ROUNDS, and why, is listed in
notes/replication/round1_mismatch_classification.md. The load-bearing changes are:

  the wage bill base       a dose is now converted to dollars on FRED WASCUR national wages
                           and salaries, the base tau_l is built on. Round one used FRED COE
                           compensation of employees in the fiscal modules and this
                           project's occupational grid in the second-round module, which are
                           two different totals and neither matches tau_l's base.
  break-even tau_k         corrected to tau_l * (1 - R) for case A and to
                           tau_l * ((1 - R) * D + (W / Y) * dC) / (D - dC) for case B. Round
                           one divided a loss that already nets out tau_k by a surplus built
                           on a different wage bill, and the result broke the bound that a
                           break-even rate cannot exceed tau_l + g.
  HI payroll income        403.2bn from the 2026 Trustees summary tables, replacing 462.4bn,
                           which is HI TOTAL income including interest, government
                           contributions and premiums.
  HI payroll share         0.8720, its own, replacing the OASDI share of 0.9126 that was
                           being applied to both funds.
  OASDI payroll income     1,322.6bn published, replacing 1,323.2bn derived.

TOLERANCES, stated once and applied throughout:
    survey_relative   0.02   survey-based aggregates, for weight and vintage differences
    fit_relative      0.05   fitted coefficients
    share_absolute    0.01   ratios and shares
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"
# NOT data/release/. See the note in the module docstring: sealed values are withheld from a
# replicator by design and data/release/ is for material intended for publication.
SEALED = ROOT / "notes" / "sealed"

TOL = {"survey_relative": 0.02, "fit_relative": 0.05, "share_absolute": 0.01}


def v(value, tol, note):
    return {"expected": None if value is None or (isinstance(value, float)
                                                  and np.isnan(value)) else round(
        float(value), 6), "tolerance": tol, "note": note}


def main():
    SEALED.mkdir(parents=True, exist_ok=True)
    S = json.loads((OUT / "slack_reestimate.json").read_text())
    f = S["fits"]["rho_on_PRIME_AGE_nonemployment"]
    tk = json.loads((OUT / "tau_k_decomposition_summary.json").read_text())
    ur = pd.read_csv(OUT / "under_reporting_factors.csv").set_index("loan")
    cb = pd.read_csv(OUT / "credit_benchmarked.csv")
    cc = pd.read_csv(OUT / "oasdi_cap_contrast.csv")
    pc = pd.read_csv(OUT / "pay_control.csv")
    tf = pd.read_csv(OUT / "trust_fund_corrected.csv")
    fx = pd.read_csv(OUT / "fiscal_extended_axis.csv")
    fx = fx[(fx.tau_l == "bottom_up_0.301") & (fx.outlays == "no_outlays")
            & (fx.tau_k_reading == "barkai_rent_0.351") & (fx.rho_mode == "fitted")
            & (fx.horizon == 10)]

    def at(df, col, target, valcol):
        s = df[np.isclose(df[col], target, atol=0.03)]
        return float(s[valcol].mean()) if len(s) else np.nan

    sealed = {
        "_README": "Open this only AFTER rebuilding from notes/replication_brief.md. "
                   "Every entry is expected value, tolerance, and the construction's "
                   "identity. A rebuilt value outside tolerance means the claim resting "
                   "on it does not stand until the difference is explained.",
        "_tolerances": TOL,
        "rho_slack": {
            "intercept": v(f["intercept"], "fit_relative",
                           "rho = intercept + slope * prime-age nonemployment percent"),
            "slope": v(f["slope"], "fit_relative", "per percentage point of nonemployment"),
            "r_squared": v(f["r_squared"], "fit_relative", "n = 14 DWS vintages"),
            "n": v(f["n"], "share_absolute", "one observation per DWS vintage"),
            "x_range_low": v(f["x_range"][0], "fit_relative",
                             "below this the relation is extrapolated"),
            "x_range_high": v(f["x_range"][1], "fit_relative",
                              "above this the relation is extrapolated"),
        },
        "fiscal": {
            "R_2026": v(tk["R_2026"], "fit_relative", "R = rho * omega, retained wage share"),
            "tau_k_sourced_low": v(tk["tau_k_range_sourced_sigma"][0], "share_absolute",
                                   "Barkai rent share 0.351"),
            "tau_k_sourced_high": v(tk["tau_k_range_sourced_sigma"][1], "share_absolute",
                                    "Barkai rent share 0.351"),
            "tau_k_needed_bottom_up_0.301": v(
                tk["tau_k_needed_to_pass"]["bottom_up_0.301"], "share_absolute",
                "tau_k such that R = 1 - tau_k / tau_l holds with equality"),
            "tau_k_needed_AMR_0.255": v(tk["tau_k_needed_to_pass"]["AMR_0.255"],
                                        "share_absolute", "at the AMR reading of tau_l"),
            # CORRECTED in the final analysis session, item 5.1. The superseded note said
            # the required rate exceeds the TOP OF THE SOURCED RANGE at every reading. It
            # does not, and this project's own replication_r_sensitivity.json says so in
            # all five cells: the required rate maxes at 0.137276 against a sourced top of
            # 0.20351. The boolean is correct; the note overstated the finding.
            "condition_passes": {"expected": False, "tolerance": "exact",
                                 "note": "required tau_k of 0.110 to 0.137 exceeds the "
                                         "OPERATIVE effective rate of 0.0708 under every "
                                         "reading of tau_l, and does NOT exceed the top of "
                                         "the sourced range of 0.20351 under any reading. "
                                         "The condition is unclosable under the tax code "
                                         "as it stands, not under every reading of the "
                                         "literature."},
        },
        "fiscal_magnitudes": {
            "terminal_year_loss_bn_at_10pct": v(
                at(fx, "share_of_total_wage_bill", 0.10, "terminal_year_loss_bn"),
                "survey_relative", "annual flow in the terminal year, 10-year horizon, "
                                   "mean across exposure groups at this dose"),
            "terminal_year_loss_bn_at_25pct": v(
                at(fx, "share_of_total_wage_bill", 0.25, "terminal_year_loss_bn"),
                "survey_relative", "as above at a 25 percent dose"),
            "pct_of_receipts_at_10pct": v(
                at(fx, "share_of_total_wage_bill", 0.10, "terminal_pct_receipts"),
                "share_absolute", "against federal current receipts"),
            "pct_of_receipts_at_25pct": v(
                at(fx, "share_of_total_wage_bill", 0.25, "terminal_pct_receipts"),
                "share_absolute", "against federal current receipts"),
        },
        "trust_funds": {
            "OASDI_pct_of_payroll_income_at_10pct": v(
                at(tf, "share_of_total_wage_bill", 0.10,
                   "OASDI_loss_pct_of_fund_payroll_income"),
                "share_absolute", "denominator is FUND payroll income, not receipts"),
            "OASDI_pct_of_payroll_income_at_25pct": v(
                at(tf, "share_of_total_wage_bill", 0.25,
                   "OASDI_loss_pct_of_fund_payroll_income"), "share_absolute", ""),
            "HI_pct_of_payroll_income_at_10pct": v(
                at(tf, "share_of_total_wage_bill", 0.10,
                   "HI_loss_pct_of_fund_payroll_income"), "share_absolute",
                "HI has no earnings cap"),
            "grid_maximum_pct": v(
                float(max(tf["OASDI_loss_pct_of_fund_payroll_income"].max(),
                          tf["HI_loss_pct_of_fund_payroll_income"].max())),
                "share_absolute", "BOUND: must lie between 0 and 100"),
        },
        "under_reporting": {
            **{k: v(float(ur.loc[k, "UNDER_REPORTING_factor"]), "survey_relative",
                    "official aggregate over the FULL SIPP household universe")
               for k in ["mortgage", "card", "auto", "student"]},
            "coverage_share": {k: v(float(ur.loc[k, "working_core_share_of_full"]),
                                    "share_absolute",
                                    "working-core balance over the full universe")
                               for k in ["mortgage", "card", "auto", "student"]},
            "identity": "factor divided by coverage share reproduces the working-core "
                        "figure to three decimals",
        },
        "household_first_round": {},
        "cap_contrast": {},
        "pay_control": {},
        "incidence": {
            "household_count_spread_low": v(1.049, "share_absolute",
                                            "max over min on household COUNTS"),
            "household_count_spread_high": v(1.092, "share_absolute", ""),
            "dollar_spread_low": v(1.75, "share_absolute",
                                   "max over min on the DOLLARS those households owe"),
            "dollar_spread_high": v(3.01, "share_absolute", ""),
            "rule": "no dollar figure may be quoted without naming the incidence "
                    "assumption; the count figures are robust to it",
        },
    }
    for ln in ["mortgage", "card", "auto", "student"]:
        s = cb[(cb.loan == ln) & np.isclose(cb.share_of_wage_bill, 0.10)]
        if len(s):
            sealed["household_first_round"][f"{ln}_bank_loss_hi_bn_at_10pct"] = v(
                float(s["bank_loss_hi_bn"].iloc[0]), "survey_relative",
                "exposure at default times LGD times the bank-held share")
            sealed["household_first_round"][f"{ln}_pct_of_fed_at_10pct"] = v(
                float(s["pct_of_fed_hi"].iloc[0]), "share_absolute",
                "against the Fed severely adverse loss for that book")
    sealed["household_first_round"]["_scope"] = (
        "FIRST ROUND ONLY. House prices, consumer demand, business revenue and the "
        "employment of non-displaced workers are held fixed. Against the Fed's "
        "economy-wide scenario this is a LOWER BOUND, not an estimate.")
    for _, r in cc.iterrows():
        sealed["cap_contrast"].setdefault(r["dataset"], {})[r["group"]] = v(
            float(r["share_under_cap"]), "share_absolute",
            "share of the group's wage bill under the 184,500 dollar base")
    for _, r in pc.iterrows():
        key = f"{r['dataset']}_{r['statistic']}_{r['index']}"
        sealed["pay_control"][key] = {
            "raw_gap": v(float(r["raw_gap"]), "survey_relative", "embodied minus cognitive"),
            "share_of_gap_that_is_pay_a": v(float(r["share_of_gap_that_is_pay_a"]),
                                            "share_absolute",
                                            "cognitive reweighted to embodied pay"),
            "share_of_gap_that_is_pay_b": v(float(r["share_of_gap_that_is_pay_b"]),
                                            "share_absolute",
                                            "embodied reweighted to cognitive pay"),
        }
    sealed["pay_control"]["_finding"] = (
        "Neither exposure-type contrast survives the pay control. Between 1.0 and 11.4 "
        "percent of the raw gap remains at the weaker end, and the SIPP Eloundou GPT cap "
        "contrast reverses sign. Report a PAY mechanism with an exposure-type CORRELATE.")


    # ---- sections 10 to 13, added in the closing session
    try:
        K = pd.read_csv(OUT / "sovereign_consolidation.csv")
        sealed["sovereign"] = {
            "federal_share_first_round_min": v(float(K["federal_share_first_round"].min()),
                                               "share_absolute",
                                               "federal over federal plus private, "
                                               "first-round column"),
            "federal_share_first_round_max": v(float(K["federal_share_first_round"].max()),
                                               "share_absolute", ""),
            "federal_share_with_second_round_min": v(
                float(K["federal_share_with_second_round"].min()), "share_absolute",
                "the second round raises the total and LOWERS the federal share"),
            "federal_share_with_second_round_max": v(
                float(K["federal_share_with_second_round"].max()), "share_absolute", ""),
            "federal_student_share": v(1605.134 / 1650.0, "share_absolute",
                                       "FRED FGCCSAQ027S over the NY Fed total"),
            "_ordering": "CRT and private mortgage insurance are LOSS TRANSFERS taken "
                         "BEFORE Enterprise capital, not additions to it",
        }
    except FileNotFoundError:
        pass
    try:
        V = pd.read_csv(OUT / "second_round_sensitivity.csv")
        cs = json.loads((OUT / "consistency_summary.json").read_text())
        sealed["second_round"] = {
            "bank_losses_bn_min": v(float(V["bank_losses_bn"].min()), "survey_relative",
                                    "50 percent cognitive AIOE dose, across all sourced "
                                    "input combinations"),
            "bank_losses_bn_max": v(float(V["bank_losses_bn"].max()), "survey_relative", ""),
            "bank_losses_bn_median": v(float(V["bank_losses_bn"].median()),
                                       "survey_relative", ""),
            "house_price_fall_pct_min": v(float(V["house_price_fall_pct"].min()),
                                          "share_absolute", "income elasticity 0.21"),
            "house_price_fall_pct_max": v(float(V["house_price_fall_pct"].max()),
                                          "share_absolute", "income elasticity 1.50"),
            "demand_event_first_share": v(float(V["demand_event_first"].mean()),
                                          "share_absolute",
                                          "share of combinations in which demand severity "
                                          "exceeds house price severity"),
            "_verdict": cs["demand_event_first_verdict"],
            "_dominant_input": "the MPC gap explains about 0.95 of the variance of the "
                               "demand severity; the house price elasticity explains 0.998 "
                               "of the variance of the house price fall",
        }
        sealed["cases"] = {
            "case_B_over_A_min": v(cs["case_B_over_A_range"][0], "share_absolute",
                                   "fiscal loss under case B over case A"),
            "case_B_over_A_max": v(cs["case_B_over_A_range"][1], "share_absolute", ""),
            "break_even_tau_k_case_A_min": v(cs["break_even_tau_k_case_A"][0],
                                             "share_absolute",
                                             "tau_l * (1 - R), at the highest R on the grid"),
            "break_even_tau_k_case_A_max": v(cs["break_even_tau_k_case_A"][1],
                                             "share_absolute",
                                             "tau_l * (1 - R) at R = 0, so it equals tau_l "
                                             "exactly. BOUND: cannot exceed tau_l + g"),
            "break_even_tau_k_case_B_min": v(cs["break_even_tau_k_case_B"][0],
                                             "share_absolute",
                                             "tau_l * ((1 - R) * D + (W / Y) * dC) "
                                             "/ (D - dC)"),
            "break_even_tau_k_case_B_max": v(cs["break_even_tau_k_case_B"][1],
                                             "share_absolute",
                                             "BOUND: may exceed tau_l, because the base "
                                             "shrinks as the loss grows, but not 1"),
            "_definition_case_A": "tau_l * (1 - R)",
            "_definition_case_B": "tau_l * ((1 - R) * D + (W / Y) * dC) / (D - dC), where D "
                                  "is the gross displaced wage bill and dC the demand "
                                  "shortfall",
            "_bounds": "0 <= case A <= tau_l + g; 0 <= either case <= 1; case B >= case A; "
                       "D - dC > 0",
            "_withdrawn_round1": "the round-one values 0.213835 to 0.378371 (case A) and "
                                 "0.560866 to 0.860022 (case B) are WITHDRAWN. They divided "
                                 "a loss that already nets out tau_k by a surplus built on a "
                                 "different wage bill total, and the case A maximum broke "
                                 "the tau_l + g bound, which is how the replicator caught it",
            "_rule": "every fiscal figure published before the closing session is a CASE A "
                     "figure; case B is the internally consistent one whenever the "
                     "second-round module is quoted",
        }
        D = pd.read_csv(OUT / "debt_increments.csv")
        em = D[(D.regime == "emerging_market") & (D.horizon == 20)]
        sealed["debt"] = {
            "debt_to_gdp_start": v(cs["debt_to_gdp_start"], "share_absolute",
                                   "FRED GFDEBTN over GDP"),
            "baseline_20y_emerging_market": v(float(em["baseline_debt_to_gdp"].iloc[0]),
                                              "share_absolute",
                                              "NO DISPLACEMENT, r 9 percent against g 3"),
            "increment_pp_at_10pct_reserve_currency_20y": v(float(
                D[(D.regime == "reserve_currency") & (D.horizon == 20)
                  & np.isclose(D.dose, 0.10) & (D.case == "B")]["INCREMENT_pp_of_gdp"].mean()),
                "survey_relative", "case B"),
            "increment_pp_at_10pct_emerging_market_20y": v(float(
                D[(D.regime == "emerging_market") & (D.horizon == 20)
                  & np.isclose(D.dose, 0.10) & (D.case == "B")]["INCREMENT_pp_of_gdp"].mean()),
                "survey_relative", "case B"),
            "_withdrawn": "A91's 389 percent at a 10 percent dose is WITHDRAWN as a "
                          "statement about automation: it is almost entirely the "
                          "no-displacement baseline compounding at r above g",
        }
    except FileNotFoundError:
        pass

    sealed["_round"] = {
        "round": 2,
        "brief": "notes/replication_brief_v2.md",
        "round_1_frozen_at": "notes/sealed/sealed_expected_values_round1_ARCHIVED.json",
        "round_1_outcome": "21 of 51 attempted quantities matched. The 30 mismatches are "
                           "classified in notes/replication/round1_mismatch_classification.md.",
        "wage_bill_base_bn": json.loads(
            (OUT / "capacities.json").read_text())["national_wage_bill_bn"],
        "wage_bill_base": "FRED WASCUR, national wages and salaries",
        "not_in": "this file must never be placed in notes/replication/, which is the "
                  "replicator's own folder",
    }
    p = SEALED / "sealed_expected_values_round2.json"
    p.write_text(json.dumps(sealed, indent=2, default=str))
    n = json.dumps(sealed).count('"expected"')
    print(f"=== SEALED EXPECTED VALUES, ROUND TWO, written to {p.relative_to(ROOT)} ===")
    print(f"  {n} sealed quantities, each with a tolerance.")
    print("  Round one stays frozen at "
          "notes/sealed/sealed_expected_values_round1_ARCHIVED.json.")
    print("  A fresh instance rebuilds from notes/replication_brief_v2.md and opens this "
          "only after.")
    for sec in ["rho_slack", "fiscal", "fiscal_magnitudes", "trust_funds",
                "under_reporting", "household_first_round", "cap_contrast",
                "pay_control", "incidence", "sovereign", "second_round", "cases",
                "debt"]:
        if sec not in sealed:
            continue
        print(f"    {sec}")


if __name__ == "__main__":
    main()
