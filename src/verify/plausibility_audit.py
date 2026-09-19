"""Item 0: the plausibility rule, applied retroactively to every headline number.

THE RULE, standing from now on. Before any headline number is reported, state in one line the
physical or accounting bound it must respect, and confirm it does. A share cannot exceed 100
percent. A loss on a tax cannot exceed the tax. A bank loss cannot exceed the bank-held
balance. A subset cannot exceed its total.

This script walks the processed outputs and checks each headline against its bound. It is
deliberately mechanical: every check names the bound, the value, and the verdict.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[2]
OUT = ROOT / "data" / "processed"
CHECKS = []


def chk(name, value, bound_desc, ok, detail=""):
    CHECKS.append({"quantity": name, "value": value, "bound": bound_desc,
                   "verdict": "OK" if ok else "VIOLATION", "detail": detail})


def main():
    # ---- 0. the CORRECTED trust fund ratios (A79) supersede the A77 ones ----
    try:
        tf = pd.read_csv(OUT / "trust_fund_corrected.csv")
        for col, lab in [("OASDI_loss_pct_of_fund_payroll_income", "OASDI"),
                         ("HI_loss_pct_of_fund_payroll_income", "HI")]:
            mx = float(tf[col].max())
            chk(f"CORRECTED {lab} loss as percent of that fund's payroll income", mx,
                "a loss on a payroll tax cannot exceed that tax base: 0 to 100 percent",
                mx <= 100.0, "rebuilt in A79 with the OASDI cap and a payroll numerator")
        bm = pd.read_csv(OUT / "credit_benchmarked.csv")
        mxb = float(bm["bank_share"].max())
        chk("CORRECTED implied bank share after benchmarking", mxb,
            "a subset cannot exceed its total: 0 to 1", mxb <= 1.0,
            "survey balances scaled to official aggregates in A79")
    except FileNotFoundError:
        pass

    # ---- 1. fiscal loss against OASDI and HI payroll income (SUPERSEDED, kept to show the
    #         violation the rule caught) ----
    fx = pd.read_csv(OUT / "fiscal_extended_axis.csv")
    b = fx[(fx.tau_l == "bottom_up_0.301") & (fx.outlays == "no_outlays")
           & (fx.tau_k_reading == "barkai_rent_0.351") & (fx.rho_mode == "fitted")
           & (fx.horizon == 10)]
    for col, lab in [("terminal_pct_OASDI", "OASDI payroll income"),
                     ("terminal_pct_HI", "HI Part A revenue")]:
        mx = float(b[col].max())
        chk(f"terminal fiscal loss as percent of {lab}", mx,
            "a loss on a payroll tax cannot exceed that tax base: 0 to 100 percent",
            mx <= 100.0,
            f"maximum across the extended axis at the ten-year horizon")
    mxr = float(b["terminal_pct_receipts"].max())
    # labour-linked share of federal receipts, corrected in A8
    LABOUR_LINKED = 0.65
    chk("terminal fiscal loss as percent of federal receipts", mxr,
        f"cannot exceed the labour-linked share of receipts, about "
        f"{LABOUR_LINKED:.0%}, so 0 to {100*LABOUR_LINKED:.0f} percent",
        mxr <= 100 * LABOUR_LINKED,
        "a displacement shock removes labour-linked revenue, not capital or excise revenue")

    # ---- 2. rho and R ----
    chk("rho on the extended axis", float(b["rho"].min()),
        "a reemployment share is a probability: 0 to 1", 0.0 <= float(b["rho"].min()) <= 1.0)
    chk("R = rho x omega", float(b["R"].max()),
        "a retained wage share is 0 to 1 unless reemployment raises wages",
        float(b["R"].max()) <= 1.0)

    # ---- 3. credit: bank share implied by SIPP against the national balance ----
    hc = pd.read_csv(OUT / "verify" / "hand_check_credit.csv")
    for loan in hc["loan"].unique():
        s = hc[hc.loan == loan].iloc[0]
        chk(f"implied bank share of {loan} balances", float(s["bank_share_implied"]),
            "a subset cannot exceed its total: 0 to 1",
            float(s["bank_share_implied"]) <= 1.0,
            "above 1 means the survey under-reports that balance relative to the aggregate")

    # ---- 4. credit losses against the balance they sit on ----
    for _, s in hc.iterrows():
        if s["total_balance_bn"] <= 0:
            continue
        ratio = s["loss_hi_bn"] / s["total_balance_bn"]
        chk(f"{s['loan']} loss at {s['share_of_wage_bill']:.0%} of wage bill, "
            f"as a share of the national balance", float(ratio),
            "a loss cannot exceed the balance it sits on: 0 to 1", ratio <= 1.0)

    # ---- 5. displacement shares ----
    ax = pd.read_csv(OUT / "scenario_axis_levels.csv")
    mx = float(ax["share_of_TOTAL_wage_bill"].max())
    chk("maximum share of the total wage bill displaced", mx,
        "a share of the wage bill is 0 to 1", mx <= 1.0)

    # ---- 6. nonemployment ----
    mx = float(b["nonemployment_terminal"].max())
    chk("terminal prime-age nonemployment", mx,
        "a nonemployment rate is 0 to 100 percent", mx <= 100.0)

    # ---- 7. stock-flow outcome shares ----
    try:
        sf = pd.read_csv(OUT / "stock_flow_v3_grid.csv")
        for col, lab, hi in [("unemployment", "unemployment rate", 1.0),
                             ("ep_ratio", "prime-age E/P ratio, percent", 100.0)]:
            m = float(sf[col].max())
            chk(f"stock-flow {lab}", m, f"0 to {hi}", m <= hi)
    except FileNotFoundError:
        pass

    A = pd.DataFrame(CHECKS)
    OUTD = OUT / "verify"; OUTD.mkdir(parents=True, exist_ok=True)
    A.to_csv(OUTD / "plausibility_audit.csv", index=False)
    pd.set_option("display.width", 260)
    pd.set_option("display.max_colwidth", 70)

    v = A[A.verdict == "VIOLATION"]
    print("=== PLAUSIBILITY AUDIT ===")
    print(f"  {len(A)} checks, {len(v)} VIOLATIONS\n")
    if len(v):
        print("=== VIOLATIONS, reported first ===")
        print(v[["quantity", "value", "bound"]].to_string(index=False))
    print("\n=== ALL CHECKS ===")
    print(A[["quantity", "value", "verdict"]].to_string(index=False))
    (OUTD / "plausibility_audit.json").write_text(
        json.dumps({"n_checks": len(A), "n_violations": len(v),
                    "checks": CHECKS}, indent=2, default=str))


if __name__ == "__main__":
    main()
