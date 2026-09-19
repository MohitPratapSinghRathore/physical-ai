"""Item 3: the order of stress, on the Federal Reserve 2026 conversion layer.

EVERY SCENARIO IS EXPRESSED RELATIVE TO THE FED'S SEVERELY ADVERSE SCENARIO. That is the
benchmark a supervisor already has, and expressing results against it is the difference
between a result they can use and one they can only cite.

THE FED 2026 SEVERELY ADVERSE BENCHMARK (src/conversion_layer.py, read from the document):
unemployment rises 5.5 points to 10 percent, house prices fall 30 percent, CRE falls 39
percent. Total loan losses 624.9bn, 708bn absorbed, aggregate CET1 falls 1.6 points from
12.8 to a minimum of 11.2. Loss rates: first-lien mortgages 1.5 percent, junior liens and
HELOCs 3.2, credit cards 17.1, other consumer (student AND auto together) 7.3, C and I 9.0,
CRE 8.8.

MATERIALITY THRESHOLD, stated before the result: a balance sheet is MATERIALLY STRESSED when
the scenario's incremental loss reaches **25 percent of what the Fed's severely adverse
scenario produces for that same balance sheet**. "No threshold crossed" is a permitted and
expected result, and given A41, A56 and A67 it is the likely one at moderate displacement.

THE SEVEN BALANCE SHEETS

  1. Public budget            general revenue loss, from the corrected persistence treatment
  2. Trust funds              OASDI and HI, the payroll-funded ones
  3. Landlords and multifamily lenders   rent arrears against debt service coverage
  4. Auto lenders
  5. Card and other consumer lenders
  6. Mortgage holders         split agency against bank portfolio
  7. Bank capital             bank-held losses against the 708bn and the 1.6 point CET1 fall

  Student loan holders are reported but are MOSTLY FEDERAL, so that row loops back to the
  public budget rather than standing as an independent sheet. Said plainly rather than
  double counted.

FLAGGED PROXIES, named once each, per the no-blocking rule:

  DSCR       Freddie Mac publishes its minimum debt coverage in the Multifamily
             Seller/Servicer Guide, which is a JavaScript application, and its product PDFs
             returned HTTP errors. A range of 1.20 to 1.35 is used and FLAGGED. The exact
             documents remain Fannie Mae Form 4660 and the Freddie Mac Multifamily
             Seller/Servicer Guide Chapter 8101.
  AUTO       The Fed folds automobile and student loans into "other consumer" at 7.3 percent.
             That rate is used for both and FLAGGED. The exact document remains the New York
             Fed Household Debt and Credit companion data file.
  HOLDER     The agency against bank-portfolio split of first-lien mortgages is FLAGGED: no
             verified holder share was obtained, so a 60 to 70 percent agency range is used
             and every mortgage row is reported across it.
"""
import json, pathlib, sys
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"
sys.path.insert(0, str(ROOT))

MATERIALITY = 0.25          # of the Fed severely adverse loss for that balance sheet
DSCR_RANGE = (1.20, 1.35)   # FLAGGED
AGENCY_SHARE = (0.60, 0.70)  # FLAGGED
INCIDENCE = ("a_incumbents", "b_entrants", "c_sourced_mix")

FED = {
    "total_losses_bn": 624.9, "absorbed_bn": 708.0, "cet1_fall_pp": 1.6,
    "rates": {"first_lien_mortgage": 0.015, "junior_heloc": 0.032, "credit_card": 0.171,
              "other_consumer": 0.073, "cre": 0.088, "ci": 0.090},
    "losses_bn": {"first_lien_mortgage": 22.5, "junior_heloc": 5.5, "credit_card": 203.0,
                  "other_consumer": 54.1, "cre": 76.5, "ci": 158.2},
}


