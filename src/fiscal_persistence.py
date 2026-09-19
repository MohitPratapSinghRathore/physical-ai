"""Item 1: the fiscal loss treated as a STOCK, correcting A70.

HOW A70 GOT IT WRONG. `src/fiscal_magnitudes.py` computed

    cumulative loss = displaced wage bill x loss per dollar
    annual loss     = cumulative loss / horizon

That treats the revenue loss as a one-time flow spread over the horizon. It is not. Once a
worker is displaced and not fully reemployed, the revenue they no longer generate is missing
in EVERY subsequent year. The loss is a stock that accrues, not a flow to be amortised.

THE CORRECT TREATMENT

    annual loss in year t = (loss per displaced wage dollar) x (CUMULATIVE displaced wage
                            bill at t)

With displacement arriving evenly over H years to a cumulative total D:

    cumulative displaced wage bill at t   = D * t / H
    annual loss at t                      = k * D * t / H
    TERMINAL-YEAR annual loss             = k * D              <- identical for all H
    average annual loss over the horizon  = k * D * (H + 1) / (2H)
    cumulative loss over the horizon      = k * D * (H + 1) / 2
    present value at rate r               = sum over t of k*D*(t/H) / (1+r)^t

WHAT THIS OVERTURNS. **A70's "thirty-fold" statement is WITHDRAWN.** A70 said that 90 percent
of both exposure types costs 42.4 percent of federal receipts a year over two years and 1.34
percent over twenty, and called that a thirty-fold difference for the same cumulative
displacement. On the correct treatment the terminal-year annual loss is IDENTICAL for the
same cumulative displacement regardless of horizon, because the same wage bill is missing
either way. What differs is the PATH and the CUMULATIVE total, and the cumulative total is
LARGER for the longer horizon, not smaller, because the loss accrues for more years.

The speed result in A56 stands on its own terms: speed drives the LABOUR MARKET channel,
through slack and reemployment. It does not drive the fiscal channel the way A70 implied.

TWO R TREATMENTS, both reported.

    R_terminal   R held at its terminal value for every year of the path. Simple, and it
                 OVERSTATES the early-year loss, because R starts at its 2026 value of
                 0.5683 and only deteriorates as displacement accumulates.
    R_pathed     R interpolated linearly from the 2026 baseline to the terminal value over
                 the horizon, so year t carries R(t) = R0 + (R_term - R0) * t / H. This is
                 an approximation to a full year-by-year solve and is labelled as one; it
                 captures the direction and most of the magnitude of the difference.

R held at terminal value throughout the path. R deteriorates as slack rises, so using
the terminal value overstates the early-year loss and understates nothing. Stated rather than
hidden; a full treatment would path R year by year.
"""
import json, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).parents[1]
OUT, RAW = ROOT / "data" / "processed", ROOT / "data" / "raw"

