"""Item 6: SEALED EXPECTED VALUES for the replication brief.

Writes data/release/sealed_expected_values.json, the file a fresh instance opens only AFTER
rebuilding the quantities in notes/replication_brief.md from raw data. It carries the
expected value, the tolerance and the construction's one-line identity, and nothing that
would let a replicator shortcut the rebuild.

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
REL = ROOT / "data" / "release"

TOL = {"survey_relative": 0.02, "fit_relative": 0.05, "share_absolute": 0.01}


def v(value, tol, note):
    return {"expected": None if value is None or (isinstance(value, float)
                                                  and np.isnan(value)) else round(
        float(value), 6), "tolerance": tol, "note": note}


def main():
    REL.mkdir(parents=True, exist_ok=True)
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
            "condition_passes": {"expected": False, "tolerance": "exact",
                                 "note": "required tau_k exceeds the top of the sourced "
                                         "range at every reading of tau_l"},
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
                                             "share_absolute", "tau_l times (1 - R)"),
            "break_even_tau_k_case_A_max": v(cs["break_even_tau_k_case_A"][1],
                                             "share_absolute", ""),
            "break_even_tau_k_case_B_min": v(cs["break_even_tau_k_case_B"][0],
                                             "share_absolute",
                                             "loss B over a surplus reduced by the demand "
                                             "shortfall"),
            "break_even_tau_k_case_B_max": v(cs["break_even_tau_k_case_B"][1],
                                             "share_absolute", ""),
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

    p = REL / "sealed_expected_values.json"
    p.write_text(json.dumps(sealed, indent=2, default=str))
    n = json.dumps(sealed).count('"expected"')
    print(f"=== SEALED EXPECTED VALUES written to {p.relative_to(ROOT)} ===")
    print(f"  {n} sealed quantities across 8 sections, each with a tolerance.")
    print("  A fresh instance rebuilds from notes/replication_brief.md and opens this "
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
