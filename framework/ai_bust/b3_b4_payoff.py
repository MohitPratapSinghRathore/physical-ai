"""MODULE B3 and B4. The bust fed through the same household engine and fiscal module that
displacement uses, and the payoff table by holder rebuilt for three outcomes.

The point of B3 is symmetry of treatment. Until now the AI-fails case was assessed against
two historical analogues while the displacement case went through a household engine, a
fiscal module and, since Module A, 8,612 balance sheets. That asymmetry flattered the
AI-fails case, because a qualitative analogue cannot show damage to the wage side. Here the
bust's unemployment path is converted into the engine's own units and run the same way.

THE CONVERSION, stated because everything downstream rests on it. B2 gives a rise in the
unemployment rate in percentage points. The engine's axis is the share of the TOTAL WAGE
BILL displaced. A rise of u percentage points removes approximately u percent of employment,
and at average wages that is u percent of the wage bill. This assumes the newly unemployed
earn the average wage. In a bust concentrated in AI-adjacent and professional sectors they
earn ABOVE average, so this UNDERSTATES the wage-bill effect; it is a lower bound and is
labelled one.

THE FISCAL SIDE uses the VERIFIED historical receipts falls rather than our own arithmetic,
because those are measured: federal receipts fell 9.52 percent in 2000 to 2002 and 15.97
percent in 2007 to 2009, and corporate tax receipts fell 35.1 and 53.4 percent.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
PROC = Path(__file__).resolve().parents[2] / "data" / "processed"
LB = Path(__file__).resolve().parents[1] / "labor_backing"
INST = Path(__file__).resolve().parents[1] / "institutions"


def main():
    B2 = pd.read_csv(HERE / "b2_transmission.csv")
    A = pd.read_csv(LB / "historical_anchors.csv").set_index("anchor")
    tsb = json.loads((LB / "two_sided_bet.json").read_text())
    fp = json.loads((PROC / "fiscal_persistence_summary.json").read_text())
    receipts = fp["federal_receipts_bn"]
    cap = json.loads((PROC / "capacities.json").read_text())
    wage_bill = cap["national_wage_bill_bn"]

    # ---------------------------------------------------------------- B3
    anchor_for = {"equity-led, bounded by 2000 to 2002": "2000_to_2002_equity_financed",
                  "credit-led, bounded by 2007 to 2009": "2007_to_2009_debt_financed"}
    b3 = []
    for scen, grp in B2.groupby("scenario"):
        lo, hi = grp.unemployment_rise_pp.min(), grp.unemployment_rise_pp.max()
        a = A.loc[anchor_for[scen]]
        for tag, u in [("low", lo), ("high", hi)]:
            dose_equiv = u / 100.0                    # pp of unemployment -> share of wages
            wage_loss = dose_equiv * wage_bill
            # first-round household credit losses: the engine's own 10 pct dose scaled down
            D = pd.read_csv(PROC / "dose_response_first_round.csv")
            d10 = D[(np.isclose(D.dose_share_of_total_wage_bill, 0.10))
                    & (D.exposure_type == "cognitive_AIOE")]
            scale = dose_equiv / 0.10
            hh = {
                "mortgage_bn": float(d10.mortgage_national_loss_hi_bn.max()) * scale,
                "card_bn": float(d10.card_consumer_lenders_loss_hi_bn.max()) * scale,
                "auto_bn": float(d10.auto_lenders_loss_hi_bn.max()) * scale,
                "student_bn": float(d10.student_loan_holders_loss_hi_bn.max()) * scale,
            }
            b3.append({
                "scenario": scen, "band": tag,
                "unemployment_rise_pp": round(u, 3),
                "wage_bill_dose_equivalent": round(dose_equiv, 5),
                "wage_bill_dose_equivalent_pct": round(100 * dose_equiv, 3),
                "wage_income_loss_bn": round(wage_loss, 1),
                "household_credit_loss_bn": round(sum(hh.values()), 2),
                **{k: round(v, 2) for k, v in hh.items()},
                # fiscal, from the VERIFIED episode
                "federal_receipts_fall_pct_VERIFIED": float(a.federal_receipts_fall_pct),
                "federal_receipts_fall_bn": round(
                    receipts * float(a.federal_receipts_fall_pct) / 100, 1),
                "corporate_tax_fall_pct_VERIFIED": float(a.corporate_tax_fall_pct),
                "ai_debt_impaired_bn": float(grp.ai_debt_impaired_bn.max()),
            })
    B3 = pd.DataFrame(b3)
    B3.to_csv(HERE / "b3_bust_through_engine.csv", index=False)

    # ---------------------------------------------------------------- B4 payoff table
    W = tsb["wage_leg"]["by_holder_share"]
    Adf = pd.read_csv(LB / "two_sided_bet_by_holder.csv")
    ai = Adf[np.isclose(Adf.ai_equity_share_scenario, 0.2)].set_index("holder")

    worst = B3.loc[B3.federal_receipts_fall_bn.idxmin()]    # most negative
    rows = []
    for h, wshare in W.items():
        ashare = float(ai.loc[h, "ai_leg_share"]) if h in ai.index else 0.0
        rows.append({
            "holder": h,
            "wage_leg_share": round(wshare, 4),
            "ai_leg_share": round(ashare, 4),
            # AI FAILS: loses on the AI leg, AND loses on the wage side via the bust
            "ai_fails_wage_leg_effect": "LOSS, small: bust costs "
                                        f"{worst.wage_bill_dose_equivalent_pct:.2f} pct of "
                                        "the wage bill",
            "ai_fails_ai_leg_effect": "LOSS, large",
            # PARTIAL: both impaired
            "partial_success": "LOSS on the wage leg, LOSS on the AI leg",
            # SUCCESS: wage leg impaired, AI leg pays
            "success": "LOSS on the wage leg, GAIN on the AI leg",
            "net_ai_fails": round(-(0.01 * wshare + 1.00 * ashare), 4),
            "net_partial": round(-(0.50 * wshare + 0.50 * ashare), 4),
            "net_success": round(-(1.00 * wshare) + (1.00 * ashare), 4),
        })
    P = pd.DataFrame(rows).sort_values("wage_leg_share", ascending=False)
    P.to_csv(HERE / "b4_payoff_by_holder.csv", index=False)

    summ = {
        "status": "SCENARIO throughout; the fiscal falls are VERIFIED historical episodes",
        "conversion": "unemployment pp -> share of wage bill, one for one, a LOWER bound "
                      "because a bust falls on above-average earners",
        "bust_wage_bill_dose_equivalent_pct": [
            round(float(B3.wage_bill_dose_equivalent_pct.min()), 3),
            round(float(B3.wage_bill_dose_equivalent_pct.max()), 3)],
        "compare_displacement_headline_dose_pct": 10.0,
        "ratio": round(10.0 / float(B3.wage_bill_dose_equivalent_pct.max()), 1),
        "household_credit_loss_bn_range": [
            round(float(B3.household_credit_loss_bn.min()), 2),
            round(float(B3.household_credit_loss_bn.max()), 2)],
        "federal_receipts_fall_bn_range": [
            round(float(B3.federal_receipts_fall_bn.min()), 1),
            round(float(B3.federal_receipts_fall_bn.max()), 1)],
        "THE_FINDING": None,
        "disjointness_verdict": None,
    }
    mx = float(B3.wage_bill_dose_equivalent_pct.max())
    summ["THE_FINDING"] = (
        f"An AI bust damages the wage side, but on these assumptions by "
        f"{B3.wage_bill_dose_equivalent_pct.min():.2f} to {mx:.2f} percent of the wage "
        f"bill, which is {10.0/mx:.0f} to "
        f"{10.0/float(B3.wage_bill_dose_equivalent_pct.min()):.0f} times SMALLER than the "
        "10 percent displacement case. Household credit losses are "
        f"{B3.household_credit_loss_bn.min():.1f} to "
        f"{B3.household_credit_loss_bn.max():.1f}bn against 30.7bn at the 10 percent dose. "
        "BUT the FISCAL hit is large and comes from the other side of the budget: federal "
        f"receipts fall {B3.federal_receipts_fall_bn.min():.0f} to "
        f"{B3.federal_receipts_fall_bn.max():.0f}bn on the verified historical episodes, "
        "driven by capital gains and corporate tax rather than by wages.")
    summ["federal_position_correction"] = (
        "THE PAYOFF TABLE UNDERSTATES THE FEDERAL POSITION IN THE AI-FAILS COLUMN, and the "
        "reason matters. The table scores each holder by what it HOLDS. The federal "
        "government holds 1.0 percent of the AI leg, so it scores as barely exposed when AI "
        "fails. But B3 shows federal receipts falling 569 to 955bn in a bust, through "
        "capital gains and corporate tax. **The state's claim on the AI upside is fiscal, "
        "not proprietary: it is the capital tax, which is exactly the contested rate of "
        "section 5.1.** So the state is exposed to an AI bust roughly in proportion to how "
        "much of the AI surplus it taxes, and at the operative 0.0708 that exposure is "
        "small, which is the same fact as being unhedged on the upside. A holder-share "
        "table cannot show this and the paper must say so in words beside it.")
    summ["disjointness_verdict"] = (
        "The claim that the instrument sets are NEARLY DISJOINT across the two failure "
        "directions SURVIVES, but it must be narrowed and the reason changes. It is not "
        "that a bust leaves the wage side untouched: it does touch it, and B3 sizes that. "
        "It is that the bust reaches the wage side through a channel one to two orders of "
        "magnitude smaller than displacement does, while reaching the FEDERAL BUDGET "
        "through capital gains and corporate receipts, which displacement barely touches. "
        "So the two failure directions hit the same institution, the federal government, "
        "through DIFFERENT TAX BASES. Instruments that protect the wage tax base do not "
        "protect the capital tax base and the reverse. That is a sharper and more "
        "defensible claim than disjointness of instrument SETS.")
    (HERE / "b3_b4_summary.json").write_text(json.dumps(summ, indent=2, default=str))

    pd.set_option("display.width", 230)
    print("B3. THE BUST IN THE ENGINE'S OWN UNITS")
    print(B3[["scenario", "band", "unemployment_rise_pp",
              "wage_bill_dose_equivalent_pct", "wage_income_loss_bn",
              "household_credit_loss_bn", "federal_receipts_fall_pct_VERIFIED",
              "federal_receipts_fall_bn"]].to_string(index=False))
    print("\nB4. PAYOFF BY HOLDER, AI equity at the central 20 pct scale")
    print(P[["holder", "wage_leg_share", "ai_leg_share", "net_ai_fails",
             "net_partial", "net_success"]].to_string(index=False))
    print("\nTHE FINDING\n  " + summ["THE_FINDING"])
    print("\nDISJOINTNESS\n  " + summ["disjointness_verdict"])


if __name__ == "__main__":
    main()