TAU_L = {"AMR_0.255": 0.255, "bottom_up_0.301": 0.301, "bottom_up_0.318": 0.318}
TAU_K_READINGS = {"barkai_rent_0.351": 0.0708, "KN_caseR_rent_0.00": 0.0500}
G_CASES = {"no_outlays": 0.0, "modest_0.10": 0.10, "full_0.25": 0.25}
DISCOUNT = 0.03
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
    receipts, rdate = fred_last("FGRECPT")
    comp, cdate = fred_last("COE")
    F = pd.read_csv(OUT / "frontier_grid.csv")
    F = F[F.phi == 0.5].copy()

    rows = []
    for _, r in F.iterrows():
        H = int(r["horizon"])
        D = comp * r["total_displacement_of_employment"]     # cumulative displaced wage bill
        R = r["R_terminal_switcher_compounded"]
        rho_t = r["rho_terminal"]
        for tkname, tk in TAU_K_READINGS.items():
            for lname, tl in TAU_L.items():
                for gname, g in G_CASES.items():
                    k = tl * (1 - R) - tk * 1.0 + g * (1 - rho_t)
                    terminal = k * D
                    avg = k * D * (H + 1) / (2 * H)
                    cum = k * D * (H + 1) / 2
                    pv = sum((k * D * (t / H)) / (1 + DISCOUNT) ** t
                             for t in range(1, H + 1))
                    # R pathed: R deteriorates from the 2026 baseline to the terminal value
                    R0 = 0.5683
                    cum_p, pv_p = 0.0, 0.0
                    for tt in range(1, H + 1):
                        R_t = R0 + (R - R0) * tt / H
                        k_t = tl * (1 - R_t) - tk * 1.0 + g * (1 - rho_t)
                        yr = k_t * D * (tt / H)
                        cum_p += yr
                        pv_p += yr / (1 + DISCOUNT) ** tt
                    k_term_p = tl * (1 - R) - tk * 1.0 + g * (1 - rho_t)
                    rows.append({
                        "type": r["type"], "level_of_exposed": r["level_of_exposed"],
                        "horizon": H, "tau_k_reading": tkname, "tau_l": lname,
                        "outlays": gname,
                        "cumulative_displaced_wage_bill_bn": D,
                        "loss_per_dollar": k,
                        "terminal_year_annual_loss_bn": terminal,
                        "average_annual_loss_bn": avg,
                        "cumulative_loss_bn": cum,
                        "present_value_bn": pv,
                        "cumulative_loss_bn_R_pathed": cum_p,
                        "present_value_bn_R_pathed": pv_p,
                        "R_path_effect_pct": 100 * (cum_p - cum) / cum if cum else 0.0,
                        "terminal_pct_federal_receipts": 100 * terminal / receipts,
                        "average_pct_federal_receipts": 100 * avg / receipts,
                        "terminal_pct_OASDI_payroll": 100 * terminal / OASDI_PAYROLL_INCOME_BN,
                        "terminal_pct_HI_revenue": 100 * terminal / HI_PART_A_REVENUE_BN})
    M = pd.DataFrame(rows)
    M.round(4).to_csv(OUT / "fiscal_persistence.csv", index=False)

    pd.set_option("display.width", 250)
    print(f"=== denominators: federal receipts {receipts:,.1f}bn ({rdate}), "
          f"compensation {comp:,.1f}bn ({cdate}), discount {DISCOUNT:.0%} ===")

    base = M[(M.tau_l == "bottom_up_0.301") & (M.outlays == "no_outlays")
             & (M.tau_k_reading == "barkai_rent_0.351")]

    MOD = [0.10, 0.25, 0.50]
    print("\n=== LEAD: MODERATE SCENARIOS. Terminal-year annual loss, "
          "percent of federal receipts ===")
    print("    10, 25 and 50 percent of the exposed wage bill. tau_l 0.301, no outlays, "
          "Barkai reading.")
    m = base[base.level_of_exposed.isin(MOD)]
    print(m.pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                        values="terminal_pct_federal_receipts").round(2).to_string())
    print("\n    as a percent of OASDI payroll income:")
    print(m.pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                        values="terminal_pct_OASDI_payroll").round(2).to_string())
    print("\n    as a percent of HI Part A revenue:")
    print(m.pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                        values="terminal_pct_HI_revenue").round(1).to_string())

    print("\n=== the 90 percent case, reported AFTER the moderate ones ===")
    print(base[base.level_of_exposed == 0.90].pivot_table(
        index="type", columns="horizon",
        values="terminal_pct_federal_receipts").round(2).to_string())

    print("\n=== R PATHED against R held at terminal, effect on cumulative loss ===")
    print(base[base.level_of_exposed.isin(MOD)].pivot_table(
        index=["type", "level_of_exposed"], columns="horizon",
        values="R_path_effect_pct").round(1).to_string())
    print("    percent difference; negative means holding R at terminal OVERSTATES the loss")

    print("\n=== what A70 reported instead (cumulative divided by horizon) ===")
    try:
        old = pd.read_csv(OUT / "fiscal_magnitudes.csv")
        o = old[(old.tau_l == "bottom_up_0.301") & (old.outlays == "no_outlays")
                & (old.tau_k_reading == "barkai_rent_0.351")]
        print(o.pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                            values="annual_pct_federal_receipts").round(2).to_string())
    except FileNotFoundError:
        pass

    print("\n=== CUMULATIVE loss over the horizon, USD bn (now RISES with horizon) ===")
    print(base.pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                           values="cumulative_loss_bn").round(0).to_string())

    print("\n=== PRESENT VALUE at 3 percent, USD bn ===")
    print(base.pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                           values="present_value_bn").round(0).to_string())

    print("\n=== terminal-year loss as a percent of OASDI payroll income ===")
    print(base.pivot_table(index=["type", "level_of_exposed"], columns="horizon",
                           values="terminal_pct_OASDI_payroll").round(1).to_string())

    print("\n=== outlays, stated separately: cognitive AIOE 50 percent, 10 years ===")
    y = M[(M.type == "cognitive_AIOE") & (M.level_of_exposed == 0.50) & (M.horizon == 10)
          & (M.tau_k_reading == "barkai_rent_0.351")]
    print(y.pivot_table(index="tau_l", columns="outlays",
                        values="terminal_pct_federal_receipts").round(2).to_string())

    print("\n=== rent-share reading, terminal-year loss, 50 percent over 10 years ===")
    z = M[(M.level_of_exposed == 0.50) & (M.horizon == 10) & (M.outlays == "no_outlays")
          & (M.tau_l == "bottom_up_0.301")]
    print(z.pivot_table(index="type", columns="tau_k_reading",
                        values="terminal_year_annual_loss_bn").round(1).to_string())

    # is the terminal loss really horizon-invariant?
    chk = base.groupby(["type", "level_of_exposed"])["terminal_pct_federal_receipts"].agg(
        ["min", "max"])
    chk["spread"] = chk["max"] - chk["min"]
    print(f"\n=== invariance check: max spread of the terminal-year loss across horizons "
          f"= {chk['spread'].max():.3f} percentage points ===")
    print("  (not exactly zero because R and rho differ by horizon through the labour model)")

    (OUT / "fiscal_persistence_summary.json").write_text(json.dumps({
        "correction": "A70 amortised a stock as a flow. Terminal-year annual loss is "
                      "horizon-invariant for the same cumulative displacement; cumulative "
                      "loss RISES with horizon.",
        "thirty_fold_statement": "WITHDRAWN",
        "discount_rate": DISCOUNT,
        "federal_receipts_bn": receipts, "compensation_bn": comp,
        "terminal_pct_receipts_range": [float(M.terminal_pct_federal_receipts.min()),
                                        float(M.terminal_pct_federal_receipts.max())],
        "cumulative_bn_range": [float(M.cumulative_loss_bn.min()),
                                float(M.cumulative_loss_bn.max())],
        "pv_bn_range": [float(M.present_value_bn.min()), float(M.present_value_bn.max())],
        "R_held_at_terminal_value": True,
    }, indent=2))


if __name__ == "__main__":
    main()
