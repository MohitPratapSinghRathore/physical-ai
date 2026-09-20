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
        chk(f"SUPERSEDED A77 terminal fiscal loss as percent of {lab}", mx,
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
        chk(f"SUPERSEDED A79 implied bank share of {loan} balances",
            float(s["bank_share_implied"]),
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

    # ---- 6b. the break-even capital tax rate (item 1 of the replication-repair session).
    #      The replicator found the sealed case A maximum of 0.378371 above the highest
    #      reading of tau_l, which tau_l * (1 - R) makes impossible. The bounds were missing
    #      from this audit as well as from the brief. They are now carried in
    #      src/consistency.py and folded in here so they run with every other check. ----
    try:
        be = pd.read_csv(OUT / "break_even_bounds.csv")
        for _, s in be.iterrows():
            chk(s["quantity"], float(s["value"]), s["bound"],
                s["verdict"] == "OK", str(s.get("detail", "")))
    except FileNotFoundError:
        pass

    # ---- 7. stock-flow outcome shares ----
    try:
        sf = pd.read_csv(OUT / "stock_flow_v3_grid.csv")
        for col, lab, hi in [("unemployment", "unemployment rate", 1.0),
                             ("ep_ratio", "prime-age E/P ratio, percent", 100.0)]:
            m = float(sf[col].max())
            chk(f"stock-flow {lab}", m, f"0 to {hi}", m <= hi)
    except FileNotFoundError:
        pass

    # ---- rho in [0, 1]. ADDED in the final analysis session, item 2. The independent
    # replicator found that the section 3a fixed-point construction returns rho = 4.39 at
    # the headline embodied dose, which is not a rate, and that no bound in this audit
    # covered it. The bound is now enforced in src/rho_bounded.py and checked here on both
    # the superseded and the bounded extended axis, so the fix stays fixed.
    try:
        import numpy as _np
        for fn, lab in [("fiscal_extended_axis.csv", "superseded extended axis"),
                        ("fiscal_extended_axis_bounded.csv", "bounded extended axis"),
                        ("rho_bounded_axis.csv", "bounded scenario axis"),
                        ("rho_bounded_dose_grid.csv", "bounded dose grid")]:
            f = OUT / fn
            if not f.exists():
                continue
            d = pd.read_csv(f)
            for col in ("rho", "rho_clamped", "rho_band_lo", "rho_band_hi"):
                if col not in d.columns:
                    continue
                v = pd.to_numeric(d[col], errors="coerce").dropna()
                if not len(v):
                    continue
                worst = float(v.min()) if abs(v.min() - 0.5) > abs(v.max() - 0.5)                     else float(v.max())
                chk(f"rho, {lab}, {col}", worst, "rho in [0, 1], it is a rate",
                    bool((v >= 0.0).all() and (v <= 1.0).all()),
                    f"{len(v)} values, min {v.min():.4f}, max {v.max():.4f}")
            # the raw fixed point is expected to BREACH the bound past the pole. That is
            # the finding, so it is recorded as a diagnostic rather than as a violation.
            if "rho_fixed_point_raw" in d.columns:
                v = pd.to_numeric(d["rho_fixed_point_raw"], errors="coerce").dropna()
                bad = int(((v < 0.0) | (v > 1.0)).sum())
                chk(f"rho raw fixed point, {lab}, DIAGNOSTIC",
                    bad, "breaches expected past the pole, must be caught and banded",
                    True, f"{bad} of {len(v)} raw values outside [0, 1]")
    except Exception as e:
        chk("rho in [0, 1]", str(e), "rho in [0, 1]", False, "audit could not run")

    # ---- the debt-only labour backing ratio, added this session. A share must lie in
    # [0, 1], and the debt-only denominator must be SMALLER than the all-claims one.
    try:
        f = ROOT / "framework" / "labor_backing" / "debt_only_ratio_timeseries.csv"
        if f.exists():
            d = pd.read_csv(f)
            for col in ["DEBT_ONLY_ratio_direct", "DEBT_ONLY_ratio_incl_indirect",
                        "all_claims_ratio_direct", "equity_share_of_all_claims"]:
                v = pd.to_numeric(d[col], errors="coerce").dropna()
                chk(f"{col} in [0, 1]", float(v.max()), "a share: 0 to 1",
                    bool((v >= 0).all() and (v <= 1).all()),
                    f"{len(v)} years, min {v.min():.4f}, max {v.max():.4f}")
            ok = bool((d.total_debt_only_bn <= d.total_all_claims_bn).all())
            chk("debt-only denominator <= all-claims denominator",
                float((d.total_debt_only_bn / d.total_all_claims_bn).max()),
                "excluding equity cannot enlarge the denominator", ok)
            chk("debt-only ratio >= all-claims ratio",
                float((d.DEBT_ONLY_ratio_direct - d.all_claims_ratio_direct).min()),
                "removing an unbacked class from the denominator must RAISE the ratio",
                bool((d.DEBT_ONLY_ratio_direct >= d.all_claims_ratio_direct).all()))
    except Exception as e:
        chk("debt-only ratio bounds", str(e), "share in [0, 1]", False, "audit failed")

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
