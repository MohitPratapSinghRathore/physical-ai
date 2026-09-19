"""Item 1: the DOSE-RESPONSE TABLE, which replaces the order of stress.

WHY THE RANKING IS RETIRED. A82 ranked balance sheets by which crossed its materiality
threshold first, and then showed that only 4 of 15 pairwise comparisons survived moving the
thresholds. That is not a marginal robustness failure, it is a sign that the question was
badly posed: each sheet is measured against a different yardstick, so the ranking is mostly
a fact about the yardsticks. A supervisor does not need to know which sheet crosses first.
They need to know, at a given dose, how large the loss is on each sheet, and how large it is
relative to what that sheet can absorb. That is a dose-response table.

WHAT EACH CELL REPORTS, for every balance sheet:

    loss in dollars            the incremental annual loss in the terminal year
    as a share of GDP          nominal GDP, FRED
    as a share of capacity     that sheet's own absorbing capacity, from src/capacity.py,
                               where the capacity measure is stated and sourced

ROWS: displacement as a share of the TOTAL wage bill (5, 10, 25, 50, 75 percent), by horizon
(2, 5, 10, 20 years), by exposure type (embodied, cognitive AIOE, cognitive GPT) and by
incidence case (incumbents, entrants, sourced mix).

THE FOUR ORDERINGS THAT WERE INVARIANT are kept as a footnote and nothing more: the mortgage
sheet crosses before the public budget, before student loans and before the trust funds, and
the public budget crosses before student loans. The other eleven comparisons were fragile
and are not ranked.

EVERY ROW STATES WHETHER IT IS INSIDE THE OBSERVED DATA RANGE (item 6). The flag comes from
the fiscal axis, where a scenario is outside the data when its terminal prime-age
nonemployment rate exceeds anything in the fitted sample.

METHOD, and what it is not.

  Credit losses are EXPOSURE AT DEFAULT times LOSS GIVEN DEFAULT, not exposure at default
  times a portfolio loss rate. The second form double counts the probability of default and
  is what made A75 understate the losses by a factor of 21.7. The exposure at default comes
  from the hand check in src/verify/, the default uplift from Gerardi, Herkenhoff, Ohanian
  and Willen, and the balances are scaled by the CORRECTED full-universe under-reporting
  factors (item 2), not A80's working-core factors.

  FIRST ROUND ONLY. Business credit, commercial real estate and the aggregate bank capital
  row are reported as ZERO in this table, and that zero is a statement about the engine, not
  about the world. The household engine holds house prices, consumer demand, business
  revenue and the employment of non-displaced workers fixed. Those channels are what item 4
  adds, in the second set of columns.

  EXPOSURE TYPE AND INCIDENCE enter the credit rows as MULTIPLIERS taken from the incidence
  run, applied to the per-level exposure at default. FLAGGED as an approximation: the
  per-level hand check is not itself run separately for each of the nine exposure-by-
  incidence combinations, so the level effect and the composition effect are treated as
  separable. The multipliers are reported alongside the table so the approximation is
  visible.

  COGNITIVE EXPOSURE MEASURES TASK OVERLAP, NOT DISPLACEMENT OR TIMING. The top quintile of
  either cognitive index contains a great deal of work that is more likely to be augmented
  than replaced. Every cognitive row in this table is a scenario about a dose, not a
  forecast that the dose will arrive.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

WB_LEVELS = [0.05, 0.10, 0.25, 0.50, 0.75]
HORIZONS = [2, 5, 10, 20]
TYPES = ["embodied", "cognitive_AIOE", "cognitive_GPT"]
CASES = ["a_incumbents", "b_entrants", "c_sourced_mix"]

# HOLDER DECOMPOSITION OF THE 13,100bn NATIONAL MORTGAGE BALANCE (NY Fed HHDC 2026Q2).
# This replaces the flagged 60 to 70 percent agency range used earlier. Three of the four
# shares are now read from a publisher.
#   GSE        6,694bn, 51.1 percent. Fannie Mae's single-family conventional guaranty book
#              is 3,538bn (its 2025 Form 10-K reports 1,663bn of credit-enhanced loans at 47
#              percent of the book) and Freddie Mac's single-family portfolio is 3,156bn
#              ("our Single-Family mortgage portfolio was $3.2 trillion at December 31,
#              2025", Table: total 3,156,290m).
#   FHA        1,647bn, 12.6 percent. FLAGGED PROXY, see lit/unverified.md: hud.gov is 403.
#   bank       1,500bn, 11.5 percent. The Federal Reserve's 2026 DFAST first-lien balance.
#   residual   3,259bn, 24.9 percent: VA, private label, credit unions and portfolio
#              lenders outside the DFAST panel. FLAGGED as a residual, not a measurement.
MORTGAGE_BALANCE_BN = 13_100.0
MORTGAGE_BANK_HELD = 1_500.0 / MORTGAGE_BALANCE_BN
MORTGAGE_GSE_SHARE = 6_694.0 / MORTGAGE_BALANCE_BN
MORTGAGE_FHA_SHARE = 1_647.0 / MORTGAGE_BALANCE_BN
MORTGAGE_RESIDUAL_SHARE = 1.0 - MORTGAGE_BANK_HELD - MORTGAGE_GSE_SHARE - MORTGAGE_FHA_SHARE
AGENCY_SHARE = (MORTGAGE_GSE_SHARE, MORTGAGE_GSE_SHARE)
RENT_NONPAYMENT = (0.25, 0.50)   # FLAGGED, share of lost renter wage income that becomes
                                 # arrears rather than being met from savings or transfers

INVARIANT_ORDERINGS = [
    "mortgage before public budget",
    "mortgage before student loans",
    "mortgage before trust funds",
    "public budget before student loans",
]


def multipliers():
    """Exposure-type and incidence multipliers on exposure at default, normalised so the
    mean across the nine combinations is one for each loan type."""
    inc = pd.read_csv(OUT / "incidence_defaults.csv")
    cols = {"mortgage": "exposure_mortgage_bn", "student": "exposure_student_bn",
            "auto": "exposure_vehicle_bn", "card": "exposure_card_bn"}
    M = {}
    for loan, c in cols.items():
        mean = inc[c].mean()
        for _, r in inc.iterrows():
            M[(r["exposure"], r["case"], loan)] = r[c] / mean
    return M, inc


def inside_flags():
    """For each exposure type, horizon and dose, whether the scenario sits inside the
    observed data range. Carried from the fiscal axis, which flags a scenario as outside
    when its terminal prime-age nonemployment rate exceeds the fitted sample."""
    fx = pd.read_csv(OUT / "fiscal_extended_axis.csv")
    fx["type"] = fx["group"].str.replace(r"_top\d+", "", regex=True)
    fx = fx[fx["type"].isin(TYPES)]
    flags, chosen = {}, {}
    for t in TYPES:
        g = fx[fx["type"] == t]
        for wb in WB_LEVELS:
            # The smallest scenario of this type that DELIVERS AT LEAST the target dose.
            # Choosing the nearest dose in either direction would silently report a
            # smaller shock than the row claims, so the rule is one-sided; where no
            # scenario of this type reaches the target the largest one is taken and the
            # row is flagged SATURATED.
            up = g[g["share_of_total_wage_bill"] >= wb]
            src = up if len(up) else g
            col = "share_of_total_wage_bill"
            key = (src.nsmallest(1, col) if len(up) else src.nlargest(1, col))[
                ["group", "level_of_exposed", col]].iloc[0]
            chosen[(t, wb)] = (key["group"], key["level_of_exposed"],
                               key["share_of_total_wage_bill"])
            sel = g[(g["group"] == key["group"])
                    & (g["level_of_exposed"] == key["level_of_exposed"])]
            for h in HORIZONS:
                s = sel[sel["horizon"] == h]
                flags[(t, wb, h)] = (not bool(s["outside_data"].any())) if len(s) else None
    return flags, chosen, fx


def build():
    cap = json.loads((OUT / "capacities.json").read_text())
    gdp = cap["gdp_bn"]
    C = cap["sheets"]
    cb = pd.read_csv(OUT / "credit_benchmarked.csv")
    tf = pd.read_csv(OUT / "trust_fund_corrected.csv")
    tf["type"] = tf["group"].str.replace(r"_top\d+", "", regex=True)
    M, inc = multipliers()
    flags, chosen, fx = inside_flags()

    rows = []
    for t in TYPES:
        for wb in WB_LEVELS:
            grp, lvl, actual = chosen[(t, wb)]
            # --- fiscal rows, by horizon, on the same chosen scenario
            fsel = fx[(fx["group"] == grp) & (fx["level_of_exposed"] == lvl)
                      & (fx["rho_mode"] == "fitted")
                      & (fx["tau_l"] == "bottom_up_0.301")
                      & (fx["outlays"] == "no_outlays")
                      & (fx["tau_k_reading"] == "barkai_rent_0.351")]
            tsel = tf[(tf["group"] == grp) & (tf["level_of_exposed"] == lvl)]
            oasdi_pct = float(tsel["OASDI_loss_pct_of_fund_payroll_income"].mean()) / 100.0
            hi_pct = float(tsel["HI_loss_pct_of_fund_payroll_income"].mean()) / 100.0
            for h in HORIZONS:
                fh = fsel[fsel["horizon"] == h]
                budget_loss = float(fh["terminal_year_loss_bn"].mean()) if len(fh) else np.nan
                for case in CASES:
                    r = {"exposure_type": t, "incidence": case,
                         "dose_share_of_total_wage_bill": wb,
                         "dose_actual_on_chosen_group": actual,
                         "chosen_group": grp, "level_of_exposed": lvl,
                         "horizon_years": h,
                         "inside_observed_data_range": flags[(t, wb, h)],
                         # ATTAINABILITY. The broadest definition of an exposure type has a
                         # maximum dose: displacing every worker in the top half of the
                         # embodiment index is 33.7 percent of the total wage bill and no
                         # more. Where the target dose exceeds that maximum the row is
                         # SATURATED: the loss shown is the loss at the largest attainable
                         # dose for that exposure type, not at the target.
                         "dose_attainable": bool(actual >= 0.95 * wb),
                         "dose_shortfall": max(0.0, wb - actual)}
                    # --- public budget
                    add(r, "public_budget", budget_loss, budget_loss, gdp,
                        C["public_budget"]["capacity_bn"])
                    # --- trust funds, scaled to dollars on their own income base
                    add(r, "oasdi", oasdi_pct * C["oasdi"]["capacity_bn"],
                        oasdi_pct * C["oasdi"]["capacity_bn"], gdp,
                        C["oasdi"]["capacity_bn"])
                    add(r, "hi", hi_pct * C["hi"]["capacity_bn"],
                        hi_pct * C["hi"]["capacity_bn"], gdp, C["hi"]["capacity_bn"])
                    # --- credit sheets
                    for loan, sheet in [("mortgage", None), ("auto", "auto_lenders"),
                                        ("card", "card_consumer_lenders"),
                                        ("student", "student_loan_holders")]:
                        s = cb[(cb["loan"] == loan)
                               & np.isclose(cb["share_of_wage_bill"], wb)]
                        if not len(s):
                            continue
                        mult = M[(t, case, loan)]
                        lo = float(s["bank_loss_lo_bn"].iloc[0]) * mult
                        hi = float(s["bank_loss_hi_bn"].iloc[0]) * mult
                        if loan == "mortgage":
                            # bank-held is what credit_benchmarked already carries; the
                            # rest of the national balance is split agency against other
                            # holders across the FLAGGED agency share
                            add(r, "mortgage_bank_held", lo, hi, gdp,
                                C["mortgage_bank_held"]["capacity_bn"])
                            tot_lo = lo / MORTGAGE_BANK_HELD
                            tot_hi = hi / MORTGAGE_BANK_HELD
                            add(r, "mortgage_agency", tot_lo * MORTGAGE_GSE_SHARE,
                                tot_hi * MORTGAGE_GSE_SHARE, gdp,
                                C["mortgage_agency"]["capacity_bn"])
                            add(r, "mortgage_FHA", tot_lo * MORTGAGE_FHA_SHARE,
                                tot_hi * MORTGAGE_FHA_SHARE, gdp,
                                C["mortgage_agency_FHA"]["capacity_bn"])
                            r["mortgage_national_loss_lo_bn"] = tot_lo
                            r["mortgage_national_loss_hi_bn"] = tot_hi
                            r["mortgage_residual_holders_loss_hi_bn"] = (
                                tot_hi * MORTGAGE_RESIDUAL_SHARE)
                        else:
                            add(r, sheet, lo, hi, gdp, C[sheet]["capacity_bn"])
                    # --- landlords and multifamily: an arrears share, not a dollar capacity
                    arrears_lo, arrears_hi = wb * RENT_NONPAYMENT[0], wb * RENT_NONPAYMENT[1]
                    r["landlords_arrears_share_lo"] = arrears_lo
                    r["landlords_arrears_share_hi"] = arrears_hi
                    br = C["landlords_multifamily"]["breach_share_range"]
                    r["landlords_breaches_dscr_lo_D"] = arrears_hi >= br[1]
                    r["landlords_breaches_dscr_hi_D"] = arrears_hi >= br[0]
                    # --- channels the first round holds fixed, by construction
                    for sheet in ["business_credit", "commercial_real_estate",
                                  "bank_capital"]:
                        add(r, sheet, 0.0, 0.0, gdp, C[sheet]["capacity_bn"])
                    rows.append(r)
    D = pd.DataFrame(rows)
    return D, cap, M, inc, chosen


def add(r, sheet, lo, hi, gdp, capacity):
    r[f"{sheet}_loss_lo_bn"] = lo
    r[f"{sheet}_loss_hi_bn"] = hi
    r[f"{sheet}_pct_gdp_hi"] = 100 * hi / gdp
    r[f"{sheet}_pct_capacity_hi"] = (100 * hi / capacity) if capacity else np.nan


SHEETS = ["public_budget", "oasdi", "hi", "mortgage_agency", "mortgage_FHA",
          "mortgage_bank_held",
          "auto_lenders", "card_consumer_lenders", "student_loan_holders",
          "business_credit", "commercial_real_estate", "bank_capital"]


def main():
    D, cap, M, inc, chosen = build()
    D.round(5).to_csv(OUT / "dose_response_first_round.csv", index=False)
    pd.set_option("display.width", 260)

    print("=== DOSE-RESPONSE TABLE, FIRST ROUND. The ranking is retired. ===")
    print(f"  GDP denominator {cap['gdp_bn']:,.1f}bn. Capacity measures from "
          f"data/processed/capacities.json, each one sourced.")
    print("  Cognitive exposure measures TASK OVERLAP, not displacement or timing.")

    print("\n=== LOSS AS A SHARE OF EACH SHEET'S OWN ABSORBING CAPACITY, percent ===")
    print("    horizon 10 years, sourced-mix incidence, upper end of the loss band")
    v = D[(D.horizon_years == 10) & (D.incidence == "c_sourced_mix")]
    piv = v.pivot_table(index=["exposure_type", "dose_share_of_total_wage_bill"],
                        values=[f"{s}_pct_capacity_hi" for s in SHEETS])
    piv.columns = [c.replace("_pct_capacity_hi", "") for c in piv.columns]
    print(piv[SHEETS].round(2).to_string())

    print("\n=== THE SAME CELLS IN DOLLARS, billions, upper end ===")
    piv2 = v.pivot_table(index=["exposure_type", "dose_share_of_total_wage_bill"],
                         values=[f"{s}_loss_hi_bn" for s in SHEETS])
    piv2.columns = [c.replace("_loss_hi_bn", "") for c in piv2.columns]
    print(piv2[SHEETS].round(1).to_string())

    print("\n=== AND AS A SHARE OF GDP, percent ===")
    piv3 = v.pivot_table(index=["exposure_type", "dose_share_of_total_wage_bill"],
                         values=[f"{s}_pct_gdp_hi" for s in SHEETS])
    piv3.columns = [c.replace("_pct_gdp_hi", "") for c in piv3.columns]
    print(piv3[SHEETS].round(3).to_string())

    print("\n=== INSIDE THE OBSERVED DATA RANGE? by dose and horizon ===")
    ins = D.pivot_table(index=["exposure_type", "dose_share_of_total_wage_bill"],
                        columns="horizon_years", values="inside_observed_data_range",
                        aggfunc="first")
    print(ins.to_string())
    allrows = D["inside_observed_data_range"]
    print(f"\n  rows inside: {int(allrows.sum())} of {len(allrows)} "
          f"({allrows.mean():.0%})")
    for wb in WB_LEVELS:
        s = D[D.dose_share_of_total_wage_bill == wb]["inside_observed_data_range"]
        tag = ("FULLY INSIDE" if s.all() else
               "FULLY OUTSIDE" if not s.any() else "PARTLY INSIDE")
        print(f"    dose {wb:.0%}: {tag} ({s.mean():.0%} of rows inside)")

    print("\n=== IS THE TARGET DOSE ATTAINABLE FOR THAT EXPOSURE TYPE? ===")
    print("    the largest dose an exposure type can deliver is bounded by its own wage bill")
    at = D.drop_duplicates(["exposure_type", "dose_share_of_total_wage_bill"])
    for _, a in at.iterrows():
        if not a.dose_attainable:
            print(f"    {a.exposure_type:15s} target {a.dose_share_of_total_wage_bill:>4.0%}: "
                  f"SATURATED at {a.dose_actual_on_chosen_group:.1%} "
                  f"({a.chosen_group}, all workers). The cell is the loss at "
                  f"{a.dose_actual_on_chosen_group:.1%}, not at the target.")
    print(f"    saturated rows: {int((~D.dose_attainable).sum())} of {len(D)}")

    print("\n=== LANDLORDS AND MULTIFAMILY, arrears against debt service coverage ===")
    br = cap["sheets"]["landlords_multifamily"]["breach_share_range"]
    print(f"  breach at an arrears share of {br[0]:.1%} (D=1.35) to {br[1]:.1%} (D=1.20), "
          f"FLAGGED range")
    for wb in WB_LEVELS:
        s = D[D.dose_share_of_total_wage_bill == wb].iloc[0]
        print(f"    dose {wb:>4.0%}: arrears {s.landlords_arrears_share_lo:.1%} to "
              f"{s.landlords_arrears_share_hi:.1%}  "
              f"{'BREACHES at both D' if s.landlords_breaches_dscr_lo_D else ('breaches at D=1.20 only' if s.landlords_breaches_dscr_hi_D else 'no breach')}")

    print("\n=== EXPOSURE-TYPE AND INCIDENCE MULTIPLIERS on exposure at default ===")
    mm = pd.DataFrame([{"exposure": k[0], "case": k[1], "loan": k[2], "mult": v}
                       for k, v in M.items()])
    print(mm.pivot_table(index=["exposure", "case"], columns="loan",
                         values="mult").round(3).to_string())

    print("\n=== FOOTNOTE: the four orderings that were invariant in A82 ===")
    for o in INVARIANT_ORDERINGS:
        print(f"    {o}")
    print("  The other eleven pairwise comparisons were fragile and are NOT ranked.")

    print("\n=== WHAT THE FIRST ROUND HOLDS FIXED ===")
    print("  business credit, commercial real estate and aggregate bank capital are ZERO "
          "here\n  BY CONSTRUCTION. The engine holds house prices, consumer demand, business "
          "revenue\n  and the employment of non-displaced workers fixed. Item 4 adds them.")

    (OUT / "dose_response_summary.json").write_text(json.dumps({
        "sheets": SHEETS,
        "invariant_orderings": INVARIANT_ORDERINGS,
        "chosen_scenarios": {f"{k[0]}@{k[1]}": {"group": v[0], "level": v[1],
                                                "actual_dose": v[2]}
                             for k, v in chosen.items()},
        "saturated_rows": int((~D.dose_attainable).sum()),
        "rows_inside_data_range": int(D["inside_observed_data_range"].sum()),
        "rows_total": int(len(D)),
        "inside_by_dose": {f"{wb}": float(
            D[D.dose_share_of_total_wage_bill == wb]["inside_observed_data_range"].mean())
            for wb in WB_LEVELS},
        "flagged": {
            "holder_decomposition": {"gse": MORTGAGE_GSE_SHARE,
                                     "fha": MORTGAGE_FHA_SHARE,
                                     "bank_portfolio": MORTGAGE_BANK_HELD,
                                     "residual": MORTGAGE_RESIDUAL_SHARE},
            "rent_nonpayment": list(RENT_NONPAYMENT),
            "separability": "exposure-type and incidence enter as multipliers on the "
                            "per-level exposure at default; the level effect and the "
                            "composition effect are treated as separable",
        },
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
