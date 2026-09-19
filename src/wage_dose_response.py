"""Item 4: the dose-response table REORGANISED AROUND THE WAGE DISTRIBUTION, with the
exposure indices demoted to named scenarios.

THE DECISION, and it is a large one. Three separate findings in two sessions have shown that
what this project called an exposure-type effect is a pay effect:

    A87  the household distress-efficiency contrast: 93 to 98 percent is pay
    A87  the OASDI earnings cap contrast: 54 to 99 percent is pay, and one case reverses
    A89  the opposite-places geography result: the home-value correlation goes to zero once
         local mean wage is controlled

Three independent tests, two datasets, two cognitive indices and a geographic cross section
all point the same way. The organising dimension of the paper therefore becomes WHERE IN THE
WAGE DISTRIBUTION DISPLACEMENT FALLS, and the exposure indices become named scenarios that
say where a particular technology would put it.

WHAT THIS COSTS, stated plainly rather than buried.

  1. THE EMBODIED VERSUS COGNITIVE FRAMING IS DEMOTED. It was the organising idea of the
     project from the scope change onward. It survives as a mapping from a technology to a
     place in the wage distribution (A88: cognitive AIOE puts 71.3 percent of its wage bill
     in the top quintile; embodied spreads across Q2 to Q4), which is useful and is not
     nothing, but it is no longer a mechanism.

  2. PAEI IS NO LONGER A CONTRIBUTION IN ITS OWN RIGHT. The embodiment index was built for
     this project, validated, decomposed into three pathways and defended across several
     sessions. Under this reorganisation its role is to locate embodied work in the wage
     distribution, which a wage variable does directly. **The honest position is that PAEI
     is a measurement instrument this paper uses, not a finding this paper reports.** Its
     one surviving independent use is the driving pathway, which is a concentrated,
     identifiable, vehicle-credit-relevant group that no wage quintile picks out.

  3. THE COMPARATIVE THESIS GOES. "Physical AI and cognitive AI stress different balance
     sheets" is not supported once pay is controlled. What is supported is that displacement
     low in the wage distribution stresses the payroll-funded trust funds and thin household
     buffers, and displacement high in it stresses income tax receipts, and that different
     technologies land in different places.

WHAT IS GAINED. The wage quintile is observable, is in every household survey and every
administrative record, needs no index, needs no assumption about task overlap, and is
directly usable by a supervisor. **A stress-test designer can ask "what if 10 percent of the
wage bill goes, concentrated in the third quintile" without adopting any view about AI.**

METHOD. Exposure at default is the quintile's balance times the displaced fraction of that
quintile's workers times the Gerardi, Herkenhoff, Ohanian and Willen one-earner default
uplift of 5.0 percentage points. FLAGGED: the two-earner superadditive factor of 8.0 points
is NOT applied here because the quintile file does not carry within-household earner counts,
so these figures UNDERSTATE the correlated-displacement case. Losses are exposure at default
times loss given default, never times a portfolio loss rate. Balances carry the corrected
full-universe under-reporting factors.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

GHOW_ONE_EARNER = 0.050
LGD = {"mortgage": (0.25, 0.40), "card": (0.80, 1.00),
       "auto": (0.45, 0.65), "student": (0.75, 1.00)}
MORTGAGE_BALANCE_BN = 13_100.0
HOLDER = {"gse": 6_694.0 / MORTGAGE_BALANCE_BN, "fha": 1_647.0 / MORTGAGE_BALANCE_BN,
          "bank": 1_500.0 / MORTGAGE_BALANCE_BN}
HOLDER["residual"] = 1.0 - sum(HOLDER.values())
FEDERAL_STUDENT_SHARE = 1605.134 / 1650.0
BANK_SHARE = {"card": min(1187.1 / 1357.2, 1.0), "auto": min(741.1 / 1568.6, 1.0),
              "student": min(741.1 / 1650.0, 1.0)}
FED_LOSSES = {"mortgage": 22.5, "card": 203.0, "auto": 54.1, "student": 54.1}
WB_LEVELS = [0.05, 0.10, 0.25, 0.50, 0.75]
QLABEL = {0: "Q1_bottom", 1: "Q2", 2: "Q3_middle", 3: "Q4", 4: "Q5_top"}
# the target names used by src/wage_targeting.py, all five quintiles
QTARGET = {0: "bottom_Q1", 1: "Q2", 2: "middle_Q3", 3: "Q4", 4: "top_Q5"}


def main():
    cap = json.loads((OUT / "capacities.json").read_text())
    C = cap["sheets"]
    gdp = cap["gdp_bn"]
    Q = pd.read_csv(OUT / "sipp_by_wage_quintile.csv")
    F = pd.read_csv(OUT / "wage_targeted_dose_response.csv")
    A = pd.read_csv(OUT / "cases_A_and_B.csv")
    wt = json.loads((OUT / "wage_targeting_summary.json").read_text())
    total_wb = wt["total_wage_bill_bn"]

    # share of the total wage bill in each quintile, from the ACS run
    shares = {}
    for _, r in F.drop_duplicates("target").iterrows():
        pass
    # recompute quintile wage-bill shares from the SIPP panel's own weights is not
    # comparable; take them from the ACS summary instead
    acs_shares = {0: 0.0324, 1: 0.0895, 2: 0.1426, 3: 0.2233, 4: 0.5122}

    # the case B multiplier on the fiscal loss, averaged across the scenario grid
    caseB_mult = float(A["case_B_over_A"].mean())

    rows = []
    for q in range(5):
        qr = Q[Q.q == q].iloc[0]
        wb_q = acs_shares[q]
        for d in WB_LEVELS:
            f = d / wb_q
            saturated = f > 1.0
            f = min(f, 1.0)
            uplift = f * GHOW_ONE_EARNER
            row = {"wage_quintile": QLABEL[q], "q": q,
                   "dose_share_of_total_wage_bill": d,
                   "delivered_share": f * wb_q, "saturated": saturated,
                   "displaced_fraction_of_quintile": f,
                   "mean_wage": qr["mean_wage"],
                   "median_runway_months": qr["median_runway_months"],
                   "pct_under_1_month": qr["pct_under_1_month"]}
            fed_tot, priv_tot = 0.0, 0.0
            for loan in ["mortgage", "card", "auto", "student"]:
                bal = float(qr[f"{loan}_balance_bn"])
                ead = bal * uplift
                lo, hi = LGD[loan]
                nat_lo, nat_hi = ead * lo, ead * hi
                row[f"{loan}_national_loss_hi_bn"] = nat_hi
                if loan == "mortgage":
                    for h, sh in HOLDER.items():
                        row[f"mortgage_{h}_loss_hi_bn"] = nat_hi * sh
                    fed_tot += nat_hi * (HOLDER["gse"] + HOLDER["fha"])
                    priv_tot += nat_hi * (HOLDER["bank"] + HOLDER["residual"])
                    row["mortgage_bank_pct_of_fed_loss"] = (
                        100 * nat_hi * HOLDER["bank"] / FED_LOSSES["mortgage"])
                elif loan == "student":
                    row["student_federal_loss_hi_bn"] = nat_hi * FEDERAL_STUDENT_SHARE
                    fed_tot += nat_hi * FEDERAL_STUDENT_SHARE
                    priv_tot += nat_hi * (1 - FEDERAL_STUDENT_SHARE)
                else:
                    row[f"{loan}_bank_loss_hi_bn"] = nat_hi * BANK_SHARE[loan]
                    priv_tot += nat_hi * BANK_SHARE[loan]
                    row[f"{loan}_pct_of_fed_loss"] = (
                        100 * nat_hi * BANK_SHARE[loan] / FED_LOSSES[loan])
            # fiscal, from the wage-targeted run where the quintile matches
            ft = F[(F.target == QTARGET[q])
                   & np.isclose(F.dose_share_of_total_wage_bill, d)]
            if len(ft):
                ft = ft.iloc[0]
                row.update({
                    "payroll_tax_loss_bn": ft["payroll_tax_loss_bn"],
                    "OASDI_loss_bn": ft["OASDI_loss_bn"], "HI_loss_bn": ft["HI_loss_bn"],
                    "income_tax_loss_bn": ft["income_tax_loss_bn"],
                    "case_A_fiscal_loss_bn": ft["total_fiscal_loss_bn"],
                    "case_B_fiscal_loss_bn": ft["total_fiscal_loss_bn"] * caseB_mult,
                    "payroll_share_of_fiscal": ft["payroll_share_of_fiscal"]})
                fed_tot += ft["total_fiscal_loss_bn"]
            row["federal_total_loss_hi_bn"] = fed_tot
            row["private_total_loss_hi_bn"] = priv_tot
            row["federal_share"] = fed_tot / max(fed_tot + priv_tot, 1e-9)
            row["federal_pct_of_receipts"] = 100 * fed_tot / C["public_budget"]["capacity_bn"]
            row["private_pct_of_bank_cet1_surplus"] = (
                100 * priv_tot / C["bank_capital"]["capacity_bn"])
            row["total_pct_gdp"] = 100 * (fed_tot + priv_tot) / gdp
            # inside the data: the quintile targeting is a direct reweighting of observed
            # households, so the binding constraint is saturation, not extrapolation
            row["inside_observed_data_range"] = (not saturated) and d <= 0.10
            rows.append(row)
    T = pd.DataFrame(rows)
    T.round(4).to_csv(OUT / "wage_quintile_dose_response.csv", index=False)

    pd.set_option("display.width", 260)
    print("=== ITEM 4: THE DOSE-RESPONSE TABLE ORGANISED BY WAGE QUINTILE ===")
    print(f"  case B multiplier on the fiscal loss, from src/consistency.py: "
          f"{caseB_mult:.3f}")
    print("\n=== WHAT A QUINTILE CAN DELIVER ===")
    for q in range(5):
        print(f"    {QLABEL[q]:10s} holds {acs_shares[q]:6.2%} of the total wage bill, "
              f"so it saturates at a {acs_shares[q]:.2%} dose")

    v = T[~T.saturated]
    print("\n=== FISCAL LOSS BY QUINTILE, billions, case A and case B ===")
    print(v.pivot_table(index="dose_share_of_total_wage_bill", columns="wage_quintile",
                        values=["case_A_fiscal_loss_bn", "case_B_fiscal_loss_bn"]
                        ).round(1).to_string())
    print("\n=== PAYROLL SHARE OF THE FISCAL LOSS, by quintile ===")
    print(v.pivot_table(index="dose_share_of_total_wage_bill", columns="wage_quintile",
                        values="payroll_share_of_fiscal").round(3).to_string())

    print("\n=== HOUSEHOLD CREDIT LOSSES BY QUINTILE, national, billions, upper end ===")
    print(v.pivot_table(index=["wage_quintile", "dose_share_of_total_wage_bill"],
                        values=[f"{l}_national_loss_hi_bn"
                                for l in ["mortgage", "card", "auto", "student"]]
                        ).round(2).to_string())

    print("\n=== WHO BEARS IT, by quintile ===")
    print(v[["wage_quintile", "dose_share_of_total_wage_bill", "federal_total_loss_hi_bn",
             "private_total_loss_hi_bn", "federal_share", "total_pct_gdp",
             "inside_observed_data_range"]].round(3).to_string(index=False))

    print("\n=== BUFFERS, which do not move monotonically with pay ===")
    for q in range(5):
        qr = Q[Q.q == q].iloc[0]
        print(f"    {QLABEL[q]:10s} mean wage {qr['mean_wage']:>10,.0f}   "
              f"median runway {qr['median_runway_months']:.2f} months   "
              f"under one month {qr['pct_under_1_month']:.1f}%")

    (OUT / "wage_quintile_summary.json").write_text(json.dumps({
        "quintile_wage_bill_shares": acs_shares,
        "total_wage_bill_bn": total_wb,
        "case_B_multiplier": caseB_mult,
        "decision": "The dose-response table is organised by wage quintile. Exposure "
                    "indices are named scenarios for where in the distribution "
                    "displacement falls.",
        "cost": ["the embodied versus cognitive framing is demoted to a mapping",
                 "PAEI is a measurement instrument this paper uses, not a finding it "
                 "reports; the driving pathway is its one surviving independent use",
                 "the comparative thesis that the two exposure types stress different "
                 "balance sheets is not supported once pay is controlled"],
        "gain": "the wage quintile is observable in every household survey and every "
                "administrative record, needs no index and no assumption about task "
                "overlap, and is directly usable by a supervisor",
    }, indent=2, default=str))


if __name__ == "__main__":
    main()
