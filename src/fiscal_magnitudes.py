"""A2: the size-driven fiscal loss in magnitudes, not in pass or fail language.

THE CONDITION ALREADY FAILS AT ZERO DISPLACEMENT. A57, A58 and A60 established that the P1r
condition is unmet in 2026 before any AI displacement: available tau_k is 0.0708 with profit
shifting against a required 0.1101 at the lowest labour tax rate, and no post-2017 cell
passes under any sourced combination. **Nothing in this module is a test of whether the
condition holds. It holds nowhere. This is a measurement of how large the revenue loss is.**

IDENTICAL ACROSS INCIDENCE CASES BY CONSTRUCTION, and this is worth stating rather than
discovering. The fiscal loss depends on the displaced wage bill and the retained wage share
R. A dollar of wage income not earned costs the same revenue whether the person who would
have earned it was laid off or was never hired. A1 showed the incidence cases differ sharply
in WHERE the credit losses land; they do not differ at all here.

THE ARITHMETIC

    revenue loss per dollar of displaced wage bill = tau_l * (1 - R) - tau_k * s

with s the additional taxable surplus per dollar displaced, capped at 1 by construction, and
R = rho * omega the retained wage share. With outlays g paid to the non-reemployed share,
add g * (1 - rho).

Denominators, all from the repository's existing FRED pulls with units read from the
provider: federal current receipts (FGRECPT), OASDI trust fund income and HI income from the
A32 working.

BOTH READINGS OF THE RENT-SHARE DISAGREEMENT are carried through, because A57 established
that Barkai and Karabarbounis-Neiman are not endpoints of an interval but incompatible
readings of one residual.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"

TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}
TAU_K_READINGS = {"barkai_rent_0.351": 0.0708, "KN_caseR_rent_0.00": 0.0500}
G_CASES = {"no_outlays": 0.0, "modest_0.10": 0.10, "full_0.25": 0.25}
# A32, verified in the repository
OASDI_PAYROLL_INCOME_BN = 1323.2
HI_PART_A_REVENUE_BN = 462.4


def fred_last(series):
    p = RAW / "fred" / f"{series}.csv"
    if not p.exists():
        import requests
        r = requests.get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series}",
                         timeout=90)
        r.raise_for_status()
        p.write_bytes(r.content)
    d = pd.read_csv(p)
    d.columns = ["date", "v"]
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    d = d.dropna()
    return float(d["v"].iloc[-1]), str(d["date"].iloc[-1])


def main():
    receipts, rdate = fred_last("FGRECPT")     # federal current receipts, USD bn
    comp, cdate = fred_last("COE")             # compensation of employees, USD bn
    rws = json.loads((OUT / "retained_wage_share_summary.json").read_text())
    rho0 = rws["rho_2026"]

    F = pd.read_csv(OUT / "frontier_grid.csv")
    F = F[F.phi == 0.5].copy()

    rows = []
    for _, r in F.iterrows():
        disp_share = r["total_displacement_of_employment"]
        wage_bill_displaced = comp * disp_share
        R = r["R_terminal_switcher_compounded"]
        rho_t = r["rho_terminal"]
        for tkname, tk in TAU_K_READINGS.items():
            for lname, tl in TAU_L.items():
                for gname, g in G_CASES.items():
                    per_dollar = tl * (1 - R) - tk * 1.0 + g * (1 - rho_t)
                    cum = wage_bill_displaced * per_dollar
                    ann = cum / r["horizon"]
                    rows.append({
                        "type": r["type"], "level_of_exposed": r["level_of_exposed"],
                        "horizon": r["horizon"], "tau_k_reading": tkname, "tau_l": lname,
                        "outlays": gname,
                        "displaced_wage_bill_bn": wage_bill_displaced,
                        "loss_per_dollar": per_dollar,
                        "cumulative_loss_bn": cum, "annual_loss_bn": ann,
                        "annual_pct_federal_receipts": 100 * ann / receipts,
                        "cumulative_pct_federal_receipts": 100 * cum / receipts,
                        "annual_pct_OASDI_payroll_income": 100 * ann / OASDI_PAYROLL_INCOME_BN,
                        "annual_pct_HI_revenue": 100 * ann / HI_PART_A_REVENUE_BN})
    M = pd.DataFrame(rows)
    M.round(4).to_csv(OUT / "fiscal_magnitudes.csv", index=False)

    pd.set_option("display.width", 250)
    print(f"=== denominators ===")
    print(f"  federal current receipts  {receipts:,.1f} bn  ({rdate})")
    print(f"  compensation of employees {comp:,.1f} bn  ({cdate})")
    print(f"  OASDI payroll income      {OASDI_PAYROLL_INCOME_BN:,.1f} bn  (A32)")
    print(f"  HI Part A revenue         {HI_PART_A_REVENUE_BN:,.1f} bn  (A32)")

    print("\n=== ANNUAL revenue loss as a percent of federal receipts ===")
    print("    tau_l 0.301, no outlays, Barkai reading, phi 0.5")
    s = M[(M.tau_l == "bottom_up_0.301") & (M.outlays == "no_outlays")
          & (M.tau_k_reading == "barkai_rent_0.351")]
    print(s.pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                        values="annual_pct_federal_receipts").round(2).to_string())

    print("\n=== the same, as a percent of OASDI payroll income ===")
    print(s.pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                        values="annual_pct_OASDI_payroll_income").round(2).to_string())

    print("\n=== effect of the rent-share disagreement on the ANNUAL loss, "
          "both types, 50 percent of exposed over 10 years ===")
    z = M[(M.level_of_exposed == 0.50) & (M.horizon == 10)
          & (M.outlays == "no_outlays") & (M.tau_l == "bottom_up_0.301")]
    print(z.pivot_table(index="type", columns="tau_k_reading",
                        values="annual_loss_bn").round(1).to_string())

    print("\n=== effect of OUTLAYS, cognitive AIOE, 50 percent over 10 years ===")
    y = M[(M.type == "cognitive_AIOE") & (M.level_of_exposed == 0.50)
          & (M.horizon == 10) & (M.tau_k_reading == "barkai_rent_0.351")]
    print(y.pivot_table(index="tau_l", columns="outlays",
                        values="annual_pct_federal_receipts").round(2).to_string())

    print("\n=== RANGE across everything ===")
    print(f"  annual loss as a share of federal receipts: "
          f"{M.annual_pct_federal_receipts.min():.2f}% to "
          f"{M.annual_pct_federal_receipts.max():.2f}%")
    print(f"  cumulative loss, USD bn: {M.cumulative_loss_bn.min():,.0f} to "
          f"{M.cumulative_loss_bn.max():,.0f}")

    (OUT / "fiscal_magnitudes_summary.json").write_text(json.dumps({
        "federal_receipts_bn": receipts, "receipts_date": rdate,
        "compensation_bn": comp, "compensation_date": cdate,
        "oasdi_payroll_income_bn": OASDI_PAYROLL_INCOME_BN,
        "hi_revenue_bn": HI_PART_A_REVENUE_BN,
        "identical_across_incidence_cases": True,
        "why": "The fiscal loss depends on the displaced wage bill and the retained wage "
               "share. A dollar of wage income not earned costs the same revenue whether "
               "the person was laid off or never hired.",
        "condition_already_fails_at_zero_displacement": True,
        "annual_pct_receipts_range": [float(M.annual_pct_federal_receipts.min()),
                                      float(M.annual_pct_federal_receipts.max())],
    }, indent=2))


if __name__ == "__main__":
    main()