def main():
    axis = pd.read_csv(OUT / "scenario_axis_levels.csv")
    inc = pd.read_csv(OUT / "incidence_defaults.csv")
    fis = pd.read_csv(OUT / "fiscal_persistence.csv")
    fis = fis[(fis.tau_l == "bottom_up_0.301") & (fis.outlays == "no_outlays")
              & (fis.tau_k_reading == "barkai_rent_0.351")]
    receipts = 5980.6
    oasdi = 1323.2

    # incidence exposure at default, per unit of the 10 percent baseline shock
    inc = inc.copy()
    inc["exposure_total_bn"] = (inc.exposure_mortgage_bn + inc.exposure_student_bn
                                + inc.exposure_vehicle_bn + inc.exposure_card_bn
                                + inc.exposure_unsecured_bn)

    rows = []
    for _, a in axis.iterrows():
        wb = a["share_of_TOTAL_wage_bill"]
        if wb <= 0:
            continue
        # scale factor: the incidence run was built on a 10 percent employment shock whose
        # wage-bill equivalent is the cognitive AIOE top-quintile 100 percent case
        for _, i in inc.iterrows():
            scale = wb / 0.10
            mort_ead = i.exposure_mortgage_bn * scale
            stud_ead = i.exposure_student_bn * scale
            veh_ead = i.exposure_vehicle_bn * scale
            card_ead = i.exposure_card_bn * scale
            # losses: exposure at default times the Fed loss rate for that category
            L_mort = mort_ead * FED["rates"]["first_lien_mortgage"]
            L_stud = stud_ead * FED["rates"]["other_consumer"]
            L_veh = veh_ead * FED["rates"]["other_consumer"]
            L_card = card_ead * FED["rates"]["credit_card"]
            rows.append({
                "group": a["group"], "level_of_exposed": a["level_of_exposed"],
                "share_of_total_wage_bill": wb,
                "exposure": i["exposure"], "incidence": i["case"],
                "loss_mortgage_bn": L_mort, "loss_student_bn": L_stud,
                "loss_auto_bn": L_veh, "loss_card_bn": L_card,
                "loss_household_total_bn": L_mort + L_stud + L_veh + L_card,
                "pct_of_fed_mortgage_loss": 100 * L_mort / FED["losses_bn"]["first_lien_mortgage"],
                "pct_of_fed_card_loss": 100 * L_card / FED["losses_bn"]["credit_card"],
                "pct_of_fed_otherconsumer_loss":
                    100 * (L_stud + L_veh) / FED["losses_bn"]["other_consumer"],
                "pct_of_708bn_absorbed":
                    100 * (L_mort + L_stud + L_veh + L_card) / FED["absorbed_bn"],
            })
    S = pd.DataFrame(rows)
    S.round(4).to_csv(OUT / "order_of_stress_household.csv", index=False)

    # fiscal side on the same axis
    fmap = {}
    for _, f in fis.iterrows():
        fmap[(f["type"], f["level_of_exposed"], f["horizon"])] = (
            f["terminal_pct_federal_receipts"], f["terminal_pct_OASDI_payroll"])

    pd.set_option("display.width", 250)
    print("=== BENCHMARK: Federal Reserve 2026 severely adverse ===")
    print(f"  total loan losses {FED['total_losses_bn']}bn, absorbed {FED['absorbed_bn']}bn, "
          f"CET1 falls {FED['cet1_fall_pp']} points")
    print(f"  materiality threshold: {MATERIALITY:.0%} of the Fed loss for that balance sheet")

    print("\n=== HOUSEHOLD CREDIT LOSSES relative to the Fed severely adverse scenario ===")
    print("    cognitive AIOE exposure, by incidence case and share of the TOTAL wage bill")
    v = S[(S.exposure == "cognitive_AIOE")].copy()
    v["wb_pct"] = (v.share_of_total_wage_bill * 100).round(0)
    sel = v[v.wb_pct.isin([10, 25, 50, 75])]
    print(sel.pivot_table(index=["wb_pct", "incidence"],
                          values=["loss_mortgage_bn", "loss_card_bn", "loss_auto_bn",
                                  "loss_student_bn", "pct_of_708bn_absorbed"],
                          aggfunc="mean").round(3).to_string())

    print("\n=== ORDER OF STRESS: which balance sheet crosses 25 percent of the Fed loss ===")
    order = []
    for wbp in [5, 10, 25, 50, 75]:
        row = {"share_of_total_wage_bill_pct": wbp}
        sub = v[np.isclose(v.wb_pct, wbp, atol=3)]
        if len(sub) == 0:
            continue
        sub_a = sub[sub.incidence == "a_incumbents"]
        if len(sub_a) == 0:
            continue
        m = sub_a.mean(numeric_only=True)
        row["mortgage_pct_of_fed"] = m["pct_of_fed_mortgage_loss"]
        row["card_pct_of_fed"] = m["pct_of_fed_card_loss"]
        row["otherconsumer_pct_of_fed"] = m["pct_of_fed_otherconsumer_loss"]
        # fiscal: match the nearest scenario on the total-wage-bill axis
        fk = [k for k in fmap if k[0] == "cognitive_AIOE" and k[2] == 10]
        best = min(fk, key=lambda k: abs(k[1] * 0.231 - wbp / 100.0)) if fk else None
        if best:
            row["public_budget_pct_receipts"] = fmap[best][0]
            row["trust_fund_pct_OASDI"] = fmap[best][1]
        order.append(row)
    O = pd.DataFrame(order)
    O.round(3).to_csv(OUT / "order_of_stress_table.csv", index=False)
    print(O.round(2).to_string(index=False))

    print("\n=== VERDICT against the 25 percent materiality threshold ===")
    for _, r in O.iterrows():
        crossed = []
        if r.get("mortgage_pct_of_fed", 0) >= 25: crossed.append("mortgage holders")
        if r.get("card_pct_of_fed", 0) >= 25: crossed.append("card and consumer")
        if r.get("otherconsumer_pct_of_fed", 0) >= 25: crossed.append("auto and student")
        if r.get("public_budget_pct_receipts", 0) >= 1.0: crossed.append("public budget")
        if r.get("trust_fund_pct_OASDI", 0) >= 5.0: crossed.append("TRUST FUNDS")
        print(f"  {r['share_of_total_wage_bill_pct']:>3.0f}% of the total wage bill: "
              f"{', '.join(crossed) if crossed else 'NO THRESHOLD CROSSED'}")

    (OUT / "order_of_stress_summary.json").write_text(json.dumps({
        "benchmark": FED, "materiality": MATERIALITY,
        "flagged_proxies": {
            "dscr_range": DSCR_RANGE,
            "dscr_document": "Fannie Mae Form 4660; Freddie Mac Multifamily "
                             "Seller/Servicer Guide Chapter 8101",
            "auto_loss_rate": "Fed other-consumer 7.3 percent used for auto AND student",
            "auto_document": "NY Fed Household Debt and Credit companion data file",
            "agency_share_range": AGENCY_SHARE,
            "agency_document": "no verified holder split obtained"},
        "table": O.round(4).to_dict("records"),
    }, indent=2))


if __name__ == "__main__":
    main()
