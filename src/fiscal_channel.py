"""Item 6: the fiscal channel, revenue and outlays, per Block 5 correction B.

NOT a wage-bill-to-receipts comparison. That was the error corrected in B.

(a) REVENUE
    (i)   gross labor tax at stake = displaced wage bill x effective labor tax rates,
          separately for federal income tax on wages (SOI-corrected), payroll taxes, and
          state and local income tax (as a range).
    (ii)  net wedge = (tau_labor - tau_capital) x wage income shifted to capital, assuming
          output is preserved.
    (iii) payroll tax at stake against OASDI and HI trust fund income.
    (iv)  consumption second round for state and local, as a labelled rough range.

(b) OUTLAYS, labelled SCENARIO not measurement. Acemoglu and Restrepo (2020, JPE 128(6))
    report in their table A17 that exposure to robots raises take-up of Social Security
    retirement and disability benefits and other government transfers. The online appendix
    is behind the journal paywall and returned HTTP 403, so the magnitudes are NOT used.
    The qualitative direction is cited from the verified main text, and the outlay range is
    built from published program parameters instead.

(c) Net fiscal position per displaced worker and per pathway, under adoption scenarios.

(d) The fiscal tau*s condition, carried into framework/propositions.md.

SOURCES, all verified:
  tau_labor 25.5 percent, tau_capital 10 percent on net capital income, and about 5 percent
    on equipment and software after the 2017 reform: Acemoglu, Manera and Restrepo, "Does
    the US Tax Code Favor Automation?", Brookings Papers on Economic Activity 2020(1),
    231-300. Read from the published PDF, not recalled.
  Wage share of AGI 66.8 percent: IRS SOI Table 1.4, tax year 2023.
  NIPA receipts and wage bill: BEA via FRED.
  Trust fund income 2025: SSA Trustees Report. OASI cost 1,448.8 with income 200.0 below
    cost; DI income 200.5; combined cost exceeded income by 160.2; payroll taxes 91.3
    percent of OASDI income; HI Trust Fund income 462.4.
  Program parameters: SSDI average 1,580 per month (SSA, 2025); SNAP 187.94 per person per
    month (USDA ERS, FY2025); Medicaid 9,255 per enrollee (KFF/MACPAC, FY2023).
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT = ROOT / "data" / "processed"

TAU_LABOR, TAU_CAPITAL, TAU_EQUIP = 0.255, 0.10, 0.05      # AMR 2020, verified
WAGE_SHARE_AGI = 0.668                                      # IRS SOI 2023
OASDI_PAYROLL_INCOME = 1323.2   # 91.3% of 1,449.3 combined OASDI income, 2025
OASDI_TOTAL_INCOME = 1449.3
HI_INCOME = 462.4
SSDI_ANNUAL = 1580.0 * 12
SNAP_ANNUAL_PP = 187.94 * 12
MEDICAID_PER_ENROLLEE = 9255.0


def main():
    w = json.loads((OUT / "legW_us_derived.json").read_text())
    lt = json.loads((OUT / "labor_tax_share.json").read_text())
    meta = json.loads((OUT / "us_series_meta.json").read_text())
    P = pd.read_csv(OUT / "pathway_totals.csv")

    wage_bill = w["wage_bill_usd_bn"]
    fed_pct = w["fed_personal_current_taxes_usd_bn"]
    fed_si = w["fed_social_insurance_contrib_usd_bn"]
    fed_receipts = w["fed_current_receipts_usd_bn"]
    sl_personal = meta.get("W071RC1Q027SBEA", {}).get("value")
    sl_receipts = meta.get("W070RC1Q027SBEA", {}).get("value")

    r_fed_inc = fed_pct * WAGE_SHARE_AGI / wage_bill
    r_payroll = fed_si / wage_bill
    r_sl_hi = (sl_personal * WAGE_SHARE_AGI / wage_bill) if sl_personal else np.nan
    r_sl_lo = 0.5 * r_sl_hi if sl_personal else np.nan   # nine states levy no wage income tax
    r_tot_lo = r_fed_inc + r_payroll + r_sl_lo
    r_tot_hi = r_fed_inc + r_payroll + r_sl_hi

    rates = {
        "federal_income_tax_on_wages": r_fed_inc,
        "federal_payroll": r_payroll,
        "state_local_income_low": r_sl_lo, "state_local_income_high": r_sl_hi,
        "total_effective_labor_tax_low": r_tot_lo,
        "total_effective_labor_tax_high": r_tot_hi,
        "AMR_tau_labor_benchmark": TAU_LABOR,
        "note": ("our bottom-up effective labor tax rate is reported alongside AMR's 25.5 "
                 "percent; they differ because AMR include the employer side and a marginal "
                 "rather than average concept"),
    }
    print("=== Effective labor tax rates (share of the wage bill) ===")
    for k, v in rates.items():
        if isinstance(v, float):
            print(f"  {k:36s} {100*v:6.2f}%")
    print(f"  AMR published benchmark               {100*TAU_LABOR:6.2f}%")

    # ---------------- (d) the fiscal tau*s condition ----------------
    # Displacing dW of wage bill removes tau_l * dW of labour tax and adds g * dW of outlays.
    # The automation generates additional taxable surplus s * dW, taxed at tau_k.
    # Government is whole iff  tau_k * s >= tau_l + g, i.e.  s >= (tau_l + g) / tau_k.
    cond = {}
    for gname, gval in [("g = 0 (no added outlays)", 0.0),
                        ("g = 0.10", 0.10), ("g = 0.25", 0.25)]:
        cond[gname] = {
            "s_required_at_tau_k_10pct": (TAU_LABOR + gval) / TAU_CAPITAL,
            "s_required_at_tau_k_5pct_equipment": (TAU_LABOR + gval) / TAU_EQUIP,
        }
    print("\n=== (d) FISCAL tau*s CONDITION: s >= (tau_l + g) / tau_k ===")
    print("    s is additional taxable surplus per dollar of displaced wage bill")
    for k, v in cond.items():
        print(f"  {k:26s} s >= {v['s_required_at_tau_k_10pct']:5.2f} (capital at 10%), "
              f"{v['s_required_at_tau_k_5pct_equipment']:5.2f} (equipment at 5%)")

    # ---------------- adoption scenarios (correction C) ----------------
    scen = []
    for _, r in P.iterrows():
        W = r["wage_bill_usd_bn"]
        for d in (0.10, 0.25, 0.50):
            for H in (10, 20):
                dW_total = W * d
                dW_annual = dW_total / H          # linear ramp, annual increment
                scen.append({"pathway": r["pathway"], "displacement": d, "horizon_yr": H,
                             "wage_bill_usd_bn": W,
                             "displaced_wage_bill_total_usd_bn": dW_total,
                             "displaced_wage_bill_annual_usd_bn": dW_annual})
    S = pd.DataFrame(scen)

    # revenue at stake, on the TOTAL displaced wage bill at the end of the horizon
    S["gross_labor_tax_lo_usd_bn"] = S["displaced_wage_bill_total_usd_bn"] * r_tot_lo
    S["gross_labor_tax_hi_usd_bn"] = S["displaced_wage_bill_total_usd_bn"] * r_tot_hi
    S["payroll_at_stake_usd_bn"] = S["displaced_wage_bill_total_usd_bn"] * r_payroll
    S["net_wedge_capital10_usd_bn"] = S["displaced_wage_bill_total_usd_bn"] * (TAU_LABOR - TAU_CAPITAL)
    S["net_wedge_equip5_usd_bn"] = S["displaced_wage_bill_total_usd_bn"] * (TAU_LABOR - TAU_EQUIP)
    S["pct_federal_receipts"] = 100 * S["gross_labor_tax_hi_usd_bn"] / fed_receipts
    S["payroll_pct_OASDI_payroll_income"] = 100 * S["payroll_at_stake_usd_bn"] / OASDI_PAYROLL_INCOME
    S["payroll_pct_HI_income"] = 100 * S["payroll_at_stake_usd_bn"] / HI_INCOME
    # consumption second round, labelled rough
    S["consumption_2nd_round_lo_usd_bn"] = S["displaced_wage_bill_total_usd_bn"] * 0.80 * 0.04
    S["consumption_2nd_round_hi_usd_bn"] = S["displaced_wage_bill_total_usd_bn"] * 0.80 * 0.06

    # ---------------- outlays, per displaced worker-year ----------------
    emp = {"driving": 6037238, "gated": 44488304, "manipulation": 29469580}
    meanwage = {p: P.loc[P["pathway"] == p, "wage_bill_usd_bn"].iloc[0] * 1e9 / emp[p]
                for p in emp}
    outlay = {}
    for p, mw in meanwage.items():
        ui_hi = 0.5 * mw * 0.5           # 50 percent replacement for 26 weeks, first year
        lo = 0.0
        hi = ui_hi + 1.5 * SNAP_ANNUAL_PP + MEDICAID_PER_ENROLLEE + 0.10 * SSDI_ANNUAL
        outlay[p] = {"mean_annual_wage_usd": mw,
                     "outlay_per_displaced_worker_low_usd": lo,
                     "outlay_per_displaced_worker_high_usd": hi,
                     "components_high": {
                         "UI_50pct_26wks": ui_hi,
                         "SNAP_1.5_persons": 1.5 * SNAP_ANNUAL_PP,
                         "Medicaid_1_enrollee": MEDICAID_PER_ENROLLEE,
                         "SSDI_10pct_take_up": 0.10 * SSDI_ANNUAL}}
    S["displaced_workers"] = S.apply(
        lambda r: r["displaced_wage_bill_total_usd_bn"] * 1e9 / meanwage[r["pathway"]], axis=1)
    S["outlays_hi_usd_bn"] = S.apply(
        lambda r: r["displaced_workers"] * outlay[r["pathway"]]["outlay_per_displaced_worker_high_usd"] / 1e9,
        axis=1)
    S["net_fiscal_hi_usd_bn"] = S["gross_labor_tax_hi_usd_bn"] + S["outlays_hi_usd_bn"]
    S["net_fiscal_per_displaced_worker_usd"] = (
        S["net_fiscal_hi_usd_bn"] * 1e9 / S["displaced_workers"].replace(0, np.nan))
    S.round(3).to_csv(OUT / "fiscal_channel_scenarios.csv", index=False)

    (OUT / "fiscal_channel_summary.json").write_text(json.dumps({
        "rates": rates, "tau_s_condition": cond, "outlay_assumptions": outlay,
        "trust_funds": {"OASDI_payroll_income_usd_bn": OASDI_PAYROLL_INCOME,
                        "OASDI_total_income_usd_bn": OASDI_TOTAL_INCOME,
                        "HI_income_usd_bn": HI_INCOME},
        "denominators": {"federal_current_receipts_usd_bn": fed_receipts,
                         "state_local_current_receipts_usd_bn": sl_receipts,
                         "wage_bill_usd_bn": wage_bill},
    }, indent=2, default=str))

    pd.set_option("display.width", 240)
    print("\n=== Revenue at stake, 25 percent displacement (total, not annual) ===")
    v = S[np.isclose(S["displacement"], 0.25) & (S["horizon_yr"] == 10)]
    print(v[["pathway", "displaced_wage_bill_total_usd_bn", "gross_labor_tax_lo_usd_bn",
             "gross_labor_tax_hi_usd_bn", "net_wedge_capital10_usd_bn",
             "payroll_at_stake_usd_bn", "payroll_pct_OASDI_payroll_income",
             "pct_federal_receipts"]].round(2).to_string(index=False))
    print("\n=== Outlays and net fiscal position, 25 percent displacement ===")
    print(v[["pathway", "displaced_workers", "outlays_hi_usd_bn", "net_fiscal_hi_usd_bn",
             "net_fiscal_per_displaced_worker_usd"]].round(1).to_string(index=False))
    print("\n=== Outlay assumptions per displaced worker-year (SCENARIO) ===")
    for p, o in outlay.items():
        print(f"  {p:14s} mean wage ${o['mean_annual_wage_usd']:>9,.0f}  "
              f"outlay range $0 to ${o['outlay_per_displaced_worker_high_usd']:>9,.0f}")


if __name__ == "__main__":
    main()
